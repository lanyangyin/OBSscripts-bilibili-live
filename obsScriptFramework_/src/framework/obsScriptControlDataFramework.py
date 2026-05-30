"""控件管理框架"""
from collections import OrderedDict as PyOrderedDict
from typing import Set
try:
    from ..data.obsScriptControlData import *
except ImportError as e:
    try:
        from obsScriptFramework_.src.data.obsScriptControlData import *
    except ImportError as e:
        raise ImportError(e)

# 控件管理
# ----------------------------------------------------------------------------------------------------------------
class ControlManager:
    """
    控件管理器，负责管理所有控件的添加、查询和唯一性验证。

    特性：
    1. 按控件分类组织控件
    2. 确保control_name全局唯一
    3. 确保同一分类下object_name唯一
    4. 自动管理load_order
    5. 提供方便的访问接口
    6. 维护基础group控件和group_props_name约束
    """

    def __init__(self):
        """初始化控件管理器"""
        # 按分类存储控件的数据字典
        self._widgets_by_category: Dict[WidgetCategory, Dict[str, ControlBaseData]] = {
            category: PyOrderedDict() for category in WidgetCategory
        }

        # 全局control_name集合，用于确保唯一性
        self._global_control_names: Set[str] = set()

        # 按分类的object_name集合，用于确保同一分类下唯一性
        self._object_names_by_category: Dict[WidgetCategory, Set[str]] = {
            category: set() for category in WidgetCategory
        }

        # 按props_name分组的控件字典
        self._widgets_by_props: Dict[str, List[str]] = {}

        # 存储所有group控件的group_props_name，用于唯一性检查
        self._group_props_names: Set[str] = set()

        # 加载顺序计数器
        self._load_order_counter = 0

        # 基础group控件（特殊控件，不参与常规管理）
        self._basic_group: Optional[GroupData] = None

        # 为每个分类创建动态属性，允许通过.语法访问分类管理器
        self._setup_category_properties()

        # 创建基础group控件
        self._create_basic_group()

    def _setup_category_properties(self):
        """为每个控件分类设置动态属性"""
        for category in WidgetCategory:
            # 创建分类管理器实例
            category_manager = _CategoryManager(self, category)

            # 设置为实例属性
            # 使用分类枚举值的名称作为属性名（小写）
            prop_name = category.name.lower()
            setattr(self, prop_name, category_manager)

    def _create_basic_group(self):
        """创建基础group控件"""
        # 使用特殊的load_order值，不参与常规排序
        basic_group = GroupData(
            widget_category=WidgetCategory.GROUP,
            control_name="group",
            object_name="base",
            description="分组框",
            widget_variant=GroupVariant.NORMAL,
            group_props_name="props",
            props_name="",
            load_order=-1  # 特殊值，表示不参与常规排序
        )

        # 将基础group控件单独存储，不添加到常规映射中
        self._basic_group = basic_group

        # 将基础group的group_props_name添加到集合中，这样其他控件可以使用"props"
        self._group_props_names.add(basic_group.group_props_name)

        # 注意：不添加到 _widgets_by_category, _widgets_by_props 等常规映射中
        # 这样它就完全独立于常规控件管理系统

    def _validate_uniqueness(self, control_name: str, category: WidgetCategory, object_name: str) -> None:
        """
        验证控件名称的唯一性

        参数:
            control_name: 控件的全局唯一标识名
            category: 控件分类
            object_name: 控件在同一分类下的对象名

        异常:
            ValueError: 如果名称违反唯一性约束
        """
        # 检查是否是基础group控件的名称
        if control_name == "group":
            raise ValueError(f"control_name 'group' 是保留名称，用于基础group控件")

        # 验证control_name全局唯一
        if control_name in self._global_control_names:
            raise ValueError(f"control_name '{control_name}' 已存在，必须是全局唯一的")

        # 验证object_name在同一分类下唯一
        if object_name in self._object_names_by_category[category]:
            raise ValueError(f"object_name '{object_name}' 在分类 {category.value} 中已存在")

    def _validate_group_props_name(self, widget: ControlBaseData) -> None:
        """
        验证group控件的group_props_name约束

        参数:
            widget: group控件数据对象

        异常:
            ValueError: 如果违反group_props_name约束
        """
        if not isinstance(widget, GroupData):
            return

        # 1. 非基础group控件的group_props_name不能等于props_name
        if widget.group_props_name == widget.props_name:
            raise ValueError(
                f"group控件 '{widget.control_name}' 的 "
                f"group_props_name '{widget.group_props_name}' 不能等于 props_name"
            )

        # 2. 所有group控件的group_props_name不能重名（包括基础group的）
        if widget.group_props_name in self._group_props_names:
            raise ValueError(
                f"group_props_name '{widget.group_props_name}' 已存在，"
                f"所有group控件的group_props_name不能重名"
            )

    def _validate_props_name(self, widget: ControlBaseData) -> None:
        """
        验证控件的props_name必须来自某个group控件的group_props_name

        参数:
            widget: 控件数据对象

        异常:
            ValueError: 如果props_name无效
        """
        # 验证props_name必须存在于已注册的group_props_name中
        if widget.props_name not in self._group_props_names:
            raise ValueError(
                f"控件 '{widget.control_name}' 的 props_name '{widget.props_name}' "
                f"必须来自某个group控件的group_props_name"
            )

    def _add_control_to_maps(self, widget: ControlBaseData) -> None:
        """
        将控件添加到各种映射中

        参数:
            widget: 控件数据对象
        """
        category = widget.widget_category

        # 添加到分类字典
        self._widgets_by_category[category][widget.control_name] = widget

        # 添加到全局control_name集合
        self._global_control_names.add(widget.control_name)

        # 添加到分类object_name集合
        self._object_names_by_category[category].add(widget.object_name)

        # 添加到props_name分组字典
        props_name = widget.props_name
        if props_name not in self._widgets_by_props:
            self._widgets_by_props[props_name] = []
        self._widgets_by_props[props_name].append(widget.control_name)

        # 如果是Group，还需要处理group_props_name
        if category == WidgetCategory.GROUP and hasattr(widget, 'group_props_name'):
            group_props_name = widget.group_props_name
            self._group_props_names.add(group_props_name)

            if group_props_name not in self._widgets_by_props:
                self._widgets_by_props[group_props_name] = []

    def _get_widget_class(self, category: WidgetCategory, **kwargs) -> type:
        """
        根据分类获取对应的数据类

        参数:
            category: 控件分类
            **kwargs: 控件属性

        返回:
            对应的数据类
        """
        widget_classes = {
            WidgetCategory.CHECKBOX: CheckBoxData,
            WidgetCategory.DIGITALBOX: DigitalBoxData,
            WidgetCategory.TEXTBOX: TextBoxData,
            WidgetCategory.BUTTON: ButtonData,
            WidgetCategory.COMBOBOX: ComboBoxData,
            WidgetCategory.LISTBOX: ListBoxData,
            WidgetCategory.GROUP: GroupData,
            WidgetCategory.COLORBOX: ColorBoxData,
            WidgetCategory.FONTBOX: FontBoxData,
            WidgetCategory.PATHBOX: PathBoxData,
        }

        return widget_classes.get(category)

    def create_widget(self, category: WidgetCategory, control_name: str, object_name: Optional[str] = None,
                      **kwargs) -> ControlBaseData:
        """
        创建新的控件实例

        参数:
            category: 控件分类
            control_name: 控件的全局唯一标识名
            object_name: 控件对象名，如果为None则使用control_name
            **kwargs: 控件属性

        返回:
            创建的控件数据对象

        异常:
            ValueError: 如果名称违反唯一性约束或其他验证失败
        """
        # 如果未提供object_name，使用control_name
        if object_name is None:
            object_name = control_name

        # 验证唯一性
        self._validate_uniqueness(control_name, category, object_name)

        # 获取对应的数据类
        widget_class = self._get_widget_class(category, **kwargs)
        if widget_class is None:
            raise ValueError(f"不支持的分类: {category}")

        # 设置widget_category
        kwargs['widget_category'] = category

        # 设置control_name和object_name
        kwargs['control_name'] = control_name
        kwargs['object_name'] = object_name

        # 设置load_order
        if 'load_order' not in kwargs:
            kwargs['load_order'] = self._load_order_counter
            self._load_order_counter += 1

        # 创建控件实例
        widget = widget_class(**kwargs)

        # 验证props_name必须来自group_props_name
        self._validate_props_name(widget)

        # 验证group控件的group_props_name约束
        self._validate_group_props_name(widget)

        # 添加到各种映射中
        self._add_control_to_maps(widget)

        return widget

    def get_widgets_by_load_order(self) -> List[ControlBaseData]:
        """
        获取按load_order排序的控件列表（不包含基础group控件）

        返回:
            按load_order升序排列的控件列表
        """
        all_widgets = []
        for category_dict in self._widgets_by_category.values():
            all_widgets.extend(category_dict.values())

        # 按load_order排序
        return sorted(all_widgets, key=lambda w: w.load_order)

    def get_props_mapping(self) -> Dict[str, List[str]]:
        """
        获取props_name到控件control_name的映射字典（不包含基础group控件）

        返回:
            props_name到控件control_name列表的映射字典
        """
        return self._widgets_by_props.copy()

    def get_widget_by_control_name(self, control_name: str) -> Optional[ControlBaseData]:
        """
        通过control_name查找控件

        参数:
            control_name: 控件的全局唯一标识名

        返回:
            控件数据对象，如果不存在则返回None
        """
        # 首先检查是否是基础group控件
        if control_name == "group":
            return self._basic_group

        # 在常规控件中查找
        for category_dict in self._widgets_by_category.values():
            if control_name in category_dict:
                return category_dict[control_name]
        return None

    def get_basic_group(self) -> GroupData:
        """
        获取基础group控件

        返回:
            基础group控件数据对象
        """
        return self._basic_group

    def clear(self):
        """清除所有常规控件，但保留基础group控件"""
        self._widgets_by_category = {category: PyOrderedDict() for category in WidgetCategory}
        self._global_control_names.clear()
        self._object_names_by_category = {category: set() for category in WidgetCategory}
        self._widgets_by_props.clear()
        self._group_props_names.clear()
        self._load_order_counter = 0

        # 重新创建基础group控件
        self._create_basic_group()

    @property
    def total_widgets(self) -> int:
        """获取常规控件总数（不包含基础group控件）"""
        return len(self._global_control_names)

    @property
    def available_group_props_names(self) -> Set[str]:
        """获取所有可用的group_props_name"""
        return self._group_props_names.copy()

    def __str__(self) -> str:
        """字符串表示"""
        result = [f"ControlManager (共 {self.total_widgets} 个常规控件)"]

        # 基础group控件信息
        if self._basic_group:
            result.append(
                f"基础group控件: {self._basic_group.control_name} (group_props_name: {self._basic_group.group_props_name})")
        else:
            result.append(f"基础group控件: 未初始化")

        result.append(f"可用group_props_name: {', '.join(sorted(self._group_props_names))}")

        # 各分类控件数量
        for category in WidgetCategory:
            count = len(self._widgets_by_category[category])
            if count > 0:
                result.append(f"  {category.value}: {count} 个")

        return "\n".join(result)


