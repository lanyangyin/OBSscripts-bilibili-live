from typing import Union, Optional, Callable, Any, Dict, List, Iterator

# 控件默认属性
DefaultPropertiesOfTheControl: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "obj": None,  # 控件脚本对象
    "props": None,  # 隶属属性集
    "number": 0,  # 载入次序
    "name": "",  # 唯一名称
    "description": "",  # 说明文本
    "visible": False,  # 可见状态
    "enabled": False,  # 可用状态
    "modified_is": False,  # 是否监听
}

# ️复选框控件
CheckBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "Bool": False,  # 复选框是否选中
    **DefaultPropertiesOfTheControl,
}


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
        return f"<CheckBoxP name='{self.name}' number={self.number} Bool={self.Bool}>"


class CheckBoxPs:
    """复选框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, CheckBoxP] = {}
        self._loading_order: List[CheckBoxP] = []

    def add(self, name: str, **kwargs) -> CheckBoxP:
        """添加复选框控件"""
        if name in self._controls:
            raise ValueError(f"复选框 '{name}' 已存在")
        control = CheckBoxP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# ️数字框控件
DigitalDisplay: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "SliderIs": False,  # 数字框是否有滑块
    "Min": 0,  # 数字显示框或滑块控件的最小值
    "Max": 0,  # 数字显示框或滑块控件的最大值
    "Step": 0,  # 数字显示框或滑块控件的步长
    **DefaultPropertiesOfTheControl,
}


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
        return f"<DigitalDisplayP name='{self.name}' number={self.number} Min={self.Min} Max={self.Max}>"


class DigitalDisplayPs:
    """数字框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, DigitalDisplayP] = {}
        self._loading_order: List[DigitalDisplayP] = []

    def add(self, name: str, **kwargs) -> DigitalDisplayP:
        """添加数字框控件"""
        if name in self._controls:
            raise ValueError(f"数字框 '{name}' 已存在")
        control = DigitalDisplayP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# 文本框控件
TextBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "Type": None,  # 文本框类型
    "Text": "",  # 显示文本
    "InfoType": None,  # 信息类型
    **DefaultPropertiesOfTheControl,
}


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
        return f"<TextBoxP name='{self.name}' number={self.number} Text='{self.Text}'>"


class TextBoxPs:
    """文本框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, TextBoxP] = {}
        self._loading_order: List[TextBoxP] = []

    def add(self, name: str, **kwargs) -> TextBoxP:
        """添加文本框控件"""
        if name in self._controls:
            raise ValueError(f"文本框 '{name}' 已存在")
        control = TextBoxP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# ️按钮控件
Button: Dict[str, Optional[Union[int, str, bool, Any, Callable]]] = {
    "Type": None,  # 按钮类型
    "Callback": None,  # 回调函数
    "Url": "",  # 需要打开的 URL
    **DefaultPropertiesOfTheControl,
}


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
        return f"<ButtonP name='{self.name}' number={self.number} Callback={self.Callback is not None}>"


class ButtonPs:
    """按钮控件管理器"""

    def __init__(self):
        self._controls: Dict[str, ButtonP] = {}
        self._loading_order: List[ButtonP] = []

    def add(self, name: str, **kwargs) -> ButtonP:
        """添加按钮控件"""
        if name in self._controls:
            raise ValueError(f"按钮 '{name}' 已存在")
        control = ButtonP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# 组合框控件
ComboBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "Type": None,  # 组合框类型
    "Text": "",  # 显示文本
    "Value": "",  # 显示文本对应的选项值
    "dictionary": {},  # 数据字典
    **DefaultPropertiesOfTheControl,
}


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
        return f"<ComboBoxP name='{self.name}' number={self.number} Text='{self.Text}'>"


class ComboBoxPs:
    """组合框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, ComboBoxP] = {}
        self._loading_order: List[ComboBoxP] = []

    def add(self, name: str, **kwargs) -> ComboBoxP:
        """添加组合框控件"""
        if name in self._controls:
            raise ValueError(f"组合框 '{name}' 已存在")
        control = ComboBoxP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# ️文件对话框控件
FileDialogBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "Text": "",  # 显示文本
    "Filter": "",  # 文件种类（筛选条件）
    **DefaultPropertiesOfTheControl,
}


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
        return f"<FileDialogBoxP name='{self.name}' number={self.number} Filter='{self.Filter}'>"


