"""控件变动回调函数框架"""
from typing import Callable, Any


class ModifiedFunction:

    def __init__(self, BtnFunctions, log_manager):
        self.BtnFunctions = BtnFunctions
        self.Log_manager = log_manager
        self.allow_execution = True

    def property_modified(self, control_name:str, modified_callback_name:str) -> Callable[[Any, Any, Any], bool]:
        def build_pm(ps, p, st=None) -> bool:
            self.Log_manager.log_info(f"监测到控件变动: {control_name}")
            if control_name == "e58581e8aeb8e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083":
                self.allow_execution = True
                self.Log_manager.log_info("允许执行控件修改回调")
            elif control_name == "e7a681e6ada2e689a7e8a18ce68ea7e4bbb6e4bfaee694b9e59b9ee8b083":
                self.allow_execution = False
                self.Log_manager.log_info("禁止执行控件修改回调")
            elif self.allow_execution:
                try:
                    return getattr(self.BtnFunctions, modified_callback_name)(control_name=control_name)
                except AttributeError:
                    self.Log_manager.log_error(f"未找到【{control_name}】对应的控件变动回调函数")
            return False
        return build_pm