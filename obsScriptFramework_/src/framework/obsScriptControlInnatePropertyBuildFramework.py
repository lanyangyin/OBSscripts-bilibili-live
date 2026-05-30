"""为控件管理器中添加控件及其天赋属性"""
# 使用正确的相对导入（从 framework 到 data，再到其他需要的模块）
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

# 为了类型提示（可选）
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
    参数：
        control_manager: 控件管理器实例
        control_property_table_dictionary: 包含控件定义的字典，必须包含键 "all_controls"
        log_manager: 日志管理器实例
        modified_function_manager: 修改回调函数管理器
        button_function_manager: 按钮回调函数管理器
    """
    def pull_innate_attribute_data_log_of_control(control_name, attribute):
        """
        拉取控件天赋属性日志
        :param control_name:
        :param attribute:
        :return:
        """
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

        kwargs = {"props_name": controls_data["props_name"]}
        kwargs |= controls_data["group_properties"]["group_1"]
        kwargs |= controls_data["group_properties"].get("group_2", {})

        control_name = controls_data["group_properties"]["group_1"]["control_name"]
        log_manager.log_info(control_name)

        del kwargs["control_name"]

        if kwargs["modified_callback_enabled"]:
            if controls_data["widget_category"] == "GROUP" and kwargs["widget_variant"] == "CHECKABLE":
                # 内置的可折叠分组框中折叠动作的数据变动实现
                modified_callback_name = kwargs["modified_callback"]
                def group_folded_modified_callback(ps, p, st=None, _control_name=control_name, _modified_callback_name=modified_callback_name):
                    """
                    折叠分组框的控件变动回调函数
                    :param ps:
                    :param p:
                    :param st:
                    :param _control_name: 折叠分组框的控件名称
                    :param _modified_callback_name: 除了折叠之外的函数实现的控件变动函数回调名称
                    :return:
                    """
                    widget = control_manager.get_widget_by_control_name(_control_name)
                    """获取控件管理器中的折叠分组框控件对象"""
                    group_props_name = widget.group_props_name
                    widget_visibility_less_list = sys_common_data_manager.get_data("system", "group_folded_props_names")
                    """已折叠组的props_name的列表"""
                    if not widget_visibility_less_list:  # 如果props_name在已折叠组的props_name的列表中就删除，不在就添加
                        sys_common_data_manager.add_data("system", "group_folded_props_names", group_props_name, 999)
                    else:
                        if group_props_name in widget_visibility_less_list:
                            sys_common_data_manager.remove_data("system", "group_folded_props_names", group_props_name)
                        else:
                            sys_common_data_manager.add_data("system", "group_folded_props_names", group_props_name, 999)
                    widget_visibility_less_list = sys_common_data_manager.get_data("system", "group_folded_props_names")
                    widget.folding_visible = widget.group_props_name not in widget_visibility_less_list
                    widget.folding_enabled = widget.group_props_name not in widget_visibility_less_list
                    widget.checked = widget.group_props_name not in widget_visibility_less_list
                    if not widget.checked:
                        log_manager.log_info(f"折叠分组框{control_name}")
                        update_widget_for_props_dict = {widget.props_name:[_control_name]}
                    else:
                        log_manager.log_info(f"展开分组框{control_name}")
                        update_widget_for_props_dict = {
                            widget.props_name: [_control_name],
                            widget.group_props_name: control_manager.get_props_mapping()[widget.group_props_name]
                        }
                    """props_name到控件control_name列表的映射字典"""
                    control_ui_updater_manager.update(
                        update_widget_for_props_dict=update_widget_for_props_dict
                    )
                    modified_function_manager.property_modified(_control_name, _modified_callback_name)(ps, p, st)
                    return True
                kwargs["modified_callback"] = group_folded_modified_callback
            else:
                kwargs["modified_callback"] = modified_function_manager.property_modified(control_name, kwargs["modified_callback"])

        if kwargs.get("click_callback", False):
            kwargs["click_callback"] = button_function_manager.select(kwargs["click_callback"])

        kwargs["widget_category"] = getattr(WidgetCategory, controls_data["widget_category"])

        if kwargs["widget_variant"]:
            category = kwargs["widget_category"]
            variant_name = kwargs["widget_variant"]
            try:
                if category == WidgetCategory.CHECKBOX:  # 无
                    kwargs["widget_variant"] = getattr(CheckBoxVariant, variant_name)
                elif category == WidgetCategory.DIGITALBOX:
                    kwargs["widget_variant"] = getattr(DigitalBoxVariant, variant_name)
                elif category == WidgetCategory.TEXTBOX:
                    kwargs["widget_variant"] = getattr(TextBoxVariant, variant_name)
                elif category == WidgetCategory.BUTTON:
                    kwargs["widget_variant"] = getattr(ButtonVariant, variant_name)
                elif category == WidgetCategory.COMBOBOX:
                    kwargs["widget_variant"] = getattr(ComboBoxVariant, variant_name)
                elif category == WidgetCategory.PATHBOX:
                    kwargs["widget_variant"] = getattr(PathBoxVariant, variant_name)
                elif category == WidgetCategory.COLORBOX:
                    kwargs["widget_variant"] = getattr(ColorBoxVariant, variant_name)
                elif category == WidgetCategory.FONTBOX:  # 无
                    kwargs["widget_variant"] = getattr(FontBoxVariant, variant_name)
                elif category == WidgetCategory.LISTBOX:
                    kwargs["widget_variant"] = getattr(ListBoxVariant, variant_name)
                elif category == WidgetCategory.GROUP:
                    kwargs["widget_variant"] = getattr(GroupVariant, variant_name)
            except:
                log_manager.log_error(f"在为{control_name}添加widget_variant时出现错误，【{variant_name}】")

        control_manager_category.add(
            control_name=control_name,
            object_name=controls_data["object_name"],
            **kwargs,
        )
        pull_innate_attribute_data_log_of_control(
            control_name=control_name,
            attribute=f"{kwargs}"
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
            modified_callback=modified_function_manager.property_modified("e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
                                                                          None),
            click_callback=lambda pr, ps: None,
        )
        pull_innate_attribute_data_log_of_control(
            control_name="e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083",
            attribute="底部按钮控件属性组"
        )
