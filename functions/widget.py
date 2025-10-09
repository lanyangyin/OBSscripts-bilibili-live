# 控件默认属性（首字母大写）
from typing import Optional, Union, Any, Dict, List, Iterator, Callable

import obspython as obs

DefaultPropertiesOfTheControl: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "ControlType": "Base",  # 添加类型标识
    "Obj": None,  # 控件脚本对象
    "Props": None,  # 隶属属性集
    "Number": 0,  # 载入次序
    "Name": "",  # 唯一名称
    "Description": "",  # 说明文本
    "Visible": False,  # 可见状态
    "Enabled": False,  # 可用状态
    "ModifiedIs": False,  # 是否监听
}

# ️复选框控件
CheckBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "CheckBox",  # 设置具体类型
    "Bool": False,  # 复选框是否选中
}


# ️数字框控件
DigitalDisplay: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "DigitalDisplay",  # 设置具体类型
    "SliderIs": False,  # 数字框是否有滑块
    "Value": 0,  # 显示文本对应的选项值
    "Suffix": "",
    "Min": 0,  # 数字显示框或滑块控件的最小值
    "Max": 0,  # 数字显示框或滑块控件的最大值
    "Step": 0,  # 数字显示框或滑块控件的步长
}


# 文本框控件
TextBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "TextBox",  # 设置具体类型
    "Type": None,  # 文本框类型
    # - obs.OBS_TEXT_DEFAULT        表示单行文本框，
    # - obs.OBS_TEXT_PASSWORD       表示单行密码文本框，
    # - obs.OBS_TEXT_MULTILINE      表示多行文本框，
    # - obs.OBS_TEXT_INFO           表示不可编辑的只读文本框，效果类似于标签。
    "Text": "",  # 显示文本
    "InfoType": None,  # 信息类型
    # - obs.OBS_TEXT_INFO_NORMAL    表示正常信息，
    # - obs.OBS_TEXT_INFO_WARNING   表示警告信息，
    # - obs.OBS_TEXT_INFO_ERROR     表示错误信息
}


# ️按钮控件
Button: Dict[str, Optional[Union[int, str, bool, Any, Callable]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "Button",  # 设置具体类型
    "Type": None,  # 按钮类型
    # - obs.OBS_BUTTON_DEFAULT      表示标准普通按钮
    # - obs.OBS_BUTTON_URL          表示可打开指定 URL 的链接按钮
    "Callback": None,  # 回调函数
    "Url": "",  # 需要打开的 URL
}


# 组合框控件
ComboBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "ComboBox",  # 设置具体类型
    "Type": None,  # 组合框类型
    # - obs.OBS_COMBO_TYPE_EDITABLE 表示可编辑组合框
    # - obs.OBS_COMBO_TYPE_LIST     表示不可编辑组合框
    "Text": "",  # 显示文本
    "Value": "",  # 显示文本对应的选项值
    "Dictionary": {},  # 数据字典
}


# ️ 路径对话框控件
PathBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "PathBox",  # 设置具体类型
    "Type": None,  # 路径对话框类型
    # OBS_PATH_FILE         表示读取文件的对话框
    # OBS_PATH_FILE_SAVE    表示写入文件的对话框
    # OBS_PATH_DIRECTORY    表示选择文件夹的对话框
    "Text": "",  # 显示文本
    "Filter": "",  # 文件种类（筛选条件）
    "StartPath": "", # 对话框起始路径
}


# 分组框控件（独立控件）
Group: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "Group",  # 设置具体类型
    "Type": None,  # 分组框类型
    # OBS_GROUP_NORMAL      表示标准普通分组框
    # OBS_GROUP_CHECKABLE   表示拥有复选框的分组框
    "GroupProps": None,  # 统辖属性集
}


# 复选框控件实例
class CheckBoxP:
    """复选框控件实例"""

    def __init__(self, **kwargs):
        for key, value in CheckBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<CheckBoxP Name='{self.Name}' Number={self.Number} Bool={self.Bool}>"


