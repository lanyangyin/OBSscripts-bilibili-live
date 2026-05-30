"""
按钮单击回调函数/控件变动回调函数
"""
import json

from .ControlFunction import ControlDataSetFunction
from .tool.addAliases import add_aliases, AliasMeta

class BtnFunction(metaclass=AliasMeta):
    def __init__(self, Log_manager, sys_c_d_m, control_manager, control_ui_updater_manager):
        """

        :param Log_manager:
        :param sys_c_d_m:
        :param control_manager:
        """
        self.Log_manager = Log_manager
        self.sys_common_data_manager = sys_c_d_m
        self.control_manager = control_manager
        self.control_ui_updater_manager = control_ui_updater_manager

    # def top(self, *args, **kwargs):
    #     """第一个控件的变动回调"""
    #     self.Log_manager.log_info("top")
    #
    # def bottom(self, *args, **kwargs):
    #     """最后一个控件的变动回调"""
    #     self.Log_manager.log_info("bottom")
    #
    # def modified_group_fold(self, *args, **kwargs):
    #     ControlDataSetFunction.clear()
    #     control_name = kwargs["control_name"]
    #     widget = self.control_manager.get_widget_by_control_name(control_name)
    #     group_props_name = widget.group_props_name
    #     widget_visibility_less_list = self.sys_common_data_manager.get_data("system", "group_not_checked")
    #     if not widget_visibility_less_list:
    #         self.sys_common_data_manager.add_data("system", "group_not_checked", group_props_name, 999)
    #     else:
    #         if group_props_name in widget_visibility_less_list:
    #             self.sys_common_data_manager.remove_data("system", "group_not_checked", group_props_name)
    #         else:
    #             self.sys_common_data_manager.add_data("system", "group_not_checked", group_props_name)

    @add_aliases("test_digitalBox")
    def test(self, *args, **kwargs):
        self.Log_manager.log_info("test")

    def set_group_fold(self, *args, **kwargs):
        """折叠分组框"""
        control_name = kwargs["control_name"]
        self.Log_manager.log_info(f"折叠分组框{control_name}")

        update_widget_for_props_dict = self.control_manager.get_props_mapping()
        self.control_ui_updater_manager.update(
            update_widget_for_props_dict=update_widget_for_props_dict
        )
        return True


