import os

import obspython as obs
from typing import Any, Dict, List, Optional, Literal

from plugins.tool.parseColor import int_to_color_str
# 根据您的实际文件路径调整导入
from ..data.obsScriptControlData import (
    WidgetCategory,
    CheckBoxData,
    DigitalBoxData,
    TextBoxData,
    ButtonData,
    ComboBoxData,
    PathBoxData,
    GroupData,
    DigitalBoxVariant,
    TextBoxVariant,
    ComboBoxVariant,
    GroupVariant,
    TextBoxInfoVariant, ListBoxData, ColorBoxData, FontBoxData, ColorBoxVariant,
)


class UIUpdater:
    """
    OBS 脚本 UI 更新器，负责将控件数据模型的状态同步到 OBS 界面。

    该类封装了原有的 update_ui_interface_data 函数，将脚本设置存储作为依赖项，
    通过构造函数传入，避免直接引用全局变量，提高可测试性和模块化。

    Attributes:
        script_settings: OBS 数据对象 (obs_data_t)，用于读写控件值。
    """

    def __init__(self, script_settings: Any, control_manager: Any, Log_manager: Any) -> None:
        """
        初始化 UIUpdater 实例。

        Args:
            control_manager: 包含控件列表和相关方法的对象，必须提供 get_widgets_by_load_order() 方法，
                    返回一个由控件数据对象（如 CheckBoxData、DigitalBoxData 等）组成的列表。
            script_settings: OBS 数据对象，通常为 GlobalVariableOfData.script_settings。
        """
        self.script_settings = script_settings
        self.control_manager = control_manager
        self.Log_manager = Log_manager

    def update(self, update_widget_for_props_dict: Dict[str, List[str]]) -> bool:
        """
        更新 UI 界面数据，使控件状态与内部数据模型同步。

        遍历所有需要关注的控件（通过 self.control_manager.get_widgets_by_load_order() 获取），
        根据预定义的配置（update_widget_for_props_dict）更新控件的可见性、
        启用状态以及当前值。同时将用户界面的改动写回到 script_settings 中。

        Args:
            update_widget_for_props_dict: 字典，键为控件所属属性集名称（props_name），
                                           值为该属性集下需要动态更新的控件名称列表（control_name）。

        Returns:
            bool: 始终返回 True，表示更新完成。

        Notes:
            - 控件数据对象应继承自 ControlBaseData，并包含对应类型的专用属性。
            - 本方法仅处理原有逻辑中涉及的控件类型（复选框、数字框、文本框、按钮、组合框、路径框、分组框），
              颜色框、字体框、列表框暂不处理（可后续扩展）。
        """
        for w in self.control_manager.get_widgets_by_load_order():
            # 检查当前控件是否需要动态更新
            if w.props_name not in update_widget_for_props_dict:
                continue
            elif w.control_name not in update_widget_for_props_dict[w.props_name]:
                continue

            self.Log_manager.log_info(
                f"{w.control_name}可见状态{obs.obs_property_visible(w.obj)}⏩{w.visible}"
            )
            # 更新可见性
            if w.widget_variant == GroupVariant.CHECKABLE:
                self.Log_manager.log_info(
                    f"--{w.control_name}折叠状态{w.folding_visible}"
                )
                if w.visible:
                    obs.obs_property_set_visible(w.obj, w.folding_visible)
                    obs.obs_property_set_visible(w.folding_control_obj, not w.folding_visible)
                else:
                    obs.obs_property_set_visible(w.obj, w.visible)
                    obs.obs_property_set_visible(w.folding_control_obj, w.visible)
            else:
                if obs.obs_property_visible(w.obj) != w.visible:
                    obs.obs_property_set_visible(w.obj, w.visible)

            self.Log_manager.log_info(
                f"{w.control_name}启用状态{obs.obs_property_enabled(w.obj)}⏩{w.enabled}"
            )
            # 更新启用状态
            if w.widget_variant is GroupVariant.CHECKABLE:
                self.Log_manager.log_info(
                    f"--{w.control_name}折叠状态{w.folding_enabled}"
                )
                if w.enabled:
                    obs.obs_property_set_enabled(w.obj, w.folding_enabled)
                    obs.obs_property_set_enabled(w.folding_control_obj, not w.folding_enabled)
                else:
                    obs.obs_property_set_enabled(w.obj, w.enabled)
                    obs.obs_property_set_enabled(w.folding_control_obj, w.enabled)
            else:
                if obs.obs_property_enabled(w.obj) != w.enabled:
                    obs.obs_property_set_enabled(w.obj, w.enabled)

            # 根据控件分类进行数据同步
            category = w.widget_category

            # 复选框
            if category is WidgetCategory.CHECKBOX:
                if isinstance(w, CheckBoxData):
                    self._update_checkbox(w)

            # 数字框
            elif category is WidgetCategory.DIGITALBOX:
                if isinstance(w, DigitalBoxData):
                    self._update_digitalbox(w)

            # 文本框
            elif category is WidgetCategory.TEXTBOX:
                if isinstance(w, TextBoxData):
                    self._update_textbox(w)

            # 按钮（无需数据同步）
            elif category is WidgetCategory.BUTTON:
                pass

            # 组合框
            elif category is WidgetCategory.COMBOBOX:
                if isinstance(w, ComboBoxData):
                    self._update_combobox(w)

            # 路径框
            elif category is WidgetCategory.PATHBOX:
                if isinstance(w, PathBoxData):
                    self._update_pathbox(w)

            # 分组框
            elif category is WidgetCategory.GROUP:
                if isinstance(w, GroupData):
                    self._update_group(w)

            # 颜色框
            elif category is WidgetCategory.COLORBOX:
                if isinstance(w, ColorBoxData):
                    self._update_colorbox(w)

            # 字体框
            elif category is WidgetCategory.FONTBOX:
                if isinstance(w, FontBoxData):
                    self._update_fontbox(w)

            # 列表框
            elif category is WidgetCategory.LISTBOX:
                if isinstance(w, ListBoxData):
                    self._update_listbox(w)

            # 其他控件类型（颜色框、字体框、列表框）暂不处理，可后续扩展
            else:
                # 可在此添加日志或忽略
                pass

        return True

    # ----------------------------------------------------------------------
    # 私有更新方法，按控件类型拆分以提高可读性
    # ----------------------------------------------------------------------

    def _update_checkbox(self, w: CheckBoxData) -> None:
        """同步复选框控件的值。"""
        #  获取当前数据
        current_bool = obs.obs_data_get_bool(self.script_settings, w.control_name)
        #  数据审查
        if type(w.checked) is not bool:
            self.Log_manager.log_warning(f"复选框 {w.control_name} 期望 bool，实际为 {type(w.checked)}")
        #  记录更新
        self.Log_manager.log_info(f"{w.control_name}的勾选状态{current_bool}⏩{w.checked}")
        #  执行更新
        if current_bool != w.checked:
            obs.obs_data_set_bool(self.script_settings, w.control_name, w.checked)

    def _update_digitalbox(self, w: DigitalBoxData) -> None:
        """同步数字框控件的范围与值。"""
        #  获取当前数据
        variant = w.widget_variant
        if variant in (DigitalBoxVariant.INT, DigitalBoxVariant.INT_SLIDER):
            current_min = obs.obs_property_int_min(w.obj)
            current_max = obs.obs_property_int_max(w.obj)
            current_step = obs.obs_property_int_step(w.obj)
            current_value = obs.obs_data_get_int(self.script_settings, w.control_name)
        elif variant in (DigitalBoxVariant.FLOAT, DigitalBoxVariant.FLOAT_SLIDER):
            current_min = obs.obs_property_float_min(w.obj)
            current_max = obs.obs_property_float_max(w.obj)
            current_step = obs.obs_property_float_step(w.obj)
            current_value = obs.obs_data_get_double(self.script_settings, w.control_name)
        #  数据审查
        if variant in (DigitalBoxVariant.INT, DigitalBoxVariant.INT_SLIDER):
            if type(w.digital) is not int:
                self.Log_manager.log_warning(f"数字框 {w.control_name} 期望 int，实际为 {type(w.digital)}")
        elif variant in (DigitalBoxVariant.FLOAT, DigitalBoxVariant.FLOAT_SLIDER):
            if type(w.digital) is not float:
                self.Log_manager.log_warning(f"数字框 {w.control_name} 期望 float，实际为 {type(w.digital)}")
        #  记录更新
        self.Log_manager.log_info(f"{w.control_name}最小值{current_min}⏩{w.min_val}")
        self.Log_manager.log_info(f"{w.control_name}最大值{current_max}⏩{w.max_val}")
        self.Log_manager.log_info(f"{w.control_name}步数{current_step}⏩{w.step}")
        self.Log_manager.log_info(f"{w.control_name}数值{current_value}⏩{w.digital}")
        #  执行更新
        if variant in (DigitalBoxVariant.INT, DigitalBoxVariant.INT_SLIDER):
            if w.min_val != current_min or w.max_val != current_max or w.step != current_step:  # 整数范围更新
                obs.obs_property_int_set_limits(w.obj, int(w.min_val), int(w.max_val), int(w.step))
            if current_value != w.digital:  # 值更新
                obs.obs_data_set_int(self.script_settings, w.control_name, w.digital)
        elif variant in (DigitalBoxVariant.FLOAT, DigitalBoxVariant.FLOAT_SLIDER):
            if w.min_val != current_min or w.max_val != current_max or w.step != current_step:  # 浮点数范围更新
                obs.obs_property_float_set_limits(w.obj, float(w.min_val), float(w.max_val), float(w.step))
            if current_value != w.digital:  # 值更新
                obs.obs_data_set_double(self.script_settings, w.control_name, w.digital)

    def _update_textbox(self, w: TextBoxData) -> None:
        """同步文本框控件的类型与内容。"""
        #  获取当前数据
        variant = w.widget_variant
        if variant is TextBoxVariant.INFO:
            current_info_type = obs.obs_property_text_info_type(w.obj)
        current_string = obs.obs_data_get_string(self.script_settings, w.control_name)
        #  数据审查
        if variant is TextBoxVariant.INFO:
            if type(w.info_type) is not TextBoxInfoVariant:
                self.Log_manager.log_warning(f"文本框 {w.control_name} 期望 TextBoxInfoVariant，实际为 {type(w.info_type)}")
        if type(w.text) is not str:
            self.Log_manager.log_warning(f"文本框 {w.control_name} 期望 str，实际为 {type(w.text)}")
        #  记录更新
        if variant is TextBoxVariant.INFO:
            self.Log_manager.log_info(f"{w.control_name}文本提示类型{current_info_type}⏩{w.info_type}")
        self.Log_manager.log_info(f"{w.control_name}文本{current_string}⏩{w.text}")
        #  执行更新
        if variant is TextBoxVariant.INFO:
            if current_info_type != w.info_type.value:  # 更新信息类型
                obs.obs_property_text_set_info_type(w.obj, w.info_type.value)
        if current_string != w.text:  # 文本内容更新
            obs.obs_data_set_string(self.script_settings, w.control_name, w.text)

    def _update_combobox(self, w: ComboBoxData) -> None:
        """同步组合框控件的选项与当前值。"""
        #  获取当前数据
        current_options = []
        """当前选项列表数据"""
        item_count = obs.obs_property_list_item_count(w.obj)
        for idx in range(item_count):
            label = obs.obs_property_list_item_name(w.obj, idx)
            value = obs.obs_property_list_item_string(w.obj, idx)
            current_options.append({"label": label, "value": value})
        current_string = obs.obs_data_get_string(self.script_settings, w.control_name)
        #  数据审查
        if not isinstance(w.items, list):
            self.Log_manager.log_warning(f"组合框 {w.control_name} 期望 list，实际为 {type(w.items)}")
            label_exists = False
            value_exists = False
        else:
            label_exists = any(item.get("label") == w.label for item in w.items)
            value_exists = any(item.get("value") == w.value for item in w.items)
        if type(w.label) is not str:
            self.Log_manager.log_warning(f"组合框 {w.control_name} 期望 str，实际为 {type(w.label)}")
        if type(w.value) is not str:
            self.Log_manager.log_warning(f"组合框 {w.control_name} 期望 str，实际为 {type(w.value)}")
        if not label_exists:
            self.Log_manager.log_warning(f"组合框 {w.control_name} 期望 in {w.items}，实际为 {w.label}")
        if not value_exists:
            self.Log_manager.log_warning(f"组合框 {w.control_name} 期望 in {w.items}，实际为 {w.value}")
        #  记录更新
        if w.items != current_options:
            self.Log_manager.log_info(f"{w.control_name}组合框列表{current_options}⏩{w.items}")
        self.Log_manager.log_info(f"{w.control_name}组合框显示文本{current_string}⏩{w.label}")
        #  执行更新
        if w.items != current_options:  # 设定组合框列表
            obs.obs_property_list_clear(w.obj)  # 清除列表
            for item in w.items:  # 先将当前显示文本对应的项插入到索引 0
                if item["label"] == w.label:
                    obs.obs_property_list_insert_string(w.obj, 0, item["label"], item["value"])
                    break
            for item in w.items:
                if item["label"] != w.label:
                    obs.obs_property_list_add_string(w.obj, item["label"], item["value"])
        if w.widget_variant is ComboBoxVariant.EDITABLE:  # 可编辑列表显示文本更新
            if current_string != w.label:
                if label_exists:
                    obs.obs_data_set_string(self.script_settings, w.control_name, w.label)
                else:
                    first_item_name = obs.obs_property_list_item_name(w.obj, 0)
                    obs.obs_data_set_string(self.script_settings, w.control_name, first_item_name)
        elif w.widget_variant is ComboBoxVariant.LIST:  # 不可编辑列表显示文本更新
            if current_string != w.value:
                if value_exists:
                    obs.obs_data_set_string(self.script_settings, w.control_name, w.value)
                else:
                    first_item_value = obs.obs_property_list_item_string(w.obj, 0)
                    obs.obs_data_set_string(self.script_settings, w.control_name, first_item_value)

    def _update_pathbox(self, w: PathBoxData) -> None:
        """同步路径框控件的路径文本。"""
        #  获取当前数据
        current_path = obs.obs_data_get_string(self.script_settings, w.control_name)
        #  数据审查
        if type(w.path_text) is not str:
            self.Log_manager.log_warning(f"路径框 {w.control_name} 期望 str，实际为 {type(w.path_text)}")
        if not os.path.exists(w.path_text):
            self.Log_manager.log_warning(f"路径框 {w.control_name} 路径不存在: {w.path_text}")
        #  记录更新
        self.Log_manager.log_info(f"{w.control_name}路径框{current_path}⏩{w.path_text}")
        #  执行更新
        if current_path != w.path_text:
            obs.obs_data_set_string(self.script_settings, w.control_name, w.path_text)

    def _update_group(self, w: GroupData) -> None:
        """同步分组框控件的勾选状态（如果可勾选）。"""
        #  获取当前数据
        variant = w.widget_variant
        if variant is GroupVariant.CHECKABLE:
            current_bool = obs.obs_data_get_bool(self.script_settings, w.control_name)
        #  数据审查
        if variant is GroupVariant.CHECKABLE:
            if type(w.checked) is not bool:
                self.Log_manager.log_warning(f"分组框 {w.control_name} 期望 bool，实际为 {type(w.checked)}")
        #  记录更新
        if variant is GroupVariant.CHECKABLE:
            self.Log_manager.log_info(f"{w.control_name}分组框{current_bool}⏩{w.checked}")
        #  执行更新
        if variant is GroupVariant.CHECKABLE:
            if current_bool != w.checked:
                obs.obs_data_set_bool(self.script_settings, w.control_name, w.checked)
            obs.obs_data_set_bool(self.script_settings, w.control_name.encode().hex(), w.checked)  # 同步折叠控件选项状态

    def _update_colorbox(self, w: ColorBoxData) -> None:
        """
        从 settings 读取颜色值并更新模型。

        OBS 颜色存储格式：0xAARRGGBB
        示例：0x80FF0000 = 50% 透明度的红色
        """
        #  获取当前数据
        current = obs.obs_data_get_int(self.script_settings, w.control_name)
        #  数据审查
        if type(w.color_value) is not int:
            self.Log_manager.log_warning(f"颜色框 {w.control_name} 期望 int，实际为 {type(w.color_value)}")
        #  记录更新
        self.Log_manager.log_info(
            f"{w.control_name}的颜色{int_to_color_str(current)}⏩{int_to_color_str(w.color_value)}"
        )
        #  执行更新
        if current != w.color_value:
            obs.obs_data_set_int(self.script_settings, w.control_name, w.color_value)

    def _update_fontbox(self, w: FontBoxData) -> None:
        """
        从 settings 读取字体数据（obs_data_t）并更新 FontBoxData 模型。

        字体数据格式：
        - "current_face"    ：字体名称，如 "Microsoft YaHei"、"Arial"
        - "current_size"    ：字体大小，整数
        - "current_style"   ：样式字符串，如 "Regular"、"Bold"
        - "current_flags"   ：标志位，按位组合控制粗体、斜体等
        """
        #  获取当前数据
        current_font_data = obs.obs_data_get_obj(self.script_settings, w.control_name)
        if current_font_data:
            current_face = obs.obs_data_get_string(current_font_data, "face")
            current_size = obs.obs_data_get_int(current_font_data, "size")
            current_style = obs.obs_data_get_string(current_font_data, "style")
            current_flags = obs.obs_data_get_int(current_font_data, "flags")
            obs.obs_data_release(current_font_data)  # 务必释放字体数据对象，避免内存泄漏
        else:
            current_face = current_size = current_style = current_flags = None
        #  数据审查
        if type(w.font_face) is not str:
            self.Log_manager.log_warning(f"字体框 {w.control_name} 期望 str，实际为 {type(w.font_face)}")
        if type(w.font_size) is not int:
            self.Log_manager.log_warning(f"字体框 {w.control_name} 期望 int，实际为 {type(w.font_size)}")
        if type(w.font_style) is not str:
            self.Log_manager.log_warning(f"字体框 {w.control_name} 期望 str，实际为 {type(w.font_style)}")
        if type(w.font_flags) is not int:
            self.Log_manager.log_warning(f"字体框 {w.control_name} 期望 int，实际为 {type(w.font_flags)}")
        #  记录更新
        self.Log_manager.log_info(f"{w.control_name}的字体系列名称{current_face}⏩{w.font_face}")
        self.Log_manager.log_info(f"{w.control_name}的字体大小{current_size}px⏩{w.font_size}px")
        self.Log_manager.log_info(f"{w.control_name}的字体样式{current_style}⏩{w.font_style}")
        self.Log_manager.log_info(f"{w.control_name}的字体标志位{current_flags}⏩{w.font_flags}")
        if current_flags is not None:
            self.Log_manager.log_info(f"{w.control_name}的标志粗体{bool(current_flags & 1)}⏩{w.font_bold}")
            self.Log_manager.log_info(f"{w.control_name}的标志斜体{bool(current_flags & 2)}⏩{w.font_italic}")
            self.Log_manager.log_info(f"{w.control_name}的标志下划线{bool(current_flags & 4)}⏩{w.font_underline}")
            self.Log_manager.log_info(f"{w.control_name}的标志删除线{bool(current_flags & 8)}⏩{w.font_strikeout}")
        else:
            self.Log_manager.log_info(f"{w.control_name}的标志粗体(无数据)⏩{w.font_bold}")
            self.Log_manager.log_info(f"{w.control_name}的标志斜体(无数据)⏩{w.font_italic}")
            self.Log_manager.log_info(f"{w.control_name}的标志下划线(无数据)⏩{w.font_underline}")
            self.Log_manager.log_info(f"{w.control_name}的标志删除线(无数据)⏩{w.font_strikeout}")

        #  执行更新
        if (current_face != w.font_face or current_size != w.font_size or
                current_style != w.font_style or current_flags != w.font_flags):
            font_data = obs.obs_data_create()
            obs.obs_data_set_string(font_data, "face", w.font_face)
            obs.obs_data_set_int(font_data, "size", w.font_size)
            obs.obs_data_set_string(font_data, "style", w.font_style)
            obs.obs_data_set_int(font_data, "flags", w.font_flags)
            obs.obs_data_set_obj(self.script_settings, w.control_name, font_data)
            obs.obs_data_release(font_data)

    def _update_listbox(self, w: ListBoxData) -> None:
        """
        从 settings 读取列表框数据（obs_data_array_t）并更新 ListBoxData 模型。

        列表框数据格式：
        - 存储在 settings 中的是一个 obs_data_array_t（数组对象）
        - 数组每个元素是一个 obs_data_t 对象，格式为 {"value": str, "selected": bool, "hidden": bool}
        - 主要读取 "value" 字段获取列表项内容
        """
        current_array = obs.obs_data_get_array(self.script_settings, w.control_name)
        current_items = []
        if current_array is not None:
            count = obs.obs_data_array_count(current_array)
            for i in range(count):
                item_obj = obs.obs_data_array_item(current_array, i)
                # 从 obs_data_t 中提取字段
                val = obs.obs_data_get_string(item_obj, "value")
                sel = obs.obs_data_get_bool(item_obj, "selected")
                hid = obs.obs_data_get_bool(item_obj, "hidden")
                current_items.append({"value": val, "selected": sel, "hidden": hid})
                obs.obs_data_release(item_obj)
            obs.obs_data_array_release(current_array)

        # 数据审查
        if not isinstance(w.items, list):
            self.Log_manager.log_warning(
                f'列表框 {w.control_name} 期望 list，实际为 {type(w.items)}'
            )

        # 记录更新
        if current_items != w.items:
            self.Log_manager.log_info(f"{w.control_name}列表框内容{current_items}⏩{w.items}")

        # 执行更新（从模型写回 settings）
        # 注意：这里假定 w.items 已经是模型希望同步到的目标状态
        # 如果需要将用户界面改动反向同步回模型，则相反方向。但 UIUpdater 通常负责模型 -> UI，此处我们做 UI -> 模型
        # 然而本方法名 _update_listbox 调用时机是模型变化后刷新 UI，所以应该将 w.items 写入 settings
        # 为了保持一致，我们实现写入逻辑（与其它 _update_xxx 方向一致）
        if current_items != w.items:
            # 构建新数组
            new_array = obs.obs_data_array_create()
            for item in w.items:
                obj = obs.obs_data_create()
                obs.obs_data_set_string(obj, "value", item.get("value", "?"))
                obs.obs_data_set_bool(obj, "selected", item.get("selected", False))
                obs.obs_data_set_bool(obj, "hidden", item.get("hidden", False))
                obs.obs_data_array_push_back(new_array, obj)
                obs.obs_data_release(obj)
            obs.obs_data_set_array(self.script_settings, w.control_name, new_array)
            obs.obs_data_array_release(new_array)