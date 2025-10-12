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

@dataclass
class ControlBase:
    """控件基类"""
    ControlType: str = "Base"
    """控件的基本类型"""
    Obj: Any = None
    """控件的obs对象"""
    Props: Union[str, Any] = None
    """控件属于哪个属性集"""
    Number: int = 0
    """控件的加载顺序数"""
    Name: str = ""
    """控件的唯一名"""
    Description: str = ""
    """控件显示给用户的信息"""
    Visible: bool = False
    """控件的可见状态"""
    Enabled: bool = False
    """控件的可用状态"""
    ModifiedIs: bool = False
    """控件变动是否触发钩子函数"""


class Widget:
    """表单管理器，管理所有控件"""

    class CheckBoxPs:
        """复选框控件管理器"""

        @dataclass
        class CheckBoxP(ControlBase):
            """复选框控件实例"""
            ControlType: str = "CheckBox"
            Bool: bool = False

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
            SliderIs: bool = False
            Value: int = 0
            Suffix: str = ""
            Min: int = 0
            Max: int = 0
            Step: int = 0

            def __repr__(self) -> str:
                type_name = "滑块数字框" if self.SliderIs else "普通数字框"
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
            Type: Optional[int] = None  # 文本框类型
            Text: str = ""
            InfoType: Optional[int] = None  # 信息类型

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
            Type: Optional[int] = None  # 按钮类型
            Callback: Optional[Callable] = None  # 回调函数
            Url: str = ""  # 需要打开的 URL

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
            Type: Optional[int] = None  # 组合框类型
            Text: str = ""
            Value: str = ""
            Dictionary: Dict[str, Any] = field(default_factory=dict)  # 数据字典

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
            Type: Optional[int] = None  # 路径对话框类型
            Text: str = ""
            Filter: str = ""  # 文件种类（筛选条件）
            StartPath: str = ""  # 对话框起始路径

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
            """分组框的控件类型为 Group"""
            Type: Optional[int] = None  # 分组框类型
            """分组框的类型为 """
            GroupProps: Any = None  # 统辖属性集

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
        self._all_controls: List[Any] = []
        self._loading_dict: Dict[int, Any] = {}

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

    def preliminary_configuration_control(self, basic_types_controls: Literal["Button", "Group", "TextBox", "ComboBox", "PathBox", "DigitalDisplay", "CheckBox"], widget_name_dict: Dict[str, Dict[str, Dict[str, str]]], widget_list: List[str]):
        """
        创建初始控件
        Args:
            basic_types_controls: 控件的基本类型
            widget_name_dict: 控件的对象名和唯一名
            widget_list: 一个用于规定控件加载顺序的列表

        Returns:

        """
        log_save(0, f"{basic_types_controls}")
        for Ps in widget_name_dict:
            log_save(0, f"  {Ps}")
            for name in widget_name_dict[Ps]:
                widget_types_controls = getattr(self, basic_types_controls)
                widget_types_controls.add(name)
                log_save(0, f"      添加{name}")
                obj = getattr(widget_types_controls, name)
                obj.Name = widget_name_dict[Ps][name]["Name"]
                obj.Number = widget_list.index(obj.Name)
                obj.Description = widget_name_dict[Ps][name]["Description"]
                obj.Props = Ps

    def __repr__(self) -> str:
        """返回表单的可读表示形式"""
        self._update_all_controls()
        return f"<Widget controls={len(self._all_controls)}>"


