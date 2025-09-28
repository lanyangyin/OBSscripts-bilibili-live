import pathlib
import json
from typing import Dict, Optional, List, Union, TypedDict
from datetime import datetime


class OperationResult(TypedDict, total=False):
    """操作结果类型定义"""
    success: bool
    message: str
    user_id: Optional[str]
    data: Optional[Dict]


class UserInfo(TypedDict, total=False):
    """用户信息类型定义"""
    user_id: str
    is_default: bool
    last_updated: Optional[str]


class BilibiliUserConfigManager:
    """
    B站用户配置管理器，负责用户登录信息的增删改查操作。

    配置文件采用JSON格式，结构示例：
    {
        "default_user": "12345",
        "users": {
            "12345": {
                "DedeUserID": "12345",
                "DedeUserID__ckMd5": "xxxxxxxx",
                "SESSDATA": "xxxxxxxx",
                "bili_jct": "xxxxxxxx",
                "buvid3": "xxxxxxxx",
                "b_nut": "xxxxxxxx",
                "last_updated": "2023-01-01T00:00:00"
            }
        }
    }
    """

    # 必需的cookie字段
    REQUIRED_COOKIE_KEYS = {
        "DedeUserID", "DedeUserID__ckMd5", "SESSDATA",
        "bili_jct", "buvid3", "b_nut"
    }

    # 最小必需的cookie字段（用于更新操作）
    MIN_REQUIRED_KEYS = {"DedeUserID", "SESSDATA", "bili_jct"}

    def __init__(self, config_path: Union[str, pathlib.Path]):
        """
        初始化配置文件管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = pathlib.Path(config_path)
        self._ensure_config_file()

    def _ensure_config_file(self) -> OperationResult:
        """确保配置文件存在且结构有效"""
        try:
            if not self.config_path.exists():
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                initial_config = {
                    "default_user": None,
                    "users": {}
                }
                return self._write_config(initial_config)

            config = self._read_config()
            if not isinstance(config, dict):
                return self._create_error_result("配置文件格式错误")

            # 修复旧格式配置文件
            if "users" not in config:
                users = {}
                for key, value in config.items():
                    if key != "DefaultUser" and isinstance(value, dict):
                        users[key] = value

                default_user = config.get("DefaultUser")
                new_config = {
                    "default_user": default_user,
                    "users": users
                }
                return self._write_config(new_config)

            return self._create_success_result("配置文件检查完成")

        except Exception as e:
            return self._create_error_result(f"配置文件初始化失败: {str(e)}")

    def _read_config(self) -> Dict:
        """读取配置文件内容"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"配置文件损坏或格式错误: {str(e)}")

    def _write_config(self, config: Dict) -> OperationResult:
        """写入配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return self._create_success_result("配置文件写入成功")
        except Exception as e:
            return self._create_error_result(f"配置文件写入失败: {str(e)}")

    def _validate_cookies(self, cookies: Dict[str, str], required_keys: set) -> OperationResult:
        """验证cookie字段完整性"""
        if not isinstance(cookies, dict):
            return self._create_error_result("cookies参数必须是字典类型")

        missing_keys = required_keys - cookies.keys()
        if missing_keys:
            return self._create_error_result(f"缺少必要字段: {', '.join(missing_keys)}")

        return self._create_success_result("cookie验证通过")

    def _create_success_result(self, message: str = "操作成功",
                               user_id: Optional[str] = None,
                               data: Optional[Dict] = None) -> OperationResult:
        """创建成功结果"""
        result: OperationResult = {"success": True, "message": message}
        if user_id is not None:
            result["user_id"] = user_id
        if data is not None:
            result["data"] = data
        return result

    def _create_error_result(self, message: str) -> OperationResult:
        """创建错误结果"""
        return {"success": False, "message": message}

    def add_user(self, cookies: Dict[str, str]) -> OperationResult:
        """
        添加新用户配置

        Args:
            cookies: 包含完整cookie信息的字典

        Returns:
            操作结果字典
        """
        try:
            # 验证cookie完整性
            validation_result = self._validate_cookies(cookies, self.REQUIRED_COOKIE_KEYS)
            if not validation_result["success"]:
                return validation_result

            uid = str(cookies["DedeUserID"])
            config = self._read_config()

            # 检查用户是否已存在
            if uid in config["users"]:
                return self._create_error_result(f"用户 {uid} 已存在，请使用update_user进行更新")

            # 添加时间戳
            user_data = cookies.copy()
            user_data["last_updated"] = datetime.now().isoformat()

            config["users"][uid] = user_data

            # 如果是第一个用户，自动设置为默认用户
            if not config["default_user"] and config["users"]:
                config["default_user"] = uid

            write_result = self._write_config(config)
            if not write_result["success"]:
                return write_result

            return self._create_success_result("用户添加成功", user_id=uid)

        except Exception as e:
            return self._create_error_result(f"添加用户失败: {str(e)}")

    def delete_user(self, user_id: Union[int, str]) -> OperationResult:
        """
        删除用户配置

        Args:
            user_id: 要删除的用户ID

        Returns:
            操作结果字典
        """
        try:
            config = self._read_config()
            user_id_str = str(user_id)

            if user_id_str not in config["users"]:
                return self._create_error_result(f"用户 {user_id_str} 不存在")

            # 检查是否为默认用户
            if config["default_user"] == user_id_str:
                return self._create_error_result("不能删除默认用户，请先更改默认用户设置")

            del config["users"][user_id_str]

            # 如果删除的是默认用户，清空默认用户设置
            if config["default_user"] == user_id_str:
                config["default_user"] = None

            write_result = self._write_config(config)
            if not write_result["success"]:
                return write_result

            return self._create_success_result("用户删除成功", user_id=user_id_str)

        except Exception as e:
            return self._create_error_result(f"删除用户失败: {str(e)}")

    def update_user(self, cookies: Dict[str, str], set_as_default: bool = False) -> OperationResult:
        """
        更新用户配置

        Args:
            cookies: 包含cookie信息的字典
            set_as_default: 是否设为默认用户

        Returns:
            操作结果字典
        """
        try:
            # 验证最小必需字段
            validation_result = self._validate_cookies(cookies, self.MIN_REQUIRED_KEYS)
            if not validation_result["success"]:
                return validation_result

            uid = str(cookies["DedeUserID"])
            config = self._read_config()

            if uid not in config["users"]:
                return self._create_error_result(f"用户 {uid} 不存在")

            # 更新用户数据
            config["users"][uid].update(cookies)
            config["users"][uid]["last_updated"] = datetime.now().isoformat()

            # 设置默认用户
            if set_as_default:
                config["default_user"] = uid

            write_result = self._write_config(config)
            if not write_result["success"]:
                return write_result

            message = "用户更新成功" + ("并设置为默认用户" if set_as_default else "")
            return self._create_success_result(message, user_id=uid)

        except Exception as e:
            return self._create_error_result(f"更新用户失败: {str(e)}")

    def set_default_user(self, user_id: Union[int, str]) -> OperationResult:
        """
        设置默认用户

        Args:
            user_id: 要设置为默认用户的用户ID

        Returns:
            操作结果字典
        """
        try:
            config = self._read_config()
            user_id_str = str(user_id)

            if user_id_str not in config["users"]:
                return self._create_error_result(f"用户 {user_id_str} 不存在")

            config["default_user"] = user_id_str
            write_result = self._write_config(config)
            if not write_result["success"]:
                return write_result

            return self._create_success_result("默认用户设置成功", user_id=user_id_str)

        except Exception as e:
            return self._create_error_result(f"设置默认用户失败: {str(e)}")

    def clear_default_user(self) -> OperationResult:
        """
        清空默认用户设置

        Returns:
            操作结果字典
        """
        try:
            config = self._read_config()
            config["default_user"] = None
            write_result = self._write_config(config)
            if not write_result["success"]:
                return write_result

            return self._create_success_result("默认用户已清除")

        except Exception as e:
            return self._create_error_result(f"清除默认用户失败: {str(e)}")

    def get_user_cookies(self, user_id: Optional[Union[int, str]] = None) -> OperationResult:
        """
        获取指定用户的cookie信息

        Args:
            user_id: 用户ID，None表示获取默认用户

        Returns:
            操作结果字典，包含cookie数据
        """
        try:
            config = self._read_config()

            # 获取目标用户ID
            if user_id is None:
                target_user_id = config.get("default_user")
                if target_user_id is None:
                    return self._create_error_result("未设置默认用户")
            else:
                target_user_id = str(user_id)

            # 检查用户是否存在
            if target_user_id not in config["users"]:
                return self._create_error_result(f"用户 {target_user_id} 不存在")

            user_data = config["users"][target_user_id].copy()
            return self._create_success_result(
                "获取用户cookie成功",
                user_id=target_user_id,
                data=user_data
            )

        except Exception as e:
            return self._create_error_result(f"获取用户cookie失败: {str(e)}")

    def get_all_users(self) -> OperationResult:
        """
        获取所有用户信息列表

        Returns:
            操作结果字典，包含用户列表
        """
        try:
            config = self._read_config()
            default_user = config.get("default_user")

            users: List[UserInfo] = []
            for uid, user_data in config["users"].items():
                user_info: UserInfo = {
                    "user_id": uid,
                    "is_default": uid == default_user,
                    "last_updated": user_data.get("last_updated")
                }
                users.append(user_info)

            return self._create_success_result(
                "获取用户列表成功",
                data={"users": users, "total": len(users)}
            )

        except Exception as e:
            return self._create_error_result(f"获取用户列表失败: {str(e)}")

    def user_exists(self, user_id: Union[int, str]) -> bool:
        """
        检查用户是否存在

        Args:
            user_id: 要检查的用户ID

        Returns:
            True表示用户存在，False表示不存在
        """
        try:
            config = self._read_config()
            return str(user_id) in config["users"]
        except Exception:
            return False

    def get_default_user_id(self) -> Optional[str]:
        """
        获取默认用户ID

        Returns:
            默认用户ID，如果没有设置默认用户则返回None
        """
        try:
            config = self._read_config()
            return config.get("default_user")
        except Exception:
            return None

    def get_user_count(self) -> int:
        """
        获取用户数量

        Returns:
            用户数量
        """
        try:
            config = self._read_config()
            return len(config["users"])
        except Exception:
            return 0


def create_sample_cookies(user_id: str) -> Dict[str, str]:
    """创建示例cookie数据"""
    return {
        "DedeUserID": user_id,
        "DedeUserID__ckMd5": f"md5_{user_id}",
        "SESSDATA": f"sessdata_{user_id}",
        "bili_jct": f"jct_{user_id}",
        "buvid3": f"buvid3_{user_id}",
        "b_nut": f"bnut_{user_id}"
    }


if __name__ == "__main__":
    # 测试示例
    import tempfile

    # 创建临时目录进行测试
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = pathlib.Path(temp_dir) / "bilibili_config.json"
        print(f"使用临时配置文件: {config_file}")

        # 初始化配置管理器
        manager = BilibiliUserConfigManager(config_file)
        print("1. 配置管理器初始化完成")

        # 测试1: 添加第一个用户
        cookies1 = create_sample_cookies("12345")
        result = manager.add_user(cookies1)
        print(f"2. 添加用户1: {result}")

        # 测试2: 添加第二个用户
        cookies2 = create_sample_cookies("67890")
        result = manager.add_user(cookies2)
        print(f"3. 添加用户2: {result}")

        # 测试3: 获取所有用户
        result = manager.get_all_users()
        print(f"4. 所有用户: {result}")

        # 测试4: 设置默认用户
        result = manager.set_default_user("12345")
        print(f"5. 设置默认用户: {result}")

        # 测试5: 获取默认用户cookie
        result = manager.get_user_cookies()
        print(f"6. 获取默认用户cookie: {result['data']}, 用户ID: {result.get('user_id')}")

        # 测试6: 更新用户信息
        update_cookies = {
            "DedeUserID": "12345",
            "SESSDATA": "updated_sessdata_12345",
            "bili_jct": "updated_jct_12345"
        }
        result = manager.update_user(update_cookies, set_as_default=True)
        print(f"7. 更新用户: {result}")

        # 测试7: 获取特定用户cookie
        result = manager.get_user_cookies("67890")
        print(f"8. 获取特定用户cookie: {result['success']}, 用户ID: {result.get('user_id')}")

        # 测试8: 检查用户是否存在
        exists = manager.user_exists("12345")
        print(f"9. 用户12345是否存在: {exists}")

        # 测试9: 获取默认用户ID
        default_id = manager.get_default_user_id()
        print(f"10. 当前默认用户ID: {default_id}")

        # 测试10: 获取用户数量
        count = manager.get_user_count()
        print(f"11. 当前用户数量: {count}")

        # 测试11: 尝试删除默认用户（应该失败）
        result = manager.delete_user("12345")
        print(f"12. 尝试删除默认用户: {result}")

        # 测试12: 清除默认用户
        result = manager.clear_default_user()
        print(f"13. 清除默认用户: {result}")

        # 测试13: 现在删除用户（应该成功）
        result = manager.delete_user("12345")
        print(f"14. 删除用户: {result}")

        # 测试14: 最终用户列表
        result = manager.get_all_users()
        print(f"15. 最终用户列表: {result}")

        # 测试15: 验证错误处理 - 添加不完整的cookie
        bad_cookies = {"DedeUserID": "99999"}  # 缺少其他必要字段
        result = manager.add_user(bad_cookies)
        print(f"16. 添加不完整cookie: {result}")

        # 测试16: 验证错误处理 - 获取不存在的用户
        result = manager.get_user_cookies("nonexistent")
        print(f"17. 获取不存在的用户: {result}")

        # 显示最终配置文件内容
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                print("18. 最终配置文件内容:")
                print(json.dumps(content, indent=2, ensure_ascii=False))

        # 测试5: 获取默认用户cookie
        result = manager.get_user_cookies()
        print(f"6. 获取默认用户cookie: {result}, 用户ID: {result.get('user_id')}")

        print("测试完成!")