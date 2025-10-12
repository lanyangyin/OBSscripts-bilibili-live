# widget.py 开头部分
"""控件管理器 - 修复版本"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, Any, Dict, List, Iterator, Callable, Literal

# 动态导入OBS模块，提供降级方案
try:
    import obspython as obs

    script_version = "0.1.6"


    class GlobalVariableOfData:
        logRecording = ""  # #日志记录的文本


    def log_save(log_level: Literal[0, 1, 2, 3], log_str: str, print_is: bool = True) -> None:
        """
        输出并保存日志
        Args:
            print_is: 是否输出
            log_level: 日志等级

                0: "INFO",
                1: "DEBUG",
                2: "WARNING",
                3: "ERROR",
            log_str: 日志内容
        Returns: None
        """
        log_type = {
            0: obs.LOG_INFO,
            1: obs.LOG_DEBUG,
            2: obs.LOG_WARNING,
            3: obs.LOG_ERROR,
        }
        log_type_str = {
            0: "INFO",
            1: "DEBUG",
            2: "WARNING",
            3: "ERROR",
        }
        now = datetime.now()
        formatted = now.strftime("%Y/%m/%d %H:%M:%S")
        log_text = f"{script_version}【{formatted}】【{log_type_str[log_level]}】{log_str}"
        if print_is:
            obs.script_log(log_type[log_level], log_text)
        GlobalVariableOfData.logRecording += log_text + "\n"


    OBS_AVAILABLE = True
except ImportError:
    # 开发/测试环境下的模拟
    class obs:
        OBS_GROUP_CHECKABLE = 1
        OBS_GROUP_NORMAL = 0
        OBS_PATH_DIRECTORY = 0
        OBS_PATH_FILE_SAVE = 1
        OBS_PATH_FILE = 2
        OBS_COMBO_TYPE_RADIO = 2
        OBS_COMBO_TYPE_LIST = 1
        OBS_COMBO_TYPE_EDITABLE = 0
        OBS_BUTTON_URL = 1
        OBS_BUTTON_DEFAULT = 0
        OBS_TEXT_INFO = 3
        OBS_TEXT_MULTILINE = 2
        OBS_TEXT_PASSWORD = 1
        OBS_TEXT_DEFAULT = 0
        OBS_TEXT_INFO_NORMAL = 0
        OBS_TEXT_INFO_WARNING = 1
        OBS_TEXT_INFO_ERROR = 2


    def log_save(log_level: Literal[0, 1, 2, 3], log_str: str, print_is: bool = True) -> None:
        print(log_str)


    OBS_AVAILABLE = False
    logging.warning("obspython模块不可用，使用模拟模式")


# 配置日志
# logger = logging.getLogger("WidgetManager")

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional, Union, Any, Callable, Dict, List, Iterator, Set
from functools import wraps
import time


# 假设这些是 OBS 的常量
class obs:
    OBS_TEXT_DEFAULT = 0
    OBS_TEXT_PASSWORD = 1
    OBS_TEXT_MULTILINE = 2
    OBS_TEXT_INFO = 3
    OBS_TEXT_INFO_NORMAL = 0
    OBS_TEXT_INFO_WARNING = 1
    OBS_TEXT_INFO_ERROR = 2
    OBS_BUTTON_DEFAULT = 0
    OBS_BUTTON_URL = 1
    OBS_COMBO_TYPE_EDITABLE = 0
    OBS_COMBO_TYPE_LIST = 1
    OBS_COMBO_TYPE_RADIO = 2
    OBS_PATH_FILE = 0
    OBS_PATH_FILE_SAVE = 1
    OBS_PATH_DIRECTORY = 2
    OBS_GROUP_NORMAL = 0
    OBS_GROUP_CHECKABLE = 1


def validate_control_name(func: Callable) -> Callable:
    """验证控件名称的装饰器"""

    @wraps(func)
    def wrapper(self, name: str, *args, **kwargs):
        if not name or not isinstance(name, str):
            raise ValueError("控件名称必须是非空字符串")
        if not name.replace('_', '').isalnum():
            raise ValueError("控件名称只能包含字母、数字和下划线")
        if hasattr(self, name) and name not in ['add', 'get', 'remove']:
            raise ValueError(f"名称 '{name}' 与现有属性冲突")
        return func(self, name, *args, **kwargs)

    return wrapper


def cache_loading_result(func: Callable) -> Callable:
    """缓存载入结果的装饰器"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        force_refresh = kwargs.get('force', False)
        if not force_refresh and hasattr(self, '_cached_loading'):
            return self._cached_loading

        result = func(self, *args, **kwargs)
        self._cached_loading = result
        return result

    return wrapper