class FileDialogBoxPs:
    """文件对话框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, FileDialogBoxP] = {}
        self._loading_order: List[FileDialogBoxP] = []

    def add(self, name: str, **kwargs) -> FileDialogBoxP:
        """添加文件对话框控件"""
        if name in self._controls:
            raise ValueError(f"文件对话框 '{name}' 已存在")
        control = FileDialogBoxP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# ️文件夹对话框控件
DirDialogBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "Text": "",  # 显示文本
    **DefaultPropertiesOfTheControl,
}


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
        return f"<DirDialogBoxP name='{self.name}' number={self.number} Text='{self.Text}'>"


class DirDialogBoxPs:
    """文件夹对话框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, DirDialogBoxP] = {}
        self._loading_order: List[DirDialogBoxP] = []

    def add(self, name: str, **kwargs) -> DirDialogBoxP:
        """添加文件夹对话框控件"""
        if name in self._controls:
            raise ValueError(f"文件夹对话框 '{name}' 已存在")
        control = DirDialogBoxP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


# 分组框控件（不再管理子控件）
Group: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "GroupProps": None,  # 统辖属性集
    **DefaultPropertiesOfTheControl,
}


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
        return f"<GroupP name='{self.name}' number={self.number}>"


class GroupPs:
    """分组框控件管理器"""

    def __init__(self):
        self._groups: Dict[str, GroupP] = {}
        self._loading_order: List[GroupP] = []

    def add(self, name: str, **kwargs) -> GroupP:
        """添加分组框控件"""
        if name in self._groups:
            raise ValueError(f"分组框 '{name}' 已存在")
        group = GroupP(name=name, **kwargs)
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
        return sorted(self._loading_order, key=lambda c: c.number)


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
        self._all_controls.extend(self.Group)  # 分组框控件

    def loading(self):
        """按载入次序排序所有控件"""
        self._update_all_controls()
        # 按number属性排序
        sorted_controls = sorted(self._all_controls, key=lambda c: c.number)

        # 创建载入次序字典
        self._loading_dict = {}
        for control in sorted_controls:
            if control.number in self._loading_dict:
                existing_control = self._loading_dict[control.number]
                raise ValueError(
                    f"载入次序冲突: 控件 '{control.name}' (类型: {type(control).__name__}) 和 "
                    f"'{existing_control.name}' (类型: {type(existing_control).__name__}) "
                    f"使用相同的number值 {control.number}"
                )
            self._loading_dict[control.number] = control

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


# 示例使用
if __name__ == "__main__":
    # 创建表单
    widget = Widget()

    # 添加复选框
    widget.CheckBox.add("global_checkbox", Bool=True, number=1, description="全局复选框")

    # 添加数字框
    widget.DigitalDisplay.add("global_display", Min=0, Max=100, Step=5, number=2)

    # 添加文本框
    widget.TextBox.add("global_text", Text="示例文本", number=3)


    # 添加按钮
    def button_callback():
        print("按钮被点击!")


    widget.Button.add("global_button", Callback=button_callback, number=4)

    # 添加组合框
    widget.ComboBox.add("global_combo", dictionary={"opt1": "选项1", "opt2": "选项2"}, number=5)

    # 添加分组框（独立控件）
    widget.Group.add("group1", number=6, description="第一组控件")

    # 添加分组内的控件（独立控件）
    widget.CheckBox.add("group_checkbox", Bool=False, number=7)
    widget.DigitalDisplay.add("group_slider", SliderIs=True, Min=0, Max=50, Step=1, number=8)

    # 添加文件对话框
    widget.FileDialogBox.add("file_dialog", Filter="图片(*.jpg *.png)", Text="选择图片", number=9)

    # 添加文件夹对话框
    widget.DirDialogBox.add("dir_dialog", Text="选择目录", number=10)

    # 输出表单信息
    print("表单结构:")
    print(widget)

    print("\n按载入次序排序的控件:")
    for control in widget.get_sorted_controls():
        print(f"{control.number}: {control}")

    # 查找控件示例
    print("\n查找控件:")
    print("通过名称查找 'global_button':", widget.get_control_by_name("global_button"))
    print("通过载入次序查找 3:", widget.get_control_by_number(3))

    # 访问控件属性示例
    print("\n访问控件属性:")
    print("全局复选框状态:", widget.CheckBox.global_checkbox.Bool)
    print("全局数字框最大值:", widget.DigitalDisplay.global_display.Max)
    print("分组复选框状态:", widget.CheckBox.group_checkbox.Bool)

    # 修改控件属性
    widget.CheckBox.global_checkbox.Bool = False
    widget.DigitalDisplay.global_display.Max = 200
    widget.TextBox.global_text.Text = "修改后的文本"

    print("\n修改后的属性:")
    print("全局复选框状态:", widget.CheckBox.global_checkbox.Bool)
    print("全局数字框最大值:", widget.DigitalDisplay.global_display.Max)
    print("全局文本框内容:", widget.TextBox.global_text.Text)