class _CategoryManager:
    """
    分类管理器，提供特定分类的控件操作接口
    """

    def __init__(self, manager: 'ControlManager', category: WidgetCategory):
        """
        初始化分类管理器

        参数:
            manager: 父控件管理器
            category: 控件分类
        """
        self._manager = manager
        self._category = category

    def add(self, control_name: str, object_name: Optional[str] = None, **kwargs) -> ControlBaseData:
        """
        向该分类添加控件

        参数:
            control_name: 控件的全局唯一标识名
            object_name: 控件对象名，如果为None则使用control_name
            **kwargs: 控件属性

        返回:
            创建的控件数据对象
        """
        # 确保设置了正确的分类
        kwargs['widget_category'] = self._category

        # 调用父管理器的创建方法
        return self._manager.create_widget(self._category, control_name, object_name, **kwargs)

    def __getattr__(self, object_name: str) -> Any:
        """
        通过object_name获取控件

        参数:
            object_name: 控件的对象名

        返回:
            控件数据对象

        异常:
            AttributeError: 如果控件不存在
        """
        # 从父管理器的分类字典中查找
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})

        # 遍历查找object_name匹配的控件
        for widget in widgets_dict.values():
            if widget.object_name == object_name:
                return widget

        # 如果找不到，抛出AttributeError
        raise AttributeError(f"分类 '{self._category.value}' 中没有名为 '{object_name}' 的控件")

    def __getitem__(self, object_name: str) -> Any:
        """支持通过[]语法访问控件（使用object_name）"""
        return self.__getattr__(object_name)

    def __contains__(self, object_name: str) -> bool:
        """检查object_name是否存在"""
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})
        return any(widget.object_name == object_name for widget in widgets_dict.values())

    def __iter__(self):
        """迭代该分类的所有控件"""
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})
        return iter(widgets_dict.values())

    def __len__(self) -> int:
        """获取该分类的控件数量"""
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})
        return len(widgets_dict)

    def keys(self):
        """获取所有控件的control_name"""
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})
        return widgets_dict.keys()

    def values(self):
        """获取所有控件对象"""
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})
        return widgets_dict.values()

    def items(self):
        """获取(control_name, 控件对象)对"""
        widgets_dict = self._manager._widgets_by_category.get(self._category, {})
        return widgets_dict.items()

    def __str__(self) -> str:
        """字符串表示"""
        count = len(self)
        return f"{self._category.value}管理器 (共 {count} 个控件)"


