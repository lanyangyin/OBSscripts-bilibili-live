"""定义了一些脚本的全局变量"""
import pathlib
from pathlib import Path
from typing import Any, Union


class ClassProperty:
    """类属性装饰器，允许像实例属性一样访问类方法"""

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, owner):
        return self.fget(owner)


class ObsScriptGlobalData:
    """脚本的全局数据变量"""

    BtnFunctions = None
    ControlDataSetFunctions = None
    control_property_table_dictionary: dict[str, Any] = {}
    # update_widget_for_props_dict: dict[str, list[str]] = {}
    # """根据控件属性集更新控件"""
    version: str = "1.0.0"
    """脚本版本号"""
    settings: Any = None
    """脚本设置体"""
    causeOfTheFrontDeskIncident = None
    """前台事件引起的原因"""
    props_dict = {}
    """控件属性集的字典"""
    property_modified_callback_allow_execution: bool = True
    """属性修改回调执行许可"""

    # 路径变量------------------------------------------------------------------------------------------------------
    __data_dir_path = Path(__file__).parent
    """
    数据文件存放文件夹路径
    ~/obsScriptFramework_/src/data
    """

    control_system_properties_common_settings_filename: str = "sys_common_config.json"
    """系统常用数据配置文件名"""
    @ClassProperty
    def control_system_properties_common_settings_filepath(self) -> str:
        """
        系统常用数据配置文件路径
        ~/obsScriptFramework_/[系统常用数据配置文件名]
        """
        return str(self.__data_dir_path.parent.parent / self.control_system_properties_common_settings_filename)

    log_folder_name:str = "LOG"
    """保存日志文件的文件夹名称"""
    @ClassProperty
    def log_folder_path(self) -> str:
        """
        控件数据定义的csv文件路径
        ~/obsScriptFramework_/[保存日志文件的文件夹名称]
        """
        return str(self.__data_dir_path.parent.parent / self.log_folder_name)

    control_data_csv_filename: str = "widgetData.csv"
    """控件数据的csv文件名"""
    @ClassProperty
    def control_data_csv_filepath(self) -> str:
        """
        控件数据的csv文件路径
        ~/obsScriptFramework_/plugins/[控件数据的csv文件名]
        """
        return str(self.__data_dir_path.parent.parent / "plugins" / self.control_data_csv_filename)

    description_filename: str = "obsScriptDescription.html"
    """脚本介绍文件名称"""
    @ClassProperty
    def description(self) -> str:
        """
        脚本介绍文件内容
        ~/obsScriptFramework_/plugins/[脚本介绍文件名称]
        """
        try:
            with open(self.__data_dir_path.parent.parent / "plugins" / self.description_filename, encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError as e:
            return str(e)

    control_attribute_definition_data_csv_filename: str = "widgetAttributeDefinitionData.csv"
    """控件数据定义的csv文件名"""
    @ClassProperty
    def control_attribute_definition_data_csv_filepath(self) -> str:
        """
        控件数据定义的csv文件路径
        ~/obsScriptFramework_/src/data/[控件数据定义的csv文件名]
        """
        return str(self.__data_dir_path / self.control_attribute_definition_data_csv_filename)


class ObsScriptGlobalManager:
    """脚本的全局管理器变量"""
    Log_manager = None
    """日志管理器"""
    control_manager: Any = None
    """控件管理器"""
    control_parser_manager: Any = None
    """控件属性文档转换器"""
    trigger_front_event_manager = None
    """前端事件触发管理器"""
    button_function_manager = None
    """按钮回调函数管理器"""
    sys_common_data_manager = None
    """系统常用数据管理器"""
    ControlUiUpdaterManager = None
    """"""


if __name__ == "__main__":
    print(ObsScriptGlobalData.description_filename)
    print(ObsScriptGlobalData.description)
    print(ObsScriptGlobalData.control_system_properties_common_settings_filepath)
