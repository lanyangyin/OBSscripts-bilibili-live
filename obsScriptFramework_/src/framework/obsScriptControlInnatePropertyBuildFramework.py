"""为控件管理器中添加控件及其天赋属性"""
from ..data.obsScriptGlobalVariable import ObsScriptGlobalData
from ..data.obsScriptControlData import (
    WidgetCategory,
    CheckBoxVariant,
    DigitalBoxVariant,
    TextBoxVariant,
    ButtonVariant,
    ComboBoxVariant,
    PathBoxVariant,
    ColorBoxVariant,
    FontBoxVariant,
    ListBoxVariant,
    GroupVariant,
)
from typing import Any, Dict


def build_controls(
    control_manager: Any,
    control_property_table_dictionary: Dict[str, Any],
    log_manager: Any,
    sys_common_data_manager: Any,
    modified_function_manager: Any,
    button_function_manager: Any,
    control_ui_updater_manager: Any
) -> None:
    """
    根据提供的配置构建所有控件。
    在控件管理器中添加控件对象，并拉取对应的控件天赋属性到控件管理器中
    """
    def pull_innate_attribute_data_log_of_control(control_name, attribute):
        log_manager.log_info(f"拉取[{control_name}]天赋属性：{attribute}")

    # ---------- 1. 创建“允许执行控件修改回调”按钮 ----------
    if not hasattr(control_manager.button, "e58581e8aeb8e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083"):
        control_manager.button.add(
            control_name="e58581e8aeb8e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            object_name="e58581e8aeb8e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            description="允许执行控件修改回调",
            long_description="允许执行控件修改回调",
            widget_variant=ButtonVariant.DEFAULT,
            modified_callback_enabled=True,
            modified_callback=modified_function_manager.property_modified(
                "e58581e8aeb8e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
                None
            ),
            click_callback=lambda pr, ps: None,
        )
        pull_innate_attribute_data_log_of_control(
            control_name="e58581e8aeb8e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            attribute="顶部按钮控件属性组"
        )

    # ---------- 2. 构建 CSV 中定义的所有控件 ----------
    for controls_data in control_property_table_dictionary["all_controls"]:
        control_manager_category = getattr(control_manager, controls_data["widget_category"].lower())

        if hasattr(control_manager_category, controls_data["object_name"]):
            continue

        # 合并所有属性：优先 properties，然后各个 group_properties（后面的覆盖前面的，但一般不会重名）
        all_props = {}
        all_props.update(controls_data.get("properties", {}))
        for group_key, group_props in controls_data.get("group_properties", {}).items():
            all_props.update(group_props)

        # 从合并后的字典中提取必需字段
        control_name = all_props.get("control_name")
        if not control_name:
            log_manager.log_error(f"控件 {controls_data['object_name']} 缺少 control_name，跳过")
            continue

        log_manager.log_info(control_name)

        # 构建传给 add 方法的参数字典
        kwargs = {
            "props_name": controls_data["props_name"],
            "control_name": control_name,
            "object_name": controls_data["object_name"],
            "description": all_props.get("description"),
            "long_description": all_props.get("long_description"),
            "widget_variant": all_props.get("widget_variant"),
            "modified_callback_enabled": all_props.get("modified_callback_enabled", False),
            "modified_callback": all_props.get("modified_callback"),
        }

        # 添加其他可能存在的字段（例如 suffix, min_val, max_val, step 等）
        extra_fields = [
            "suffix", "callback", "filter_str", "default_path", "group_props_name",
            "url", "checked", "min_val", "max_val", "step", "digital", "info_type",
            "text", "label", "value", "items", "color_alpha", "color_red", "color_green",
            "color_blue", "font_face", "font_size", "font_style", "font_bold",
            "font_italic", "font_underline", "font_strikeout", "path_text",
            "load_order", "props", "obj", "group_props", "folding_control_obj",
            "folding_visible", "folding_enabled", "color_value", "font_data", "font_flags"
        ]
        for field in extra_fields:
            if field in all_props:
                kwargs[field] = all_props[field]

        # 特殊处理：按钮的 click_callback
        if controls_data["widget_category"] == "BUTTON":
            click_callback = all_props.get("click_callback")
            if click_callback:
                kwargs["click_callback"] = button_function_manager.select(click_callback)
            else:
                kwargs["click_callback"] = lambda pr, ps: None

        # 特殊处理：分组框的 group_props 和折叠逻辑
        group_props_name = all_props.get("group_props_name")
        if group_props_name:
            kwargs["group_props_name"] = group_props_name

        # 处理 modified_callback
        if kwargs.get("modified_callback_enabled"):
            if controls_data["widget_category"] == "GROUP" and kwargs.get("widget_variant") == "CHECKABLE":
                # 内置的可折叠分组框中折叠动作的数据变动实现
                def group_folded_modified_callback(ps, p, st=None, _control_name=control_name, _modified_callback_name=kwargs["modified_callback"]):
                    widget = control_manager.get_widget_by_control_name(_control_name)
                    if not widget:
                        return False
                    group_props_name = widget.group_props_name
                    widget_visibility_less_list = sys_common_data_manager.get_data("system", "group_folded_props_names") or []
                    if not widget_visibility_less_list:
                        sys_common_data_manager.add_data("system", "group_folded_props_names", group_props_name, 999)
                    else:
                        if group_props_name in widget_visibility_less_list:
                            sys_common_data_manager.remove_data("system", "group_folded_props_names", group_props_name)
                        else:
                            sys_common_data_manager.add_data("system", "group_folded_props_names", group_props_name, 999)
                    widget_visibility_less_list = sys_common_data_manager.get_data("system", "group_folded_props_names") or []
                    widget.folding_visible = group_props_name not in widget_visibility_less_list
                    widget.folding_enabled = group_props_name not in widget_visibility_less_list
                    widget.checked = group_props_name not in widget_visibility_less_list
                    if not widget.checked:
                        log_manager.log_info(f"折叠分组框{_control_name}")
                        update_widget_for_props_dict = {widget.props_name: [_control_name]}
                    else:
                        log_manager.log_info(f"展开分组框{_control_name}")
                        update_widget_for_props_dict = {
                            widget.props_name: [_control_name],
                            widget.group_props_name: control_manager.get_props_mapping().get(widget.group_props_name, [])
                        }
                    control_ui_updater_manager.update(update_widget_for_props_dict=update_widget_for_props_dict)
                    if _modified_callback_name:
                        modified_function_manager.property_modified(_control_name, _modified_callback_name)(ps, p, st)
                    return True
                kwargs["modified_callback"] = group_folded_modified_callback
            else:
                kwargs["modified_callback"] = modified_function_manager.property_modified(control_name, kwargs["modified_callback"])

        # 转换 widget_variant 字符串为对应的枚举值
        variant_str = kwargs.get("widget_variant")
        if variant_str:
            category = controls_data["widget_category"]
            try:
                if category == "CHECKBOX":
                    kwargs["widget_variant"] = getattr(CheckBoxVariant, variant_str)
                elif category == "DIGITALBOX":
                    kwargs["widget_variant"] = getattr(DigitalBoxVariant, variant_str)
                elif category == "TEXTBOX":
                    kwargs["widget_variant"] = getattr(TextBoxVariant, variant_str)
                elif category == "BUTTON":
                    kwargs["widget_variant"] = getattr(ButtonVariant, variant_str)
                elif category == "COMBOBOX":
                    kwargs["widget_variant"] = getattr(ComboBoxVariant, variant_str)
                elif category == "PATHBOX":
                    kwargs["widget_variant"] = getattr(PathBoxVariant, variant_str)
                elif category == "COLORBOX":
                    kwargs["widget_variant"] = getattr(ColorBoxVariant, variant_str)
                elif category == "FONTBOX":
                    kwargs["widget_variant"] = getattr(FontBoxVariant, variant_str)
                elif category == "LISTBOX":
                    kwargs["widget_variant"] = getattr(ListBoxVariant, variant_str)
                elif category == "GROUP":
                    kwargs["widget_variant"] = getattr(GroupVariant, variant_str)
            except AttributeError:
                log_manager.log_error(f"为 {control_name} 添加 widget_variant 时出错，无效值：{variant_str}")

        # 添加控件到管理器
        # 避免重复传递 control_name 和 object_name
        kwargs.pop("control_name", None)
        kwargs.pop("object_name", None)

        # 删除非控件构造参数的字段（这些字段可能来自 CSV 派生，但控件类不接受）
        unsupported_params = [
            "color_value",  # ColorBox 不接受
            "font_data",  # FontBox 不接受
            "font_flags",  # FontBox 不接受
            "folding_control_obj", "folding_visible", "folding_enabled",  # Group 运行时字段
            "group_props", "props", "obj", "load_order"  # 其他非构造参数
        ]
        for key in unsupported_params:
            kwargs.pop(key, None)

        control_manager_category.add(
            control_name=control_name,
            object_name=controls_data["object_name"],
            **kwargs,
        )
        pull_innate_attribute_data_log_of_control(
            control_name=control_name,
            attribute=str(kwargs)
        )

    # ---------- 3. 创建“禁止执行控件修改回调”按钮 ----------
    if not hasattr(control_manager.button, "e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083"):
        control_manager.button.add(
            control_name="e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            object_name="e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            description="禁止执行控件修改回调",
            long_description="禁止执行控件修改回调",
            widget_variant=ButtonVariant.DEFAULT,
            modified_callback_enabled=True,
            modified_callback=modified_function_manager.property_modified(
                "e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
                None
            ),
            click_callback=lambda pr, ps: None,
        )
        pull_innate_attribute_data_log_of_control(
            control_name="e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            attribute="底部按钮控件属性组"
        )