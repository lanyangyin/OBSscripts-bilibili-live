from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any, Optional, Union, Literal, List, Iterator, Callable

import obspython as obs


@lru_cache(maxsize=None)
def test():
    return True

def clear_cache():
    # 清除函数缓存
    test.cache_clear()

# ====================================================================================================================


# -----------------------------------------------------------
# OBS Script Functions                                      -
# -----------------------------------------------------------

script_version = bytes.fromhex('302e322e37').decode('utf-8')
"""脚本版本.encode().hex()"""


class GlobalVariableOfData:
    """定义了一些全局变量"""
    props_dict: Dict[str, Any] = {}
    """属性集字典"""
    causeOfTheFrontDeskIncident = ""
    """前台事件引起的原因"""
    update_widget_for_props_dict: dict[str, set[str]] = {}
    """根据控件属性集更新控件"""
    script_loading_is: bool = False
    """是否正式加载脚本"""
    widget_loading_number: int = 0
    """控件加载顺序"""
    isScript_propertiesIs: bool = False  # Script_properties()被调用
    """是否允许Script_properties()被调用"""
    script_settings: bool = None  # #脚本的所有设定属性集
    """脚本的所有设定属性集"""

    logRecording: str = ""  # #日志记录的文本
    """日志记录的文本"""
    networkConnectionStatus: bool = False  # #网络连接状态
    """网络连接状态"""
    sslVerification: bool = True
    """SSL验证"""

    # 文件配置类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    scriptsDataDirpath: Optional[Path] = None  # #脚本所在目录，末尾带/
    """脚本所在目录，末尾带/"""
    scriptsUsersConfigFilepath: Optional[Path] = None  # #用户配置文件路径
    """用户配置文件路径"""
    scriptsTempDir: Optional[Path] = None  # #临时文件文件夹
    """临时文件文件夹"""
    scriptsLogDir: Optional[Path] = None  # #日志文件文件夹
    """日志文件文件夹"""
    scriptsCacheDir: Optional[Path] = None  # #缓存文件文件夹
    """缓存文件文件夹"""

    # 源类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    browserSource: Any = None 
    """浏览器源"""


class ExplanatoryDictionary:
    """定义了一些数据的说明字典"""
    textBox_type_name4textBox_type: Dict[int, str] = {
        obs.OBS_TEXT_INFO_NORMAL: '正常信息',
        obs.OBS_TEXT_INFO_WARNING: '警告信息',
        obs.OBS_TEXT_INFO_ERROR: '错误信息'
    }
    """只读文本框的消息类型 说明字典"""

    information4frontend_event: Dict[int, str] = {
        # 推流相关事件
        obs.OBS_FRONTEND_EVENT_STREAMING_STARTING: "推流正在启动",
        obs.OBS_FRONTEND_EVENT_STREAMING_STARTED: "推流已开始",
        obs.OBS_FRONTEND_EVENT_STREAMING_STOPPING: "推流正在停止",
        obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED: "推流已停止",

        # 录制相关事件
        obs.OBS_FRONTEND_EVENT_RECORDING_STARTING: "录制正在启动",
        obs.OBS_FRONTEND_EVENT_RECORDING_STARTED: "录制已开始",
        obs.OBS_FRONTEND_EVENT_RECORDING_STOPPING: "录制正在停止",
        obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED: "录制已停止",
        obs.OBS_FRONTEND_EVENT_RECORDING_PAUSED: "录制已暂停",
        obs.OBS_FRONTEND_EVENT_RECORDING_UNPAUSED: "录制已恢复",

        # 回放缓存相关事件
        obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTING: "回放缓存正在启动",
        obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED: "回放缓存已开始",
        obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPING: "回放缓存正在停止",
        obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED: "回放缓存已停止",
        obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED: "回放已保存",

        # 场景相关事件
        obs.OBS_FRONTEND_EVENT_SCENE_CHANGED: "当前场景已改变",
        obs.OBS_FRONTEND_EVENT_PREVIEW_SCENE_CHANGED: "预览场景已改变",
        obs.OBS_FRONTEND_EVENT_SCENE_LIST_CHANGED: "场景列表已改变",

        # 转场相关事件
        obs.OBS_FRONTEND_EVENT_TRANSITION_CHANGED: "转场效果已改变",
        obs.OBS_FRONTEND_EVENT_TRANSITION_STOPPED: "转场效果已停止",
        obs.OBS_FRONTEND_EVENT_TRANSITION_LIST_CHANGED: "转场列表已改变",
        obs.OBS_FRONTEND_EVENT_TRANSITION_DURATION_CHANGED: "转场持续时间已更改",

        # 配置文件相关事件
        obs.OBS_FRONTEND_EVENT_PROFILE_CHANGING: "配置文件即将切换",
        obs.OBS_FRONTEND_EVENT_PROFILE_CHANGED: "配置文件已切换",
        obs.OBS_FRONTEND_EVENT_PROFILE_LIST_CHANGED: "配置文件列表已改变",
        obs.OBS_FRONTEND_EVENT_PROFILE_RENAMED: "配置文件已重命名",

        # 场景集合相关事件
        obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGING: "场景集合即将切换",
        obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED: "场景集合已切换",
        obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_LIST_CHANGED: "场景集合列表已改变",
        obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_RENAMED: "场景集合已重命名",
        obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CLEANUP: "场景集合清理完成",

        # 工作室模式事件
        obs.OBS_FRONTEND_EVENT_STUDIO_MODE_ENABLED: "工作室模式已启用",
        obs.OBS_FRONTEND_EVENT_STUDIO_MODE_DISABLED: "工作室模式已禁用",

        # 系统级事件
        obs.OBS_FRONTEND_EVENT_EXIT: "OBS 即将退出",
        obs.OBS_FRONTEND_EVENT_FINISHED_LOADING: "OBS 完成加载",
        obs.OBS_FRONTEND_EVENT_SCRIPTING_SHUTDOWN: "脚本关闭中",

        # 虚拟摄像头事件
        obs.OBS_FRONTEND_EVENT_VIRTUALCAM_STARTED: "虚拟摄像头已启动",
        obs.OBS_FRONTEND_EVENT_VIRTUALCAM_STOPPED: "虚拟摄像头已停止",

        # 控制条事件
        obs.OBS_FRONTEND_EVENT_TBAR_VALUE_CHANGED: "转场控制条(T-Bar)值已改变",

        # OBS 28+ 新增事件
        obs.OBS_FRONTEND_EVENT_SCREENSHOT_TAKEN: "截图已完成",
        obs.OBS_FRONTEND_EVENT_THEME_CHANGED: "主题已更改"
    }
    """obs前台事件 说明字典"""

    log_type: Dict[int, str] = {
        obs.LOG_INFO: "INFO",
        obs.LOG_DEBUG: "DEBUG",
        obs.LOG_WARNING: "WARNING",
        obs.LOG_ERROR: "ERROR"
    }
    """obs日志警告等级 说明字典"""

    information4login_qr_return_code: Dict[int, str] = {
        0: "登录成功",
        86101: "未扫码",
        86090: "二维码已扫码未确认",
        86038: "二维码已失效",
    }
    """登陆二维码返回码 说明字典"""


