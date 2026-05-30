"""控件后台属性默认模版(定量)"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Any, Union, Optional, Callable, Dict, List
import obspython as obs


# 控件分类
# ----------------------------------------------------------------------------------------------------------------
class WidgetCategory(Enum):
    """控件分类枚举，用于替代魔法字符串，确保类型安全。"""
    CHECKBOX = "CheckBox"
    """复选框"""
    DIGITALBOX = "DigitalBox"
    """数字框"""
    TEXTBOX = "TextBox"
    """文本框"""
    BUTTON = "Button"
    """按钮"""
    COMBOBOX = "ComboBox"
    """组合框"""
    PATHBOX = "PathBox"
    """路径选择框"""
    GROUP = "Group"
    """分组框"""
    COLORBOX = "ColorBox"
    """颜色选择框"""
    FONTBOX = "FontBox"
    """字体选择框"""
    LISTBOX = "ListBox"
    """列表框"""


# 控件类型
# ----------------------------------------------------------------------------------------------------------------
class CheckBoxVariant(Enum):
    """复选框 控件类型"""
    pass


class DigitalBoxVariant(Enum):
    """
    数字框 控件类型
    INT 表示整数数字框，
    FLOAT 表示浮点数数字框，
    INT_SLIDER 表示整数数字框带滑块，
    FLOAT_SLIDER 表示浮点数数字框带滑块，
    """
    INT = "Int"
    """整数"""
    FLOAT = "Float"
    """浮点数"""
    INT_SLIDER = "IntSlider"
    """整数带滑块"""
    FLOAT_SLIDER = "FloatSlider"
    """浮点数带滑块"""


class TextBoxVariant(Enum):
    """
    文本框 类型
    DEFAULT 表示单行文本框，
    PASSWORD 表示单行密码文本框，
    MULTILINE 表示多行文本框，
    INFO 表示不可编辑的只读文本框，效果类似于标签。
    """
    DEFAULT = obs.OBS_TEXT_DEFAULT
    """单行"""
    PASSWORD = obs.OBS_TEXT_PASSWORD
    """单行密码"""
    MULTILINE = obs.OBS_TEXT_MULTILINE
    """多行"""
    INFO = obs.OBS_TEXT_INFO
    """不可编辑"""


class TextBoxInfoVariant(Enum):
    """
    文本框信息类型
    NORMAL 表示正常信息，
    WARNING 表示警告信息，
    ERROR 表示错误信息
    """
    NORMAL = obs.OBS_TEXT_INFO_NORMAL
    """正常信息"""
    WARNING = obs.OBS_TEXT_INFO_WARNING
    """警告信息"""
    ERROR = obs.OBS_TEXT_INFO_ERROR
    """错误信息"""


class ButtonVariant(Enum):
    """
    按钮 类型
    DEFAULT 表示标准普通按钮，
    URL 表示可打开指定 URL 的链接按钮。
    """
    DEFAULT = obs.OBS_BUTTON_DEFAULT
    """普通"""
    URL = obs.OBS_BUTTON_URL
    """打开链接"""


class ComboBoxVariant(Enum):
    """
    组合框 类型
    EDITABLE 表示可编辑组合框，仅适用于字符串格式，用户可以输入自己的内容，
    LIST 表示不可编辑组合框
    """
    EDITABLE = obs.OBS_COMBO_TYPE_EDITABLE
    """可编辑"""
    LIST = obs.OBS_COMBO_TYPE_LIST
    """不可编辑"""


class ListBoxVariant(Enum):
    """
    列表框 类型
    STRINGS 表示字符串列表框，
    FILES 表示文件路径列表框，
    FILES_AND_URLS 表示文件路径和网址列表框。
    """
    STRINGS = obs.OBS_EDITABLE_LIST_TYPE_STRINGS
    """字符串"""
    FILES = obs.OBS_EDITABLE_LIST_TYPE_FILES
    """文件路径"""
    FILES_AND_URLS = obs.OBS_EDITABLE_LIST_TYPE_FILES_AND_URLS
    """文件路径和网址"""


class GroupVariant(Enum):
    """
    分组框 类型
    NORMAL 表示标准普通分组框，
    CHECKABLE 表示拥有复选框的分组框。
    """
    NORMAL = obs.OBS_GROUP_NORMAL
    """标准"""
    CHECKABLE = obs.OBS_GROUP_CHECKABLE
    """拥有复选框"""


class ColorBoxVariant(Enum):
    """
    颜色选择框 类型
    COLOR 无透明度。
    ALPHA 带透明度。
    """
    COLOR = "color"
    """无透明度"""
    ALPHA = "alpha"
    """带透明度"""


class FontBoxVariant(Enum):
    """
    字体选择框 类型
    null
    """


class PathBoxVariant(Enum):
    """
    路径对话框 类型
    FILE 表示读取文件的对话框，
    FILE_SAVE 表示写入文件的对话框，
    DIRECTORY 表示选择文件夹的对话框。
    """
    FILE = obs.OBS_PATH_FILE
    """读取文件"""
    FILE_SAVE = obs.OBS_PATH_FILE_SAVE
    """写入文件"""
    DIRECTORY = obs.OBS_PATH_DIRECTORY
    """选择文件夹"""


# 控件属性
# ----------------------------------------------------------------------------------------------------------------
@dataclass
class ControlBaseData:
    """
    所有控件的基类数据模型。
    注意：dataclass 主要用于存储数据，复杂逻辑应放在管理器类中。
    """
    widget_category: WidgetCategory = None
    """📵🥚控件的基本类型"""
    props_name: str = "props"
    """📵🥚控件所属属性集的名称"""
    object_name: str = ""
    """📵🥚控件对象名"""
    control_name: str = ""
    """📵🥚控件的唯一标识名，用于在脚本内部引用。"""
    description: str = ""
    """📵🥚显示给用户的简短描述/标签。"""
    long_description: str = "长描述示例"
    """📵🥚显示给用户的详细帮助信息。"""
    widget_variant: Union[
        CheckBoxVariant,
        ComboBoxVariant,
        PathBoxVariant,
        ButtonVariant,
        GroupVariant,
        ColorBoxVariant,
        FontBoxVariant,
        ListBoxVariant,
        TextBoxVariant,
        DigitalBoxVariant
    ] = None
    """📵🥚控件在 OBS API 中的功能类型 (如 OBS_TEXT_DEFAULT)。"""
    modified_callback_enabled: bool = False
    """📵🥚该控件的值变化时是否触发修改回调函数。"""
    modified_callback: Callable = None
    """📵🥚该控件的值变化时是否触发修改回调函数。"""
    load_order: int = 0
    """📵控件的加载顺序，数值越小越靠前。"""
    props: Any = None
    """📵控件所属属性集对象 (obs_properties_t)。"""
    obj: Any = None
    """📵控件对应的 OBS 底层对象 (obs_property_t)。"""
    visible: bool = True
    """控件的可见状态。"""
    enabled: bool = True
    """控件的可用（是否灰显）状态。"""


@dataclass
class CheckBoxData(ControlBaseData):
    """复选框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.CHECKBOX
    """📵🥚控件的基本类型"""
    checked: bool = False
    """复选框的选中状态。"""