# 单例控件管理器实例
# ----------------------------------------------------------------------------------------------------------------
_global_control_manager = None


def get_control_manager() -> ControlManager:
    """
    获取全局控件管理器单例

    返回:
        全局控件管理器实例
    """
    global _global_control_manager
    if _global_control_manager is None:
        _global_control_manager = ControlManager()
    return _global_control_manager


# 使用示例
# ----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    from obsScriptFramework_.src.tool.scriptCsv2Json import ControlTemplateParser
    parser = ControlTemplateParser()
    # 获取控件管理器
    cm = get_control_manager()

    print("=" * 60)
    print("控件管理器使用示例")
    print("=" * 60)

    # 1. 获取基础group控件
    print("\n1. 基础group控件")
    print("-" * 40)
    basic_group = cm.get_basic_group()
    print(f"基础group控件: {basic_group.control_name}")
    print(f"  props_name: {basic_group.props_name}")
    print(f"  group_props_name: {basic_group.group_props_name}")
    print(f"可用group_props_name: {cm.available_group_props_names}")

    result = parser.parse_csv(
        "../data/widgetData.csv",
        initial_props_name=cm.get_basic_group().group_props_name
    )
    parser.export_to_json(result, "parsed_controls_with_props.json")
    for controls_data in result["all_controls"]:
        controls = getattr(cm, controls_data["widget_category"].lower())
        args = controls_data["group_properties"]["group_1"] | controls_data["group_properties"].get("group_2", {})
        args |= {"props_name": controls_data["props_name"]}
        del args['control_name']
        controls.add(
            control_name=controls_data["group_properties"]["group_1"]["control_name"],
            object_name=controls_data["object_name"],
            **args
        )

    # 2. 添加控件示例
    print("\n2. 添加控件示例")
    print("-" * 40)

    # 添加一个复选框，使用基础group的group_props_name作为props_name
    cm.checkbox.add(
        control_name="enable_feature",
        object_name="enable_feature_checkbox",
        description="启用高级功能",
        long_description="启用功能",
        modified_callback_enabled=False,
        checked=True,
        props_name="props"  # 来自基础group的group_props_name
    )
    print(f"添加了复选框: enable_feature (props_name: 'props')")
    print(cm.checkbox.enable_feature_checkbox.props_name)

    # 添加一个数字框
    cm.digitalbox.add(
        control_name="volume_level",
        object_name="volume_slider",
        description="音量大小",
        widget_variant=DigitalBoxVariant.INT_SLIDER,
        value=75,
        min_val=0,
        max_val=100,
        suffix="%",
        props_name="props"  # 来自基础group的group_props_name
    )
    print(f"添加了数字框: volume_level (props_name: 'props')")

    # 3. 添加一个新分组框
    print("\n3. 添加新分组框示例")
    print("-" * 40)

    # 添加一个可勾选分组框
    cm.group.add(
        control_name="audio_settings",
        object_name="audio_group",
        description="音频设置",
        widget_variant=GroupVariant.CHECKABLE,
        group_props_name="audio_props",  # 新的group_props_name
        props_name="props",  # 来自基础group的group_props_name
        checked=True
    )
    print(f"添加了分组框: audio_settings")
    print(f"  group_props_name: 'audio_props'")
    print(f"  props_name: 'props'")

    # 现在可以向audio_props添加控件
    cm.checkbox.add(
        control_name="enable_echo",
        object_name="echo_checkbox",
        description="启用回声消除",
        checked=False,
        props_name="audio_props"  # 来自audio_settings分组的group_props_name
    )
    print(f"添加了复选框: enable_echo (props_name: 'audio_props')")

    # 4. 验证规则测试
    print("\n4. 验证规则测试")
    print("-" * 40)

    # 测试1: 尝试使用无效的props_name
    try:
        cm.checkbox.add(
            control_name="test_invalid_props",
            object_name="test_invalid",
            description="测试无效props_name",
            checked=True,
            props_name="invalid_props"  # 不存在于任何group的group_props_name中
        )
    except ValueError as e:
        print(f"测试1 - 使用无效props_name: {e}")

    # 测试2: 尝试添加group_props_name重复的分组
    try:
        cm.group.add(
            control_name="duplicate_group",
            object_name="dup_group",
            description="重复分组",
            widget_variant=GroupVariant.NORMAL,
            group_props_name="audio_props",  # 已经存在
            props_name="props"
        )
    except ValueError as e:
        print(f"测试2 - 重复group_props_name: {e}")

    # 测试3: 尝试添加group_props_name等于props_name的分组
    try:
        cm.group.add(
            control_name="invalid_group",
            object_name="invalid_grp",
            description="无效分组",
            widget_variant=GroupVariant.NORMAL,
            group_props_name="props",  # 等于props_name，这是不允许的（基础group除外）
            props_name="props"
        )
    except ValueError as e:
        print(f"测试3 - group_props_name等于props_name: {e}")

    # 测试4: 尝试使用保留名称"group"作为control_name
    try:
        cm.checkbox.add(
            control_name="group",  # 保留名称
            object_name="group_checkbox",
            description="测试保留名称",
            checked=True,
            props_name="props"
        )
    except ValueError as e:
        print(f"测试4 - 使用保留名称: {e}")

    # 5. 添加更多分组和控件
    print("\n5. 添加更多分组和控件")
    print("-" * 40)

    # 添加另一个分组框
    cm.group.add(
        control_name="video_settings",
        object_name="video_group",
        description="视频设置",
        widget_variant=GroupVariant.NORMAL,
        group_props_name="video_props",
        props_name="props"
    )
    print(f"添加了分组框: video_settings (group_props_name: 'video_props')")

    # 向video_props添加控件
    cm.combobox.add(
        control_name="resolution",
        object_name="res_combo",
        description="分辨率",
        widget_variant=ComboBoxVariant.LIST,
        display_text="1920x1080",
        value="1920x1080",
        items=[
            {"label": "1920x1080 (全高清)", "value": "1920x1080"},
            {"label": "1280x720 (高清)", "value": "1280x720"},
            {"label": "3840x2160 (4K)", "value": "3840x2160"}
        ],
        props_name="video_props"  # 来自video_settings分组的group_props_name
    )
    print(f"添加了组合框: resolution (props_name: 'video_props')")

    # 6. 显示统计信息
    print("\n6. 统计信息")
    print("-" * 40)
    print(cm)

    # 7. 按load_order排序的控件列表（不包含基础group）
    print("\n7. 按load_order排序的控件列表（不包含基础group）")
    print("-" * 40)

    sorted_widgets = cm.get_widgets_by_load_order()
    for widget in sorted_widgets:
        props_info = f"props_name: {widget.props_name}"
        if widget.widget_category == WidgetCategory.GROUP:
            props_info += f", group_props_name: {widget.group_props_name}"
        print(f"  [{widget.load_order:2d}] {widget.widget_category.value}: {widget.control_name} ({props_info})")

    # 8. 获取props_name映射（不包含基础group）
    print("\n8. props_name到控件的映射（不包含基础group）")
    print("-" * 40)

    props_mapping = cm.get_props_mapping()
    for props_name, control_names in props_mapping.items():
        print(f"  {props_name}: {', '.join(control_names)}")

    # 9. 通过control_name查找控件测试
    print("\n9. 通过control_name查找控件")
    print("-" * 40)

    # 查找基础group控件
    basic_group = cm.get_widget_by_control_name("group")
    print(f"查找基础group控件: {'成功' if basic_group else '失败'}")

    # 查找常规控件
    volume_widget = cm.get_widget_by_control_name("volume_level")
    print(f"查找volume_level: {'成功' if volume_widget else '失败'}")

    # 查找不存在的控件
    non_existent = cm.get_widget_by_control_name("non_existent")
    print(f"查找不存在的控件: {'成功' if non_existent else '失败'}")

    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)