def log_save(log_level, log_str: str) -> None:
    """
    输出并保存日志
    Args:
        log_level: 日志等级

            - obs.LOG_INFO
            - obs.LOG_DEBUG
            - obs.LOG_WARNING
            - obs.LOG_ERROR
        log_str: 日志内容
    Returns: None
    """
    now: datetime = datetime.now()
    formatted: str = now.strftime("%Y/%m/%d %H:%M:%S")
    log_text: str = f"{script_version} 【{formatted}】【{ExplanatoryDictionary.log_type[log_level]}】 \t{log_str}"
    obs.script_log(log_level, log_str)
    GlobalVariableOfData.logRecording += log_text + "\n"


@dataclass
class ControlBase:
    """控件基类"""
    ControlType: Literal[
        "Base", "CheckBox", "DigitalDisplay", "TextBox", "Button", "ComboBox", "PathBox", "Group"] = "Base"
    """📵控件的基本类型"""
    Obj: Any = None
    """📵控件的obs对象"""
    Props: str = None
    """📵控件属于哪个属性集"""
    Number: int = 0
    """📵控件的加载顺序数"""
    Name: str = ""
    """📵控件的唯一名"""
    Description: str = ""
    """📵控件显示给用户的信息"""
    Visible: bool = False
    """控件的可见状态"""
    Enabled: bool = False
    """控件的可用状态"""
    ModifiedIs: bool = False
    """📵控件变动是否触发钩子函数"""


