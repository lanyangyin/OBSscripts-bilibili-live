"""按钮单击函数框架"""
from typing import Callable, Any


class ObsScriptButtonFunction:

    def __init__(self, BtnFunctions, log):
        self.BtnFunctions = BtnFunctions
        self.log = log

    def select(self, button_name: str) -> Callable[[Any, Any], bool]:
        def build_bf(ps, p):
            try:
                getattr(self.BtnFunctions, button_name)(button_name)
            except AttributeError:
                self.log.log_error(f"未找到名为【{button_name}】的回调函数")
            return True
        return build_bf