@dataclass
class ControlBase:
    """控件基类"""
    ControlType: str = "Base"
    Obj: Any = None
    Props: Any = None
    Number: int = 0
    Name: str = ""
    Description: str = ""
    Visible: bool = False
    Enabled: bool = False
    ModifiedIs: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """将控件转换为字典"""
        return asdict(self)

    def validate(self) -> List[str]:
        """验证控件数据的有效性，返回错误信息列表"""
        errors = []
        if not self.Name.strip():
            errors.append("控件名称不能为空")
        if self.Number < 0:
            errors.append("载入次序不能为负数")
        return errors


class Widget:
    """表单管理器，管理所有控件"""

    class ControlManagerBase:
        """控件管理器基类（内部使用）"""

        def __init__(self, control_class: type):
            self._control_class = control_class
            self._controls: Dict[str, Any] = {}
            self._loading_order: List[Any] = []
            self._used_numbers: Set[int] = set()

        @validate_control_name
        def add(self, name: str, **kwargs) -> Any:
            """添加控件的通用实现"""
            if name in self._controls:
                existing = self._controls[name]
                raise ValueError(
                    f"控件 '{name}' 已存在 "
                    f"(类型: {type(existing).__name__}, 载入次序: {existing.Number})"
                )

            # 验证 Number 唯一性
            number = kwargs.get('Number', 0)
            if number in self._used_numbers:
                raise ValueError(f"载入次序 {number} 已被使用")

            if "Name" not in kwargs:
                kwargs["Name"] = name

            control = self._control_class(**kwargs)

            # 数据验证
            if errors := control.validate():
                raise ValueError(f"控件数据无效: {', '.join(errors)}")

            self._controls[name] = control
            self._loading_order.append(control)
            self._used_numbers.add(number)
            setattr(self, name, control)

            # 触发事件
            if hasattr(self, '_parent_widget'):
                self._parent_widget._trigger_event('control_added', control)

            return control

        def get(self, name: str) -> Optional[Any]:
            """获取控件"""
            return self._controls.get(name)

        def remove(self, name: str) -> bool:
            """移除控件"""
            if name in self._controls:
                control = self._controls.pop(name)
                if hasattr(self, name):
                    delattr(self, name)
                if control in self._loading_order:
                    self._loading_order.remove(control)
                if control.Number in self._used_numbers:
                    self._used_numbers.remove(control.Number)

                # 触发事件
                if hasattr(self, '_parent_widget'):
                    self._parent_widget._trigger_event('control_removed', control)

                return True
            return False

        def __iter__(self) -> Iterator[Any]:
            return iter(self._controls.values())

        def __len__(self) -> int:
            return len(self._controls)

        def __contains__(self, name: str) -> bool:
            return name in self._controls

        def get_loading_order(self) -> List[Any]:
            return sorted(self._loading_order, key=lambda c: c.Number)

        def add_multiple(self, controls_config: List[Dict]) -> List[Any]:
            """批量添加控件"""
            results = []
            for config in controls_config:
                name = config.pop('name')
                results.append(self.add(name, **config))
            return results

        def remove_multiple(self, names: List[str]) -> List[bool]:
            """批量移除控件"""
            return [self.remove(name) for name in names]

        def find(self, **filters) -> List[Any]:
            """根据属性值查找控件"""
            results = []
            for control in self._controls.values():
                match = True
                for key, value in filters.items():
                    if not hasattr(control, key) or getattr(control, key) != value:
                        match = False
                        break
                if match:
                    results.append(control)
            return results

        def to_dict(self) -> Dict[str, Any]:
            """将管理器状态序列化"""
            return {name: control.to_dict() for name, control in self._controls.items()}

    class CheckBoxPs(ControlManagerBase):
        """复选框控件管理器"""

        @dataclass
        class CheckBoxP(ControlBase):
            """复选框控件实例"""
            ControlType: str = "CheckBox"
            Bool: bool = False

            def __repr__(self) -> str:
                type_name = "未知类复选框"
                return f"<CheckBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Bool={self.Bool}>"

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.CheckBoxPs.CheckBoxP)
            self._parent_widget = parent_widget

    class DigitalDisplayPs(ControlManagerBase):
        """数字框控件管理器"""

        @dataclass
        class DigitalDisplayP(ControlBase):
            """数字框控件实例"""
            ControlType: str = "DigitalDisplay"
            SliderIs: bool = False
            Value: int = 0
            Suffix: str = ""
            Min: int = 0
            Max: int = 0
            Step: int = 0

            def __repr__(self) -> str:
                type_name = "滑块数字框" if self.SliderIs else "普通数字框"
                return f"<DigitalDisplayP Name='{self.Name}' Number={self.Number} Type='{type_name}' Min={self.Min} Max={self.Max}>"

            def validate(self) -> List[str]:
                errors = super().validate()
                if self.Min > self.Max:
                    errors.append("最小值不能大于最大值")
                if self.Value < self.Min or self.Value > self.Max:
                    errors.append("当前值必须在最小值和最大值之间")
                if self.Step <= 0:
                    errors.append("步长必须大于0")
                return errors

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.DigitalDisplayPs.DigitalDisplayP)
            self._parent_widget = parent_widget

    class TextBoxPs(ControlManagerBase):
        """文本框控件管理器"""

        @dataclass
        class TextBoxP(ControlBase):
            """文本框控件实例"""
            ControlType: str = "TextBox"
            Type: Optional[int] = None
            Text: str = ""
            InfoType: Optional[int] = None

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

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.TextBoxPs.TextBoxP)
            self._parent_widget = parent_widget

    class ButtonPs(ControlManagerBase):
        """按钮控件管理器"""

        @dataclass
        class ButtonP(ControlBase):
            """按钮控件实例"""
            ControlType: str = "Button"
            Type: Optional[int] = None
            Callback: Optional[Callable] = None
            Url: str = ""

            def __repr__(self) -> str:
                type_name = "未知类按钮"
                if self.Type == obs.OBS_BUTTON_DEFAULT:
                    type_name = "标准按钮"
                elif self.Type == obs.OBS_BUTTON_URL:
                    type_name = "打开 URL 的按钮"
                return f"<ButtonP Name='{self.Name}' Number={self.Number} Type='{type_name}' Callback={self.Callback is not None}>"

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.ButtonPs.ButtonP)
            self._parent_widget = parent_widget

    class ComboBoxPs(ControlManagerBase):
        """组合框控件管理器"""

        @dataclass
        class ComboBoxP(ControlBase):
            """组合框控件实例"""
            ControlType: str = "ComboBox"
            Type: Optional[int] = None
            Text: str = ""
            Value: str = ""
            Dictionary: Dict[str, Any] = field(default_factory=dict)

            def __repr__(self) -> str:
                type_name = "未知类组合框"
                if self.Type == obs.OBS_COMBO_TYPE_EDITABLE:
                    type_name = "可以编辑。 仅与字符串列表一起使用"
                elif self.Type == obs.OBS_COMBO_TYPE_LIST:
                    type_name = "不可编辑。显示为组合框"
                elif self.Type == obs.OBS_COMBO_TYPE_RADIO:
                    type_name = "不可编辑。显示为单选按钮"
                return f"<ComboBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Text='{self.Text}'>"

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.ComboBoxPs.ComboBoxP)
            self._parent_widget = parent_widget

    class PathBoxPs(ControlManagerBase):
        """路径对话框控件管理器"""

        @dataclass
        class PathBoxP(ControlBase):
            """路径对话框控件实例"""
            ControlType: str = "PathBox"
            Type: Optional[int] = None
            Text: str = ""
            Filter: str = ""
            StartPath: str = ""

            def __repr__(self) -> str:
                type_name = "未知类型路径对话框"
                if self.Type == obs.OBS_PATH_FILE:
                    type_name = "文件对话框"
                elif self.Type == obs.OBS_PATH_FILE_SAVE:
                    type_name = "保存文件对话框"
                elif self.Type == obs.OBS_PATH_DIRECTORY:
                    type_name = "文件夹对话框"
                return f"<PathBoxP Name='{self.Name}' Number={self.Number} Type='{type_name}' Text='{self.Text}'>"

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.PathBoxPs.PathBoxP)
            self._parent_widget = parent_widget

    class GroupPs(ControlManagerBase):
        """分组框控件管理器"""

        @dataclass
        class GroupP(ControlBase):
            """分组框控件实例"""
            ControlType: str = "Group"
            Type: Optional[int] = None
            GroupProps: Any = None

            def __repr__(self) -> str:
                type_name = "未知类分组框"
                if self.Type == obs.OBS_GROUP_NORMAL:
                    type_name = "只有名称和内容的普通组"
                elif self.Type == obs.OBS_GROUP_CHECKABLE:
                    type_name = "具有复选框、名称和内容的可选组"
                return f"<GroupP Name='{self.Name}' Number={self.Number} Type='{type_name}'>"

        def __init__(self, parent_widget: Widget = None):
            super().__init__(Widget.GroupPs.GroupP)
            self._parent_widget = parent_widget

    def __init__(self):
        """初始化表单管理器"""
        # 初始化所有控件管理器，并传递 self 作为父引用
        self.CheckBox = Widget.CheckBoxPs(self)
        self.DigitalDisplay = Widget.DigitalDisplayPs(self)
        self.TextBox = Widget.TextBoxPs(self)
        self.Button = Widget.ButtonPs(self)
        self.ComboBox = Widget.ComboBoxPs(self)
        self.PathBox = Widget.PathBoxPs(self)
        self.Group = Widget.GroupPs(self)

        self._all_controls: List[Any] = []
        self._loading_dict: Dict[int, Any] = {}
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._last_update_time: float = 0

    def _update_all_controls(self) -> None:
        """更新所有控件列表"""
        self._all_controls = []
        managers = [
            self.CheckBox, self.DigitalDisplay, self.TextBox,
            self.Button, self.ComboBox, self.PathBox, self.Group
        ]
        for manager in managers:
            self._all_controls.extend(manager)
        self._last_update_time = time.time()

    @cache_loading_result
    def loading(self, force: bool = False) -> Dict[int, Any]:
        """按载入次序排序所有控件"""
        self._update_all_controls()

        sorted_controls = sorted(self._all_controls, key=lambda c: c.Number)
        name_dict = {}
        loading_dict = {}

        for control in sorted_controls:
            # 检查名称冲突
            if control.Name in name_dict:
                existing = name_dict[control.Name]
                raise ValueError(
                    f"控件名称冲突: '{control.Name}' "
                    f"(类型: {type(control).__name__}, 次序: {control.Number}) 与 "
                    f"'{existing.Name}' (类型: {type(existing).__name__}, 次序: {existing.Number}) 重名"
                )
            name_dict[control.Name] = control

            # 检查载入次序冲突
            if control.Number in loading_dict:
                existing = loading_dict[control.Number]
                raise ValueError(
                    f"载入次序冲突: '{control.Name}' (类型: {type(control).__name__}) 和 "
                    f"'{existing.Name}' (类型: {type(existing).__name__}) "
                    f"使用相同次序 {control.Number}"
                )
            loading_dict[control.Number] = control

        return loading_dict

    def get_control_by_number(self, number: int) -> Optional[Any]:
        """通过载入次序获取控件"""
        loading_dict = self.loading()
        return loading_dict.get(number)

    def get_control_by_name(self, name: str) -> Optional[Any]:
        """通过名称获取控件"""
        managers = [
            self.CheckBox, self.DigitalDisplay, self.TextBox,
            self.Button, self.ComboBox, self.PathBox, self.Group
        ]
        for manager in managers:
            if name in manager:
                return manager.get(name)
        return None

    def get_sorted_controls(self) -> List[Any]:
        """获取按载入次序排序的所有控件列表"""
        loading_dict = self.loading()
        return list(loading_dict.values())

    def find_controls(self, **filters) -> List[Any]:
        """在所有控件中查找符合条件的控件"""
        self._update_all_controls()
        results = []
        for control in self._all_controls:
            match = True
            for key, value in filters.items():
                if not hasattr(control, key) or getattr(control, key) != value:
                    match = False
                    break
            if match:
                results.append(control)
        return results

    def get_controls_by_type(self, control_type: type) -> List[Any]:
        """按类型获取控件"""
        self._update_all_controls()
        return [c for c in self._all_controls if isinstance(c, control_type)]

    def validate_all_controls(self) -> Dict[str, List[str]]:
        """验证所有控件的有效性"""
        errors = {}
        self._update_all_controls()
        for control in self._all_controls:
            if control_errors := control.validate():
                errors[control.Name] = control_errors
        return errors

    def to_dict(self) -> Dict[str, Any]:
        """将整个表单序列化为字典"""
        return {
            'checkboxes': self.CheckBox.to_dict(),
            'digital_displays': self.DigitalDisplay.to_dict(),
            'text_boxes': self.TextBox.to_dict(),
            'buttons': self.Button.to_dict(),
            'combo_boxes': self.ComboBox.to_dict(),
            'path_boxes': self.PathBox.to_dict(),
            'groups': self.Group.to_dict(),
            'sorted_controls': [c.to_dict() for c in self.get_sorted_controls()]
        }

    def on_control_added(self, handler: Callable) -> None:
        """注册控件添加事件处理器"""
        self._add_event_handler('control_added', handler)

    def on_control_removed(self, handler: Callable) -> None:
        """注册控件移除事件处理器"""
        self._add_event_handler('control_removed', handler)

    def _add_event_handler(self, event_type: str, handler: Callable) -> None:
        """添加事件处理器"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    def _trigger_event(self, event_type: str, *args, **kwargs) -> None:
        """触发事件"""
        for handler in self._event_handlers.get(event_type, []):
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"事件处理器执行失败: {e}")

    def clean(self) -> Widget:
        """清除所有控件并重置表单"""
        # 重置所有控件管理器
        self.CheckBox = Widget.CheckBoxPs(self)
        self.DigitalDisplay = Widget.DigitalDisplayPs(self)
        self.TextBox = Widget.TextBoxPs(self)
        self.Button = Widget.ButtonPs(self)
        self.ComboBox = Widget.ComboBoxPs(self)
        self.PathBox = Widget.PathBoxPs(self)
        self.Group = Widget.GroupPs(self)

        # 清空内部存储
        self._all_controls = []
        self._loading_dict = {}
        if hasattr(self, '_cached_loading'):
            delattr(self, '_cached_loading')

        return self

    def __repr__(self) -> str:
        """返回表单的可读表示形式"""
        self._update_all_controls()
        control_counts = {
            'CheckBox': len(self.CheckBox),
            'DigitalDisplay': len(self.DigitalDisplay),
            'TextBox': len(self.TextBox),
            'Button': len(self.Button),
            'ComboBox': len(self.ComboBox),
            'PathBox': len(self.PathBox),
            'Group': len(self.Group)
        }
        return f"<Widget total_controls={len(self._all_controls)}, {control_counts}>"

if __name__ == "__main__":
    # 创建控件表单
    widget = Widget()

    widget_Button_name_list: Dict[str, set[str]] = {
        "props": {
            "top", "bottom",
        },
        "account_props": {
            "login", "accountListUpdate", "qrAddAccount", "qrPictureDisplay", "accountDelete", "accountBackup",
            "accountRestore", "logout",
        },
        "room_props": {
            "roomOpened", "roomCoverView", "roomCoverUpdate", "roomCommonTitlesTrue", "roomTitleChange",
            "roomNewsChange",
            "roomCommonAreasTrue", "roomParentAreaTrue", "roomSubAreaTrue", "bliveWebJump",
        },
        "live_props": {
            "liveFaceAuth", "liveStart", "liveRtmpAddressCopy", "liveRtmpCodeCopy", "liveRtmpCodeUpdate", "liveStop",
            "liveBookingsDayTrue", "liveBookingsHourTrue", "liveBookingsMinuteTrue", "liveBookingsCreate",
            "liveBookingsCancel", },
    }

    widget_Group_name_list: Dict[str, set[str]] = {
        "props": {
            "account",
            "room",
            "live",
        },
    }

    widget_TextBox_name_list: Dict[str, set[str]] = {
        "account_props": {
            "loginStatus",
        },
        "room_props": {
            "roomStatus", "roomTitle", "roomNews",
        },
        "live_props": {
            "liveBookingsTitle",
        },
    }

    widget_ComboBox_name_list: Dict[str, set[str]] = {
        "account_props": {
            "uid",
        },
        "room_props": {
            "roomCommonTitles", "roomCommonAreas", "roomParentArea", "roomSubArea",
        },
        "live_props": {
            "liveStreamingPlatform", "liveBookings",
        },
    }

    widget_PathBox_name_list: Dict[str, set[str]] = {
        "room_props": {
            "roomCover",
        },
    }

    widget_DigitalDisplay_name_list: Dict[str, set[str]] = {
        "live_props": {
            "liveBookingsDay", "liveBookingsHour", "liveBookingsMinute",
        },
    }

    widget_CheckBox_name_list: Dict[str, set[str]] = {
        "live_props": {
            "liveBookingsDynamic",
        },
    }

    for P in widget_Button_name_list:
        log_save(0, "【按钮】")
        for Button_name in widget_Button_name_list[P]:
            widget.Button.add(Button_name)
            log_save(0, f"添加{Button_name}")
            obj = getattr(widget.Button, Button_name)
            obj.Props = P

    for P in widget_Group_name_list:
        log_save(0, "【分组框】")
        for Group_name in widget_Group_name_list[P]:
            widget.Group.add(Group_name)
            log_save(0, f"添加{Group_name}")
            obj = getattr(widget.Group, Group_name)
            obj.Props = P

    for P in widget_TextBox_name_list:
        log_save(0, "【文本框】")
        for TextBox_name in widget_TextBox_name_list[P]:
            widget.TextBox.add(TextBox_name)
            log_save(0, f"添加{TextBox_name}")
            obj = getattr(widget.TextBox, TextBox_name)
            obj.Props = P

    for P in widget_ComboBox_name_list:
        log_save(0, "【组合框】")
        for ComboBox_name in widget_ComboBox_name_list[P]:
            widget.ComboBox.add(ComboBox_name)
            log_save(0, f"添加{ComboBox_name}")
            obj = getattr(widget.ComboBox, ComboBox_name)
            obj.Props = P

    for P in widget_PathBox_name_list:
        log_save(0, "【路径对话框】")
        for PathBox_name in widget_PathBox_name_list[P]:
            widget.PathBox.add(PathBox_name)
            log_save(0, f"添加{PathBox_name}")
            obj = getattr(widget.PathBox, PathBox_name)
            obj.Props = P

    for P in widget_DigitalDisplay_name_list:
        log_save(0, "【数字框】")
        for DigitalDisplay_name in widget_DigitalDisplay_name_list[P]:
            widget.DigitalDisplay.add(DigitalDisplay_name)
            log_save(0, f"添加{DigitalDisplay_name}")
            obj = getattr(widget.DigitalDisplay, DigitalDisplay_name)
            obj.Props = P

    for P in widget_CheckBox_name_list:
        log_save(0, "【复选框】")
        for CheckBox_name in widget_CheckBox_name_list[P]:
            widget.CheckBox.add(CheckBox_name)
            log_save(0, f"添加{CheckBox_name}")
            obj = getattr(widget.CheckBox, CheckBox_name)
            obj.Props = P


    class GlobalVariableOfData:
        widget_loading_number = 0


    w_list = [
        widget.Button.top,
        widget.Group.account,
        widget.TextBox.loginStatus,
        widget.ComboBox.uid,
        widget.Button.login,
        widget.Button.accountListUpdate,
        widget.Button.qrAddAccount,
        widget.Button.qrPictureDisplay,
        widget.Button.accountDelete,
        widget.Button.accountBackup,
        widget.Button.accountRestore,
        widget.Button.logout,
        widget.Group.room,
        widget.TextBox.roomStatus,
        widget.Button.roomOpened,
        widget.Button.roomCoverView,
        widget.PathBox.roomCover,
        widget.Button.roomCoverUpdate,
        widget.ComboBox.roomCommonTitles,
        widget.Button.roomCommonTitlesTrue,
        widget.TextBox.roomTitle,
        widget.Button.roomTitleChange,
        widget.TextBox.roomNews,
        widget.Button.roomNewsChange,
        widget.ComboBox.roomCommonAreas,
        widget.Button.roomCommonAreasTrue,
        widget.ComboBox.roomParentArea,
        widget.Button.roomParentAreaTrue,
        widget.ComboBox.roomSubArea,
        widget.Button.roomSubAreaTrue,
        widget.Button.bliveWebJump,
        widget.Group.live,
        widget.Button.liveFaceAuth,
        widget.ComboBox.liveStreamingPlatform,
        widget.Button.liveStart,
        widget.Button.liveRtmpAddressCopy,
        widget.Button.liveRtmpCodeCopy,
        widget.Button.liveRtmpCodeUpdate,
        widget.Button.liveStop,
        widget.DigitalDisplay.liveBookingsDay,
        widget.Button.liveBookingsDayTrue,
        widget.DigitalDisplay.liveBookingsHour,
        widget.Button.liveBookingsHourTrue,
        widget.DigitalDisplay.liveBookingsMinute,
        widget.Button.liveBookingsMinuteTrue,
        widget.CheckBox.liveBookingsDynamic,
        widget.TextBox.liveBookingsTitle,
        widget.Button.liveBookingsCreate,
        widget.ComboBox.liveBookings,
        widget.Button.liveBookingsCancel,
        widget.Button.bottom,
    ]

    for w in w_list:
        w.Number = (
            lambda v: (setattr(GlobalVariableOfData, 'widget_loading_number', v + 1), v)[1]
        )(GlobalVariableOfData.widget_loading_number)

    if len(w_list) == len(widget.get_sorted_controls()):
        log_save(0, "控件数量检测通过")
    else:
        log_save(3, "⚾控件数量检测不通过：设定控件载入顺序时的控件数量 和 创建的控件对象数量 不统一")

    # 创建一个 OBS 属性集对象，他将包含所有控件对应的属性对象
    props = "obs.obs_properties_create(props)"
    # 为 分组框【配置】 建立属性集
    account_props = "obs.obs_properties_create(account_props)"
    # 为 分组框【直播间】 建立属性集
    room_props = "obs.obs_properties_create(room_props)"
    # 为 分组框【直播】 建立属性集
    live_props = "obs.obs_properties_create(live_props)"

    props_dict = {
        "props": props,
        "account_props": account_props,
        "room_props": room_props,
        "live_props": live_props,
    }
    """控件属性集的字典，仅在这里赋值一次，避免重复赋值导致溢出或者obs崩溃"""
    for w in widget.get_sorted_controls():
        if w.ControlType == "Group":
            w.Props = props_dict[{
                "account": "account_props",
                "room": "room_props",
                "live": "live_props",
            }[w.Name]]