class CheckBoxPs:
    """复选框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, CheckBoxP] = {}
        self._loading_order: List[CheckBoxP] = []

    def add(self, name: str, **kwargs) -> CheckBoxP:
        """添加复选框控件"""
        if name in self._controls:
            raise ValueError(f"复选框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = CheckBoxP(**kwargs)
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


# 数字框控件实例
class DigitalDisplayP:
    """数字框控件实例"""

    def __init__(self, **kwargs):
        for key, value in DigitalDisplay.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<DigitalDisplayP Name='{self.Name}' Number={self.Number} Min={self.Min} Max={self.Max}>"


class DigitalDisplayPs:
    """数字框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, DigitalDisplayP] = {}
        self._loading_order: List[DigitalDisplayP] = []

    def add(self, name: str, **kwargs) -> DigitalDisplayP:
        """添加数字框控件"""
        if name in self._controls:
            raise ValueError(f"数字框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = DigitalDisplayP(**kwargs)
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


# 文本框控件实例
class TextBoxP:
    """文本框控件实例"""

    def __init__(self, **kwargs):
        for key, value in TextBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<TextBoxP Name='{self.Name}' Number={self.Number} Text='{self.Text}'>"


class TextBoxPs:
    """文本框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, TextBoxP] = {}
        self._loading_order: List[TextBoxP] = []

    def add(self, name: str, **kwargs) -> TextBoxP:
        """添加文本框控件"""
        if name in self._controls:
            raise ValueError(f"文本框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = TextBoxP(**kwargs)
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


# 按钮控件实例
class ButtonP:
    """按钮控件实例"""

    def __init__(self, **kwargs):
        for key, value in Button.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<ButtonP Name='{self.Name}' Number={self.Number} Callback={self.Callback is not None}>"


class ButtonPs:
    """按钮控件管理器"""

    def __init__(self):
        self._controls: Dict[str, ButtonP] = {}
        self._loading_order: List[ButtonP] = []

    def add(self, name: str, **kwargs) -> ButtonP:
        """添加按钮控件"""
        if name in self._controls:
            raise ValueError(f"按钮 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = ButtonP(**kwargs)
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


# 组合框控件实例
class ComboBoxP:
    """组合框控件实例"""

    def __init__(self, **kwargs):
        for key, value in ComboBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<ComboBoxP Name='{self.Name}' Number={self.Number} Text='{self.Text}'>"


class ComboBoxPs:
    """组合框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, ComboBoxP] = {}
        self._loading_order: List[ComboBoxP] = []

    def add(self, name: str, **kwargs) -> ComboBoxP:
        """添加组合框控件"""
        if name in self._controls:
            raise ValueError(f"组合框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = ComboBoxP(**kwargs)
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


# 路径对话框控件实例
class PathBoxP:
    """路径对话框控件实例"""

    def __init__(self, **kwargs):
        for key, value in PathBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        type_name = "未知类型"
        if self.Type == obs.OBS_PATH_FILE:
            type_name = "文件对话框"
        elif self.Type == obs.OBS_PATH_FILE_SAVE:
            type_name = "保存文件对话框"
        elif self.Type == obs.OBS_PATH_DIRECTORY:
            type_name = "文件夹对话框"

        return (f"<PathBoxP Name='{self.Name}' Number={self.Number} "
                f"Type='{type_name}' Text='{self.Text}'>")


class PathBoxPs:
    """路径对话框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, PathBoxP] = {}
        self._loading_order: List[PathBoxP] = []

    def add(self, name: str, **kwargs) -> PathBoxP:
        """添加路径对话框控件"""
        if name in self._controls:
            raise ValueError(f"路径对话框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = PathBoxP(**kwargs)
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


# 分组框控件实例
class GroupP:
    """分组框控件实例（独立控件）"""

    def __init__(self, **kwargs):
        for key, value in Group.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<GroupP Name='{self.Name}' Number={self.Number}>"


class GroupPs:
    """分组框控件管理器"""

    def __init__(self):
        self._groups: Dict[str, GroupP] = {}
        self._loading_order: List[GroupP] = []

    def add(self, name: str, **kwargs) -> GroupP:
        """添加分组框控件"""
        if name in self._groups:
            raise ValueError(f"分组框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        group = GroupP(**kwargs)
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


# 表单管理器
class Widget:
    """表单管理器，管理所有控件"""

    def __init__(self):
        """初始化表单管理器"""
        self.CheckBox = CheckBoxPs()
        self.DigitalDisplay = DigitalDisplayPs()
        self.TextBox = TextBoxPs()
        self.Button = ButtonPs()
        self.ComboBox = ComboBoxPs()
        self.PathBox = PathBoxPs()
        self.Group = GroupPs()
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
        self.CheckBox = CheckBoxPs()
        self.DigitalDisplay = DigitalDisplayPs()
        self.TextBox = TextBoxPs()
        self.Button = ButtonPs()
        self.ComboBox = ComboBoxPs()
        self.PathBox = PathBoxPs()
        self.Group = GroupPs()

        # 清空内部存储
        self._all_controls = []
        self._loading_dict = {}

        return self  # 支持链式调用

    def __repr__(self) -> str:
        """返回表单的可读表示形式"""
        self._update_all_controls()
        return f"<Widget controls={len(self._all_controls)}>"


if __name__ == "__main__":
    # 创建控件表单
    widget = Widget()

    widget_Button_name_list = {
        "props": {
            "top", "bottom",
        },
        "account_props": {
            "login", "accountListUpdate", "qrAddAccount", "qrPictureDisplay", "accountDelete", "accountBackup",
            "accountRestore", "logout",
        },
        "room_props": {
            "roomOpened", "roomCoverView", "roomCoverUpdate", "roomCommonTitlesTrue", "roomTitleChange","roomNewsChange",
            "roomCommonAreasTrue", "roomParentAreaTrue", "roomSubAreaTrue", "bliveWebJump",
        },
        "live_props": {
            "liveFaceAuth", "liveStart", "liveRtmpAddressCopy", "liveRtmpCodeCopy", "liveRtmpCodeUpdate", "liveStop",
            "liveBookingsDayTrue", "liveBookingsHourTrue", "liveBookingsMinuteTrue", "liveBookingsCreate",
            "liveBookingsCancel",},
    }

    widget_Group_name_list = {
        "props": {
            "account": "account_props",
            "room": "room_props",
            "live": "live_props",
        },
    }

    widget_TextBox_name_list = {
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

    widget_ComboBox_name_list = {
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

    widget_PathBox_name_list = {
        "room_props": {
            "roomCover",
        },
    }

    widget_DigitalDisplay_name_list = {
        "live_props": {
            "liveBookingsDay", "liveBookingsHour", "liveBookingsMinute",
        },
    }

    widget_CheckBox_name_list = {
        "live_props": {
            "liveBookingsDynamic",
        },
    }

    for P in widget_Button_name_list:
        for Button_name in widget_Button_name_list[P]:
            widget.Button.add(Button_name)
            obj = getattr(widget.Button, Button_name)
            obj.Props = P

    for P in widget_Group_name_list:
        for Group_name in widget_Group_name_list[P]:
            widget.Group.add(Group_name)
            obj = getattr(widget.Group, Group_name)
            obj.Props = P
            obj.GroupProps = widget_Group_name_list[P][Group_name]

    for P in widget_TextBox_name_list:
        for TextBox_name in widget_TextBox_name_list[P]:
            widget.TextBox.add(TextBox_name)
            obj = getattr(widget.TextBox, TextBox_name)
            obj.Props = P

    for P in widget_ComboBox_name_list:
        for ComboBox_name in widget_ComboBox_name_list[P]:
            widget.ComboBox.add(ComboBox_name)
            obj = getattr(widget.ComboBox, ComboBox_name)
            obj.Props = P

    for P in widget_PathBox_name_list:
        for PathBox_name in widget_PathBox_name_list[P]:
            widget.PathBox.add(PathBox_name)
            obj = getattr(widget.PathBox, PathBox_name)
            obj.Props = P

    for P in widget_DigitalDisplay_name_list:
        for DigitalDisplay_name in widget_DigitalDisplay_name_list[P]:
            widget.DigitalDisplay.add(DigitalDisplay_name)
            obj = getattr(widget.DigitalDisplay, DigitalDisplay_name)
            obj.Props = P

    for P in widget_CheckBox_name_list:
        for CheckBox_name in widget_CheckBox_name_list[P]:
            widget.CheckBox.add(CheckBox_name)
            obj = getattr(widget.CheckBox, CheckBox_name)
            obj.Props = P