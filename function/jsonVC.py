from pprint import pprint
from typing import Union, Optional, Callable, Any, Dict, List, Iterator
import obspython as obs

# 控件默认属性（首字母大写）
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


# ️文件对话框控件
FileDialogBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "FileDialogBox",  # 设置具体类型
    "Text": "",  # 显示文本
    "Filter": "",  # 文件种类（筛选条件）
}


# ️文件夹对话框控件
DirDialogBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "DirDialogBox",  # 设置具体类型
    "Text": "",  # 显示文本
}


# ️ 路径对话框控件
PathBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "PathBox",  # 设置具体类型
    "Type": None,  # 路径对话框类型
    # obs.OBS_PATH_FILE         表示读取文件的对话框
    # obs.OBS_PATH_FILE_SAVE    表示写入文件的对话框
    # obs.OBS_PATH_DIRECTORY    表示选择文件夹的对话框
    "Text": "",  # 显示文本
    "Filter": "",  # 文件种类（筛选条件）
    "StartPath": "", # 对话框起始路径
}

# 分组框控件（独立控件）
Group: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "Group",  # 设置具体类型
    "Type": None,  # 分组框类型
    # obs.OBS_GROUP_NORMAL      表示标准普通分组框
    # obs.OBS_GROUP_CHECKABLE   表示拥有复选框的分组框
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


# 文件对话框控件实例
class FileDialogBoxP:
    """文件对话框控件实例"""

    def __init__(self, **kwargs):
        for key, value in FileDialogBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<FileDialogBoxP Name='{self.Name}' Number={self.Number} Filter='{self.Filter}'>"


