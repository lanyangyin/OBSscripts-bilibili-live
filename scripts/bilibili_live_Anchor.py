# coding=utf-8
#         Copyright (C) 2024  lanyangyin
#
#         This program is free software: you can redistribute it and/or modify
#         it under the terms of the GNU General Public License as published by
#         the Free Software Foundation, either version 3 of the License, or
#         (at your option) any later version.
#
#         This program is distributed in the hope that it will be useful,
#         but WITHOUT ANY WARRANTY; without even the implied warranty of
#         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#         GNU General Public License for more details.
#
#         You should have received a copy of the GNU General Public License
#         along with this program.  If not, see <https://www.gnu.org/licenses/>.
#         2436725966@qq.com
# import asyncio
# import base64
import hashlib
import io
import json
import os
# import os
import pathlib
import random
import ssl
import string
# import pprint
import sys
# import tempfile
# import threading
import time
import urllib
from datetime import datetime, timedelta
from typing import Optional, Dict, Literal, Union, List, Any, Callable, Iterator
# import zlib
from urllib.parse import quote, unquote, parse_qs, urlparse
from pathlib import Path
import socket
import urllib.request
from urllib.error import URLError

import urllib3
from PIL.ImageFile import ImageFile
from requests.exceptions import SSLError

import obspython as obs
# import pypinyin
import qrcode
from qrcode.main import QRCode
import requests
import pyperclip as cb
from PIL import Image, ImageOps

# import websockets


# 控件默认属性（首字母大写）
DefaultPropertiesOfTheControl: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    "ControlType": "Base",  # 添加类型标识
    "Obj": None,  # 控件脚本对象
    "Props": None,  # 隶属属性集
    "Number": 0,  # 载入次序
    "Name": "",  # 唯一名称
    "Description": "",  # 说明文本
    "Visible": False,  # 可见状态
    "Enabled": False,  # 可用状态
    "ModifiedIs": False,  # 是否监听
}

# ️复选框控件
CheckBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "CheckBox",  # 设置具体类型
    "Bool": False,  # 复选框是否选中
}


# ️数字框控件
DigitalDisplay: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "DigitalDisplay",  # 设置具体类型
    "SliderIs": False,  # 数字框是否有滑块
    "Value": 0,  # 显示文本对应的选项值
    "Suffix": "",
    "Min": 0,  # 数字显示框或滑块控件的最小值
    "Max": 0,  # 数字显示框或滑块控件的最大值
    "Step": 0,  # 数字显示框或滑块控件的步长
}


# 文本框控件
TextBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "TextBox",  # 设置具体类型
    "Type": None,  # 文本框类型
    # - obs.OBS_TEXT_DEFAULT        表示单行文本框，
    # - obs.OBS_TEXT_PASSWORD       表示单行密码文本框，
    # - obs.OBS_TEXT_MULTILINE      表示多行文本框，
    # - obs.OBS_TEXT_INFO           表示不可编辑的只读文本框，效果类似于标签。
    "Text": "",  # 显示文本
    "InfoType": None,  # 信息类型
    # - obs.OBS_TEXT_INFO_NORMAL    表示正常信息，
    # - obs.OBS_TEXT_INFO_WARNING   表示警告信息，
    # - obs.OBS_TEXT_INFO_ERROR     表示错误信息
}


# ️按钮控件
Button: Dict[str, Optional[Union[int, str, bool, Any, Callable]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "Button",  # 设置具体类型
    "Type": None,  # 按钮类型
    # - obs.OBS_BUTTON_DEFAULT      表示标准普通按钮
    # - obs.OBS_BUTTON_URL          表示可打开指定 URL 的链接按钮
    "Callback": None,  # 回调函数
    "Url": "",  # 需要打开的 URL
}


# 组合框控件
ComboBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "ComboBox",  # 设置具体类型
    "Type": None,  # 组合框类型
    # - obs.OBS_COMBO_TYPE_EDITABLE 表示可编辑组合框
    # - obs.OBS_COMBO_TYPE_LIST     表示不可编辑组合框
    "Text": "",  # 显示文本
    "Value": "",  # 显示文本对应的选项值
    "Dictionary": {},  # 数据字典
}


# ️ 路径对话框控件
PathBox: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "PathBox",  # 设置具体类型
    "Type": None,  # 路径对话框类型
    # OBS_PATH_FILE         表示读取文件的对话框
    # OBS_PATH_FILE_SAVE    表示写入文件的对话框
    # OBS_PATH_DIRECTORY    表示选择文件夹的对话框
    "Text": "",  # 显示文本
    "Filter": "",  # 文件种类（筛选条件）
    "StartPath": "", # 对话框起始路径
}


# 分组框控件（独立控件）
Group: Dict[str, Optional[Union[int, str, bool, Any]]] = {
    **DefaultPropertiesOfTheControl,
    "ControlType": "Group",  # 设置具体类型
    "Type": None,  # 分组框类型
    # OBS_GROUP_NORMAL      表示标准普通分组框
    # OBS_GROUP_CHECKABLE   表示拥有复选框的分组框
    "GroupProps": None,  # 统辖属性集
}


# 复选框控件实例
class CheckBoxP:
    """复选框控件实例"""

    def __init__(self, **kwargs):
        for key, value in CheckBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<CheckBoxP Name='{self.Name}' Number={self.Number} Bool={self.Bool}>"


