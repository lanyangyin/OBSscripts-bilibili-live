import os
import sys
from pathlib import Path
import obspython as obs

script_file_path = Path(__file__)
"""脚本文件路径"""
script_file_dir = script_file_path.parent
"""脚本所在文件夹路径"""
script_file_name = script_file_path.stem
"""脚本无后缀名称"""
script_config_folder = script_file_dir.joinpath(script_file_name + "_")
"""脚本配置文件夹路径"""
os.makedirs(script_config_folder, exist_ok=True)  # 新建脚本配置文件夹
sys.path.insert(0, f'{script_config_folder}')  # 将脚本配置文件夹也加入环境用来导入包
ImportSuccess = (False, None)

try:
    # 尝试从脚本配置文件夹导入（生产环境）
    from src.tool.LogManager import LogManager
    from src.tool.scriptCsv2Json import ControlTemplateParser
    from src.tool.CommonDataManager import CommonDataManager
    from src.data.obsScriptGlobalVariable import ObsScriptGlobalData, ObsScriptGlobalManager
    from src.data.obsScriptControlData import WidgetCategory
    from src.data.obsScriptControlData import (CheckBoxVariant, DigitalBoxVariant, TextBoxVariant, ButtonVariant,
                                               ComboBoxVariant, PathBoxVariant, ColorBoxVariant, FontBoxVariant,
                                               ListBoxVariant, GroupVariant)
    from plugins.ButtonFunction import BtnFunction
    from plugins.ControlFunction import ControlDataSetFunction
    from src.framework.obsScriptControlDataFramework import get_control_manager
    from src.framework.obsScriptControlInnatePropertyBuildFramework import build_controls
    from src.framework.obsScriptControlFreePropertyBuildFramework import apply_user_properties
    from src.framework.obsScriptModifiedFunctionFramework import ModifiedFunction
    from src.framework.obsTriggerFrontendEventFramework import TriggerFrontendEvent
    from src.framework.obsScriptControlUiUpdaterFramework import UIUpdater
    from src.framework.obsSciptButtonFunctionFramework import ObsScriptButtonFunction  # 确保两个块一致
    ImportSuccess = (True, None)

except ImportError:
    # 若失败，尝试从开发测试路径导入
    try:
        from obsScriptFramework_.src.tool.LogManager import LogManager
        from obsScriptFramework_.src.tool.scriptCsv2Json import ControlTemplateParser
        from obsScriptFramework_.src.tool.CommonDataManager import CommonDataManager
        from obsScriptFramework_.src.data.obsScriptGlobalVariable import ObsScriptGlobalData, ObsScriptGlobalManager
        from obsScriptFramework_.src.data.obsScriptControlData import WidgetCategory
        from obsScriptFramework_.src.data.obsScriptControlData import (CheckBoxVariant, DigitalBoxVariant, TextBoxVariant,
                                                                       ButtonVariant, ComboBoxVariant, PathBoxVariant,
                                                                       ColorBoxVariant, FontBoxVariant, ListBoxVariant,
                                                                       GroupVariant)
        from obsScriptFramework_.plugins.ButtonFunction import BtnFunction
        from obsScriptFramework_.plugins.ControlFunction import ControlDataSetFunction
        from obsScriptFramework_.src.framework.obsScriptControlDataFramework import get_control_manager
        from obsScriptFramework_.src.framework.obsSciptButtonFunctionFramework import ObsScriptButtonFunction
        from obsScriptFramework_.src.framework.obsScriptControlInnatePropertyBuildFramework import build_controls
        from obsScriptFramework_.src.framework.obsScriptControlFreePropertyBuildFramework import apply_user_properties
        from obsScriptFramework_.src.framework.obsScriptModifiedFunctionFramework import ModifiedFunction
        from obsScriptFramework_.src.framework.obsTriggerFrontendEventFramework import TriggerFrontendEvent
        from obsScriptFramework_.src.framework.obsScriptControlUiUpdaterFramework import UIUpdater
        ImportSuccess = (True, None)

    except ImportError as e:
        ImportSuccess = (False, str(e.msg))
        obs.script_log(obs.LOG_ERROR, str(e.msg))


