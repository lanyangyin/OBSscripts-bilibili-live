from typing import Any, Dict, Optional, Iterator


# 控件默认属性的基类
class DefaultPropertiesOfTheControl:
    def __init__(self,
                 number: int = 0,
                 obj: Any = None,
                 name: str = "",
                 description: str = "",
                 visible: bool = False,
                 enabled: bool = False,
                 props: Any = None,
                 modified_is: bool = False
                 ):
        """
        控件默认属性的基类
        Args:
            number: 载入次序
            obj: 控件脚本对象
            name: 唯一名称
            description: 说明文本
            visible: 可见状态
            enabled: 可用状态
            props: 隶属属性集
            modified_is: 是否监听
        """
        self.number = number
        self.obj = obj
        self.name = name
        self.description = description
        self.visible = visible
        self.enabled = enabled
        self.props = props
        self.modifiedIs = modified_is

# ️复选框控件
class GvCheckBox(DefaultPropertiesOfTheControl):
    def __init__(self, check_bool: bool = False, **kwargs):
        """
        ️复选框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            check_bool: 选中状态
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.bool = check_bool

# ️数字显示框控件
class GvDigitalDisplayBox(DefaultPropertiesOfTheControl):
    def __init__(self, digital_min: int = 0, digital_max: int = 0, digital_step: int = 0, **kwargs):
        """
        数字显示框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            digital_min: 数字显示框或滑块控件的最小值。
            digital_max: 数字显示框或滑块控件的最大值。。
            digital_step: 数字显示框或滑块控件的步长。。
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.min = digital_min
        self.max = digital_max
        self.step = digital_step

# ️数字滑块控件
class GvDigitalSlider(DefaultPropertiesOfTheControl):
    def __init__(self, digital_min: int = 0, digital_max: int = 0, digital_step: int = 0, **kwargs):
        """
        数字滑块控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            digital_min: 数字显示框或滑块控件的最小值
            digital_max: 数字显示框或滑块控件的最大值
            digital_step: 数字显示框或滑块控件的步长
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.min = digital_min
        self.max = digital_max
        self.step = digital_step

# 文本框控件
class GvTextBox(DefaultPropertiesOfTheControl):
    def __init__(self, text: str = "", text_box_type: Any = None, text_box_info_type: Any = None, **kwargs):
        """
        文本框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            text: 显示文本 (新增特有属性)
            text_box_type: 文本框类型

                - obs.OBS_TEXT_DEFAULT表示单行文本框，
                - obs.OBS_TEXT_PASSWORD表示单行密码文本框，
                - obs.OBS_TEXT_MULTILINE表示多行文本框，
                - obs.OBS_TEXT_INFO表示不可编辑的只读文本框，效果类似于标签。
            text_box_info_type: 信息类型

                - obs.OBS_TEXT_INFO_NORMAL表示正常信息，
                - obs.OBS_TEXT_INFO_WARNING表示警告信息，
                - obs.OBS_TEXT_INFO_ERROR表示错误信息
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.type = text_box_type
        self.text = text
        self.InfoType = text_box_info_type

# ️按钮控件
class GvButton(DefaultPropertiesOfTheControl):
    def __init__(self, callback, button_type, url: "", **kwargs):
        """
        ️按钮控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            callback: 回调函数
            button_type: 按钮类型

                - obs.OBS_BUTTON_DEFAULT表示标准普通按钮
                - obs.OBS_BUTTON_URL表示可打开指定 URL 的链接按钮
            url: 需要打开的 URL，他必须符合格式要求，拥有https或http前缀。
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.callback = callback
        self.type = button_type
        self.url = url

# 组合框控件
class GvComboBox(DefaultPropertiesOfTheControl):
    def __init__(self, text: str = "", combo_box_type: Any = None, value: str = "", dictionary: dict[str, str] = None, **kwargs):
        """
        组合框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            combo_box_type: 组合框类型

                - obs.OBS_COMBO_TYPE_EDITABLE表示可编辑组合框
                - obs.OBS_COMBO_TYPE_LIST表示不可编辑组合框
            text: 显示文本 (新增特有属性)
            value: 选项值 (新增特有属性)
            dictionary: 数据字典 (新增特有属性)
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.type = combo_box_type
        self.text = text
        self.value = value
        self.dictionary = dictionary or {}

# ️文件对话框控件
class GvFileDialogBox(DefaultPropertiesOfTheControl):
    def __init__(self, file_filter: str = "", text: str = "", **kwargs):
        """
        ️文件对话框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            file_filter: 文件种类（筛选条件）

                可包含多个使用双分号分隔的条目，每个条目可包含一个或更多使用空格分隔的文件扩展名。比如"图片(\*.jpg \*.png);音频(\*.wav)"。
            text: 显示文本 (新增特有属性)
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.filter = file_filter
        self.text = text

# ️文件夹对话框控件
class GvDirDialogBox(DefaultPropertiesOfTheControl):
    def __init__(self, text: str = "", **kwargs):
        """
        ️文件夹对话框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            text: 显示文本 (新增特有属性)
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.text = text