class FileDialogBoxPs:
    """文件对话框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, FileDialogBoxP] = {}
        self._loading_order: List[FileDialogBoxP] = []

    def add(self, name: str, **kwargs) -> FileDialogBoxP:
        """添加文件对话框控件"""
        if name in self._controls:
            raise ValueError(f"文件对话框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = FileDialogBoxP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[FileDialogBoxP]:
        """获取文件对话框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除文件对话框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[FileDialogBoxP]:
        """迭代所有文件对话框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """文件对话框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查文件对话框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[FileDialogBoxP]:
        """获取按载入次序排序的文件对话框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 文件夹对话框控件实例
class DirDialogBoxP:
    """文件夹对话框控件实例"""

    def __init__(self, **kwargs):
        for key, value in DirDialogBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<DirDialogBoxP Name='{self.Name}' Number={self.Number} Text='{self.Text}'>"


class DirDialogBoxPs:
    """文件夹对话框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, DirDialogBoxP] = {}
        self._loading_order: List[DirDialogBoxP] = []

    def add(self, name: str, **kwargs) -> DirDialogBoxP:
        """添加文件夹对话框控件"""
        if name in self._controls:
            raise ValueError(f"文件夹对话框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = DirDialogBoxP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[DirDialogBoxP]:
        """获取文件夹对话框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除文件夹对话框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[DirDialogBoxP]:
        """迭代所有文件夹对话框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """文件夹对话框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查文件夹对话框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[DirDialogBoxP]:
        """获取按载入次序排序的文件夹对话框控件列表"""
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
        self.FileDialogBox = FileDialogBoxPs()
        self.DirDialogBox = DirDialogBoxPs()
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
        self._all_controls.extend(self.FileDialogBox)
        self._all_controls.extend(self.DirDialogBox)
        self._all_controls.extend(self.PathBox)
        self._all_controls.extend(self.Group)  # 分组框控件

    def loading(self):
        """按载入次序排序所有控件"""
        self._update_all_controls()
        # 按Number属性排序
        sorted_controls = sorted(self._all_controls, key=lambda c: c.Number)
        # ...收集所有控件...
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
                        self.Button, self.ComboBox, self.FileDialogBox,
                        self.DirDialogBox, self.Group]:
            if name in manager:
                return manager.get(name)
        return None

    def get_sorted_controls(self) -> List[Any]:
        """获取按载入次序排序的所有控件列表"""
        self.loading()
        return list(self._loading_dict.values())

    def __repr__(self) -> str:
        """返回表单的可读表示形式"""
        self._update_all_controls()
        return f"<Widget controls={len(self._all_controls)}>"


# 拓展示例使用代码
if __name__ == "__main__":
    class GlobalVariableOfData:
        widget_loading_number = 0

    # 1. 创建表单实例
    widget = Widget()

    print("=== 高级表单管理示例 ===")

    # 2. 创建配置区域

    # 添加文件选择对话框
    widget.PathBox.add("BackgroundImage",
                       Type=obs.OBS_PATH_FILE,
                       Text="选择背景图片",
                       Filter="图片文件(*.jpg *.png *.bmp);所有文件(*.*)",
                       StartPath="C:/Images",
                       Number=60,
                       Description="背景图片")

    # 添加文件夹选择对话框
    widget.PathBox.add("OutputDirectory",
                       Type=obs.OBS_PATH_DIRECTORY,
                       Text="选择输出目录",
                       StartPath="C:/Output",
                       Number=70,
                       Description="输出目录")

    # 添加保存文件对话框
    widget.PathBox.add("LogFile",
                       Type=obs.OBS_PATH_FILE_SAVE,
                       Text="保存日志文件",
                       Filter="日志文件(*.log);文本文件(*.txt);所有文件(*.*)",
                       StartPath="C:/Logs",
                       Number=80,
                       Description="日志文件")


    # 创建分组框
    appearance_group = widget.Group.add("AppearanceSettings",
                                        Number=(lambda v: (setattr(GlobalVariableOfData, 'widget_loading_number', v + 1), v)[1])(GlobalVariableOfData.widget_loading_number),
                                        Description="外观设置")

    behavior_group = widget.Group.add("BehaviorSettings",
                                      Number=20,
                                      Description="行为设置")

    # 3. 添加各种控件到表单
    # 添加复选框控件
    widget.CheckBox.add("AutoStart",
                        Bool=True,
                        Number=(lambda v: (setattr(GlobalVariableOfData, 'widget_loading_number', v + 1), v)[1])(GlobalVariableOfData.widget_loading_number),
                        Description="启动时自动运行")

    widget.CheckBox.add("ShowNotifications",
                        Bool=True,
                        Number=12,
                        Description="显示通知")

    # 添加数字控件
    widget.DigitalDisplay.add("VolumeLevel",
                              Name="Volume_Level",
                              Min=0,
                              Max=100,
                              Step=5,
                              Value=75,
                              Number=21,
                              Description="音量级别")

    widget.DigitalDisplay.add("AnimationSpeed",
                              SliderIs=True,
                              Min=1,
                              Max=10,
                              Step=1,
                              Value=5,
                              Number=22,
                              Description="动画速度")

    # 添加文本框控件
    widget.TextBox.add("UserName",
                       Text="访客",
                       Number=30,
                       Description="用户名")

    widget.TextBox.add("StatusMessage",
                       Text="系统就绪",
                       Number=31,
                       Description="状态信息")


    # 添加按钮控件
    def save_settings():
        # 模拟保存设置到文件或数据库
        print("保存所有设置...")
        # 更新状态信息
        widget.TextBox.StatusMessage.Text = "设置已保存"


    widget.Button.add("SaveButton",
                      Callback=save_settings,
                      Number=40,
                      Description="保存设置")


    def reset_to_default():
        print("恢复默认设置...")
        # 重置所有控件到默认值
        widget.CheckBox.AutoStart.Bool = True
        widget.CheckBox.ShowNotifications.Bool = True
        widget.DigitalDisplay.VolumeLevel.Value = 75
        widget.DigitalDisplay.AnimationSpeed.Value = 5
        widget.TextBox.UserName.Text = "访客"
        widget.TextBox.StatusMessage.Text = "已恢复默认设置"


    widget.Button.add("ResetButton",
                      Callback=reset_to_default,
                      Number=41,
                      Description="恢复默认")

    # 添加组合框控件
    themes = {
        "light": "明亮主题",
        "dark": "暗黑主题",
        "blue": "蓝色主题",
        "green": "绿色主题"
    }

    widget.ComboBox.add("ThemeSelection",
                        Dictionary=themes,
                        Value="dark",
                        Number=50,
                        Description="界面主题")

    # 添加文件对话框控件
    widget.FileDialogBox.add("BackgroundImage",
                             Filter="图片文件(*.jpg *.png *.bmp);所有文件(*.*)",
                             Text="选择背景图片",
                             Number=60,
                             Description="背景图片")

    # 添加文件夹对话框控件
    widget.DirDialogBox.add("OutputDirectory",
                            Text="选择输出目录",
                            Number=70,
                            Description="输出目录")

    # 4. 表单验证和初始化
    print("\n=== 表单验证和初始化 ===")

    # 检查载入次序冲突
    try:
        widget.loading()
        print("表单验证通过，无载入次序冲突")
    except ValueError as e:
        print(f"表单验证错误: {e}")
        # 在实际应用中，这里可以处理错误，如重新分配Number值

    # 5. 动态访问和修改控件
    print("\n=== 动态访问和修改控件 ===")

    # 通过名称访问控件
    volume_control = widget.get_control_by_name("VolumeLevel")
    # volume_control = widget.DigitalDisplay.VolumeLevel
    # print(f"{volume_control.name}")
    print(f"{volume_control.Name}")
    print(f"{type(volume_control).__name__}")
    print(f"当前音量: {volume_control.Value}")
    if volume_control.ControlType == "CheckBox":
        print("复选框控件")
    elif volume_control.ControlType == "DigitalDisplay":
        print("数字框控件")
    elif volume_control.ControlType == "TextBox":
        print("文本框控件")
    elif volume_control.ControlType == "Button":
        print("按钮控件")
    elif volume_control.ControlType == "ComboBox":
        print("组合框控件")
    elif volume_control.ControlType == "FileDialogBox":
        print("文件对话框控件")
    elif volume_control.ControlType == "DirDialogBox":
        print("文件夹对话框控件")
    elif volume_control.ControlType == "Group":
        print("分组框控件")

    # 修改音量
    volume_control.Value = 85
    print(f"修改后音量: {volume_control.Value}")

    # 通过载入次序访问控件
    theme_control = widget.get_control_by_number(50)
    if theme_control and hasattr(theme_control, "Value"):
        print(f"当前主题: {theme_control.Value}")
        # 修改主题
        theme_control.Value = "blue"
        print(f"修改后主题: {theme_control.Value}")

    # 6. 批量操作控件
    print("\n=== 批量操作控件 ===")

    # 禁用所有复选框
    for checkbox in widget.CheckBox:
        checkbox.Enabled = False
        print(f"禁用复选框: {checkbox.Name}")

    # 稍后启用它们
    for checkbox in widget.CheckBox:
        checkbox.Enabled = True

    # 7. 表单状态保存和加载
    print("\n=== 表单状态保存和加载 ===")


    def save_form_state():
        """保存表单状态到字典"""
        state = {}
        for control in widget.get_sorted_controls():
            # 根据控件类型保存状态
            if isinstance(control, CheckBoxP):
                state[control.Name] = {"Bool": control.Bool}
            elif isinstance(control, (DigitalDisplayP, TextBoxP)):
                state[control.Name] = {"Value": control.Value if hasattr(control, "Value") else control.Text}
            elif isinstance(control, ComboBoxP):
                state[control.Name] = {"Value": control.Value}
            # 其他控件类型...
        return state


    def load_form_state(state: dict):
        """从字典加载表单状态"""
        for name, data in state.items():
            control = widget.get_control_by_name(name)
            if control:
                if isinstance(control, CheckBoxP) and "Bool" in data:
                    control.Bool = data["Bool"]
                elif isinstance(control, DigitalDisplayP) and "Value" in data:
                    control.Value = data["Value"]
                elif isinstance(control, TextBoxP) and "Value" in data:
                    control.Text = data["Value"]
                elif isinstance(control, ComboBoxP) and "Value" in data:
                    control.Value = data["Value"]


    # 保存当前状态
    current_state = save_form_state()
    print("已保存表单状态:", current_state)

    # 修改一些值
    widget.CheckBox.AutoStart.Bool = False
    widget.DigitalDisplay.VolumeLevel.Value = 50
    widget.TextBox.UserName.Text = "管理员"

    # 加载之前保存的状态
    load_form_state(current_state)
    print("已恢复表单状态")

    # 验证恢复结果
    print(f"自动启动状态: {widget.CheckBox.AutoStart.Bool}")
    print(f"音量级别: {widget.DigitalDisplay.VolumeLevel.Value}")
    print(f"用户名: {widget.TextBox.UserName.Text}")

    # 8. 事件处理系统
    print("\n=== 事件处理系统 ===")


    # 创建自定义事件处理
    def on_theme_changed(new_theme):
        print(f"主题已更改为: {new_theme}")
        # 在实际应用中，这里可以更新UI或应用主题设置


    # 监控主题变化
    theme_control = widget.ComboBox.ThemeSelection
    previous_theme = theme_control.Value


    def check_theme_changed():
        global previous_theme
        if theme_control.Value != previous_theme:
            on_theme_changed(theme_control.Value)
            previous_theme = theme_control.Value


    # 模拟主题变化
    print("模拟主题变化:")
    theme_control.Value = "green"
    check_theme_changed()

    # 9. 表单统计和元数据
    print("\n=== 表单统计和元数据 ===")

    # 获取所有控件数量
    widget._update_all_controls()
    print(f"表单总计控件数: {len(widget._all_controls)}")

    # 按类型统计
    type_count = {}
    for control in widget._all_controls:
        type_name = type(control).__name__
        type_count[type_name] = type_count.get(type_name, 0) + 1

    print("控件类型统计:")
    for type_name, count in type_count.items():
        print(f"  {type_name}: {count}")

    # 10. 高级搜索功能
    print("\n=== 高级搜索功能 ===")

    # 搜索包含"set"的控件
    print("包含'set'的控件:")
    for control in widget._all_controls:
        if "set" in control.Name.lower():
            print(f"  - {control.Name} ({type(control).__name__})")

    # 11. 动态添加控件
    print("\n=== 动态添加控件 ===")

    # 在运行时添加新控件
    widget.CheckBox.add("NewFeatureToggle",
                        Bool=False,
                        Number=100,
                        Description="新功能开关")

    widget.Button.add("ActivateFeature",
                      Callback=lambda: print("新功能激活!"),
                      Number=101,
                      Description="激活新功能")

    print("已添加新控件:")
    print(f"  - {widget.CheckBox.NewFeatureToggle.Name}")
    print(f"  - {widget.Button.ActivateFeature.Name}")

    # 12. 表单导出和导入
    print("\n=== 表单导出和导入 ===")


    def export_form_config():
        """导出表单配置为字典"""
        config = {}
        for manager in [widget.CheckBox, widget.DigitalDisplay, widget.TextBox,
                        widget.Button, widget.ComboBox, widget.FileDialogBox,
                        widget.DirDialogBox, widget.Group]:
            for control in manager:
                # 获取控件类型
                control_type = type(control).__name__.replace('P', '')

                # 创建配置项
                config[control.Name] = {
                    "Type": control_type,
                    "Properties": {k: v for k, v in control.__dict__.items()
                                   if not k.startswith('_') and k != 'Callback'}
                }

                # 特殊处理回调函数
                if isinstance(control, ButtonP) and control.Callback:
                    config[control.Name]["Callback"] = "defined"
        return config


    # 导出配置
    form_config = export_form_config()
    print("表单配置已导出，包含", len(form_config), "个控件")

    # 在实际应用中，这里可以将配置保存为JSON文件

    # 13. UI生成示例
    print("\n=== UI生成示例 ===")


    def generate_ui_layout():
        """生成UI布局（模拟）"""
        print("生成UI布局:")

        # 按载入次序排序控件
        sorted_controls = widget.get_sorted_controls()

        # 生成UI元素
        for control in sorted_controls:
            print(control.Number)
            indent = "  " * (int(control.Number / 10))  # 根据载入次序缩进

            if isinstance(control, GroupP):
                print(f"{indent}[Group] {control.Name}: {control.Description}")
            elif isinstance(control, CheckBoxP):
                print(f"{indent}[CheckBox] {control.Name}: {control.Bool} - {control.Description}")
            elif isinstance(control, DigitalDisplayP):
                if control.SliderIs:
                    type_name = "Slider"
                else:
                    type_name = "DigitalDisplay"
                print(
                    f"{indent}[{type_name}] {control.Name}: {control.Value} ({control.Min}-{control.Max}) - {control.Description}")
            elif isinstance(control, TextBoxP):
                print(f"{indent}[TextBox] {control.Name}: '{control.Text}' - {control.Description}")
            elif isinstance(control, ButtonP):
                print(f"{indent}[Button] {control.Name} - {control.Description}")
            elif isinstance(control, ComboBoxP):
                print(f"{indent}[ComboBox] {control.Name}: {control.Value} - {control.Description}")
            elif isinstance(control, FileDialogBoxP):
                print(f"{indent}[FileDialog] {control.Name}: {control.Filter} - {control.Description}")
            elif isinstance(control, DirDialogBoxP):
                print(f"{indent}[DirDialog] {control.Name} - {control.Description}")


    # 生成UI布局
    generate_ui_layout()

    # 14. 最终表单信息
    print("\n=== 最终表单信息 ===")
    print(widget)
    for control in widget.Group:
        print(control.Name)
    print("控件总数:", len(widget._all_controls))