class CheckBoxPs:
    """复选框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, CheckBoxP] = {}
        self._loading_order: List[CheckBoxP] = []

    def add(self, name: str, **kwargs) -> CheckBoxP:
        """添加复选框控件"""
        if name in self._controls:
            raise ValueError(f"复选框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = CheckBoxP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[CheckBoxP]:
        """获取复选框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除复选框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[CheckBoxP]:
        """迭代所有复选框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """复选框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查复选框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[CheckBoxP]:
        """获取按载入次序排序的复选框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 数字框控件实例
class DigitalDisplayP:
    """数字框控件实例"""

    def __init__(self, **kwargs):
        for key, value in DigitalDisplay.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<DigitalDisplayP Name='{self.Name}' Number={self.Number} Min={self.Min} Max={self.Max}>"


class DigitalDisplayPs:
    """数字框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, DigitalDisplayP] = {}
        self._loading_order: List[DigitalDisplayP] = []

    def add(self, name: str, **kwargs) -> DigitalDisplayP:
        """添加数字框控件"""
        if name in self._controls:
            raise ValueError(f"数字框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = DigitalDisplayP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[DigitalDisplayP]:
        """获取数字框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除数字框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[DigitalDisplayP]:
        """迭代所有数字框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """数字框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查数字框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[DigitalDisplayP]:
        """获取按载入次序排序的数字框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 文本框控件实例
class TextBoxP:
    """文本框控件实例"""

    def __init__(self, **kwargs):
        for key, value in TextBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<TextBoxP Name='{self.Name}' Number={self.Number} Text='{self.Text}'>"


class TextBoxPs:
    """文本框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, TextBoxP] = {}
        self._loading_order: List[TextBoxP] = []

    def add(self, name: str, **kwargs) -> TextBoxP:
        """添加文本框控件"""
        if name in self._controls:
            raise ValueError(f"文本框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = TextBoxP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[TextBoxP]:
        """获取文本框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除文本框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[TextBoxP]:
        """迭代所有文本框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """文本框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查文本框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[TextBoxP]:
        """获取按载入次序排序的文本框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 按钮控件实例
class ButtonP:
    """按钮控件实例"""

    def __init__(self, **kwargs):
        for key, value in Button.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<ButtonP Name='{self.Name}' Number={self.Number} Callback={self.Callback is not None}>"


class ButtonPs:
    """按钮控件管理器"""

    def __init__(self):
        self._controls: Dict[str, ButtonP] = {}
        self._loading_order: List[ButtonP] = []

    def add(self, name: str, **kwargs) -> ButtonP:
        """添加按钮控件"""
        if name in self._controls:
            raise ValueError(f"按钮 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = ButtonP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[ButtonP]:
        """获取按钮控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除按钮控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[ButtonP]:
        """迭代所有按钮控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """按钮控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查按钮控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[ButtonP]:
        """获取按载入次序排序的按钮控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 组合框控件实例
class ComboBoxP:
    """组合框控件实例"""

    def __init__(self, **kwargs):
        for key, value in ComboBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<ComboBoxP Name='{self.Name}' Number={self.Number} Text='{self.Text}'>"


class ComboBoxPs:
    """组合框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, ComboBoxP] = {}
        self._loading_order: List[ComboBoxP] = []

    def add(self, name: str, **kwargs) -> ComboBoxP:
        """添加组合框控件"""
        if name in self._controls:
            raise ValueError(f"组合框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = ComboBoxP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[ComboBoxP]:
        """获取组合框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除组合框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[ComboBoxP]:
        """迭代所有组合框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """组合框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查组合框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[ComboBoxP]:
        """获取按载入次序排序的组合框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 路径对话框控件实例
class PathBoxP:
    """路径对话框控件实例"""

    def __init__(self, **kwargs):
        for key, value in PathBox.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        type_name = "未知类型"
        if self.Type == obs.OBS_PATH_FILE:
            type_name = "文件对话框"
        elif self.Type == obs.OBS_PATH_FILE_SAVE:
            type_name = "保存文件对话框"
        elif self.Type == obs.OBS_PATH_DIRECTORY:
            type_name = "文件夹对话框"

        return (f"<PathBoxP Name='{self.Name}' Number={self.Number} "
                f"Type='{type_name}' Text='{self.Text}'>")


class PathBoxPs:
    """路径对话框控件管理器"""

    def __init__(self):
        self._controls: Dict[str, PathBoxP] = {}
        self._loading_order: List[PathBoxP] = []

    def add(self, name: str, **kwargs) -> PathBoxP:
        """添加路径对话框控件"""
        if name in self._controls:
            raise ValueError(f"路径对话框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        control = PathBoxP(**kwargs)
        self._controls[name] = control
        self._loading_order.append(control)
        setattr(self, name, control)
        return control

    def get(self, name: str) -> Optional[PathBoxP]:
        """获取路径对话框控件"""
        return self._controls.get(name)

    def remove(self, name: str) -> bool:
        """移除路径对话框控件"""
        if name in self._controls:
            control = self._controls.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if control in self._loading_order:
                self._loading_order.remove(control)
            return True
        return False

    def __iter__(self) -> Iterator[PathBoxP]:
        """迭代所有路径对话框控件"""
        return iter(self._controls.values())

    def __len__(self) -> int:
        """路径对话框控件数量"""
        return len(self._controls)

    def __contains__(self, name: str) -> bool:
        """检查路径对话框控件是否存在"""
        return name in self._controls

    def get_loading_order(self) -> List[PathBoxP]:
        """获取按载入次序排序的路径对话框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 分组框控件实例
class GroupP:
    """分组框控件实例（独立控件）"""

    def __init__(self, **kwargs):
        for key, value in Group.items():
            setattr(self, key, value)
        # 更新传入的自定义属性
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<GroupP Name='{self.Name}' Number={self.Number}>"


class GroupPs:
    """分组框控件管理器"""

    def __init__(self):
        self._groups: Dict[str, GroupP] = {}
        self._loading_order: List[GroupP] = []

    def add(self, name: str, **kwargs) -> GroupP:
        """添加分组框控件"""
        if name in self._groups:
            raise ValueError(f"分组框 '{name}' 已存在")
        # 确保Name属性设置正确
        if "Name" not in kwargs:
            kwargs["Name"] = name
        group = GroupP(**kwargs)
        self._groups[name] = group
        self._loading_order.append(group)
        setattr(self, name, group)
        return group

    def get(self, name: str) -> Optional[GroupP]:
        """获取分组框控件"""
        return self._groups.get(name)

    def remove(self, name: str) -> bool:
        """移除分组框控件"""
        if name in self._groups:
            group = self._groups.pop(name)
            if hasattr(self, name):
                delattr(self, name)
            if group in self._loading_order:
                self._loading_order.remove(group)
            return True
        return False

    def __iter__(self) -> Iterator[GroupP]:
        """迭代所有分组框控件"""
        return iter(self._groups.values())

    def __len__(self) -> int:
        """分组框控件数量"""
        return len(self._groups)

    def __contains__(self, name: str) -> bool:
        """检查分组框控件是否存在"""
        return name in self._groups

    def get_loading_order(self) -> List[GroupP]:
        """获取按载入次序排序的分组框控件列表"""
        return sorted(self._loading_order, key=lambda c: c.Number)


# 表单管理器
class Widget:
    """表单管理器，管理所有控件"""

    def __init__(self):
        """初始化表单管理器"""
        self.CheckBox = CheckBoxPs()
        self.DigitalDisplay = DigitalDisplayPs()
        self.TextBox = TextBoxPs()
        self.Button = ButtonPs()
        self.ComboBox = ComboBoxPs()
        self.PathBox = PathBoxPs()
        self.Group = GroupPs()
        self._all_controls: List[Any] = []
        self._loading_dict: Dict[int, Any] = {}

    def _update_all_controls(self):
        """更新所有控件列表"""
        self._all_controls = []
        # 收集所有类型的控件
        self._all_controls.extend(self.CheckBox)
        self._all_controls.extend(self.DigitalDisplay)
        self._all_controls.extend(self.TextBox)
        self._all_controls.extend(self.Button)
        self._all_controls.extend(self.ComboBox)
        self._all_controls.extend(self.PathBox)
        self._all_controls.extend(self.Group)

    def loading(self):
        """按载入次序排序所有控件"""
        self._update_all_controls()
        # 按Number属性排序
        sorted_controls = sorted(self._all_controls, key=lambda c: c.Number)
        name_dict = {}  # 用于检测名称冲突

        # 创建载入次序字典
        self._loading_dict = {}
        for control in sorted_controls:
            # 检查名称冲突
            if control.Name in name_dict:
                existing_control = name_dict[control.Name]
                raise ValueError(
                    f"控件名称冲突: 控件 '{control.Name}' "
                    f"(类型: {type(control).__name__}, 载入次序: {control.Number}) 与 "
                    f"'{existing_control.Name}' "
                    f"(类型: {type(existing_control).__name__}, 载入次序: {existing_control.Number}) 重名"
                )
            else:
                name_dict[control.Name] = control
            if control.Number in self._loading_dict:
                existing_control = self._loading_dict[control.Number]
                raise ValueError(
                    f"载入次序冲突: 控件 '{control.Name}' (类型: {type(control).__name__}) 和 "
                    f"'{existing_control.Name}' (类型: {type(existing_control).__name__}) "
                    f"使用相同的Number值 {control.Number}"
                )
            self._loading_dict[control.Number] = control

    def get_control_by_number(self, number: int) -> Optional[Any]:
        """通过载入次序获取控件"""
        self.loading()  # 确保已排序
        return self._loading_dict.get(number)

    def get_control_by_name(self, name: str) -> Optional[Any]:
        """通过名称获取控件"""
        # 在顶级控件中查找
        for manager in [self.CheckBox, self.DigitalDisplay, self.TextBox,
                        self.Button, self.ComboBox, self.PathBox, self.Group]:
            if name in manager:
                return manager.get(name)
        return None

    def get_sorted_controls(self) -> List[Any]:
        """获取按载入次序排序的所有控件列表"""
        self.loading()
        return list(self._loading_dict.values())

    def clean(self):
        """清除所有控件并重置表单"""
        # 重置所有控件管理器
        self.CheckBox = CheckBoxPs()
        self.DigitalDisplay = DigitalDisplayPs()
        self.TextBox = TextBoxPs()
        self.Button = ButtonPs()
        self.ComboBox = ComboBoxPs()
        self.PathBox = PathBoxPs()
        self.Group = GroupPs()

        # 清空内部存储
        self._all_controls = []
        self._loading_dict = {}

        return self  # 支持链式调用

    def __repr__(self) -> str:
        """返回表单的可读表示形式"""
        self._update_all_controls()
        return f"<Widget controls={len(self._all_controls)}>"

# 创建控件表单
widget = Widget()

widget_Button_name_list = {
    "props": {
        "top", "bottom",
    },
    "account_props": {
        "login", "accountListUpdate", "qrAddAccount", "qrPictureDisplay", "accountDelete", "accountBackup",
        "accountRestore", "logout",
    },
    "room_props": {
        "roomOpened", "roomCoverView", "roomCoverUpdate", "roomCommonTitlesTrue", "roomTitleChange","roomNewsChange",
        "roomCommonAreasTrue", "roomParentAreaTrue", "roomSubAreaTrue", "bliveWebJump",
    },
    "live_props": {
        "liveFaceAuth", "liveStart", "liveRtmpAddressCopy", "liveRtmpCodeCopy", "liveRtmpCodeUpdate", "liveStop",
        "liveBookingsDayTrue", "liveBookingsHourTrue", "liveBookingsMinuteTrue", "liveBookingsCreate",
        "liveBookingsCancel",},
}

widget_Group_name_list = {
    "props": {
        "account": "account_props",
        "room": "room_props",
        "live": "live_props",
    },
}

widget_TextBox_name_list = {
    "account_props": {
        "loginStatus",
    },
    "room_props": {
        "roomStatus", "roomTitle", "roomNews",
    },
    "live_props": {
        "liveBookingsTitle",
    },
}

widget_ComboBox_name_list = {
    "account_props": {
        "uid",
    },
    "room_props": {
        "roomCommonTitles", "roomCommonAreas", "roomParentArea", "roomSubArea",
    },
    "live_props": {
        "liveStreamingPlatform", "liveBookings",
    },
}

widget_PathBox_name_list = {
    "room_props": {
        "roomCover",
    },
}

widget_DigitalDisplay_name_list = {
    "live_props": {
        "liveBookingsDay", "liveBookingsHour", "liveBookingsMinute",
    },
}

widget_CheckBox_name_list = {
    "live_props": {
        "liveBookingsDynamic",
    },
}

for P in widget_Button_name_list:
    for Button_name in widget_Button_name_list[P]:
        widget.Button.add(Button_name)
        obj = getattr(widget.Button, Button_name)
        obj.Props = P

for P in widget_Group_name_list:
    for Group_name in widget_Group_name_list[P]:
        widget.Group.add(Group_name)
        obj = getattr(widget.Group, Group_name)
        obj.Props = P
        obj.GroupProps = widget_Group_name_list[P][Group_name]

for P in widget_TextBox_name_list:
    for TextBox_name in widget_TextBox_name_list[P]:
        widget.TextBox.add(TextBox_name)
        obj = getattr(widget.TextBox, TextBox_name)
        obj.Props = P

for P in widget_ComboBox_name_list:
    for ComboBox_name in widget_ComboBox_name_list[P]:
        widget.ComboBox.add(ComboBox_name)
        obj = getattr(widget.ComboBox, ComboBox_name)
        obj.Props = P

for P in widget_PathBox_name_list:
    for PathBox_name in widget_PathBox_name_list[P]:
        widget.PathBox.add(PathBox_name)
        obj = getattr(widget.PathBox, PathBox_name)
        obj.Props = P

for P in widget_DigitalDisplay_name_list:
    for DigitalDisplay_name in widget_DigitalDisplay_name_list[P]:
        widget.DigitalDisplay.add(DigitalDisplay_name)
        obj = getattr(widget.DigitalDisplay, DigitalDisplay_name)
        obj.Props = P

for P in widget_CheckBox_name_list:
    for CheckBox_name in widget_CheckBox_name_list[P]:
        widget.CheckBox.add(CheckBox_name)
        obj = getattr(widget.CheckBox, CheckBox_name)
        obj.Props = P

# 全局变量
textBox_type_name4textBox_type = {
    obs.OBS_TEXT_INFO_NORMAL: '正常信息',
    obs.OBS_TEXT_INFO_WARNING: '警告信息',
    obs.OBS_TEXT_INFO_ERROR: '错误信息'
}
"""
只读文本框的消息类型字典\n
- obs.OBS_TEXT_INFO_NORMAL：'正常信息', 
- obs.OBS_TEXT_INFO_WARNING：'警告信息', 
- obs.OBS_TEXT_INFO_ERROR：'错误信息'
"""

information4login_qr_return_code = {
    0: "登录成功",
    86101: "未扫码",
    86090: "二维码已扫码未确认",
    86038: "二维码已失效",
}
"""
登陆二维码被调用后轮询函数返回值对应的含义\n
- 0: "登录成功",
- 86101: "未扫码",
- 86090: "二维码已扫码未确认",
- 86038: "二维码已失效",
"""

information4frontend_event = {
    # 推流相关事件
    obs.OBS_FRONTEND_EVENT_STREAMING_STARTING: "推流正在启动",
    obs.OBS_FRONTEND_EVENT_STREAMING_STARTED: "推流已开始",
    obs.OBS_FRONTEND_EVENT_STREAMING_STOPPING: "推流正在停止",
    obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED: "推流已停止",

    # 录制相关事件
    obs.OBS_FRONTEND_EVENT_RECORDING_STARTING: "录制正在启动",
    obs.OBS_FRONTEND_EVENT_RECORDING_STARTED: "录制已开始",
    obs.OBS_FRONTEND_EVENT_RECORDING_STOPPING: "录制正在停止",
    obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED: "录制已停止",
    obs.OBS_FRONTEND_EVENT_RECORDING_PAUSED: "录制已暂停",
    obs.OBS_FRONTEND_EVENT_RECORDING_UNPAUSED: "录制已恢复",

    # 回放缓存相关事件
    obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTING: "回放缓存正在启动",
    obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED: "回放缓存已开始",
    obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPING: "回放缓存正在停止",
    obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED: "回放缓存已停止",
    obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED: "回放已保存",

    # 场景相关事件
    obs.OBS_FRONTEND_EVENT_SCENE_CHANGED: "当前场景已改变",
    obs.OBS_FRONTEND_EVENT_PREVIEW_SCENE_CHANGED: "预览场景已改变",
    obs.OBS_FRONTEND_EVENT_SCENE_LIST_CHANGED: "场景列表已改变",

    # 转场相关事件
    obs.OBS_FRONTEND_EVENT_TRANSITION_CHANGED: "转场效果已改变",
    obs.OBS_FRONTEND_EVENT_TRANSITION_STOPPED: "转场效果已停止",
    obs.OBS_FRONTEND_EVENT_TRANSITION_LIST_CHANGED: "转场列表已改变",
    obs.OBS_FRONTEND_EVENT_TRANSITION_DURATION_CHANGED: "转场持续时间已更改",

    # 配置文件相关事件
    obs.OBS_FRONTEND_EVENT_PROFILE_CHANGING: "配置文件即将切换",
    obs.OBS_FRONTEND_EVENT_PROFILE_CHANGED: "配置文件已切换",
    obs.OBS_FRONTEND_EVENT_PROFILE_LIST_CHANGED: "配置文件列表已改变",
    obs.OBS_FRONTEND_EVENT_PROFILE_RENAMED: "配置文件已重命名",

    # 场景集合相关事件
    obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGING: "场景集合即将切换",
    obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED: "场景集合已切换",
    obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_LIST_CHANGED: "场景集合列表已改变",
    obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_RENAMED: "场景集合已重命名",
    obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CLEANUP: "场景集合清理完成",

    # 工作室模式事件
    obs.OBS_FRONTEND_EVENT_STUDIO_MODE_ENABLED: "工作室模式已启用",
    obs.OBS_FRONTEND_EVENT_STUDIO_MODE_DISABLED: "工作室模式已禁用",

    # 系统级事件
    obs.OBS_FRONTEND_EVENT_EXIT: "OBS 即将退出",
    obs.OBS_FRONTEND_EVENT_FINISHED_LOADING: "OBS 完成加载",
    obs.OBS_FRONTEND_EVENT_SCRIPTING_SHUTDOWN: "脚本关闭中",

    # 虚拟摄像头事件
    obs.OBS_FRONTEND_EVENT_VIRTUALCAM_STARTED: "虚拟摄像头已启动",
    obs.OBS_FRONTEND_EVENT_VIRTUALCAM_STOPPED: "虚拟摄像头已停止",

    # 控制条事件
    obs.OBS_FRONTEND_EVENT_TBAR_VALUE_CHANGED: "转场控制条(T-Bar)值已改变",

    # OBS 28+ 新增事件
    obs.OBS_FRONTEND_EVENT_SCREENSHOT_TAKEN: "截图已完成",
    obs.OBS_FRONTEND_EVENT_THEME_CHANGED: "主题已更改"
}
"""obs前台事件文本"""


class GlobalVariableOfData:
    widget_loading_number = 0
    """控件加载顺序"""
    isScript_propertiesIs = False  # Script_properties()被调用
    """Script_properties()被调用"""
    streaming_active = None  # OBS推流状态
    """OBS推流状态"""
    script_settings = None  # #脚本的所有设定属性集
    """脚本的所有设定属性集"""

    logRecording = ""  # #日志记录的文本
    """日志记录的文本"""
    networkConnectionStatus = False  # #网络连接状态
    """网络连接状态"""
    sslVerification = True
    """SSL验证"""
    # 文件配置类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    scriptsDataDirpath = None  # #脚本所在目录，末尾带/
    """脚本所在目录，末尾带/"""
    scriptsUsersConfigFilepath = None  # #用户配置文件路径
    """用户配置文件路径"""
    scriptsTempDir = None   # #临时文件文件夹
    """临时文件文件夹"""
    scriptsLogDir = None  # #日志文件文件夹
    """日志文件文件夹"""
    scriptsCacheDir = None  # #缓存文件文件夹
    """缓存文件文件夹"""

    # 用户类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    loginQrCode_key = None  # ##登陆二维码密钥
    """登陆二维码密钥"""
    loginQrCodeReturn = None  # ##登陆二维码返回数据
    """登陆二维码返回数据"""
    loginQRCodePillowImg = None  # ##登录二维码的pillow_img实例
    """登录二维码的pillow_img实例"""


def script_path():
    """
    用于获取脚本所在文件夹的路径，这其实是一个obs插件内置函数，
    只在obs插件指定的函数内部使用有效,
    这里构建这个函数是没必要的，写在这里只是为了避免IDE出现error提示
    Example:
        假如脚本路径在 "/Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/bilibili_live.py"
        >>> print(script_path())
        /Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/
        >>> print(Path(f'{script_path()}bilibili-live') / "config.json")
        /Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/bilibili-live/config.json
    """
    pass


def log_save(log_level: Literal[0, 1, 2, 3], log_str: str, print_is:bool = True) -> None:
    """
    输出并保存日志
    Args:
        print_is: 是否输出
        log_level: 日志等级

            0: "INFO",
            1: "DEBUG",
            2: "WARNING",
            3: "ERROR",
        log_str: 日志内容
    Returns: None
    """
    log_type = {
        0: obs.LOG_INFO,
        1: obs.LOG_DEBUG,
        2: obs.LOG_WARNING,
        3: obs.LOG_ERROR,
    }
    log_type_str = {
        0: "INFO",
        1: "DEBUG",
        2: "WARNING",
        3: "ERROR",
    }
    now = datetime.now()
    formatted = now.strftime("%Y/%m/%d %H:%M:%S")
    log_text = f"【{formatted}】【{log_type_str[log_level]}】{log_str}"
    if print_is:
        obs.script_log(log_type[log_level], log_text)
    GlobalVariableOfData.logRecording += log_text + "\n"


# 工具类函数
class BilibiliUserLogsIn2ConfigFile:
    """
    管理B站用户登录配置文件的增删改查操作
    配置文件结构示例：
    {
        "DefaultUser": "12345",
        "12345": {
            "DedeUserID": "12345",
            "SESSDATA": "xxxxx",
            "bili_jct": "xxxxx",
            ...
        }
    }
    """

    def __init__(self, config_path: pathlib.Path):
        """
        初始化配置文件管理器
        Args:
            config_path: 配置文件路径对象
        Raises:
            IOError: 文件读写失败时抛出
            json.JSONDecodeError: 配置文件内容格式错误时抛出
        """
        self.configPath = config_path
        self._ensure_config_file()

    def _ensure_config_file(self):
        """确保配置文件存在且结构有效"""
        if not self.configPath.exists():
            log_save(1, f'脚本数据文件【{GlobalVariableOfData.scriptsDataDirpath}】不存在，尝试创建')
            self.configPath.parent.mkdir(parents=True, exist_ok=True)
            self._write_config({"DefaultUser": None})
            log_save(1, f'success：脚本数据文件 创建成功')

        config = self._read_config()
        if "DefaultUser" not in config:
            log_save(1, f'脚本数据文件中不存在"DefaultUser"字段，尝试创建')
            config["DefaultUser"] = None
            self._write_config(config)
            log_save(1, f'success："DefaultUser"字段 创建成功')

    def _read_config(self) -> Dict:
        """读取配置文件内容"""
        try:
            with open(self.configPath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"配置文件损坏或格式错误: {str(e)}") from e

    def _write_config(self, config: Dict):
        """写入配置文件"""
        try:
            with open(self.configPath, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise RuntimeError(f"配置文件写入失败: {str(e)}") from e

    def add_user(self, cookies: Dict) -> None:
        """
        添加新用户配置
        Args:
            cookies: 包含完整cookie信息的字典，必须包含以下字段：
                     DedeUserID, DedeUserID__ckMd5, SESSDATA,
                     bili_jct, buvid3, b_nut
        Raises:
            ValueError: 缺少必要字段或用户已存在时抛出
        """
        required_keys = {
            "DedeUserID", "DedeUserID__ckMd5", "SESSDATA",
            "bili_jct", "buvid3", "b_nut"
        }
        if not required_keys.issubset(cookies.keys()):
            missing = required_keys - cookies.keys()
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")

        uid = str(cookies["DedeUserID"])
        config = self._read_config()

        if uid in config:
            raise ValueError(f"用户 {uid} 已存在")

        config[uid] = cookies
        self._write_config(config)

    def delete_user(self, uid: int) -> None:
        """
        删除用户配置
        Args:
            uid: 要删除的用户ID
        Raises:
            ValueError: 用户不存在时抛出
        """
        config = self._read_config()
        uid_str = str(uid)

        if uid_str not in config:
            raise ValueError(f"用户 {uid} 不存在")

        # 处理默认用户
        if config["DefaultUser"] == uid_str:
            config["DefaultUser"] = None

        del config[uid_str]
        self._write_config(config)

    def update_user(self, cookies: Optional[dict], set_default_user_is: bool = True) -> None:
        """
        更新用户配置或清空默认用户
        Args:
            cookies: 包含完整cookie信息的字典，传 None 表示清空默认用户
                - 示例: {"DedeUserID": "123", "SESSDATA": "xxx"...}
                - 传 None 时需配合 set_default_user=True 使用
            set_default_user_is: 是否设为默认用户
                - 当 cookies=None 时必须为 True
        Raises:
            ValueError: 以下情况时抛出
                - cookies 不完整或用户不存在
                - cookies=None 但 set_default_user=False
        """
        config = self._read_config()

        # 处理清空默认用户场景
        if cookies is None:
            if not set_default_user_is:
                raise ValueError("传入cookies=None 时必须设置 set_default_user=True")
            config["DefaultUser"] = None
            self._write_config(config)
            return

        # 原始验证逻辑
        required_keys = {"DedeUserID", "SESSDATA", "bili_jct"}
        if not required_keys.issubset(cookies.keys()):
            missing = required_keys - cookies.keys()
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")

        uid = str(cookies["DedeUserID"])
        if uid not in config:
            raise ValueError(f"用户 {uid} 不存在")

        # 更新用户数据
        config[uid].update(cookies)

        # 设置默认用户
        if set_default_user_is:
            config["DefaultUser"] = uid

        self._write_config(config)

    def get_cookies(self, uid: Optional[int] = None) -> Optional[dict]:
        """
        获取指定用户的cookie信息
        Args:
            uid: 用户ID，None表示获取默认用户
        Returns:
            用户cookie字典，未找到返回None
        """
        config = self._read_config()
        # 如果uid是None表示获取默认用户
        if uid is None:
            uid = config.get("DefaultUser")
        # 如果默认用户是None输出None
        if uid is None:
            return None

        uid_str = str(uid)
        return config.get(uid_str)

    def get_users(self) -> Dict[int, Optional[str]]:
        """
        获取所有用户列表（包含默认用户占位）
        Returns:
            Dict[int, Optional[str]]
            - 键 0: 默认用户ID（若未设置则为 None）
            - 键 1~N: 其他用户ID（按插入顺序编号）
        """
        config = self._read_config()
        # 获取所有用户ID（排除系统字段）
        user_ids = [
            uid for uid in config.keys()
            if uid not in {"DefaultUser", "0"}  # 过滤系统保留字段
            and uid.isdigit()  # 确保是数字型用户ID
        ]
        # 构建字典（强制包含 0: None）
        users = {
            0: config.get("DefaultUser")  # 允许 None
        }
        # 添加其他用户（过滤掉默认用户避免重复）
        default_uid = config.get("DefaultUser")
        if default_uid and default_uid in user_ids:
            user_ids.remove(default_uid)  # 避免重复
        for idx, uid in enumerate(user_ids, start=1):
            users[idx] = uid
        return users


class CommonTitlesManager:
    """
    管理用户常用标题的JSON文件

    功能:
    - 管理 {user_id: [title1, title2, ...]} 格式的JSON文件
    - 每个用户的标题列表最多包含5个元素
    - 支持增删改查操作
    - 自动创建不存在的目录和文件

    参数:
        directory: 文件存放目录
    """

    def __init__(self, directory: Union[str, Path]):
        """
        初始化CommonTitlesManager

        Args:
            directory: 文件存放目录
        """
        self.directory = Path(directory)
        self.filepath = self.directory / "commonData.json"
        self.data: Dict[str, List[str]] = {}

        # 确保目录存在
        self.directory.mkdir(parents=True, exist_ok=True)

        # 如果文件不存在则创建
        if not self.filepath.exists():
            self._save_data()
        else:
            self._load_data()

    def _load_data(self) -> None:
        """从文件加载数据"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # 文件为空或格式错误时创建新文件
            self.data = {}
            self._save_data()

    def _save_data(self) -> None:
        """保存数据到文件"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_titles(self, user_id: str) -> List[str]:
        """
        获取指定用户的常用标题列表

        Args:
            user_id: 用户ID

        Returns:
            该用户的常用标题列表（如果没有则为空列表）
        """
        return self.data.get(user_id, [])

    def add_title(self, user_id: str, title: str) -> None:
        """
        为用户添加新标题

        特点:
        - 如果标题已存在，则移动到列表最前面
        - 确保列表长度不超过5个
        - 如果用户不存在，则创建新条目

        Args:
            user_id: 用户ID
            title: 要添加的标题
        """
        titles = self.get_titles(user_id)

        # 移除重复项（如果存在）
        if title in titles:
            titles.remove(title)

        # 添加到列表开头
        titles.insert(0, title)

        # 确保不超过5个元素
        if len(titles) > 5:
            titles = titles[:5]

        # 更新数据并保存
        self.data[user_id] = titles
        self._save_data()

    def remove_title(self, user_id: str, title: str) -> bool:
        """
        移除用户的指定标题

        Args:
            user_id: 用户ID
            title: 要移除的标题

        Returns:
            True: 成功移除
            False: 标题不存在
        """
        if user_id not in self.data:
            return False

        titles = self.data[user_id]

        if title in titles:
            titles.remove(title)
            # 如果列表为空，则删除用户条目
            if not titles:
                del self.data[user_id]
            self._save_data()
            return True
        return False

    def update_title(self, user_id: str, old_title: str, new_title: str) -> bool:
        """
        更新用户的标题

        Args:
            user_id: 用户ID
            old_title: 要替换的旧标题
            new_title: 新标题

        Returns:
            True: 更新成功
            False: 旧标题不存在
        """
        if user_id not in self.data:
            return False

        titles = self.data[user_id]

        if old_title in titles:
            # 替换标题并移动到列表前面
            index = titles.index(old_title)
            titles.pop(index)
            titles.insert(0, new_title)
            self._save_data()
            return True
        return False

    def clear_user_titles(self, user_id: str) -> None:
        """
        清除指定用户的所有标题

        Args:
            user_id: 用户ID
        """
        if user_id in self.data:
            del self.data[user_id]
            self._save_data()

    def get_all_users(self) -> List[str]:
        """
        获取所有有标题的用户ID列表

        Returns:
            用户ID列表
        """
        return list(self.data.keys())

    def get_all_data(self) -> Dict[str, List[str]]:
        """
        获取所有数据

        Returns:
            完整的{user_id: titles}字典
        """
        return self.data.copy()

    def __str__(self) -> str:
        """返回数据的字符串表示"""
        return json.dumps(self.data, ensure_ascii=False, indent=2)


def check_network_connection():
    """检查网络连接，通过多个服务提供者的链接验证"""
    log_save(0, "======= 开始网络连接检查 =======")

    # 1. 首先尝试快速DNS连接检查
    log_save(0, "[步骤1] 尝试通过DNS连接检查网络 (8.8.8.8:53)...")
    try:
        start_time = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        elapsed = (time.time() - start_time) * 1000
        log_save(0, f"🧩  DNS连接成功! 耗时: {elapsed:.2f}ms")
        return True
    except OSError as e:
        log_save(1, f"⚠️ DNS连接失败: {str(e)}")

    # 2. 尝试多个服务提供者的链接
    log_save(0, "\n[步骤2] 开始尝试多个服务提供者的连接...")

    # 定义测试URL及其提供商
    test_services = [
        {"url": "http://www.gstatic.com/generate_204", "provider": "Google"},
        {"url": "http://www.google-analytics.com/generate_204", "provider": "Google"},
        {"url": "http://connectivitycheck.gstatic.com/generate_204", "provider": "Google"},
        {"url": "http://captive.apple.com", "provider": "Apple"},
        {"url": "http://www.msftconnecttest.com/connecttest.txt", "provider": "Microsoft"},
        {"url": "http://cp.cloudflare.com/", "provider": "Cloudflare"},
        {"url": "http://detectportal.firefox.com/success.txt", "provider": "Firefox"},
        {"url": "http://www.v2ex.com/generate_204", "provider": "V2ex"},
        {"url": "http://connect.rom.miui.com/generate_204", "provider": "小米"},
        {"url": "http://connectivitycheck.platform.hicloud.com/generate_204", "provider": "华为"},
        {"url": "http://wifi.vivo.com.cn/generate_204", "provider": "Vivo"}
    ]

    for service in test_services:
        url = service["url"]
        provider = service["provider"]
        log_save(0, f"\n- 尝试 {provider} 服务: {url}")

        try:
            # 发送HEAD请求减少数据传输量
            start_time = time.time()
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as response:
                elapsed = (time.time() - start_time) * 1000

                # 检查响应状态
                if response.status < 500:  # 排除服务器错误
                    log_save(0, f"  🧩  连接成功! 状态码: {response.status} | 耗时: {elapsed:.2f}ms")
                    return True
                else:
                    log_save(1, f"  ⚠️ 服务器错误: 状态码 {response.status}")
        except TimeoutError:
            log_save(1, "  ⏱️ 连接超时 (3秒)")
        except ConnectionError:
            log_save(1, "  🔌 连接错误 (网络问题)")
        except URLError as e:
            log_save(1, f"  ❌ URL错误: {str(e.reason)}")
        except Exception as e:
            log_save(1, f"  ⚠️ 未知错误: {str(e)}")

    # 3. 最后尝试基本HTTP连接
    log_save(1, "\n[步骤3] 尝试基本HTTP连接检查 (http://example.com)...")
    try:
        start_time = time.time()
        urllib.request.urlopen("http://example.com", timeout=3)
        elapsed = (time.time() - start_time) * 1000
        log_save(0, f"🧩  HTTP连接成功! 耗时: {elapsed:.2f}ms")
        return True
    except URLError as e:
        log_save(3, f"❌ 所有连接尝试失败: {str(e)}")
        return False


def check_ssl_verification(test_url="https://api.bilibili.com", timeout=5):
    """
    检测 SSL 证书验证是否可用

    参数:
    test_url (str): 用于测试的 URL（默认为 Bilibili API）
    timeout (int): 测试请求的超时时间（秒）

    返回:
    tuple: (verify_ssl: bool, warning: str)
        verify_ssl: 是否启用 SSL 验证
        warning: 警告信息（如果存在问题）
    """
    # 默认启用 SSL 验证
    verify_ssl = True
    warning = "✅ "

    try:
        # 尝试使用 SSL 验证进行请求
        response = requests.head(
            test_url,
            timeout=timeout,
            verify=True  # 强制启用验证
        )

        # 检查响应状态
        if response.status_code >= 400:
            warning = f"❌ 测试请求返回错误状态: {response.status_code}"

    except SSLError as e:
        # 捕获 SSL 验证错误
        verify_ssl = False
        warning = f"❌ SSL 验证失败: {e}】已禁用 SSL 证书验证（可能存在安全风险）"

        # 禁用 SSL 验证警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    except requests.exceptions.RequestException as e:
        # 其他网络错误
        verify_ssl = False
        warning = f"❌ 网络请求错误: {e}】已禁用 SSL 证书验证（可能存在安全风险）"

    except Exception as e:
        # 其他未知错误
        verify_ssl = False
        warning = f"❌ 未知错误: {e}】已禁用 SSL 证书验证（可能存在安全风险）"

    # 如果验证失败，配置全局 SSL 上下文
    if not verify_ssl:
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except Exception as e:
            warning += f"】配置全局 SSL 上下文失败: {e}"

    return verify_ssl, warning


def get_future_timestamp(days=0, hours=0, minutes=0):
    """
    获取当前时间加上指定天数、小时、分钟后的10位Unix时间戳

    参数:
    days (int): 要添加的天数
    hours (int): 要添加的小时数
    minutes (int): 要添加的分钟数

    返回:
    int: 10位Unix时间戳（秒级）
    """
    # 获取当前时间（本地时区）
    current_time = datetime.now()

    # 创建时间增量（x天y小时z分钟）
    time_delta = timedelta(
        days=days,
        hours=hours,
        minutes=minutes
    )

    # 计算未来时间
    future_time = current_time + time_delta

    # 转换为Unix时间戳（10位整数）
    timestamp = int(future_time.timestamp())

    return timestamp


def url2pillow_image(url, ssl_verification: bool = True) -> Optional[ImageFile]:
    """
    将url图片转换为pillow_image实例
    Args:
        url:
    Returns:
        pillow_image实例
    """
    try:
        # 添加请求头模拟浏览器访问，避免被拒绝
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # 发送 GET 请求
        response = requests.get(verify=ssl_verification, url = url, headers=headers, stream=True)
        response.raise_for_status()  # 检查 HTTP 错误
        # 将响应内容转为字节流
        image_data = io.BytesIO(response.content)
        # 用 Pillow 打开图像
        img = Image.open(image_data)
        return img
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"处理图像时出错: {e}")


def dict2cookie(jsondict: Dict[str, Union[str, int, float, bool]], safe: str = "/:") -> str:
    """
    将字典转换为符合HTTP标准的Cookie字符串格式
    Args:
        jsondict: 包含Cookie键值对的字典
            - 示例: {"name": "value", "age": 20, "secure": True}
        safe: URL编码中保留的安全字符（默认保留/和:）
    Returns:
        str: 符合Cookie规范的字符串
            - 示例: "name=value; age=20; secure"
    Raises:
        TypeError: 当输入不是字典时抛出
    """
    if not isinstance(jsondict, dict):
        raise TypeError("输入必须是字典类型")

    cookie_parts = []

    for key, value in jsondict.items():
        # 处理键
        encoded_key = quote(str(key), safe=safe, encoding='utf-8')

        # 处理不同类型的值
        if value is True:
            # 布尔值True表示为标志属性
            cookie_parts.append(encoded_key)
        elif value is False or value is None:
            # 跳过False和None值
            continue
        else:
            # 其他类型转换为字符串并编码
            str_value = str(value)
            encoded_value = quote(str_value, safe=safe, encoding='utf-8')
            cookie_parts.append(f"{encoded_key}={encoded_value}")

    return "; ".join(cookie_parts)


def cookie2dict(cookie: str) -> Dict[str, str]:
    """
    将符合HTTP标准的Cookie字符串转换为字典
    Args:
        cookie: Cookie字符串
            示例: "name=value; age=20; token=abc%20123"
    Returns:
        解析后的字典，键值均为字符串类型
        示例: {'name': 'value', 'age': '20', 'token': 'abc 123'}
    Raises:
        TypeError: 当输入不是字符串时抛出
    Features:
        - 自动处理URL解码
        - 兼容不同分隔符（; 或 ; ）
        - 过滤空键和空值条目
        - 保留重复键的最后出现值（符合HTTP规范）
        - 处理值中的等号
        - 更健壮的解码错误处理
    """
    if not isinstance(cookie, str):
        raise TypeError("输入必须是字符串类型")

    cookie_dict = {}
    # 处理空字符串
    if not cookie.strip():
        return cookie_dict

    # 分割Cookie字符串
    for pair in cookie.split(';'):
        pair = pair.strip()
        if not pair:
            continue

        # 仅分割第一个等号，正确处理含等号的值
        parts = pair.split('=', 1)
        if len(parts) != 2:
            continue  # 跳过无效条目

        key, value = parts
        key = key.strip()
        if not key:  # 过滤空键
            continue

        # 值处理：去除首尾空格
        value = value.strip()

        # 处理带引号的值 (如: "value")
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        # 执行URL解码
        try:
            decoded_value = urllib.parse.unquote(value)
        except Exception:
            decoded_value = value  # 解码失败保留原始值

        # 过滤空值（空字符串）
        if decoded_value == "":
            continue

        cookie_dict[key] = decoded_value

    return cookie_dict


def utf_8_to_url(text: str, safe: str = "/:") -> str:
    """
    将字符串编码为 URL 安全的 UTF-8 格式

    改进点:
    1. 添加安全字符参数
    2. 更清晰的函数名
    3. 更好的错误处理

    @param string: 要编码的字符串
    @param safe: 编码中保留的安全字符（默认保留/和:）
    @return: URL编码的字符串
    """
    try:
        return quote(text, safe=safe, encoding='utf-8')
    except Exception:
        # 编码失败时返回原始字符串
        return text


def url2dict(url: str, decode: bool = True, handle_multiple: bool = True) -> Dict[str, Union[str, int, float, bool, None, List[Any]]]:
    """
    将 URL 参数解析为字典，支持复杂参数处理

    功能特点：
    1. 自动处理 URL 编码参数
    2. 支持多值参数（保留所有值）
    3. 处理空值和缺失值
    4. 支持 URL 片段(#)和完整 URL
    5. 自动类型转换尝试
    6. 查询参数优先级高于片段参数

    Args:
        url: 包含查询参数的 URL 字符串
        decode: 是否自动 URL 解码参数值（默认 True）
        handle_multiple: 是否保留多值参数的所有值（默认 True）

    Returns:
        解析后的参数字典，单值参数为基本类型，多值参数为列表

    Examples:
        >>> url2dict("https://example.com?name=John&age=30&lang=Python&lang=Java")
        {'name': 'John', 'age': 30, 'lang': ['Python', 'Java']}

        >>> url2dict("search?q=hello%20world&safe=on&price=")
        {'q': 'hello world', 'safe': True, 'price': None}
    """

    # 内部辅助函数
    def _convert_types(value: str) -> Union[str, int, float, bool, None]:
        """尝试将字符串值转换为合适的类型（修复类型转换顺序）"""
        if value == '':
            return None

        # 先尝试数字转换（避免数字被误转为布尔值）
        if value.isdigit():
            try:
                return int(value)
            except (ValueError, TypeError):
                pass

        if '.' in value or 'e' in value.lower():
            try:
                return float(value)
            except (ValueError, TypeError):
                pass

        if value.endswith('%') and value[:-1].replace('.', '', 1).isdigit():
            try:
                return float(value[:-1]) / 100.0
            except (ValueError, TypeError):
                pass

        # 最后尝试布尔值
        if value.lower() in {'true', 'yes', 'on', '1'}:
            return True
        if value.lower() in {'false', 'no', 'off', '0'}:
            return False

        return value

    def _fallback_parse(query_str: str) -> Dict[str, Any]:
        """手动解析回退方案"""
        result = {}
        if not query_str:
            return result

        pairs = [p for p in query_str.split('&') if p]

        for pair in pairs:
            parts = pair.split('=', 1)
            key = parts[0]
            value = parts[1] if len(parts) > 1 else ''

            key = unquote(key) if decode else key
            value_str = unquote(value) if decode else value
            converted_value = _convert_types(value_str)

            if handle_multiple and key in result:
                existing = result[key]
                if isinstance(existing, list):
                    existing.append(converted_value)
                else:
                    result[key] = [existing, converted_value]
            else:
                result[key] = converted_value

        return result

    def _parse_query_string(query_str: str) -> Dict[str, Any]:
        """解析查询字符串为字典"""
        if not query_str:
            return {}

        try:
            params_dict = parse_qs(query_str, keep_blank_values=True)
        except Exception:
            return _fallback_parse(query_str)

        result = {}
        for key, values in params_dict.items():
            clean_key = unquote(key) if decode else key

            if handle_multiple and len(values) > 1:
                converted_values = [_convert_types(unquote(v) if decode else v) for v in values]
                result[clean_key] = converted_values
            else:
                value = values[0] if values else ''
                clean_value = unquote(value) if decode else value
                result[clean_key] = _convert_types(clean_value)

        return result

    # 主函数逻辑开始
    if not url or not isinstance(url, str):
        return {}

    parsed = urlparse(url)
    query_str = parsed.query
    fragment_str = parsed.fragment

    # 处理片段中的参数
    frag_query_str = None
    if fragment_str:
        if '?' in fragment_str:
            _, frag_query = fragment_str.split('?', 1)
            frag_query_str = frag_query
        elif '=' in fragment_str:
            frag_query_str = fragment_str

    # 分别解析查询参数和片段参数
    query_dict = _parse_query_string(query_str)
    frag_dict = _parse_query_string(frag_query_str) if frag_query_str else {}

    # 合并参数：查询参数优先于片段参数
    result = {}
    result.update(frag_dict)
    result.update(query_dict)

    return result


def qr_text8pil_img(
        qr_str: str,
        border: int = 2,
        error_correction: Literal[0, 1, 2, 3] = qrcode.constants.ERROR_CORRECT_L,
        invert: bool = False
) -> Dict[str, Union[str, Image.Image]]:
    """
    字符串转二维码（返回包含 PIL 图像对象的字典）
    Args:
        qr_str: 二维码文本（必须是有效的非空字符串）
        border: 边框大小（必须是非负整数，默认2）
        error_correction: 纠错级别（默认L）
            - ERROR_CORRECT_L: 1
            - ERROR_CORRECT_M: 0
            - ERROR_CORRECT_Q: 3
            - ERROR_CORRECT_H: 2
        invert: 是否反转颜色（默认False）
    Returns:
        Dict: 包含以下键的字典
            - str: ASCII 字符串形式的二维码
            - img: PIL.Image 对象（二维码图像）
    Raises:
        ValueError: 输入参数不合法时抛出
    """
    # 验证输入参数
    if not isinstance(qr_str, str) or not qr_str:
        raise ValueError("qr_str 必须是有效的非空字符串")
    if not isinstance(border, int) or border < 0:
        raise ValueError("border 必须是非负整数")

    # 创建 QRCode 对象
    qr = QRCode(
        version=1,
        box_size=10,
        border=border,
        error_correction=error_correction,
    )

    # 添加数据并生成二维码
    qr.add_data(qr_str)
    qr.make(fit=True)

    # 生成二维码图像
    img = qr.make_image()

    # 创建内存缓冲区用于ASCII输出
    output = io.StringIO()
    sys.stdout = output

    try:
        # 生成ASCII表示
        qr.print_ascii(out=None, tty=False, invert=invert)
        output_str = output.getvalue()
    finally:
        # 确保恢复标准输出
        sys.stdout = sys.__stdout__

    # 处理颜色反转
    if invert:
        # 将二维码图像转换为RGBA模式以便正确处理反转
        if img.mode == '1':
            img = img.convert('L')
        img = ImageOps.invert(img)

    return {"str": output_str, "img": img}


def pil_image2central_proportion_cutting(
        pil_image: Image.Image,
        target_width2height_ratio: float
) -> Optional[Image.Image]:
    """
    对图像进行中心比例裁切，保持目标宽高比
    Args:
        pil_image: 要处理的 PIL 图像对象
        target_width2height_ratio: 目标宽高比（宽度/高度的比值）
            示例：
            - 16:9 → 16/9 ≈ 1.778
            - 1:1 → 1.0
            - 4:3 → 1.333
    Returns:
        Image.Image: 裁切后的新图像对象，如果裁切失败返回 None
    Raises:
        TypeError: 输入不是有效的 PIL 图像对象
        ValueError: 目标比例不是正数或裁切尺寸无效
    """
    # 参数验证
    if not isinstance(pil_image, Image.Image):
        raise TypeError("输入必须是有效的 PIL.Image.Image 对象")

    if target_width2height_ratio <= 0:
        raise ValueError("目标比例必须是正数")

    # 获取原始尺寸
    original_width, original_height = pil_image.size
    original_ratio = original_width / original_height

    try:
        # 计算裁切区域
        if original_ratio > target_width2height_ratio:
            # 过宽：固定高度，计算宽度
            crop_height = original_height
            crop_width = int(round(crop_height * target_width2height_ratio))
        else:
            # 过高：固定宽度，计算高度
            crop_width = original_width
            crop_height = int(round(crop_width / target_width2height_ratio))

        # 验证裁切尺寸
        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("计算出的裁切尺寸无效")
        if crop_width > original_width or crop_height > original_height:
            raise ValueError("原始图片尺寸不足以完成裁切")

        # 计算裁切坐标
        left = (original_width - crop_width) // 2
        top = (original_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        return pil_image.crop((left, top, right, bottom))

    except ValueError as e:
        raise ValueError(f"裁切失败: {str(e)}")
    except Exception as e:
        raise ValueError(f"未知错误: {str(e)}")


def pil_image2zooming(
        pil_image: Image.Image,
        zooming_quality: Literal[1, 2, 3, 4],
        target_width: Optional[int] = None,  # Optional[int] 可以简写为 int | None(3.9中为Union[int, None])
        scale_factor: Optional[int] = None  # Optional[int] 可以简写为 int | None(3.9中为Union[int, None])
) -> Image.Image:
    """
    对 PIL 图像进行缩放操作，支持指定目标宽度或缩小倍数

    Args:
        pil_image: 要缩放的 PIL 图像对象
        zooming_quality: 缩放质量等级 (1-4)
            1 = 最近邻 (速度快质量低)
            2 = 双线性 (平衡模式)
            3 = 双三次 (高质量放大)
            4 = Lanczos (最高质量)
        target_width: 目标宽度（与 scale_factor 二选一）
        scale_factor: 缩小倍数（与 target_width 二选一）

    Returns:
        Dict: 包含两种缩放结果的字典
            widthZoomingPIL_Image: 按宽度缩放的结果图像（如参数有效）
            timesZoomingPIL_Image: 按比例缩放的结果图像（如参数有效）

    Raises:
        ValueError: 参数不符合要求时抛出
        TypeError: 输入图像类型错误时抛出
    """
    # 参数验证
    if not isinstance(pil_image, Image.Image):
        raise TypeError("输入必须是 PIL.Image.Image 对象")
    if zooming_quality not in (1, 2, 3, 4):
        raise ValueError("缩放质量等级必须是 1-4 的整数")
    if not (False if bool(target_width) == bool(scale_factor) else True):
        raise ValueError("正确使用参数 target_width 或 scale_factor")
    # 选择重采样滤波器
    resampling_filter4zooming_quality = {
        1: Image.Resampling.NEAREST,
        2: Image.Resampling.BILINEAR,
        3: Image.Resampling.BICUBIC,
        4: Image.Resampling.LANCZOS,
    }
    resampling_filter = resampling_filter4zooming_quality[zooming_quality]
    # """
    # 滤波器名称	        质量	速度	适用场景
    # Image.NEAREST	    低	最快	像素艺术/保留原始像素值
    # Image.BILINEAR	中	较快	通用缩放（默认选项）
    # Image.BICUBIC	    高	较慢	高质量放大
    # Image.LANCZOS	    最高	最慢	超高精度缩放（推荐选项）
    # """
    original_width, original_height = pil_image.size
    width_height_ratio = original_width / original_height
    new_width = None
    if target_width:
        if target_width > original_width:
            raise ValueError("目标宽度必须小于原宽度")
        new_width = target_width
    elif scale_factor:
        if scale_factor < original_height:
            raise ValueError("比例因子必须小于原高度")
        if 1 < scale_factor:
            raise ValueError("比例因子必须大于1")
        new_width = original_width / scale_factor
    new_height = new_width / width_height_ratio
    zooming_pil_image = pil_image.resize((round(new_width), round(new_height)), resampling_filter)
    return zooming_pil_image


def pil_image2binary(
        pil_image: Image.Image,
        img_format: Literal["PNG", "JPEG"],
        compress_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
) -> bytes:
    """
    将 PIL 图像对象转换为指定格式的二进制数据

    Args:
        pil_image: PIL 图像对象
        img_format: 输出图像格式
            "PNG" - 使用无损压缩
            "JPEG" - 使用有损压缩
        compress_level: 压缩等级 (不同格式有不同表现)
            对于 PNG: 压缩级别 0-9 (0=无压缩，9=最大压缩)
            对于 JPEG: 质量等级 5-95 (自动映射压缩级别到质量参数)

    Returns:
        bytes: 图像二进制数据

    Raises:
        ValueError: 参数不合法时抛出
        OSError: 图像保存失败时抛出
    """
    # 参数验证
    if not isinstance(pil_image, Image.Image):
        raise ValueError("输入必须是有效的 PIL.Image.Image 对象")
    if img_format not in ("PNG", "JPEG"):
        raise ValueError(f"不支持的图像格式: {img_format}，只支持 PNG/JPEG")
    if compress_level not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        raise ValueError(f"不支持的压缩级别: {compress_level}，只支持 0～9")
    # 准备保存参数
    save_kwargs = {}
    if img_format == "PNG":
        save_kwargs = {
            "format": "PNG",
            "compress_level": compress_level  # 将压缩级别映射到质量参数 (0=最高压缩，9=最高质量)
        }
    if img_format == "JPEG":
        quality = 95 - (compress_level * 10)
        quality = max(5, min(95, quality))  # 确保在有效范围内
        # 转换图像模式为 RGB
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        save_kwargs = {
            "format": "JPEG",
            "quality": quality,
            "subsampling": 0 if quality >= 90 else 1  # 高质量使用全采样
        }
    # 执行转换
    buffer = io.BytesIO()
    try:
        pil_image.save(buffer, **save_kwargs)
    except Exception as e:
        raise OSError(f"图像保存失败: {str(e)}") from e
    image_bytes = buffer.getvalue()  # 转换为字节流
    return image_bytes
# end

# 不登录也能用的api
class BilibiliApiGeneric:
    """
    不登录也能用的api
    """
    def __init__(self, ssl_verification: bool = True):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        }
        self.sslVerification = ssl_verification

    def get_bilibili_user_card(self, mid, photo=False) -> dict:
        """
        获取Bilibili用户名片信息

        参数:
        mid (int/str): 目标用户mid (必需)
        photo (bool): 是否请求用户主页头图 (可选，默认为False)

        返回:
        dict: 解析后的用户信息字典，包含主要字段
        """
        # API地址
        url = "https://api.bilibili.com/x/web-interface/card"

        # 请求参数
        params = {
            'mid': mid,
            'photo': 'true' if photo else 'false'
        }

        try:
            # 发送GET请求
            response = requests.get(verify=self.sslVerification, url = url, params=params,  headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            data = response.json()

            # 检查API返回状态
            if data['code'] != 0:
                return {
                    'error': True,
                    'code': data['code'],
                    'message': data['message'],
                    'ttl': data.get('ttl')
                }

            # 提取主要数据
            result = {
                'basic_info': {
                    'mid': data['data']['card'].get('mid'),
                    'name': data['data']['card'].get('name'),
                    'sex': data['data']['card'].get('sex'),
                    'avatar': data['data']['card'].get('face'),
                    'sign': data['data']['card'].get('sign'),
                    'level': data['data']['card']['level_info']['current_level'] if 'level_info' in data['data'][
                        'card'] else 0,
                    'status': '正常' if data['data']['card'].get('spacesta') == 0 else '封禁'
                },
                'stats': {
                    'following': data['data'].get('following'),
                    'archive_count': data['data'].get('archive_count'),
                    'follower': data['data'].get('follower'),
                    'like_num': data['data'].get('like_num'),
                    'attention': data['data']['card'].get('attention')  # 关注数
                },
                'verification': {
                    'role': data['data']['card']['Official'].get('role') if 'Official' in data['data'][
                        'card'] else -1,
                    'title': data['data']['card']['Official'].get('title') if 'Official' in data['data'][
                        'card'] else '',
                    'type': data['data']['card']['Official'].get('type') if 'Official' in data['data'][
                        'card'] else -1
                },
                'vip_info': {
                    'type': data['data']['card']['vip'].get('vipType') if 'vip' in data['data']['card'] else 0,
                    'status': data['data']['card']['vip'].get('vipStatus') if 'vip' in data['data']['card'] else 0,
                    'label': data['data']['card']['vip']['label'].get('text') if 'vip' in data['data'][
                        'card'] and 'label' in data['data']['card']['vip'] else ''
                }
            }

            # 如果请求了头图
            if photo and 'space' in data['data']:
                result['space_image'] = {
                    'small': data['data']['space'].get('s_img'),
                    'large': data['data']['space'].get('l_img')
                }

            # 添加勋章信息（如果存在）
            if 'nameplate' in data['data']['card']:
                result['nameplate'] = {
                    'id': data['data']['card']['nameplate'].get('nid'),
                    'name': data['data']['card']['nameplate'].get('name'),
                    'image': data['data']['card']['nameplate'].get('image'),
                    'level': data['data']['card']['nameplate'].get('level')
                }

            # 添加挂件信息（如果存在）
            if 'pendant' in data['data']['card']:
                result['pendant'] = {
                    'id': data['data']['card']['pendant'].get('pid'),
                    'name': data['data']['card']['pendant'].get('name'),
                    'image': data['data']['card']['pendant'].get('image')
                }

            return result

        except requests.exceptions.RequestException as e:
            return {'error': True, 'message': f'网络请求失败: {str(e)}'}
        except ValueError as e:
            return {'error': True, 'message': f'JSON解析失败: {str(e)}'}
        except KeyError as e:
            return {'error': True, 'message': f'响应数据缺少必要字段: {str(e)}'}

    def get_room_base_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间基本信息

        Args:
            room_id: 直播间短ID

        Returns:
            包含直播间信息的字典，结构:
                - "room_id": int,       # 直播间长ID
                - "uid": int,            # 主播用户mid
                - "area_id": int,        # 直播间分区ID
                - "live_status": int,    # 直播状态(0:未开播,1:直播中,2:轮播中)
                - "live_url": str,       # 直播间网页url
                - "parent_area_id": int, # 父分区ID
                - "title": str,          # 直播间标题
                - "parent_area_name": str, # 父分区名称
                - "area_name": str,      # 分区名称
                - "live_time": str,      # 开播时间(yyyy-MM-dd HH:mm:ss)
                - "description": str,    # 直播间简介
                - "tags": str,           # 直播间标签(逗号分隔)
                - "attention": int,      # 关注数
                - "online": int,         # 在线人数
                - "short_id": int,       # 直播间短ID(0表示无短号)
                - "uname": str,          # 主播用户名
                - "cover": str,          # 直播间封面url
                - "background": str,     # 直播间背景url
                - # 其他字段: join_slide, live_id, live_id_str

        Raises:
            RequestException: 网络请求失败
            ValueError: API返回错误或数据结构异常
        """
        api_url = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
        params = {
            "req_biz": "web_room_componet",
            "room_ids": room_id
        }

        try:
            # 发送API请求
            response = requests.get(verify=self.sslVerification, url = api_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            data = response.json()

            # 验证API响应
            if data.get("code") != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                raise ValueError(f"API错误: {error_msg}")

            # 提取房间信息
            by_room_ids = data.get("data").get("by_room_ids")
            if not by_room_ids:
                raise ValueError("未找到房间信息")

            # 返回第一个房间信息（即使多个也取第一个）
            room_info = next(iter(by_room_ids.values()), None)
            if not room_info:
                raise ValueError("房间信息为空")

            return room_info

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"网络请求失败: {e}") from e
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"数据处理失败: {e}") from e

    def get_area_obj_list(self):
        """
        获取B站直播分区信息

        返回数据结构:
            {
                "code": int,         # 0表示成功，非0表示错误\n
                "msg": str,          # 错误信息（通常与message相同）\n
                "message": str,      # 错误信息\n
                "data": [            # 父分区列表\n
                    {
                        "id": int,   # 父分区ID\n
                        "name": str, # 父分区名称\n
                        "list": [    # 子分区列表\n
                            {
                                # 子分区核心字段\n
                                "id": str,         # 子分区ID\n
                                "parent_id": str,   # 父分区ID\n
                                "old_area_id": str, # 旧分区ID\n
                                "name": str,       # 子分区名称\n
                                "hot_status": int,  # 是否热门分区(0:否, 1:是)\n
                                "pic": str,        # 分区图标URL\n

                                # 其他可选字段\n
                                "act_id": str,      # 活动ID（作用不明）\n
                                "pk_status": str,   # PK状态（作用不明）\n
                                "lock_status": str, # 锁定状态（作用不明）\n
                                "parent_name": str, # 父分区名称（冗余）\n
                                "area_type": int    # 分区类型\n
                            },
                            ...  # 更多子分区\n
                        ]
                    },
                    ...  # 更多父分区\n
                ]
            }

        Raises:
            requests.RequestException: 网络请求失败
            ValueError: 返回数据结构异常或API返回错误
        """
        api_url = "https://api.live.bilibili.com/room/v1/Area/getList"

        try:
            # 发送API请求
            response = requests.get(verify=self.sslVerification, url = api_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查HTTP错误状态

            # 解析JSON响应
            data = response.json()

            # 基本验证响应结构
            if not isinstance(data, dict) or "code" not in data:
                raise ValueError("返回数据结构异常")

            # 检查API错误码
            if data.get("code") != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                raise ValueError(f"API返回错误: {error_msg}")

            # 检查核心数据结构
            if "data" not in data or not isinstance(data["data"], list):
                raise ValueError("返回数据缺少分区列表")

            return data

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"网络请求失败: {e}") from e
        except ValueError as e:
            raise ValueError(f"数据处理失败: {e}") from e

    def get_anchor_common_areas(self, room_id: Union[str, int]) -> Dict[str, Any]:
        """
        获取主播常用分区信息

        该API返回主播设置的常用分区列表（通常为3个分区）

         Args:
            room_id: 直播间ID（整数或字符串）

        Returns:
        {
            "code": int,        # 0表示成功\n
            "msg": str,         # 状态消息\n
            "message": str,     # 状态消息（通常与msg相同）\n
            "data": [           # 常用分区列表\n
                {
                    "id": str,             # 分区ID\n
                    "pic": str,             # 分区图标URL\n
                    "hot_status": str,      # 热门状态（0:非热门）\n
                    "name": str,            # 分区名称\n
                    "parent_id": str,       # 父分区ID\n
                    "parent_name": str,     # 父分区名称\n
                    "act_flag": int         # 活动标志（通常为0）\n
                },
                ...  # 更多分区（通常最多3个）\n
            ]
        }

        Raises:
            ValueError: 输入参数无效
            requests.RequestException: 网络请求失败
            RuntimeError: API返回错误或无效数据
        """
        # 验证房间ID
        if not room_id:
            raise ValueError("房间ID不能为空")

        # API配置
        api_url = "https://api.live.bilibili.com/room/v1/Area/getMyChooseArea"
        params = {"roomid": str(room_id)}

        try:
            # 发送API请求
            response = requests.get(verify=self.sslVerification, url = api_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            result = response.json()

            # 验证基本结构
            if not isinstance(result, dict) or "code" not in result:
                raise RuntimeError("API返回无效的响应格式")

            # 检查API错误码
            if result.get("code") != 0:
                error_msg = result.get("message") or result.get("msg") or "未知错误"
                raise RuntimeError(f"API返回错误: {error_msg} (code: {result['code']})")

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], list):
                raise RuntimeError("API返回数据格式无效")

            # 验证分区数据
            for area in result["data"]:
                required_keys = {"id", "name", "parent_id", "parent_name"}
                if not required_keys.issubset(area.keys()):
                    raise RuntimeError("分区数据缺少必需字段")

            return result

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"获取主播分区信息失败: {e}"
            ) from e
        except (ValueError, TypeError) as e:
            raise ValueError(f"数据处理失败: {e}") from e

    def live_user_v1_master_info(self, uid: int):
        """
        <h2 id="获取主播信息" tabindex="-1"><a class="header-anchor" href="#获取主播信息" aria-hidden="true">#</a> 获取主播信息</h2>
        <blockquote><p>https://api.live.bilibili.com/live_user/v1/Master/info</p></blockquote>
        <p><em>请求方式：GET</em></p>
        <p><strong>url参数：</strong></p>
        <table><thead><tr><th>参数名</th><th>类型</th><th>内容</th><th>必要性</th><th>备注</th></tr></thead><tbody><tr><td>uid</td><td>num</td><td>目标用户mid</td><td>必要</td><td></td></tr></tbody></table>
        <p><strong>json回复：</strong></p>
        <p>根对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>code</td><td>num</td><td>返回值</td><td>0：成功<br>1：参数错误</td></tr><tr><td>msg</td><td>str</td><td>错误信息</td><td>默认为空</td></tr><tr><td>message</td><td>str</td><td>错误信息</td><td>默认为空</td></tr><tr><td>data</td><td>obj</td><td>信息本体</td><td></td></tr></tbody></table>
        <p><code>data</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>info</td><td>obj</td><td>主播信息</td><td></td></tr><tr><td>exp</td><td>obj</td><td>经验等级</td><td></td></tr><tr><td>follower_num</td><td>num</td><td>主播粉丝数</td><td></td></tr><tr><td>room_id</td><td>num</td><td>直播间id（短号）</td><td></td></tr><tr><td>medal_name</td><td>str</td><td>粉丝勋章名</td><td></td></tr><tr><td>glory_count</td><td>num</td><td>主播荣誉数</td><td></td></tr><tr><td>pendant</td><td>str</td><td>直播间头像框url</td><td></td></tr><tr><td>link_group_num</td><td>num</td><td>0</td><td><strong>作用尚不明确</strong></td></tr><tr><td>room_news</td><td>obj</td><td>主播公告</td><td></td></tr></tbody></table>
        <p><code>info</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>uid</td><td>num</td><td>主播mid</td><td></td></tr><tr><td>uname</td><td>str</td><td>主播用户名</td><td></td></tr><tr><td>face</td><td>str</td><td>主播头像url</td><td></td></tr><tr><td>official_verify</td><td>obj</td><td>认证信息</td><td></td></tr><tr><td>gender</td><td>num</td><td>主播性别</td><td>-1：保密<br>0：女<br>1：男</td></tr></tbody></table>
        <p><code>info</code>中的<code>official_verify</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>type</td><td>num</td><td>主播认证类型</td><td>-1：无<br>0：个人认证<br>1：机构认证</td></tr><tr><td>desc</td><td>str</td><td>主播认证信息</td><td></td></tr></tbody></table>
        <p><code>exp</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>master_level</td><td>obj</td><td>主播等级</td><td></td></tr></tbody></table>
        <p><code>exp</code>中的<code>master_level</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>level</td><td>num</td><td>当前等级</td><td></td></tr><tr><td>color</td><td>num</td><td>等级框颜色</td><td></td></tr><tr><td>current</td><td>array</td><td>当前等级信息</td><td></td></tr><tr><td>next</td><td>array</td><td>下一等级信息</td><td></td></tr></tbody></table>
        <p><code>master_level</code>中的<code>current</code>数组：</p>
        <table><thead><tr><th>项</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>0</td><td>num</td><td>升级积分</td><td></td></tr><tr><td>1</td><td>num</td><td>总积分</td><td></td></tr></tbody></table>
        <p><code>master_level</code>中的<code>next</code>数组：</p>
        <table><thead><tr><th>项</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>0</td><td>num</td><td>升级积分</td><td></td></tr><tr><td>1</td><td>num</td><td>总积分</td><td></td></tr></tbody></table>
        <p><code>room_news</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>content</td><td>str</td><td>公告内容</td><td></td></tr><tr><td>ctime</td><td>str</td><td>公告时间</td><td></td></tr><tr><td>ctime_text</td><td>str</td><td>公告日期</td><td></td></tr></tbody></table>
        @param uid:目标用户mid
        @return:
        """
        api = "https://api.live.bilibili.com/live_user/v1/Master/info"
        live_user_v1_master_info_data = {
            "uid": uid
        }
        live_user_v1_master_info = requests.get(verify=self.sslVerification, url = api, headers=self.headers, params=live_user_v1_master_info_data).json()
        return live_user_v1_master_info

    def get_room_info_old(self, mid: int) -> Dict[str, Any]:
        """
        通过B站UID查询直播间基础信息
        Args:
            mid: B站用户UID
        Returns:
            直播间信息字典，包含以下字段：

                - roomStatus: 直播间状态 (0:无房间, 1:有房间)
                - roundStatus: 轮播状态 (0:未轮播, 1:轮播)
                - liveStatus: 直播状态 (0:未开播, 1:直播中)
                - url: 直播间网页URL
                - title: 直播间标题
                - cover: 直播间封面URL
                - online: 直播间人气值
                - roomid: 直播间ID（短号）
                - broadcast_type: 广播类型
                - online_hidden: 是否隐藏在线人数
        Raises:
            ValueError: 输入参数无效时抛出
            ConnectionError: 网络请求失败时抛出
            RuntimeError: API返回错误状态时抛出
        """
        # 参数验证
        if not isinstance(mid, int) or mid <= 0:
            raise ValueError("mid 必须是正整数")

        api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
        params = {"mid": mid}

        try:
            # 设置合理的超时时间
            response = requests.get(verify=self.sslVerification, url = api, headers=self.headers, params=params, timeout=5.0)
            response.raise_for_status()  # 检查HTTP状态码
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"请求直播间信息失败: {e}") from e

        # 解析JSON响应
        try:
            data = response.json()
        except ValueError as e:
            raise RuntimeError(f"解析API响应失败: {e}") from e

        # 检查API返回状态码
        if data.get("code") != 0:
            error_msg = data.get("message")
            raise RuntimeError(f"API返回错误: {error_msg} (code: {data['code']})")

        # 检查数据是否存在
        result = data.get("data")
        if not result:
            raise RuntimeError("API返回数据为空")

        # 确保返回完整字段结构
        return {
            "roomStatus": result.get("roomStatus"),
            "roundStatus": result.get("roundStatus"),
            "liveStatus": result.get("liveStatus"),
            "url": result.get("url"),
            "title": result.get("title"),
            "cover": result.get("cover"),
            "online": result.get("online"),
            "roomid": result.get("roomid"),
            "broadcast_type": result.get("broadcast_type"),
            "online_hidden": result.get("online_hidden"),
        }

    # 登陆用函数
    def generate(self, ) -> Dict:
        """
        申请登录二维码
        @return: {'url': 二维码文本, 'qrcode_key': 扫描秘钥}
        """
        api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
        url8qrcode_key = requests.get(verify=self.sslVerification, url = api, headers=self.headers).json()
        # print(url8qrcode_key)
        generate_data = url8qrcode_key['data']
        url = generate_data['url']
        qrcode_key = generate_data['qrcode_key']
        return {'url': url, 'qrcode_key': qrcode_key}

    def poll(self, qrcode_key: str) -> Dict[str, Union[Dict[str, str], int]]:  # 3.Dict[str, Dict[str, str] | int]
        """
        获取登陆状态，登陆成功获取 基础的 cookies
        @param qrcode_key: 扫描秘钥
        @return: {'code', 'cookies'}
        @rtype: Dict
        """
        api = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}'
        poll_return = requests.get(verify=self.sslVerification, url = api, data=qrcode_key, headers=self.headers).json()
        data = poll_return['data']
        cookies = {}
        """
        - DedeUserID:           用户id
        - DedeUserID__ckMd5:    携带时间戳加密的用户id
        - SESSDATA:             账户密钥
        - bili_jct:             csrf鉴权
        """
        code = data['code']
        """
        - 0：    扫码登录成功 
        - 86038：二维码已失效 
        - 86090：二维码已扫码未确认 
        - 86101：未扫码
        """
        if code == 0:  # code = 0 代表登陆成功
            data_dict = url2dict(data['url'])
            cookies["DedeUserID"] = data_dict['DedeUserID']
            cookies["DedeUserID__ckMd5"] = data_dict['DedeUserID__ckMd5']
            cookies["SESSDATA"] = data_dict['SESSDATA']
            cookies["bili_jct"] = data_dict['bili_jct']
            # 补充 cookie
            buvid3 = requests.get(verify=self.sslVerification, url = f'https://www.bilibili.com/video/', headers=self.headers)
            cookies.update(buvid3.cookies.get_dict())
        return {'code': code, 'cookies': cookies}
# end


# 登陆后才能用的函数
class BilibiliApiMaster:
    """登陆后才能用的函数"""

    def __init__(self, cookie: str, ssl_verification: bool = True):
        """
        完善 浏览器headers
        @param cookie: B站cookie
        @param sslVerification: 是否SSL验证
        """
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0")
        self.headers = {
            "User-Agent": user_agent,
            "cookie": cookie,
        }
        self.cookies = cookie2dict(cookie)
        self.cookie = cookie
        self.csrf = self.cookies.get("bili_jct", "")
        self.sslVerification = ssl_verification

    def get_nav_info(self) -> Dict[str, Any]:
        """
        获取导航栏用户信息（需要登录）

        Returns:
            包含用户信息的字典，主要字段:
            {
                "isLogin": bool,       # 是否已登录
                "mid": int,            # 用户mid
                "uname": str,          # 用户昵称
                "face": str,           # 用户头像URL
                "level_info": {        # 等级信息
                    "current_level": int,  # 当前等级
                    "current_exp": int,    # 当前经验
                    "next_exp": int/str    # 升级所需经验(Lv6时为"--")
                },
                "vipStatus": int,     # 会员开通状态(0:无,1:有)
                "vipType": int,        # 会员类型(0:无,1:月度,2:年度及以上)
                "vip_label": {         # 会员标签
                    "text": str,       # 会员名称
                    "label_theme": str # 会员标签主题
                },
                "official": {          # 认证信息
                    "type": int,       # 是否认证(-1:无,0:认证)
                    "title": str       # 认证信息
                },
                # 其他字段: money, moral, pendant, wallet等
            }

        Raises:
            RequestException: 网络请求失败
            PermissionError: 账号未登录或认证失败
        """
        api_url = "https://api.bilibili.com/x/web-interface/nav"

        try:
            # 发送API请求
            response = requests.get(verify=self.sslVerification, url = api_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            data = response.json()

            # 返回用户信息
            return data.get("data")

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"网络请求失败: {e}") from e
        except PermissionError as e:
            raise PermissionError(f"认证失败: {e}") from e

    def get_room_highlight_state(self):
        """
        获取直播间号
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/highlight/getRoomHighlightState"
        headers = self.headers
        room_id = requests.get(verify=self.sslVerification, url = api, headers=headers).json()["data"]["room_id"]
        return room_id

    def get_room_news(self) -> str:
        # 获取直播公告
        headers = self.headers
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getRoomNews"
        params = {
            'room_id': self.get_room_highlight_state(),
            'uid': cookie2dict(self.headers["cookie"])["DedeUserID"]
        }
        room_news = requests.get(verify=self.sslVerification, url = api, headers=headers, params=params).json()
        return room_news["data"]["content"]

    def get_reserve_list(self) -> List[Dict[str, Any]]:
        """
        获取用户直播预约列表

        Returns:
            预约列表，每个预约项包含:
            {
                "reserve_info": {
                    "sid": int,          # 预约ID
                    "name": str,         # 预约名称
                    "total": int,        # 预约人数
                    "is_follow": int,    # 是否已关注(0/1)
                    "live_plan_start_time": int,  # 计划开播时间(Unix时间戳)
                    "lottery": {         # 抽奖信息
                        "lottery_id": int,
                        "lottery_text": str
                    },
                    "button_color": int, # 按钮颜色
                    "card_style": int,   # 卡片样式
                    "type": int,         # 预约类型
                    "close_page_group": bool  # 是否关闭页面组
                },
                "products": Any,        # 相关商品(通常为null)
                "stat": int              # 状态码
            }

        Raises:
            RequestException: 网络请求失败
            ValueError: API返回错误或数据结构异常
        """
        api_url = "https://api.live.bilibili.com/xlive/app-ucenter/v2/schedule/GetReserveList"

        try:
            # 发送API请求
            response = requests.get(verify=self.sslVerification, url = api_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            data = response.json()

            # 验证API响应
            if data.get("code") != 0:
                error_msg = data.get("message")
                raise ValueError(f"API错误: {error_msg}")

            # 提取预约列表
            reserve_list = data.get("data").get("list") if data.get("data").get("list") else []
            if not isinstance(reserve_list, list):
                raise ValueError("返回数据格式异常，缺少预约列表")

            return reserve_list

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"获取预约列表失败: {e}") from e
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"数据处理失败: {e}") from e

    # """需要Csrf鉴权的"""
    def create_live_room(self) -> Dict[str, Any]:
        """
        开通直播间（创建直播间房间）

        Returns:
            开通成功的直播间返回值

        Raises:
            RuntimeError: 开通失败时抛出，包含错误信息
            ValueError: 缺少必要参数时抛出

        错误代码:
            - 0: 成功
            - 1531193016: 已经创建过直播间
            - -400: 请求错误
        """
        # 检查必要的CSRF token
        if not self.csrf:
            raise ValueError("缺少bili_jct值，无法进行CSRF验证")

        api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/preLive/CreateRoom"

        # 准备请求数据
        data = {
            "platform": "web",
            "visit_id": "",
            "csrf": self.csrf,
            "csrf_token": self.csrf,
        }

        try:
            # 发送POST请求
            response = requests.post(verify=self.sslVerification, url = api_url,
                data=data,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            result = response.json()
            return result

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"网络请求失败: {e}") from e
        except (ValueError, KeyError) as e:
            raise RuntimeError(f"解析响应失败: {e}") from e

    def change_room_area(self, area_id: int):
        """
        更改直播分区
        @param area_id:二级分区id
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v2/room/AnchorChangeRoomArea"
        headers = self.headers
        csrf = self.csrf
        AnchorChangeRoomArea_data = {
            "platform": "pc",
            "room_id": self.get_room_highlight_state(),
            "area_id": area_id,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        ChangeRoomArea_ReturnValue = requests.post(verify=self.sslVerification, url = api, headers=headers, params=AnchorChangeRoomArea_data).json()
        return ChangeRoomArea_ReturnValue

    def rename_fans_medal(self, medal_name: str) -> dict:
        """
        修改粉丝勋章名称

        Args:
            medal_name: 新的粉丝勋章名称

        Returns:
            包含操作结果的字典，结构:
            {
                "code": int,      # 返回代码 (0表示成功)
                "message": str,    # 操作结果消息
                "msg": str,        # 操作结果消息(同message)
                "data": dict       # 附加数据
            }

            常见错误代码:
            - 5200012: 勋章名称不可含有特殊字符
            - 其他错误代码参考B站API文档
        """
        api_url = "https://api.live.bilibili.com/fans_medal/v1/medal/rename"

        # 准备请求参数
        params = {
            "uid": self.cookies.get("DedeUserID", ""),
            "source": "1",
            "medal_name": medal_name,
            "platform": "pc",
            "csrf_token": self.csrf,
            "csrf": self.csrf
        }

        # 准备请求头
        headers = {
            **self.headers,
            "origin": "https://link.bilibili.com",
            "referer": "https://link.bilibili.com/p/center/index",
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=1, i"
        }

        try:
            # 发送POST请求
            response = requests.post(
                api_url,
                headers=headers,
                data=params,
                timeout=10
            )

            # 尝试解析JSON响应
            try:
                result = response.json()
                return result
            except ValueError:
                # JSON解析失败时返回原始文本
                return {
                    "code": -1,
                    "message": f"响应解析失败: {response.text[:100]}...",
                    "msg": f"响应解析失败: {response.text[:100]}...",
                    "data": {}
                }

        except requests.exceptions.RequestException as e:
            # 网络请求异常
            return {
                "code": -1,
                "message": f"网络请求失败: {str(e)}",
                "msg": f"网络请求失败: {str(e)}",
                "data": {}
            }

    def start_live(self, area_id: int,  platform: Literal["pc_link", "web_link", "android_link"]):
        """
        开始直播
        Args:
            area_id: 二级分区id
            platform: 直播平台
        Returns:
        """
        api = "https://api.live.bilibili.com/room/v1/Room/startLive"
        headers = self.headers
        csrf = self.csrf
        startLivedata = {
            "access_key": "",  # 留空
            "appkey": "aae92bc66f3edfab",  # 固定应用密钥
            "platform": platform,  # 直播姬（pc）：pc_link、web在线直播：web_link、bililink：android_link
            "room_id": self.get_room_highlight_state(),
            "area_v2": area_id,
            "build": "9343",  # 客户端版本号
            "backup_stream": 0,
            "csrf": csrf,
            "csrf_token": csrf,
            "ts": str(int(time.time()))  # 当前UNIX时间戳
        }

        # 对参数按字典序排序
        sorted_params = sorted(startLivedata.items(), key=lambda x: x[0])

        # 生成签名字符串 (参数串 + 固定盐值)
        query_string = "&".join(f"{k}={v}" for k, v in sorted_params)
        sign_string = query_string + "af125a0d5279fd576c1b4418a3e8276d"

        # 计算MD5签名
        md5_sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

        # 添加签名到参数
        startLivedata["sign"] = md5_sign
        startLive_ReturnValue = requests.post(verify=self.sslVerification, url = api, headers=headers, params=startLivedata).json()
        return startLive_ReturnValue

    def stop_live(self,  platform: Literal["pc_link", "web_link", "android_link"]):
        """
        结束直播
        @return:
        """
        api = "https://api.live.bilibili.com/room/v1/Room/stopLive"
        headers = self.headers
        csrf = self.csrf
        stopLive_data = {
            "platform": platform,
            "room_id": self.get_room_highlight_state(),
            "csrf": csrf,
            "csrf_token": csrf,
        }
        stopLive_ReturnValue = requests.post(verify=self.sslVerification, url = api, headers=headers, params=stopLive_data).json()
        return stopLive_ReturnValue

    def create_reserve(self, title: str, live_plan_start_time: int, create_dynamic: bool = False, business_type: int = 10) -> Dict[str, Any]:
        """
        创建直播预约

        Args:
            title: 预约标题
            live_plan_start_time: 直播计划开始时间(Unix时间戳)
            create_dynamic: 是否同步发布动态(默认False)
            business_type: 业务类型(默认10)

        Returns:
            包含预约结果的字典，结构:
            {
                "code": int,    # 0表示成功
                "message": str, # 错误信息
                "ttl": int,     # 1
                "data": {
                    "sid": int  # 预约ID
                }
            }

        Raises:
            ValueError: 缺少必要参数或请求失败
        """
        # 验证必要参数
        if not self.csrf:
            raise ValueError("缺少bili_jct参数，无法获取csrf token")

        # 生成随机visit_id (16位字母数字组合)
        visit_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

        # 构建请求负载
        payload = {
            "title": title,
            "type": "2",  # 固定值
            "from": "23",  # 固定值
            "create_dynamic": "1" if create_dynamic else "0",
            "live_plan_start_time": str(live_plan_start_time),
            "business_type": str(business_type),
            "csrf_token": self.csrf,
            "csrf": self.csrf,
            "visit_id": visit_id
        }

        api_url = "https://api.live.bilibili.com/xlive/app-ucenter/v2/schedule/CreateReserve"

        try:
            response = requests.post(verify=self.sslVerification, url = api_url,
                headers=self.headers,
                data=payload,
                timeout=10
            )
            response.raise_for_status()

            # 解析响应
            result = response.json()

            return result

        except requests.exceptions.RequestException as e:
            raise ValueError(f"网络请求失败: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"响应解析失败: {e}") from e

    def cancel_reserve(self, sid: int, from_value: int = 13) -> Dict[str, Any]:
        """
        取消直播预约

        Args:
            sid: 预约活动ID
            from_value: 来源标识（默认13）

        Returns:
            包含操作结果的字典，结构:
            {
                "code": int,     # 0表示成功
                "message": str,   # 错误信息
                "ttl": int,       # 1
                "data": dict      # 空字典
            }

        Raises:
            ValueError: 缺少必要的CSRF token
            RequestException: 网络请求失败
        """
        # 检查CSRF token
        if not self.csrf:
            raise ValueError("缺少bili_jct值，无法进行身份验证")

        # 生成随机visit_id (12位字母数字)
        visit_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

        # 构造请求参数
        payload = {
            "sid": sid,
            "from": from_value,
            "csrf_token": self.csrf,
            "csrf": self.csrf,
            "visit_id": visit_id
        }

        try:
            # 发送POST请求
            response = requests.post(verify=self.sslVerification, url = "https://api.live.bilibili.com/xlive/app-ucenter/v2/schedule/CancelReserve",
                headers=self.headers,
                data=payload,
                timeout=10
            )
            response.raise_for_status()  # 检查HTTP错误

            # 解析并返回JSON响应
            return response.json()

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"取消预约请求失败: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"解析响应失败: {e}") from e

    def get_live_stream_info(self) -> Dict[str, Any]:
        """
        获取直播间推流信息

        Returns:
            包含推流信息的字典，结构:
            {
                "code": int,        # API状态码(0:成功)
                "message": str,      # API消息
                "data": {
                    "rtmp": {
                        "addr": str,     # RTMP服务器地址
                        "code": str      # 推流代码(包含streamkey)
                    },
                    "stream_line": [    # 可用线路列表
                        {
                            "cdn_name": str,  # CDN名称
                            "checked": int,   # 是否选中(0/1)
                            "name": str,      # 线路名称
                            "src": int        # 线路标识
                        }
                    ]
                }
            }

            如果请求失败，返回:
            {
                "code": -1,
                "error": "错误信息"
            }
        """
        api_url = "https://api.live.bilibili.com/live_stream/v1/StreamList/get_stream_by_roomId"
        params = {"room_id": self.get_room_highlight_state()}

        try:
            # 发送API请求
            response = requests.get(verify=self.sslVerification, url = api_url,headers=self.headers,params=params,timeout=10)

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "code": -1,
                    "error": f"HTTP错误: {response.status_code}"
                }

            # 解析JSON响应
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            return {
                "code": -1,
                "error": f"网络请求失败: {str(e)}"
            }
        except ValueError as e:
            return {
                "code": -1,
                "error": f"JSON解析失败: {str(e)}"
            }

    def fetch_stream_addr(self, platform: Literal["pc_link", "web_link", "android_link"], reset_key: bool = False):
        """
        推流码信息
        @param reset_key: 布尔值，是否更新推流码
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/live/FetchWebUpStreamAddr"
        headers = self.headers
        csrf = self.csrf
        FetchWebUpStreamAddr_data = {
            "platform": platform,
            "backup_stream": 0,
            "reset_key": reset_key,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        FetchWebUpStreamAddre_ReturnValue = requests.post(verify=self.sslVerification, url = api, headers=headers, params=FetchWebUpStreamAddr_data).json()
        return FetchWebUpStreamAddre_ReturnValue

    def change_room_title(self, title: str):
        """
        更新直播标题
        @return:
        """
        headers = self.headers
        csrf = self.csrf
        api = "https://api.live.bilibili.com/room/v1/Room/update"
        room_v1_Room_update_data = {
            'room_id': self.get_room_highlight_state(),
            'title': title,
            'csrf_token': csrf,
            'csrf': csrf
        }
        room_v1_Room_update_ReturnValue = requests.post(verify=self.sslVerification, url = api, headers=headers, data=room_v1_Room_update_data).json()
        return room_v1_Room_update_ReturnValue

    def change_room_news(self, content: str):
        """
        更新直播公告
        @return:
        """
        headers = self.headers
        csrf = self.csrf
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/updateRoomNews"
        updateRoomNews_data = {
            'room_id': self.get_room_highlight_state(),
            'uid': self.cookies["DedeUserID"],
            'content': content,
            'csrf_token': csrf,
            'csrf': csrf
        }
        updateRoomNews_ReturnValue = requests.post(verify=self.sslVerification, url = api, headers=headers, data=updateRoomNews_data).json()
        return updateRoomNews_ReturnValue

    def upload_cover(self, image_binary: bytes):
        """
        上传直播间封面到B站(符合官方请求格式)
        :param image_binary: png/jpeg图像的二进制格式数据
        """
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
              "537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        # 构建请求参数
        api_url = "https://api.bilibili.com/x/upload/web/image"
        # 准备multipart/form-data数据
        boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        headers = {
            "User-Agent": UA,
            "Cookie": self.cookie,
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
        # 构建multipart body
        data_parts = []
        # 添加普通字段
        fields = {
            "bucket": "live",
            "dir": "new_room_cover",
            "csrf": self.cookies["bili_jct"]
        }
        for name, value in fields.items():
            data_parts.append(
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f'{value}\r\n'
            )
        data_parts.append(
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="blob"\r\n'
            f'Content-Type: image/jpeg\r\n\r\n'
        )
        data_parts.append(image_binary)
        data_parts.append(f'\r\n--{boundary}--\r\n')
        # 构建最终body
        body = b''
        for part in data_parts:
            if isinstance(part, str):
                body += part.encode('utf-8')
            else:
                body += part
        # 发送请求
        response = requests.post(verify=self.sslVerification, url = api_url, headers=headers, data=body).json()
        # 处理响应
        result = response
        return result

    def update_cover(self, cover_url: str):
        ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
              "537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        headers = {
            "User-Agent": ua,
            "cookie": self.cookie,
        }
        # 构建请求参数
        api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/preLive/UpdatePreLiveInfo"
        update_cover_data = {
            "platform": "web",
            "mobi_app": "web",
            "build": 1,
            "cover": cover_url,
            "coverVertical": "",
            "liveDirectionType": 1,
            "csrf_token": self.cookies["bili_jct"],
            "csrf": self.cookies["bili_jct"],
        }
        return requests.post(verify=self.sslVerification, url = api_url, headers=headers, params=update_cover_data).json()
# end

# ====================================================================================================================


# -----------------------------------------------------------
# OBS Script Functions                                      -
# -----------------------------------------------------------

def trigger_frontend_event(event):
    """
    处理推流事件
    """
    log_save(0, f"┏━━━━监测到obs前端事件━━━━━┓")
    log_save(0, f"┃　　　　监测到obs前端事件　　　　　┃{information4frontend_event[event]}")
    log_save(0, f"┗━━━━监测到obs前端事件━━━━━┛")
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        last_status_change = time.time()
        log_save(0, f"监控到推流开始事件: {last_status_change}")
        if GlobalVariableOfData.streaming_active != obs.obs_frontend_streaming_active():
            log_save(0, f"推流状态发生变化：{GlobalVariableOfData.streaming_active}➡️{obs.obs_frontend_streaming_active()}")
            GlobalVariableOfData.streaming_active = obs.obs_frontend_streaming_active()
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        last_status_change = time.time()
        log_save(0, f"监控到推流停止事件: {last_status_change}")
        if GlobalVariableOfData.streaming_active != obs.obs_frontend_streaming_active():
            log_save(0, f"推流状态发生变化：{GlobalVariableOfData.streaming_active}➡️{obs.obs_frontend_streaming_active()}")
            GlobalVariableOfData.streaming_active = obs.obs_frontend_streaming_active()
            log_save(0, f"尝试关闭直播")
            button_function_stop_live()
    return True


def property_modified(t=""):
    if t == "bottom_button":
        log_save(0, f"┏━UI变动事件测试函数被调用（Script_properties）开始━┓")
        log_save(0, f"┃　UI变动事件测试函数被调用（Script_properties）开始　┃")
        log_save(0, f"┗━UI变动事件测试函数被调用（Script_properties）开始━┛")
        GlobalVariableOfData.isScript_propertiesIs = True
    if not GlobalVariableOfData.isScript_propertiesIs:
        if t == "room_parentArea_comboBox":
            return button_function_start_parent_area()
        elif t == "room_cover_fileDialogBox":
            return button_function_update_room_cover()
        elif t == "room_commonTitles_comboBox":
            return button_function_true_live_room_title()
        elif t == "room_commonAreas_comboBox":
            return button_function_true_live_room_area()
        elif t == "live_bookings_day_digitalSlider":
            return button_function_true_live_appointment_day()
        elif t == "live_bookings_hour_digitalSlider":
            return button_function_true_live_appointment_hour()
        elif t == "live_bookings_minute_digitalSlider":
            return button_function_true_live_appointment_minute()
        log_save(0, f"┏━UI变动事件测试函数被调用━┓")
        log_save(0, f"┃　UI变动事件测试函数被调用　┃ {t}")
        log_save(0, f"┗━UI变动事件测试函数被调用━┛")
    if t == "top_button":
        log_save(0, f"┏━UI变动事件测试函数被调用（Script_properties）结束━┓")
        log_save(0, f"┃　UI变动事件测试函数被调用（Script_properties）结束　┃")
        log_save(0, f"┗━UI变动事件测试函数被调用（Script_properties）结束━┛")
        GlobalVariableOfData.isScript_propertiesIs = False
    return False


# --- 设置默认值
def script_defaults(settings):  # 设置其默认值
    """
    调用以设置与脚本关联的默认设置(如果有的话)。为了设置其默认值，您通常会调用默认值函数。
    :param settings:与脚本关联的设置。
    """
    # 检查网络连接
    GlobalVariableOfData.networkConnectionStatus = check_network_connection()
    if GlobalVariableOfData.networkConnectionStatus:
        log_save(0, f"⭐检查网络连接: 网络可用⭐")
    else:
        log_save(3, f"⚠️检查网络连接: 网络不可用❌")
        return None
    GlobalVariableOfData.sslVerification, ssl_warning = check_ssl_verification()
    if not GlobalVariableOfData.sslVerification:
        log_save(3, f"[SSL 警告] {ssl_warning}")
    else:
        log_save(0, f"[SSL 正常] {ssl_warning}")
    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║设置路径变量")
    log_save(0, f"║╔{4 * '═'}路径变量{4 * '═'}╗")
    GlobalVariableOfData.scriptsDataDirpath = f"{script_path()}bilibili-live"
    log_save(0, f"║║脚本用户数据文件夹路径：{GlobalVariableOfData.scriptsDataDirpath}")
    GlobalVariableOfData.scriptsUsersConfigFilepath = Path(GlobalVariableOfData.scriptsDataDirpath) / "config.json"
    log_save(0, f"║║脚本用户数据路径：{GlobalVariableOfData.scriptsUsersConfigFilepath}")
    GlobalVariableOfData.scriptsTempDir = Path(GlobalVariableOfData.scriptsDataDirpath) / "temp"
    os.makedirs(GlobalVariableOfData.scriptsTempDir, exist_ok=True)
    log_save(0, f"║║脚本临时文件夹路径：{GlobalVariableOfData.scriptsTempDir}")
    GlobalVariableOfData.scriptsLogDir = Path(GlobalVariableOfData.scriptsDataDirpath) / "log"
    os.makedirs(GlobalVariableOfData.scriptsLogDir, exist_ok=True)
    log_save(0, f"║║脚本日志文件夹路径：{GlobalVariableOfData.scriptsLogDir}")
    GlobalVariableOfData.scriptsCacheDir = Path(GlobalVariableOfData.scriptsDataDirpath) / "cache"
    os.makedirs(GlobalVariableOfData.scriptsCacheDir, exist_ok=True)
    log_save(0, f"║║脚本缓存文件夹路径：{GlobalVariableOfData.scriptsCacheDir}")
    log_save(0, f"║╚{4 * '═'}路径变量{4 * '═'}╝")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    b_a_m = BilibiliApiMaster(dict2cookie(b_u_l_c.get_cookies()), GlobalVariableOfData.sslVerification) if b_u_l_c.get_cookies() else None
    b_a_g = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification)
    # 获取 用户配置文件 中 每一个 用户 的 昵称
    all_is_login4uid = {}
    all_uname4uid = {}
    """账号字典"""
    for uid in b_u_l_c.get_users().values():
        if uid:
            all_is_login4uid[uid] = BilibiliApiMaster(
                dict2cookie(b_u_l_c.get_cookies(int(uid))), GlobalVariableOfData.sslVerification
            ).get_nav_info()
            all_uname4uid[uid] = b_a_g.get_bilibili_user_card(uid)['basic_info']['name']
    log_save(0, f"║║载入账号字典：{all_uname4uid}")
    # 获取 '登录用户' 的昵称
    uname = all_uname4uid[b_u_l_c.get_users()[0]] if b_u_l_c.get_cookies() else None
    """登录用户的昵称，没有登录则为None"""
    log_save(0, f"║║用户：{(uname + ' 已登录') if b_u_l_c.get_cookies() else '⚠️未登录账号'}")
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = b_a_g.get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间id"""
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (b_a_g.get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间基本信息"""
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_base_info if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间封面链接
    room_cover_url = (room_base_info["cover"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户直播间封面链接"""
    log_save(0, f"║║登录账户 的 直播间封面链接：{(room_cover_url if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间标题
    room_title = (room_base_info["title"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户直播间标题"""
    log_save(0, f"║║登录账户 的 直播间标题：{(room_title if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 创建用户常用直播间标题实例
    c_t_m = CommonTitlesManager(directory=Path(GlobalVariableOfData.scriptsDataDirpath))
    # 添加当前直播间标题 到 常用直播间标 题配置文件
    (c_t_m.add_title(b_u_l_c.get_users()[0], room_title) if room_status else None) if b_u_l_c.get_cookies() else None
    # 获取 常用直播间标题
    common_title4number = {str(number): commonTitle for number, commonTitle in enumerate(c_t_m.get_titles(b_u_l_c.get_users()[0]))}
    """常用直播间标题】{'0': 't1', '1': 't2', '2': 't3',}"""
    log_save(0, f"║║登录账户 的 常用直播间标题：{(common_title4number if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 直播间公告
    room_news = (b_a_m.get_room_news() if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间公告"""
    log_save(0, f"║║登录账户 的 直播间公告：{(room_news if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间的分区
    area = ({"parent_area_id": room_base_info["parent_area_id"], "parent_area_name": room_base_info["parent_area_name"], "area_id": room_base_info["area_id"], "area_name": room_base_info["area_name"], } if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间分区】{"parent_area_id": 3, "parent_area_name": "手游", "area_id": 255, "area_name": "明日方舟"}"""
    log_save(0, f"║║登录账户 的 直播间分区数据：{(area if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间 常用分区信息
    common_areas = (b_a_g.get_anchor_common_areas(room_id)["data"] if room_status else None) if b_u_l_c.get_cookies() else None
    """获取 '登录用户' 直播间 常用分区信息】[{"id": "255", "name": "明日方舟", "parent_id": "3", "parent_name": "手游",}, ]"""
    log_save(0, f"║║登录账户 的 常用分区信息：{(common_areas if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 常用直播间分区字典
    common_area_id_dict_str4common_area_name_dict_str = (({json.dumps({area['parent_id']: area['id']}, ensure_ascii=False): json.dumps({area['parent_name']: area['name']}, ensure_ascii=False) for area in common_areas} if common_areas else {"-1": "无常用分区"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """登录用户的常用直播间分区字典】{'{parent_id: id}': '{parent_name: name}', }"""
    log_save(0, f"║║登录账户 的 常用直播间分区：{(list(common_area_id_dict_str4common_area_name_dict_str.values()) if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 B站直播分区信息
    area_obj_list = b_a_g.get_area_obj_list() if b_u_l_c.get_cookies() else None
    """B站直播分区信息"""
    log_save(0, f"║║获取B站直播分区信息：{area_obj_list if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 直播间父分区数据
    parent_live_area_name4parent_live_area_id = (({str(AreaObj["id"]): AreaObj["name"] for AreaObj in area_obj_list['data']} | {} if area else {"-1": "请选择一级分区"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """直播间父分区数据"""
    log_save(0, f"║║获取 直播间父分区数据：{(parent_live_area_name4parent_live_area_id if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else '⚠️未登录账号'}")
    # 获取 登录账户 的 直播间父分区 对应的 直播间子分区数据
    sub_live_area_name4sub_live_area_id = (({str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in [AreaObj["list"] for AreaObj in area_obj_list["data"] if str(area["parent_area_id"]) == str(AreaObj["id"])][0]} if area else {"-1": "请选择一级分区"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """登录账户 的 直播间父分区 对应的 直播间子分区数据"""
    log_save(0, f"║║获取 登录账户 的 直播间父分区 对应的 直播间子分区数据：{(sub_live_area_name4sub_live_area_id if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else '⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播状态
    live_status = (room_info_old["liveStatus"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播状态】0：未开播 1：直播中"""
    log_save(0, f"║║登录账户 的 直播状态：{(('直播中' if live_status else '未开播') if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 登录用户的直播预约列表信息
    reserve_list = (b_a_m.get_reserve_list() if room_status else None) if b_u_l_c.get_cookies() else None
    """获取 '登录用户' 的 直播预约列表信息"""
    log_save(0, f"║║登录账户 的 直播预约列表信息：{(reserve_list if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 登录用户的直播预约字典
    reserve_name4reserve_sid = (({str(reserve['reserve_info']['sid']): f"{reserve['reserve_info']['name']}|{datetime.fromtimestamp(reserve['reserve_info']['live_plan_start_time'])}" for reserve in reserve_list} if reserve_list else {"-1": "无直播预约"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """获取 '登录用户' 的 直播预约字典"""
    log_save(0, f"║║登录账户 的 直播预约：{(list(reserve_name4reserve_sid.values()) if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")

    # 脚本后端属性
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║")
    log_save(0, f"║获取脚本后端属性")
    log_save(0, f"║╔{8*'═'}脚本后端属性{8*'═'}╗")
    # 记录obs推流状态
    GlobalVariableOfData.streaming_active = obs.obs_frontend_streaming_active()
    log_save(0, f"║║obs推流状态: {GlobalVariableOfData.streaming_active}")
    # obs脚本中控件的数据
    GlobalVariableOfData.script_settings = settings
    log_save(0, f"║║获取脚本属性集")
    log_save(0, f"║╚{8*'═'}脚本后端属性{8*'═'}╝")

    GlobalVariableOfData.widget_loading_number = 0
    w_list = [
        widget.Button.top,
        widget.Group.account,
            widget.TextBox.loginStatus,
            widget.ComboBox.uid,
            widget.Button.login,
            widget.Button.accountListUpdate,
            widget.Button.qrAddAccount,
            widget.Button.qrPictureDisplay,
            widget.Button.accountDelete,
            widget.Button.accountBackup,
            widget.Button.accountRestore,
            widget.Button.logout,
        widget.Group.room,
            widget.TextBox.roomStatus,
            widget.Button.roomOpened,
            widget.Button.roomCoverView,
            widget.PathBox.roomCover,
            widget.Button.roomCoverUpdate,
            widget.ComboBox.roomCommonTitles,
            widget.Button.roomCommonTitlesTrue,
            widget.TextBox.roomTitle,
            widget.Button.roomTitleChange,
            widget.TextBox.roomNews,
            widget.Button.roomNewsChange,
            widget.ComboBox.roomCommonAreas,
            widget.Button.roomCommonAreasTrue,
            widget.ComboBox.roomParentArea,
            widget.Button.roomParentAreaTrue,
            widget.ComboBox.roomSubArea,
            widget.Button.roomSubAreaTrue,
            widget.Button.bliveWebJump,
        widget.Group.live,
            widget.Button.liveFaceAuth,
            widget.ComboBox.liveStreamingPlatform,
            widget.Button.liveStart,
            widget.Button.liveRtmpAddressCopy,
            widget.Button.liveRtmpCodeCopy,
            widget.Button.liveRtmpCodeUpdate,
            widget.Button.liveStop,
            widget.DigitalDisplay.liveBookingsDay,
            widget.Button.liveBookingsDayTrue,
            widget.DigitalDisplay.liveBookingsHour,
            widget.Button.liveBookingsHourTrue,
            widget.DigitalDisplay.liveBookingsMinute,
            widget.Button.liveBookingsMinuteTrue,
            widget.CheckBox.liveBookingsDynamic,
            widget.TextBox.liveBookingsTitle,
            widget.Button.liveBookingsCreate,
            widget.ComboBox.liveBookings,
            widget.Button.liveBookingsCancel,
        widget.Button.bottom,
    ]

    for w in w_list:
        w.Number = (
            lambda v: (setattr(GlobalVariableOfData, 'widget_loading_number', v + 1), v)[1]
        )(GlobalVariableOfData.widget_loading_number)
    if len(w_list) == len(widget.get_sorted_controls()):
        pass
    else:
        log_save(3, "设定控件载入顺序时的控件数量 和 创建的控件对象数量 不统一")
        return False

    # 设置控件属性
    widget.Button.top.Name = "top_button"
    widget.Button.top.Description = "Top"
    widget.Button.top.Visible = False
    widget.Button.top.Enabled = False
    widget.Button.top.ModifiedIs = True
    widget.Button.top.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.top.Callback = lambda ps, p: button_function_test("顶部")

    # 分组框【账号】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    widget.Group.account.Name = "account_group"
    widget.Group.account.Description = "账号"
    widget.Group.account.Visible = True
    widget.Group.account.Enabled = True
    widget.Group.account.ModifiedIs = False
    widget.Group.account.Type = obs.OBS_GROUP_NORMAL

    widget.TextBox.loginStatus.Name = "login_status_textBox"
    widget.TextBox.loginStatus.Description = "登录状态"
    widget.TextBox.loginStatus.Visible = True
    widget.TextBox.loginStatus.Enabled = True
    widget.TextBox.loginStatus.ModifiedIs = True
    widget.TextBox.loginStatus.Type = obs.OBS_TEXT_INFO
    widget.TextBox.loginStatus.Text = f'{uname} 已登录' if b_u_l_c.get_cookies() else '未登录，请登录后点击【更新账号列表】'
    widget.TextBox.loginStatus.InfoType = obs.OBS_TEXT_INFO_NORMAL if b_u_l_c.get_cookies() else obs.OBS_TEXT_INFO_WARNING

    widget.ComboBox.uid.Name = "uid_comboBox"
    widget.ComboBox.uid.Description = "用户"
    widget.ComboBox.uid.Visible = True
    widget.ComboBox.uid.Enabled = True
    widget.ComboBox.uid.ModifiedIs = True
    widget.ComboBox.uid.Type = obs.OBS_COMBO_TYPE_LIST
    widget.ComboBox.uid.Text = uname if b_u_l_c.get_cookies() else '添加或选择一个账号登录'
    widget.ComboBox.uid.Value = b_u_l_c.get_users()[0] if b_u_l_c.get_cookies() else '-1'
    widget.ComboBox.uid.Dictionary = {uid or '-1': all_uname4uid.get(uid, '添加或选择一个账号登录') for uid in b_u_l_c.get_users().values()}

    widget.Button.login.Name = "login_button"
    widget.Button.login.Description = "登录账号"
    widget.Button.login.Visible = True if all_uname4uid else False
    widget.Button.login.Enabled = True if all_uname4uid else False
    widget.Button.login.ModifiedIs = False
    widget.Button.login.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.login.Callback = button_function_login

    widget.Button.accountListUpdate.Name = "account_list_update_button"
    widget.Button.accountListUpdate.Description = "更新账号列表"
    widget.Button.accountListUpdate.Visible = True
    widget.Button.accountListUpdate.Enabled = True
    widget.Button.accountListUpdate.ModifiedIs = False
    widget.Button.accountListUpdate.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.accountListUpdate.Callback = button_function_update_account_list

    widget.Button.qrAddAccount.Name = "qr_add_account_button"
    widget.Button.qrAddAccount.Description = "二维码添加账户"
    widget.Button.qrAddAccount.Visible = True
    widget.Button.qrAddAccount.Enabled = True
    widget.Button.qrAddAccount.ModifiedIs = False
    widget.Button.qrAddAccount.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.qrAddAccount.Callback = button_function_qr_add_account

    widget.Button.qrPictureDisplay.Name = "qr_picture_display_button"
    widget.Button.qrPictureDisplay.Description = "显示二维码图片"
    widget.Button.qrPictureDisplay.Visible = False
    widget.Button.qrPictureDisplay.Enabled = False
    widget.Button.qrPictureDisplay.ModifiedIs = False
    widget.Button.qrPictureDisplay.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.qrPictureDisplay.Callback = lambda ps, p: button_function_show_qr_picture()

    widget.Button.accountDelete.Name = "account_delete_button"
    widget.Button.accountDelete.Description = "删除账户"
    widget.Button.accountDelete.Visible = True if all_uname4uid else False
    widget.Button.accountDelete.Enabled = True if all_uname4uid else False
    widget.Button.accountDelete.ModifiedIs = False
    widget.Button.accountDelete.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.accountDelete.Callback = button_function_del_user

    widget.Button.accountBackup.Name = "account_backup_button"
    widget.Button.accountBackup.Description = "备份账户"
    widget.Button.accountBackup.Visible = False
    widget.Button.accountBackup.Enabled = False
    widget.Button.accountBackup.ModifiedIs = False
    widget.Button.accountBackup.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.accountBackup.Callback = button_function_backup_users

    widget.Button.accountRestore.Name = "account_restore_button"
    widget.Button.accountRestore.Description = "恢复账户"
    widget.Button.accountRestore.Visible = False
    widget.Button.accountRestore.Enabled = False
    widget.Button.accountRestore.ModifiedIs = False
    widget.Button.accountRestore.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.accountRestore.Callback = button_function_restore_user

    widget.Button.logout.Name = "logout_button"
    widget.Button.logout.Description = "登出账号"
    widget.Button.logout.Visible = True if b_u_l_c.get_cookies() else False
    widget.Button.logout.Enabled = True if b_u_l_c.get_cookies() else False
    widget.Button.logout.ModifiedIs = False
    widget.Button.logout.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.logout.Callback = button_function_logout


    # 分组框【直播间】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    widget.Group.room.Name = "room_group"
    widget.Group.room.Description = "直播间"
    widget.Group.room.Visible = True
    widget.Group.room.Enabled = True
    widget.Group.room.ModifiedIs = False
    widget.Group.room.Type = obs.OBS_GROUP_NORMAL

    widget.TextBox.roomStatus.Name = "room_status_textBox"
    widget.TextBox.roomStatus.Description = "查看直播间封面"
    widget.TextBox.roomStatus.Visible = True
    widget.TextBox.roomStatus.Enabled = True
    widget.TextBox.roomStatus.ModifiedIs = False
    widget.TextBox.roomStatus.Type = obs.OBS_TEXT_INFO
    widget.TextBox.roomStatus.Text = (f"{str(room_id)}{'直播中' if live_status else '未开播'}" if room_status else "无直播间") if b_u_l_c.get_cookies() else "未登录"
    widget.TextBox.roomStatus.InfoType = (obs.OBS_TEXT_INFO_NORMAL if bool(room_status) else obs.OBS_TEXT_INFO_WARNING) if b_u_l_c.get_cookies() else obs.OBS_TEXT_INFO_ERROR

    widget.Button.roomOpened.Name = "room_opened_button"
    widget.Button.roomOpened.Description = "开通直播间"
    widget.Button.roomOpened.Visible = (not bool(room_status)) if b_u_l_c.get_cookies() else False
    widget.Button.roomOpened.Enabled = (not bool(room_status)) if b_u_l_c.get_cookies() else False
    widget.Button.roomOpened.ModifiedIs = False
    widget.Button.roomOpened.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomOpened.Callback = button_function_opened_room

    widget.Button.roomCoverView.Name = "room_cover_view_button"
    widget.Button.roomCoverView.Description = "查看直播间封面"
    widget.Button.roomCoverView.Visible = bool(room_status)
    widget.Button.roomCoverView.Enabled = bool(room_status)
    widget.Button.roomCoverView.ModifiedIs = False
    widget.Button.roomCoverView.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomCoverView.Callback = button_function_check_room_cover

    widget.PathBox.roomCover.Name = "room_cover_fileDialogBox"
    widget.PathBox.roomCover.Description = "直播间封面"
    widget.PathBox.roomCover.Visible = bool(room_status)
    widget.PathBox.roomCover.Enabled = bool(room_status)
    widget.PathBox.roomCover.ModifiedIs = False
    widget.PathBox.roomCover.Type = obs.OBS_PATH_FILE
    widget.PathBox.roomCover.Text = ""
    widget.PathBox.roomCover.Filter = "图片(*.jpg *.jpeg *.png)"
    widget.PathBox.roomCover.StartPath = ""

    widget.Button.roomCoverUpdate.Name = "room_cover_update_button"
    widget.Button.roomCoverUpdate.Description = "上传直播间封面"
    widget.Button.roomCoverUpdate.Visible = False
    widget.Button.roomCoverUpdate.Enabled = False
    widget.Button.roomCoverUpdate.ModifiedIs = False
    widget.Button.roomCoverUpdate.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomCoverUpdate.Callback = lambda ps, p: button_function_update_room_cover()

    widget.ComboBox.roomCommonTitles.Name = "room_commonTitles_comboBox"
    widget.ComboBox.roomCommonTitles.Description = "常用标题"
    widget.ComboBox.roomCommonTitles.Visible = bool(room_status)
    widget.ComboBox.roomCommonTitles.Enabled = bool(room_status)
    widget.ComboBox.roomCommonTitles.ModifiedIs = True
    widget.ComboBox.roomCommonTitles.Type = obs.OBS_COMBO_TYPE_EDITABLE
    widget.ComboBox.roomCommonTitles.Text = room_title if bool(room_status) else ""
    widget.ComboBox.roomCommonTitles.Value = "0"
    widget.ComboBox.roomCommonTitles.Dictionary = common_title4number

    widget.Button.roomCommonTitlesTrue.Name = "room_commonTitles_true_button"
    widget.Button.roomCommonTitlesTrue.Description = "确认标题"
    widget.Button.roomCommonTitlesTrue.Visible = False
    widget.Button.roomCommonTitlesTrue.Enabled = False
    widget.Button.roomCommonTitlesTrue.ModifiedIs = False
    widget.Button.roomCommonTitlesTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomCommonTitlesTrue.Callback = lambda ps, p: button_function_true_live_room_title()

    widget.TextBox.roomTitle.Name = "room_title_textBox"
    widget.TextBox.roomTitle.Description = "直播间标题"
    widget.TextBox.roomTitle.Visible = bool(room_status)
    widget.TextBox.roomTitle.Enabled = bool(room_status)
    widget.TextBox.roomTitle.ModifiedIs = True
    widget.TextBox.roomTitle.Type = obs.OBS_TEXT_DEFAULT
    widget.TextBox.roomTitle.Text = room_title if bool(room_status) else ""

    widget.Button.roomTitleChange.Name = "room_title_change_button"
    widget.Button.roomTitleChange.Description = "更改直播间标题"
    widget.Button.roomTitleChange.Visible = bool(room_status)
    widget.Button.roomTitleChange.Enabled = bool(room_status)
    widget.Button.roomTitleChange.ModifiedIs = False
    widget.Button.roomTitleChange.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomTitleChange.Callback = lambda ps, p: button_function_change_live_room_title()

    widget.TextBox.roomNews.Name = "room_news_textBox"
    widget.TextBox.roomNews.Description = "直播间公告"
    widget.TextBox.roomNews.Visible = bool(room_status)
    widget.TextBox.roomNews.Enabled = bool(room_status)
    widget.TextBox.roomNews.ModifiedIs = True
    widget.TextBox.roomNews.Type = obs.OBS_TEXT_DEFAULT
    widget.TextBox.roomNews.Text = room_news if bool(room_status) else ""

    widget.Button.roomNewsChange.Name = "room_news_change_button"
    widget.Button.roomNewsChange.Description = "更改直播间公告"
    widget.Button.roomNewsChange.Visible = bool(room_status)
    widget.Button.roomNewsChange.Enabled = bool(room_status)
    widget.Button.roomNewsChange.ModifiedIs = False
    widget.Button.roomNewsChange.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomNewsChange.Callback = lambda ps, p: button_function_change_live_room_news()

    widget.ComboBox.roomCommonAreas.Name = "room_commonAreas_comboBox"
    widget.ComboBox.roomCommonAreas.Description = "常用分区"
    widget.ComboBox.roomCommonAreas.Visible = bool(room_status)
    widget.ComboBox.roomCommonAreas.Enabled = bool(room_status)
    widget.ComboBox.roomCommonAreas.ModifiedIs = True
    widget.ComboBox.roomCommonAreas.Type = obs.OBS_COMBO_TYPE_LIST
    widget.ComboBox.roomCommonAreas.Text = common_area_id_dict_str4common_area_name_dict_str[json.dumps({area["parent_area_id"]: str(area["area_id"])})] if common_areas else "无常用分区"
    widget.ComboBox.roomCommonAreas.Value = json.dumps({area["parent_area_id"]: str(area["area_id"])}, ensure_ascii=False) if common_areas else "-1"
    widget.ComboBox.roomCommonAreas.Dictionary = common_area_id_dict_str4common_area_name_dict_str

    widget.Button.roomCommonAreasTrue.Name = "room_commonAreas_true_button"
    widget.Button.roomCommonAreasTrue.Description = "确认分区"
    widget.Button.roomCommonAreasTrue.Visible = False
    widget.Button.roomCommonAreasTrue.Enabled = False
    widget.Button.roomCommonAreasTrue.ModifiedIs = False
    widget.Button.roomCommonAreasTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomCommonAreasTrue.Callback = lambda ps, p: button_function_true_live_room_area()

    widget.ComboBox.roomParentArea.Name = "room_parentArea_comboBox"
    widget.ComboBox.roomParentArea.Description = "一级分区"
    widget.ComboBox.roomParentArea.Visible = bool(room_status)
    widget.ComboBox.roomParentArea.Enabled = bool(room_status)
    widget.ComboBox.roomParentArea.ModifiedIs = True
    widget.ComboBox.roomParentArea.Type = obs.OBS_COMBO_TYPE_LIST
    widget.ComboBox.roomParentArea.Text = str(area["parent_area_name"]) if bool(area) else "请选择一级分区"
    widget.ComboBox.roomParentArea.Value = str(area["parent_area_id"]) if bool(area) else "-1"
    widget.ComboBox.roomParentArea.Dictionary = parent_live_area_name4parent_live_area_id

    widget.Button.roomParentAreaTrue.Name = "room_parentArea_true_button"
    widget.Button.roomParentAreaTrue.Description = "确认一级分区"
    widget.Button.roomParentAreaTrue.Visible = False
    widget.Button.roomParentAreaTrue.Enabled = False
    widget.Button.roomParentAreaTrue.ModifiedIs = False
    widget.Button.roomParentAreaTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomParentAreaTrue.Callback = lambda ps, p: button_function_start_parent_area()

    widget.ComboBox.roomSubArea.Name = "room_subArea_comboBox"
    widget.ComboBox.roomSubArea.Description = "二级分区"
    widget.ComboBox.roomSubArea.Visible = bool(room_status)
    widget.ComboBox.roomSubArea.Enabled = bool(room_status)
    widget.ComboBox.roomSubArea.ModifiedIs = True
    widget.ComboBox.roomSubArea.Type = obs.OBS_COMBO_TYPE_LIST
    widget.ComboBox.roomSubArea.Text = str(area["area_name"]) if bool(area) else "请确认一级分区"
    widget.ComboBox.roomSubArea.Value = str(area["area_id"]) if bool(area) else "-1"
    widget.ComboBox.roomSubArea.Dictionary = sub_live_area_name4sub_live_area_id

    widget.Button.roomSubAreaTrue.Name = "room_subArea_true_button"
    widget.Button.roomSubAreaTrue.Description = "「确认分区」"
    widget.Button.roomSubAreaTrue.Visible = bool(room_status)
    widget.Button.roomSubAreaTrue.Enabled = bool(room_status)
    widget.Button.roomSubAreaTrue.ModifiedIs = False
    widget.Button.roomSubAreaTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.roomSubAreaTrue.Callback = lambda ps, p: button_function_start_sub_area()

    widget.Button.bliveWebJump.Name = "blive_web_jump_button"
    widget.Button.bliveWebJump.Description = "跳转直播间后台网页"
    widget.Button.bliveWebJump.Visible = True if b_u_l_c.get_cookies() else False
    widget.Button.bliveWebJump.Enabled = True if b_u_l_c.get_cookies() else False
    widget.Button.bliveWebJump.ModifiedIs = False
    widget.Button.bliveWebJump.Type = obs.OBS_BUTTON_URL
    widget.Button.bliveWebJump.Callback = button_function_jump_blive_web
    widget.Button.bliveWebJump.Url = "https://link.bilibili.com/p/center/index#/my-room/start-live"


    # 分组框【直播】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    widget.Group.live.Name = "live_group"
    widget.Group.live.Description = "直播"
    widget.Group.live.Visible = bool(room_status)
    widget.Group.live.Enabled = bool(room_status)
    widget.Group.live.ModifiedIs = False
    widget.Group.live.Type = obs.OBS_GROUP_NORMAL

    widget.Button.liveFaceAuth.Name = "live_face_auth_button"
    widget.Button.liveFaceAuth.Description = "人脸认证"
    widget.Button.liveFaceAuth.Visible = bool(room_status)
    widget.Button.liveFaceAuth.Enabled = bool(room_status)
    widget.Button.liveFaceAuth.ModifiedIs = False
    widget.Button.liveFaceAuth.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveFaceAuth.Callback = lambda ps, p: button_function_face_auth()

    widget.ComboBox.liveStreamingPlatform.Name = "live_streaming_platform_comboBox"
    widget.ComboBox.liveStreamingPlatform.Description = "直播平台"
    widget.ComboBox.liveStreamingPlatform.Visible = bool(room_status)
    widget.ComboBox.liveStreamingPlatform.Enabled = bool(room_status)
    widget.ComboBox.liveStreamingPlatform.ModifiedIs = True
    widget.ComboBox.liveStreamingPlatform.Type = obs.OBS_COMBO_TYPE_LIST
    widget.ComboBox.liveStreamingPlatform.Text = ""
    widget.ComboBox.liveStreamingPlatform.Value = ""
    widget.ComboBox.liveStreamingPlatform.Dictionary = {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}

    widget.Button.liveStart.Name = "live_start_button"
    widget.Button.liveStart.Description = "开始直播并复制推流码"
    widget.Button.liveStart.Visible = True if ((not live_status) and room_status) else False
    widget.Button.liveStart.Enabled = True if ((not live_status) and room_status) else False
    widget.Button.liveStart.ModifiedIs = False
    widget.Button.liveStart.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveStart.Callback = lambda ps, p: button_function_start_live()

    widget.Button.liveRtmpAddressCopy.Name = "live_rtmp_address_copy_button"
    widget.Button.liveRtmpAddressCopy.Description = "复制直播服务器"
    widget.Button.liveRtmpAddressCopy.Visible = True if (live_status and room_status) else False
    widget.Button.liveRtmpAddressCopy.Enabled = True if (live_status and room_status) else False
    widget.Button.liveRtmpAddressCopy.ModifiedIs = False
    widget.Button.liveRtmpAddressCopy.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveRtmpAddressCopy.Callback = button_function_rtmp_address_copy

    widget.Button.liveRtmpCodeCopy.Name = "live_rtmp_code_copy_button"
    widget.Button.liveRtmpCodeCopy.Description = "复制直播推流码"
    widget.Button.liveRtmpCodeCopy.Visible = True if (live_status and room_status) else False
    widget.Button.liveRtmpCodeCopy.Enabled = True if (live_status and room_status) else False
    widget.Button.liveRtmpCodeCopy.ModifiedIs = False
    widget.Button.liveRtmpCodeCopy.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveRtmpCodeCopy.Callback = button_function_rtmp_stream_code_copy

    widget.Button.liveRtmpCodeUpdate.Name = "live_rtmp_code_update_button"
    widget.Button.liveRtmpCodeUpdate.Description = "更新推流码并复制"
    widget.Button.liveRtmpCodeUpdate.Visible = True if (live_status and room_status) else False
    widget.Button.liveRtmpCodeUpdate.Enabled = True if (live_status and room_status) else False
    widget.Button.liveRtmpCodeUpdate.ModifiedIs = False
    widget.Button.liveRtmpCodeUpdate.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveRtmpCodeUpdate.Callback = button_function_rtmp_stream_code_update

    widget.Button.liveStop.Name = "live_stop_button"
    widget.Button.liveStop.Description = "结束直播"
    widget.Button.liveStop.Visible = True if (live_status and room_status) else False
    widget.Button.liveStop.Enabled = True if (live_status and room_status) else False
    widget.Button.liveStop.ModifiedIs = False
    widget.Button.liveStop.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveStop.Callback = lambda ps, p: button_function_stop_live()

    widget.DigitalDisplay.liveBookingsDay.Name = "live_bookings_day_digitalSlider"
    widget.DigitalDisplay.liveBookingsDay.Description = "预约天"
    widget.DigitalDisplay.liveBookingsDay.Visible = bool(room_status)
    widget.DigitalDisplay.liveBookingsDay.Enabled = bool(room_status)
    widget.DigitalDisplay.liveBookingsDay.ModifiedIs = True
    widget.DigitalDisplay.liveBookingsDay.SliderIs = True
    widget.DigitalDisplay.liveBookingsDay.Value = 0
    widget.DigitalDisplay.liveBookingsDay.Suffix = "天"
    widget.DigitalDisplay.liveBookingsDay.Min = 0
    widget.DigitalDisplay.liveBookingsDay.Max = 180
    widget.DigitalDisplay.liveBookingsDay.Step = 1

    widget.Button.liveBookingsDayTrue.Name = "live_bookings_day_true_button"
    widget.Button.liveBookingsDayTrue.Description = "确认预约天"
    widget.Button.liveBookingsDayTrue.Visible = False
    widget.Button.liveBookingsDayTrue.Enabled = False
    widget.Button.liveBookingsDayTrue.ModifiedIs = False
    widget.Button.liveBookingsDayTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveBookingsDayTrue.Callback = lambda ps, p: button_function_true_live_appointment_day()

    widget.DigitalDisplay.liveBookingsHour.Name = "live_bookings_hour_digitalSlider"
    widget.DigitalDisplay.liveBookingsHour.Description = "预约时"
    widget.DigitalDisplay.liveBookingsHour.Visible = bool(room_status)
    widget.DigitalDisplay.liveBookingsHour.Enabled = bool(room_status)
    widget.DigitalDisplay.liveBookingsHour.ModifiedIs = True
    widget.DigitalDisplay.liveBookingsHour.SliderIs = True
    widget.DigitalDisplay.liveBookingsHour.Value = 0
    widget.DigitalDisplay.liveBookingsHour.Suffix = "时"
    widget.DigitalDisplay.liveBookingsHour.Min = 0
    widget.DigitalDisplay.liveBookingsHour.Max = 23
    widget.DigitalDisplay.liveBookingsHour.Step = 1

    widget.Button.liveBookingsHourTrue.Name = "live_bookings_hour_true_button"
    widget.Button.liveBookingsHourTrue.Description = "确认预约时"
    widget.Button.liveBookingsHourTrue.Visible = False
    widget.Button.liveBookingsHourTrue.Enabled = False
    widget.Button.liveBookingsHourTrue.ModifiedIs = False
    widget.Button.liveBookingsHourTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveBookingsHourTrue.Callback = lambda ps, p: button_function_test("确认预约时")

    widget.DigitalDisplay.liveBookingsMinute.Name = "live_bookings_minute_digitalSlider"
    widget.DigitalDisplay.liveBookingsMinute.Description = "预约分"
    widget.DigitalDisplay.liveBookingsMinute.Visible = bool(room_status)
    widget.DigitalDisplay.liveBookingsMinute.Enabled = bool(room_status)
    widget.DigitalDisplay.liveBookingsMinute.ModifiedIs = True
    widget.DigitalDisplay.liveBookingsMinute.SliderIs = True
    widget.DigitalDisplay.liveBookingsMinute.Value = 0
    widget.DigitalDisplay.liveBookingsMinute.Suffix = "分"
    widget.DigitalDisplay.liveBookingsMinute.Min = 5
    widget.DigitalDisplay.liveBookingsMinute.Max = 59
    widget.DigitalDisplay.liveBookingsMinute.Step = 1

    widget.Button.liveBookingsMinuteTrue.Name = "live_bookings_minute_true_button"
    widget.Button.liveBookingsMinuteTrue.Description = "确认预约分"
    widget.Button.liveBookingsMinuteTrue.Visible = False
    widget.Button.liveBookingsMinuteTrue.Enabled = False
    widget.Button.liveBookingsMinuteTrue.ModifiedIs = False
    widget.Button.liveBookingsMinuteTrue.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveBookingsMinuteTrue.Callback = lambda ps, p: button_function_test("确认预约分")

    widget.CheckBox.liveBookingsDynamic.Name = "live_bookings_dynamic_checkBox"
    widget.CheckBox.liveBookingsDynamic.Description = "是否发直播预约动态"
    widget.CheckBox.liveBookingsDynamic.Visible = bool(room_status)
    widget.CheckBox.liveBookingsDynamic.Enabled = bool(room_status)
    widget.CheckBox.liveBookingsDynamic.ModifiedIs = True
    widget.CheckBox.liveBookingsDynamic.Bool = False

    widget.TextBox.liveBookingsTitle.Name = "live_bookings_title_textBox"
    widget.TextBox.liveBookingsTitle.Description = "直播预约标题"
    widget.TextBox.liveBookingsTitle.Visible = bool(room_status)
    widget.TextBox.liveBookingsTitle.Enabled = bool(room_status)
    widget.TextBox.liveBookingsTitle.ModifiedIs = True
    widget.TextBox.liveBookingsTitle.Type = obs.OBS_TEXT_DEFAULT
    widget.TextBox.liveBookingsTitle.Text = ""

    widget.Button.liveBookingsCreate.Name = "live_bookings_create_button"
    widget.Button.liveBookingsCreate.Description = "发布直播预约"
    widget.Button.liveBookingsCreate.Visible = bool(room_status)
    widget.Button.liveBookingsCreate.Enabled = bool(room_status)
    widget.Button.liveBookingsCreate.ModifiedIs = False
    widget.Button.liveBookingsCreate.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveBookingsCreate.Callback = button_function_creat_live_appointment

    widget.ComboBox.liveBookings.Name = "live_bookings_comboBox"
    widget.ComboBox.liveBookings.Description = "直播预约列表"
    widget.ComboBox.liveBookings.Visible = bool(room_status)
    widget.ComboBox.liveBookings.Enabled = bool(room_status)
    widget.ComboBox.liveBookings.ModifiedIs = True
    widget.ComboBox.liveBookings.Type = obs.OBS_COMBO_TYPE_LIST
    widget.ComboBox.liveBookings.Text = ""
    widget.ComboBox.liveBookings.Value = ""
    widget.ComboBox.liveBookings.Dictionary = reserve_name4reserve_sid

    widget.Button.liveBookingsCancel.Name = "live_bookings_cancel_button"
    widget.Button.liveBookingsCancel.Description = "取消直播预约"
    widget.Button.liveBookingsCancel.Visible = bool(room_status)
    widget.Button.liveBookingsCancel.Enabled = bool(room_status)
    widget.Button.liveBookingsCancel.ModifiedIs = False
    widget.Button.liveBookingsCancel.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.liveBookingsCancel.Callback = button_function_cancel_live_appointment

    widget.Button.bottom.Name = "bottom_button"
    widget.Button.bottom.Description = "Bottom"
    widget.Button.bottom.Visible = False
    widget.Button.bottom.Enabled = False
    widget.Button.bottom.ModifiedIs = True
    widget.Button.bottom.Type = obs.OBS_BUTTON_DEFAULT
    widget.Button.bottom.Callback = lambda ps, p: button_function_test("底部")

    return True


# --- 一个名为script_description的函数返回显示给的描述
def script_description():
    """
    调用以检索要在“脚本”窗口中显示给用户的描述字符串。
    """
    if not GlobalVariableOfData.networkConnectionStatus:
        return "<font color=yellow>网络不可用</font>"
    t = ('<html lang="zh-CN"><body><pre>\
<font color=yellow>!脚本路径中尽量不要有中文</font><br>\
<font color="white" size=5>⟳</font><font color=green size=4>为重新载入插件按钮</font><br>\
使用<font color="#ee4343">管理员权限</font>运行obs<br>\
其它问题请前往<a href="https://github.com/lanyangyin/OBSscripts-bilibili-live/issues">Github</a>或者<a href="https://message.bilibili.com/#/whisper/mid143474500">B站</a>提问\
</pre></body></html>')
    return t


# --- 一个名为script_load的函数将在启动时调用
def script_load(settings):
    """
    在脚本启动时调用与脚本相关的特定设置。所提供的设置参数通常不用于由用户设置的设置;
    相反，该参数用于脚本中可能使用的任何额外的内部设置数据。
    :param settings:与脚本关联的设置。
    """
    log_save(0, "╔══已载入: bilibili_live══╗")
    log_save(0, "║  已载入: bilibili_live  ║")
    log_save(0, "╚══已载入: bilibili_live══╝")
    # 注册事件回调
    log_save(0, "┌──开始监视obs事件──┐")
    log_save(0, "│  开始监视obs事件  │")
    log_save(0, "└──开始监视obs事件──┘")
    obs.obs_frontend_add_event_callback(trigger_frontend_event)
    # obs_data_t 类型的数据对象。这个数据对象可以用来存储和管理设置项，例如场景、源或过滤器的配置信息
    # settings = obs.obs_data_create()


# 控件状态更新时调用
def script_update(settings):
    """
    当用户更改了脚本的设置(如果有的话)时调用。
    这里更改控件属性不会实时显示，
    不要在这里控制控件的【可见】、【可用】、【值】和【名称】
    :param settings:与脚本关联的设置。
    """
    # log_save(0, "╔════监测到控件数据变动════╗")
    # log_save(0, "║    监测到控件数据变动    ║")
    # log_save(0, "╚════监测到控件数据变动════╝")
    return True


# --- 一个名为script_properties的函数定义了用户可以使用的属性
def script_properties():  # 建立控件
    """
    建立控件
    调用以定义与脚本关联的用户属性。这些属性用于定义如何向用户显示设置属性。
    通常用于自动生成用户界面小部件，也可以用来枚举特定设置的可用值或有效值。
    Returns:通过 obs_properties_create() 创建的 Obs_properties_t 对象
    obs_properties_t 类型的属性对象。这个属性对象通常用于枚举 libobs 对象的可用设置，
    """
    log_save(0, f"")
    log_save(0, f"╔{'═' * 20}调用内置函数script_properties调整脚本控件{'═' * 20}╗")
    log_save(0, f"║{' ' * 20}调用内置函数script_properties调整脚本控件{' ' * 20}║")
    # 网络连通
    if not GlobalVariableOfData.networkConnectionStatus:
        return None
    # 创建一个 OBS 属性集对象，他将包含所有控件对应的属性对象
    props = obs.obs_properties_create()
    # 为 分组框【配置】 建立属性集
    account_props = obs.obs_properties_create()
    # 为 分组框【直播间】 建立属性集
    room_props = obs.obs_properties_create()
    # 为 分组框【直播】 建立属性集
    live_props = obs.obs_properties_create()

    props_dict = {
        "props": props,
        "account_props": account_props,
        "room_props": room_props,
        "live_props": live_props,
    }

    for w in widget.get_sorted_controls():
        if w.ControlType == "CheckBox":
            log_save(0, f"复选框控件: {w.Name} 【{w.Description}】")
            obs.obs_properties_add_bool(props_dict[w.Props], w.Name, w.Description)
        elif w.ControlType == "DigitalDisplay":
            log_save(0, f"数字框控件: {w.Name} 【{w.Description}】")
            if w.SliderIs:
                w.Obj = obs.obs_properties_add_int_slider(props_dict[w.Props], w.Name, w.Description, w.Min, w.Max, w.Step)
            else:
                w.Obj = obs.obs_properties_add_int(props_dict[w.Props], w.Name, w.Description, w.Min, w.Max, w.Step)
            obs.obs_property_int_set_suffix(w.Obj, w.Suffix)
        elif w.ControlType == "TextBox":
            log_save(0, f"文本框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_text(props_dict[w.Props], w.Name, w.Description, w.Type)
        elif w.ControlType == "Button":
            log_save(0, f"按钮控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_button(props_dict[w.Props], w.Name, w.Description, w.Callback)
            obs.obs_property_button_set_type(w.Obj, w.Type)
            if w.Type == obs.OBS_BUTTON_URL:
                obs.obs_property_button_set_url(w.Obj, w.Url)
        elif w.ControlType == "ComboBox":
            log_save(0, f"组合框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_list(props_dict[w.Props], w.Name, w.Description, w.Type, obs.OBS_COMBO_FORMAT_STRING)
        elif w.ControlType == "PathBox":
            log_save(0, f"路径对话框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_path(props_dict[w.Props], w.Name, w.Description, w.Type, w.Filter, w.StartPath)
        elif w.ControlType == "Group":
            log_save(0, f"分组框控件: {w.Name} 【{w.Description}】")
            w.Obj = obs.obs_properties_add_group(props_dict[w.Props], w.Name, w.Description, w.Type, props_dict[w.GroupProps])
        if w.ModifiedIs:
            obs.obs_property_set_modified_callback(w.Obj, lambda ps, p, st, name=w.Name: property_modified(name))
    # 更新UI界面数据#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
    update_ui_interface_data(is_script_properties=True)
    log_save(0, f"║{' ' * 20}调用内置函数script_properties调整脚本控件{' ' * 20}║")
    log_save(0, f"╚{'═' * 20}调用内置函数script_properties调整脚本控件{'═' * 20}╝")
    log_save(0, f"")
    return props


def update_ui_interface_data(is_script_properties=False):
    """
    更新UI界面数据
    Returns:
    """
    for w in widget.get_sorted_controls():
        if obs.obs_property_visible(w.Obj) != w.Visible:
            obs.obs_property_set_visible(w.Obj, w.Visible)
        if obs.obs_property_enabled(w.Obj) != w.Enabled:
            obs.obs_property_set_enabled(w.Obj, w.Enabled)
        if w.ControlType == "CheckBox":
            if obs.obs_data_get_bool(GlobalVariableOfData.script_settings, w.Name) != w.Bool:
                obs.obs_data_set_bool(GlobalVariableOfData.script_settings, w.Name, w.Bool)
        elif w.ControlType == "DigitalDisplay":
            if w.Min != obs.obs_property_int_min(w.Obj) or w.Max != obs.obs_property_int_max(w.Obj) or w.Step != obs.obs_property_int_step(w.Obj):
                obs.obs_property_int_set_limits(w.Obj, w.Min, w.Max, w.Step)
            if obs.obs_data_get_int(GlobalVariableOfData.script_settings, w.Name) != w.Value:
                obs.obs_data_set_int(GlobalVariableOfData.script_settings, w.Name, w.Value)
        elif w.ControlType == "TextBox":
            if w.Type == obs.OBS_TEXT_INFO:
                if obs.obs_property_text_info_type(w.Obj) != w.InfoType:
                    obs.obs_property_text_set_info_type(w.Obj, w.InfoType)
            if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Text:
                obs.obs_data_set_string(GlobalVariableOfData.script_settings, w.Name, w.Text)
        elif w.ControlType == "Button":
            pass
        elif w.ControlType == "ComboBox":
            if w.Dictionary != {obs.obs_property_list_item_string(w.Obj, idx): obs.obs_property_list_item_name(w.Obj, idx) for idx in range(obs.obs_property_list_item_count(w.Obj))}:
                obs.obs_property_list_clear(w.Obj)
                for common_area_id_dict_str in w.Dictionary:
                    obs.obs_property_list_add_string(w.Obj, w.Dictionary[common_area_id_dict_str], common_area_id_dict_str) if common_area_id_dict_str != w.Value else obs.obs_property_list_insert_string(w.Obj, 0, w.Text, w.Value)
            if w.Type == obs.OBS_COMBO_TYPE_EDITABLE:
                if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Text:
                    obs.obs_data_set_string(GlobalVariableOfData.script_settings, w.Name, obs.obs_property_list_item_name(w.Obj, 0))
            else:
                if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Value:
                    obs.obs_data_set_string(GlobalVariableOfData.script_settings, w.Name, obs.obs_property_list_item_string(w.Obj, 0))
        elif w.ControlType == "PathBox":
            if obs.obs_data_get_string(GlobalVariableOfData.script_settings, w.Name) != w.Text:
                obs.obs_data_set_string(GlobalVariableOfData.script_settings, w.Name, w.Text)
        elif w.ControlType == "Group":
            pass
    return True


def button_function_login(props, prop):
    """
    登录并刷新控件状态
    Args:
        props:
        prop:
    Returns:
    """
    # ＝＝＝＝＝＝＝＝＝＝＝
    # ＝     登录      ＝
    # ＝＝＝＝＝＝＝＝＝＝＝
    uid = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'uid_comboBox')
    if uid in ["-1"]:
        log_save(2, "请添加或选择一个账号登录")
        return False
    log_save(0, f"即将登录的账号：{uid}")
    log_save(0, f"将选定的账号：{uid}，在配置文件中转移到默认账号的位置")
    try:
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
        uid = str(uid)
        log_save(0, f"尝试登录用户: {uid}")
        b_u_l_c.update_user(b_u_l_c.get_cookies(int(uid)))
        log_save(0, f"用户 {uid} 登录成功")
    except ValueError as e:
        log_save(3, f"参数错误: {str(e)}")
        raise
    except Exception as e:
        log_save(2, f"登录过程异常: {str(e)}")
        raise RuntimeError("登录服务暂时不可用") from e
    # ＝＝＝＝＝＝＝＝＝＝＝
    # ＝     更新      ＝
    # ＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    log_save(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfData.script_settings)
    # 更新脚本用户小部件
    log_save(0, f"更新控件UI")
    update_ui_interface_data()
    return True


def button_function_update_account_list(props=None, prop=None, settings=GlobalVariableOfData.script_settings):
    """
    更新账号列表
    Args:
        settings:
        props:
        prop:

    Returns:
    """
    # 调整控件数据
    # 设置控件前准备（获取数据） 开始
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
    user_interface_nav4uid = {uid: BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies(int(uid))), ).get_nav_info() for uid in [x for x in b_u_l_c.get_users().values() if x]}
    # 获取 用户配置文件 中 每一个 用户 的 昵称
    all_uname4uid = {uid: user_interface_nav4uid[uid]["uname"] for uid in user_interface_nav4uid}
    # 获取 '登录用户' 的昵称
    uname = all_uname4uid[b_u_l_c.get_users()[0]] if b_u_l_c.get_cookies() else None

    # 设置控件前准备（获取数据）结束
    # 设置 分组框【账号】 可见状态
    widget.Group.account.Visible = True
    # 设置 分组框【账号】 可用状态
    widget.Group.account.Enabled = True
    # 设置 只读文本框【登录状态】 可见状态
    widget.TextBox.loginStatus.Visible = True
    # 设置 只读文本框【登录状态】 可用状态
    widget.TextBox.loginStatus.Enabled = True
    # 设置 只读文本框【登录状态】 信息类型
    widget.TextBox.loginStatus.Type = obs.OBS_TEXT_INFO_NORMAL if b_u_l_c.get_cookies() else obs.OBS_TEXT_INFO_WARNING
    # 设置 只读文本框【登录状态】 内容
    widget.TextBox.loginStatus.Text = f'{uname} 已登录' if b_u_l_c.get_cookies() else '未登录，请登录后点击【更新账号列表】'
    # 设置 组合框【用户】 可见状态
    widget.ComboBox.uid.Visible = True
    # 设置 组合框【用户】 可用状态
    widget.ComboBox.uid.Enabled = True
    # 设置 组合框【用户】 的数据字典
    widget.ComboBox.uid.Dictionary = {uid or '-1': all_uname4uid.get(uid, '添加或选择一个账号登录') for uid in b_u_l_c.get_users().values()}
    # 设置 组合框【用户】 默认显示内容
    widget.ComboBox.uid.Obj_string = uname if b_u_l_c.get_cookies() else '添加或选择一个账号登录'
    # 设置 组合框【用户】 默认显示内容 的 列表值
    widget.ComboBox.uid.Value = b_u_l_c.get_users()[0] if b_u_l_c.get_cookies() else '-1'
    # 设置 按钮【登录账号】 可见状态
    widget.Button.login.Visible = True if all_uname4uid else False
    # 设置 按钮【登录账号】 可用状态
    widget.Button.login.Enabled = True if all_uname4uid else False
    # 设置 按钮【更新账号列表】 可见状态
    widget.Button.accountListUpdate.Visible = True
    # 设置 按钮【更新账号列表】 可用状态
    widget.Button.accountListUpdate.Enabled = True
    # 设置 按钮【二维码添加账户】 可见状态
    widget.Button.qrAddAccount.Visible = True
    # 设置 按钮【二维码添加账户】 可用状态
    widget.Button.qrAddAccount.Enabled = True
    # 设置 按钮【显示二维码图片】 可见状态
    widget.Button.qrPictureDisplay.Visible = False
    # 设置 按钮【显示二维码图片】 可用状态
    widget.Button.qrPictureDisplay.Enabled = False
    # 设置 按钮【删除账户】 可见状态
    widget.Button.accountDelete.Visible = True if all_uname4uid else False
    # 设置 按钮【删除账户】 可用状态
    widget.Button.accountDelete.Enabled = True if all_uname4uid else False
    # 设置 按钮【备份账户】 可见状态
    widget.Button.accountBackup.Visible = False
    # 设置 按钮【备份账户】 可用状态
    widget.Button.accountBackup.Enabled = False
    # 设置 按钮【恢复账户】 可见状态
    widget.Button.accountRestore.Visible = False
    # 设置 按钮【恢复账户】 可用状态
    widget.Button.accountRestore.Enabled = False
    # 设置 按钮【登出账号】 可见状态
    widget.Button.logout.Visible = True if all_uname4uid and b_u_l_c.get_cookies() else False
    # 设置 按钮【登出账号】 可用状态
    widget.Button.logout.Enabled = True if all_uname4uid and b_u_l_c.get_cookies() else False

    # 更新UI界面数据
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 只读文本框++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐只读文本框 UI{30*'─'}┐")
    # 【账号】分组————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【账号】")
    # 只读文本框【登录状态】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️只读文本框【登录状态】 UI")
    # 设置 只读文本框【登录状态】 可见状态
    if obs.obs_property_visible(widget.TextBox.loginStatus.Obj) != widget.TextBox.loginStatus.Visible:
        log_save(0, f"　│││✏️ 只读文本框【登录状态】 可见状态 发生变动: {obs.obs_property_visible(widget.TextBox.loginStatus.Obj)}➡️{widget.TextBox.loginStatus.Visible}")
        obs.obs_property_set_visible(widget.TextBox.loginStatus.Obj, widget.TextBox.loginStatus.Visible)
    else:
        log_save(0, f"　│││🧩 只读文本框【登录状态】 可见状态 未 发生变动")
    # 设置 只读文本框【登录状态】 可用状态
    if obs.obs_property_enabled(widget.TextBox.loginStatus.Obj) != widget.TextBox.loginStatus.Enabled:
        log_save(0, f"　│││✏️ 只读文本框【登录状态】 可用状态 发生变动: {obs.obs_property_enabled(widget.TextBox.loginStatus.Obj)}➡️{widget.TextBox.loginStatus.Enabled}")
        obs.obs_property_set_enabled(widget.TextBox.loginStatus.Obj, widget.TextBox.loginStatus.Enabled)
    else:
        log_save(0, f"　│││🧩 只读文本框【登录状态】 可用状态 未 发生变动")
    # 设置 只读文本框【登录状态】 信息类型
    if obs.obs_property_text_info_type(widget.TextBox.loginStatus.Obj) != widget.TextBox.loginStatus.Type:
        log_save(0, f"　│││✏️ 只读文本框【登录状态】 信息类型 发生变动: {textBox_type_name4textBox_type[obs.obs_property_text_info_type(widget.TextBox.loginStatus.Obj)]}➡️{textBox_type_name4textBox_type[widget.TextBox.loginStatus.Type]}")
        obs.obs_property_text_set_info_type(widget.TextBox.loginStatus.Obj, widget.TextBox.loginStatus.Type)
    else:
        log_save(0, f"　│││🧩 只读文本框【登录状态】 信息类型 未 发生变动")
    # 设置 只读文本框【登录状态】 文本
    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'login_status_textBox') != widget.TextBox.loginStatus.Text:
        log_save(0, f"　│││✏️ 只读文本框【登录状态】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'login_status_textBox')}➡️{widget.TextBox.loginStatus.Text}")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'login_status_textBox', f'{widget.TextBox.loginStatus.Text}')
    else:
        log_save(0, f"　│││🧩 只读文本框【登录状态】 文本 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌只读文本框 UI{30*'─'}┘")

    # 组合框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐组合框 UI{30*'─'}┐")
    # 【账号】分组————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【账号】")
    # 组合框【用户】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【用户】 UI")
    # 设置 组合框【用户】 可见状态
    if obs.obs_property_visible(widget.ComboBox.uid.Obj) != widget.ComboBox.uid.Visible:
        log_save(0, f"　│││✏️ 组合框【用户】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.uid.Obj)}➡️{widget.ComboBox.uid.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.uid.Obj, widget.ComboBox.uid.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【用户】 可见状态 未 发生变动")
    # 设置 组合框【用户】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.uid.Obj) != widget.ComboBox.uid.Enabled:
        log_save(0, f"　│││✏️ 组合框【用户】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.uid.Obj)}➡️{widget.ComboBox.uid.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.uid.Obj, widget.ComboBox.uid.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【用户】 可用状态 未 发生变动")
    # 判断 组合框【用户】字典数据 和 当前数据是否有变化
    if widget.ComboBox.uid.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.uid.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.uid.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.uid.Obj))}:
        log_save(0, f"　│││✏️ 组合框【用户】 列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.uid.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.uid.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.uid.Obj))})}个元素➡️{len(widget.ComboBox.uid.Dictionary)}个元素")
        # 清空 组合框【用户】
        log_save(0, f"　│││📑 更新 组合框【用户】数据 第一步：清空 组合框【用户】")
        obs.obs_property_list_clear(widget.ComboBox.uid.Obj)
        # 添加 组合框【用户】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑  更新 组合框【用户】数据 第二步：添加 组合框【用户】 列表选项  如果有默认值，会被设置在第一位")
        for uid in widget.ComboBox.uid.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.uid.Obj, widget.ComboBox.uid.Dictionary[uid], uid) if uid != widget.ComboBox.uid.Value else obs.obs_property_list_insert_string(widget.ComboBox.uid.Obj, 0, widget.ComboBox.uid.Obj_string, widget.ComboBox.uid.Value)
        # 设置 组合框【用户】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【用户】数据 第三步：更新 组合框【用户】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'uid_comboBox', obs.obs_property_list_item_string(widget.ComboBox.uid.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【用户】 列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌组合框 UI{30*'─'}┘")

    # 按钮+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐按钮 UI{30*'─'}┐")
    # 【账号】分组————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【账号】")
    # 按钮【登录账号】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【登录账号】 UI")
    # 设置 按钮【登录账号】 可见状态
    if obs.obs_property_visible(widget.Button.login.Obj) != widget.Button.login.Visible:
        log_save(0, f"　│││✏️ 按钮【登录账号】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.login.Obj)}➡️{widget.Button.login.Visible}")
        obs.obs_property_set_visible(widget.Button.login.Obj, widget.Button.login.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【登录账号】 可见状态 未 发生变动")
    # 设置 按钮【登录账号】 可用状态
    if obs.obs_property_enabled(widget.Button.login.Obj) != widget.Button.login.Enabled:
        log_save(0, f"　│││✏️ 按钮【登录账号】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.login.Obj)}➡️{widget.Button.login.Enabled}")
        obs.obs_property_set_enabled(widget.Button.login.Obj, widget.Button.login.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【登录账号】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【二维码添加账户】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【二维码添加账户】 UI")
    # 设置 按钮【二维码添加账户】 可见状态
    if obs.obs_property_visible(widget.Button.qrAddAccount.Obj) != widget.Button.qrAddAccount.Visible:
        log_save(0, f"　│││✏️ 按钮【二维码添加账户】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.qrAddAccount.Obj)}➡️{widget.Button.qrAddAccount.Visible}")
        obs.obs_property_set_visible(widget.Button.qrAddAccount.Obj, widget.Button.qrAddAccount.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【二维码添加账户】 可见状态 未 发生变动")
    # 设置 按钮【二维码添加账户】 可用状态
    if obs.obs_property_enabled(widget.Button.qrAddAccount.Obj) != widget.Button.qrAddAccount.Enabled:
        log_save(0, f"　│││✏️ 按钮【二维码添加账户】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.qrAddAccount.Obj)}➡️{widget.Button.qrAddAccount.Enabled}")
        obs.obs_property_set_enabled(widget.Button.qrAddAccount.Obj, widget.Button.qrAddAccount.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【二维码添加账户】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【显示二维码图片】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【显示二维码图片】 UI")
    # 设置 按钮【显示二维码图片】 可见状态
    if obs.obs_property_visible(widget.Button.qrPictureDisplay.Obj) != widget.Button.qrPictureDisplay.Visible:
        log_save(0, f"　│││✏️ 按钮【显示二维码图片】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.qrPictureDisplay.Obj)}➡️{widget.Button.qrPictureDisplay.Visible}")
        obs.obs_property_set_visible(widget.Button.qrPictureDisplay.Obj, widget.Button.qrPictureDisplay.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【显示二维码图片】 可见状态 未 发生变动")
    # 设置 按钮【显示二维码图片】 可用状态
    if obs.obs_property_enabled(widget.Button.qrPictureDisplay.Obj) != widget.Button.qrPictureDisplay.Enabled:
        log_save(0, f"　│││✏️ 按钮【显示二维码图片】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.qrPictureDisplay.Obj)}➡️{widget.Button.qrPictureDisplay.Enabled}")
        obs.obs_property_set_enabled(widget.Button.qrPictureDisplay.Obj, widget.Button.qrPictureDisplay.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【显示二维码图片】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【删除账户】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【删除账户】 UI")
    # 设置 按钮【删除账户】 可见状态
    if obs.obs_property_visible(widget.Button.accountDelete.Obj) != widget.Button.accountDelete.Visible:
        log_save(0, f"　│││✏️ 按钮【删除账户】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.accountDelete.Obj)}➡️{widget.Button.accountDelete.Visible}")
        obs.obs_property_set_visible(widget.Button.accountDelete.Obj, widget.Button.accountDelete.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【删除账户】 可见状态 未 发生变动")
    # 设置 按钮【删除账户】 可用状态
    if obs.obs_property_enabled(widget.Button.accountDelete.Obj) != widget.Button.accountDelete.Enabled:
        log_save(0, f"　│││✏️ 按钮【删除账户】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.accountDelete.Obj)}➡️{widget.Button.accountDelete.Enabled}")
        obs.obs_property_set_enabled(widget.Button.accountDelete.Obj, widget.Button.accountDelete.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【删除账户】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【备份账户】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【备份账户】 UI")
    # 设置 按钮【备份账户】 可见状态
    if obs.obs_property_visible(widget.Button.accountBackup.Obj) != widget.Button.accountBackup.Visible:
        log_save(0, f"　│││✏️ 按钮【备份账户】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.accountBackup.Obj)}➡️{widget.Button.accountBackup.Visible}")
        obs.obs_property_set_visible(widget.Button.accountBackup.Obj, widget.Button.accountBackup.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【备份账户】 可见状态 未 发生变动")
    # 设置 按钮【备份账户】 可用状态
    if obs.obs_property_enabled(widget.Button.accountBackup.Obj) != widget.Button.accountBackup.Enabled:
        log_save(0, f"　│││✏️ 按钮【备份账户】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.accountBackup.Obj)}➡️{widget.Button.accountBackup.Enabled}")
        obs.obs_property_set_enabled(widget.Button.accountBackup.Obj, widget.Button.accountBackup.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【备份账户】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【恢复账户】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【恢复账户】 UI")
    # 设置 按钮【恢复账户】 可见状态
    if obs.obs_property_visible(widget.Button.accountRestore.Obj) != widget.Button.accountRestore.Visible:
        log_save(0, f"　│││✏️ 按钮【恢复账户】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.accountRestore.Obj)}➡️{widget.Button.accountRestore.Visible}")
        obs.obs_property_set_visible(widget.Button.accountRestore.Obj, widget.Button.accountRestore.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【恢复账户】 可见状态 未 发生变动")
    # 设置 按钮【恢复账户】 可用状态
    if obs.obs_property_enabled(widget.Button.accountRestore.Obj) != widget.Button.accountRestore.Enabled:
        log_save(0, f"　│││✏️ 按钮【恢复账户】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.accountRestore.Obj)}➡️{widget.Button.accountRestore.Enabled}")
        obs.obs_property_set_enabled(widget.Button.accountRestore.Obj, widget.Button.accountRestore.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【恢复账户】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【登出账号】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【登出账号】 UI")
    # 设置 按钮【登出账号】 可见状态
    if obs.obs_property_visible(widget.Button.logout.Obj) != widget.Button.logout.Visible:
        log_save(0, f"　│││✏️ 按钮【登出账号】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.logout.Obj)}➡️{widget.Button.logout.Visible}")
        obs.obs_property_set_visible(widget.Button.logout.Obj, widget.Button.logout.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【登出账号】 可见状态 未 发生变动")
    # 设置 按钮【登出账号】 可用状态
    if obs.obs_property_enabled(widget.Button.logout.Obj) != widget.Button.logout.Enabled:
        log_save(0, f"　│││✏️ 按钮【登出账号】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.logout.Obj)}➡️{widget.Button.logout.Enabled}")
        obs.obs_property_set_enabled(widget.Button.logout.Obj, widget.Button.logout.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【登出账号】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌按钮 UI{30*'─'}┘")

    log_save(0, f"　│                       更新UI界面数据                       │")
    log_save(0, f"╲────────────────────────更新UI界面数据────────────────────────╱")
    return True


def button_function_qr_add_account(props, prop):
    """
    二维码添加账号
    Args:
        props:
        prop:
    Returns:
    """
    # 判断是否需要展示登录二维码图片
    if GlobalVariableOfData.loginQRCodePillowImg:
        return button_function_show_qr_picture()

    # 申请登录二维码
    url8qrkey = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).generate()
    # 获取二维码url
    url = url8qrkey['url']
    log_save(0, f"获取登录二维码链接{url}")
    # 获取二维码key
    GlobalVariableOfData.loginQrCode_key = url8qrkey['qrcode_key']
    log_save(0, f"获取登录二维码密钥{GlobalVariableOfData.loginQrCode_key}")
    # 获取二维码对象
    qr = qr_text8pil_img(url)
    # 获取登录二维码的pillow img实例
    GlobalVariableOfData.loginQRCodePillowImg = qr["img"]
    # 输出二维码图形字符串
    log_save(0, f"\n\n{qr['str']}")
    log_save(0, f"字符串二维码已输出，如果乱码或者扫描不上，建议点击 按钮【显示登录二维码图片】")
    # 获取二维码扫描登陆状态
    GlobalVariableOfData.loginQrCodeReturn = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).poll(GlobalVariableOfData.loginQrCode_key)
    log_save(0, f"开始轮询登录状态")
    # 轮询登录状态
    log_save(2, str(information4login_qr_return_code[GlobalVariableOfData.loginQrCodeReturn['code']]))

    def check_poll():
        """
        二维码扫描登录状态检测
        @return: cookies，超时为{}
        """
        # 获取uid对应的cookies
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(GlobalVariableOfData.scriptsUsersConfigFilepath)
        user_list_dict = b_u_l_c.get_users()
        code_old = GlobalVariableOfData.loginQrCodeReturn['code']
        GlobalVariableOfData.loginQrCodeReturn = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).poll(GlobalVariableOfData.loginQrCode_key)
        # 二维码扫描登陆状态改变时，输出改变后状态
        log_save(2, str(information4login_qr_return_code[GlobalVariableOfData.loginQrCodeReturn['code']])) if code_old != GlobalVariableOfData.loginQrCodeReturn['code'] else None
        if GlobalVariableOfData.loginQrCodeReturn['code'] == 0 or GlobalVariableOfData.loginQrCodeReturn['code'] == 86038:
            log_save(0, "轮询结束")
            GlobalVariableOfData.loginQRCodePillowImg = None
            # 二维码扫描登陆状态为成功或者超时时获取cookies结束[轮询二维码扫描登陆状态]
            cookies = GlobalVariableOfData.loginQrCodeReturn['cookies']
            if cookies:
                # 获取登陆账号cookies中携带的uid
                uid = int(cookies['DedeUserID'])
                if str(uid) in user_list_dict.values():
                    log_save(1, "已有该用户，正在更新用户登录信息")
                    b_u_l_c.update_user(cookies, False)
                else:
                    b_u_l_c.add_user(cookies)
                    log_save(0, "添加用户成功")
                    # 请点击按钮【更新账号列表】，更新用户列表
                    log_save(0, "请点击按钮【更新账号列表】，更新用户列表")
            else:
                log_save(0, "添加用户失败")
            # 结束计时器
            obs.remove_current_callback()

    # 开始计时器
    obs.timer_add(check_poll, 1000)
    return True


def button_function_show_qr_picture():
    """
    显示二维码图片
    """
    if GlobalVariableOfData.loginQRCodePillowImg:
        log_save(0, f"有可展示的登录二维码图片，展示登录二维码图片")
        GlobalVariableOfData.loginQRCodePillowImg.show()
        return True
    else:
        log_save(2, f"没有可展示的登录二维码图片，请点击按钮 【二维码添加账号】创建")
        return False


def button_function_del_user(props, prop):
    """
    删除用户
    Args:
        props:
        prop:
    Returns:
    """
    uid = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'uid_comboBox')
    if uid in ["-1"]:
        log_save(3, "请选择一个账号")
        return False
    # ＝＝＝＝＝＝＝＝＝＝＝
    # ＝     删除      ＝
    # ＝＝＝＝＝＝＝＝＝＝＝
    log_save(0, f"即将删除的账号：{uid}")
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    b_u_l_c.delete_user(uid)
    # ＝＝＝＝＝＝＝＝＝＝＝
    # ＝     更新      ＝
    # ＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    log_save(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfData.script_settings)
    # 更新脚本用户小部件
    log_save(0, f"更新控件UI")
    update_ui_interface_data()
    return True


def button_function_backup_users(props, prop):
    """
    备份用户
    Args:
        props:
        prop:
    Returns:
    """
    pass


def button_function_restore_user(props, prop):
    """
    恢复用户
    Args:
        props:
        prop:
    Returns:
    """
    pass


def button_function_logout(props, prop):
    """
    登出
    Args:
        props:
        prop:
    Returns:
    """
    uid = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'uid_comboBox')
    if uid in ["-1"]:
        log_save(3, "未登陆账号")
        return False
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　登出        ＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 移除默认账户
    log_save(0, f"即将登出的账号：{uid}")
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    b_u_l_c.update_user(None)
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　更新     　　＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    log_save(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfData.script_settings)
    # 更新脚本用户小部件
    log_save(0, f"更新控件UI")
    update_ui_interface_data()
    return True


def button_function_opened_room(props, prop):
    """创建直播间"""
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 开通直播间
    create_live_room_return = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).create_live_room()
    log_save(0, f"开通直播间返回值: {create_live_room_return}")
    # 处理API响应
    code = create_live_room_return.get("code", -1)
    message = create_live_room_return.get("message", "未知错误")
    if code == 0:
        # 成功开通，返回房间号
        room_id = create_live_room_return.get("data", {}).get("roomID", "")
        if not room_id:
            log_save(0, "API返回了空房间号")
        log_save(0, room_id)
    elif code == 1531193016:
        # 已经创建过直播间
        log_save(0, "已经创建过直播间")
    else:
        # 其他错误
        log_save(0, f"开通直播间失败: {message} (代码: {code})")
    return True


def button_function_check_room_cover(props, prop):
    """
    查看直播间封面
    Args:
        props:
        prop:
    Returns:
    """
    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间id"""
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (
        BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间基本信息"""
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_base_info if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间封面链接
    room_cover_url = (room_base_info["cover"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户直播间封面链接"""
    log_save(0, f"║║登录账户 的 直播间封面链接：{(room_cover_url if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")

    # # 获取'默认账户'直播间的基础信息
    room_cover_pillow_img = url2pillow_image(room_cover_url, GlobalVariableOfData.sslVerification)
    if room_cover_pillow_img:
        log_save(0, f"显示16:9封面，格式: {room_cover_pillow_img.format}，尺寸: {room_cover_pillow_img.size}")
        room_cover_pillow_img.show()
        room_cover_pillow_img0403 = pil_image2central_proportion_cutting(room_cover_pillow_img, 4 / 3)
        log_save(0, f"展示4:3图片")
        room_cover_pillow_img0403.show()
    pass


def button_function_update_room_cover():
    """上传直播间封面"""
    # 获取文件对话框内容
    widget.PathBox.roomCover.Text = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_cover_fileDialogBox')
    log_save(0, f"获得图片文件：{widget.PathBox.roomCover.Text}")
    if widget.PathBox.roomCover.Text:
        pil_image = Image.open(widget.PathBox.roomCover.Text)
        log_save(0, f"图片文件PIL_Image实例化，当前文件大小(宽X高)：{pil_image.size}")
        pil_image1609 = pil_image2central_proportion_cutting(pil_image, 16 / 9)
        pil_image1609_w, pil_image1609_h = pil_image1609.size
        log_save(0, f"图片16:9裁切后大小(宽X高)：{pil_image1609.size}")
        pil_image1609zooming_width1020 = pil_image1609 if pil_image1609_w < 1020 else pil_image2zooming(pil_image1609, 4, target_width=1020)
        log_save(0, f"限制宽<1020，进行缩放，缩放后大小：{pil_image1609zooming_width1020.size}")
        pil_image1609 = pil_image2central_proportion_cutting(pil_image1609zooming_width1020, 16 / 9)
        log_save(0, f"缩放后图片16:9裁切后大小(宽X高)：{pil_image1609.size}")
        pil_image0403 = pil_image2central_proportion_cutting(pil_image1609zooming_width1020, 4 / 3)
        log_save(0, f"缩放后图片4:3裁切后大小(宽X高)：{pil_image0403.size}")

        log_save(0, f"图片二进制化")
        pil_image1609zooming_width1020_binary = pil_image2binary(pil_image1609zooming_width1020, img_format="JPEG", compress_level=0)
        # 创建用户配置文件实例
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
        b_a_c_authentication = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies()))
        # 上传封面图片返回
        upload_cover_return = b_a_c_authentication.upload_cover(pil_image1609zooming_width1020_binary)
        log_save(0, f"上传封面返回：{upload_cover_return}")
        if upload_cover_return["code"] == 0:
            log_save(0, f"展示4:3图片")
            pil_image0403.show()
            log_save(0, f"展示16:9图片")
            pil_image1609.show()
            log_save(0, f"上传封面成功")
            # 获得封面图片链接
            cover_url = upload_cover_return['data']['location']
            log_save(0, f"获得封面链接：{cover_url}")
            update_cover_return = b_a_c_authentication.update_cover(cover_url)
            log_save(0, f"更改封面返回：{upload_cover_return}")
            if update_cover_return["code"] == 0:
                log_save(0, f"更改封面成功")
            else:
                log_save(3, f"更改封面失败：{update_cover_return['message']}")
                return False
        else:
            log_save(3, f"上传封面失败：{upload_cover_return['message']}")
            return False
    else:
        log_save(2, "未获取到图片")
        return False
    return True


def button_function_face_auth():
    """展示人脸认证的二维码"""
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取登录用户的uid
    uid = b_u_l_c.get_users()[0]
    log_save(0, f"获取登录用户的uid：{uid}")
    # 获取人脸认证的链接
    qr_url = f"https://www.bilibili.com/blackboard/live/face-auth-middle.html?source_event=400&mid={uid}"
    log_save(0, f"获取人脸认证的链接：{qr_url}")
    if uid:
        # 获取二维码对象
        qr = qr_text8pil_img(qr_url)
        qr['img'].show()
    else:
        log_save(3, f"未登录")


def button_function_true_live_room_title():
    """将可 可编辑组合框【常用标题】 中的文本 复制到 普通文本框【直播间标题】 """
    # 获取 可编辑组合框【常用标题】 当前 显示文本
    title_text = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_commonTitles_comboBox')
    log_save(0, f"获取 可编辑组合框【常用标题】 当前 显示文本：{title_text}")
    # 更新 普通文本框【直播间标题】 的 文本
    obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_title_textBox', title_text)
    log_save(0, f"更新 普通文本框【直播间标题】 的 文本")
    return True


def button_function_change_live_room_title():
    """
    更改直播间标题
    Args:
        props:
        prop:
    Returns:
    """
    # 获取当前直播间标题
    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    # 获取 '默认账户' cookie
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (
        BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间标题
    room_title = (room_base_info["title"] if room_status else None) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间标题：{(room_title if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")

    # 设置 普通文本框【直播间标题】 可见状态
    widget.TextBox.roomTitle.Visible = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播间标题】 可见状态：{str(widget.TextBox.roomTitle.Visible)}")
    # 设置 普通文本框【直播间标题】 可用状态
    widget.TextBox.roomTitle.Enabled = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播间标题】 可用状态：{str(widget.TextBox.roomTitle.Enabled)}")
    # 设置 普通文本框【直播间标题】 内容
    widget.TextBox.roomTitle.Text = room_title if bool(room_status) else ""
    log_save(0, f"║║║设置 普通文本框【直播间标题】 内容：{str(widget.TextBox.roomTitle.Text)}")

    # 将当前直播间标题和目标直播间标题做对比
    # 获取 普通文本框【直播间标题】 当前 文本
    live_room_title_textbox_string = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_title_textBox')
    log_save(0, f"获取 普通文本框【直播间标题】 当前 文本：{live_room_title_textbox_string}")
    # 更新直播间标题
    if room_title == live_room_title_textbox_string:
        log_save(0, f"直播间标题未更改")
        return False
    turn_title_return = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).change_room_title(
        live_room_title_textbox_string)
    log_save(0, f"更改直播间标题返回消息：{turn_title_return}")
    if turn_title_return['code'] == 0:
        log_save(0, "直播间标题更改成功")
    else:
        log_save(0, f"直播间标题更改失败{turn_title_return['message']}")
        return False

    # 刷新一下 可编辑组合框【常用标题】 和 普通文本框【直播间标题】
    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    # 获取 '默认账户' cookie
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (
        BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间标题
    room_title = (room_base_info["title"] if room_status else None) if b_u_l_c.get_cookies() else None
    log_save(0, f"║║登录账户 的 直播间标题：{(room_title if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 创建用户常用直播间标题实例
    c_t_m = CommonTitlesManager(directory=Path(GlobalVariableOfData.scriptsDataDirpath))
    # 添加当前直播间标题 到 常用直播间标 题配置文件
    (c_t_m.add_title(b_u_l_c.get_users()[0], room_title) if room_status else None) if b_u_l_c.get_cookies() else None
    # 获取 常用直播间标题
    common_title4number = {str(number): commonTitle for number, commonTitle in enumerate(c_t_m.get_titles(b_u_l_c.get_users()[0]))}
    """常用直播间标题】{'0': 't1', '1': 't2', '2': 't3',}"""
    log_save(0, f"║║登录账户 的 常用直播间标题：{(common_title4number if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【直播间】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播间】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播间】 中控件属性{7*'═'}╗")
    # 设置 可编辑组合框【常用标题】 可见状态
    widget.ComboBox.roomCommonTitles.Visible = bool(room_status)
    log_save(0, f"║║║设置 可编辑组合框【常用标题】 可见状态：{str(widget.ComboBox.roomCommonTitles.Visible)}")
    # 设置 可编辑组合框【常用标题】 可用状态
    widget.ComboBox.roomCommonTitles.Enabled = bool(room_status)
    log_save(0, f"║║║设置 可编辑组合框【常用标题】 可用状态：{str(widget.ComboBox.roomCommonTitles.Enabled)}")
    # 设置 可编辑组合框【常用标题】 的数据字典
    widget.ComboBox.roomCommonTitles.Dictionary = common_title4number
    log_save(0, f"║║║设置 可编辑组合框【常用标题】 数据字典：{str(widget.ComboBox.roomCommonTitles.Dictionary)}")
    # 设置 可编辑组合框【常用标题】 默认显示内容
    widget.ComboBox.roomCommonTitles.Text = room_title if bool(room_status) else ""
    log_save(0, f"║║║设置 可编辑组合框【常用标题】 默认显示内容：{str(widget.ComboBox.roomCommonTitles.Text)}")
    # 设置 可编辑组合框【常用标题】 默认显示内容 的 列表值
    widget.ComboBox.roomCommonTitles.Value = "0"
    log_save(0, f"║║║设置 可编辑组合框【常用标题】 默认显示内容 的 列表值：{str(widget.ComboBox.roomCommonTitles.Value)}")

    # 设置 普通文本框【直播间标题】 可见状态
    widget.TextBox.roomTitle.Visible = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播间标题】 可见状态：{str(widget.TextBox.roomTitle.Visible)}")
    # 设置 普通文本框【直播间标题】 可用状态
    widget.TextBox.roomTitle.Enabled = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播间标题】 可用状态：{str(widget.TextBox.roomTitle.Enabled)}")
    # 设置 普通文本框【直播间标题】 内容
    widget.TextBox.roomTitle.Text = room_title if bool(room_status) else ""
    log_save(0, f"║║║设置 普通文本框【直播间标题】 内容：{str(widget.TextBox.roomTitle.Text)}")
    # 设置 分组框【直播间】 中控件属性结束
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播间】 中控件属性{7*'═'}╝")
    # 设置 控件属性 结束
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")

    # 可编辑组合框++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐可编辑组合框 UI{30*'─'}┐")
    # 【直播间】分组———————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播间】")
    # 可编辑组合框【常用标题】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️可编辑组合框【常用标题】 UI")
    # 设置 可编辑组合框【常用标题】 可见状态
    if obs.obs_property_visible(widget.ComboBox.roomCommonTitles.Obj) != widget.ComboBox.roomCommonTitles.Visible:
        log_save(0, f"　│││✏️ 可编辑组合框【常用标题】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.roomCommonTitles.Obj)}➡️{widget.ComboBox.roomCommonTitles.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.roomCommonTitles.Obj, widget.ComboBox.roomCommonTitles.Visible)
    else:
        log_save(0, f"　│││🧩 可编辑组合框【常用标题】 可见状态 未 发生变动")
    # 设置 可编辑组合框【常用标题】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.roomCommonTitles.Obj) != widget.ComboBox.roomCommonTitles.Enabled:
        log_save(0, f"　│││✏️ 可编辑组合框【常用标题】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.roomCommonTitles.Obj)}➡️{widget.ComboBox.roomCommonTitles.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.roomCommonTitles.Obj, widget.ComboBox.roomCommonTitles.Enabled)
    else:
        log_save(0, f"　│││🧩 可编辑组合框【常用标题】 可用状态 未 发生变动")
    # 判断 可编辑组合框【常用标题】字典数据 和 当前数据是否有变化
    if widget.ComboBox.roomCommonTitles.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.roomCommonTitles.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomCommonTitles.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomCommonTitles.Obj))}:
        log_save(0, f"　│││✏️ 可编辑组合框【常用标题】列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.roomCommonTitles.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomCommonTitles.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomCommonTitles.Obj))})}个元素➡️{len(widget.ComboBox.roomCommonTitles.Dictionary)}个元素")
        # 清空 可编辑组合框【常用标题】
        log_save(0, f"　│││更新 可编辑组合框【常用标题】数据 第一步：清空 可编辑组合框【常用标题】")
        obs.obs_property_list_clear(widget.ComboBox.roomCommonTitles.Obj)
        # 添加 可编辑组合框【常用标题】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││更新 可编辑组合框【常用标题】数据 第二步：添加 可编辑组合框【常用标题】 列表选项  如果有默认值，会被设置在第一位")
        for number in widget.ComboBox.roomCommonTitles.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.roomCommonTitles.Obj, widget.ComboBox.roomCommonTitles.Dictionary[number], number) if number != widget.ComboBox.roomCommonTitles.Value else obs.obs_property_list_insert_string(widget.ComboBox.roomCommonTitles.Obj, 0, widget.ComboBox.roomCommonTitles.Text, widget.ComboBox.roomCommonTitles.Value)
        # 设置 可编辑组合框【常用标题】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││更新 可编辑组合框【常用标题】数据 第三步：更新 可编辑组合框【常用标题】 显示文本：{obs.obs_property_list_item_name(widget.ComboBox.roomCommonTitles.Obj, 0)}")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_commonTitles_comboBox', obs.obs_property_list_item_name(widget.ComboBox.roomCommonTitles.Obj, 0))
    else:
        log_save(0, f"　│││🧩 可编辑组合框【常用标题】列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    # 普通文本框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐普通文本框 UI{30*'─'}┐")
    # 【账号】分组————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【账号】")
    log_save(0, f"　│└{'─'*60}┘")
    # 【直播间】分组———————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播间】")
    # 普通文本框【直播间标题】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️普通文本框【直播间标题】 UI")
    # 设置 普通文本框【直播间标题】 可见状态
    if obs.obs_property_visible(widget.TextBox.roomTitle.Obj) != widget.TextBox.roomTitle.Visible:
        log_save(0, f"　│││✏️ 普通文本框【直播间标题】 可见状态 发生变动: {obs.obs_property_visible(widget.TextBox.roomTitle.Obj)}➡️{widget.TextBox.roomTitle.Visible}")
        obs.obs_property_set_visible(widget.TextBox.roomTitle.Obj, widget.TextBox.roomTitle.Visible)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播间标题】 可见状态 未 发生变动")
    # 设置 普通文本框【直播间标题】 可用状态
    if obs.obs_property_enabled(widget.TextBox.roomTitle.Obj) != widget.TextBox.roomTitle.Enabled:
        log_save(0, f"　│││✏️ 普通文本框【直播间标题】 可用状态 发生变动: {obs.obs_property_enabled(widget.TextBox.roomTitle.Obj)}➡️{widget.TextBox.roomTitle.Enabled}")
        obs.obs_property_set_enabled(widget.TextBox.roomTitle.Obj, widget.TextBox.roomTitle.Enabled)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播间标题】 可用状态 未 发生变动")
    # 设置 普通文本框【直播间标题】 文本
    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_title_textBox') != widget.TextBox.roomTitle.Text:
        log_save(0, f"　│││✏️ 普通文本框【直播间标题】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_title_textBox')}➡️{widget.TextBox.roomTitle.Text}")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, "room_title_textBox", widget.TextBox.roomTitle.Text)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播间标题】 文本 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌普通文本框 UI{30*'─'}┘")
    return True


def button_function_change_live_room_news():
    """
    更改直播间公告
    Args:
        props:
        prop:
    Returns:
    """
    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间id"""
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (
        BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间基本信息"""
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_base_info if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 直播间公告
    room_news = (BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=
        dict2cookie(b_u_l_c.get_cookies())).get_room_news() if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间公告"""
    log_save(0, f"║║登录账户 的 直播间公告：{(room_news if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")


    live_room_news_textbox_string = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_news_textBox')
    if room_news == live_room_news_textbox_string:
        log_save(0, "直播间公告未改变")
        return False
    # 获取 '默认账户' cookie
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    cookies = b_u_l_c.get_cookies()
    turn_news_return = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(cookies), ).change_room_news(
        live_room_news_textbox_string)
    log_save(0, f'更改直播间公告返回消息：{turn_news_return}')
    if turn_news_return['code'] == 0:
        log_save(0, "直播间公告更改成功")
    else:
        log_save(0, f"直播间公告更改失败{turn_news_return['message']}")
        return False


    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间id"""
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (
        BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间基本信息"""
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_base_info if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 直播间公告
    room_news = (BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=
        dict2cookie(b_u_l_c.get_cookies())).get_room_news() if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间公告"""
    log_save(0, f"║║登录账户 的 直播间公告：{(room_news if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【直播间】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播间】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播间】 中控件属性{7*'═'}╗")
    # 设置 普通文本框【直播间公告】 可见状态
    widget.TextBox.roomNews.Visible = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播间公告】 可见状态：{str(widget.TextBox.roomNews.Visible)}")
    # 设置 普通文本框【直播间公告】 可用状态
    widget.TextBox.roomNews.Enabled = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播间公告】 可用状态：{str(widget.TextBox.roomNews.Enabled)}")
    # 设置 普通文本框【直播间公告】 内容
    widget.TextBox.roomNews.Text = room_news if bool(room_status) else ""
    log_save(0, f"║║║设置 普通文本框【直播间公告】 内容：{str(widget.TextBox.roomNews.Text)}")
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播间】 中控件属性{7*'═'}╝")
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")


    # 普通文本框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐普通文本框 UI{30*'─'}┐")
    # 【直播间】分组———————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播间】")
    # 普通文本框【直播间公告】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️普通文本框【直播间公告】 UI")
    # 设置 普通文本框【直播间公告】 可见状态
    if obs.obs_property_visible(widget.TextBox.roomNews.Obj) != widget.TextBox.roomNews.Visible:
        log_save(0, f"　│││✏️ 普通文本框【直播间公告】 可见状态 发生变动: {obs.obs_property_visible(widget.TextBox.roomNews.Obj)}➡️{widget.TextBox.roomNews.Visible}")
        obs.obs_property_set_visible(widget.TextBox.roomNews.Obj, widget.TextBox.roomNews.Visible)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播间公告】 可见状态 未 发生变动")
    # 设置 普通文本框【直播间公告】 可用状态
    if obs.obs_property_enabled(widget.TextBox.roomNews.Obj) != widget.TextBox.roomNews.Enabled:
        log_save(0, f"　│││✏️ 普通文本框【直播间公告】 可用状态 发生变动: {obs.obs_property_enabled(widget.TextBox.roomNews.Obj)}➡️{widget.TextBox.roomNews.Enabled}")
        obs.obs_property_set_enabled(widget.TextBox.roomNews.Obj, widget.TextBox.roomNews.Enabled)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播间公告】 可用状态 未 发生变动")
    # 设置 普通文本框【直播间公告】 文本
    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_news_textBox') != widget.TextBox.roomNews.Text:
        log_save(0, f"　│││✏️ 普通文本框【直播间公告】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_news_textBox')}➡️{widget.TextBox.roomNews.Text}")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, "room_news_textBox", widget.TextBox.roomNews.Text)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播间公告】 文本 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌普通文本框 UI{30*'─'}┘")
    return True


def button_function_true_live_room_area():
    """将可 组合框【常用分区】 中的值 映射到 组合框【一级分区】 和 组合框【二级分区】 """
    # #获取 组合框【常用分区】 当前选项的值
    room_common_areas_combobox_value = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_commonAreas_comboBox')
    log_save(0, f"获取 组合框【常用分区】 当前选项的值: {room_common_areas_combobox_value}")
    if room_common_areas_combobox_value == "-1":
        log_save(0, f"无常用分区")
        return False
    room_common_parent_area_id = list(json.loads(room_common_areas_combobox_value).keys())[0]
    log_save(0, f"获取 常用分区 父分区id: {room_common_parent_area_id}")
    room_common_sub_area_id = list(json.loads(room_common_areas_combobox_value).values())[0]
    log_save(0, f"获取 常用分区 子分区id: {room_common_sub_area_id}")
    # 更新 组合框【一级分区】
    obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_parentArea_comboBox', room_common_parent_area_id)
    obs.obs_property_modified(widget.ComboBox.roomParentArea.Obj, GlobalVariableOfData.script_settings)
    # 更新 组合框【二级分区】
    obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_subArea_comboBox', room_common_sub_area_id)
    return True


def button_function_start_parent_area():
    """确认一级分区"""
    # #获取 组合框【一级分区】 当前选项的值
    parent_live_area_combobox_value = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_parentArea_comboBox')
    log_save(0, f"获取 组合框【一级分区】 当前选项的值: {parent_live_area_combobox_value}")
    if parent_live_area_combobox_value in ["-1"]:
        log_save(2, "请选择一级分区")
        return False

    # 记录旧的 组合框【二级分区】 数据字典
    sub_live_area_name4sub_live_area_id_old = widget.ComboBox.roomSubArea.Dictionary
    # 获取B站直播分区信息
    area_obj_list = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_area_obj_list()
    # 获取 组合框【二级分区】 数据字典
    sub_live_area_name4sub_live_area_id = {str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in [AreaObj["list"] for AreaObj in area_obj_list["data"] if str(parent_live_area_combobox_value) == str(AreaObj["id"])][0]}
    log_save(0,  f"获取 当前父分区对应的子分区数据{sub_live_area_name4sub_live_area_id}")
    #  设置 临时 组合框【二级分区】 数据字典
    widget.ComboBox.roomSubArea.Dictionary = sub_live_area_name4sub_live_area_id

    # 临时 更新 组合框【二级分区】 数据
    # 组合框【二级分区】 UI
    log_save(0, f"　│┌{'─'*55}")
    log_save(0, f"　││组合框【二级分区】 UI")
    # 判断 组合框【二级分区】字典数据 和 当前数据是否有变化
    if widget.ComboBox.roomSubArea.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.roomSubArea.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomSubArea.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomSubArea.Obj))}:
        log_save(0, f"　││组合框【二级分区】数据发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.roomSubArea.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomSubArea.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomSubArea.Obj))})}个元素➡️{len(widget.ComboBox.roomSubArea.Dictionary)}个元素")
        # 清空 组合框【二级分区】
        log_save(0, f"　││更新 组合框【二级分区】数据 第一步：清空 组合框【二级分区】")
        obs.obs_property_list_clear(widget.ComboBox.roomSubArea.Obj)
        # 添加 组合框【二级分区】 列表选项  默认值会被设置在第一位
        log_save(0, f"　││更新 组合框【二级分区】数据 第二步：添加 组合框【二级分区】 列表选项  如果有默认值，会被设置在第一位")
        for subLiveAreaId in widget.ComboBox.roomSubArea.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.roomSubArea.Obj, widget.ComboBox.roomSubArea.Dictionary[subLiveAreaId], subLiveAreaId) if subLiveAreaId != widget.ComboBox.roomSubArea.Value else obs.obs_property_list_insert_string(widget.ComboBox.roomSubArea.Obj, 0, widget.ComboBox.roomSubArea.Text, widget.ComboBox.roomSubArea.Value)
        # 设置 组合框【二级分区】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　││更新 组合框【二级分区】数据 第三步：更新 组合框【二级分区】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_subArea_comboBox', obs.obs_property_list_item_string(widget.ComboBox.roomSubArea.Obj, 0))
    log_save(0, f"　│└{'─'*55}")

    # 返还旧的 组合框【二级分区】 数据字典
    widget.ComboBox.roomSubArea.Dictionary = sub_live_area_name4sub_live_area_id_old
    return True


def button_function_start_sub_area():
    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    log_save(0, f"║║")
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间id"""
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间基本信息"""
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_base_info if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间的分区
    area = ({"parent_area_id": room_base_info["parent_area_id"], "parent_area_name": room_base_info["parent_area_name"], "area_id": room_base_info["area_id"], "area_name": room_base_info["area_name"], } if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间分区】{"parent_area_id": 3, "parent_area_name": "手游", "area_id": 255, "area_name": "明日方舟"}"""
    log_save(0, f"║║登录账户 的 直播间分区数据：{(area if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")

    # #获取 组合框【二级分区】 当前选项的值
    sub_live_area_combobox_value = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_subArea_comboBox')
    if sub_live_area_combobox_value == str(area["area_id"]):
        log_save(0, "分区未变化")
        return False
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    change_room_area_return = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).change_room_area(int(sub_live_area_combobox_value))
    log_save(0, f"更新直播间分区返回：{change_room_area_return}")
    if change_room_area_return["code"] == 0:
        log_save(0, "直播间分区更改成功")
    else:
        if change_room_area_return["code"] == 60024:
            button_function_face_auth()
        log_save(2, f"直播间分区更改失败：{change_room_area_return['message']}")
        return False

    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间id
    room_id = (room_info_old["roomid"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间id"""
    log_save(0, f"║║登录账户 的 直播间id：{(room_id if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间基本信息
    room_base_info = (
        BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_base_info(room_id) if room_status else None) if b_u_l_c.get_cookies() else None
    """直播间基本信息"""
    log_save(0, f"║║登录账户 的 直播间基本信息：{room_base_info if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间的分区
    area = ({"parent_area_id": room_base_info["parent_area_id"], "parent_area_name": room_base_info["parent_area_name"], "area_id": room_base_info["area_id"], "area_name": room_base_info["area_name"], } if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播间分区】{"parent_area_id": 3, "parent_area_name": "手游", "area_id": 255, "area_name": "明日方舟"}"""
    log_save(0, f"║║登录账户 的 直播间分区数据：{(area if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 直播间 常用分区信息
    common_areas = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_anchor_common_areas(room_id)["data"]
    """获取 '登录用户' 直播间 常用分区信息】[{"id": "255", "name": "明日方舟", "parent_id": "3", "parent_name": "手游",}, ]"""
    log_save(0, f"║║登录账户 的 常用分区信息：{(common_areas if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 常用直播间分区
    common_area_id_dict_str4common_area_name_dict_str = (({json.dumps({area['parent_id']: area['id']}, ensure_ascii=False): json.dumps({area['parent_name']: area['name']}, ensure_ascii=False) for area in common_areas} if common_areas else {"-1": "无常用分区"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """登录用户的常用直播间分区字典】{'{parent_id: id}': '{parent_name: name}', }"""
    log_save(0, f"║║登录账户 的 常用直播间分区：{(common_area_id_dict_str4common_area_name_dict_str.values() if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 B站直播分区信息
    area_obj_list = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_area_obj_list()
    """B站直播分区信息"""
    log_save(0, f"║║获取B站直播分区信息：{area_obj_list if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 直播间父分区数据
    parent_live_area_name4parent_live_area_id = (({str(AreaObj["id"]): AreaObj["name"] for AreaObj in area_obj_list['data']} | {} if area else {"-1": "请选择一级分区"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """直播间父分区数据"""
    log_save(0, f"║║获取 直播间父分区数据：{(parent_live_area_name4parent_live_area_id if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else '⚠️未登录账号'}")
    # 获取 登录账户 的 直播间父分区 对应的 直播间子分区数据
    sub_live_area_name4sub_live_area_id = (({str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in [AreaObj["list"] for AreaObj in area_obj_list["data"] if str(area["parent_area_id"]) == str(AreaObj["id"])][0]} if area else {"-1": "请选择一级分区"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """登录账户 的 直播间父分区 对应的 直播间子分区数据"""
    log_save(0, f"║║获取 登录账户 的 直播间父分区 对应的 直播间子分区数据：{(sub_live_area_name4sub_live_area_id if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else '⚠️未登录账号'}")
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【账号】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播间】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播间】 中控件属性{7*'═'}╗")
    # 设置 组合框【常用分区】 可见状态
    widget.ComboBox.roomCommonAreas.Visible = bool(room_status)
    log_save(0, f"║║║设置 组合框【常用分区】 可见状态：{str(widget.ComboBox.roomCommonAreas.Visible)}")
    # 设置 组合框【常用分区】 可用状态
    widget.ComboBox.roomCommonAreas.Enabled = bool(room_status)
    log_save(0, f"║║║设置 组合框【常用分区】 可用状态：{str(widget.ComboBox.roomCommonAreas.Enabled)}")
    # 设置 组合框【常用分区】 的数据字典
    widget.ComboBox.roomCommonAreas.Dictionary = common_area_id_dict_str4common_area_name_dict_str
    log_save(0, f"║║║设置 组合框【常用分区】 数据字典：{str(widget.ComboBox.roomCommonAreas.Dictionary)}")
    # 设置 组合框【常用分区】 默认显示内容
    widget.ComboBox.roomCommonAreas.Text = common_area_id_dict_str4common_area_name_dict_str[json.dumps({area["parent_area_id"]: str(area["area_id"])})] if common_areas else "无常用分区"
    log_save(0, f"║║║设置 组合框【常用分区】 默认显示内容：{str(widget.ComboBox.roomCommonAreas.Text)}")
    # 设置 组合框【常用分区】 默认显示内容 的 列表值
    widget.ComboBox.roomCommonAreas.Value = json.dumps({area["parent_area_id"]: str(area["area_id"])}, ensure_ascii=False) if common_areas else "-1"
    log_save(0, f"║║║设置 组合框【常用分区】 默认显示内容 的 列表值：{str(widget.ComboBox.roomCommonAreas.Value)}")

    # 设置 组合框【一级分区】 可见状态
    widget.ComboBox.roomParentArea.Visible = bool(room_status)
    log_save(0, f"║║║设置 组合框【一级分区】 可见状态：{str(widget.ComboBox.roomParentArea.Visible)}")
    # 设置 组合框【一级分区】 可用状态
    widget.ComboBox.roomParentArea.Enabled = bool(room_status)
    log_save(0, f"║║║设置 组合框【一级分区】 可用状态：{str(widget.ComboBox.roomParentArea.Enabled)}")
    # 设置 组合框【一级分区】 的数据字典
    widget.ComboBox.roomParentArea.Dictionary = parent_live_area_name4parent_live_area_id
    log_save(0, f"║║║设置 组合框【一级分区】 数据字典：{str(widget.ComboBox.roomParentArea.Dictionary)}")
    # 设置 组合框【一级分区】 默认显示内容
    widget.ComboBox.roomParentArea.Text = str(area["parent_area_name"]) if bool(area) else "请选择一级分区"
    log_save(0, f"║║║设置 组合框【一级分区】 默认显示内容：{str(widget.ComboBox.roomParentArea.Text)}")
    # 设置 组合框【一级分区】 默认显示内容 的 列表值
    widget.ComboBox.roomParentArea.Value = str(area["parent_area_id"]) if bool(area) else "-1"
    log_save(0, f"║║║设置 组合框【一级分区】 默认显示内容 的 列表值：{str(widget.ComboBox.roomParentArea.Value)}")

    # 设置 组合框【二级分区】 可见状态
    widget.ComboBox.roomSubArea.Visible = bool(room_status)
    log_save(0, f"║║║设置 组合框【二级分区】 可见状态：{str(widget.ComboBox.roomSubArea.Visible)}")
    # 设置 组合框【二级分区】 可用状态
    widget.ComboBox.roomSubArea.Obj_enabled = bool(room_status)
    log_save(0, f"║║║设置 组合框【二级分区】 可用状态：{str(widget.ComboBox.roomSubArea.Obj_enabled)}")
    # 设置 组合框【二级分区】 数据字典
    widget.ComboBox.roomSubArea.Dictionary = sub_live_area_name4sub_live_area_id
    log_save(0, f"║║║设置 组合框【二级分区】 数据字典：{str(widget.ComboBox.roomSubArea.Dictionary)}")
    # 设置 组合框【二级分区】 默认显示内容
    widget.ComboBox.roomSubArea.Text = str(area["area_name"]) if bool(area) else "请确认一级分区"
    log_save(0, f"║║║设置 组合框【二级分区】 默认显示内容：{str(widget.ComboBox.roomSubArea.Text)}")
    # 设置 组合框【二级分区】 默认显示内容 的 列表值
    widget.ComboBox.roomSubArea.Value = str(area["area_id"]) if bool(area) else "-1"
    log_save(0, f"║║║设置 组合框【二级分区】 默认显示内容 的 列表值：{str(widget.ComboBox.roomSubArea.Value)}")
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播间】 中控件属性{7*'═'}╝")
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")


    # 组合框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐组合框 UI{30*'─'}┐")
    # 【直播间】分组———————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播间】")
    # 组合框【一级分区】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛组合框【常用分区】 UI")
    # 设置 组合框【常用分区 可见状态
    if obs.obs_property_visible(widget.ComboBox.roomCommonAreas.Obj) != widget.ComboBox.roomCommonAreas.Visible:
        log_save(0, f"　│││✏️ 组合框【常用分区】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.roomCommonAreas.Obj)}➡️{widget.ComboBox.roomCommonAreas.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.roomCommonAreas.Obj, widget.ComboBox.roomCommonAreas.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【常用分区】 可见状态 未 发生变动")
    # 设置 组合框【常用分区】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.roomCommonAreas.Obj) != widget.ComboBox.roomCommonAreas.Enabled:
        log_save(0, f"　│││✏️ 组合框【常用分区】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.roomCommonAreas.Obj)}➡️{widget.ComboBox.roomCommonAreas.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.roomCommonAreas.Obj, widget.ComboBox.roomCommonAreas.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【常用分区】 可用状态 未 发生变动")
    # 判断 组合框【常用分区】字典数据 和 当前数据是否有变化
    if widget.ComboBox.roomCommonAreas.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.roomCommonAreas.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomCommonAreas.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomCommonAreas.Obj))}:
        log_save(0, f"　│││✏️ 组合框【常用分区】列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.roomCommonAreas.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomCommonAreas.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomCommonAreas.Obj))})}个元素➡️{len(widget.ComboBox.roomCommonAreas.Dictionary)}个元素")
        # 清空 组合框【常用分区】
        log_save(0, f"　│││📑 更新 组合框【常用分区】数据 第一步：清空 组合框【常用分区】")
        obs.obs_property_list_clear(widget.ComboBox.roomCommonAreas.Obj)
        # 添加 组合框【常用分区】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑  更新 组合框【常用分区】数据 第二步：添加 组合框【常用分区】 列表选项  如果有默认值，会被设置在第一位")
        for common_area_id_dict_str in widget.ComboBox.roomCommonAreas.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.roomCommonAreas.Obj, widget.ComboBox.roomCommonAreas.Dictionary[common_area_id_dict_str], common_area_id_dict_str) if common_area_id_dict_str != widget.ComboBox.roomCommonAreas.Value else obs.obs_property_list_insert_string(widget.ComboBox.roomCommonAreas.Obj, 0, widget.ComboBox.roomCommonAreas.Text, widget.ComboBox.roomCommonAreas.Value)
        # 设置 组合框【常用分区】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【常用分区】数据 第三步：更新 组合框【常用分区】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_commonAreas_comboBox', obs.obs_property_list_item_string(widget.ComboBox.roomCommonAreas.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【常用分区】列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 组合框【一级分区】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【一级分区】 UI")
    # 设置 组合框【一级分区】 可见状态
    if obs.obs_property_visible(widget.ComboBox.roomParentArea.Obj) != widget.ComboBox.roomParentArea.Visible:
        log_save(0, f"　│││✏️ 组合框【一级分区】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.roomParentArea.Obj)}➡️{widget.ComboBox.roomParentArea.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.roomParentArea.Obj, widget.ComboBox.roomParentArea.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【一级分区】 可见状态 未 发生变动")
    # 设置 组合框【一级分区】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.roomParentArea.Obj) != widget.ComboBox.roomParentArea.Enabled:
        log_save(0, f"　│││✏️ 组合框【一级分区】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.roomParentArea.Obj)}➡️{widget.ComboBox.roomParentArea.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.roomParentArea.Obj, widget.ComboBox.roomParentArea.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【一级分区】 可用状态 未 发生变动")
    # 判断 组合框【一级分区】字典数据 和 当前数据是否有变化
    if widget.ComboBox.roomParentArea.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.roomParentArea.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomParentArea.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomParentArea.Obj))}:
        log_save(0, f"　│││✏️ 组合框【一级分区】列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.roomParentArea.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomParentArea.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomParentArea.Obj))})}个元素➡️{len(widget.ComboBox.roomParentArea.Dictionary)}个元素")
        # 清空 组合框【一级分区】
        log_save(0, f"　│││📑 更新 组合框【一级分区】数据 第一步：清空 组合框【一级分区】")
        obs.obs_property_list_clear(widget.ComboBox.roomParentArea.Obj)
        # 添加 组合框【一级分区】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑  更新 组合框【一级分区】数据 第二步：添加 组合框【一级分区】 列表选项  如果有默认值，会被设置在第一位")
        for common_area_id_dict_str in widget.ComboBox.roomParentArea.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.roomParentArea.Obj, widget.ComboBox.roomParentArea.Dictionary[common_area_id_dict_str], common_area_id_dict_str) if common_area_id_dict_str != widget.ComboBox.roomParentArea.Value else obs.obs_property_list_insert_string(widget.ComboBox.roomParentArea.Obj, 0, widget.ComboBox.roomParentArea.Text, widget.ComboBox.roomParentArea.Value)
        # 设置 组合框【一级分区】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【一级分区】数据 第三步：更新 组合框【一级分区】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_parentArea_comboBox', obs.obs_property_list_item_string(widget.ComboBox.roomParentArea.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【一级分区】列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 组合框【二级分区】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【二级分区】 UI")
    # 设置 组合框【二级分区】 可见状态
    if obs.obs_property_visible(widget.ComboBox.roomSubArea.Obj) != widget.ComboBox.roomSubArea.Visible:
        log_save(0, f"　│││✏️ 组合框【二级分区】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.roomSubArea.Obj)}➡️{widget.ComboBox.roomSubArea.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.roomSubArea.Obj, widget.ComboBox.roomSubArea.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【二级分区】 可见状态 未 发生变动")
    # 设置 组合框【二级分区】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.roomSubArea.Obj) != widget.ComboBox.roomSubArea.Obj_enabled:
        log_save(0, f"　│││✏️ 组合框【二级分区】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.roomSubArea.Obj)}➡️{widget.ComboBox.roomSubArea.Obj_enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.roomSubArea.Obj, widget.ComboBox.roomSubArea.Obj_enabled)
    else:
        log_save(0, f"　│││🧩 组合框【二级分区】 可用状态 未 发生变动")
    # 判断 组合框【二级分区】字典数据 和 当前数据是否有变化
    if widget.ComboBox.roomSubArea.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.roomSubArea.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomSubArea.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomSubArea.Obj))}:
        log_save(0, f"　│││✏️ 组合框【二级分区】 列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.roomSubArea.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.roomSubArea.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.roomSubArea.Obj))})}个元素➡️{len(widget.ComboBox.roomSubArea.Dictionary)}个元素")
        # 清空 组合框【二级分区】
        log_save(0, f"　│││📑 更新 组合框【二级分区】数据 第一步：清空 组合框【二级分区】")
        obs.obs_property_list_clear(widget.ComboBox.roomSubArea.Obj)
        # 添加 组合框【二级分区】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑  更新 组合框【二级分区】数据 第二步：添加 组合框【二级分区】 列表选项  如果有默认值，会被设置在第一位")
        for subLiveAreaId in widget.ComboBox.roomSubArea.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.roomSubArea.Obj, widget.ComboBox.roomSubArea.Dictionary[subLiveAreaId], subLiveAreaId) if subLiveAreaId != widget.ComboBox.roomSubArea.Value else obs.obs_property_list_insert_string(widget.ComboBox.roomSubArea.Obj, 0, widget.ComboBox.roomSubArea.Text, widget.ComboBox.roomSubArea.Value)
        # 设置 组合框【二级分区】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【二级分区】数据 第三步：更新 组合框【二级分区】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'room_subArea_comboBox', obs.obs_property_list_item_string(widget.ComboBox.roomSubArea.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【二级分区】 列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌组合框 UI{30*'─'}┘")
    return True


def button_function_jump_blive_web(props, prop):
    """
    跳转直播间后台网页
    Args:
        props:
        prop:
    Returns:
    """
    log_save(0, f"即将跳转到网页{widget.Button.bliveWebJump.Url}")
    pass


# ____________________-------------------____________________---------------------_______________________---------------
def button_function_start_live():
    """
    开始直播
    """
    # 执行更改直播间标题
    button_function_change_live_room_title()
    # 执行更改直播间公告
    button_function_change_live_room_news()
    # 执行更改直播间分区
    button_function_start_sub_area()
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取二级分区id
    sub_live_area_combobox_value = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'room_subArea_comboBox')
    log_save(0, f"在【{sub_live_area_combobox_value}】分区 开播")
    # 获取开播平台
    live_streaming_platform = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_streaming_platform_comboBox')
    log_save(0, f"使用【{live_streaming_platform}】平台 开播")
    start_live = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).start_live(int(sub_live_area_combobox_value), live_streaming_platform)
    log_save(0, f"开播返回：{start_live}")
    if start_live["code"] == 0:
        log_save(0, f"开播成功。")
    else:
        if start_live["code"] == 60024:
            button_function_face_auth()
        log_save(3, f"开播失败：【{start_live['message']}】。")
        return True

    # 推流地址
    rtmp_server = start_live["data"]["rtmp"]["addr"]
    log_save(0, f"rtmp推流地址：{rtmp_server}")
    # 将 rtmp推流码
    rtmp_push_code = start_live["data"]["rtmp"]["code"]
    log_save(0, f"rtmp推流码：{rtmp_push_code}")
    # 复制到剪贴板
    cb.copy(rtmp_push_code)
    log_save(0, f"已将rtmp推流码复制到剪贴板")

    # 获取当前流服务
    streaming_service = obs.obs_frontend_get_streaming_service()
    # 获取当前流服务设置
    streaming_service_settings = obs.obs_service_get_settings(streaming_service)
    currently_service_string = obs.obs_data_get_string(streaming_service_settings, "service")
    log_save(0, f"目前推流服务：【{currently_service_string}】")
    currently_rtmp_server = obs.obs_data_get_string(streaming_service_settings, "server")
    log_save(0, f"目前rtmp推流地址：【{currently_rtmp_server}】")
    currently_rtmp_push_code = obs.obs_data_get_string(streaming_service_settings, "key")
    log_save(0, f"目前rtmp推流码：【{currently_rtmp_push_code}】")
    log_save(0, f"obs推流状态：{obs.obs_frontend_streaming_active()}")
    if currently_rtmp_push_code == rtmp_push_code and currently_rtmp_server == "rtmp://live-push.bilivideo.com/live-bvc/" :  # and currently_service_string == "Bilibili Live - RTMP | 哔哩哔哩直播 - RTMP" :
        log_save(0, f"推流信息未发生变化")
        if obs.obs_frontend_streaming_active():
            log_save(0, f"正处于推流状态中。。。")
            pass
        else:
            log_save(0, f"直接开始推流")
            obs.obs_frontend_streaming_start()
    else:
        log_save(0, f"推流信息发生变化")
        # # 写入推流服务
        # obs.obs_data_set_string(streaming_service_settings, "service", "Bilibili Live - RTMP | 哔哩哔哩直播 - RTMP")
        # log_save(0, f"向obs写入推流服务：【Bilibili Live - RTMP | 哔哩哔哩直播 - RTMP】")
        # 写入推流地址
        obs.obs_data_set_string(streaming_service_settings, "server", "rtmp://live-push.bilivideo.com/live-bvc/")
        log_save(0, f"向obs写入推流地址：【rtmp://live-push.bilivideo.com/live-bvc/】")
        # 写入rtmp推流码
        obs.obs_data_set_string(streaming_service_settings, "key", rtmp_push_code)
        log_save(0, f"向obs写入rtmp推流码：【{rtmp_push_code}】")
        # 应用更新
        obs.obs_service_update(streaming_service, streaming_service_settings)
        # 检查是否需要重启推流
        if obs.obs_frontend_streaming_active():
            log_save(0, f"由于：正处于推流状态中】➡️开始重启推流")
            # 停止推流
            log_save(0, f"重启推流第一步：停止推流")
            obs.obs_frontend_streaming_stop()

            # 设置定时器稍后重启
            def restart_streaming():
                """重启推流"""
                if not obs.obs_frontend_streaming_active():
                    log_save(0, f"重启推流第三步：开始推流")
                    obs.obs_frontend_streaming_start()
                    log_save(0, f"重启推流第4️⃣步：关闭重启推流的计时器")
                    obs.remove_current_callback()

            log_save(0, f"重启推流第二步：开启重启推流的计时器，3s间隔")
            obs.timer_add(restart_streaming, 3000)
        else:
            log_save(0, f"由于：当前并未正在推流】➡️直接开始推流")
            obs.obs_frontend_streaming_start()
    # 释放流服务设置
    obs.obs_data_release(streaming_service_settings)
    # 保存到配置文件
    obs.obs_frontend_save_streaming_service()

    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播状态
    live_status = (room_info_old["liveStatus"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播状态】0：未开播 1：直播中"""
    log_save(0, f"║║登录账户 的 直播状态：{(('直播中' if live_status else '未开播') if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")

    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【直播】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╗")
    # 设置 分组框【直播】 可见状态
    widget.Group.live.Visible = bool(room_status)
    log_save(0, f"║║║设置 分组框【直播】 可见状态：{widget.Group.live.Visible}")
    # 设置 分组框【直播】 可用状态
    widget.Group.live.Enabled = bool(room_status)
    log_save(0, f"║║║设置 分组框【直播】 可用状态：{widget.Group.live.Enabled}")

    # 设置 组合框【直播平台】 可见状态
    widget.ComboBox.liveStreamingPlatform.Visible = bool(room_status)
    log_save(0, f"║║║设置 组合框【直播平台】 可见状态：{str(widget.Button.bliveWebJump.Visible)}")
    # 设置 组合框【直播平台】 可用状态
    widget.ComboBox.liveStreamingPlatform.Enabled = True if ((not live_status) and room_status) else False
    log_save(0, f"║║║设置 组合框【直播平台】 可用状态：{str(widget.ComboBox.liveStreamingPlatform.Enabled)}")
    # 设置 组合框【直播平台】 的数据字典
    widget.ComboBox.liveStreamingPlatform.Dictionary = {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}
    log_save(0, f"║║║设置 组合框【直播平台】 的数据字典：{str(widget.ComboBox.liveStreamingPlatform.Dictionary)}")
    # 设置 组合框【直播平台】 的内容
    widget.ComboBox.liveStreamingPlatform.Text = ""
    log_save(0, f"║║║设置 组合框【直播平台】 的内容：{str(widget.ComboBox.liveStreamingPlatform.Text)}")
    # 设置 组合框【直播平台】 的内容 的 列表值
    widget.ComboBox.liveStreamingPlatform.Value = ""
    log_save(0, f"║║║设置 组合框【直播平台】 的内容 的 列表值：{str(widget.ComboBox.liveStreamingPlatform.Value)}")

    # 设置 按钮【开始直播并复制推流码】 可见状态
    widget.Button.liveStart.Visible = True if ((not live_status) and room_status) else False
    log_save(0, f"║║║设置 按钮【开始直播并复制推流码】 可见状态：{str(widget.Button.liveStart.Visible)}")
    # 设置 按钮【开始直播并复制推流码】 可用状态
    widget.Button.liveStart.Enabled = True if ((not live_status) and room_status) else False
    log_save(0, f"║║║设置 按钮【开始直播并复制推流码】 可用状态：{str(widget.Button.liveStart.Enabled)}")

    # 设置 按钮【复制直播服务器】 可见状态
    widget.Button.liveRtmpAddressCopy.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播服务器】 可见状态：{str(widget.Button.liveRtmpAddressCopy.Visible)}")
    # 设置 按钮【复制直播服务器】 可用状态
    widget.Button.liveRtmpAddressCopy.Enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播服务器】 可用状态：{str(widget.Button.liveRtmpAddressCopy.Enabled)}")

    # 设置 按钮【复制直播推流码】 可见状态
    widget.Button.liveRtmpCodeCopy.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播推流码】 可见状态：{str(widget.Button.liveRtmpCodeCopy.Visible)}")
    # 设置 按钮【复制直播推流码】 可用状态
    widget.Button.liveRtmpCodeCopy.Enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播推流码】 可用状态：{str(widget.Button.liveRtmpCodeCopy.Enabled)}")

    # 设置 按钮【更新推流码并复制】 可见状态
    widget.Button.liveRtmpCodeUpdate.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【更新推流码并复制】 可见状态：{str(widget.Button.liveRtmpCodeUpdate.Visible)}")
    # 设置 按钮【更新推流码并复制】 可用状态
    widget.Button.liveRtmpCodeUpdate.Obj_enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【更新推流码并复制】 可用状态：{str(widget.Button.liveRtmpCodeUpdate.Obj_enabled)}")

    # 设置 按钮【结束直播】 可见状态
    widget.Button.liveStop.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【结束直播】 可见状态：{str(widget.Button.liveStop.Visible)}")
    # 设置 按钮【结束直播】 可用状态
    widget.Button.liveStop.Enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【结束直播】 可用状态：{str(widget.Button.liveStop.Enabled)}")
    # 设置 分组框【直播】 中控件属性 结束
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╝")
    # 设置 控件属性 结束
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")


    # 分组框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐分组框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 分组框【直播】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️分组框【直播】 UI")
    # 设置 分组框【直播】 可见状态
    if obs.obs_property_visible(widget.Group.live.Obj) != widget.Group.live.Visible:
        log_save(0, f"　│││✏️ 分组框【直播】 可见状态 发生变动: {obs.obs_property_visible(widget.Group.live.Obj)}➡️{widget.Group.live.Visible}")
        obs.obs_property_set_visible(widget.Group.live.Obj, widget.Group.live.Visible)
    else:
        log_save(0, f"　│││🧩 分组框【直播】 可见状态 未 发生变动")
    # 设置 分组框【直播】 可用状态
    if obs.obs_property_enabled(widget.Group.live.Obj) != widget.Group.live.Enabled:
        log_save(0, f"　│││✏️ 分组框【直播】 可用状态 发生变动: {obs.obs_property_enabled(widget.Group.live.Obj)}➡️{widget.Group.live.Enabled}")
        obs.obs_property_set_enabled(widget.Group.live.Obj, widget.Group.live.Enabled)
    else:
        log_save(0, f"　│││🧩 分组框【直播】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌分组框 UI{30*'─'}┘")

    # 组合框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐组合框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 组合框【直播平台】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【直播平台】 UI")
    # 设置 组合框【直播平台】 可见状态
    if obs.obs_property_visible(widget.ComboBox.liveStreamingPlatform.Obj) != widget.ComboBox.liveStreamingPlatform.Visible:
        log_save(0, f"　│││✏️ 组合框【直播平台】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.liveStreamingPlatform.Obj)}➡️{widget.ComboBox.liveStreamingPlatform.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.liveStreamingPlatform.Obj, widget.ComboBox.liveStreamingPlatform.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【直播平台】 可见状态 未 发生变动")
    # 设置 组合框【直播平台】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.liveStreamingPlatform.Obj) != widget.ComboBox.liveStreamingPlatform.Enabled:
        log_save(0, f"　│││✏️ 组合框【直播平台】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.liveStreamingPlatform.Obj)}➡️{widget.ComboBox.liveStreamingPlatform.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.liveStreamingPlatform.Obj, widget.ComboBox.liveStreamingPlatform.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【直播平台】 可用状态 未 发生变动")
    # 判断 组合框【直播平台】字典数据 和 当前数据是否有变化
    if widget.ComboBox.liveStreamingPlatform.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.liveStreamingPlatform.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveStreamingPlatform.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveStreamingPlatform.Obj))}:
        log_save(0, f"　│││✏️ 组合框【直播平台】 列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.liveStreamingPlatform.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveStreamingPlatform.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveStreamingPlatform.Obj))})}个元素➡️{len(widget.ComboBox.liveStreamingPlatform.Dictionary)}个元素")
        # 清空 组合框【直播平台】
        log_save(0, f"　│││📑 更新 组合框【直播平台】数据 第一步：清空 组合框【直播平台】")
        obs.obs_property_list_clear(widget.ComboBox.liveStreamingPlatform.Obj)
        # 添加 组合框【直播平台】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑 更新 组合框【直播平台】数据 第二步：添加 组合框【直播平台】 列表选项  如果有默认值，会被设置在第一位")
        for LivePlatforms in widget.ComboBox.liveStreamingPlatform.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.liveStreamingPlatform.Obj, widget.ComboBox.liveStreamingPlatform.Dictionary[LivePlatforms], LivePlatforms) if LivePlatforms != widget.ComboBox.liveStreamingPlatform.Value else obs.obs_property_list_insert_string(widget.ComboBox.liveStreamingPlatform.Obj, 0, widget.ComboBox.liveStreamingPlatform.Text, widget.ComboBox.liveStreamingPlatform.Value)
        # 设置 组合框【直播平台】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【直播平台】数据 第三步：更新 组合框【直播平台】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'live_streaming_platform_comboBox', obs.obs_property_list_item_string(widget.ComboBox.liveStreamingPlatform.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【直播平台】 列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌组合框 UI{30*'─'}┘")

    # 按钮+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐按钮 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 按钮【开始直播并复制推流码】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【开始直播并复制推流码】 UI")
    # 设置 按钮【开始直播并复制推流码】 可见状态
    if obs.obs_property_visible(widget.Button.liveStart.Obj) != widget.Button.liveStart.Visible:
        log_save(0, f"　│││✏️ 按钮【开始直播并复制推流码】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveStart.Obj)}➡️{widget.Button.liveStart.Visible}")
        obs.obs_property_set_visible(widget.Button.liveStart.Obj, widget.Button.liveStart.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【开始直播并复制推流码】 可见状态 未 发生变动")
    # 设置 按钮【开始直播并复制推流码】 可用状态
    if obs.obs_property_enabled(widget.Button.liveStart.Obj) != widget.Button.liveStart.Enabled:
        log_save(0, f"　│││✏️ 按钮【开始直播并复制推流码】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveStart.Obj)}➡️{widget.Button.liveStart.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveStart.Obj, widget.Button.liveStart.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【开始直播并复制推流码】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【复制直播服务器】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【复制直播服务器】 UI")
    # 设置 按钮【复制直播服务器】 可见状态
    if obs.obs_property_visible(widget.Button.liveRtmpAddressCopy.Obj) != widget.Button.liveRtmpAddressCopy.Visible:
        log_save(0, f"　│││✏️ 按钮【复制直播服务器】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveRtmpAddressCopy.Obj)}➡️{widget.Button.liveRtmpAddressCopy.Visible}")
        obs.obs_property_set_visible(widget.Button.liveRtmpAddressCopy.Obj, widget.Button.liveRtmpAddressCopy.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播服务器】 可见状态 未 发生变动")
    # 设置 按钮【复制直播服务器】 可用状态
    if obs.obs_property_enabled(widget.Button.liveRtmpAddressCopy.Obj) != widget.Button.liveRtmpAddressCopy.Enabled:
        log_save(0, f"　│││✏️ 按钮【复制直播服务器】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveRtmpAddressCopy.Obj)}➡️{widget.Button.liveRtmpAddressCopy.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveRtmpAddressCopy.Obj, widget.Button.liveRtmpAddressCopy.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播服务器】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【复制直播推流码】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【复制直播推流码】 UI")
    # 设置 按钮【复制直播推流码】 可见状态
    if obs.obs_property_visible(widget.Button.liveRtmpCodeCopy.Obj) != widget.Button.liveRtmpCodeCopy.Visible:
        log_save(0, f"　│││✏️ 按钮【复制直播推流码】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveRtmpCodeCopy.Obj)}➡️{widget.Button.liveRtmpCodeCopy.Visible}")
        obs.obs_property_set_visible(widget.Button.liveRtmpCodeCopy.Obj, widget.Button.liveRtmpCodeCopy.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播推流码】 可见状态 未 发生变动")
    # 设置 按钮【复制直播推流码】 可用状态
    if obs.obs_property_enabled(widget.Button.liveRtmpCodeCopy.Obj) != widget.Button.liveRtmpCodeCopy.Enabled:
        log_save(0, f"　│││✏️ 按钮【复制直播推流码】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveRtmpCodeCopy.Obj)}➡️{widget.Button.liveRtmpCodeCopy.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveRtmpCodeCopy.Obj, widget.Button.liveRtmpCodeCopy.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播推流码】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【更新推流码并复制】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【更新推流码并复制】 UI")
    # 设置 按钮【更新推流码并复制】 可见状态
    if obs.obs_property_visible(widget.Button.liveRtmpCodeUpdate.Obj) != widget.Button.liveRtmpCodeUpdate.Visible:
        log_save(0, f"　│││✏️ 按钮【更新推流码并复制】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveRtmpCodeUpdate.Obj)}➡️{widget.Button.liveRtmpCodeUpdate.Visible}")
        obs.obs_property_set_visible(widget.Button.liveRtmpCodeUpdate.Obj, widget.Button.liveRtmpCodeUpdate.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【更新推流码并复制】 可见状态 未 发生变动")
    # 设置 按钮【更新推流码并复制】 可用状态
    if obs.obs_property_enabled(widget.Button.liveRtmpCodeUpdate.Obj) != widget.Button.liveRtmpCodeUpdate.Obj_enabled:
        log_save(0, f"　│││✏️ 按钮【更新推流码并复制】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveRtmpCodeUpdate.Obj)}➡️{widget.Button.liveRtmpCodeUpdate.Obj_enabled}")
        obs.obs_property_set_enabled(widget.Button.liveRtmpCodeUpdate.Obj, widget.Button.liveRtmpCodeUpdate.Obj_enabled)
    else:
        log_save(0, f"　│││🧩 按钮【更新推流码并复制】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【结束直播】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【结束直播】 UI")
    # 设置 按钮【结束直播】 可见状态
    if obs.obs_property_visible(widget.Button.liveStop.Obj) != widget.Button.liveStop.Visible:
        log_save(0, f"　│││✏️ 按钮【结束直播】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveStop.Obj)}➡️{widget.Button.liveStop.Visible}")
        obs.obs_property_set_visible(widget.Button.liveStop.Obj, widget.Button.liveStop.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【结束直播】 可见状态 未 发生变动")
    # 设置 按钮【结束直播】 可用状态
    if obs.obs_property_enabled(widget.Button.liveStop.Obj) != widget.Button.liveStop.Enabled:
        log_save(0, f"　│││✏️ 按钮【结束直播】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveStop.Obj)}➡️{widget.Button.liveStop.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveStop.Obj, widget.Button.liveStop.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【结束直播】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌按钮 UI{30*'─'}┘")
    return True


def button_function_rtmp_address_copy(props, prop):
    """
    复制直播服务器
    Args:
        props:
        prop:
    Returns:
    """
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    stream_addr = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).get_live_stream_info()
    log_save(0, f"获取直播服务器返回：{stream_addr}")
    if stream_addr["code"] == 0:
        log_save(0, f"获取直播服务器成功")
        log_save(0, f"直播服务器：【{stream_addr['data']['rtmp']['addr']}】")
        cb.copy(stream_addr['data']['rtmp']['addr'])
        log_save(0, f"已将 直播服务器 复制到剪贴板")
    else:
        log_save(3, f"获取直播服务器失败：{stream_addr['error']}")
    return True


def button_function_rtmp_stream_code_copy(props, prop):
    """
    复制直播推流码
    Args:
        props:
        prop:
    Returns:
    """
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    stream_addr = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).get_live_stream_info()
    log_save(0, f"获取直播推流码返回：{stream_addr}")
    if stream_addr["code"] == 0:
        log_save(0, f"获取直播推流码成功")
        log_save(0, f"直播推流码：【{stream_addr['data']['rtmp']['code']}】")
        cb.copy(stream_addr['data']['rtmp']['code'])
        log_save(0, f"已将 直播推流码 复制到剪贴板")
    else:
        log_save(3, f"获取直播推流码失败：{stream_addr['message']}")
        return False
    return True


def button_function_rtmp_stream_code_update(props, prop):
    """
    更新推流码并复制
    Args:
        props:
        prop:
    Returns:
    """
    # 获取开播平台
    live_streaming_platform = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_streaming_platform_comboBox')
    log_save(0, f"使用【{live_streaming_platform}】平台 开播")
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    stream_addr = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).fetch_stream_addr(live_streaming_platform, True)
    log_save(0, f"更新直播推流码返回：{stream_addr}")
    if stream_addr["code"] == 0:
        log_save(0, f"更新直播推流码成功")
        log_save(0, f"直播推流码：【{stream_addr['data']['addr']['code']}】")
        cb.copy(stream_addr['data']['addr']['code'])
        log_save(0, f"已将 直播推流码 复制到剪贴板")
    else:
        log_save(3, f"更新直播推流码失败：{stream_addr['message']}")
        return False
    # 重新开播
    button_function_stop_live()
    return True


def button_function_stop_live():
    """
    结束直播
    """
    # 停止推流
    if obs.obs_frontend_streaming_active():
        log_save(0, f"停止推流")
        obs.obs_frontend_streaming_stop()

    # 获取开播平台
    live_streaming_platform = obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_streaming_platform_comboBox')
    log_save(0, f"使用【{live_streaming_platform}】平台 开播")


    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    stop_live = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).stop_live(live_streaming_platform)
    log_save(0, f"停播返回：{stop_live}")
    if stop_live["code"] == 0:
        log_save(0, f"停播成功。")
    else:
        log_save(3, f"停播失败：【{stop_live['message']}】。")
        return False

    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播状态
    live_status = (room_info_old["liveStatus"] if room_status else None) if b_u_l_c.get_cookies() else None
    """登录用户的直播状态】0：未开播 1：直播中"""
    log_save(0, f"║║登录账户 的 直播状态：{(('直播中' if live_status else '未开播') if room_status else '⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")

    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【直播】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╗")
    # 设置 分组框【直播】 可见状态
    widget.Group.live.Visible = bool(room_status)
    log_save(0, f"║║║设置 分组框【直播】 可见状态：{widget.Group.live.Visible}")
    # 设置 分组框【直播】 可用状态
    widget.Group.live.Enabled = bool(room_status)
    log_save(0, f"║║║设置 分组框【直播】 可用状态：{widget.Group.live.Enabled}")

    # 设置 组合框【直播平台】 可见状态
    widget.ComboBox.liveStreamingPlatform.Visible = bool(room_status)
    log_save(0, f"║║║设置 组合框【直播平台】 可见状态：{str(widget.Button.bliveWebJump.Visible)}")
    # 设置 组合框【直播平台】 可用状态
    widget.ComboBox.liveStreamingPlatform.Enabled = True if ((not live_status) and room_status) else False
    log_save(0, f"║║║设置 组合框【直播平台】 可用状态：{str(widget.ComboBox.liveStreamingPlatform.Enabled)}")
    # 设置 组合框【直播平台】 的数据字典
    widget.ComboBox.liveStreamingPlatform.Dictionary = {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}
    log_save(0, f"║║║设置 组合框【直播平台】 的数据字典：{str(widget.ComboBox.liveStreamingPlatform.Dictionary)}")
    # 设置 组合框【直播平台】 的内容
    widget.ComboBox.liveStreamingPlatform.Text = ""
    log_save(0, f"║║║设置 组合框【直播平台】 的内容：{str(widget.ComboBox.liveStreamingPlatform.Text)}")
    # 设置 组合框【直播平台】 的内容 的 列表值
    widget.ComboBox.liveStreamingPlatform.Value = ""
    log_save(0, f"║║║设置 组合框【直播平台】 的内容 的 列表值：{str(widget.ComboBox.liveStreamingPlatform.Value)}")

    # 设置 按钮【开始直播并复制推流码】 可见状态
    widget.Button.liveStart.Visible = True if ((not live_status) and room_status) else False
    log_save(0, f"║║║设置 按钮【开始直播并复制推流码】 可见状态：{str(widget.Button.liveStart.Visible)}")
    # 设置 按钮【开始直播并复制推流码】 可用状态
    widget.Button.liveStart.Enabled = True if ((not live_status) and room_status) else False
    log_save(0, f"║║║设置 按钮【开始直播并复制推流码】 可用状态：{str(widget.Button.liveStart.Enabled)}")

    # 设置 按钮【复制直播服务器】 可见状态
    widget.Button.liveRtmpAddressCopy.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播服务器】 可见状态：{str(widget.Button.liveRtmpAddressCopy.Visible)}")
    # 设置 按钮【复制直播服务器】 可用状态
    widget.Button.liveRtmpAddressCopy.Enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播服务器】 可用状态：{str(widget.Button.liveRtmpAddressCopy.Enabled)}")

    # 设置 按钮【复制直播推流码】 可见状态
    widget.Button.liveRtmpCodeCopy.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播推流码】 可见状态：{str(widget.Button.liveRtmpCodeCopy.Visible)}")
    # 设置 按钮【复制直播推流码】 可用状态
    widget.Button.liveRtmpCodeCopy.Enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【复制直播推流码】 可用状态：{str(widget.Button.liveRtmpCodeCopy.Enabled)}")

    # 设置 按钮【更新推流码并复制】 可见状态
    widget.Button.liveRtmpCodeUpdate.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【更新推流码并复制】 可见状态：{str(widget.Button.liveRtmpCodeUpdate.Visible)}")
    # 设置 按钮【更新推流码并复制】 可用状态
    widget.Button.liveRtmpCodeUpdate.Obj_enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【更新推流码并复制】 可用状态：{str(widget.Button.liveRtmpCodeUpdate.Obj_enabled)}")

    # 设置 按钮【结束直播】 可见状态
    widget.Button.liveStop.Visible = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【结束直播】 可见状态：{str(widget.Button.liveStop.Visible)}")
    # 设置 按钮【结束直播】 可用状态
    widget.Button.liveStop.Enabled = True if (live_status and room_status) else False
    log_save(0, f"║║║设置 按钮【结束直播】 可用状态：{str(widget.Button.liveStop.Enabled)}")
    # 设置 分组框【直播】 中控件属性 结束
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╝")
    # 设置 控件属性 结束
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")


    # 分组框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐分组框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 分组框【直播】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️分组框【直播】 UI")
    # 设置 分组框【直播】 可见状态
    if obs.obs_property_visible(widget.Group.live.Obj) != widget.Group.live.Visible:
        log_save(0, f"　│││✏️ 分组框【直播】 可见状态 发生变动: {obs.obs_property_visible(widget.Group.live.Obj)}➡️{widget.Group.live.Visible}")
        obs.obs_property_set_visible(widget.Group.live.Obj, widget.Group.live.Visible)
    else:
        log_save(0, f"　│││🧩 分组框【直播】 可见状态 未 发生变动")
    # 设置 分组框【直播】 可用状态
    if obs.obs_property_enabled(widget.Group.live.Obj) != widget.Group.live.Enabled:
        log_save(0, f"　│││✏️ 分组框【直播】 可用状态 发生变动: {obs.obs_property_enabled(widget.Group.live.Obj)}➡️{widget.Group.live.Enabled}")
        obs.obs_property_set_enabled(widget.Group.live.Obj, widget.Group.live.Enabled)
    else:
        log_save(0, f"　│││🧩 分组框【直播】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌分组框 UI{30*'─'}┘")

    # 组合框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐组合框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 组合框【直播平台】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【直播平台】 UI")
    # 设置 组合框【直播平台】 可见状态
    if obs.obs_property_visible(widget.ComboBox.liveStreamingPlatform.Obj) != widget.ComboBox.liveStreamingPlatform.Visible:
        log_save(0, f"　│││✏️ 组合框【直播平台】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.liveStreamingPlatform.Obj)}➡️{widget.ComboBox.liveStreamingPlatform.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.liveStreamingPlatform.Obj, widget.ComboBox.liveStreamingPlatform.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【直播平台】 可见状态 未 发生变动")
    # 设置 组合框【直播平台】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.liveStreamingPlatform.Obj) != widget.ComboBox.liveStreamingPlatform.Enabled:
        log_save(0, f"　│││✏️ 组合框【直播平台】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.liveStreamingPlatform.Obj)}➡️{widget.ComboBox.liveStreamingPlatform.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.liveStreamingPlatform.Obj, widget.ComboBox.liveStreamingPlatform.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【直播平台】 可用状态 未 发生变动")
    # 判断 组合框【直播平台】字典数据 和 当前数据是否有变化
    if widget.ComboBox.liveStreamingPlatform.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.liveStreamingPlatform.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveStreamingPlatform.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveStreamingPlatform.Obj))}:
        log_save(0, f"　│││✏️ 组合框【直播平台】 列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.liveStreamingPlatform.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveStreamingPlatform.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveStreamingPlatform.Obj))})}个元素➡️{len(widget.ComboBox.liveStreamingPlatform.Dictionary)}个元素")
        # 清空 组合框【直播平台】
        log_save(0, f"　│││📑 更新 组合框【直播平台】数据 第一步：清空 组合框【直播平台】")
        obs.obs_property_list_clear(widget.ComboBox.liveStreamingPlatform.Obj)
        # 添加 组合框【直播平台】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑 更新 组合框【直播平台】数据 第二步：添加 组合框【直播平台】 列表选项  如果有默认值，会被设置在第一位")
        for LivePlatforms in widget.ComboBox.liveStreamingPlatform.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.liveStreamingPlatform.Obj, widget.ComboBox.liveStreamingPlatform.Dictionary[LivePlatforms], LivePlatforms) if LivePlatforms != widget.ComboBox.liveStreamingPlatform.Value else obs.obs_property_list_insert_string(widget.ComboBox.liveStreamingPlatform.Obj, 0, widget.ComboBox.liveStreamingPlatform.Text, widget.ComboBox.liveStreamingPlatform.Value)
        # 设置 组合框【直播平台】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【直播平台】数据 第三步：更新 组合框【直播平台】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'live_streaming_platform_comboBox', obs.obs_property_list_item_string(widget.ComboBox.liveStreamingPlatform.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【直播平台】 列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌组合框 UI{30*'─'}┘")

    # 按钮+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐按钮 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 按钮【开始直播并复制推流码】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【开始直播并复制推流码】 UI")
    # 设置 按钮【开始直播并复制推流码】 可见状态
    if obs.obs_property_visible(widget.Button.liveStart.Obj) != widget.Button.liveStart.Visible:
        log_save(0, f"　│││✏️ 按钮【开始直播并复制推流码】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveStart.Obj)}➡️{widget.Button.liveStart.Visible}")
        obs.obs_property_set_visible(widget.Button.liveStart.Obj, widget.Button.liveStart.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【开始直播并复制推流码】 可见状态 未 发生变动")
    # 设置 按钮【开始直播并复制推流码】 可用状态
    if obs.obs_property_enabled(widget.Button.liveStart.Obj) != widget.Button.liveStart.Enabled:
        log_save(0, f"　│││✏️ 按钮【开始直播并复制推流码】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveStart.Obj)}➡️{widget.Button.liveStart.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveStart.Obj, widget.Button.liveStart.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【开始直播并复制推流码】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【复制直播服务器】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【复制直播服务器】 UI")
    # 设置 按钮【复制直播服务器】 可见状态
    if obs.obs_property_visible(widget.Button.liveRtmpAddressCopy.Obj) != widget.Button.liveRtmpAddressCopy.Visible:
        log_save(0, f"　│││✏️ 按钮【复制直播服务器】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveRtmpAddressCopy.Obj)}➡️{widget.Button.liveRtmpAddressCopy.Visible}")
        obs.obs_property_set_visible(widget.Button.liveRtmpAddressCopy.Obj, widget.Button.liveRtmpAddressCopy.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播服务器】 可见状态 未 发生变动")
    # 设置 按钮【复制直播服务器】 可用状态
    if obs.obs_property_enabled(widget.Button.liveRtmpAddressCopy.Obj) != widget.Button.liveRtmpAddressCopy.Enabled:
        log_save(0, f"　│││✏️ 按钮【复制直播服务器】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveRtmpAddressCopy.Obj)}➡️{widget.Button.liveRtmpAddressCopy.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveRtmpAddressCopy.Obj, widget.Button.liveRtmpAddressCopy.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播服务器】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【复制直播推流码】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【复制直播推流码】 UI")
    # 设置 按钮【复制直播推流码】 可见状态
    if obs.obs_property_visible(widget.Button.liveRtmpCodeCopy.Obj) != widget.Button.liveRtmpCodeCopy.Visible:
        log_save(0, f"　│││✏️ 按钮【复制直播推流码】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveRtmpCodeCopy.Obj)}➡️{widget.Button.liveRtmpCodeCopy.Visible}")
        obs.obs_property_set_visible(widget.Button.liveRtmpCodeCopy.Obj, widget.Button.liveRtmpCodeCopy.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播推流码】 可见状态 未 发生变动")
    # 设置 按钮【复制直播推流码】 可用状态
    if obs.obs_property_enabled(widget.Button.liveRtmpCodeCopy.Obj) != widget.Button.liveRtmpCodeCopy.Enabled:
        log_save(0, f"　│││✏️ 按钮【复制直播推流码】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveRtmpCodeCopy.Obj)}➡️{widget.Button.liveRtmpCodeCopy.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveRtmpCodeCopy.Obj, widget.Button.liveRtmpCodeCopy.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【复制直播推流码】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【更新推流码并复制】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【更新推流码并复制】 UI")
    # 设置 按钮【更新推流码并复制】 可见状态
    if obs.obs_property_visible(widget.Button.liveRtmpCodeUpdate.Obj) != widget.Button.liveRtmpCodeUpdate.Visible:
        log_save(0, f"　│││✏️ 按钮【更新推流码并复制】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveRtmpCodeUpdate.Obj)}➡️{widget.Button.liveRtmpCodeUpdate.Visible}")
        obs.obs_property_set_visible(widget.Button.liveRtmpCodeUpdate.Obj, widget.Button.liveRtmpCodeUpdate.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【更新推流码并复制】 可见状态 未 发生变动")
    # 设置 按钮【更新推流码并复制】 可用状态
    if obs.obs_property_enabled(widget.Button.liveRtmpCodeUpdate.Obj) != widget.Button.liveRtmpCodeUpdate.Obj_enabled:
        log_save(0, f"　│││✏️ 按钮【更新推流码并复制】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveRtmpCodeUpdate.Obj)}➡️{widget.Button.liveRtmpCodeUpdate.Obj_enabled}")
        obs.obs_property_set_enabled(widget.Button.liveRtmpCodeUpdate.Obj, widget.Button.liveRtmpCodeUpdate.Obj_enabled)
    else:
        log_save(0, f"　│││🧩 按钮【更新推流码并复制】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 按钮【结束直播】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️按钮【结束直播】 UI")
    # 设置 按钮【结束直播】 可见状态
    if obs.obs_property_visible(widget.Button.liveStop.Obj) != widget.Button.liveStop.Visible:
        log_save(0, f"　│││✏️ 按钮【结束直播】 可见状态 发生变动: {obs.obs_property_visible(widget.Button.liveStop.Obj)}➡️{widget.Button.liveStop.Visible}")
        obs.obs_property_set_visible(widget.Button.liveStop.Obj, widget.Button.liveStop.Visible)
    else:
        log_save(0, f"　│││🧩 按钮【结束直播】 可见状态 未 发生变动")
    # 设置 按钮【结束直播】 可用状态
    if obs.obs_property_enabled(widget.Button.liveStop.Obj) != widget.Button.liveStop.Enabled:
        log_save(0, f"　│││✏️ 按钮【结束直播】 可用状态 发生变动: {obs.obs_property_enabled(widget.Button.liveStop.Obj)}➡️{widget.Button.liveStop.Enabled}")
        obs.obs_property_set_enabled(widget.Button.liveStop.Obj, widget.Button.liveStop.Enabled)
    else:
        log_save(0, f"　│││🧩 按钮【结束直播】 可用状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌按钮 UI{30*'─'}┘")
    return True


def button_function_true_live_appointment_day():
    """确认预约天"""
    appointment_day_int = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "live_bookings_day_digitalSlider")
    appointment_day_digital_slider_min = obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj)
    appointment_day_digital_slider_max = obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj)
    appointment_hour_int = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "live_bookings_hour_digitalSlider")
    appointment_hour_digital_slider_min = obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj)
    appointment_hour_digital_slider_max = obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj)
    appointment_minute_int = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "live_bookings_minute_digitalSlider")
    appointment_minute_digital_slider_min = obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsMinute.Obj)
    appointment_minute_digital_slider_max = obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsMinute.Obj)

    if appointment_day_int == 180 and (appointment_hour_digital_slider_min != 0 or appointment_hour_digital_slider_max != 0 or appointment_minute_digital_slider_min != 0 or appointment_minute_digital_slider_max != 0):
        log_save(0, f"由于【预约天】等于180天了，所以将【预约时】和【预约分】锁定为：0")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsHour.Obj, 0, 0, 0)
        if appointment_hour_int > 0:
            obs.obs_data_set_int(GlobalVariableOfData.script_settings, "live_bookings_hour_digitalSlider", 0)
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsMinute.Obj, 0, 0, 0)
        if appointment_minute_int > 0:
            obs.obs_data_set_int(GlobalVariableOfData.script_settings, "live_bookings_minute_digitalSlider", 0)
        return True

    if (((0 < appointment_day_int < 180) and appointment_hour_int <= 23) or (appointment_day_int == 0 and (0 < appointment_hour_int <= 23))) and (appointment_hour_digital_slider_min != 0 or appointment_hour_digital_slider_max != 23 or appointment_minute_digital_slider_min != 0 or appointment_minute_digital_slider_max != 59):
        log_save(0, f"由于【预约天】不为180天，且【预约天】和【预约时】其中一个不为0 所以将【预约分】最低值设定为：0")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsHour.Obj, 0, 23, 1)
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsMinute.Obj, 0, 59, 1)
        return True

    if appointment_day_int == 0 and appointment_hour_int == 0 and (appointment_hour_digital_slider_min != 0 or appointment_hour_digital_slider_max != 23 or appointment_minute_digital_slider_min != 5 or appointment_minute_digital_slider_max != 59):
        log_save(0, f"【预约天】和【预约时】其中均为0 所以将【预约分】最低值设定为：5")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsHour.Obj, 0, 23, 1)
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsMinute.Obj, 5, 59, 1)
        if appointment_minute_int < 5:
            obs.obs_data_set_int(GlobalVariableOfData.script_settings, "live_bookings_minute_digitalSlider", 5)
        return True
    return False


def button_function_true_live_appointment_hour():
    return button_function_true_live_appointment_day()


def button_function_true_live_appointment_minute():
    return button_function_true_live_appointment_day()


def button_function_creat_live_appointment(props, prop):
    """创建直播预约"""
    # 获取直播预约天
    live_bookings_day = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "live_bookings_day_digitalSlider")
    log_save(0, f"直播预约天: {live_bookings_day}")
    # 获取直播预约时
    live_bookings_hour = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "live_bookings_hour_digitalSlider")
    log_save(0, f"直播预约时: {live_bookings_hour}")
    # 获取直播预约分
    live_bookings_minute = obs.obs_data_get_int(GlobalVariableOfData.script_settings, "live_bookings_minute_digitalSlider")
    log_save(0, f"直播预约分: {live_bookings_minute}")
    # 限制直播时间内范围
    if not (5 <= (live_bookings_day*24*60 + live_bookings_hour*60 + live_bookings_minute) <= 180*24*60):
        log_save(3, f"直播预约时间: {live_bookings_day}天{live_bookings_hour}时{live_bookings_minute}分，需要大于 5min 以及 小于 59day")
        return False
    else:
        log_save(0, f"直播预约时间: {live_bookings_day}天{live_bookings_hour}时{live_bookings_minute}分")
    # live_bookings_time = get_future_timestamp(live_bookings_day, live_bookings_hour, live_bookings_minute)
    # log_save(0, f"直播预约时间戳: {live_bookings_time}，时间: {datetime.fromtimestamp(live_bookings_time)}")
    # 获取直播预约标题
    live_bookings_title = obs.obs_data_get_string(GlobalVariableOfData.script_settings, "live_bookings_title_textBox")
    log_save(0, f"直播预约标题: {live_bookings_title}")
    # 获取是否发动态
    live_bookings_dynamic_is = obs.obs_data_get_bool(GlobalVariableOfData.script_settings, "live_bookings_dynamic_bool")
    log_save(0, f"直播预约是否发动态: {live_bookings_dynamic_is}")
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 创建直播预约
    create_reserve_return = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=
        dict2cookie(b_u_l_c.get_cookies())).create_reserve(title = live_bookings_title, live_plan_start_time = get_future_timestamp(live_bookings_day, live_bookings_hour, live_bookings_minute), create_dynamic = live_bookings_dynamic_is)
    log_save(0, f"创建直播预约返回: {create_reserve_return}")
    if create_reserve_return['code'] == 0:
        log_save(0, f"创建直播预约成功")
    else:
        log_save(3, f"创建直播预约失败: {create_reserve_return['message']}")
        if create_reserve_return['code'] == -400:
            log_save(3, f"直播预约标题错误: 【{live_bookings_title}】")
        return False

    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    log_save(0, f"║║")
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 登录用户的直播预约列表信息
    reserve_list = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).get_reserve_list()
    """获取 '登录用户' 的 直播预约列表信息"""
    log_save(0, f"║║登录账户 的 直播预约列表信息：{(reserve_list if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 登录用户的直播预约字典
    reserve_name4reserve_sid = (({str(reserve['reserve_info']['sid']): f"{reserve['reserve_info']['name']}|{datetime.fromtimestamp(reserve['reserve_info']['live_plan_start_time'])}" for reserve in reserve_list} if reserve_list else {"-1": "无直播预约"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """获取 '登录用户' 的 直播预约字典"""
    log_save(0, f"║║登录账户 的 直播预约：{(list(reserve_name4reserve_sid.values()) if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    log_save(0, f"║")
    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【直播】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╗")
    # 设置 数字滑块【预约天】 可见状态
    widget.DigitalDisplay.liveBookingsDay.Visible = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约天】 可见状态：{str(widget.DigitalDisplay.liveBookingsDay.Visible)}")
    # 设置 数字滑块【预约天】 可用状态
    widget.DigitalDisplay.liveBookingsDay.Enabled = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约天】 可用状态：{str(widget.DigitalDisplay.liveBookingsDay.Enabled)}")
    # 设置 数字滑块【预约天】 显示选项值
    widget.DigitalDisplay.liveBookingsDay.Value = 0
    log_save(0, f"║║║设置 数字滑块【预约天】 显示选项值：{str(widget.DigitalDisplay.liveBookingsDay.Value)}")
    # 设置 数字滑块【预约天】 最小值
    widget.DigitalDisplay.liveBookingsDay.Min = 0
    log_save(0, f"║║║设置 数字滑块【预约天】 最小值：{str(widget.DigitalDisplay.liveBookingsDay.Min)}")
    # 设置 数字滑块【预约天】 最大值
    widget.DigitalDisplay.liveBookingsDay.Max = 180
    log_save(0, f"║║║设置 数字滑块【预约天】 最大值：{str(widget.DigitalDisplay.liveBookingsDay.Max)}")
    # 设置 数字滑块【预约天】 步长
    widget.DigitalDisplay.liveBookingsDay.Step = 1
    log_save(0, f"║║║设置 数字滑块【预约天】 步长：{str(widget.DigitalDisplay.liveBookingsDay.Step)}")

    # 设置 数字滑块【预约时】 可见状态
    widget.DigitalDisplay.liveBookingsHour.Visible = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约时】 可见状态：{str(widget.DigitalDisplay.liveBookingsHour.Visible)}")
    # 设置 数字滑块【预约时】 可用状态
    widget.DigitalDisplay.liveBookingsHour.Enabled = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约时】 可用状态：{str(widget.DigitalDisplay.liveBookingsHour.Enabled)}")
    # 设置 数字滑块【预约时】 显示选项值
    widget.DigitalDisplay.liveBookingsHour.Value = 0
    log_save(0, f"║║║设置 数字滑块【预约时】 显示选项值：{str(widget.DigitalDisplay.liveBookingsHour.Value)}")
    # 设置 数字滑块【预约时】 最小值
    widget.DigitalDisplay.liveBookingsHour.Min = 0
    log_save(0, f"║║║设置 数字滑块【预约时】 最小值：{str(widget.DigitalDisplay.liveBookingsHour.Min)}")
    # 设置 数字滑块【预约时】 最大值
    widget.DigitalDisplay.liveBookingsHour.Max = 23
    log_save(0, f"║║║设置 数字滑块【预约时】 最大值：{str(widget.DigitalDisplay.liveBookingsHour.Max)}")
    # 设置 数字滑块【预约时】 步长
    widget.DigitalDisplay.liveBookingsHour.Step = 1
    log_save(0, f"║║║设置 数字滑块【预约时】 步长：{str(widget.DigitalDisplay.liveBookingsHour.Step)}")

    # 设置 数字滑块【预约分】 可见状态
    widget.DigitalDisplay.liveBookingsMinute.Visible = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约分】 可见状态：{str(widget.DigitalDisplay.liveBookingsMinute.Visible)}")
    # 设置 数字滑块【预约分】 可用状态
    widget.DigitalDisplay.liveBookingsMinute.Enabled = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约分】 可用状态：{str(widget.DigitalDisplay.liveBookingsMinute.Enabled)}")
    # 设置 数字滑块【预约分】 显示选项值
    widget.DigitalDisplay.liveBookingsMinute.Value = 5
    log_save(0, f"║║║设置 数字滑块【预约分】 显示选项值：{str(widget.DigitalDisplay.liveBookingsMinute.Value)}")
    # 设置 数字滑块【预约分】 最小值
    widget.DigitalDisplay.liveBookingsMinute.Min = 5
    log_save(0, f"║║║设置 数字滑块【预约分】 最小值：{str(widget.DigitalDisplay.liveBookingsMinute.Min)}")
    # 设置 数字滑块【预约分】 最大值
    widget.DigitalDisplay.liveBookingsMinute.Max = 59
    log_save(0, f"║║║设置 数字滑块【预约分】 最大值：{str(widget.DigitalDisplay.liveBookingsMinute.Max)}")
    # 设置 数字滑块【预约分】 步长
    widget.DigitalDisplay.liveBookingsMinute.Step = 1
    log_save(0, f"║║║设置 数字滑块【预约分】 步长：{str(widget.DigitalDisplay.liveBookingsMinute.Step)}")

    # 设置 复选框【是否发直播预约动态】 可见状态
    widget.CheckBox.liveBookingsDynamic.Visible =bool(room_status)
    log_save(0, f"║║║设置 复选框【是否发直播预约动态】 可见状态：{str(widget.CheckBox.liveBookingsDynamic.Visible)}")
    # 设置 普通文本框【是否发直播预约动态】 可用状态
    widget.CheckBox.liveBookingsDynamic.Enabled = bool(room_status)
    log_save(0, f"║║║设置 复选框【是否发直播预约动态】 可用状态：{str(widget.CheckBox.liveBookingsDynamic.Enabled)}")
    # 设置 普通文本框【是否发直播预约动态】 内容
    widget.CheckBox.liveBookingsDynamic.Bool = False
    log_save(0, f"║║║设置 复选框【是否发直播预约动态】 选中状态：{str(widget.CheckBox.liveBookingsDynamic.Bool)}")

    # 设置 普通文本框【直播预约标题】 可见状态
    widget.TextBox.liveBookingsTitle.Visible = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播预约标题】 可见状态：{str(widget.TextBox.liveBookingsTitle.Visible)}")
    # 设置 普通文本框【直播预约标题】 可用状态
    widget.TextBox.liveBookingsTitle.Enabled = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播预约标题】 可用状态：{str(widget.TextBox.liveBookingsTitle.Enabled)}")
    # 设置 普通文本框【直播预约标题】 内容
    widget.TextBox.liveBookingsTitle.Text = ""
    log_save(0, f"║║║设置 普通文本框【直播预约标题】 内容：{str(widget.TextBox.liveBookingsTitle.Text)}")

    # 设置 组合框【直播预约列表】 可见状态
    widget.ComboBox.liveBookings.Visible = True
    log_save(0, f"║║║设置 组合框【直播预约列表】 可见状态：{str(widget.ComboBox.liveBookings.Visible)}")
    # 设置 组合框【直播预约列表】 可用状态
    widget.ComboBox.liveBookings.Enabled = True
    log_save(0, f"║║║设置 组合框【直播预约列表】 可用状态：{str(widget.ComboBox.liveBookings.Enabled)}")
    # 设置 组合框【直播预约列表】 的数据字典
    widget.ComboBox.liveBookings.Dictionary = reserve_name4reserve_sid
    log_save(0, f"║║║设置 组合框【直播预约列表】 的数据字典：{str(widget.ComboBox.liveBookings.Dictionary)}")
    # 设置 组合框【直播预约列表】 的内容
    widget.ComboBox.liveBookings.Text = ""
    log_save(0, f"║║║设置 组合框【直播预约列表】 的内容：{str(widget.ComboBox.liveBookings.Text)}")
    # 设置 组合框【直播预约列表】 的内容 的 列表值
    widget.ComboBox.liveBookings.Value = ""
    log_save(0, f"║║║设置 组合框【直播预约列表】 的内容 的 列表值：{str(widget.ComboBox.liveBookings.Value)}")
    # 设置 分组框【直播】 中控件属性 结束
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╝")
    # 设置 控件属性 结束
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")

    # 数字滑块+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐数字滑块 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 数字滑块【预约天】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️数字滑块【预约天】 UI")
    # 设置 数字滑块【预约天】 可见状态
    if obs.obs_property_visible(widget.DigitalDisplay.liveBookingsDay.Obj) != widget.DigitalDisplay.liveBookingsDay.Visible:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 可见状态 发生变动: {obs.obs_property_visible(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Visible}")
        obs.obs_property_set_visible(widget.DigitalDisplay.liveBookingsDay.Obj, widget.DigitalDisplay.liveBookingsDay.Visible)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约天】 可见状态 未 发生变动")
    # 设置 数字滑块【预约天】 可用状态
    if obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsDay.Obj) != widget.DigitalDisplay.liveBookingsDay.Enabled:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 可用状态 发生变动: {obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Enabled}")
        obs.obs_property_set_enabled(widget.DigitalDisplay.liveBookingsDay.Obj, widget.DigitalDisplay.liveBookingsDay.Enabled)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约天】 可用状态 未 发生变动")
    if widget.DigitalDisplay.liveBookingsDay.Min != obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj) or widget.DigitalDisplay.liveBookingsDay.Max != obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj) or widget.DigitalDisplay.liveBookingsDay.Step != obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsDay.Obj):
        log_save(0, f"　│││✏️ 数字滑块【预约天】 最小值/最大值/步长 发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Min}/{widget.DigitalDisplay.liveBookingsDay.Max}/{widget.DigitalDisplay.liveBookingsDay.Step}")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsDay.Obj, widget.DigitalDisplay.liveBookingsDay.Min, widget.DigitalDisplay.liveBookingsDay.Max, widget.DigitalDisplay.liveBookingsDay.Step)
    else:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 最小值/最大值/步长 未发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Min}/{widget.DigitalDisplay.liveBookingsDay.Max}/{widget.DigitalDisplay.liveBookingsDay.Step}")
        log_save(0, f"　│││🧩 数字滑块【预约天】 最小值/最大值/步长 未 发生变动")
    # 设置 数字滑块【预约天】 显示选项值
    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_day_digitalSlider') != widget.DigitalDisplay.liveBookingsDay.Value:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 显示选项值 发生变动: {obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_day_digitalSlider')}➡️{widget.DigitalDisplay.liveBookingsDay.Value}")
        obs.obs_data_set_int(GlobalVariableOfData.script_settings, 'live_bookings_day_digitalSlider', widget.DigitalDisplay.liveBookingsDay.Value)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约天】 显示选项值 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 数字滑块【预约时】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️数字滑块【预约时】 UI")
    # 设置 数字滑块【预约时】 可见状态
    if obs.obs_property_visible(widget.DigitalDisplay.liveBookingsHour.Obj) != widget.DigitalDisplay.liveBookingsHour.Visible:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 可见状态 发生变动: {obs.obs_property_visible(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Visible}")
        obs.obs_property_set_visible(widget.DigitalDisplay.liveBookingsHour.Obj, widget.DigitalDisplay.liveBookingsHour.Visible)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约时】 可见状态 未 发生变动")
    # 设置 数字滑块【预约时】 可用状态
    if obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsHour.Obj) != widget.DigitalDisplay.liveBookingsHour.Enabled:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 可用状态 发生变动: {obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Enabled}")
        obs.obs_property_set_enabled(widget.DigitalDisplay.liveBookingsHour.Obj, widget.DigitalDisplay.liveBookingsHour.Enabled)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约时】 可用状态 未 发生变动")
    if widget.DigitalDisplay.liveBookingsHour.Min != obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj) or widget.DigitalDisplay.liveBookingsHour.Max != obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj) or widget.DigitalDisplay.liveBookingsHour.Step != obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsHour.Obj):
        log_save(0, f"　│││✏️ 数字滑块【预约时】 最小值/最大值/步长 发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Min}/{widget.DigitalDisplay.liveBookingsHour.Max}/{widget.DigitalDisplay.liveBookingsHour.Step}")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsHour.Obj, widget.DigitalDisplay.liveBookingsHour.Min, widget.DigitalDisplay.liveBookingsHour.Max, widget.DigitalDisplay.liveBookingsHour.Step)
    else:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 最小值/最大值/步长 未发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Min}/{widget.DigitalDisplay.liveBookingsHour.Max}/{widget.DigitalDisplay.liveBookingsHour.Step}")
        log_save(0, f"　│││🧩 数字滑块【预约时】 最小值/最大值/步长 未 发生变动")
    # 设置 数字滑块【预约时】 显示选项值
    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_hour_digitalSlider') != widget.DigitalDisplay.liveBookingsHour.Value:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 显示选项值 发生变动: {obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_hour_digitalSlider')}➡️{widget.DigitalDisplay.liveBookingsHour.Value}")
        obs.obs_data_set_int(GlobalVariableOfData.script_settings, 'live_bookings_hour_digitalSlider', widget.DigitalDisplay.liveBookingsHour.Value)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约时】 显示选项值 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 数字滑块【预约分】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️数字滑块【预约分】 UI")
    # 设置 数字滑块【预约分】 可见状态
    if obs.obs_property_visible(widget.DigitalDisplay.liveBookingsMinute.Obj) != widget.DigitalDisplay.liveBookingsMinute.Visible:
        log_save(0, f"　│││✏️ 数字滑块【预约分】 可见状态 发生变动: {obs.obs_property_visible(widget.DigitalDisplay.liveBookingsMinute.Obj)}➡️{widget.DigitalDisplay.liveBookingsMinute.Visible}")
        obs.obs_property_set_visible(widget.DigitalDisplay.liveBookingsMinute.Obj, widget.DigitalDisplay.liveBookingsMinute.Visible)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 可见状态 未 发生变动")
    # 设置 数字滑块【预约分】 可用状态
    if obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsMinute.Obj) != widget.DigitalDisplay.liveBookingsMinute.Enabled:
        log_save(0, f"　│││✏️ 数字滑块【预约分】 可用状态 发生变动: {obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsMinute.Obj)}➡️{widget.DigitalDisplay.liveBookingsMinute.Enabled}")
        obs.obs_property_set_enabled(widget.DigitalDisplay.liveBookingsMinute.Obj, widget.DigitalDisplay.liveBookingsMinute.Enabled)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 可用状态 未 发生变动")
    if widget.DigitalDisplay.liveBookingsMinute.Min != obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsMinute.Obj) or widget.DigitalDisplay.liveBookingsMinute.Max != obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsMinute.Obj) or widget.DigitalDisplay.liveBookingsMinute.Step != obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsMinute.Obj):
        log_save(0, f"　│││✏️ 数字滑块【预约分】 最小值/最大值/步长 发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsMinute.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsMinute.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsMinute.Obj)}➡️{widget.DigitalDisplay.liveBookingsMinute.Min}/{widget.DigitalDisplay.liveBookingsMinute.Max}/{widget.DigitalDisplay.liveBookingsMinute.Step}")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsMinute.Obj, widget.DigitalDisplay.liveBookingsMinute.Min, widget.DigitalDisplay.liveBookingsMinute.Max, widget.DigitalDisplay.liveBookingsMinute.Step)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 最小值/最大值/步长 未 发生变动")
    # 设置 数字滑块【预约分】 显示选项值
    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_minute_digitalSlider') != widget.DigitalDisplay.liveBookingsMinute.Value:
        log_save(0, f"　│││✏️ 数字滑块【预约分】 显示选项值 发生变动: {obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_minute_digitalSlider')}➡️{widget.DigitalDisplay.liveBookingsMinute.Value}")
        obs.obs_data_set_int(GlobalVariableOfData.script_settings, 'live_bookings_minute_digitalSlider', widget.DigitalDisplay.liveBookingsMinute.Value)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 显示选项值 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌数字滑块 UI{30*'─'}┘")

    # 复选框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐复选框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 普通文本框【直播间公告】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️复选框【是否发直播预约动态】 UI")
    # 设置 复选框【是否发直播预约动态】 可见状态
    if obs.obs_property_visible(widget.CheckBox.liveBookingsDynamic.Obj) != widget.CheckBox.liveBookingsDynamic.Visible:
        log_save(0, f"　│││✏️ 复选框【是否发直播预约动态】 可见状态 发生变动: {obs.obs_property_visible(widget.CheckBox.liveBookingsDynamic.Obj)}➡️{widget.CheckBox.liveBookingsDynamic.Visible}")
        obs.obs_property_set_visible(widget.CheckBox.liveBookingsDynamic.Obj, widget.CheckBox.liveBookingsDynamic.Visible)
    else:
        log_save(0, f"　│││🧩 复选框【是否发直播预约动态】 可见状态 未 发生变动")
    # 设置 复选框【是否发直播预约动态】 可用状态
    if obs.obs_property_enabled(widget.CheckBox.liveBookingsDynamic.Obj) != widget.CheckBox.liveBookingsDynamic.Enabled:
        log_save(0, f"　│││✏️ 复选框【是否发直播预约动态】 可用状态 发生变动: {obs.obs_property_enabled(widget.CheckBox.liveBookingsDynamic.Obj)}➡️{widget.CheckBox.liveBookingsDynamic.Enabled}")
        obs.obs_property_set_enabled(widget.CheckBox.liveBookingsDynamic.Obj, widget.CheckBox.liveBookingsDynamic.Enabled)
    else:
        log_save(0, f"　│││🧩 复选框【是否发直播预约动态】 可用状态 未 发生变动")
    # 设置 复选框【是否发直播预约动态】 文本
    if obs.obs_data_get_bool(GlobalVariableOfData.script_settings, 'live_bookings_dynamic_bool') != widget.CheckBox.liveBookingsDynamic.Bool:
        log_save(0, f"　│││✏️ 复选框【是否发直播预约动态】 选中状态 发生变动: {obs.obs_data_get_bool(GlobalVariableOfData.script_settings, 'live_bookings_dynamic_bool')}➡️{widget.CheckBox.liveBookingsDynamic.Bool}")
        obs.obs_data_set_bool(GlobalVariableOfData.script_settings, "live_bookings_dynamic_bool", widget.CheckBox.liveBookingsDynamic.Bool)
    else:
        log_save(0, f"　│││🧩 复选框【是否发直播预约动态】 选中状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌复选框 UI{30*'─'}┘")

    # 普通文本框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐普通文本框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 普通文本框【直播间公告】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️普通文本框【直播预约标题】 UI")
    # 设置 普通文本框【直播预约标题】 可见状态
    if obs.obs_property_visible(widget.TextBox.liveBookingsTitle.Obj) != widget.TextBox.liveBookingsTitle.Visible:
        log_save(0, f"　│││✏️ 普通文本框【直播预约标题】 可见状态 发生变动: {obs.obs_property_visible(widget.TextBox.liveBookingsTitle.Obj)}➡️{widget.TextBox.liveBookingsTitle.Visible}")
        obs.obs_property_set_visible(widget.TextBox.liveBookingsTitle.Obj, widget.TextBox.liveBookingsTitle.Visible)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播预约标题】 可见状态 未 发生变动")
    # 设置 普通文本框【直播预约标题】 可用状态
    if obs.obs_property_enabled(widget.TextBox.liveBookingsTitle.Obj) != widget.TextBox.liveBookingsTitle.Enabled:
        log_save(0, f"　│││✏️ 普通文本框【直播预约标题】 可用状态 发生变动: {obs.obs_property_enabled(widget.TextBox.liveBookingsTitle.Obj)}➡️{widget.TextBox.liveBookingsTitle.Enabled}")
        obs.obs_property_set_enabled(widget.TextBox.liveBookingsTitle.Obj, widget.TextBox.liveBookingsTitle.Enabled)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播预约标题】 可用状态 未 发生变动")
    # 设置 普通文本框【直播预约标题】 文本
    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_bookings_title_textBox') != widget.TextBox.liveBookingsTitle.Text:
        log_save(0, f"　│││✏️ 普通文本框【直播预约标题】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_bookings_title_textBox')}➡️{widget.TextBox.liveBookingsTitle.Text}")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, "live_bookings_title_textBox", widget.TextBox.liveBookingsTitle.Text)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播预约标题】 文本 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌普通文本框 UI{30*'─'}┘")

    # 组合框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐组合框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 组合框【直播预约列表】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【直播预约列表】 UI")
    # 设置 组合框【直播预约列表】 可见状态
    if obs.obs_property_visible(widget.ComboBox.liveBookings.Obj) != widget.ComboBox.liveBookings.Visible:
        log_save(0, f"　│││✏️ 组合框【直播预约列表】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.liveBookings.Obj)}➡️{widget.ComboBox.liveBookings.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.liveBookings.Obj, widget.ComboBox.liveBookings.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【直播预约列表】 可见状态 未 发生变动")
    # 设置 组合框【直播预约列表】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.liveBookings.Obj) != widget.ComboBox.liveBookings.Enabled:
        log_save(0, f"　│││✏️ 组合框【直播预约列表】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.liveBookings.Obj)}➡️{widget.ComboBox.liveBookings.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.liveBookings.Obj, widget.ComboBox.liveBookings.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【直播预约列表】 可用状态 未 发生变动")
    # 判断 组合框【直播预约列表】字典数据 和 当前数据是否有变化
    if widget.ComboBox.liveBookings.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.liveBookings.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveBookings.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveBookings.Obj))}:
        log_save(0, f"　│││✏️ 组合框【直播预约列表】 列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.liveBookings.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveBookings.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveBookings.Obj))})}个元素➡️{len(widget.ComboBox.liveBookings.Dictionary)}个元素")
        # 清空 组合框【直播预约列表】
        log_save(0, f"　│││📑 更新 组合框【直播预约列表】数据 第一步：清空 组合框【直播预约列表】")
        obs.obs_property_list_clear(widget.ComboBox.liveBookings.Obj)
        # 添加 组合框【直播预约列表】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑 更新 组合框【直播预约列表】数据 第二步：添加 组合框【直播预约列表】 列表选项  如果有默认值，会被设置在第一位")
        for reserve_sid in widget.ComboBox.liveBookings.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.liveBookings.Obj, widget.ComboBox.liveBookings.Dictionary[reserve_sid], reserve_sid) if reserve_sid != widget.ComboBox.liveBookings.Value else obs.obs_property_list_insert_string(widget.ComboBox.liveBookings.Obj, 0, widget.ComboBox.liveBookings.Text, widget.ComboBox.liveBookings.Value)
        # 设置 组合框【直播预约列表】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【直播预约列表】数据 第三步：更新 组合框【直播预约列表】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'live_bookings_comboBox', obs.obs_property_list_item_string(widget.ComboBox.liveBookings.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【直播预约列表】 列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌组合框 UI{30*'─'}┘")
    return True