if __name__ == "__main__":
    # 创建控件表单
    widget = Widget()

    widget_Button_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "props": {
            "top": {
                "Name": "top_button",
                "Description": "Top",
            },
            "bottom": {
                "Name": "bottom_button",
                "Description": "Bottom",
            },
        },
        "account_props": {
            "login": {
                "Name": "login_button",
                "Description": "登录账号",
            },
            "accountListUpdate": {
                "Name": "account_list_update_button",
                "Description": "更新账号列表",
            },
            "qrAddAccount": {
                "Name": "qr_add_account_button",
                "Description": "二维码添加账户",
            },
            "qrPictureDisplay": {
                "Name": "qr_picture_display_button",
                "Description": "显示二维码图片",
            },
            "accountDelete": {
                "Name": "account_delete_button",
                "Description": "删除账户",
            },
            "accountBackup": {
                "Name": "account_backup_button",
                "Description": "备份账户",
            },
            "accountRestore": {
                "Name": "account_restore_button",
                "Description": "恢复账户",
            },
            "logout": {
                "Name": "logout_button",
                "Description": "登出账号",
            },
        },
        "room_props": {
            "roomOpened": {
                "Name": "room_opened_button",
                "Description": "开通直播间",
            },
            "roomCoverView": {
                "Name": "room_cover_view_button",
                "Description": "查看直播间封面",
            },
            "roomCoverUpdate": {
                "Name": "room_cover_update_button",
                "Description": "上传直播间封面",
            },
            "roomCommonTitlesTrue": {
                "Name": "room_commonTitles_true_button",
                "Description": "确认标题",
            },
            "roomTitleChange": {
                "Name": "room_title_change_button",
                "Description": "更改直播间标题",
            },
            "roomNewsChange": {
                "Name": "room_news_change_button",
                "Description": "更改直播间公告",
            },
            "roomCommonAreasTrue": {
                "Name": "room_commonAreas_true_button",
                "Description": "确认分区",
            },
            "roomParentAreaTrue": {
                "Name": "room_parentArea_true_button",
                "Description": "确认一级分区",
            },
            "roomSubAreaTrue": {
                "Name": "room_subArea_true_button",
                "Description": "「确认分区」",
            },
            "bliveWebJump": {
                "Name": "blive_web_jump_button",
                "Description": "跳转直播间后台网页",
            },
        },
        "live_props": {
            "liveFaceAuth": {
                "Name": "live_face_auth_button",
                "Description": "人脸认证",
            },
            "liveStart": {
                "Name": "live_start_button",
                "Description": "开始直播并复制推流码",
            },
            "liveRtmpAddressCopy": {
                "Name": "live_rtmp_address_copy_button",
                "Description": "复制直播服务器",
            },
            "liveRtmpCodeCopy": {
                "Name": "live_rtmp_code_copy_button",
                "Description": "复制直播推流码",
            },
            "liveRtmpCodeUpdate": {
                "Name": "live_rtmp_code_update_button",
                "Description": "更新推流码并复制",
            },
            "liveStop": {
                "Name": "live_stop_button",
                "Description": "结束直播",
            },
            "liveBookingsDayTrue": {
                "Name": "live_bookings_day_true_button",
                "Description": "确认预约天",
            },
            "liveBookingsHourTrue": {
                "Name": "live_bookings_hour_true_button",
                "Description": "确认预约时",
            },
            "liveBookingsMinuteTrue": {
                "Name": "live_bookings_minute_true_button",
                "Description": "确认预约分",
            },
            "liveBookingsCreate": {
                "Name": "live_bookings_create_button",
                "Description": "发布直播预约",
            },
            "liveBookingsCancel": {
                "Name": "live_bookings_cancel_button",
                "Description": "取消直播预约",
            },
        },
    }
    """按钮控件名称列表"""

    widget_Group_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "props": {
            "account": {
                "Name": "account_group",
                "Description": "账号",
            },
            "room": {
                "Name": "room_group",
                "Description": "直播间",
            },
            "live": {
                "Name": "live_group",
                "Description": "直播",
            },
        },
    }
    """分组框控件名称列表"""

    widget_TextBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "account_props": {
            "loginStatus": {
                "Name": "login_status_textBox",
                "Description": "登录状态",
            },
        },
        "room_props": {
            "roomStatus": {
                "Name": "room_status_textBox",
                "Description": "查看直播间封面",
            },
            "roomTitle": {
                "Name": "room_title_textBox",
                "Description": "直播间标题",
            },
            "roomNews": {
                "Name": "room_news_textBox",
                "Description": "直播间公告",
            },
        },
        "live_props": {
            "liveBookingsTitle": {
                "Name": "live_bookings_title_textBox",
                "Description": "直播预约标题",
            },
        },
    }
    """文本框控件名称列表"""

    widget_ComboBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "account_props": {
            "uid": {
                "Name": "uid_comboBox",
                "Description": "用户",
            },
        },
        "room_props": {
            "roomCommonTitles": {
                "Name": "room_commonTitles_comboBox",
                "Description": "常用标题",
            },
            "roomCommonAreas": {
                "Name": "room_commonAreas_comboBox",
                "Description": "常用分区",
            },
            "roomParentArea": {
                "Name": "room_parentArea_comboBox",
                "Description": "一级分区",
            },
            "roomSubArea": {
                "Name": "room_subArea_comboBox",
                "Description": "二级分区",
            },
        },
        "live_props": {
            "liveStreamingPlatform": {
                "Name": "live_streaming_platform_comboBox",
                "Description": "直播平台",
            },
            "liveBookings": {
                "Name": "live_bookings_comboBox",
                "Description": "直播预约列表",
            },
        },
    }
    """组合框控件名称列表"""

    widget_PathBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "room_props": {
            "roomCover": {
                "Name": "room_cover_fileDialogBox",
                "Description": "直播间封面",
            },
        },
    }
    """路径对话框控件名称列表"""

    widget_DigitalDisplay_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "live_props": {
            "liveBookingsDay": {
                "Name": "live_bookings_day_digitalSlider",
                "Description": "预约天",
            },
            "liveBookingsHour": {
                "Name": "live_bookings_hour_digitalSlider",
                "Description": "预约时",
            },
            "liveBookingsMinute": {
                "Name": "live_bookings_minute_digitalSlider",
                "Description": "预约分",
            },
        },
    }
    """数字框控件名称列表"""

    widget_CheckBox_dict: Dict[str, Dict[str, Dict[str, str]]] = {
        "live_props": {
            "liveBookingsDynamic": {
                "Name": "live_bookings_dynamic_checkBox",
                "Description": "是否发直播预约动态",
            },
        },
    }
    """复选框控件名称列表"""

    widget_name_dict_all: dict[Literal["Button", "Group", "TextBox", "ComboBox", "PathBox", "DigitalDisplay", "CheckBox"], dict[str, dict[str, dict[str, str]]]] = {
        "Button": widget_Button_dict,
        "Group": widget_Group_dict,
        "TextBox": widget_TextBox_dict,
        "ComboBox": widget_ComboBox_dict,
        "PathBox": widget_PathBox_dict,
        "DigitalDisplay": widget_DigitalDisplay_dict,
        "CheckBox": widget_CheckBox_dict,
    }

    w_list: List[str] = [
        "top_button",
        "account_group",
        "login_status_textBox",
        "uid_comboBox",
        "login_button",
        "account_list_update_button",
        "qr_add_account_button",
        "qr_picture_display_button",
        "account_delete_button",
        "account_backup_button",
        "account_restore_button",
        "logout_button",
        "room_group",
        "room_status_textBox",
        "room_opened_button",
        "room_cover_view_button",
        "room_cover_fileDialogBox",
        "room_cover_update_button",
        "room_commonTitles_comboBox",
        "room_commonTitles_true_button",
        "room_title_textBox",
        "room_title_change_button",
        "room_news_textBox",
        "room_news_change_button",
        "room_commonAreas_comboBox",
        "room_commonAreas_true_button",
        "room_parentArea_comboBox",
        "room_parentArea_true_button",
        "room_subArea_comboBox",
        "room_subArea_true_button",
        "blive_web_jump_button",
        "live_group",
        "live_face_auth_button",
        "live_streaming_platform_comboBox",
        "live_start_button",
        "live_rtmp_address_copy_button",
        "live_rtmp_code_copy_button",
        "live_rtmp_code_update_button",
        "live_stop_button",
        "live_bookings_day_digitalSlider",
        "live_bookings_day_true_button",
        "live_bookings_hour_digitalSlider",
        "live_bookings_hour_true_button",
        "live_bookings_minute_digitalSlider",
        "live_bookings_minute_true_button",
        "live_bookings_dynamic_checkBox",
        "live_bookings_title_textBox",
        "live_bookings_create_button",
        "live_bookings_comboBox",
        "live_bookings_cancel_button",
        "bottom_button",
    ]

    for P in widget_name_dict_all:
        widget.preliminary_configuration_control(P, widget_name_dict_all[P], w_list)

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
        log_save(0, w.Name)