def script_defaults(settings):  # 设置其默认值
    """
    调用以设置与脚本关联的默认设置(如果有的话)。为了设置其默认值，您通常会调用默认值函数。
    :param settings:与脚本关联的设置。
    """
    # 包载入判断
    if not ImportSuccess[0]:
        return
    # 脚本设置体
    ObsScriptGlobalData.settings = settings
    # # 控件系统属性常用设置文件路径
    # ObsScriptGlobalData.control_system_properties_common_settings_filepath = script_config_folder / ObsScriptGlobalData.control_system_properties_common_settings_filename
    # 日志管理器
    ObsScriptGlobalManager.Log_manager = LogManager(ObsScriptGlobalData.log_folder_path)
    # 控件管理器
    ObsScriptGlobalManager.control_manager = get_control_manager()
    # 控件属性文档转换器
    ObsScriptGlobalManager.control_parser_manager = ControlTemplateParser()
    # 控件系统属性常用设置属性
    ObsScriptGlobalManager.sys_common_data_manager = CommonDataManager(filepath=ObsScriptGlobalData.control_system_properties_common_settings_filepath)
    ObsScriptGlobalManager.ControlUiUpdaterManager = UIUpdater(
        script_settings=ObsScriptGlobalData.settings,
        control_manager=ObsScriptGlobalManager.control_manager,
        Log_manager=ObsScriptGlobalManager.Log_manager
    )
    # 按钮回调函数类
    ObsScriptGlobalData.BtnFunctions = BtnFunction(
        Log_manager=ObsScriptGlobalManager.Log_manager,
        sys_c_d_m=ObsScriptGlobalManager.sys_common_data_manager,
        control_manager=ObsScriptGlobalManager.control_manager,
        control_ui_updater_manager=ObsScriptGlobalManager.ControlUiUpdaterManager
    )
    # 控件获取属性函数类
    ObsScriptGlobalData.ControlDataSetFunctions = ControlDataSetFunction(
        sys_c_d_m=ObsScriptGlobalManager.sys_common_data_manager,
        control_manager=ObsScriptGlobalManager.control_manager
    )
    # 前端事件触发管理器
    ObsScriptGlobalManager.trigger_front_event_manager = TriggerFrontendEvent(
        BtnFunctions=ObsScriptGlobalData.BtnFunctions,
        log_manager=ObsScriptGlobalManager.Log_manager
    )
    # 按钮回调函数管理器
    ObsScriptGlobalManager.button_function_manager = ObsScriptButtonFunction(
        BtnFunctions=ObsScriptGlobalData.BtnFunctions,
        log=ObsScriptGlobalManager.Log_manager
    )
    # 控件变动回调函数管理器
    ObsScriptGlobalData.modified_function_manager = ModifiedFunction(
        BtnFunctions=ObsScriptGlobalData.BtnFunctions,
        log_manager=ObsScriptGlobalManager.Log_manager
    )
    # 控件属性表字典
    ObsScriptGlobalData.control_property_table_dictionary = ObsScriptGlobalManager.control_parser_manager.parse_csv_files(
        attribute_def_path=ObsScriptGlobalData.control_attribute_definition_data_csv_filepath,
        data_path=ObsScriptGlobalData.control_data_csv_filepath,
        initial_props_name=ObsScriptGlobalManager.control_manager.get_basic_group().group_props_name
    )
    # 设定 天赋属性
    build_controls(
        control_manager=ObsScriptGlobalManager.control_manager,
        control_property_table_dictionary=ObsScriptGlobalData.control_property_table_dictionary,
        log_manager=ObsScriptGlobalManager.Log_manager,
        sys_common_data_manager=ObsScriptGlobalManager.sys_common_data_manager,
        modified_function_manager=ObsScriptGlobalData.modified_function_manager,
        button_function_manager=ObsScriptGlobalManager.button_function_manager,
        control_ui_updater_manager=ObsScriptGlobalManager.ControlUiUpdaterManager
    )
    # 设定控件用户属性
    apply_user_properties(
        log_manager=ObsScriptGlobalManager.Log_manager,
        control_manager=ObsScriptGlobalManager.control_manager,
        control_property_table_dictionary=ObsScriptGlobalData.control_property_table_dictionary,
        ControlDataSetFunctions=ObsScriptGlobalData.ControlDataSetFunctions,
        all_props_mapping=None
    )