# 分组框控件
class GvGroup(DefaultPropertiesOfTheControl):
    def __init__(self, group_props=None, **kwargs):
        """
        分组框控件 (继承自DefaultPropertiesOfTheControl)
        Args:
            group_props: 统辖属性集 (新增特有属性)
            **kwargs: 接收基类的所有参数
        """
        super().__init__(**kwargs)  # 传递基类参数
        self.groupProps = group_props  # 子类特有属性


class GvCheckBoxs:
    """分组框管理器，用于统一管理多个分组框控件"""

    def __init__(self):
        self.CheckBoxsDict: Dict[str, GvCheckBox] = {}

    def add(self, name: str, **kwargs) -> GvCheckBox:
        """
        添加一个新的分组框控件

        :param name: 分组的唯一名称
        :param kwargs: 传递给GvGroup构造函数的参数
        :return: 新创建的分组对象
        """
        if name in self.CheckBoxsDict:
            raise ValueError(f"分组名称 '{name}' 已存在")

        # 确保name属性设置为group_name
        if 'name' not in kwargs:
            kwargs['name'] = name

        check_box = GvCheckBox(**kwargs)
        self.CheckBoxsDict[name] = check_box
        setattr(self, name, check_box)
        return check_box

    def get(self, name: str) -> Optional[GvCheckBox]:
        """获取指定名称的分组框控件"""
        return self.CheckBoxsDict.get(name)

    def remove(self, name: str) -> bool:
        """移除指定名称的分组框控件"""
        if name in self.CheckBoxsDict:
            del self.CheckBoxsDict[name]
            if hasattr(self, name):
                delattr(self, name)
            return True
        return False

    def __getitem__(self, name: str) -> GvCheckBox:
        """通过名称索引访问分组框控件"""
        if name not in self.CheckBoxsDict:
            raise KeyError(f"分组 '{name}' 不存在")
        return self.CheckBoxsDict[name]

    def __iter__(self) -> Iterator[GvCheckBox]:
        """迭代所有分组框控件"""
        return iter(self.CheckBoxsDict.values())

    def __len__(self) -> int:
        """获取分组框数量"""
        return len(self.CheckBoxsDict)

    def __contains__(self, name: str) -> bool:
        """检查分组框是否存在"""
        return name in self.CheckBoxsDict

    def __repr__(self) -> str:
        """返回管理器的可读表示形式"""
        check_boxs_list = list(self.CheckBoxsDict.keys())
        return f"<GvGroups(groups={check_boxs_list})>"


class GvGroups:
    """分组框管理器，用于统一管理多个分组框控件"""

    def __init__(self):
        self.GroupsDict: Dict[str, GvGroup] = {}

    def add(self, name: str, **kwargs) -> GvGroup:
        """
        添加一个新的分组框控件

        :param name: 分组的唯一名称
        :param kwargs: 传递给GvGroup构造函数的参数
        :return: 新创建的分组对象
        """
        if name in self.GroupsDict:
            raise ValueError(f"分组名称 '{name}' 已存在")

        # 确保name属性设置为group_name
        if 'name' not in kwargs:
            kwargs['name'] = name

        group = GvGroup(**kwargs)
        self.GroupsDict[name] = group
        setattr(self, name, group)
        return group

    def get(self, name: str) -> Optional[GvGroup]:
        """获取指定名称的分组框控件"""
        return self.GroupsDict.get(name)

    def remove(self, name: str) -> bool:
        """移除指定名称的分组框控件"""
        if name in self.GroupsDict:
            del self.GroupsDict[name]
            if hasattr(self, name):
                delattr(self, name)
            return True
        return False

    def __getitem__(self, name: str) -> GvGroup:
        """通过名称索引访问分组框控件"""
        if name not in self.GroupsDict:
            raise KeyError(f"分组 '{name}' 不存在")
        return self.GroupsDict[name]

    def __iter__(self) -> Iterator[GvGroup]:
        """迭代所有分组框控件"""
        return iter(self.GroupsDict.values())

    def __len__(self) -> int:
        """获取分组框数量"""
        return len(self.GroupsDict)

    def __contains__(self, name: str) -> bool:
        """检查分组框是否存在"""
        return name in self.GroupsDict

    def __repr__(self) -> str:
        """返回管理器的可读表示形式"""
        groups_list = list(self.GroupsDict.keys())
        return f"<GvGroups(groups={groups_list})>"


class Widget:
    def __init__(self):
        """初始化表单管理器"""
        self.groups = GvGroups()
        self.LoadingDict = {}

    def loading(self):
        for p in self.groups.GroupsDict.values():
            if p.number in self.LoadingDict:
                self.LoadingDict[p.number] = p