def button_function_cancel_live_appointment(props, prop):
    """取消直播预约"""
    # 获取当前直播预约的sid
    live_bookings_sid = obs.obs_data_get_string(GlobalVariableOfData.script_settings, "live_bookings_comboBox")
    log_save(0, f"当前直播预约的sid: {live_bookings_sid}")
    if live_bookings_sid in ["-1"]:
        log_save(3, f"无直播预约")
        return False
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    cancel_reserve_return = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).cancel_reserve(live_bookings_sid)
    log_save(0, f"取消直播预约返回: {cancel_reserve_return}")
    if cancel_reserve_return['code'] == 0:
        log_save(0, f"取消直播预约成功")
    else:
        log_save(3, f"取消直播预约失败: {cancel_reserve_return['message']}")
        return False

    # 调整控件数据
    log_save(0, f"")
    log_save(0, f"╔{25 * '═'}调整控件数据{25 * '═'}╗")
    log_save(0, f"║{25 * ' '}调整控件数据{25 * ' '}║")
    # 设置控件前准备（获取数据） 开始
    log_save(0, f"║")
    log_save(1, f"║设置控件前准备（获取数据）")
    log_save(0, f"║╔{6*'═'}设置控件前准备（获取数据）{6*'═'}╗")
    log_save(0, f"║║")
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(config_path=GlobalVariableOfData.scriptsUsersConfigFilepath)
    # 获取 '登录用户' 对应的直播间基础信息
    room_info_old = BilibiliApiGeneric(ssl_verification=GlobalVariableOfData.sslVerification).get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else None
    """直播间基础信息"""
    log_save(0, f"║║登录账户 的 直播间基础信息：{room_info_old if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 获取 '登录用户' 的 直播间状态
    room_status = room_info_old["roomStatus"] if b_u_l_c.get_cookies() else None
    """登录用户的直播间存在状态"""
    log_save(0, f"║║登录账户 的 直播间状态：{('有直播间' if room_status else '无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 登录用户的直播预约列表信息
    reserve_list = BilibiliApiMaster(ssl_verification=GlobalVariableOfData.sslVerification, cookie=dict2cookie(b_u_l_c.get_cookies())).get_reserve_list()
    """获取 '登录用户' 的 直播预约列表信息"""
    log_save(0, f"║║登录账户 的 直播预约列表信息：{(reserve_list if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 登录用户的直播预约字典
    reserve_name4reserve_sid = (({str(reserve['reserve_info']['sid']): f"{reserve['reserve_info']['name']}|{datetime.fromtimestamp(reserve['reserve_info']['live_plan_start_time'])}" for reserve in reserve_list} if reserve_list else {"-1": "无直播预约"}) if room_status else {"-1": '⚠️无直播间'}) if b_u_l_c.get_cookies() else {"-1": "⚠️未登录账号"}
    """获取 '登录用户' 的 直播预约字典"""
    log_save(0, f"║║登录账户 的 直播预约：{(list(reserve_name4reserve_sid.values()) if room_status else f'⚠️无直播间') if b_u_l_c.get_cookies() else f'⚠️未登录账号'}")
    # 设置控件前准备（获取数据）结束
    log_save(0, f"║╚{6*'═'}设置控件前准备（获取数据）{6*'═'}╝")
    log_save(0, f"║")
    # 设置控件属性
    log_save(0, f"║")
    log_save(0, f"║╔{15*'═'}设置 控件属性{15*'═'}╗")
    # 分组框【直播】
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    log_save(0, f"║║")
    log_save(0, f"║║设置 分组框【直播】 中 控件属性")
    log_save(0, f"║║╔{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╗")
    # 设置 数字滑块【预约天】 可见状态
    widget.DigitalDisplay.liveBookingsDay.Visible = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约天】 可见状态：{str(widget.DigitalDisplay.liveBookingsDay.Visible)}")
    # 设置 数字滑块【预约天】 可用状态
    widget.DigitalDisplay.liveBookingsDay.Enabled = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约天】 可用状态：{str(widget.DigitalDisplay.liveBookingsDay.Enabled)}")
    # 设置 数字滑块【预约天】 显示选项值
    widget.DigitalDisplay.liveBookingsDay.Value = 0
    log_save(0, f"║║║设置 数字滑块【预约天】 显示选项值：{str(widget.DigitalDisplay.liveBookingsDay.Value)}")
    # 设置 数字滑块【预约天】 最小值
    widget.DigitalDisplay.liveBookingsDay.Min = 0
    log_save(0, f"║║║设置 数字滑块【预约天】 最小值：{str(widget.DigitalDisplay.liveBookingsDay.Min)}")
    # 设置 数字滑块【预约天】 最大值
    widget.DigitalDisplay.liveBookingsDay.Max = 180
    log_save(0, f"║║║设置 数字滑块【预约天】 最大值：{str(widget.DigitalDisplay.liveBookingsDay.Max)}")
    # 设置 数字滑块【预约天】 步长
    widget.DigitalDisplay.liveBookingsDay.Step = 1
    log_save(0, f"║║║设置 数字滑块【预约天】 步长：{str(widget.DigitalDisplay.liveBookingsDay.Step)}")

    # 设置 数字滑块【预约时】 可见状态
    widget.DigitalDisplay.liveBookingsHour.Visible = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约时】 可见状态：{str(widget.DigitalDisplay.liveBookingsHour.Visible)}")
    # 设置 数字滑块【预约时】 可用状态
    widget.DigitalDisplay.liveBookingsHour.Enabled = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约时】 可用状态：{str(widget.DigitalDisplay.liveBookingsHour.Enabled)}")
    # 设置 数字滑块【预约时】 显示选项值
    widget.DigitalDisplay.liveBookingsHour.Value = 0
    log_save(0, f"║║║设置 数字滑块【预约时】 显示选项值：{str(widget.DigitalDisplay.liveBookingsHour.Value)}")
    # 设置 数字滑块【预约时】 最小值
    widget.DigitalDisplay.liveBookingsHour.Min = 0
    log_save(0, f"║║║设置 数字滑块【预约时】 最小值：{str(widget.DigitalDisplay.liveBookingsHour.Min)}")
    # 设置 数字滑块【预约时】 最大值
    widget.DigitalDisplay.liveBookingsHour.Max = 23
    log_save(0, f"║║║设置 数字滑块【预约时】 最大值：{str(widget.DigitalDisplay.liveBookingsHour.Max)}")
    # 设置 数字滑块【预约时】 步长
    widget.DigitalDisplay.liveBookingsHour.Step = 1
    log_save(0, f"║║║设置 数字滑块【预约时】 步长：{str(widget.DigitalDisplay.liveBookingsHour.Step)}")

    # 设置 数字滑块【预约分】 可见状态
    widget.DigitalDisplay.liveBookingsMinute.Visible = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约分】 可见状态：{str(widget.DigitalDisplay.liveBookingsMinute.Visible)}")
    # 设置 数字滑块【预约分】 可用状态
    widget.DigitalDisplay.liveBookingsMinute.Enabled = bool(room_status)
    log_save(0, f"║║║设置 数字滑块【预约分】 可用状态：{str(widget.DigitalDisplay.liveBookingsMinute.Enabled)}")
    # 设置 数字滑块【预约分】 显示选项值
    widget.DigitalDisplay.liveBookingsMinute.Value = 5
    log_save(0, f"║║║设置 数字滑块【预约分】 显示选项值：{str(widget.DigitalDisplay.liveBookingsMinute.Value)}")
    # 设置 数字滑块【预约分】 最小值
    widget.DigitalDisplay.liveBookingsMinute.Min = 5
    log_save(0, f"║║║设置 数字滑块【预约分】 最小值：{str(widget.DigitalDisplay.liveBookingsMinute.Min)}")
    # 设置 数字滑块【预约分】 最大值
    widget.DigitalDisplay.liveBookingsMinute.Max = 59
    log_save(0, f"║║║设置 数字滑块【预约分】 最大值：{str(widget.DigitalDisplay.liveBookingsMinute.Max)}")
    # 设置 数字滑块【预约分】 步长
    widget.DigitalDisplay.liveBookingsMinute.Step = 1
    log_save(0, f"║║║设置 数字滑块【预约分】 步长：{str(widget.DigitalDisplay.liveBookingsMinute.Step)}")

    # 设置 复选框【是否发直播预约动态】 可见状态
    widget.CheckBox.liveBookingsDynamic.Visible =bool(room_status)
    log_save(0, f"║║║设置 复选框【是否发直播预约动态】 可见状态：{str(widget.CheckBox.liveBookingsDynamic.Visible)}")
    # 设置 普通文本框【是否发直播预约动态】 可用状态
    widget.CheckBox.liveBookingsDynamic.Enabled = bool(room_status)
    log_save(0, f"║║║设置 复选框【是否发直播预约动态】 可用状态：{str(widget.CheckBox.liveBookingsDynamic.Enabled)}")
    # 设置 普通文本框【是否发直播预约动态】 内容
    widget.CheckBox.liveBookingsDynamic.Bool = False
    log_save(0, f"║║║设置 复选框【是否发直播预约动态】 选中状态：{str(widget.CheckBox.liveBookingsDynamic.Bool)}")

    # 设置 普通文本框【直播预约标题】 可见状态
    widget.TextBox.liveBookingsTitle.Visible = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播预约标题】 可见状态：{str(widget.TextBox.liveBookingsTitle.Visible)}")
    # 设置 普通文本框【直播预约标题】 可用状态
    widget.TextBox.liveBookingsTitle.Enabled = bool(room_status)
    log_save(0, f"║║║设置 普通文本框【直播预约标题】 可用状态：{str(widget.TextBox.liveBookingsTitle.Enabled)}")
    # 设置 普通文本框【直播预约标题】 内容
    widget.TextBox.liveBookingsTitle.Text = ""
    log_save(0, f"║║║设置 普通文本框【直播预约标题】 内容：{str(widget.TextBox.liveBookingsTitle.Text)}")

    # 设置 组合框【直播预约列表】 可见状态
    widget.ComboBox.liveBookings.Visible = True
    log_save(0, f"║║║设置 组合框【直播预约列表】 可见状态：{str(widget.ComboBox.liveBookings.Visible)}")
    # 设置 组合框【直播预约列表】 可用状态
    widget.ComboBox.liveBookings.Enabled = True
    log_save(0, f"║║║设置 组合框【直播预约列表】 可用状态：{str(widget.ComboBox.liveBookings.Enabled)}")
    # 设置 组合框【直播预约列表】 的数据字典
    widget.ComboBox.liveBookings.Dictionary = reserve_name4reserve_sid
    log_save(0, f"║║║设置 组合框【直播预约列表】 的数据字典：{str(widget.ComboBox.liveBookings.Dictionary)}")
    # 设置 组合框【直播预约列表】 的内容
    widget.ComboBox.liveBookings.Text = ""
    log_save(0, f"║║║设置 组合框【直播预约列表】 的内容：{str(widget.ComboBox.liveBookings.Text)}")
    # 设置 组合框【直播预约列表】 的内容 的 列表值
    widget.ComboBox.liveBookings.Value = ""
    log_save(0, f"║║║设置 组合框【直播预约列表】 的内容 的 列表值：{str(widget.ComboBox.liveBookings.Value)}")
    # 设置 分组框【直播】 中控件属性 结束
    log_save(0, f"║║╚{7*'═'}设置 分组框【直播】 中控件属性{7*'═'}╝")
    # 设置 控件属性 结束
    log_save(0, f"║╚{15*'═'}设置 控件属性{15*'═'}╝")
    # 调整控件数据 结束
    log_save(0, f"╚{25 * '═'}调整控件数据{25 * '═'}╝")
    log_save(0, f"")

    # 数字滑块+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐数字滑块 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 数字滑块【预约天】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️数字滑块【预约天】 UI")
    # 设置 数字滑块【预约天】 可见状态
    if obs.obs_property_visible(widget.DigitalDisplay.liveBookingsDay.Obj) != widget.DigitalDisplay.liveBookingsDay.Visible:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 可见状态 发生变动: {obs.obs_property_visible(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Visible}")
        obs.obs_property_set_visible(widget.DigitalDisplay.liveBookingsDay.Obj, widget.DigitalDisplay.liveBookingsDay.Visible)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约天】 可见状态 未 发生变动")
    # 设置 数字滑块【预约天】 可用状态
    if obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsDay.Obj) != widget.DigitalDisplay.liveBookingsDay.Enabled:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 可用状态 发生变动: {obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Enabled}")
        obs.obs_property_set_enabled(widget.DigitalDisplay.liveBookingsDay.Obj, widget.DigitalDisplay.liveBookingsDay.Enabled)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约天】 可用状态 未 发生变动")
    if widget.DigitalDisplay.liveBookingsDay.Min != obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj) or widget.DigitalDisplay.liveBookingsDay.Max != obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj) or widget.DigitalDisplay.liveBookingsDay.Step != obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsDay.Obj):
        log_save(0, f"　│││✏️ 数字滑块【预约天】 最小值/最大值/步长 发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Min}/{widget.DigitalDisplay.liveBookingsDay.Max}/{widget.DigitalDisplay.liveBookingsDay.Step}")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsDay.Obj, widget.DigitalDisplay.liveBookingsDay.Min, widget.DigitalDisplay.liveBookingsDay.Max, widget.DigitalDisplay.liveBookingsDay.Step)
    else:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 最小值/最大值/步长 未发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsDay.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsDay.Obj)}➡️{widget.DigitalDisplay.liveBookingsDay.Min}/{widget.DigitalDisplay.liveBookingsDay.Max}/{widget.DigitalDisplay.liveBookingsDay.Step}")
        log_save(0, f"　│││🧩 数字滑块【预约天】 最小值/最大值/步长 未 发生变动")
    # 设置 数字滑块【预约天】 显示选项值
    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_day_digitalSlider') != widget.DigitalDisplay.liveBookingsDay.Value:
        log_save(0, f"　│││✏️ 数字滑块【预约天】 显示选项值 发生变动: {obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_day_digitalSlider')}➡️{widget.DigitalDisplay.liveBookingsDay.Value}")
        obs.obs_data_set_int(GlobalVariableOfData.script_settings, 'live_bookings_day_digitalSlider', widget.DigitalDisplay.liveBookingsDay.Value)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约天】 显示选项值 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 数字滑块【预约时】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️数字滑块【预约时】 UI")
    # 设置 数字滑块【预约时】 可见状态
    if obs.obs_property_visible(widget.DigitalDisplay.liveBookingsHour.Obj) != widget.DigitalDisplay.liveBookingsHour.Visible:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 可见状态 发生变动: {obs.obs_property_visible(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Visible}")
        obs.obs_property_set_visible(widget.DigitalDisplay.liveBookingsHour.Obj, widget.DigitalDisplay.liveBookingsHour.Visible)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约时】 可见状态 未 发生变动")
    # 设置 数字滑块【预约时】 可用状态
    if obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsHour.Obj) != widget.DigitalDisplay.liveBookingsHour.Enabled:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 可用状态 发生变动: {obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Enabled}")
        obs.obs_property_set_enabled(widget.DigitalDisplay.liveBookingsHour.Obj, widget.DigitalDisplay.liveBookingsHour.Enabled)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约时】 可用状态 未 发生变动")
    if widget.DigitalDisplay.liveBookingsHour.Min != obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj) or widget.DigitalDisplay.liveBookingsHour.Max != obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj) or widget.DigitalDisplay.liveBookingsHour.Step != obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsHour.Obj):
        log_save(0, f"　│││✏️ 数字滑块【预约时】 最小值/最大值/步长 发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Min}/{widget.DigitalDisplay.liveBookingsHour.Max}/{widget.DigitalDisplay.liveBookingsHour.Step}")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsHour.Obj, widget.DigitalDisplay.liveBookingsHour.Min, widget.DigitalDisplay.liveBookingsHour.Max, widget.DigitalDisplay.liveBookingsHour.Step)
    else:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 最小值/最大值/步长 未发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsHour.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsHour.Obj)}➡️{widget.DigitalDisplay.liveBookingsHour.Min}/{widget.DigitalDisplay.liveBookingsHour.Max}/{widget.DigitalDisplay.liveBookingsHour.Step}")
        log_save(0, f"　│││🧩 数字滑块【预约时】 最小值/最大值/步长 未 发生变动")
    # 设置 数字滑块【预约时】 显示选项值
    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_hour_digitalSlider') != widget.DigitalDisplay.liveBookingsHour.Value:
        log_save(0, f"　│││✏️ 数字滑块【预约时】 显示选项值 发生变动: {obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_hour_digitalSlider')}➡️{widget.DigitalDisplay.liveBookingsHour.Value}")
        obs.obs_data_set_int(GlobalVariableOfData.script_settings, 'live_bookings_hour_digitalSlider', widget.DigitalDisplay.liveBookingsHour.Value)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约时】 显示选项值 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    # 数字滑块【预约分】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️数字滑块【预约分】 UI")
    # 设置 数字滑块【预约分】 可见状态
    if obs.obs_property_visible(widget.DigitalDisplay.liveBookingsMinute.Obj) != widget.DigitalDisplay.liveBookingsMinute.Visible:
        log_save(0, f"　│││✏️ 数字滑块【预约分】 可见状态 发生变动: {obs.obs_property_visible(widget.DigitalDisplay.liveBookingsMinute.Obj)}➡️{widget.DigitalDisplay.liveBookingsMinute.Visible}")
        obs.obs_property_set_visible(widget.DigitalDisplay.liveBookingsMinute.Obj, widget.DigitalDisplay.liveBookingsMinute.Visible)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 可见状态 未 发生变动")
    # 设置 数字滑块【预约分】 可用状态
    if obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsMinute.Obj) != widget.DigitalDisplay.liveBookingsMinute.Enabled:
        log_save(0, f"　│││✏️ 数字滑块【预约分】 可用状态 发生变动: {obs.obs_property_enabled(widget.DigitalDisplay.liveBookingsMinute.Obj)}➡️{widget.DigitalDisplay.liveBookingsMinute.Enabled}")
        obs.obs_property_set_enabled(widget.DigitalDisplay.liveBookingsMinute.Obj, widget.DigitalDisplay.liveBookingsMinute.Enabled)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 可用状态 未 发生变动")
    if widget.DigitalDisplay.liveBookingsMinute.Min != obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsMinute.Obj) or widget.DigitalDisplay.liveBookingsMinute.Max != obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsMinute.Obj) or widget.DigitalDisplay.liveBookingsMinute.Step != obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsMinute.Obj):
        log_save(0, f"　│││✏️ 数字滑块【预约分】 最小值/最大值/步长 发生变动: {obs.obs_property_int_min(widget.DigitalDisplay.liveBookingsMinute.Obj)}/{obs.obs_property_int_max(widget.DigitalDisplay.liveBookingsMinute.Obj)}/{obs.obs_property_int_step(widget.DigitalDisplay.liveBookingsMinute.Obj)}➡️{widget.DigitalDisplay.liveBookingsMinute.Min}/{widget.DigitalDisplay.liveBookingsMinute.Max}/{widget.DigitalDisplay.liveBookingsMinute.Step}")
        obs.obs_property_int_set_limits(widget.DigitalDisplay.liveBookingsMinute.Obj, widget.DigitalDisplay.liveBookingsMinute.Min, widget.DigitalDisplay.liveBookingsMinute.Max, widget.DigitalDisplay.liveBookingsMinute.Step)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 最小值/最大值/步长 未 发生变动")
    # 设置 数字滑块【预约分】 显示选项值
    if obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_minute_digitalSlider') != widget.DigitalDisplay.liveBookingsMinute.Value:
        log_save(0, f"　│││✏️ 数字滑块【预约分】 显示选项值 发生变动: {obs.obs_data_get_int(GlobalVariableOfData.script_settings, 'live_bookings_minute_digitalSlider')}➡️{widget.DigitalDisplay.liveBookingsMinute.Value}")
        obs.obs_data_set_int(GlobalVariableOfData.script_settings, 'live_bookings_minute_digitalSlider', widget.DigitalDisplay.liveBookingsMinute.Value)
    else:
        log_save(0, f"　│││🧩 数字滑块【预约分】 显示选项值 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌数字滑块 UI{30*'─'}┘")

    # 复选框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐复选框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 普通文本框【直播间公告】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️复选框【是否发直播预约动态】 UI")
    # 设置 复选框【是否发直播预约动态】 可见状态
    if obs.obs_property_visible(widget.CheckBox.liveBookingsDynamic.Obj) != widget.CheckBox.liveBookingsDynamic.Visible:
        log_save(0, f"　│││✏️ 复选框【是否发直播预约动态】 可见状态 发生变动: {obs.obs_property_visible(widget.CheckBox.liveBookingsDynamic.Obj)}➡️{widget.CheckBox.liveBookingsDynamic.Visible}")
        obs.obs_property_set_visible(widget.CheckBox.liveBookingsDynamic.Obj, widget.CheckBox.liveBookingsDynamic.Visible)
    else:
        log_save(0, f"　│││🧩 复选框【是否发直播预约动态】 可见状态 未 发生变动")
    # 设置 复选框【是否发直播预约动态】 可用状态
    if obs.obs_property_enabled(widget.CheckBox.liveBookingsDynamic.Obj) != widget.CheckBox.liveBookingsDynamic.Enabled:
        log_save(0, f"　│││✏️ 复选框【是否发直播预约动态】 可用状态 发生变动: {obs.obs_property_enabled(widget.CheckBox.liveBookingsDynamic.Obj)}➡️{widget.CheckBox.liveBookingsDynamic.Enabled}")
        obs.obs_property_set_enabled(widget.CheckBox.liveBookingsDynamic.Obj, widget.CheckBox.liveBookingsDynamic.Enabled)
    else:
        log_save(0, f"　│││🧩 复选框【是否发直播预约动态】 可用状态 未 发生变动")
    # 设置 复选框【是否发直播预约动态】 文本
    if obs.obs_data_get_bool(GlobalVariableOfData.script_settings, 'live_bookings_dynamic_bool') != widget.CheckBox.liveBookingsDynamic.Bool:
        log_save(0, f"　│││✏️ 复选框【是否发直播预约动态】 选中状态 发生变动: {obs.obs_data_get_bool(GlobalVariableOfData.script_settings, 'live_bookings_dynamic_bool')}➡️{widget.CheckBox.liveBookingsDynamic.Bool}")
        obs.obs_data_set_bool(GlobalVariableOfData.script_settings, "live_bookings_dynamic_bool", widget.CheckBox.liveBookingsDynamic.Bool)
    else:
        log_save(0, f"　│││🧩 复选框【是否发直播预约动态】 选中状态 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌复选框 UI{30*'─'}┘")

    # 普通文本框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐普通文本框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 普通文本框【直播间公告】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️普通文本框【直播预约标题】 UI")
    # 设置 普通文本框【直播预约标题】 可见状态
    if obs.obs_property_visible(widget.TextBox.liveBookingsTitle.Obj) != widget.TextBox.liveBookingsTitle.Visible:
        log_save(0, f"　│││✏️ 普通文本框【直播预约标题】 可见状态 发生变动: {obs.obs_property_visible(widget.TextBox.liveBookingsTitle.Obj)}➡️{widget.TextBox.liveBookingsTitle.Visible}")
        obs.obs_property_set_visible(widget.TextBox.liveBookingsTitle.Obj, widget.TextBox.liveBookingsTitle.Visible)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播预约标题】 可见状态 未 发生变动")
    # 设置 普通文本框【直播预约标题】 可用状态
    if obs.obs_property_enabled(widget.TextBox.liveBookingsTitle.Obj) != widget.TextBox.liveBookingsTitle.Enabled:
        log_save(0, f"　│││✏️ 普通文本框【直播预约标题】 可用状态 发生变动: {obs.obs_property_enabled(widget.TextBox.liveBookingsTitle.Obj)}➡️{widget.TextBox.liveBookingsTitle.Enabled}")
        obs.obs_property_set_enabled(widget.TextBox.liveBookingsTitle.Obj, widget.TextBox.liveBookingsTitle.Enabled)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播预约标题】 可用状态 未 发生变动")
    # 设置 普通文本框【直播预约标题】 文本
    if obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_bookings_title_textBox') != widget.TextBox.liveBookingsTitle.Text:
        log_save(0, f"　│││✏️ 普通文本框【直播预约标题】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfData.script_settings, 'live_bookings_title_textBox')}➡️{widget.TextBox.liveBookingsTitle.Text}")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, "live_bookings_title_textBox", widget.TextBox.liveBookingsTitle.Text)
    else:
        log_save(0, f"　│││🧩 普通文本框【直播预约标题】 文本 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌普通文本框 UI{30*'─'}┘")

    # 组合框+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    log_save(0, f"　┌{30*'─'}⭐组合框 UI{30*'─'}┐")
    # 【直播】分组—————————————————————————————————————————————————————————————————————————————————————————————————————————
    log_save(0, f"　│┌{'─'*60}┐")
    log_save(0, f"　││▶️分组框【直播】")
    # 组合框【直播预约列表】 UI
    log_save(0, f"　││┌{'─'*55}")
    log_save(0, f"　│││⚛️组合框【直播预约列表】 UI")
    # 设置 组合框【直播预约列表】 可见状态
    if obs.obs_property_visible(widget.ComboBox.liveBookings.Obj) != widget.ComboBox.liveBookings.Visible:
        log_save(0, f"　│││✏️ 组合框【直播预约列表】 可见状态 发生变动: {obs.obs_property_visible(widget.ComboBox.liveBookings.Obj)}➡️{widget.ComboBox.liveBookings.Visible}")
        obs.obs_property_set_visible(widget.ComboBox.liveBookings.Obj, widget.ComboBox.liveBookings.Visible)
    else:
        log_save(0, f"　│││🧩 组合框【直播预约列表】 可见状态 未 发生变动")
    # 设置 组合框【直播预约列表】 可用状态
    if obs.obs_property_enabled(widget.ComboBox.liveBookings.Obj) != widget.ComboBox.liveBookings.Enabled:
        log_save(0, f"　│││✏️ 组合框【直播预约列表】 可用状态 发生变动: {obs.obs_property_enabled(widget.ComboBox.liveBookings.Obj)}➡️{widget.ComboBox.liveBookings.Enabled}")
        obs.obs_property_set_enabled(widget.ComboBox.liveBookings.Obj, widget.ComboBox.liveBookings.Enabled)
    else:
        log_save(0, f"　│││🧩 组合框【直播预约列表】 可用状态 未 发生变动")
    # 判断 组合框【直播预约列表】字典数据 和 当前数据是否有变化
    if widget.ComboBox.liveBookings.Dictionary != {obs.obs_property_list_item_string(widget.ComboBox.liveBookings.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveBookings.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveBookings.Obj))}:
        log_save(0, f"　│││✏️ 组合框【直播预约列表】 列表数据 发生变动：{len({obs.obs_property_list_item_string(widget.ComboBox.liveBookings.Obj, idx): obs.obs_property_list_item_name(widget.ComboBox.liveBookings.Obj, idx) for idx in range(obs.obs_property_list_item_count(widget.ComboBox.liveBookings.Obj))})}个元素➡️{len(widget.ComboBox.liveBookings.Dictionary)}个元素")
        # 清空 组合框【直播预约列表】
        log_save(0, f"　│││📑 更新 组合框【直播预约列表】数据 第一步：清空 组合框【直播预约列表】")
        obs.obs_property_list_clear(widget.ComboBox.liveBookings.Obj)
        # 添加 组合框【直播预约列表】 列表选项  默认值会被设置在第一位
        log_save(0, f"　│││📑 更新 组合框【直播预约列表】数据 第二步：添加 组合框【直播预约列表】 列表选项  如果有默认值，会被设置在第一位")
        for reserve_sid in widget.ComboBox.liveBookings.Dictionary:
            obs.obs_property_list_add_string(widget.ComboBox.liveBookings.Obj, widget.ComboBox.liveBookings.Dictionary[reserve_sid], reserve_sid) if reserve_sid != widget.ComboBox.liveBookings.Value else obs.obs_property_list_insert_string(widget.ComboBox.liveBookings.Obj, 0, widget.ComboBox.liveBookings.Text, widget.ComboBox.liveBookings.Value)
        # 设置 组合框【直播预约列表】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        log_save(0, f"　│││📑 更新 组合框【直播预约列表】数据 第三步：更新 组合框【直播预约列表】 文本")
        obs.obs_data_set_string(GlobalVariableOfData.script_settings, 'live_bookings_comboBox', obs.obs_property_list_item_string(widget.ComboBox.liveBookings.Obj, 0))
    else:
        log_save(0, f"　│││🧩 组合框【直播预约列表】 列表数据 未 发生变动")
    log_save(0, f"　││└{'─'*55}")
    log_save(0, f"　│└{'─'*60}┘")
    log_save(0, f"　└{30*'─'}👌组合框 UI{30*'─'}┘")
    return True

def button_function_test(p_name):
    if p_name:
        log_save(0, f"【{p_name}】按钮被触发")
    return True


def script_unload():
    """
    在脚本被卸载时调用。
    """
    # """注销事件回调"""
    log_save(0, "┌——停止监视obs事件——┐")
    log_save(0, "│  停止监视obs事件  │")
    log_save(0, "└——停止监视obs事件——┘")
    obs.obs_frontend_remove_event_callback(trigger_frontend_event)
    log_save(0, "╔══已卸载: bilibili-live══╗")
    log_save(0, "║  已卸载: bilibili-live  ║")
    log_save(0, "╚══已卸载: bilibili-live══╝")
    log_save(0, "==保存日志文件==")
    log_save(0, f"{'═' * 120}\n")
    with open(Path(GlobalVariableOfData.scriptsLogDir) / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", "w", encoding="utf-8") as f:
        f.write(str(GlobalVariableOfData.logRecording))
