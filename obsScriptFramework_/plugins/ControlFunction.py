"""控件数据get函数"""
import json
from functools import lru_cache

from plugins.GlobalVariable import GlobalVariable
from src.data.obsScriptControlData import TextBoxInfoVariant
from .tool.addClearCache import add_clear_cache, ClearableCache
from .tool.addAliases import add_aliases, AliasMeta

class ControlDataSetFunction(ClearableCache, metaclass=AliasMeta):
    """获得计算控件自由属性值的缓存回调函数"""
    def __init__(self, sys_c_d_m, control_manager):
        self.sys_c_d_m = sys_c_d_m
        self.control_manager = control_manager

    @lru_cache(maxsize=None)
    @add_clear_cache
    def get_common_group_fold(self, *args, **kwargs) -> set[str]:
        """
        获取已折叠分组框所对应属性集名称的集合
        :return: 属性集名称集合
        """
        widget_visibility_less_list = self.sys_c_d_m.get_data("system", "group_folded_props_names")
        widget_visibility_less_set = set(widget_visibility_less_list)
        return widget_visibility_less_set

    @lru_cache(maxsize=None)
    @add_clear_cache
    def group_foldless_is(self, *args, **kwargs) -> bool:
        """
        获取控件是否展开
        :param args:
        :param kwargs:
            control_name
        :return: 是否展开
        """
        ControlDataSetFunction.clear()
        control_name = kwargs["control_name"]
        widget = self.control_manager.get_widget_by_control_name(control_name)
        group_props_name = widget.group_props_name
        widget_visibility_less_set = self.get_common_group_fold()
        return group_props_name not in widget_visibility_less_set

    @staticmethod
    @lru_cache(maxsize=None)
    @add_clear_cache
    def default_true(*args, **kwargs):
        return True

    @staticmethod
    @lru_cache(maxsize=None)
    @add_clear_cache
    def default_false(*args, **kwargs):
        return False

    @staticmethod
    @lru_cache(maxsize=None)
    @add_clear_cache
    def test(*args, **kwargs):
        return True

    @staticmethod
    @lru_cache(maxsize=None)
    @add_clear_cache
    def test1(*args, **kwargs):
        return True

    #  ==============================================参考数据============================================================
    ## 按钮网址
    @staticmethod
    def url_reference_data(*args, **kwargs):
        v = "https://www.tcptest.cn/http"
        return v

    ## 单选框选择状态
    @staticmethod
    def checked_reference_data(*args, **kwargs):
        v = True
        return v

    @staticmethod
    def checked_reference_data0(*args, **kwargs):
        v = False
        return v

    ## 数字框数值
    @staticmethod
    def min_val_reference_data(*args, **kwargs):
        v = 0
        return v

    @staticmethod
    def min_val_reference_data0(*args, **kwargs):
        v = 1
        return v

    @staticmethod
    def max_val_reference_data(*args, **kwargs):
        v = 100
        return v

    @staticmethod
    def max_val_reference_data0(*args, **kwargs):
        v = 1000
        return v

    @staticmethod
    def step_reference_data(*args, **kwargs):
        v = 1
        return v

    @staticmethod
    def step_reference_data0(*args, **kwargs):
        v = 9
        return v

    @staticmethod
    def digital_reference_data(*args, **kwargs):
        v = 50
        return v

    @staticmethod
    def digital_reference_data0(*args, **kwargs):
        v = 2
        return v

    @staticmethod
    def digital_reference_dataX(*args, **kwargs):
        v = 2000
        return v

    ## 通知框类型
    @staticmethod
    def info_type_reference_data(*args, **kwargs):
        v = TextBoxInfoVariant.NORMAL
        return v

    @staticmethod
    def info_type_reference_data0(*args, **kwargs):
        v = TextBoxInfoVariant.ERROR
        return v

    @staticmethod
    def info_type_reference_data1(*args, **kwargs):
        v = TextBoxInfoVariant.WARNING
        return v

    ## 文本框内容
    @staticmethod
    def text_reference_data(*args, **kwargs):
        v = GlobalVariable.text_test
        return v

    @staticmethod
    def text_reference_data0(*args, **kwargs):
        v = "这是一段文本测试0"
        return v

    ## 组合框
    @staticmethod
    def label_reference_data(*args, **kwargs):
        v = "这是组合框/列表框元素标签测试1"
        return v

    @staticmethod
    def label_reference_data0(*args, **kwargs):
        v = "这是组合框标签测试"
        return v

    @staticmethod
    def label_reference_data1(*args, **kwargs):
        v = "这是组合框标签测试"
        return v

    @staticmethod
    def value_reference_data(*args, **kwargs):
        v = "v这是组合框/列表框元素值测试1"
        return v

    @staticmethod
    def value_reference_data0(*args, **kwargs):
        v = "这是组合框值测试"
        return v

    @staticmethod
    def value_reference_data1(*args, **kwargs):
        v = "这是组合框值测试"
        return v

    @staticmethod
    def items_reference_data(*args, **kwargs):
        v = [
            {
                "label": "这是组合框/列表框元素标签测试",
                "value": "v这是组合框/列表框元素值测试",
            },
            {
                "label": "这是组合框/列表框元素标签测试0",
                "value": "v这是组合框/列表框元素值测试0",
            },
            {
                "label": "这是组合框/列表框元素标签测试1",
                "value": "v这是组合框/列表框元素值测试1",
            },
            {
                "label": "这是组合框/列表框元素标签测试1",
                "value": "v这是组合框/列表框元素值测试1",
            },
            {
                "label": "这是组合框/列表框元素标签测试1",
                "value": "v这是组合框/列表框元素值测试1",
            }
        ]
        return v

    @staticmethod
    def items_reference_data0(*args, **kwargs):
        v = [
            {
                "value": "这是组合框/列表框元素值测试",
                "selected": False,
                "hidden": False
            },
            {
                "value": "这是组合框/列表框元素值测试0",
                "selected": True,
                "hidden": False
            },
            {
                "value": "这是组合框/列表框元素值测试1",
                "selected": True,
                "hidden": False
            },
            {
                "value": "这是组合框/列表框元素值测试2",
                "selected": False,
                "hidden": False
            }
        ]
        return v

    ## 颜色框
    @staticmethod
    def color_alpha_reference_data(*args, **kwargs):
        v = 200
        return v

    @staticmethod
    def color_red_reference_data(*args, **kwargs):
        v = 255
        return v

    @staticmethod
    def color_green_reference_data(*args, **kwargs):
        v = 128
        return v

    @staticmethod
    def color_blue_reference_data(*args, **kwargs):
        v = 234
        return v

    ##  字体框
    @staticmethod
    def font_face_reference_data(*args, **kwargs):
        v = "Kai"
        return v

    @staticmethod
    def font_size_reference_data(*args, **kwargs):
        v = 36
        return v

    @staticmethod
    def font_style_reference_data(*args, **kwargs):
        v = "Regular"
        return v

    @staticmethod
    def font_bold_reference_data(*args, **kwargs):
        v = False
        return v

    @staticmethod
    def font_italic_reference_data(*args, **kwargs):
        v = False
        return v

    @staticmethod
    def font_underline_reference_data(*args, **kwargs):
        v = False
        return v

    @staticmethod
    def font_strikeout_reference_data(*args, **kwargs):
        v = False
        return v

    @staticmethod
    def path_text_reference_data(*args, **kwargs):
        v = "C:\\"
        return v