def script_description():
    """
    调用以检索要在“脚本”窗口中显示给用户的描述字符串。
    """
    # 包载入判断
    if not ImportSuccess[0]:
        return ImportSuccess[1]
    return ObsScriptGlobalData.description


def script_load(settings):
    """
    在脚本启动时调用与脚本相关的特定设置。所提供的设置参数通常不用于由用户设置的设置;
    相反，该参数用于脚本中可能使用的任何额外的内部设置数据。
    :param settings:与脚本关联的设置。
    """
    # 包载入判断
    if not ImportSuccess[0]:
        return
    ObsScriptGlobalManager.Log_manager.log_info(f"{script_file_name} 加载成功")
    obs.obs_frontend_add_event_callback(ObsScriptGlobalManager.trigger_front_event_manager.event_callback())
    pass


def script_update(settings):
    """
    当用户更改了脚本的设置(如果有的话)时调用。
    这里更改控件属性不会实时显示，
    不要在这里控制控件的【可见】、【可用】、【值】和【名称】
    :param settings:与脚本关联的设置。
    """
    # 包载入判断
    if not ImportSuccess[0]:
        return
    pass


def script_properties():
    """主属性创建函数"""
    # 包载入判断
    if not ImportSuccess[0]:
        return None
    ObsScriptGlobalManager.Log_manager.log_info(f"生成控件")

    for props_name in ObsScriptGlobalManager.control_manager.available_group_props_names:
        ObsScriptGlobalManager.Log_manager.log_info(f"构建属性集: {props_name}")
        ObsScriptGlobalData.props_dict[props_name] = obs.obs_properties_create()

    sorted_widgets = ObsScriptGlobalManager.control_manager.get_widgets_by_load_order()
    for w in sorted_widgets:
        w.props = ObsScriptGlobalData.props_dict[w.props_name]
        if hasattr(w, "group_props_name"):
            w.group_props = ObsScriptGlobalData.props_dict[w.group_props_name]

        # 获取按载入次序排序的所有控件列表
        if w.widget_category == WidgetCategory.CHECKBOX:
            # 添加复选框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"复选框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_bool(w.props, w.control_name, w.description)
        elif w.widget_category == WidgetCategory.DIGITALBOX:
            # 添加数字控件
            ObsScriptGlobalManager.Log_manager.log_info(f"数字框控件: {w.control_name} 【{w.description}】")
            if w.widget_variant == DigitalBoxVariant.INT_SLIDER:
                w.obj = obs.obs_properties_add_int_slider(
                    w.props, w.control_name, w.description, w.min_val, w.max_val, w.step
                )
            elif w.widget_variant == DigitalBoxVariant.INT:
                w.obj = obs.obs_properties_add_int(
                    w.props, w.control_name, w.description, w.min_val, w.max_val, w.step
                )
            elif w.widget_variant == DigitalBoxVariant.FLOAT_SLIDER:
                w.obj = obs.obs_properties_add_float_slider(
                    w.props, w.control_name, w.description, w.min_val, w.max_val, w.step
                )
            elif w.widget_variant == DigitalBoxVariant.FLOAT:
                w.obj = obs.obs_properties_add_float(
                    w.props, w.control_name, w.description, w.min_val, w.max_val, w.step
                )
            if w.widget_variant == DigitalBoxVariant.INT_SLIDER or w.widget_variant == DigitalBoxVariant.INT:
                obs.obs_property_int_set_suffix(w.obj, w.suffix)
            if w.widget_variant == DigitalBoxVariant.FLOAT_SLIDER or w.widget_variant == DigitalBoxVariant.FLOAT:
                obs.obs_property_float_set_suffix(w.obj, w.suffix)
        elif w.widget_category == WidgetCategory.TEXTBOX:
            # 添加文本框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"文本框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_text(w.props, w.control_name, w.description, w.widget_variant.value)
        elif w.widget_category == WidgetCategory.BUTTON:
            # 添加按钮控件
            ObsScriptGlobalManager.Log_manager.log_info(f"按钮控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_button(
                w.props, w.control_name, w.description, w.click_callback
            )
            obs.obs_property_button_set_type(w.obj, w.widget_variant.value)
            if w.widget_variant == ButtonVariant.URL:  # 是否为链接跳转按钮
                obs.obs_property_button_set_url(w.obj, w.url)
        elif w.widget_category == WidgetCategory.COMBOBOX:
            # 添加组合框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"组合框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_list(
                w.props, w.control_name, w.description, w.widget_variant.value, obs.OBS_COMBO_FORMAT_STRING
            )
        elif w.widget_category == WidgetCategory.PATHBOX:
            # 添加路径对话框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"路径对话框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_path(
                w.props, w.control_name, w.description, w.widget_variant.value, w.filter_str, w.default_path
            )
        elif w.widget_category == WidgetCategory.COLORBOX:
            # 添加颜色对话框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"颜色对话框控件: {w.control_name} 【{w.description}】")
            if w.widget_variant == ColorBoxVariant.COLOR:
                w.obj = obs.obs_properties_add_color(w.props, w.control_name, w.description)
            elif w.widget_variant == ColorBoxVariant.ALPHA:
                w.obj = obs.obs_properties_add_color_alpha(w.props, w.control_name, w.description)
        elif w.widget_category == WidgetCategory.FONTBOX:
            # 添加字体对话框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"字体对话框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_font(w.props, w.control_name, w.description)
        elif w.widget_category == WidgetCategory.LISTBOX:
            # 添加列表对话框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"列表对话框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_editable_list(
                w.props, w.control_name, w.description, w.widget_variant.value, w.filter_str, w.default_path
            )
        elif w.widget_category == WidgetCategory.GROUP:
            # 分组框控件
            ObsScriptGlobalManager.Log_manager.log_info(f"分组框控件: {w.control_name} 【{w.description}】")
            w.obj = obs.obs_properties_add_group(
                w.props, w.control_name, w.description + f"{'[⏬]' if w.widget_variant == GroupVariant.CHECKABLE else ''}", w.widget_variant.value, w.group_props
            )
            if w.widget_variant == GroupVariant.CHECKABLE:  # 如果分组框的派生类型是复选分组框
                # 添加复选框控件作为折叠分组框
                ObsScriptGlobalManager.Log_manager.log_info(f"折叠分组框[复选框控件]: {w.control_name} 【{w.description}】")
                w.folding_control_obj = obs.obs_properties_add_bool(w.props, w.control_name.encode().hex(), w.description + "[⏫]")
                widget_visibility_less_list = ObsScriptGlobalManager.sys_common_data_manager.get_data("system", "group_folded_props_names")
                w.folding_visible = w.group_props_name not in widget_visibility_less_list
                w.folding_enabled = w.group_props_name not in widget_visibility_less_list
                w.checked = w.group_props_name not in widget_visibility_less_list

        if w.long_description:
            obs.obs_property_set_long_description(w.obj, w.long_description)

        if w.modified_callback_enabled:
            ObsScriptGlobalManager.Log_manager.log_info(f"为{w.widget_category}: 【{w.description}】添加钩子函数")
            obs.obs_property_set_modified_callback(w.obj, w.modified_callback)
            if w.widget_variant == GroupVariant.CHECKABLE:  # 如果分组框的派生类型是复选分组框
                ObsScriptGlobalManager.Log_manager.log_info(f"为{w.widget_category}: 【{w.description}】添加钩子函数")
                obs.obs_property_set_modified_callback(w.folding_control_obj, w.modified_callback)
    # GlobalVariableOfData.props_dict = props_dict
    # 更新UI界面数据#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
    ObsScriptGlobalManager.ControlUiUpdaterManager.update(
        update_widget_for_props_dict=ObsScriptGlobalManager.control_manager.get_props_mapping()
    )
    return ObsScriptGlobalData.props_dict[ObsScriptGlobalManager.control_manager.get_basic_group().group_props_name]

    pass


def script_tick(seconds):
    """
    每帧调用
    这里更改控件属性不会实时显示，
    不要在这里控制控件的【可见】、【可用】、【值】和【名称】
    Args:
        seconds:

    Returns:

    """
    # 包载入判断
    if not ImportSuccess[0]:
        return
    pass


def script_unload():
    """
    在脚本被卸载时调用。
    """
    # 包载入判断
    if not ImportSuccess[0]:
        return
    ObsScriptGlobalManager.Log_manager.flush()
    pass




