# obsScriptFramework_/src/framework/obsScriptControlFreePropertyBuildFramework.py
from src.data.obsScriptControlData import WidgetCategory, GroupVariant, TextBoxVariant


# 保留原有的 build_controls 函数，并在其下方添加新函数

def apply_user_properties(
    log_manager,
    control_manager,
    control_property_table_dictionary,
    ControlDataSetFunctions,
    all_props_mapping=None,
):
    """
    根据 CSV 中定义的控件自由属性，调用对应的回调函数填充控件对象属性。
    拉取控件自由属性到控件管理器中
    参数：
        log_manager: 日志管理器实例
        control_manager: 控件管理器实例
        control_property_table_dictionary: 包含控件定义的字典，必须包含键 "all_controls"
        ControlDataSetFunctions: ControlDataSetFunction 实例，包含获取属性值的方法
        update_widget_for_props_dict: 已有的需要更新控件的映射字典，如果为 None 则重新获取

    返回：
        all_props_mapping: 计算出的控件属性组名称到控件标识名列表的映射字典
    """

    # 确定需要更新控件的映射
    if all_props_mapping is None:
        all_props_mapping = control_manager.get_props_mapping()

    fold_props_name = ControlDataSetFunctions.get_common_group_fold()
    # 遍历所有控件数据，填充用户属性
    for controls_data in control_property_table_dictionary["all_controls"]:
        props_name = controls_data["props_name"]
        if props_name in fold_props_name:
            log_manager.log_info(f'被折叠的控件：{controls_data["group_properties"]["group_1"]["control_name"]}')
            # continue
        if props_name in all_props_mapping:
            # 合并所有属性
            all_props = {}
            all_props.update(controls_data.get("properties", {}))
            for group_key, group_props in controls_data.get("group_properties", {}).items():
                all_props.update(group_props)

            control_name = all_props.get("control_name")
            if not control_name:
                continue  # 或记录错误并跳过
            if control_name in all_props_mapping[props_name]:
                # 合并公共自由属性和私有自由属性
                control_properties = controls_data["group_properties"].get("group_3", {})
                control_properties |= controls_data["group_properties"].get("group_4", {})
                log_manager.log_info(f"拉取[{control_name}]自由属性：{control_properties}")

                # 获取控件对象
                control_manager_category = getattr(control_manager, controls_data["widget_category"].lower())
                control_manager_category_object = getattr(control_manager_category, controls_data["object_name"])

                # 遍历所有自由属性，调用对应的回调函数获取值并设置
                for control_properties_name in control_properties:
                    if getattr(control_manager_category_object, "widget_category") == WidgetCategory.GROUP:
                        if getattr(control_manager_category_object, "widget_variant") == GroupVariant.NORMAL:
                            if control_properties_name == "checked":
                                log_manager.log_info(
                                    f"⭕拉取[{control_name}]自由属性：{control_properties_name}|该控件无此属性值"
                                )
                                continue
                    elif getattr(control_manager_category_object, "widget_category") == WidgetCategory.TEXTBOX:
                        if getattr(control_manager_category_object, "widget_variant") != TextBoxVariant.INFO:
                            if control_properties_name == "info_type":
                                log_manager.log_info(
                                    f"⭕拉取[{control_name}]自由属性：{control_properties_name}|该控件无此属性值"
                                )
                                continue
                    control_property_function_name = control_properties[control_properties_name]
                    """控件自由属性值的获取函数的名称"""
                    if hasattr(ControlDataSetFunctions, str(control_property_function_name)):
                        get_property_function = getattr(ControlDataSetFunctions, control_property_function_name)
                        """控件自由属性值的获取函数，类型是函数"""
                        control_property_value = get_property_function(control_name=control_name)
                        """控件自由属性值的获取的值"""
                        setattr(control_manager_category_object, control_properties_name, control_property_value)
                        log_manager.log_info(
                            f"拉取[{control_name}]自由属性：{control_properties_name}|属性值获取回调函数名：{control_property_function_name}"
                        )
                    else:
                        log_manager.log_error(
                            f"❌拉取[{control_name}]自由属性：{control_properties_name}|属性值获取回调函数名：{control_property_function_name}"
                        )

    return all_props_mapping