@dataclass
class DigitalBoxData(ControlBaseData):
    """数字框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.DIGITALBOX
    """📵🥚控件的基本类型"""
    widget_variant: DigitalBoxVariant = DigitalBoxVariant.INT
    """📵🥚数字框的变体类型。"""
    suffix: str = ""
    """📵🥚显示在数值后的单位后缀 (如 '%', 'px')。"""
    digital: Union[int, float] = 0
    """当前显示的数值。"""
    min_val: Union[int, float] = 0  # 避免与内置函数 `min` 冲突
    """允许的最小值。"""
    max_val: Union[int, float] = 100  # 避免与内置函数 `max` 冲突
    """允许的最大值。"""
    step: Union[int, float] = 1
    """调整时的步长。"""


@dataclass
class TextBoxData(ControlBaseData):
    """文本框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.TEXTBOX
    """📵🥚控件的基本类型"""
    widget_variant: TextBoxVariant = TextBoxVariant.DEFAULT
    """📵🥚OBS 文本框类型常量。"""
    info_type: TextBoxInfoVariant = TextBoxInfoVariant.NORMAL
    """仅当 widget_variant 为 OBS_TEXT_INFO 时有效的信息类型。"""
    text: str = ""
    """文本框中的文字内容。"""


@dataclass
class ButtonData(ControlBaseData):
    """按钮控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.BUTTON
    """📵🥚控件的基本类型"""
    widget_variant: ButtonVariant = ButtonVariant.DEFAULT
    """📵🥚OBS 按钮类型常量。"""
    click_callback: Optional[Callable[[Any, Any], bool]] = None
    """📵🥚按钮被点击时触发的回调函数。"""
    url: str = ""
    """📵🥚仅当 widget_variant 为 OBS_BUTTON_URL 时有效的跳转链接。"""


@dataclass
class ComboBoxData(ControlBaseData):
    """组合框（下拉列表）控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.COMBOBOX
    """📵🥚控件的基本类型"""
    widget_variant: ComboBoxVariant = ComboBoxVariant.LIST
    """📵🥚OBS 组合框类型常量。"""
    label: str = ""  # 明确区分显示文本和值
    """当前显示在下拉框中的文本。"""
    value: str = ""
    """当前选中项对应的内部值。"""
    items: List[Dict[Literal["label", "value"], str]] = field(default_factory=list)
    """下拉框的选项列表，每个项是 {'label': '...', 'value': '...'}。"""


