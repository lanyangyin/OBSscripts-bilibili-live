"""前端事件触发管理框架头"""
from ..data.ExplanatoryDictionary import *

class TriggerFrontendEvent:
    """前端事件触发管理器"""
    def __init__(self, BtnFunctions, log_manager):
        """

        :param kwargs:
        """
        self.BtnFunctions = BtnFunctions
        self.Log_manager = log_manager
        self.allow_execution = True

    def event_callback(self):
        def trigger_frontend_event(event):
            """前端事件触发回调"""
            self.Log_manager.log_info(f"监测到obs前端事件: {information4frontend_event[event]}")
            if self.allow_execution:
                self.allow_execution = False
                self.Log_manager.log_info("允许执行前端事件回调")
                try:
                    getattr(self.BtnFunctions, FrontendEvent(event).name)
                except AttributeError:
                    self.Log_manager.log_debug(f"未找到【{FrontendEvent(event).name}】回调函数")
                self.allow_execution = True
            else:
                self.Log_manager.log_debug("正在执行其他的前端事件回调，禁止执行")
        return trigger_frontend_event

