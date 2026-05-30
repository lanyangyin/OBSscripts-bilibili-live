"""用于记录日志"""
from datetime import datetime
from pathlib import Path
from typing import Union

from ..data import ExplanatoryDictionary
from ..data.obsScriptGlobalVariable import ObsScriptGlobalData
import obspython as obs
import traceback

class LogManager:
    """日志管理"""
    def __init__(self, log_dir: Union[str, Path], log_num_max: int = 100, word_max: int = 100000):
        """
        :param log_dir: 保存日志文件的文件夹路径
        :param log_num_max: 保存的最大日志文件数
        :param word_max: 日志最大字数限制
        """
        self.logRecording = ""
        # 确保 log_dir 是 Path 对象
        self.log_dir = Path(log_dir)
        self.log_num_max = log_num_max
        self.word_max = word_max

        # 确保日志目录存在
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 添加更多配置项
        self.enable_file_logging = True
        self.enable_console_logging = True
        self.current_log_file = None

    def log_go(self, log_level: int, log_str: str) -> None:
        """
        输出并预存日志
        Args:
            log_level: 日志等级
                - obs.LOG_INFO
                - obs.LOG_DEBUG
                - obs.LOG_WARNING
                - obs.LOG_ERROR
            log_str: 日志内容
        Returns: None
        """
        try:
            # 获取版本号，处理可能的异常
            version = getattr(ObsScriptGlobalData, 'version', 'Unknown')

            # 格式化时间
            now = datetime.now()
            formatted = now.strftime("%Y/%m/%d %H:%M:%S")

            # 获取日志类型描述
            log_type_desc = ExplanatoryDictionary.log_type.get(
                log_level,
                f"UNKNOWN({log_level})"
            )

            # 构建日志文本
            log_text = f"{version} 【{formatted}】【{log_type_desc}】 \t{log_str}"

            # 输出到 OBS 日志
            obs.script_log(log_level, log_text)

            # 添加到缓存
            self.logRecording += log_text + "\n"

            # 检查是否需要保存到文件
            if len(self.logRecording) > self.word_max:
                self.log_save()

        except Exception as e:
            # 日志记录器本身的错误处理
            error_msg = f"LogManager error: {type(e).__name__} - {str(e)}"
            obs.script_log(obs.LOG_ERROR, error_msg)
            # 防止无限递归，不使用 log_go 记录这个错误
            print(f"LogManager内部错误: {error_msg}")

    def log_save(self, force_save: bool = False) -> bool:
        """
        保存日志到文件

        Args:
            force_save: 是否强制保存，即使缓存为空

        Returns:
            bool: 是否成功保存
        """
        try:
            # 如果没有日志内容且不是强制保存，则跳过
            if not self.logRecording.strip() and not force_save:
                return False

            # 生成新的日志文件名
            new_log_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            new_log_path = self.log_dir / new_log_filename

            # 写入新的日志文件
            with open(new_log_path, "w", encoding="utf-8") as f:
                f.write(self.logRecording)

            # 记录日志文件路径（用于调试）
            self.current_log_file = new_log_path

            # 清理过期的日志文件
            self._cleanup_old_logs()

            # 清空缓存
            self.logRecording = ""

            # 记录保存成功的信息
            save_msg = f"日志已保存到: {new_log_path}"
            obs.script_log(obs.LOG_INFO, save_msg)

            return True

        except Exception as e:
            error_msg = f"保存日志失败: {type(e).__name__} - {str(e)}"
            obs.script_log(obs.LOG_ERROR, error_msg)
            return False

    def _cleanup_old_logs(self) -> None:
        """清理过期的日志文件"""
        try:
            # 获取所有.log文件并按修改时间排序（最新的在前）
            log_files = sorted(
                [f for f in self.log_dir.glob("*.log") if f.is_file()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )

            # 如果文件数量超过限制，删除最旧的文件
            if len(log_files) > self.log_num_max:
                files_to_delete = log_files[self.log_num_max:]
                for old_file in files_to_delete:
                    try:
                        old_file.unlink()
                        obs.script_log(obs.LOG_DEBUG, f"已删除旧日志文件: {old_file.name}")
                    except Exception as e:
                        obs.script_log(obs.LOG_WARNING, f"删除日志文件失败 {old_file.name}: {e}")
        except Exception as e:
            obs.script_log(obs.LOG_ERROR, f"清理旧日志时出错: {e}")

    def log_exception(self, exception: Exception, context: str = "") -> None:
        """
        记录异常信息

        Args:
            exception: 异常对象
            context: 异常发生的上下文描述
        """
        try:
            # 获取完整的堆栈信息
            traceback_info = traceback.format_exc()

            # 构建异常信息
            error_msg = f"{context}: {type(exception).__name__}: {str(exception)}"

            # 记录异常
            self.log_go(obs.LOG_ERROR, error_msg)

            # 如果堆栈信息不为空，也记录下来
            if traceback_info and traceback_info != "NoneType: None\n":
                # 将堆栈信息拆分成多行记录
                lines = traceback_info.strip().split('\n')
                for line in lines:
                    if line.strip():  # 跳过空行
                        self.log_go(obs.LOG_DEBUG, f"  {line}")

        except Exception as e:
            # 处理记录异常时的错误
            print(f"记录异常时出错: {e}")

    def log_info(self, message: str) -> None:
        """记录信息级别的日志"""
        self.log_go(obs.LOG_INFO, message)

    def log_warning(self, message: str) -> None:
        """记录警告级别的日志"""
        self.log_go(obs.LOG_WARNING, message)

    def log_error(self, message: str) -> None:
        """记录错误级别的日志"""
        self.log_go(obs.LOG_ERROR, message)

    def log_debug(self, message: str) -> None:
        """记录调试级别的日志"""
        self.log_go(obs.LOG_DEBUG, message)

    def flush(self) -> bool:
        """
        强制将缓存的日志保存到文件

        Returns:
            bool: 是否成功保存
        """
        return self.log_save(force_save=True)

    def get_log_count(self) -> int:
        """获取当前日志文件夹中的日志文件数量"""
        try:
            log_files = list(self.log_dir.glob("*.log"))
            return len(log_files)
        except Exception as e:
            self.log_error(f"获取日志文件数量失败: {e}")
            return 0

    def get_log_size(self) -> tuple:
        """
        获取日志缓存大小和文件大小

        Returns:
            tuple: (缓存大小, 总文件大小)
        """
        cache_size = len(self.logRecording)
        total_file_size = 0

        try:
            # 计算所有日志文件的总大小
            for log_file in self.log_dir.glob("*.log"):
                if log_file.is_file():
                    total_file_size += log_file.stat().st_size
        except Exception as e:
            self.log_error(f"计算日志文件大小时出错: {e}")

        return cache_size, total_file_size

    def __del__(self):
        """析构函数，确保程序退出时保存日志"""
        try:
            if self.logRecording.strip():
                self.flush()
        except:
            pass  # 析构函数中不抛出异常