@dataclass
class ListBoxData(ControlBaseData):
    """列表框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.LISTBOX
    """📵🥚控件的基本类型"""
    widget_variant: ListBoxVariant = ListBoxVariant.STRINGS
    """📵🥚OBS 列表框类型常量。"""
    filter_str: str = "*.*"
    """📵🥚文件类型过滤器（如 '*.png;*.jpg'）。"""
    default_path: str = ""
    """📵🥚对话框的默认起始路径。"""
    items: List[Dict[Literal["value", "selected", "hidden"], Any]] = field(default_factory=list)
    """表框中的项目列表，每个项目是字典格式。"""


@dataclass
class GroupData(ControlBaseData):
    """分组框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.GROUP
    """📵🥚控件的基本类型"""
    widget_variant: GroupVariant = GroupVariant.NORMAL
    """📵🥚OBS 分组框类型常量。"""
    group_props_name: str = "GroupProps"
    """📵🥚该分组所包含控件使用的属性集名称。"""
    group_props: Any = None
    """📵该分组所包含控件使用的属性集对象。"""
    folding_control_obj: Any = None  # 更清晰的命名
    """📵仅当 widget_variant 为 OBS_GROUP_CHECKABLE 时关联的折叠控制对象。"""
    folding_visible: bool = True
    """📵折叠控件独立可见性。"""
    folding_enabled: bool = True
    """📵折叠控件独立可用性。"""
    checked: bool = True  # 对于可勾选分组
    """仅当 widget_variant 为 OBS_GROUP_CHECKABLE 时有效，表示分组是否被勾选。"""


@dataclass
class ColorBoxData(ControlBaseData):
    """颜色选择框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.COLORBOX
    """📵🥚控件的基本类型"""
    widget_variant: ColorBoxVariant = ColorBoxVariant.ALPHA
    """📵🥚颜色对话框的变体类型：COLOR（无透明度）或 ALPHA（带透明度）。"""
    color_alpha: int = 0xFF
    """透明度"""
    color_red: int = 0xFF
    """红色"""
    color_green: int = 0xFF
    """绿色"""
    color_blue: int = 0xFF
    """蓝色"""

    @property
    def color_value(self) -> int:
        """📵当前颜色值（ARGB格式的整数）。"""
        bgr = (self.color_blue * 0x10000) + (self.color_green * 0x100) + self.color_red
        if self.widget_variant == ColorBoxVariant.ALPHA:
            return (self.color_alpha * 0x1000000) + bgr
        elif self.widget_variant == ColorBoxVariant.COLOR:
            return bgr
        else:
            return bgr

    def set_from_color_value(self, color_value: int):
        """根据 color_value 整数设置本控件的各颜色分量。"""
        self.color_blue = (color_value >> 16) & 0xFF
        self.color_green = (color_value >> 8) & 0xFF
        self.color_red = color_value & 0xFF
        if self.widget_variant == ColorBoxVariant.ALPHA:
            self.color_alpha = (color_value >> 24) & 0xFF
        else:
            self.color_alpha = 0xFF  # 无 Alpha 控件时默认不透明


@dataclass
class FontBoxData(ControlBaseData):
    """字体选择框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.FONTBOX
    """📵🥚控件的基本类型"""
    font_data: Any = None
    """📵字体数据对象（obs_data_t），包含字体信息。"""
    font_face: str = "Kai"
    """字体系列名称"""
    font_size: int = 36
    """字体大小"""
    font_style: Literal[
        "Regular", "Bold", "Light", "Black"
    ] = "Regular"
    """字体样式 Regular, Bold, Light, Black"""
    font_bold: bool = False
    """字体标志位 粗体。"""
    font_italic: bool = False
    """字体标志位 斜体。"""
    font_underline: bool = False
    """字体标志位 下划线。"""
    font_strikeout: bool = False
    """字体标志位 删除线。"""

    @property
    def font_flags(self):
        """📵字体标志位"""
        font_bold = 1 if self.font_bold else 0
        font_italic = 1 if self.font_italic else 0
        font_underline = 1 if self.font_underline else 0
        font_strikeout = 1 if self.font_strikeout else 0
        return int(f"0b{font_bold}{font_italic}{font_underline}{font_strikeout}", 2)

    def set_from_font_flags(self, font_flags: int):
        """根据 font_flags 整数设置本控件的各字体标志位。"""
        self.font_bold = bool(font_flags & 1)
        self.font_italic = bool(font_flags & 2)
        self.font_underline = bool(font_flags & 4)
        self.font_strikeout = bool(font_flags & 8)


@dataclass
class PathBoxData(ControlBaseData):
    """路径选择框控件的专用数据模型。"""
    widget_category: WidgetCategory = WidgetCategory.PATHBOX
    """📵🥚控件的基本类型"""
    widget_variant: PathBoxVariant = PathBoxVariant.FILE
    """📵🥚OBS 路径框类型常量。"""
    default_path: str = ""
    """📵🥚对话框打开时的初始路径。"""
    filter_str: str = "*.*"  # 避免与内置函数 `filter` 冲突
    """📵🥚文件对话框的文件类型过滤器 (如 '*.png;*.jpg')。"""
    path_text: str = ""  # 明确这是路径文本
    """当前显示或选中的路径字符串。"""