class Widget:
    """表单管理器，管理所有控件"""

    class CheckBoxPs:
        """复选框控件管理器"""

        @dataclass
        class CheckBoxP(ControlBase):
            """复选框控件实例"""
            ControlType: str = "CheckBox"
            """📵复选框的控件类型为 CheckBox"""
            Bool: bool = False
            """复选框的选中状态"""

            def __repr__(self) -> str:
                type_name = "未知类复选框"
                return f"<CheckBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Bool={self.Bool}>"

        def __init__(self):
            self._controls: Dict[str, Widget.CheckBoxPs.CheckBoxP] = {}
            self._loading_order: List[Widget.CheckBoxPs.CheckBoxP] = []

        def add(self, name: str, **kwargs) -> CheckBoxP:
            """添加复选框控件"""
            if name in self._controls:
                raise ValueError(f"复选框 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            control = Widget.CheckBoxPs.CheckBoxP(**kwargs)
            self._controls[name] = control
            self._loading_order.append(control)
            setattr(self, name, control)
            return control

        def get(self, name: str) -> Optional[CheckBoxP]:
            """获取复选框控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除复选框控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                return True
            return False

        def __iter__(self) -> Iterator[CheckBoxP]:
            """迭代所有复选框控件"""
            return iter(self._controls.values())

        def __len__(self) -> int:
            """复选框控件数量"""
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            """检查复选框控件是否存在"""
            return name in self._controls

        def get_loading_order(self) -> List[CheckBoxP]:
            """获取按载入次序排序的复选框控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    class DigitalDisplayPs:
        """数字框控件管理器"""

        @dataclass
        class DigitalDisplayP(ControlBase):
            """数字框控件实例"""
            ControlType: str = "DigitalDisplay"
            """📵数字框的控件类型为 PathBox"""
            Type: Literal["ThereIsASlider", "NoSlider"] = ""
            """📵数字框的类型"""
            Value: int = 0
            """数字框显示的数值"""
            Suffix: str = ""
            """数字框显示的数值的单位"""
            Min: int = 0
            """数字框显示的数值的最小值"""
            Max: int = 0
            """数字框显示的数值的最大值"""
            Step: int = 0
            """数字框显示的步长"""

            def __repr__(self) -> str:
                type_name = "滑块数字框" if self.Type == "ThereIsASlider" else "普通数字框"
                return f"<DigitalDisplayP Name='{self.Name}' Number={self.Number} Type='{type_name}' Min={self.Min} Max={self.Max}>"

        def __init__(self):
            self._controls: Dict[str, Widget.DigitalDisplayPs.DigitalDisplayP] = {}
            self._loading_order: List[Widget.DigitalDisplayPs.DigitalDisplayP] = []

        def add(self, name: str, **kwargs) -> DigitalDisplayP:
            """添加数字框控件"""
            if name in self._controls:
                raise ValueError(f"数字框 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            control = Widget.DigitalDisplayPs.DigitalDisplayP(**kwargs)
            self._controls[name] = control
            self._loading_order.append(control)
            setattr(self, name, control)
            return control

        def get(self, name: str) -> Optional[DigitalDisplayP]:
            """获取数字框控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除数字框控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                return True
            return False

        def __iter__(self) -> Iterator[DigitalDisplayP]:
            """迭代所有数字框控件"""
            return iter(self._controls.values())

        def __len__(self) -> int:
            """数字框控件数量"""
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            """检查数字框控件是否存在"""
            return name in self._controls

        def get_loading_order(self) -> List[DigitalDisplayP]:
            """获取按载入次序排序的数字框控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    class TextBoxPs:
        """文本框控件管理器"""

        @dataclass
        class TextBoxP(ControlBase):
            """文本框控件实例"""
            ControlType: str = "TextBox"
            """📵文本框的控件类型为 TextBox"""
            Type: Optional[int] = None  # 文本框类型
            """📵文本框的类型"""
            LongDescription: str = ""
            """📵长描述"""
            Text: str = ""
            """文本框显示的文字"""
            InfoType: Any = obs.OBS_TEXT_INFO_NORMAL  # 信息类型
            """
            文本框中文字的警告类型
            obs.OBS_TEXT_INFO_NORMAL, obs.OBS_TEXT_INFO_WARNING, obs.OBS_TEXT_INFO_ERROR
            """

            def __repr__(self) -> str:
                type_name = "未知类文本框"
                if self.Type == obs.OBS_TEXT_DEFAULT:
                    type_name = "单行文本"
                elif self.Type == obs.OBS_TEXT_PASSWORD:
                    type_name = "单行文本（带密码）"
                elif self.Type == obs.OBS_TEXT_MULTILINE:
                    type_name = "多行文本"
                elif self.Type == obs.OBS_TEXT_INFO:
                    type_name = "只读信息文本"
                return f"<TextBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Text='{self.Text}'>"

        def __init__(self):
            self._controls: Dict[str, Widget.TextBoxPs.TextBoxP] = {}
            self._loading_order: List[Widget.TextBoxPs.TextBoxP] = []

        def add(self, name: str, **kwargs) -> TextBoxP:
            """添加文本框控件"""
            if name in self._controls:
                raise ValueError(f"文本框 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            control = Widget.TextBoxPs.TextBoxP(**kwargs)
            self._controls[name] = control
            self._loading_order.append(control)
            setattr(self, name, control)
            return control

        def get(self, name: str) -> Optional[TextBoxP]:
            """获取文本框控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除文本框控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                return True
            return False

        def __iter__(self) -> Iterator[TextBoxP]:
            """迭代所有文本框控件"""
            return iter(self._controls.values())

        def __len__(self) -> int:
            """文本框控件数量"""
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            """检查文本框控件是否存在"""
            return name in self._controls

        def get_loading_order(self) -> List[TextBoxP]:
            """获取按载入次序排序的文本框控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    class ButtonPs:
        """按钮控件管理器"""

        @dataclass
        class ButtonP(ControlBase):
            """按钮控件实例"""
            ControlType: str = "Button"
            """📵按钮的控件类型为 Button"""
            Type: Optional[int] = None  # 按钮类型
            """📵按钮的类型 """
            Callback: Optional[Callable[[Any, Any], Literal[True, False]]] = None  # 回调函数
            """📵按钮被按下后触发的回调函数"""
            Url: str = ""  # 需要打开的 URL
            """📵URL类型的按钮被按下后跳转的URL"""

            def __repr__(self) -> str:
                type_name = "未知类按钮"
                if self.Type == obs.OBS_BUTTON_DEFAULT:
                    type_name = "标准按钮"
                elif self.Type == obs.OBS_BUTTON_URL:
                    type_name = "打开 URL 的按钮"
                return f"<ButtonP Name='{self.Name}' Number={self.Number} Type='{type_name}' Callback={self.Callback is not None}>"

        def __init__(self):
            self._controls: Dict[str, Widget.ButtonPs.ButtonP] = {}
            self._loading_order: List[Widget.ButtonPs.ButtonP] = []

        def add(self, name: str, **kwargs) -> ButtonP:
            """添加按钮控件"""
            if name in self._controls:
                raise ValueError(f"按钮 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            control = Widget.ButtonPs.ButtonP(**kwargs)
            self._controls[name] = control
            self._loading_order.append(control)
            setattr(self, name, control)
            return control

        def get(self, name: str) -> Optional[ButtonP]:
            """获取按钮控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除按钮控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                return True
            return False

        def __iter__(self) -> Iterator[ButtonP]:
            """迭代所有按钮控件"""
            return iter(self._controls.values())

        def __len__(self) -> int:
            """按钮控件数量"""
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            """检查按钮控件是否存在"""
            return name in self._controls

        def get_loading_order(self) -> List[ButtonP]:
            """获取按载入次序排序的按钮控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    class ComboBoxPs:
        """组合框控件管理器"""

        @dataclass
        class ComboBoxP(ControlBase):
            """组合框控件实例"""
            ControlType: str = "ComboBox"
            """📵组合框的控件类型为 ComboBox"""
            Type: Optional[int] = None  # 组合框类型
            """📵组合框类型"""
            Text: str = ""
            """组合框显示的文字"""
            Value: str = ""
            """组合框显示的文字对应的值"""
            Dictionary: Dict[str, Any] = field(default_factory=dict)  # 数据字典
            """组合框选项字典"""

            def __repr__(self) -> str:
                type_name = "未知类组合框"
                if self.Type == obs.OBS_COMBO_TYPE_EDITABLE:
                    type_name = "可以编辑。 仅与字符串列表一起使用"
                elif self.Type == obs.OBS_COMBO_TYPE_LIST:
                    type_name = "不可编辑。显示为组合框"
                elif self.Type == obs.OBS_COMBO_TYPE_RADIO:
                    type_name = "不可编辑。显示为单选按钮"
                return f"<ComboBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Text='{self.Text}'>"

        def __init__(self):
            self._controls: Dict[str, Widget.ComboBoxPs.ComboBoxP] = {}
            self._loading_order: List[Widget.ComboBoxPs.ComboBoxP] = []

        def add(self, name: str, **kwargs) -> ComboBoxP:
            """添加组合框控件"""
            if name in self._controls:
                raise ValueError(f"组合框 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            control = Widget.ComboBoxPs.ComboBoxP(**kwargs)
            self._controls[name] = control
            self._loading_order.append(control)
            setattr(self, name, control)
            return control

        def get(self, name: str) -> Optional[ComboBoxP]:
            """获取组合框控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除组合框控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                return True
            return False

        def __iter__(self) -> Iterator[ComboBoxP]:
            """迭代所有组合框控件"""
            return iter(self._controls.values())

        def __len__(self) -> int:
            """组合框控件数量"""
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            """检查组合框控件是否存在"""
            return name in self._controls

        def get_loading_order(self) -> List[ComboBoxP]:
            """获取按载入次序排序的组合框控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    class PathBoxPs:
        """路径对话框控件管理器"""

        @dataclass
        class PathBoxP(ControlBase):
            """路径对话框控件实例"""
            ControlType: str = "PathBox"
            """📵路径对话框的控件类型为 PathBox"""
            Type: Optional[int] = None  # 路径对话框类型
            """📵路径对话框的类型"""
            Text: str = ""
            """路径对话框显示的路径"""
            Filter: Optional[str] = ""  # 文件种类（筛选条件）
            """路径对话框筛选的文件种类（筛选条件）"""
            StartPath: str = ""  # 对话框起始路径
            """路径对话框选择文件的起始路径"""

            def __repr__(self) -> str:
                type_name = "未知类型路径对话框"
                if self.Type == obs.OBS_PATH_FILE:
                    type_name = "文件对话框"
                elif self.Type == obs.OBS_PATH_FILE_SAVE:
                    type_name = "保存文件对话框"
                elif self.Type == obs.OBS_PATH_DIRECTORY:
                    type_name = "文件夹对话框"
                return f"<PathBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Text='{self.Text}'>"

        def __init__(self):
            self._controls: Dict[str, Widget.PathBoxPs.PathBoxP] = {}
            self._loading_order: List[Widget.PathBoxPs.PathBoxP] = []

        def add(self, name: str, **kwargs) -> PathBoxP:
            """添加路径对话框控件"""
            if name in self._controls:
                raise ValueError(f"路径对话框 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            control = Widget.PathBoxPs.PathBoxP(**kwargs)
            self._controls[name] = control
            self._loading_order.append(control)
            setattr(self, name, control)
            return control

        def get(self, name: str) -> Optional[PathBoxP]:
            """获取路径对话框控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除路径对话框控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                return True
            return False

        def __iter__(self) -> Iterator[PathBoxP]:
            """迭代所有路径对话框控件"""
            return iter(self._controls.values())

        def __len__(self) -> int:
            """路径对话框控件数量"""
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            """检查路径对话框控件是否存在"""
            return name in self._controls

        def get_loading_order(self) -> List[PathBoxP]:
            """获取按载入次序排序的路径对话框控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    class GroupPs:
        """分组框控件管理器"""

        @dataclass
        class GroupP(ControlBase):
            """分组框控件实例（独立控件）"""
            ControlType: str = "Group"
            """📵分组框的控件类型为 Group"""
            Type: Any = None  # 分组框类型
            """
            📵分组框的类型
            [obs.OBS_GROUP_NORMAL, obs.OBS_GROUP_CHECKABLE]
            """
            GroupProps: Any = None  # 统辖属性集
            """📵分组框的自身控件属性集"""
            Bool: Any = False
            """带复选框的分组框的选中状态"""

            def __repr__(self) -> str:
                type_name = "未知类分组框"
                if self.Type == obs.OBS_GROUP_NORMAL:
                    type_name = "只有名称和内容的普通组"
                elif self.Type == obs.OBS_GROUP_CHECKABLE:
                    type_name = "具有复选框、名称和内容的可选组"
                return f"<GroupP Name='{self.Name}' Number={self.Number} Type='{type_name}'>"

        def __init__(self):
            self._groups: Dict[str, Widget.GroupPs.GroupP] = {}
            self._loading_order: List[Widget.GroupPs.GroupP] = []

        def add(self, name: str, **kwargs) -> GroupP:
            """添加分组框控件"""
            if name in self._groups:
                raise ValueError(f"分组框 '{name}' 已存在")
            # 确保Name属性设置正确
            if "Name" not in kwargs:
                kwargs["Name"] = name
            group = Widget.GroupPs.GroupP(**kwargs)
            self._groups[name] = group
            self._loading_order.append(group)
            setattr(self, name, group)
            return group

        def get(self, name: str) -> Optional[GroupP]:
            """获取分组框控件"""
            return self._groups.get(name)

        def remove(self, name: str) -> bool:
            """移除分组框控件"""
            if name in self._groups:
                group = self._groups.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if group in self._loading_order:
                    self._loading_order.remove(group)
                return True
            return False

        def __iter__(self) -> Iterator[GroupP]:
            """迭代所有分组框控件"""
            return iter(self._groups.values())

        def __len__(self) -> int:
            """分组框控件数量"""
            return len(self._groups)

        def __contains__(self, name: str) -> bool:
            """检查分组框控件是否存在"""
            return name in self._groups

        def get_loading_order(self) -> List[GroupP]:
            """获取按载入次序排序的分组框控件列表"""
            return sorted(self._loading_order, key=lambda c: c.Number)

    def __init__(self):
        """初始化表单管理器"""
        self.CheckBox = Widget.CheckBoxPs()
        """复选框"""
        self.DigitalDisplay = Widget.DigitalDisplayPs()
        """数字框"""
        self.TextBox = Widget.TextBoxPs()
        """文本框"""
        self.Button = Widget.ButtonPs()
        """按钮"""
        self.ComboBox = Widget.ComboBoxPs()
        """组合框"""
        self.PathBox = Widget.PathBoxPs()
        """路径对话框"""
        self.Group = Widget.GroupPs()
        """分组框"""
        self.widget_Button_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """按钮控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_Group_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """分组框控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_TextBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """文本框控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_ComboBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """组合框控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_PathBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """路径对话框控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_DigitalDisplay_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """数字框控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_CheckBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
        """复选框控件名称列表【属性集ps】【控件在自己类中的对象名】【"Name"|"Description"】【控件唯一名|控件用户层介绍】"""
        self.widget_list: List[str] = []
        """一个用于规定控件加载顺序的列表"""
        self.props_Collection: dict[str, set[str]] = {}
        """一个用于记录控件属性集名称的集合"""
        self._all_controls: List[Any] = []
        self._loading_dict: Dict[int, Any] = {}

    @property
    def widget_dict_all(self) -> dict[
        Literal["Button", "Group", "TextBox", "ComboBox", "PathBox", "DigitalDisplay", "CheckBox"], dict[
            str, dict[str, dict[str, Union[Callable[[Any, Any], bool], str]]]]]:
        """记录7大控件类型的所有控件的不变属性"""
        return {
            "Button": self.widget_Button_dict,
            "Group": self.widget_Group_dict,
            "TextBox": self.widget_TextBox_dict,
            "ComboBox": self.widget_ComboBox_dict,
            "PathBox": self.widget_PathBox_dict,
            "DigitalDisplay": self.widget_DigitalDisplay_dict,
            "CheckBox": self.widget_CheckBox_dict,
        }

    @property
    def verification_number_controls(self):
        """和排序列表进行控件数量验证"""
        return len(self.widget_list) == len(self.get_sorted_controls())

    def _update_all_controls(self):
        """更新所有控件列表"""
        self._all_controls = []
        # 收集所有类型的控件
        self._all_controls.extend(self.CheckBox)
        self._all_controls.extend(self.DigitalDisplay)
        self._all_controls.extend(self.TextBox)
        self._all_controls.extend(self.Button)
        self._all_controls.extend(self.ComboBox)
        self._all_controls.extend(self.PathBox)
        self._all_controls.extend(self.Group)

    def loading(self):
        """按载入次序排序所有控件"""
        self._update_all_controls()
        # 按Number属性排序
        sorted_controls = sorted(self._all_controls, key=lambda c: c.Number)
        name_dict = {}  # 用于检测名称冲突

        # 创建载入次序字典
        self._loading_dict = {}
        for control in sorted_controls:
            # 检查名称冲突
            if control.Name in name_dict:
                existing_control = name_dict[control.Name]
                raise ValueError(
                    f"控件名称冲突: 控件 '{control.Name}' "
                    f"(类型: {type(control).__name__}, 载入次序: {control.Number}) 与 "
                    f"'{existing_control.Name}' "
                    f"(类型: {type(existing_control).__name__}, 载入次序: {existing_control.Number}) 重名"
                )
            else:
                name_dict[control.Name] = control
            if control.Number in self._loading_dict:
                existing_control = self._loading_dict[control.Number]
                raise ValueError(
                    f"载入次序冲突: 控件 '{control.Name}' (类型: {type(control).__name__}) 和 "
                    f"'{existing_control.Name}' (类型: {type(existing_control).__name__}) "
                    f"使用相同的Number值 {control.Number}"
                )
            self._loading_dict[control.Number] = control

    def get_control_by_number(self, number: int) -> Optional[Any]:
        """通过载入次序获取控件"""
        self.loading()  # 确保已排序
        return self._loading_dict.get(number)

    def get_control_by_name(self, name: str) -> Optional[Any]:
        """通过名称获取控件"""
        # 在顶级控件中查找
        for manager in [self.CheckBox, self.DigitalDisplay, self.TextBox,
                        self.Button, self.ComboBox, self.PathBox, self.Group]:
            if name in manager:
                return manager.get(name)
        return None

    def get_sorted_controls(self) -> List[Any]:
        """获取按载入次序排序的所有控件列表"""
        self.loading()
        return list(self._loading_dict.values())

    def clean(self):
        """清除所有控件并重置表单"""
        # 重置所有控件管理器
        self.CheckBox = Widget.CheckBoxPs()
        self.DigitalDisplay = Widget.DigitalDisplayPs()
        self.TextBox = Widget.TextBoxPs()
        self.Button = Widget.ButtonPs()
        self.ComboBox = Widget.ComboBoxPs()
        self.PathBox = Widget.PathBoxPs()
        self.Group = Widget.GroupPs()

        # 清空内部存储
        self._all_controls = []
        self._loading_dict = {}

        return self  # 支持链式调用

    def preliminary_configuration_control(self):
        """
        创建初始控件
        """
        for basic_types_controls in self.widget_dict_all:
            log_save(obs.LOG_INFO, f"{basic_types_controls}")
            for Ps in self.widget_dict_all[basic_types_controls]:
                if Ps not in  self.props_Collection:
                    self.props_Collection[Ps] = set()
                log_save(obs.LOG_INFO, f"\t{Ps}")
                for name in self.widget_dict_all[basic_types_controls][Ps]:
                    widget_types_controls = getattr(self, basic_types_controls)
                    widget_types_controls.add(name)
                    log_save(obs.LOG_INFO, f"\t\t添加 {name}")
                    obj = getattr(widget_types_controls, name)
                    obj.Name = self.widget_dict_all[basic_types_controls][Ps][name]["Name"]
                    self.props_Collection[Ps].add(obj.Name)
                    if obj.ControlType in ["DigitalDisplay", "TextBox", "Button", "ComboBox", "PathBox", "Group"]:
                        obj.Type = self.widget_dict_all[basic_types_controls][Ps][name]["Type"]
                    if obj.ControlType in ["Button"]:
                        obj.Callback = self.widget_dict_all[basic_types_controls][Ps][name]["Callback"]
                        if obj.Type == obs.OBS_BUTTON_URL:
                            obj.Url = self.widget_dict_all[basic_types_controls][Ps][name]["Url"]
                    if obj.ControlType in ["Group"]:
                        obj.GroupProps = self.widget_dict_all[basic_types_controls][Ps][name]["GroupProps"]
                    if obj.ControlType in ["TextBox"]:
                        obj.LongDescription = self.widget_dict_all[basic_types_controls][Ps][name].get("LongDescription", "")
                    if obj.ControlType in ["DigitalDisplay"]:
                        obj.Suffix = self.widget_dict_all[basic_types_controls][Ps][name]["Suffix"]
                    if obj.ControlType in ["PathBox"]:
                        obj.Filter = self.widget_dict_all[basic_types_controls][Ps][name]["Filter"]
                        obj.StartPath = self.widget_dict_all[basic_types_controls][Ps][name]["StartPath"]
                    obj.Number = self.widget_list.index(obj.Name)
                    obj.ModifiedIs = self.widget_dict_all[basic_types_controls][Ps][name]["ModifiedIs"]
                    obj.Description = self.widget_dict_all[basic_types_controls][Ps][name]["Description"]
                    obj.Props = Ps

    def __repr__(self) -> str:
        """返回表单的可读表示形式"""
        self._update_all_controls()
        return f"<Widget controls={len(self._all_controls)}>"


def trigger_frontend_event(event):
    """
    处理前端事件
    Args:
        event: obs前端事件

    Returns:

    """
    log_save(obs.LOG_INFO, f"监测到obs前端事件: {ExplanatoryDictionary.information4frontend_event[event]}")

    if GlobalVariableOfData.causeOfTheFrontDeskIncident:
        log_save(obs.LOG_INFO, f"此次 事件 由【{GlobalVariableOfData.causeOfTheFrontDeskIncident}】引起")

    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        if not GlobalVariableOfData.causeOfTheFrontDeskIncident:
            log_save(obs.LOG_INFO, "此次 推流已开始 事件 由前台按钮【开始直播】引起")
        GlobalVariableOfData.causeOfTheFrontDeskIncident = ""
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        if not GlobalVariableOfData.causeOfTheFrontDeskIncident:
            log_save(obs.LOG_INFO, "此次 推流已开始 事件 由前台按钮【停止直播】引起")
        GlobalVariableOfData.causeOfTheFrontDeskIncident = ""
    clear_cache()
    return True


def property_modified(t: str) -> bool:
    """
    控件变动拉钩
    Args:
        t: 控件全局唯一名

    Returns:

    """
    log_save(obs.LOG_INFO, f"检测到控件【{t}】变动事件")
    if t == "bottom_button":  # 这个按钮用来标记脚本开始构造控件
        log_save(obs.LOG_INFO, f"检测到脚本构造控件体开始，断开控件事件钩子")
        GlobalVariableOfData.isScript_propertiesIs = True
    if t == "top_button":
        log_save(obs.LOG_INFO, f"检测到脚本构造控件体结束，启动控件事件钩子")
        GlobalVariableOfData.isScript_propertiesIs = False
    if not GlobalVariableOfData.isScript_propertiesIs:
        print(t)
    else:
        log_save(obs.LOG_INFO, f"控件事件钩子已断开")
        return False
    return False


def script_defaults(settings):
    """设置默认值"""
    # =================================================================================================================
    # 设置脚本属性=======================================================================================================
    GlobalVariableOfData.script_settings = settings
    # =================================================================================================================
    # 设置属性集合=======================================================================================================
    if not GlobalVariableOfData.update_widget_for_props_dict:
        GlobalVariableOfData.update_widget_for_props_dict = widget.props_Collection
    log_save(obs.LOG_INFO, f"║║💫更新属性集为{GlobalVariableOfData.update_widget_for_props_dict}的控件")

    update_widget_for_props_name = set()
    for props_name in GlobalVariableOfData.update_widget_for_props_dict:
        update_widget_for_props_name |= GlobalVariableOfData.update_widget_for_props_dict[props_name]
    # =================================================================================================================
    # 设置控件属性=======================================================================================================
    if widget.Button.top.Name in update_widget_for_props_name:
        widget.Button.top.Visible = False
        widget.Button.top.Enabled = False

    if widget.Button.createBrowserSource.Name in update_widget_for_props_name:
        widget.Button.createBrowserSource.Visible = True
        widget.Button.createBrowserSource.Enabled = True

    # 在现有的控件属性设置部分添加移除按钮的设置
    if widget.Button.removeBrowserSource.Name in update_widget_for_props_name:
        widget.Button.removeBrowserSource.Visible = True
        widget.Button.removeBrowserSource.Enabled = True

    if widget.DigitalDisplay.browserWidth.Name in update_widget_for_props_name:
        widget.DigitalDisplay.browserWidth.Visible = True
        widget.DigitalDisplay.browserWidth.Enabled = True
        widget.DigitalDisplay.browserWidth.Value = 1280
        widget.DigitalDisplay.browserWidth.Min = 1
        widget.DigitalDisplay.browserWidth.Max = 4090
        widget.DigitalDisplay.browserWidth.Step = 1

    if widget.DigitalDisplay.browserHeight.Name in update_widget_for_props_name:
        widget.DigitalDisplay.browserHeight.Visible = True
        widget.DigitalDisplay.browserHeight.Enabled = True
        widget.DigitalDisplay.browserHeight.Value = 720
        widget.DigitalDisplay.browserHeight.Min = 1
        widget.DigitalDisplay.browserHeight.Max = 4090
        widget.DigitalDisplay.browserHeight.Step = 1

    if widget.DigitalDisplay.browserFps.Name in update_widget_for_props_name:
        widget.DigitalDisplay.browserFps.Visible = True
        widget.DigitalDisplay.browserFps.Enabled = True
        widget.DigitalDisplay.browserFps.Value = 0
        widget.DigitalDisplay.browserFps.Min = 0
        widget.DigitalDisplay.browserFps.Max = 60
        widget.DigitalDisplay.browserFps.Step = 1

    if widget.TextBox.browserSourceName.Name in update_widget_for_props_name:
        widget.TextBox.browserSourceName.Visible = True
        widget.TextBox.browserSourceName.Enabled = True
        widget.TextBox.browserSourceName.Text = "Python浏览器源"

    if widget.TextBox.browserUrl.Name in update_widget_for_props_name:
        widget.TextBox.browserUrl.Visible = True
        widget.TextBox.browserUrl.Enabled = True
        widget.TextBox.browserUrl.Text = "https://www.example.com"

    if widget.TextBox.browserCss.Name in update_widget_for_props_name:
        widget.TextBox.browserCss.Visible = True
        widget.TextBox.browserCss.Enabled = True
        widget.TextBox.browserCss.Text = "body { background-color: transparent; }"

    if widget.TextBox.infoText.Name in update_widget_for_props_name:
        widget.TextBox.infoText.Visible = True
        widget.TextBox.infoText.Enabled = True

    if widget.Button.bottom.Name in update_widget_for_props_name:
        widget.Button.bottom.Visible = False
        widget.Button.bottom.Enabled = False


def script_description():
    """脚本描述"""
    return ("OBS浏览器源创建脚本\n\n"
            "使用此脚本可以创建和配置浏览器源，并将其添加到当前场景中。\n"
            "支持自定义URL、尺寸、FPS和CSS样式。")


def script_load(settings):
    """
    在脚本启动时调用与脚本相关的特定设置。所提供的设置参数通常不用于由用户设置的设置;
    相反，该参数用于脚本中可能使用的任何额外的内部设置数据。
    :param settings:与脚本关联的设置。
    """
    log_save(obs.LOG_INFO, "已载入: bilibili_live")

    # 注册事件回调
    log_save(obs.LOG_INFO, "开始监视obs事件")
    obs.obs_frontend_add_event_callback(trigger_frontend_event)
    # obs_data_t 类型的数据对象。这个数据对象可以用来存储和管理设置项，例如场景、源或过滤器的配置信息
    # settings = obs.obs_data_create()


def script_update(settings):
    """脚本设置更新时调用"""
    # 这里可以添加设置更新时的处理逻辑
    pass


def script_properties():  # 建立控件
    """
    在脚本控制台中建立控件
    调用以定义与脚本关联的用户属性。这些属性用于定义如何向用户显示设置属性。
    通常用于自动生成用户界面小部件，也可以用来枚举特定设置的可用值或有效值。
    Returns:通过 obs_properties_create() 创建的 Obs_properties_t 对象
    obs_properties_t 类型的属性对象。这个属性对象通常用于枚举 libobs 对象的可用设置，
    """
    log_save(obs.LOG_INFO, f"")
    log_save(obs.LOG_INFO, f"╔{'═' * 20}构造控件体 开始{'═' * 20}╗")
    # 创建一个 OBS 属性集对象，他将包含所有控件对应的属性对象
    props_dict = {"props": obs.obs_properties_create()}
    """控件属性集的字典，仅在这里赋值一次，避免重复赋值导致溢出或者obs崩溃"""
    for props_name in widget.props_Collection:
        props_dict[props_name] = obs.obs_properties_create()

    for w in widget.get_sorted_controls():
        # 获取按载入次序排序的所有控件列表
        if w.ControlType == "CheckBox":
            # 添加复选框控件
            log_save(obs.LOG_INFO, f"复选框控件: {w.Name} 【{w.Description}】")
            obs.obs_properties_add_bool(props_dict[w.Props], w.Name, w.Description)
        elif w.ControlType == "DigitalDisplay":
            # 添加数字控件
            log_save(obs.LOG_INFO, f"数字框控件: {w.Name} 【{w.Description}】")
            if w.Type == "ThereIsASlider":  # 是否为数字控件添加滑动条
                w.Obj = obs.obs_properties_add_int_slider(props_dict[w.Props], w.Name, w.Description, w.Min, w.Max,
                                                          w.Step)
            else:
                w.Obj = obs.obs_properties_add_int(props_dict[w.Props], w.Name, w.Description, w.Min, w.Max, w.Step)
            obs.obs_property_int_set_suffix(w.Obj, w.Suffix)
        elif w.ControlType == "TextBox":
            # 添加文本框控件
            log_save(obs.LOG_INFO, f"文本框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_text(props_dict[w.Props], w.Name, w.Description, w.Type)
            if w.LongDescription:
                obs.obs_property_set_long_description(w.Obj, w.LongDescription)

        elif w.ControlType == "Button":
            # 添加按钮控件
            log_save(obs.LOG_INFO, f"按钮控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_button(props_dict[w.Props], w.Name, w.Description, w.Callback)
            obs.obs_property_button_set_type(w.Obj, w.Type)
            if w.Type == obs.OBS_BUTTON_URL:  # 是否为链接跳转按钮
                obs.obs_property_button_set_url(w.Obj, w.Url)
        elif w.ControlType == "ComboBox":
            # 添加组合框控件
            log_save(obs.LOG_INFO, f"组合框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_list(props_dict[w.Props], w.Name, w.Description, w.Type,
                                                obs.OBS_COMBO_FORMAT_STRING)
        elif w.ControlType == "PathBox":
            # 添加路径对话框控件
            log_save(obs.LOG_INFO, f"路径对话框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_path(props_dict[w.Props], w.Name, w.Description, w.Type, w.Filter,
                                                w.StartPath)
        elif w.ControlType == "Group":
            # 分组框控件
            log_save(obs.LOG_INFO, f"分组框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_group(props_dict[w.Props], w.Name, w.Description, w.Type,
                                                 props_dict[w.GroupProps])

        if w.ModifiedIs:
            log_save(obs.LOG_INFO, f"为{w.ControlType}: 【{w.Description}】添加钩子函数")
            obs.obs_property_set_modified_callback(w.Obj, lambda ps, p, st, name=w.Name: property_modified(name))

    GlobalVariableOfData.props_dict = props_dict
    # 更新UI界面数据#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
    update_ui_interface_data()
    log_save(obs.LOG_INFO, f"╚{'═' * 20}构造控件体 结束{'═' * 20}╝")
    log_save(obs.LOG_INFO, f"")
    return props_dict["props"]


def update_ui_interface_data():
    """
    更新UI界面数据
    Returns:
    """
    for w in widget.get_sorted_controls():
        if w.Props in GlobalVariableOfData.update_widget_for_props_dict:
            if w.Name in GlobalVariableOfData.update_widget_for_props_dict[w.Props]:
                if obs.obs_property_visible(w.Obj) != w.Visible:
                    obs.obs_property_set_visible(w.Obj, w.Visible)
                if obs.obs_property_enabled(w.Obj) != w.Enabled:
                    obs.obs_property_set_enabled(w.Obj, w.Enabled)
                log_save(obs.LOG_INFO, f"{w.Name}可见：{w.Visible}")
                log_save(obs.LOG_INFO, f"{w.Name}可用：{w.Visible}")

                if w.ControlType == "CheckBox":
                    if obs.obs_data_get_bool(GlobalVariableOfData.script_settings, w.Name) != w.Bool:
                        obs.obs_data_set_bool(GlobalVariableOfData.script_settings, w.Name, w.Bool)
                elif w.ControlType == "DigitalDisplay":
                    if w.Min != obs.obs_property_int_min(w.Obj) or w.Max != obs.obs_property_int_max(
                            w.Obj) or w.Step != obs.obs_property_int_step(w.Obj):
                        obs.obs_property_int_set_limits(w.Obj, w.Min, w.Max, w.Step)
                    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, w.Name) != w.Value:
                        obs.obs_data_set_int(GlobalVariableOfData.script_settings, w.Name, w.Value)
                elif w.ControlType == "TextBox":
                    if w.Type == obs.OBS_TEXT_INFO:
                        if obs.obs_property_text_info_type(w.Obj) != w.InfoType:
                            obs.obs_property_text_set_info_type(w.Obj, w.InfoType)
                    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Text:
                        obs.obs_data_set_string(GlobalVariableOfData.script_settings, w.Name, w.Text)
                elif w.ControlType == "Button":
                    pass
                elif w.ControlType == "ComboBox":
                    combo_box_option_dictionary = {}
                    for idx in range(obs.obs_property_list_item_count(w.Obj)):
                        combo_box_option_dictionary_key = obs.obs_property_list_item_string(w.Obj, idx)
                        combo_box_option_dictionary_value = obs.obs_property_list_item_name(w.Obj, idx)
                        combo_box_option_dictionary[combo_box_option_dictionary_key] = combo_box_option_dictionary_value
                    if w.Dictionary != combo_box_option_dictionary:
                        obs.obs_property_list_clear(w.Obj)
                        for common_area_id_dict_str in w.Dictionary:
                            if common_area_id_dict_str != w.Value:
                                obs.obs_property_list_add_string(
                                    w.Obj, w.Dictionary[common_area_id_dict_str], common_area_id_dict_str
                                )
                            else:
                                obs.obs_property_list_insert_string(w.Obj, 0, w.Text, w.Value)
                    if w.Type == obs.OBS_COMBO_TYPE_EDITABLE:
                        if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Text:
                            obs.obs_data_set_string(
                                GlobalVariableOfData.script_settings, w.Name, obs.obs_property_list_item_name(w.Obj, 0)
                            )
                    else:
                        if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Value:
                            obs.obs_data_set_string(
                                GlobalVariableOfData.script_settings, w.Name, obs.obs_property_list_item_string(w.Obj, 0)
                            )
                elif w.ControlType == "PathBox":
                    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Text:
                        obs.obs_data_set_string(GlobalVariableOfData.script_settings, w.Name, w.Text)
                elif w.ControlType == "Group":
                    if w.Type == obs.OBS_GROUP_CHECKABLE:
                        if obs.obs_data_get_bool(GlobalVariableOfData.script_settings, w.Name) != w.Bool:
                            obs.obs_data_set_bool(GlobalVariableOfData.script_settings, w.Name, w.Bool)
                        pass
    return True


def script_unload():
    """脚本卸载时调用"""
    print("浏览器源管理器脚本已卸载")


class ButtonFunction:
    """按钮回调函数"""

    @staticmethod
    def create_and_add_browser_source(*args):
        """创建并添加浏览器源的完整流程"""
        if len(args) == 2:
            props = args[0]
            prop = args[1]
        if len(args) == 3:
            settings = args[2]
        # 从脚本设置获取参数
        url = obs.obs_data_get_string(GlobalVariableOfData.script_settings, "browser_url")
        width = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "browser_width")
        height = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "browser_height")
        fps = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "browser_fps")
        source_name = obs.obs_data_get_string(GlobalVariableOfData.script_settings, "browser_source_name")
        css = obs.obs_data_get_string(GlobalVariableOfData.script_settings, "browser_css")
        # 如果FPS为0，则不设置自定义FPS
        if fps == 0:
            fps = None
        # 如果CSS为空，则不设置
        if not css or css.strip() == "":
            css = None
        # 创建浏览器源
        GlobalVariableOfData.browserSource = obs.obs_source_create("browser_source", source_name, None, None)
        if not GlobalVariableOfData.browserSource:
            print("错误: 未创建浏览器源")
            return False

        settings = obs.obs_data_create()

        # 基本设置
        obs.obs_data_set_string(settings, "url", url)
        obs.obs_data_set_int(settings, "width", width)
        obs.obs_data_set_int(settings, "height", height)

        # 可选设置
        if fps:
            obs.obs_data_set_bool(settings, "fps_custom", True)
            obs.obs_data_set_int(settings, "fps", fps)

        if css:
            obs.obs_data_set_string(settings, "css", css)

        # 其他常用设置
        obs.obs_data_set_bool(settings, "shutdown", False)  # 不关闭源
        obs.obs_data_set_bool(settings, "restart_when_active", True)  # 激活时重启

        # 应用设置
        obs.obs_source_update(GlobalVariableOfData.browserSource, settings)
        obs.obs_data_release(settings)

        print(f"浏览器源配置完成 - URL: {url}, 尺寸: {width}x{height}")
        if not GlobalVariableOfData.browserSource:
            print("错误: 未创建浏览器源")
            return False

        # 获取当前场景
        current_scene = obs.obs_frontend_get_current_scene()
        if not current_scene:
            print("无法获取当前场景")
            return False

        scene = obs.obs_scene_from_source(current_scene)
        if scene:
            # 添加到场景
            obs.obs_scene_add(scene, GlobalVariableOfData.browserSource)
            print(f"已将浏览器源 '{source_name}' 添加到当前场景")

            # 释放引用（场景现在持有源的引用）
            obs.obs_source_release(GlobalVariableOfData.browserSource)
            GlobalVariableOfData.browserSource = None
        else:
            print("无法获取场景对象")

        # 释放场景源
        obs.obs_source_release(current_scene)

        return True

    @staticmethod
    def remove_browser_source(*args):
        """移除浏览器源"""
        if len(args) == 2:
            props = args[0]
            prop = args[1]

        # 从脚本设置获取源名称
        _source_name = obs.obs_data_get_string(GlobalVariableOfData.script_settings, "browser_source_name")

        if not _source_name:
            log_save(obs.LOG_WARNING, "无法移除浏览器源：未指定源名称")
            return False

        # 获取当前场景
        current_scene = obs.obs_frontend_get_current_scene()
        if not current_scene:
            log_save(obs.LOG_WARNING, "无法获取当前场景")
            return False

        scene = obs.obs_scene_from_source(current_scene)
        if scene:
            # 获取场景中的所有场景项
            scene_items = obs.obs_scene_enum_items(scene)
            if scene_items:
                for item in scene_items:
                    source = obs.obs_sceneitem_get_source(item)
                    if source:
                        source_id = obs.obs_source_get_id(source)
                        # 检查是否为浏览器源
                        if source_id == "browser_source":
                            source_name = obs.obs_source_get_name(source)
                            if source_name:
                                log_save(obs.LOG_DEBUG, f"找到浏览器源: {source_name}")
                                if _source_name in source_name:
                                    log_save(obs.LOG_INFO, f"从场景中移除浏览器源: {source_name}")
                                    # 在场景中查找指定名称的源
                                    source = obs.obs_scene_find_source(scene, source_name)
                                    if source:
                                        # 从场景中移除源
                                        obs.obs_sceneitem_remove(source)
                                        log_save(obs.LOG_INFO, f"已从场景中移除浏览器源: {source_name}")
                # 释放场景项列表
                obs.sceneitem_list_release(scene_items)
        else:
            log_save(obs.LOG_WARNING, "无法获取场景对象")

        # 释放场景源
        obs.obs_source_release(current_scene)
        return True

# 创建控件表单
widget = Widget()

widget.widget_TextBox_dict = {
    "props": {
        "browserSourceName": {
            "Name": "browser_source_name",
            "Description": "源名称",
            "Type": obs.OBS_TEXT_DEFAULT,
            "ModifiedIs": False
        },
        "browserUrl": {
            "Name": "browser_url",
            "Description": "网页URL",
            "Type": obs.OBS_TEXT_DEFAULT,
            "ModifiedIs": False
        },
        "browserCss": {
            "Name": "browser_css",
            "Description": "自定义CSS",
            "LongDescription": "可选的CSS样式，用于修改浏览器源的外观",
            "Type": obs.OBS_TEXT_MULTILINE,
            "ModifiedIs": False
        },
        "infoText": {
            "Name": "info_text",
            "Description": "说明",
            "LongDescription": "点击'创建浏览器源'按钮将在当前场景中添加一个新的浏览器源。\n确保输入的URL是有效的，并且OBS有网络访问权限。",
            "Type": obs.OBS_TEXT_INFO,
            "ModifiedIs": False
        },
    },
}

widget.widget_Button_dict = {
    "props": {
        "top": {
            "Name": "top_button",
            "Description": "Top",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": lambda ps, p: log_save(obs.LOG_INFO, f"【{'顶部'}】按钮被触发"),
            "ModifiedIs": True
        },
        "createBrowserSource": {
            "Name": "create_browser_source",
            "Description": "创建浏览器源",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.create_and_add_browser_source,
            "ModifiedIs": False
        },
        "removeBrowserSource": {  # 新增的移除按钮
            "Name": "remove_browser_source",
            "Description": "移除浏览器源",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.remove_browser_source,
            "ModifiedIs": False
        },
        "bottom": {
            "Name": "bottom_button",
            "Description": "Bottom",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": lambda ps, p: log_save(obs.LOG_INFO, f"【{'底部'}】按钮被触发"),
            "ModifiedIs": True
        },
    },
}

widget.widget_DigitalDisplay_dict = {
    "props": {
        "browserWidth": {
            "Name": "browser_width",
            "Description": "宽度",
            "Type": "ThereIsASlider",
            "Suffix": "px",
            "ModifiedIs": True
        },
        "browserHeight": {
            "Name": "browser_height",
            "Description": "高度",
            "Type": "ThereIsASlider",
            "Suffix": "px",
            "ModifiedIs": True
        },
        "browserFps": {
            "Name": "browser_fps",
            "Description": "自定义FPS (0=默认)",
            "Type": "ThereIsAUnSlider",
            "Suffix": "",
            "ModifiedIs": True
        },
    },
}

widget.widget_list = [
    "top_button",
    "create_browser_source",
    "remove_browser_source",  # 新增的移除按钮
    "browser_width",
    "browser_height",
    "browser_fps",
    "browser_source_name",
    "browser_url",
    "browser_css",
    "info_text",
    "bottom_button",
]

widget.preliminary_configuration_control()

if widget.verification_number_controls:
    log_save(obs.LOG_INFO, "控件数量检测通过")
else:
    log_save(obs.LOG_ERROR, "⚾控件数量检测不通过：设定控件载入顺序时的控件数量 和 创建的控件对象数量 不统一")
