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
import io
import json
import os
# import os
import pathlib
import random
import string
# import pprint
import sys
# import tempfile
# import threading
import time
import urllib
from datetime import datetime
from typing import Optional, Dict, Literal, Union, List, Any
# import zlib
from urllib.parse import quote, unquote, parse_qs, urlparse
from pathlib import Path
import socket
import urllib.request
from urllib.error import URLError

import obspython as obs
# import pypinyin
import qrcode
import requests
import pyperclip as cb
from PIL import Image


# import websockets

# 全局变量
textBox_type_name4textBox_type = {
    obs.OBS_TEXT_INFO_NORMAL: '正常信息',
    obs.OBS_TEXT_INFO_WARNING: '警告信息',
    obs.OBS_TEXT_INFO_ERROR: '错误信息'
}
"""
只读文本框的消息类型字典

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
登陆二维码被调用后轮询函数返回值对应的含义

- 0: "登录成功",
- 86101: "未扫码",
- 86090: "二维码已扫码未确认",
- 86038: "二维码已失效",
"""

information4frontend_event = {
    obs.OBS_FRONTEND_EVENT_STREAMING_STARTING: "推流正在启动",
    obs.OBS_FRONTEND_EVENT_STREAMING_STARTED: "推流已开始",
    obs.OBS_FRONTEND_EVENT_STREAMING_STOPPING: "推流正在停止",
    obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED: "推流已停止",
    obs.OBS_FRONTEND_EVENT_RECORDING_STARTED: "录制已开始",
    obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED: "录制已停止",
    obs.OBS_FRONTEND_EVENT_SCENE_CHANGED: "当前场景改变",
    obs.OBS_FRONTEND_EVENT_TRANSITION_CHANGED: "转场效果改变",
    obs.OBS_FRONTEND_EVENT_PROFILE_CHANGED: "配置文件切换",
    obs.OBS_FRONTEND_EVENT_PROFILE_LIST_CHANGED: "配置文件列表改变",
    obs.OBS_FRONTEND_EVENT_SCENE_LIST_CHANGED: "场景列表改变",
    obs.OBS_FRONTEND_EVENT_EXIT: "OBS 即将退出",
    obs.OBS_FRONTEND_EVENT_FINISHED_LOADING: "OBS 完成加载",
}


class GlobalVariableOfTheControl:
    isScript_propertiesNum = 0
    """
    `Script_properties`被调用的次数
    """

    streaming_active = None
    """
    推流状态
    """

    # #记录obs脚本中控件的数据
    script_settings = None

    # #控件对象的属性集
    props = None

    # ##【账号】分组框中的控件对象 属性集
    setting_props = None

    # ##【直播间】分组框中的控件对象 属性集
    liveRoom_props = None

    # ##【直播】分组框中的控件对象 属性集
    live_props = None

    # #【账号】分组框中的控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##分组框【账号】的实例
    setting_group = None
    setting_group_visible = False  # ###分组框【账号】的实例的【可见】
    setting_group_enabled = False  # ###分组框【账号】的实例的【可用】

    # ##只读文本框【登录状态】的实例
    login_status_textBox = None
    login_status_textBox_visible = False  # ###只读文本框【登录状态】的实例的【可见】
    login_status_textBox_enabled = False  # ###只读文本框【登录状态】的实例的【可用】
    login_status_textBox_type = None  # ###只读文本框【登录状态】的实例的【类型】
    login_status_textBox_string = ""  # ###只读文本框【登录状态】的实例的【显示】
    """
    obs.OBS_TEXT_INFO_NORMAL
    obs.OBS_TEXT_INFO_WARNING
    """

    # ##组合框【用户】的实例
    uid_comboBox = None
    uid_comboBox_visible = False
    uid_comboBox_enabled = False
    uid_comboBox_string = ""
    """
    组合框【用户】的第0行显示的字符串
    """
    uid_comboBox_value = ""
    """
    组合框【用户】的第0行显示的字符串在组合框中对应值
    """
    uid_comboBox_dict = {}
    """
    组合框【用户】的实例的【字典】
    """

    # ##按钮【登录账号】的实例
    login_button = None
    login_button_visible = False  # ###按钮【登录账号】的实例的【可见】
    login_button_enabled = False  # ###按钮【登录账号】的实例的【可用】

    # ##按钮【更新账号列表】的实例
    update_account_list_button = None
    update_account_list_button_visible = False  # ###按钮【更新账号列表】的实例的【可见】
    update_account_list_button_enabled = False  # ###按钮【更新账号列表】的实例的【可用】

    # ##按钮【二维码添加账户】的实例
    qr_add_account_button = None
    qr_add_account_button_visible = False
    qr_add_account_button_enabled = False

    # ##按钮【显示登录二维码图片】的实例
    display_qr_picture_button = None
    display_qr_picture_button_visible = False
    display_qr_picture_button_enabled = False

    # ##按钮【删除账户】的实例
    delete_account_button = None
    delete_account_button_visible = False
    delete_account_button_enabled = False

    # ##按钮【备份账户】的实例
    backup_account_button = None
    backup_account_button_visible = False
    backup_account_button_enabled = False

    # ##按钮【恢复账户】的实例
    restore_account_button = None
    restore_account_button_visible = False
    restore_account_button_enabled = False

    # ##按钮【退出登录】的实例
    logout_button = None
    logout_button_visible = False
    logout_button_enabled = False

    # #【直播间】分组框中的控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##分组框【直播间】的实例
    liveRoom_group = None
    liveRoom_group_visible = False  # ###分组框【直播间】的实例的【可见】
    liveRoom_group__enabled = False  # ###分组框【直播间】的实例的【可用】

    # ##只读文本框【直播间 状态】的实例
    room_status_textBox = None
    room_status_textBox_visible = False
    room_status_textBox_enabled = False
    room_status_textBox_type = None
    room_status_textBox_string = ""

    # ##按钮【查看当前直播间封面】的实例
    viewLiveCover_button = None
    viewLiveCover_button_visible = False
    viewLiveCover_button_enabled = False

    # ##文件对话框【直播间封面】的实例
    room_cover_fileDialogBox = None
    room_cover_fileDialogBox_visible = False
    room_cover_fileDialogBox_enabled = False
    room_cover_fileDialogBox_string = ""

    # ##按钮【上传直播间封面】的实例
    room_cover_update_button = None
    room_cover_update_button_visible = False
    room_cover_update_button_enabled = False

    # ##普通文本框【直播间标题】的实例
    liveRoom_title_textBox = None
    liveRoom_title_textBox_visible = False
    liveRoom_title_textBox_enabled = False
    liveRoom_title_textBox_string = ""

    # ##按钮【更改直播间标题】的实例
    change_liveRoom_title_button = None
    change_liveRoom_title_button_visible = False
    change_liveRoom_title_button_enabled = False

    # ##普通文本框【直播间公告】的实例
    liveRoom_news_textBox = None
    liveRoom_news_textBox_visible = False
    liveRoom_news_textBox_enabled = False
    liveRoom_news_textBox_string = ""

    # ##按钮【更改直播间公告】的实例
    change_liveRoom_news_button = None
    change_liveRoom_news_button_visible = False  # ###按钮【更改直播间公告】的实例的【可见】
    change_liveRoom_news_button_enabled = False  # ###按钮【更改直播间公告】的实例的【可用】

    # ##组合框【一级分区】的实例
    parentLiveArea_comboBox = None
    parentLiveArea_comboBox_visible = False
    parentLiveArea_comboBox_enabled = False
    parentLiveArea_comboBox_string = ""
    parentLiveArea_comboBox_value = ""
    parentLiveArea_comboBox_dict = {}

    # ##按钮【确认一级分区】的实例
    parentLiveArea_true_button = None
    parentLiveArea_true_button_visible = False
    parentLiveArea_true_button_enabled = False

    # ##组合框【二级分区】的实例
    subLiveArea_comboBox = None
    subLiveArea_comboBox_visible = False
    subLiveArea_comboBox_enabled = False
    subLiveArea_comboBox_string = ""
    subLiveArea_comboBox_value = ""
    subLiveArea_comboBox_dict = {}

    # ##按钮【「确认分区」】的实例
    subLiveArea_true_button = None
    subLiveArea_true_button_visible = False
    subLiveArea_true_button_enabled = False

    # ##普通文本框【直播间标签】的实例
    liveRoom_Tags_textBox = None
    liveRoom_Tags_textBox_visible = False
    liveRoom_Tags_textBox_enabled = False
    liveRoom_Tags_textBox_string = ""

    # ##按钮【更改直播间标签】的实例
    change_liveRoom_Tags_button = None
    change_liveRoom_Tags_button_visible = False
    change_liveRoom_Tags_button_enabled = False

    # ##url按钮【跳转直播间后台网页】
    jump_blive_web_button = None
    jump_blive_web_button_visible = False
    jump_blive_web_button_enabled = False
    jump_blive_web_button_url = ""

    # #【直播】分组框中的控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##分组框【直播】的实例
    live_group = None
    live_group_visible = False  # ###分组框【直播】的实例的【可见】
    live_group__enabled = False  # ###分组框【直播】的实例的【可用】

    # ##组合框【直播平台】的实例
    live_streaming_platform_comboBox = None
    live_streaming_platform_comboBox_visible = False
    live_streaming_platform_comboBox_enabled = False
    live_streaming_platform_comboBox_string = ""
    live_streaming_platform_comboBox_value = ""
    live_streaming_platform_comboBox_dict = {}
    """
    {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}
    """

    # ##按钮【开始直播并复制推流码】的实例
    start_live_button = None
    start_live_button_visible = False  # ###按钮【开始直播并复制推流码】的实例的【可见】
    start_live_button_enabled = False  # ###按钮【开始直播并复制推流码】的实例的【可用】

    # ##按钮【复制直播服务器】的实例
    rtmp_address_copy_button = None
    rtmp_address_copy_button_visible = False
    rtmp_address_copy_button_enabled = False

    # ##按钮【复制直播推流码】的实例
    rtmp_stream_code_copy_button = None
    rtmp_stream_code_copy_button_visible = False
    rtmp_stream_code_copy_button_enabled = False

    # ##按钮【更新推流码并复制】的实例
    rtmp_stream_code_update_button = None
    rtmp_stream_code_update_button_visible = False
    rtmp_stream_code_update_button_enabled = False

    # ##按钮【结束直播】的实例
    stop_live_button = None
    stop_live_button_visible = False
    stop_live_button_enabled = False


class GlobalVariableOfData:
    # #是否 操作 用户配置文件 中 每一个 用户 的 可用性
    accountAvailabilityDetectionSwitch = True
    # #日志记录的文本
    logRecording = ""
    # #网络连接状态
    networkConnectionStatus = False
    # 文件配置类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # #脚本所在目录，末尾带/
    scripts_data_dirpath = None

    # #配置文件所在路径
    scripts_config_filepath = None

    # #临时文件文件夹
    scripts_temp_dir = None
    # 用户类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    loginQrCode_key = None

    loginQrCodeReturn = None

    # ##登录二维码的pillow img实例
    LoginQRCodePillowImg = None
    """
    登录二维码的pillow img实例
    """


def script_path():
    """
    用于获取脚本所在文件夹的路径，这其实是一个obs插件内置函数，
    只在obs插件指定的函数内部使用有效,
    这里构建这个函数是没必要的，写在这里只是为了避免IDE出现error提示
    Example:
        假如脚本路径在"/Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/bilibili_live.py"
        >>> print(script_path())
        /Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/
        >>> print(Path(f'{script_path()}bilibili-live') / "config.json")
        /Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/bilibili-live/config.json
    """
    pass


def logSave(logLevel: Literal[0, 1, 2, 3], logStr: str) -> None:
    """
    输出并保存日志
    Args:
        logLevel: 日志等级
        logStr: 日志内容
    Returns: None
    """
    logType = {
        0: obs.LOG_INFO,
        1: obs.LOG_DEBUG,
        2: obs.LOG_WARNING,
        3: obs.LOG_ERROR,
    }
    now = datetime.now()
    formatted = now.strftime("%Y/%m/%d %H:%M:%S")
    log_text = f"【{formatted}】【{logLevel}】{logStr}"
    obs.script_log(logType[logLevel], log_text)
    GlobalVariableOfData.logRecording += log_text + "\n"


def check_network_connection():
    """检查网络连接，通过多个服务提供者的链接验证"""
    logSave(0, "======= 开始网络连接检查 =======")

    # 1. 首先尝试快速DNS连接检查
    logSave(0, "[步骤1] 尝试通过DNS连接检查网络 (8.8.8.8:53)...")
    try:
        start_time = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        elapsed = (time.time() - start_time) * 1000
        logSave(0, f"✅ DNS连接成功! 耗时: {elapsed:.2f}ms")
        return True
    except OSError as e:
        logSave(1, f"⚠️ DNS连接失败: {str(e)}")

    # 2. 尝试多个服务提供者的链接
    logSave(0, "\n[步骤2] 开始尝试多个服务提供者的连接...")

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
        logSave(0, f"\n- 尝试 {provider} 服务: {url}")

        try:
            # 发送HEAD请求减少数据传输量
            start_time = time.time()
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as response:
                elapsed = (time.time() - start_time) * 1000

                # 检查响应状态
                if response.status < 500:  # 排除服务器错误
                    logSave(0, f"  ✅ 连接成功! 状态码: {response.status} | 耗时: {elapsed:.2f}ms")
                    return True
                else:
                    logSave(1, f"  ⚠️ 服务器错误: 状态码 {response.status}")
        except TimeoutError:
            logSave(1, "  ⏱️ 连接超时 (3秒)")
        except ConnectionError:
            logSave(1, "  🔌 连接错误 (网络问题)")
        except URLError as e:
            logSave(1, f"  ❌ URL错误: {str(e.reason)}")
        except Exception as e:
            logSave(1, f"  ⚠️ 未知错误: {str(e)}")

    # 3. 最后尝试基本HTTP连接
    logSave(1, "\n[步骤3] 尝试基本HTTP连接检查 (http://example.com)...")
    try:
        start_time = time.time()
        urllib.request.urlopen("http://example.com", timeout=3)
        elapsed = (time.time() - start_time) * 1000
        logSave(0, f"✅ HTTP连接成功! 耗时: {elapsed:.2f}ms")
        return True
    except URLError as e:
        logSave(3, f"❌ 所有连接尝试失败: {str(e)}")
        return False


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

    def __init__(self, configPath: pathlib.Path):
        """
        初始化配置文件管理器
        Args:
            configPath: 配置文件路径对象
        Raises:
            IOError: 文件读写失败时抛出
            json.JSONDecodeError: 配置文件内容格式错误时抛出
        """
        self.configPath = configPath
        self._ensure_config_file()

    def _ensure_config_file(self):
        """确保配置文件存在且结构有效"""
        if not self.configPath.exists():
            logSave(1, f'脚本数据文件【{GlobalVariableOfData.scripts_data_dirpath}】不存在，尝试创建')
            self.configPath.parent.mkdir(parents=True, exist_ok=True)
            self._write_config({"DefaultUser": None})
            logSave(1, f'success：脚本数据文件 创建成功')

        config = self._read_config()
        if "DefaultUser" not in config:
            logSave(1, f'脚本数据文件中不存在"DefaultUser"字段，尝试创建')
            config["DefaultUser"] = None
            self._write_config(config)
            logSave(1, f'success："DefaultUser"字段 创建成功')

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

    def update_ser(self, cookies: Optional[dict], setDefaultUserIs: bool = True) -> None:
        """
        更新用户配置或清空默认用户
        Args:
            cookies: 包含完整cookie信息的字典，传 None 表示清空默认用户
                - 示例: {"DedeUserID": "123", "SESSDATA": "xxx"...}
                - 传 None 时需配合 set_default_user=True 使用
            setDefaultUserIs: 是否设为默认用户
                - 当 cookies=None 时必须为 True
        Raises:
            ValueError: 以下情况时抛出
                - cookies 不完整或用户不存在
                - cookies=None 但 set_default_user=False
        """
        config = self._read_config()

        # 处理清空默认用户场景
        if cookies is None:
            if not setDefaultUserIs:
                raise ValueError("cookies=None 时必须设置 set_default_user=True")
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
        if setDefaultUserIs:
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


def url2pillow_image(url) -> Image.Image:
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
        response = requests.get(url, headers=headers, stream=True)
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


def utf_8_to_url(string: str, safe: str = "/:") -> str:
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
        return quote(string, safe=safe, encoding='utf-8')
    except Exception:
        # 编码失败时返回原始字符串
        return string


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


def qr_text8pil_img(qr_str: str, border: int = 2, invert: bool = False) -> Dict[str, Union[str, bytes, Image.Image]]:
    """
    字符串转二维码（返回包含 PIL 图像对象的字典）
    Args:
        qr_str: 二维码文本
        border: 边框大小（默认2）
        invert: 是否反转颜色（默认False）
    Returns:
        Dict: 包含以下键的字典
            - str: ASCII 字符串形式的二维码
            - img: qrcode PIL.Image.Image 对象
    Raises:
        ValueError: 输入参数不合法时抛出
    """
    # 创建了一个 QRCode 对象 qr
    qr = qrcode.QRCode(
        version=1,  # 版本
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 纠错级别
        box_size=10,  # 方块大小
        border=border,  # 边框大小
    )
    # 将要转换的文本 qr_str 添加到二维码中
    qr.make(fit=True)
    qr.add_data(qr_str)
    # 生成二维码图像对象 img
    img = qr.make_image()
    # 将 Pillow 图像对象保存到一个内存中的字节流 buf 中
    buf = io.BytesIO()
    img.save(buf)
    # 捕获 print 输出
    save_stdout = sys.stdout  # 保存了当前的标准输出（stdout）
    output = io.StringIO()  # 创建一个 StringIO 对象来捕获 print 输出
    sys.stdout = output  # 将系统的标准输出重定向到 output
    # 使用 qr 对象的 print_ascii 方法将二维码以 ASCII 字符串的形式打印出来，并根据 invert 参数的值决定是否反转黑白颜色
    qr.print_ascii(out=None, tty=False, invert=invert)
    # 重定向输出到变量中
    output_str = output.getvalue()
    sys.stdout = save_stdout  # 恢复 sys.stdout
    # 1. 将 PyPNGImage 对象保存到临时文件
    img.save(os.path.join(GlobalVariableOfData.scripts_temp_dir, f"loginQRCode.png"))
    # 将临时文件打开为PIL.Image.Image 对象
    qr_pil_img = Image.open(os.path.join(GlobalVariableOfData.scripts_temp_dir, f"loginQRCode.png"))
    """
    qr的PIL.Image.Image 对象
    """
    try:
        os.remove(os.path.join(GlobalVariableOfData.scripts_temp_dir, f"loginQRCode.png"))
    except Exception as e:
        print(f"删除临时文件失败: {e}")
    return {"str": output_str, "img": qr_pil_img}


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
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        }

    def get_room_base_info(self, room_id: int):
        """
        直播间的
        @param room_id:
        @return:
        "data": {
            "by_uids": {},
            "by_room_ids": {
                "25322725": {
                    "room_id": 25322725,
                    "uid": 143474500,
                    "area_id": 192,
                    "live_status": 0,
                    "live_url": "https://live.bilibili.com/25322725",
                    "parent_area_id": 5,
                    "title": "obsのlua插件2测试",
                    "parent_area_name": "电台",
                    "area_name": "聊天电台",
                    "live_time": "0000-00-00 00:00:00",
                    "description": "个人简介测试",
                    "tags": "我的个人标签测试",
                    "attention": 35,
                    "online": 0,
                    "short_id": 0,
                    "uname": "兰阳音",
                    "cover": "http://i0.hdslb.com/bfs/live/new_room_cover/c17af2dbbbdfce33888e834bdb720edbf9515f95.jpg",
                    "background": "",
                    "join_slide": 1,
                    "live_id": 0,
                    "live_id_str": "0"
                }
            }
        }
        """
        api = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
        get_room_base_info_data = {
            'room_ids': room_id,
            'req_biz': "link-center"
        }
        room_base_info = requests.get(api, headers=self.headers, params=get_room_base_info_data).json()
        return room_base_info["data"]

    def get_area_obj_list(self):
        """
        获取直播分区
        @return:
        <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>code</td>
            <td>num</td>
            <td>返回值</td>
            <td>0：成功</td>
        </tr>
        <tr>
            <td>msg</td>
            <td>str</td>
            <td>错误信息</td>
            <td>默认为success</td>
        </tr>
        <tr>
            <td>message</td>
            <td>str</td>
            <td>错误信息</td>
            <td>默认为success</td>
        </tr>
        <tr>
            <td>data</td>
            <td>array</td>
            <td>父分区列表</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    <p><code>data</code>数组：</p>
    <table>
        <thead>
        <tr>
            <th>项</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>0</td>
            <td>obj</td>
            <td>父分区1</td>
            <td></td>
        </tr>
        <tr>
            <td>n</td>
            <td>obj</td>
            <td>父分区(n+1)</td>
            <td></td>
        </tr>
        <tr>
            <td>……</td>
            <td>obj</td>
            <td>……</td>
            <td>……</td>
        </tr>
        </tbody>
    </table>
    <p><code>data</code>数组中的对象：</p>
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>id</td>
            <td>num</td>
            <td>父分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>name</td>
            <td>name</td>
            <td>父分区名</td>
            <td></td>
        </tr>
        <tr>
            <td>list</td>
            <td>list</td>
            <td>子分区列表</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    <p><code>data</code>数组中的对象中的<code>list</code>数组：</p>
    <table>
        <thead>
        <tr>
            <th>项</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>0</td>
            <td>obj</td>
            <td>子分区1</td>
            <td></td>
        </tr>
        <tr>
            <td>n</td>
            <td>obj</td>
            <td>子分区(n+1)</td>
            <td></td>
        </tr>
        <tr>
            <td>……</td>
            <td>obj</td>
            <td>……</td>
            <td>……</td>
        </tr>
        </tbody>
    </table>
    <p><code>list</code>数组中的对象：</p>
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>id</td>
            <td>str</td>
            <td>子分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>parent_id</td>
            <td>str</td>
            <td>父分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>old_area_id</td>
            <td>str</td>
            <td>旧分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>name</td>
            <td>str</td>
            <td>子分区名</td>
            <td></td>
        </tr>
        <tr>
            <td>act_id</td>
            <td>str</td>
            <td>0</td>
            <td><strong>作用尚不明确</strong></td>
        </tr>
        <tr>
            <td>pk_status</td>
            <td>str</td>
            <td>？？？</td>
            <td><strong>作用尚不明确</strong></td>
        </tr>
        <tr>
            <td>hot_status</td>
            <td>num</td>
            <td>是否为热门分区</td>
            <td>0：否<br>1：是</td>
        </tr>
        <tr>
            <td>lock_status</td>
            <td>str</td>
            <td>0</td>
            <td><strong>作用尚不明确</strong></td>
        </tr>
        <tr>
            <td>pic</td>
            <td>str</td>
            <td>子分区标志图片url</td>
            <td></td>
        </tr>
        <tr>
            <td>parent_name</td>
            <td>str</td>
            <td>父分区名</td>
            <td></td>
        </tr>
        <tr>
            <td>area_type</td>
            <td>num</td>
            <td></td>
            <td></td>
        </tr>
        </tbody>
    </table>

        """
        get_area_obj_list_api = "https://api.live.bilibili.com/room/v1/Area/getList"
        area_list = requests.get(get_area_obj_list_api, headers=self.headers).json()
        return area_list["data"]

    def getsub_live_area_obj_list(self, parent_live_area_id: str) -> Optional[list[Dict[str, Union[str, int]]]]:  # 3.10及以上可以写成 Optional[list[Dict[str, str | int]]]
        """
        返回父分区对应的子分区对象列表
        Args:
            parent_live_area_id: 父分区id
        Returns:子分区对象列表或None
        """
        area_obj_list = self.get_area_obj_list()
        """
        所有分区的对象列表
        """
        for AreaObj in area_obj_list:
            if str(parent_live_area_id) == str(AreaObj["id"]):
                sub_live_area_obj_list = AreaObj["list"]
                """
                对应一级分区的二级分区对象列表
                """
                return sub_live_area_obj_list
        return None

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
        live_user_v1_master_info = requests.get(api, headers=self.headers, params=live_user_v1_master_info_data).json()
        return live_user_v1_master_info
    
    def get_room_info_old(self, mid: int) -> Dict:
        """
        直接用Bid查询到的直播间基础信息<br>
        @param mid: B站UID
        @type mid: int
        @return:
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>roomStatus</td>
                <td>num</td>
                <td>直播间 状态</td>
                <td>0：无房间<br>1：有房间</td>
            </tr>
            <tr>
                <td>roundStatus</td>
                <td>num</td>
                <td>轮播状态</td>
                <td>0：未轮播<br>1：轮播</td>
            </tr>
            <tr>
                <td>liveStatus</td>
                <td>num</td>
                <td>直播状态</td>
                <td>0：未开播<br>1：直播中</td>
            </tr>
            <tr>
                <td>url</td>
                <td>str</td>
                <td>直播间网页url</td>
                <td></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>直播间标题</td>
                <td></td>
            </tr>
            <tr>
                <td>cover</td>
                <td>str</td>
                <td>直播间封面url</td>
                <td></td>
            </tr>
            <tr>
                <td>online</td>
                <td>num</td>
                <td>直播间人气</td>
                <td>值为上次直播时刷新</td>
            </tr>
            <tr>
                <td>roomid</td>
                <td>num</td>
                <td>直播间id（短号）</td>
                <td></td>
            </tr>
            <tr>
                <td>broadcast_type</td>
                <td>num</td>
                <td>0</td>
                <td></td>
            </tr>
            <tr>
                <td>online_hidden</td>
                <td>num</td>
                <td>0</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        @rtype: Dict
        """
        api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
        get_room_info_old_data = {
            "mid": mid,
        }
        room_info_old = requests.get(api, headers=self.headers, params=get_room_info_old_data).json()
        return room_info_old["data"]

    # 登陆用函数
    def generate(self, ) -> Dict:
        """
        申请登录二维码
        @return: {'url': 二维码文本, 'qrcode_key': 扫描秘钥}
        """
        api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
        url8qrcode_key = requests.get(api, headers=self.headers).json()
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
        poll_return = requests.get(api, data=qrcode_key, headers=self.headers).json()
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
            buvid3 = requests.get(f'https://www.bilibili.com/video/', headers=self.headers)
            cookies.update(buvid3.cookies.get_dict())
        return {'code': code, 'cookies': cookies}


# end


# 登陆后才能用的函数
class BilibiliApiMaster:
    """登陆后才能用的函数"""

    def __init__(self, cookie: str):
        """
        完善 浏览器headers
        @param cookie: B站cookie
        """
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0")
        self.headers = {
            "User-Agent": user_agent,
            "cookie": cookie,
        }

    def interface_nav(self) -> Dict:
        """
        获取登录后导航栏用户信息
        @return:
        <p><code>data</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>isLogin</td>
                <td>bool</td>
                <td>是否已登录</td>
                <td>false：未登录<br>true：已登录</td>
            </tr>
            <tr>
                <td>email_verified</td>
                <td>num</td>
                <td>是否验证邮箱地址</td>
                <td>0：未验证<br>1：已验证</td>
            </tr>
            <tr>
                <td>face</td>
                <td>str</td>
                <td>用户头像 url</td>
                <td></td>
            </tr>
            <tr>
                <td>level_info</td>
                <td>obj</td>
                <td>等级信息</td>
                <td></td>
            </tr>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>用户 mid</td>
                <td></td>
            </tr>
            <tr>
                <td>mobile_verified</td>
                <td>num</td>
                <td>是否验证手机号</td>
                <td>0：未验证<br>1：已验证</td>
            </tr>
            <tr>
                <td>money</td>
                <td>num</td>
                <td>拥有硬币数</td>
                <td></td>
            </tr>
            <tr>
                <td>moral</td>
                <td>num</td>
                <td>当前节操值</td>
                <td>上限为70</td>
            </tr>
            <tr>
                <td>official</td>
                <td>obj</td>
                <td>认证信息</td>
                <td></td>
            </tr>
            <tr>
                <td>officialVerify</td>
                <td>obj</td>
                <td>认证信息 2</td>
                <td></td>
            </tr>
            <tr>
                <td>pendant</td>
                <td>obj</td>
                <td>头像框信息</td>
                <td></td>
            </tr>
            <tr>
                <td>scores</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>uname</td>
                <td>str</td>
                <td>用户昵称</td>
                <td></td>
            </tr>
            <tr>
                <td>vipDueDate</td>
                <td>num</td>
                <td>会员到期时间</td>
                <td>毫秒 时间戳</td>
            </tr>
            <tr>
                <td>vipStatus</td>
                <td>num</td>
                <td>会员开通状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>vipType</td>
                <td>num</td>
                <td>会员类型</td>
                <td>0：无<br>1：月度大会员<br>2：年度及以上大会员</td>
            </tr>
            <tr>
                <td>vip_pay_type</td>
                <td>num</td>
                <td>会员开通状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>vip_theme_type</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>vip_label</td>
                <td>obj</td>
                <td>会员标签</td>
                <td></td>
            </tr>
            <tr>
                <td>vip_avatar_subscript</td>
                <td>num</td>
                <td>是否显示会员图标</td>
                <td>0：不显示<br>1：显示</td>
            </tr>
            <tr>
                <td>vip_nickname_color</td>
                <td>str</td>
                <td>会员昵称颜色</td>
                <td>颜色码</td>
            </tr>
            <tr>
                <td>wallet</td>
                <td>obj</td>
                <td>B币钱包信息</td>
                <td></td>
            </tr>
            <tr>
                <td>has_shop</td>
                <td>bool</td>
                <td>是否拥有推广商品</td>
                <td>false：无<br>true：有</td>
            </tr>
            <tr>
                <td>shop_url</td>
                <td>str</td>
                <td>商品推广页面 url</td>
                <td></td>
            </tr>
            <tr>
                <td>allowance_count</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>answer_status</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>is_senior_member</td>
                <td>num</td>
                <td>是否硬核会员</td>
                <td>0：非硬核会员<br>1：硬核会员</td>
            </tr>
            <tr>
                <td>wbi_img</td>
                <td>obj</td>
                <td>Wbi 签名实时口令</td>
                <td>该字段即使用户未登录也存在</td>
            </tr>
            <tr>
                <td>is_jury</td>
                <td>bool</td>
                <td>是否风纪委员</td>
                <td>true：风纪委员<br>false：非风纪委员</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>level_info</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>current_level</td>
                <td>num</td>
                <td>当前等级</td>
                <td></td>
            </tr>
            <tr>
                <td>current_min</td>
                <td>num</td>
                <td>当前等级经验最低值</td>
                <td></td>
            </tr>
            <tr>
                <td>current_exp</td>
                <td>num</td>
                <td>当前经验</td>
                <td></td>
            </tr>
            <tr>
                <td>next_exp</td>
                <td>小于6级时：num<br>6级时：str</td>
                <td>升级下一等级需达到的经验</td>
                <td>当用户等级为Lv6时，值为<code>--</code>，代表无穷大</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>role</td>
                <td>num</td>
                <td>认证类型</td>
                <td>见<a href="/bilibili-API-collect/docs/user/official_role.html" class="">用户认证类型一览</a></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证备注</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：认证</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official_verify</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：认证</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>pendant</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>pid</td>
                <td>num</td>
                <td>挂件id</td>
                <td></td>
            </tr>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>挂件名称</td>
                <td></td>
            </tr>
            <tr>
                <td>image</td>
                <td>str</td>
                <td>挂件图片url</td>
                <td></td>
            </tr>
            <tr>
                <td>expire</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>vip_label</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>path</td>
                <td>str</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>text</td>
                <td>str</td>
                <td>会员名称</td>
                <td></td>
            </tr>
            <tr>
                <td>label_theme</td>
                <td>str</td>
                <td>会员标签</td>
                <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>wallet</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>登录用户mid</td>
                <td></td>
            </tr>
            <tr>
                <td>bcoin_balance</td>
                <td>num</td>
                <td>拥有B币数</td>
                <td></td>
            </tr>
            <tr>
                <td>coupon_balance</td>
                <td>num</td>
                <td>每月奖励B币数</td>
                <td></td>
            </tr>
            <tr>
                <td>coupon_due_time</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>wbi_img</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>img_url</td>
                <td>str</td>
                <td>Wbi 签名参数 <code>imgKey</code>的伪装 url</td>
                <td>详见文档 <a href="/bilibili-API-collect/docs/misc/sign/wbi.html" class="">Wbi 签名</a></td>
            </tr>
            <tr>
                <td>sub_url</td>
                <td>str</td>
                <td>Wbi 签名参数 <code>subKey</code>的伪装 url</td>
                <td>详见文档 <a href="/bilibili-API-collect/docs/misc/sign/wbi.html" class="">Wbi 签名</a></td>
            </tr>
            </tbody>
        </table>

        """
        api = "https://api.bilibili.com/x/web-interface/nav"
        headers = self.headers
        nav = requests.get(api, headers=headers).json()
        return nav["data"]

    def get_room_highlight_state(self):
        """
        获取直播间号
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/highlight/getRoomHighlightState"
        headers = self.headers
        room_id = requests.get(api, headers=headers).json()["data"]["room_id"]
        return room_id

    def get_room_news(self) -> str:
        # 获取直播公告
        headers = self.headers
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getRoomNews"
        params = {
            'room_id': self.get_room_highlight_state(),
            'uid': cookie2dict(self.headers["cookie"])["DedeUserID"]
        }
        room_news = requests.get(api, headers=headers, params=params).json()
        return room_news["data"]["content"]


class BilibiliApiCsrfAuthentication:
    """需要Csrf鉴权的"""

    def __init__(self, cookie: str):
        """
        需要Csrf
        :param cookie:
        """
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0")
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
        }
        self.cookies = cookie2dict(cookie)
        self.cookie = cookie
        self.csrf = self.cookies["bili_jct"]

    def AnchorChangeRoomArea(self, area_id: int):
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
            "room_id": BilibiliApiMaster(self.cookie).get_room_highlight_state(),
            "area_id": area_id,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        ChangeRoomArea_ReturnValue = requests.post(api, headers=headers, params=AnchorChangeRoomArea_data).json()
        return ChangeRoomArea_ReturnValue

    def startLive(self, area_id: int,  platform: str = "web_link"):
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
            "platform": platform,  # 直播姬（pc）：pc_link、web在线直播：web_link、bililink：android_link
            "room_id": BilibiliApiMaster(self.cookie).get_room_highlight_state(),
            "area_v2": area_id,
            "backup_stream": 0,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        startLive_ReturnValue = requests.post(api, headers=headers, params=startLivedata).json()
        return startLive_ReturnValue

    def stopLive(self):
        """
        结束直播
        @return:
        """
        api = "https://api.live.bilibili.com/room/v1/Room/stopLive"
        headers = self.headers
        csrf = self.csrf
        stopLive_data = {
            "platform": "pc",
            "room_id": BilibiliApiMaster(self.cookie).get_room_highlight_state(),
            "csrf": csrf,
            "csrf_token": csrf,
        }
        stopLive_ReturnValue = requests.post(api, headers=headers, params=stopLive_data).json()
        return stopLive_ReturnValue

    def FetchWebUpStreamAddr(self, reset_key: bool = False):
        """
        推流码信息
        @param reset_key: 布尔值，是否更新
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/live/FetchWebUpStreamAddr"
        headers = self.headers
        csrf = self.csrf
        FetchWebUpStreamAddr_data = {
            "platform": "pc",
            "backup_stream": 0,
            "reset_key": reset_key,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        FetchWebUpStreamAddre_ReturnValue = requests.post(api, headers=headers, params=FetchWebUpStreamAddr_data).json()
        return FetchWebUpStreamAddre_ReturnValue

    def send(self, roomid: int, msg: str):
        api = "https://api.live.bilibili.com/msg/send"
        headers = self.headers
        csrf = self.csrf
        send_data = {
            'msg': msg,
            'color': 16777215,
            'fontsize': 25,
            'rnd': str(time.time())[:8],
            'roomid': roomid,
            'csrf': csrf,
            'csrf_token': csrf
        }
        send_ReturnValue = requests.post(api, headers=headers, params=send_data).json()
        return send_ReturnValue

    def room_v1_Room_update(self, title: str):
        """
        更新直播标题
        @return:
        """
        headers = self.headers
        csrf = self.csrf
        api = "https://api.live.bilibili.com/room/v1/Room/update"
        room_v1_Room_update_data = {
            'room_id': BilibiliApiMaster(self.cookie).get_room_highlight_state(),
            'title': title,
            'csrf_token': csrf,
            'csrf': csrf
        }
        room_v1_Room_update_ReturnValue = requests.post(api, headers=headers, data=room_v1_Room_update_data).json()
        return room_v1_Room_update_ReturnValue

    def updateRoomNews(self, content: str):
        """
        更新直播公告
        @return:
        """
        headers = self.headers
        csrf = self.csrf
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/updateRoomNews"
        updateRoomNews_data = {
            'room_id': BilibiliApiMaster(self.cookie).get_room_highlight_state(),
            'uid': self.cookies["DedeUserID"],
            'content': content,
            'csrf_token': csrf,
            'csrf': csrf
        }
        updateRoomNews_ReturnValue = requests.post(api, headers=headers, data=updateRoomNews_data).json()
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
        response = requests.post(url=api_url, headers=headers, data=body).json()
        # 处理响应
        result = response
        logSave(0, f'"[上传结果]", {result}')
        return result

    def update_cover(self, CoverUrl: str):
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
              "537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        headers = {
            "User-Agent": UA,
            "cookie": self.cookie,
        }
        # 构建请求参数
        api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/preLive/UpdatePreLiveInfo"
        update_cover_data = {
            "platform": "web",
            "mobi_app": "web",
            "build": 1,
            "cover": CoverUrl,
            "coverVertical": "",
            "liveDirectionType": 1,
            "csrf_token": self.cookies["bili_jct"],
            "csrf": self.cookies["bili_jct"],
        }
        update_cover_ReturnValue = requests.post(api_url, headers=headers, params=update_cover_data).json()
        logSave(0, f"更新封面消息{update_cover_ReturnValue}")


# end


# 整合类函数
def login_try(config_path: Path, uid: Optional[int]):
    try:
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=config_path)
        uid = str(uid)
        logSave(0, f"尝试登录用户: {uid}")
        # 验证cookies完整性
        cookies = b_u_l_c.get_cookies(int(uid))
        if cookies is None:
            raise ValueError(f"缺少该用户: {uid}")
        required_keys = {"DedeUserID", "SESSDATA", "bili_jct"}
        missing = required_keys - cookies.keys()
        if missing:
            raise ValueError(f"cookies缺少必要字段: {', '.join(missing)}")
        isLogin = BilibiliApiMaster(dict2cookie(cookies)).interface_nav()["isLogin"]
        if not isLogin:
            logSave(3, f"用户 {uid} 的cookies已过期")
            return False
        b_u_l_c.update_ser(cookies)
        logSave(0, f"用户 {uid} 登录成功")
        return True
    except ValueError as e:
        logSave(3, f"参数错误: {str(e)}")
        raise
    except Exception as e:
        logSave(2, f"登录过程异常: {str(e)}")
        raise RuntimeError("登录服务暂时不可用") from e


def check_poll():
    """
    二维码扫描登录状态检测
    @return: cookies，超时为{}
    """
    # 获取uid对应的cookies
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(GlobalVariableOfData.scripts_config_filepath)
    user_list_dict = b_u_l_c.get_users()
    code_old = GlobalVariableOfData.loginQrCodeReturn['code']
    GlobalVariableOfData.loginQrCodeReturn = BilibiliApiGeneric().poll(GlobalVariableOfData.loginQrCode_key)
    # 二维码扫描登陆状态改变时，输出改变后状态
    logSave(2, str(information4login_qr_return_code[GlobalVariableOfData.loginQrCodeReturn['code']])) if code_old != GlobalVariableOfData.loginQrCodeReturn['code'] else None
    if GlobalVariableOfData.loginQrCodeReturn['code'] == 0 or GlobalVariableOfData.loginQrCodeReturn['code'] == 86038:
        GlobalVariableOfData.LoginQRCodePillowImg = None
        # 二维码扫描登陆状态为成功或者超时时获取cookies结束[轮询二维码扫描登陆状态]
        cookies = GlobalVariableOfData.loginQrCodeReturn['cookies']
        if cookies:
            # 获取登陆账号cookies中携带的uid
            uid = int(cookies['DedeUserID'])
            if str(uid) in user_list_dict.values():
                logSave(1, "已有该用户，正在更新用户登录信息")
                b_u_l_c.update_ser(cookies, False)
            else:
                b_u_l_c.add_user(cookies)
                logSave(0, "添加用户成功")
                # 请点击按钮【更新账号列表】，更新用户列表
                logSave(0, "请点击按钮【更新账号列表】，更新用户列表")
        else:
            logSave(0, "添加用户失败")
        # 结束计时器
        obs.remove_current_callback()


def qr_add_user():
    """
    扫码登陆记录用户cookies
    """
    # 申请登录二维码
    url8qrkey = BilibiliApiGeneric().generate()
    # 获取二维码url
    url = url8qrkey['url']
    logSave(0, f"获取登录二维码链接{url}")
    # 获取二维码key
    GlobalVariableOfData.loginQrCode_key = url8qrkey['qrcode_key']
    logSave(0, f"获取登录二维码密钥{GlobalVariableOfData.loginQrCode_key}")
    # 获取二维码对象
    qr = qr_text8pil_img(url)
    # 获取登录二维码的pillow img实例
    GlobalVariableOfData.LoginQRCodePillowImg = qr["img"]
    # 输出二维码图形字符串
    logSave(0, qr["str"])
    logSave(0, f"字符串二维码已输出，如果乱码或者扫描不上，建议点击 按钮【显示登录二维码图片】")
    # 获取二维码扫描登陆状态
    GlobalVariableOfData.loginQrCodeReturn = BilibiliApiGeneric().poll(GlobalVariableOfData.loginQrCode_key)
    logSave(0, f"开始轮询登录状态")
    # 轮询登录状态
    logSave(2, str(information4login_qr_return_code[GlobalVariableOfData.loginQrCodeReturn['code']]))
    # 开始计时器
    obs.timer_add(check_poll, 1000)


# end

# ====================================================================================================================


# -----------------------------------------------------------
# OBS Script Functions                                      -
# -----------------------------------------------------------

def on_event(event):
    """
    处理推流事件
    """
    logSave(0, f"┏━━━━监测到obs前端事件━━━━━┓")
    logSave(0, f"┃    监测到obs前端事件     ┃{information4frontend_event[event]}")
    logSave(0, f"┗━━━━监测到obs前端事件━━━━━┛")
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        last_status_change = time.time()
        logSave(0, f"监控到推流开始事件: {last_status_change}")
        if GlobalVariableOfTheControl.streaming_active is not None and GlobalVariableOfTheControl.streaming_active != obs.obs_frontend_streaming_active():
            logSave(0, f"推流状态发生变化：{GlobalVariableOfTheControl.streaming_active}➡️{obs.obs_frontend_streaming_active()}")
            GlobalVariableOfTheControl.streaming_active = obs.obs_frontend_streaming_active()
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        last_status_change = time.time()
        logSave(0, f"监控到推流停止事件: {last_status_change}")
        if GlobalVariableOfTheControl.streaming_active is not None and GlobalVariableOfTheControl.streaming_active != obs.obs_frontend_streaming_active():
            logSave(0, f"推流状态发生变化：{GlobalVariableOfTheControl.streaming_active}➡️{obs.obs_frontend_streaming_active()}")
            GlobalVariableOfTheControl.streaming_active = obs.obs_frontend_streaming_active()
            logSave(0, f"尝试关闭直播")


# --- 设置默认值
def script_defaults(settings):  # 设置其默认值
    """
    调用以设置与脚本关联的默认设置(如果有的话)。为了设置其默认值，您通常会调用默认值函数。
    :param settings:与脚本关联的设置。
    """
    logSave(0, "╔══════设置控件默认属性══════╗")
    logSave(0, "║      设置控件默认属性      ║")
    logSave(0, "╚══════设置控件默认属性══════╝")
    # obs推流状态
    GlobalVariableOfTheControl.streaming_active = obs.obs_frontend_streaming_active()

    # obs脚本中控件的数据
    GlobalVariableOfTheControl.script_settings = settings

    # 路径变量
    # #脚本数据保存目录
    GlobalVariableOfData.scripts_data_dirpath = f"{script_path()}bilibili-live"
    logSave(0, f"脚本用户数据文件夹路径：{GlobalVariableOfData.scripts_data_dirpath}")
    # #脚本用户数据路径
    GlobalVariableOfData.scripts_config_filepath = Path(GlobalVariableOfData.scripts_data_dirpath) / "config.json"
    logSave(0, f"脚本用户数据路径：{GlobalVariableOfData.scripts_config_filepath}")
    GlobalVariableOfData.scripts_temp_dir = Path(GlobalVariableOfData.scripts_data_dirpath) / "temp"
    os.makedirs(GlobalVariableOfData.scripts_temp_dir, exist_ok=True)
    logSave(0, f"脚本临时文件夹路径：{GlobalVariableOfData.scripts_temp_dir}")
    GlobalVariableOfData.networkConnectionStatus = check_network_connection()
    if not GlobalVariableOfData.networkConnectionStatus:
        logSave(1, f"======= 最终结果: 网络{'可用' if GlobalVariableOfData.networkConnectionStatus else '不可用'} =======")
        return None
    if GlobalVariableOfData.accountAvailabilityDetectionSwitch:
        logSave(1, f"执行账号可用性检测")
        # 创建用户配置文件实例
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
        # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
        user_interface_nav4uid = {uid: BilibiliApiMaster(dict2cookie(
            b_u_l_c.get_cookies(int(uid)))).interface_nav() for uid in [x for x in b_u_l_c.get_users().values() if x]}
        # 获取 用户配置文件 中 每一个 用户 的 可用性
        user_is_login4uid = {uid: user_interface_nav4uid[uid]["isLogin"] for uid in user_interface_nav4uid}
        # 删除 用户配置文件 中 不可用 用户
        [b_u_l_c.delete_user(int(uid)) for uid in user_is_login4uid if not user_is_login4uid[uid]]
        # 获取 用户配置文件 中 每一个 可用 用户 的 昵称
        all_uname4uid = {uid: user_interface_nav4uid[uid]["uname"] for uid in user_is_login4uid if user_is_login4uid[uid]}
        """
        全部账户的数据
        {uid: uname}
        """
        # 输出日志
        [logSave(1, f"账号：{uid} {'不可用，已删除' if not user_is_login4uid[uid] else '可用'}") for uid in user_is_login4uid]
        logSave(1, f"可用账号：{str(all_uname4uid)}")
        GlobalVariableOfData.accountAvailabilityDetectionSwitch = False
        logSave(1, f"关闭账号可用性检测")

    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
    user_interface_nav4uid = {uid: BilibiliApiMaster(dict2cookie(b_u_l_c.get_cookies(int(uid)))).interface_nav() for uid in [x for x in b_u_l_c.get_users().values() if x]}
    # 获取 用户配置文件 中 每一个 用户 的 昵称
    all_uname4uid = {uid: user_interface_nav4uid[uid]["uname"] for uid in user_interface_nav4uid}
    logSave(0, f"载入账号：{str(all_uname4uid)}")
    DefaultUserInterfaceNav = BilibiliApiMaster(dict2cookie(
        b_u_l_c.get_cookies())).interface_nav() if b_u_l_c.get_cookies() else None  # 获取 '默认账户' 导航栏用户信息
    DefaultUname = DefaultUserInterfaceNav["uname"] if b_u_l_c.get_cookies() else None  # 获取默认账号的昵称
    """
    默认用户config["DefaultUser"]的昵称
    没有则为None
    """
    logSave(0, f"用户：{DefaultUname} 已登录" if b_u_l_c.get_cookies() else f"未登录账号")
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 设置 只读文本框【登录状态】 可见状态
    GlobalVariableOfTheControl.login_status_textBox_visible = True
    logSave(0, f"设置 只读文本框【登录状态】 可见状态：{str(GlobalVariableOfTheControl.login_status_textBox_visible)}")
    # 设置 只读文本框【登录状态】 可用状态
    GlobalVariableOfTheControl.login_status_textBox_enabled = True
    logSave(0, f"设置 只读文本框【登录状态】 可用状态：{str(GlobalVariableOfTheControl.login_status_textBox_enabled)}")
    # 设置 只读文本框【登录状态】 信息类型
    GlobalVariableOfTheControl.login_status_textBox_type = obs.OBS_TEXT_INFO_NORMAL if b_u_l_c.get_cookies() else obs.OBS_TEXT_INFO_WARNING
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 只读文本框【登录状态】 信息类型：{textBox_type_name4textBox_type[GlobalVariableOfTheControl.login_status_textBox_type]}")
    # 设置 只读文本框【登录状态】 内容
    GlobalVariableOfTheControl.login_status_textBox_string = f'{DefaultUname} 已登录' if b_u_l_c.get_cookies() else '未登录，请登录后点击【更新账号列表】'
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 只读文本框【登录状态】 内容：{GlobalVariableOfTheControl.login_status_textBox_string}")

    # 设置 组合框【用户】 可见状态
    GlobalVariableOfTheControl.uid_comboBox_visible = True
    logSave(0, f"设置 组合框【用户】 可见状态：{str(GlobalVariableOfTheControl.uid_comboBox_visible)}")
    # 设置 组合框【用户】 可用状态
    GlobalVariableOfTheControl.uid_comboBox_enabled = True
    logSave(0, f"设置 组合框【用户】 可用状态：{str(GlobalVariableOfTheControl.uid_comboBox_enabled)}")
    # 设置 组合框【用户】 的数据字典
    GlobalVariableOfTheControl.uid_comboBox_dict = {uid or '-1': all_uname4uid.get(uid, '添加或选择一个账号登录') for uid in b_u_l_c.get_users().values()}
    logSave(0, f"设置 组合框【用户】 数据字典：{str(GlobalVariableOfTheControl.uid_comboBox_dict)}")
    # 设置 组合框【用户】 默认显示内容
    GlobalVariableOfTheControl.uid_comboBox_string = DefaultUname if b_u_l_c.get_cookies() else '添加或选择一个账号登录'
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 组合框【用户】 内容：{GlobalVariableOfTheControl.uid_comboBox_string}")
    # 设置 组合框【用户】 默认显示内容 的 列表值
    GlobalVariableOfTheControl.uid_comboBox_value = b_u_l_c.get_users()[0] if b_u_l_c.get_cookies() else '-1'
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 组合框【用户】 列表值：{GlobalVariableOfTheControl.uid_comboBox_value}")

    # 设置 按钮【登录账号】 可见状态
    GlobalVariableOfTheControl.login_button_visible = True if all_uname4uid else False
    logSave(0, f"根据 是否有账户：{str(bool(all_uname4uid))}，设置 按钮【登录账号】 可见状态：{str(GlobalVariableOfTheControl.login_button_visible)}")
    # 设置 按钮【登录账号】 可用状态
    GlobalVariableOfTheControl.login_button_enabled = True if all_uname4uid else False
    logSave(0, f"根据 是否有账户：{str(bool(all_uname4uid))}，设置 按钮【登录账号】 可用状态：{str(GlobalVariableOfTheControl.login_button_enabled)}")

    # 设置 按钮【更新账号列表】 可见状态
    GlobalVariableOfTheControl.update_account_list_button_visible = True
    logSave(0, f"设置 按钮【更新账号列表】 可见状态：{str(GlobalVariableOfTheControl.update_account_list_button_visible)}")
    # 设置 按钮【更新账号列表】 可用状态
    GlobalVariableOfTheControl.update_account_list_button_enabled = True
    logSave(0, f"设置 按钮【更新账号列表】 可用状态：{str(GlobalVariableOfTheControl.update_account_list_button_enabled)}")

    # 设置 按钮【二维码添加账户】 可见状态
    GlobalVariableOfTheControl.qr_add_account_button_visible = True
    logSave(0, f"设置 按钮【二维码添加账户】 可见状态：{str(GlobalVariableOfTheControl.qr_add_account_button_visible)}")
    # 设置 按钮【二维码添加账户】 可用状态
    GlobalVariableOfTheControl.qr_add_account_button_enabled = True
    logSave(0, f"设置 按钮【二维码添加账户】 可用状态：{str(GlobalVariableOfTheControl.qr_add_account_button_enabled)}")

    # 设置 按钮【显示二维码图片】 可见状态
    GlobalVariableOfTheControl.display_qr_picture_button_visible = True
    logSave(0, f"设置 按钮【显示二维码图片】 可见状态：{str(GlobalVariableOfTheControl.display_qr_picture_button_visible)}")
    # 设置 按钮【显示二维码图片】 可用状态
    GlobalVariableOfTheControl.display_qr_picture_button_enabled = True
    logSave(0, f"设置 按钮【显示二维码图片】 可用状态：{str(GlobalVariableOfTheControl.display_qr_picture_button_enabled)}")

    # 设置 按钮【删除账户】 可见状态
    GlobalVariableOfTheControl.delete_account_button_visible = True if all_uname4uid else False
    logSave(0, f"根据 是否有账户：{str(bool(all_uname4uid))}，设置 按钮【删除账户】 可见状态：{str(GlobalVariableOfTheControl.delete_account_button_visible)}")
    # 设置 按钮【删除账户】 可用状态
    GlobalVariableOfTheControl.delete_account_button_enabled = True if all_uname4uid else False
    logSave(0, f"根据 是否有账户：{str(bool(all_uname4uid))}，设置 按钮【删除账户】 可用状态：{str(GlobalVariableOfTheControl.delete_account_button_enabled)}")

    # 设置 按钮【备份账户】 可见状态
    GlobalVariableOfTheControl.backup_account_button_visible = False
    logSave(0, f"设置 按钮【备份账户】 可见状态：{str(GlobalVariableOfTheControl.backup_account_button_visible)}")
    # 设置 按钮【备份账户】 可用状态
    GlobalVariableOfTheControl.backup_account_button_enabled = False
    logSave(0, f"设置 按钮【备份账户】 可用状态：{str(GlobalVariableOfTheControl.backup_account_button_enabled)}")

    # 设置 按钮【恢复账户】 可见状态
    GlobalVariableOfTheControl.restore_account_button_visible = False
    logSave(0, f"设置 按钮【恢复账户】 可见状态：{str(GlobalVariableOfTheControl.restore_account_button_visible)}")
    # 设置 按钮【恢复账户】 可用状态
    GlobalVariableOfTheControl.restore_account_button_enabled = False
    logSave(0, f"设置 按钮【恢复账户】 可用状态：{str(GlobalVariableOfTheControl.restore_account_button_enabled)}")

    # 设置 按钮【登出账号】 可见状态
    GlobalVariableOfTheControl.logout_button_visible = True if all_uname4uid and b_u_l_c.get_cookies() else False
    logSave(0, f"根据 是否有账户：{str(bool(all_uname4uid))}，是否登录：{str(bool(b_u_l_c.get_cookies()))}，设置 按钮【登出账号】 可见状态：{str(GlobalVariableOfTheControl.logout_button_visible)}")
    # 设置 按钮【登出账号】 可用状态
    GlobalVariableOfTheControl.logout_button_enabled = True if all_uname4uid and b_u_l_c.get_cookies() else False
    logSave(0, f"根据 是否有账户：{str(bool(all_uname4uid))}，是否登录：{str(bool(b_u_l_c.get_cookies()))}，设置 按钮【登出账号】 可用状态：{str(GlobalVariableOfTheControl.logout_button_enabled)}")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    # 获取'默认账户'获取用户对应的直播间 状态
    RoomInfoOld = BilibiliApiGeneric().get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else {}
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 获取 登录账户 对应的直播间 状态：数据长度为{len(RoomInfoOld)}")
    # 获取 默认用户 的 直播间 状态
    DefaultRoomStatus = RoomInfoOld["roomStatus"] if b_u_l_c.get_cookies() else None
    """
    登录的用户的直播间存在状态
    """
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 获取 登录账户 是否有直播间：{DefaultRoomStatus}")
    # 获取默认用户的 直播间id
    DefaultRoomid = RoomInfoOld["roomid"] if bool(DefaultRoomStatus) else 0
    """
    登录的用户的直播间id
    """
    logSave(0, f"根据 登录账户 直播间存在：{bool(DefaultRoomStatus)} 获取 登录账户 的 直播间id：{DefaultRoomid}")
    # 获取默认用户的 直播状态
    DefaultLiveStatus = RoomInfoOld["liveStatus"] if bool(DefaultRoomStatus) else None
    """
    直播状态
    0：未开播 1：直播中
    """
    logSave(0, f"根据 登录账户 直播间存在：{bool(DefaultRoomStatus)} 获取 登录账户 的 直播状态：{DefaultLiveStatus}")
    # 获取'默认账户'直播间的基础信息
    RoomBaseInfo = BilibiliApiGeneric().get_room_base_info(DefaultRoomid) if DefaultRoomStatus else {}
    # 获取'默认账户'直播间的分区
    DefaultArea = {
            "id": RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["parent_area_id"],
            "name": RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["parent_area_name"],
            "data": {
                "id": RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["area_id"],
                "name": RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["area_name"],
            }
        } if DefaultRoomStatus else {}
    """
    默认的直播分区
    {"id": parent_area_id, "name": parent_area_name, "data":{"id": area_id, "name": area_name}}
    """
    logSave(0, f"获取 登录账户 当前直播间分区数据{DefaultArea}")
    # 获取完整直播分区
    parentLiveAreaNameByid4dict = {str(AreaObj["id"]): AreaObj["name"] for AreaObj in BilibiliApiGeneric().get_area_obj_list()} | {} if DefaultArea else {"-1": "请选择一级分区"}
    logSave(0, f"根据 登录账户 当前直播间分区数据存在：{bool(DefaultArea)} 获取 直播间父分区数据{parentLiveAreaNameByid4dict}")
    subLiveAreaNameByid4dict = {str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in BilibiliApiGeneric().getsub_live_area_obj_list(DefaultArea['id'])} if DefaultArea else {"-1": "请选择一级分区"}
    logSave(0, f"根据 登录账户 当前直播间分区数据存在：{bool(DefaultArea)} 获取 登录账户 当前父分区对应的子分区数据{subLiveAreaNameByid4dict}")

    # 设置 只读文本框【直播间 状态】 可见状态
    GlobalVariableOfTheControl.room_status_textBox_visible = True
    logSave(0, f"设置 按钮【查看直播间封面】 可见状态：{str(GlobalVariableOfTheControl.room_status_textBox_visible)}")
    # 设置 只读文本框【直播间 状态】 可用状态
    GlobalVariableOfTheControl.room_status_textBox_enabled = True
    logSave(0, f"设置 按钮【查看直播间封面】 可用状态：{str(GlobalVariableOfTheControl.room_status_textBox_enabled)}")
    # 设置 只读文本框【直播间 状态】 的类型
    GlobalVariableOfTheControl.room_status_textBox_type = (obs.OBS_TEXT_INFO_NORMAL if bool(DefaultRoomStatus) else obs.OBS_TEXT_INFO_WARNING) if b_u_l_c.get_cookies() else obs.OBS_TEXT_INFO_ERROR
    logSave(0, f"根据 登录状态：{bool(b_u_l_c.get_cookies())} 和 直播间存在：{bool(DefaultRoomStatus)} 设置 只读文本框【直播间 状态】 的类型{textBox_type_name4textBox_type[GlobalVariableOfTheControl.room_status_textBox_type]}")
    # 设置 只读文本框【直播间 状态】 的内容
    GlobalVariableOfTheControl.room_status_textBox_string = (f"{str(DefaultRoomid)}{'直播中' if DefaultLiveStatus else '未开播'}" if DefaultRoomStatus else "无直播间") if b_u_l_c.get_cookies() else "未登录"
    logSave(0, f"根据 登录状态：{bool(b_u_l_c.get_cookies())} 和 直播间存在：{bool(DefaultRoomStatus)} 设置 只读文本框【直播间 状态】 的内容{GlobalVariableOfTheControl.room_status_textBox_type}")

    # 设置 按钮【查看直播间封面】 可见状态
    GlobalVariableOfTheControl.viewLiveCover_button_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【查看直播间封面】 可见状态：{str(GlobalVariableOfTheControl.viewLiveCover_button_visible)}")
    # 设置 按钮【查看直播间封面】 可用状态
    GlobalVariableOfTheControl.viewLiveCover_button_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【查看直播间封面】 可用状态：{str(GlobalVariableOfTheControl.viewLiveCover_button_enabled)}")

    # 设置 文件对话框【直播间封面】 可见状态
    GlobalVariableOfTheControl.room_cover_fileDialogBox_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 文件对话框【直播间封面】 可见状态：{str(GlobalVariableOfTheControl.room_cover_fileDialogBox_visible)}")
    # 设置 文件对话框【直播间封面】 可用状态
    GlobalVariableOfTheControl.room_cover_fileDialogBox_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 文件对话框【直播间封面】 可用状态：{str(GlobalVariableOfTheControl.room_cover_fileDialogBox_enabled)}")
    # 设置 文件对话框【直播间封面】 内容
    GlobalVariableOfTheControl.room_cover_fileDialogBox_string = ""
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 文件对话框【直播间封面】 内容：{str(GlobalVariableOfTheControl.room_cover_fileDialogBox_string)}")

    # 设置 按钮【上传直播间封面】 可见状态
    GlobalVariableOfTheControl.room_cover_update_button_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【上传直播间封面】 可见状态：{str(GlobalVariableOfTheControl.room_cover_update_button_visible)}")
    # 设置 按钮【上传直播间封面】 可用状态
    GlobalVariableOfTheControl.room_cover_update_button_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【上传直播间封面】 可用状态：{str(GlobalVariableOfTheControl.room_cover_update_button_enabled)}")

    # 设置 普通文本框【直播间标题】 可见状态
    GlobalVariableOfTheControl.liveRoom_title_textBox_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 普通文本框【直播间标题】 可见状态：{str(GlobalVariableOfTheControl.liveRoom_title_textBox_visible)}")
    # 设置 普通文本框【直播间标题】 可用状态
    GlobalVariableOfTheControl.liveRoom_title_textBox_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 普通文本框【直播间标题】 可用状态：{str(GlobalVariableOfTheControl.liveRoom_title_textBox_enabled)}")
    # 设置 普通文本框【直播间标题】 内容
    GlobalVariableOfTheControl.liveRoom_title_textBox_string = RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["title"] if bool(GlobalVariableOfTheControl.liveRoom_title_textBox_visible) else ""
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 普通文本框【直播间标题】 内容：{str(GlobalVariableOfTheControl.liveRoom_title_textBox_string)}")

    # 设置 按钮【更改直播间标题】 可见状态
    GlobalVariableOfTheControl.change_liveRoom_title_button_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【更改直播间标题】 可见状态：{str(GlobalVariableOfTheControl.change_liveRoom_title_button_visible)}")
    # 设置 按钮【更改直播间标题】 可用状态
    GlobalVariableOfTheControl.change_liveRoom_title_button_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【更改直播间标题】 可用状态：{str(GlobalVariableOfTheControl.change_liveRoom_title_button_enabled)}")

    # 设置 普通文本框【直播间公告】 可见状态
    GlobalVariableOfTheControl.liveRoom_news_textBox_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 普通文本框【直播间公告】 可见状态：{str(GlobalVariableOfTheControl.liveRoom_news_textBox_visible)}")
    # 设置 普通文本框【直播间公告】 可用状态
    GlobalVariableOfTheControl.liveRoom_news_textBox_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 普通文本框【直播间公告】 可用状态：{str(GlobalVariableOfTheControl.liveRoom_news_textBox_enabled)}")
    # 设置 普通文本框【直播间公告】 内容
    GlobalVariableOfTheControl.liveRoom_news_textBox_string = BilibiliApiMaster(dict2cookie(
        b_u_l_c.get_cookies())).get_room_news() if bool(DefaultRoomStatus) else ""
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 普通文本框【直播间公告】 内容：{str(GlobalVariableOfTheControl.liveRoom_news_textBox_string)}")

    # 设置 按钮【更改直播间公告】 可见状态
    GlobalVariableOfTheControl.change_liveRoom_news_button_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【更改直播间公告】 可见状态：{str(GlobalVariableOfTheControl.change_liveRoom_news_button_visible)}")
    # 设置 按钮【更改直播间公告】 可用状态
    GlobalVariableOfTheControl.change_liveRoom_news_button_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【更改直播间公告】 可用状态：{str(GlobalVariableOfTheControl.change_liveRoom_news_button_enabled)}")

    # 设置 组合框【一级分区】 可见状态
    GlobalVariableOfTheControl.parentLiveArea_comboBox_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 组合框【一级分区】 可见状态：{str(GlobalVariableOfTheControl.parentLiveArea_comboBox_visible)}")
    # 设置 组合框【一级分区】 可用状态
    GlobalVariableOfTheControl.parentLiveArea_comboBox_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 组合框【一级分区】 可用状态：{str(GlobalVariableOfTheControl.parentLiveArea_comboBox_enabled)}")
    # 设置 组合框【一级分区】 的数据字典
    GlobalVariableOfTheControl.parentLiveArea_comboBox_dict = parentLiveAreaNameByid4dict
    logSave(0, f"设置 组合框【一级分区】 数据字典：{str(GlobalVariableOfTheControl.parentLiveArea_comboBox_dict)}")
    # 设置 组合框【一级分区】 默认显示内容
    GlobalVariableOfTheControl.parentLiveArea_comboBox_string = str(DefaultArea["name"]) if bool(DefaultArea) else "请选择一级分区"
    logSave(0, f"根据 默认账户当前直播间 分区存在：{str(bool(DefaultArea))}，设置 组合框【一级分区】 默认显示内容：{str(GlobalVariableOfTheControl.parentLiveArea_comboBox_string)}")
    # 设置 组合框【一级分区】 默认显示内容 的 列表值
    GlobalVariableOfTheControl.parentLiveArea_comboBox_value = str(DefaultArea["id"]) if bool(DefaultArea) else "-1"
    logSave(0, f"根据 默认账户当前直播间 分区存在：{str(bool(DefaultArea))}，设置 组合框【一级分区】 默认显示内容 的 列表值：{str(GlobalVariableOfTheControl.parentLiveArea_comboBox_value)}")

    # 设置 按钮【确认一级分区】 可见状态
    GlobalVariableOfTheControl.parentLiveArea_true_button_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【确认一级分区】 可见状态：{str(GlobalVariableOfTheControl.parentLiveArea_true_button_visible)}")
    # 设置 按钮【确认一级分区】 可用状态
    GlobalVariableOfTheControl.parentLiveArea_true_button_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【确认一级分区】 可用状态：{str(GlobalVariableOfTheControl.parentLiveArea_true_button_enabled)}")

    # 设置 组合框【二级分区】 可见状态
    GlobalVariableOfTheControl.subLiveArea_comboBox_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 组合框【二级分区】 可见状态：{str(GlobalVariableOfTheControl.subLiveArea_comboBox_visible)}")
    # 设置 组合框【二级分区】 可用状态
    GlobalVariableOfTheControl.subLiveArea_comboBox_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 组合框【二级分区】 可用状态：{str(GlobalVariableOfTheControl.subLiveArea_comboBox_enabled)}")
    # 设置 组合框【二级分区】 数据字典
    GlobalVariableOfTheControl.subLiveArea_comboBox_dict = subLiveAreaNameByid4dict
    logSave(0, f"设置 组合框【二级分区】 数据字典：{str(GlobalVariableOfTheControl.subLiveArea_comboBox_dict)}")
    # 设置 组合框【二级分区】 默认显示内容
    GlobalVariableOfTheControl.subLiveArea_comboBox_string = str(DefaultArea["data"]["name"]) if bool(DefaultArea) else "请确认一级分区"
    logSave(0, f"根据 默认账户当前直播间 分区存在：{str(bool(DefaultArea))}，设置 组合框【二级分区】 默认显示内容：{str(GlobalVariableOfTheControl.subLiveArea_comboBox_string)}")
    # 设置 组合框【二级分区】 默认显示内容 的 列表值
    GlobalVariableOfTheControl.subLiveArea_comboBox_value = str(DefaultArea["data"]["id"]) if bool(DefaultArea) else "-1"
    logSave(0, f"根据 默认账户当前直播间 分区存在：{str(bool(DefaultArea))}，设置 组合框【二级分区】 默认显示内容 的 列表值：{str(GlobalVariableOfTheControl.subLiveArea_comboBox_value)}")

    # 设置 按钮【「确认分区」】 可见状态
    GlobalVariableOfTheControl.subLiveArea_true_button_visible = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【确认分区】 可见状态：{str(bool(GlobalVariableOfTheControl.subLiveArea_true_button_visible))}")
    # 设置 按钮【「确认分区」】 可用状态
    GlobalVariableOfTheControl.subLiveArea_true_button_enabled = bool(DefaultRoomStatus)
    logSave(0, f"根据 直播间存在：{str(bool(DefaultRoomStatus))}，设置 按钮【确认分区】 可见状态：{str(bool(GlobalVariableOfTheControl.subLiveArea_true_button_enabled))}")

    # 设置 url按钮【跳转直播间后台网页】 可见状态
    GlobalVariableOfTheControl.jump_blive_web_button_visible = True
    logSave(0, f"设置 url按钮【跳转直播间后台网页】 可见状态：{str(bool(GlobalVariableOfTheControl.jump_blive_web_button_visible))}")
    # 设置 url按钮【跳转直播间后台网页】 可用状态
    GlobalVariableOfTheControl.jump_blive_web_button_enabled = True
    logSave(0, f"设置 url按钮【跳转直播间后台网页】 可用状态：{str(bool(GlobalVariableOfTheControl.jump_blive_web_button_enabled))}")
    # 设置 url按钮【跳转直播间后台网页】 链接
    GlobalVariableOfTheControl.jump_blive_web_button_url = "https://link.bilibili.com/p/center/index#/my-room/start-live"
    logSave(0, f"设置 url按钮【跳转直播间后台网页】 链接：{GlobalVariableOfTheControl.jump_blive_web_button_url}")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 设置 组合框【直播平台】 可见状态
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 组合框【直播平台】 可见状态：{str(GlobalVariableOfTheControl.jump_blive_web_button_visible)}")
    # 设置 组合框【直播平台】 可用状态
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 组合框【直播平台】 可用状态：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled)}")
    # 设置 组合框【直播平台】 的数据字典
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict = {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}
    logSave(0, f"设置 组合框【直播平台】 的数据字典：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict)}")
    # 设置 组合框【直播平台】 的内容
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_string = ""
    logSave(0, f"设置 组合框【直播平台】 的内容：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_string)}")
    # 设置 组合框【直播平台】 的内容 的 列表值
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_value = ""
    logSave(0, f"设置 组合框【直播平台】 的内容 的 列表值：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_value)}")

    # 设置 按钮【开始直播并复制推流码】 可见状态
    GlobalVariableOfTheControl.start_live_button_visible = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【开始直播并复制推流码】 可见状态：{str(GlobalVariableOfTheControl.start_live_button_visible)}")
    # 设置 按钮【开始直播并复制推流码】 可用状态
    GlobalVariableOfTheControl.start_live_button_enabled = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【开始直播并复制推流码】 可用状态：{str(GlobalVariableOfTheControl.start_live_button_enabled)}")

    # 设置 按钮【复制直播服务器】 可见状态
    GlobalVariableOfTheControl.rtmp_address_copy_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播服务器】 可见状态：{str(GlobalVariableOfTheControl.rtmp_address_copy_button_visible)}")
    # 设置 按钮【复制直播服务器】 可用状态
    GlobalVariableOfTheControl.rtmp_address_copy_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播服务器】 可用状态：{str(GlobalVariableOfTheControl.rtmp_address_copy_button_enabled)}")

    # 设置 按钮【复制直播推流码】 可见状态
    GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播推流码】 可见状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible)}")
    # 设置 按钮【复制直播推流码】 可用状态
    GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播推流码】 可用状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled)}")

    # 设置 按钮【更新推流码并复制】 可见状态
    GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【更新推流码并复制】 可见状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible)}")
    # 设置 按钮【更新推流码并复制】 可用状态
    GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【更新推流码并复制】 可用状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled)}")

    # 设置 按钮【结束直播】 可见状态
    GlobalVariableOfTheControl.stop_live_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【结束直播】 可见状态：{str(GlobalVariableOfTheControl.stop_live_button_visible)}")
    # 设置 按钮【结束直播】 可用状态
    GlobalVariableOfTheControl.stop_live_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【结束直播】 可用状态：{str(GlobalVariableOfTheControl.stop_live_button_enabled)}")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


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
    logSave(0, "╔═════════════════════════╗")
    logSave(0, "║　　已载入: bilibili_live  ║")
    logSave(0, "╚═════════════════════════╝")
    # 注册事件回调
    logSave(0, "╭───────────────╮")
    logSave(0, "│　开始监视obs事件 │")
    logSave(0, "╰───────────────╯")
    obs.obs_frontend_add_event_callback(on_event)
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
    logSave(0, "╔══════════════════════╗")
    logSave(0, "║　　　监测到控件数据变动   ║")
    logSave(0, "╚══════════════════════╝")
    pass


# --- 一个名为script_properties的函数定义了用户可以使用的属性
def script_properties():  # 建立控件
    """
    建立控件
    调用以定义与脚本关联的用户属性。这些属性用于定义如何向用户显示设置属性。
    通常用于自动生成用户界面小部件，也可以用来枚举特定设置的可用值或有效值。
    Returns:通过 obs_properties_create() 创建的 Obs_properties_t 对象
    obs_properties_t 类型的属性对象。这个属性对象通常用于枚举 libobs 对象的可用设置，
    """
    logSave(0, f"╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    logSave(0, f"║                          调用内置函数script_properties调整脚本控件                            ║")
    # 网络连通
    if not GlobalVariableOfData.networkConnectionStatus:
        return None
    # 创建一个 OBS 属性集对象，他将包含所有控件对应的属性对象
    GlobalVariableOfTheControl.props = obs.obs_properties_create()
    # 为 分组框【配置】 建立属性集
    GlobalVariableOfTheControl.setting_props = obs.obs_properties_create()
    # 为 分组框【直播间】 建立属性集
    GlobalVariableOfTheControl.liveRoom_props = obs.obs_properties_create()
    # 为 分组框【直播】 建立属性集
    GlobalVariableOfTheControl.live_props = obs.obs_properties_create()

    # —————————————————————————————————————————————————————————————————————————————————————————————————————
    # 添加 分组框【配置】
    GlobalVariableOfTheControl.setting_group = obs.obs_properties_add_group(GlobalVariableOfTheControl.props, 'setting_group', "【账号】", obs.OBS_GROUP_NORMAL, GlobalVariableOfTheControl.setting_props)

    # 添加 只读文本框【登录状态】
    GlobalVariableOfTheControl.login_status_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.setting_props, 'login_status_textBox', "登录状态：", obs.OBS_TEXT_INFO)
    # 添加 只读文本框【登录状态】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.login_status_textBox, lambda ps, p, st: test("只读文本框【登录状态】"))

    # 添加 组合框【用户】
    GlobalVariableOfTheControl.uid_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.setting_props, 'uid_comboBox', '用户：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    # 添加 组合框【用户】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.uid_comboBox, lambda ps, p, st: test("组合框【用户】"))

    # 添加 按钮【登录账号】
    GlobalVariableOfTheControl.login_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "login_button", "登录账号", button_function_login)

    # 添加 按钮【更新账号列表】
    GlobalVariableOfTheControl.update_account_list_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "update_account_list_button", "更新账号列表", button_function_update_account_list)

    # 添加 按钮【二维码添加账户】
    GlobalVariableOfTheControl.qr_add_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "qr_add_account_button", "二维码添加账户", button_function_qr_add_account)

    # 添加 按钮【显示登录二维码图片】
    GlobalVariableOfTheControl.display_qr_picture_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "display_qr_picture_button", "显示登录二维码图片", button_function_show_qr_picture)

    # 添加 按钮【删除账户】
    GlobalVariableOfTheControl.delete_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "delete_account_button", "删除账户", button_function_del_user)

    # 添加 按钮【备份账户】
    GlobalVariableOfTheControl.backup_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "backup_account_button", "备份账户", button_function_backup_users)

    # 添加 按钮【恢复账户】
    GlobalVariableOfTheControl.restore_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "restore_account_button", "恢复账户", button_function_restore_user)

    # 添加 按钮【登出账号】
    GlobalVariableOfTheControl.logout_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "logout_button", "登出账号", button_function_logout)

    # ————————————————————————————————————————————————————————————————
    # 添加 分组框【直播间】
    GlobalVariableOfTheControl.liveRoom_group = obs.obs_properties_add_group(GlobalVariableOfTheControl.props, 'liveRoom_group', '【直播间】', obs.OBS_GROUP_NORMAL, GlobalVariableOfTheControl.liveRoom_props)

    # 添加 只读文本框【直播间 状态】
    GlobalVariableOfTheControl.room_status_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.liveRoom_props, 'room_status_textBox', f'直播间 状态', obs.OBS_TEXT_INFO)
    # 添加 只读文本框【直播间 状态】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.room_status_textBox, lambda ps, p, st: test("只读文本框【直播间 状态】"))

    # 添加 按钮【查看直播间封面】
    GlobalVariableOfTheControl.viewLiveCover_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, 'viewLiveCover_button', f'查看直播间封面', button_function_check_room_cover)

    # 添加 文件对话框【直播间封面】
    GlobalVariableOfTheControl.room_cover_fileDialogBox = obs.obs_properties_add_path(GlobalVariableOfTheControl.liveRoom_props, 'room_cover_fileDialogBox', f'直播间封面', obs.OBS_PATH_FILE, '*jpg *jpeg *.png', None)
    # 添加 文件对话框【直播间封面】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.room_cover_fileDialogBox, lambda ps, p, st: test("文件对话框【直播间封面】"))

    # 添加 按钮【上传直播间封面】
    GlobalVariableOfTheControl.room_cover_update_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "room_cover_update_button", "上传直播间封面", button_function_update_room_cover)

    # 添加 普通文本框【直播间标题】
    GlobalVariableOfTheControl.liveRoom_title_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.liveRoom_props, "liveRoom_title_textBox", "直播间标题", obs.OBS_TEXT_DEFAULT)
    # 添加 普通文本框【直播间标题】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.liveRoom_title_textBox, lambda ps, p, st: test("普通文本框【直播间标题】"))

    # 添加 按钮【更改直播间标题】
    GlobalVariableOfTheControl.change_liveRoom_title_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "change_liveRoom_title_button", "更改直播间标题", button_function_change_live_room_title)

    # 添加 普通文本框【直播间公告】
    GlobalVariableOfTheControl.liveRoom_news_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.liveRoom_props, "liveRoom_news_textBox", "直播间公告", obs.OBS_TEXT_DEFAULT)
    # 添加 普通文本框【直播间公告】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.liveRoom_news_textBox, lambda ps, p, st: test("普通文本框【直播间公告】"))

    # 添加 按钮【更改直播间公告】
    GlobalVariableOfTheControl.change_liveRoom_news_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "change_liveRoom_news_button", "更改直播间公告", button_function_change_live_room_news)

    # 添加 组合框【一级分区】
    GlobalVariableOfTheControl.parentLiveArea_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.liveRoom_props, 'parentLiveArea_comboBox', '一级分区：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    # 添加 组合框【一级分区】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.parentLiveArea_comboBox, lambda ps, p, st: test("组合框【一级分区】"))

    # 添加 按钮【确认一级分区】
    GlobalVariableOfTheControl.parentLiveArea_true_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "parentLiveArea_true_button", "确认一级分区", button_function_start_area1)

    # 添加 组合框【二级分区】
    GlobalVariableOfTheControl.subLiveArea_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.liveRoom_props, 'subLiveArea_comboBox', '二级分区：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    # 添加 组合框【二级分区】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.subLiveArea_comboBox, lambda ps, p, st: test("组合框【二级分区】"))

    # 添加 按钮【「确认分区」】
    GlobalVariableOfTheControl.subLiveArea_true_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "subLiveArea_true_button", "「确认分区」", lambda ps, p: button_function_start_area())

    # 添加 url按钮【跳转直播间后台网页】
    GlobalVariableOfTheControl.jump_blive_web_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, 'jump_blive_web_button', f'跳转直播间后台网页', button_function_jump_blive_web)
    # 设置 url按钮【跳转直播间后台网页】 类型
    obs.obs_property_button_set_type(GlobalVariableOfTheControl.jump_blive_web_button, obs.OBS_BUTTON_URL)

    # ————————————————————————————————————————————————————————————————
    # 添加 分组框【直播】
    GlobalVariableOfTheControl.live_group = obs.obs_properties_add_group(GlobalVariableOfTheControl.props, 'live_group', '【直播】', obs.OBS_GROUP_NORMAL, GlobalVariableOfTheControl.live_props)

    # 添加 组合框【直播平台】
    GlobalVariableOfTheControl.live_streaming_platform_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.live_props, 'live_streaming_platform_comboBox', '直播平台：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    # 添加 组合框【直播平台】变动后事件
    obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.live_streaming_platform_comboBox, lambda ps, p, st: test("按钮【开始直播并复制推流码】"))

    # 添加 按钮【开始直播并复制推流码】
    GlobalVariableOfTheControl.start_live_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "start_live_button", "开始直播并复制推流码", button_function_start_live)

    # 添加 按钮【复制直播服务器】
    GlobalVariableOfTheControl.rtmp_address_copy_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "rtmp_address_copy_button", "复制直播服务器", button_function_rtmp_address_copy)

    # 添加 按钮【复制直播推流码】
    GlobalVariableOfTheControl.rtmp_stream_code_copy_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "rtmp_stream_code_copy_button", "复制直播推流码", button_function_rtmp_stream_code_copy)

    # 添加 按钮【更新推流码并复制】
    GlobalVariableOfTheControl.rtmp_stream_code_update_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "rtmp_stream_code_update_button", "更新推流码并复制", button_function_rtmp_stream_code_update)

    # 添加 按钮【结束直播】
    GlobalVariableOfTheControl.stop_live_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "stop_live_button", "结束直播", button_function_stop_live)

    # ————————————————————————————————————————————————————————————————————————————————
    # 更新UI界面数据#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
    GlobalVariableOfTheControl.isScript_propertiesNum += 1
    if GlobalVariableOfTheControl.isScript_propertiesNum <= 1:
        logSave(0, f"╒══════════════════创建初始控件════════════════╕")
        logSave(0, f"│                  创建初始控件                │")
        update_ui_interface_data(is_script_properties=True)
        logSave(0, f"│                  创建初始控件                │")
        logSave(0, f"╘══════════════════创建初始控件════════════════╛")
    else:
        logSave(0, f"╒══════════════════载入控件UI数据════════════════╕")
        logSave(0, f"│                  载入控件UI数据                │")
        update_ui_interface_data(is_script_properties=True)
        logSave(0, f"│                  载入控件UI数据                │")
        logSave(0, f"╘══════════════════载入控件UI数据════════════════╛")
    logSave(0, f"║                          调用内置函数script_properties调整脚本控件                          ║")
    logSave(0, f"╚══════════════════════════调用内置函数script_properties调整脚本控件══════════════════════════╝")
    return GlobalVariableOfTheControl.props


def update_ui_interface_data(is_script_properties=False):
    """
    更新UI界面数据
    Returns:
    """
    if is_script_properties:
        logSave(0, f"╱─────────────────────────────────────────────────────────╲")
        logSave(0, f"│由于[Script_properties]而被调用[updateTheUIInterfaceData]   │")

    # 只读文本框【登录状态】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│只读文本框【登录状态】 UI")
    # 设置 只读文本框【登录状态】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.login_status_textBox) != GlobalVariableOfTheControl.login_status_textBox_visible:
        logSave(0, f"│只读文本框【登录状态】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.login_status_textBox)}➡️{GlobalVariableOfTheControl.login_status_textBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.login_status_textBox_visible)
    # 设置 只读文本框【登录状态】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.login_status_textBox) != GlobalVariableOfTheControl.login_status_textBox_enabled:
        logSave(0, f"│只读文本框【登录状态】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.login_status_textBox)}➡️{GlobalVariableOfTheControl.login_status_textBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.login_status_textBox_enabled)
    # 设置 只读文本框【登录状态】 信息类型
    if obs.obs_property_text_info_type(GlobalVariableOfTheControl.login_status_textBox) != GlobalVariableOfTheControl.login_status_textBox_type:
        logSave(0, f"│只读文本框【登录状态】 信息类型 发生变动: {textBox_type_name4textBox_type[obs.obs_property_text_info_type(GlobalVariableOfTheControl.login_status_textBox)]}➡️{textBox_type_name4textBox_type[GlobalVariableOfTheControl.login_status_textBox_type]}")
        obs.obs_property_text_set_info_type(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.login_status_textBox_type)
    # 设置 只读文本框【登录状态】 文本
    if obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'login_status_textBox') != GlobalVariableOfTheControl.login_status_textBox_string:
        logSave(0, f"│只读文本框【登录状态】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'login_status_textBox')}➡️{GlobalVariableOfTheControl.login_status_textBox_string}")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'login_status_textBox', f'{GlobalVariableOfTheControl.login_status_textBox_string}')
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 组合框【用户】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│组合框【用户】 UI")
    # 设置 组合框【用户】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.uid_comboBox) != GlobalVariableOfTheControl.uid_comboBox_visible:
        logSave(0, f"│组合框【用户】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.uid_comboBox)}➡️{GlobalVariableOfTheControl.uid_comboBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.uid_comboBox_visible)
    # 设置 组合框【用户】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.uid_comboBox) != GlobalVariableOfTheControl.uid_comboBox_enabled:
        logSave(0, f"│组合框【用户】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.uid_comboBox)}➡️{GlobalVariableOfTheControl.uid_comboBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.uid_comboBox_enabled)
    # 判断 组合框【用户】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.uid_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))}:
        logSave(0, f"│组合框【用户】数据发生变动：{len({obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))})}个元素➡️{len(GlobalVariableOfTheControl.uid_comboBox_dict)}个元素")
        # 清空 组合框【用户】
        logSave(0, f"│更新 组合框【用户】数据 第一步：清空 组合框【用户】")
        obs.obs_property_list_clear(GlobalVariableOfTheControl.uid_comboBox)
        # 添加 组合框【用户】 列表选项  默认值会被设置在第一位
        logSave(0, f"│更新 组合框【用户】数据 第二步：添加 组合框【用户】 列表选项  如果有默认值，会被设置在第一位")
        for uid in GlobalVariableOfTheControl.uid_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.uid_comboBox_dict[uid], uid) if uid != GlobalVariableOfTheControl.uid_comboBox_value else obs.obs_property_list_insert_string(GlobalVariableOfTheControl.uid_comboBox, 0, GlobalVariableOfTheControl.uid_comboBox_string, GlobalVariableOfTheControl.uid_comboBox_value)
        # 设置 组合框【用户】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        logSave(0, f"│更新 组合框【用户】数据 第三步：更新 组合框【用户】 文本")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'uid_comboBox', obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, 0))
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【登录账号】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【登录账号】 UI")
    # 设置 按钮【登录账号】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.login_button) != GlobalVariableOfTheControl.login_button_visible:
        logSave(0, f"│按钮【登录账号】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.login_button)}➡️{GlobalVariableOfTheControl.login_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.login_button_visible)
    # 设置 按钮【登录账号】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.login_button) != GlobalVariableOfTheControl.login_button_enabled:
        logSave(0, f"│按钮【登录账号】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.login_button)}➡️{GlobalVariableOfTheControl.login_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.login_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【二维码添加账户】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【二维码添加账户】 UI")
    # 设置 按钮【二维码添加账户】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.qr_add_account_button) != GlobalVariableOfTheControl.qr_add_account_button_visible:
        logSave(0, f"│按钮【二维码添加账户】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.qr_add_account_button)}➡️{GlobalVariableOfTheControl.qr_add_account_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.qr_add_account_button, GlobalVariableOfTheControl.qr_add_account_button_visible)
    # 设置 按钮【二维码添加账户】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.qr_add_account_button) != GlobalVariableOfTheControl.qr_add_account_button_enabled:
        logSave(0, f"│按钮【二维码添加账户】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.qr_add_account_button)}➡️{GlobalVariableOfTheControl.qr_add_account_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.qr_add_account_button, GlobalVariableOfTheControl.qr_add_account_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【显示二维码图片】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【显示二维码图片】 UI")
    # 设置 按钮【显示二维码图片】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.display_qr_picture_button) != GlobalVariableOfTheControl.display_qr_picture_button_visible:
        logSave(0, f"│按钮【显示二维码图片】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.display_qr_picture_button)}➡️{GlobalVariableOfTheControl.display_qr_picture_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.display_qr_picture_button, GlobalVariableOfTheControl.display_qr_picture_button_visible)
    # 设置 按钮【显示二维码图片】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.display_qr_picture_button) != GlobalVariableOfTheControl.display_qr_picture_button_enabled:
        logSave(0, f"│按钮【显示二维码图片】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.display_qr_picture_button)}➡️{GlobalVariableOfTheControl.display_qr_picture_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.display_qr_picture_button, GlobalVariableOfTheControl.display_qr_picture_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【删除账户】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【删除账户】 UI")
    # 设置 按钮【删除账户】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.delete_account_button) != GlobalVariableOfTheControl.delete_account_button_visible:
        logSave(0, f"│按钮【删除账户】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.delete_account_button)}➡️{GlobalVariableOfTheControl.delete_account_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.delete_account_button_visible)
    # 设置 按钮【删除账户】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.delete_account_button) != GlobalVariableOfTheControl.delete_account_button_enabled:
        logSave(0, f"│按钮【删除账户】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.delete_account_button)}➡️{GlobalVariableOfTheControl.delete_account_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.delete_account_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【备份账户】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【备份账户】 UI")
    # 设置 按钮【备份账户】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.backup_account_button) != GlobalVariableOfTheControl.backup_account_button_visible:
        logSave(0, f"│按钮【备份账户】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.backup_account_button)}➡️{GlobalVariableOfTheControl.backup_account_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.backup_account_button_visible)
    # 设置 按钮【备份账户】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.backup_account_button) != GlobalVariableOfTheControl.backup_account_button_enabled:
        logSave(0, f"│按钮【备份账户】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.backup_account_button)}➡️{GlobalVariableOfTheControl.backup_account_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.backup_account_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【恢复账户】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【恢复账户】 UI")
    # 设置 按钮【恢复账户】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.restore_account_button) != GlobalVariableOfTheControl.restore_account_button_visible:
        logSave(0, f"│按钮【恢复账户】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.restore_account_button)}➡️{GlobalVariableOfTheControl.restore_account_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.restore_account_button_visible)
    # 设置 按钮【恢复账户】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.restore_account_button) != GlobalVariableOfTheControl.restore_account_button_enabled:
        logSave(0, f"│按钮【恢复账户】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.restore_account_button)}➡️{GlobalVariableOfTheControl.restore_account_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.restore_account_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【登出账号】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【登出账号】 UI")
    # 设置 按钮【登出账号】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.logout_button) != GlobalVariableOfTheControl.logout_button_visible:
        logSave(0, f"│按钮【登出账号】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.logout_button)}➡️{GlobalVariableOfTheControl.logout_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.logout_button_visible)
    # 设置 按钮【登出账号】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.logout_button) != GlobalVariableOfTheControl.logout_button_enabled:
        logSave(0, f"│按钮【登出账号】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.logout_button)}➡️{GlobalVariableOfTheControl.logout_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.logout_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # ————————————————————————————————————————————————————————————————
    # 只读文本框【直播间 状态】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│只读文本框【直播间 状态】 UI")
    # 设置 只读文本框【直播间 状态】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.room_status_textBox) != GlobalVariableOfTheControl.room_status_textBox_visible:
        logSave(0, f"│只读文本框【直播间 状态】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.room_status_textBox)}➡️{GlobalVariableOfTheControl.room_status_textBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.room_status_textBox, GlobalVariableOfTheControl.room_status_textBox_visible)
    # 设置 只读文本框【直播间 状态】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.room_status_textBox) != GlobalVariableOfTheControl.room_status_textBox_enabled:
        logSave(0, f"│只读文本框【直播间 状态】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.room_status_textBox)}➡️{GlobalVariableOfTheControl.room_status_textBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.room_status_textBox, GlobalVariableOfTheControl.room_status_textBox_enabled)
    # 设置 只读文本框【直播间 状态】 信息类型
    if obs.obs_property_text_info_type(GlobalVariableOfTheControl.room_status_textBox) != GlobalVariableOfTheControl.room_status_textBox_type:
        logSave(0, f"│只读文本框【直播间 状态】 信息类型 发生变动: {textBox_type_name4textBox_type[obs.obs_property_text_info_type(GlobalVariableOfTheControl.room_status_textBox)]}➡️{textBox_type_name4textBox_type[GlobalVariableOfTheControl.room_status_textBox_type]}")
        obs.obs_property_text_set_info_type(GlobalVariableOfTheControl.room_status_textBox, GlobalVariableOfTheControl.room_status_textBox_type)
    # 设置 只读文本框【直播间 状态】 文本
    if obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'room_status_textBox') != GlobalVariableOfTheControl.room_status_textBox_string:
        logSave(0, f"│只读文本框【直播间 状态】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'room_status_textBox')}➡️{GlobalVariableOfTheControl.room_status_textBox_string}")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, "room_status_textBox", GlobalVariableOfTheControl.room_status_textBox_string)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【查看直播间封面】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【查看直播间封面】 UI")
    # 设置 按钮【查看直播间封面】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.viewLiveCover_button) != GlobalVariableOfTheControl.viewLiveCover_button_visible:
        logSave(0, f"│按钮【查看直播间封面】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.viewLiveCover_button)}➡️{GlobalVariableOfTheControl.viewLiveCover_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.viewLiveCover_button, GlobalVariableOfTheControl.viewLiveCover_button_visible)
    # 设置 按钮【查看直播间封面】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.viewLiveCover_button) != GlobalVariableOfTheControl.viewLiveCover_button_enabled:
        logSave(0, f"│按钮【查看直播间封面】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.viewLiveCover_button)}➡️{GlobalVariableOfTheControl.viewLiveCover_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.viewLiveCover_button, GlobalVariableOfTheControl.viewLiveCover_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 文件对话框【直播间封面】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│文件对话框【直播间封面】 UI")
    # 设置 文件对话框【直播间封面】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.room_cover_fileDialogBox) != GlobalVariableOfTheControl.room_cover_fileDialogBox_visible:
        logSave(0, f"│文件对话框【直播间封面】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.room_cover_fileDialogBox)}➡️{GlobalVariableOfTheControl.room_cover_fileDialogBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.room_cover_fileDialogBox, GlobalVariableOfTheControl.room_cover_fileDialogBox_visible)
    # 设置 文件对话框【直播间封面】 文件路径
    if obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'room_cover_fileDialogBox') != GlobalVariableOfTheControl.room_cover_fileDialogBox_string:
        logSave(0, f"│文件对话框【直播间封面】 文件路径 发生变动: {obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'room_cover_fileDialogBox')}➡️{GlobalVariableOfTheControl.room_cover_fileDialogBox_string}")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, "room_cover_fileDialogBox", GlobalVariableOfTheControl.room_cover_fileDialogBox_string)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【上传直播间封面】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【上传直播间封面】 UI")
    # 设置 按钮【上传直播间封面】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.room_cover_update_button) != GlobalVariableOfTheControl.room_cover_update_button_visible:
        logSave(0, f"│按钮【上传直播间封面】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.room_cover_update_button)}➡️{GlobalVariableOfTheControl.room_cover_update_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.room_cover_update_button, GlobalVariableOfTheControl.room_cover_update_button_visible)
    # 设置 按钮【上传直播间封面】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.room_cover_update_button) != GlobalVariableOfTheControl.room_cover_update_button_enabled:
        logSave(0, f"│按钮【上传直播间封面】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.room_cover_update_button)}➡️{GlobalVariableOfTheControl.room_cover_update_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.room_cover_update_button, GlobalVariableOfTheControl.room_cover_update_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 普通文本框【直播间标题】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│普通文本框【直播间标题】 UI")
    # 设置 普通文本框【直播间标题】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.liveRoom_title_textBox) != GlobalVariableOfTheControl.liveRoom_title_textBox_visible:
        logSave(0, f"│普通文本框【直播间标题】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.liveRoom_title_textBox)}➡️{GlobalVariableOfTheControl.liveRoom_title_textBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.liveRoom_title_textBox, GlobalVariableOfTheControl.liveRoom_title_textBox_visible)
    # 设置 普通文本框【直播间标题】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.liveRoom_title_textBox) != GlobalVariableOfTheControl.liveRoom_title_textBox_enabled:
        logSave(0, f"│普通文本框【直播间标题】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.liveRoom_title_textBox)}➡️{GlobalVariableOfTheControl.liveRoom_title_textBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.liveRoom_title_textBox, GlobalVariableOfTheControl.liveRoom_title_textBox_enabled)
    # 设置 普通文本框【直播间标题】 文本
    if obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'liveRoom_title_textBox') != GlobalVariableOfTheControl.liveRoom_title_textBox_string:
        logSave(0, f"│普通文本框【直播间标题】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'liveRoom_title_textBox')}➡️{GlobalVariableOfTheControl.liveRoom_title_textBox_string}")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, "liveRoom_title_textBox", GlobalVariableOfTheControl.liveRoom_title_textBox_string)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【更改直播间标题】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【更改直播间标题】 UI")
    # 设置 按钮【更改直播间标题】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.change_liveRoom_title_button) != GlobalVariableOfTheControl.change_liveRoom_title_button_visible:
        logSave(0, f"│按钮【更改直播间标题】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.change_liveRoom_title_button)}➡️{GlobalVariableOfTheControl.change_liveRoom_title_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.change_liveRoom_title_button, GlobalVariableOfTheControl.change_liveRoom_title_button_visible)
    # 设置 按钮【更改直播间标题】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.change_liveRoom_title_button) != GlobalVariableOfTheControl.change_liveRoom_title_button_enabled:
        logSave(0, f"│按钮【更改直播间标题】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.change_liveRoom_title_button)}➡️{GlobalVariableOfTheControl.change_liveRoom_title_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.change_liveRoom_title_button, GlobalVariableOfTheControl.change_liveRoom_title_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 普通文本框【直播间公告】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│普通文本框【直播间公告】 UI")
    # 设置 普通文本框【直播间公告】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.liveRoom_news_textBox) != GlobalVariableOfTheControl.liveRoom_news_textBox_visible:
        logSave(0, f"│普通文本框【直播间公告】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.liveRoom_news_textBox)}➡️{GlobalVariableOfTheControl.liveRoom_news_textBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.liveRoom_news_textBox, GlobalVariableOfTheControl.liveRoom_news_textBox_visible)
    # 设置 普通文本框【直播间公告】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.liveRoom_news_textBox) != GlobalVariableOfTheControl.liveRoom_news_textBox_enabled:
        logSave(0, f"│普通文本框【直播间公告】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.liveRoom_news_textBox)}➡️{GlobalVariableOfTheControl.liveRoom_news_textBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.liveRoom_news_textBox, GlobalVariableOfTheControl.liveRoom_news_textBox_enabled)
    # 设置 普通文本框【直播间公告】 文本
    if obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'liveRoom_news_textBox') != GlobalVariableOfTheControl.liveRoom_news_textBox_string:
        logSave(0, f"│普通文本框【直播间公告】 文本 发生变动: {obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'liveRoom_news_textBox')}➡️{GlobalVariableOfTheControl.liveRoom_news_textBox_string}")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, "liveRoom_news_textBox", GlobalVariableOfTheControl.liveRoom_news_textBox_string)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【更改直播间公告】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【更改直播间公告】 UI")
    # 设置 按钮【更改直播间公告】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.change_liveRoom_news_button) != GlobalVariableOfTheControl.change_liveRoom_news_button_visible:
        logSave(0, f"│按钮【更改直播间公告】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.change_liveRoom_news_button)}➡️{GlobalVariableOfTheControl.change_liveRoom_news_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.change_liveRoom_news_button, GlobalVariableOfTheControl.change_liveRoom_news_button_visible)
    # 设置 按钮【更改直播间公告】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.change_liveRoom_news_button) != GlobalVariableOfTheControl.change_liveRoom_news_button_enabled:
        logSave(0, f"│按钮【更改直播间公告】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.change_liveRoom_news_button)}➡️{GlobalVariableOfTheControl.change_liveRoom_news_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.change_liveRoom_news_button, GlobalVariableOfTheControl.change_liveRoom_news_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 组合框【一级分区】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│组合框【一级分区】 UI")
    # 设置 组合框【一级分区】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.parentLiveArea_comboBox) != GlobalVariableOfTheControl.parentLiveArea_comboBox_visible:
        logSave(0, f"│组合框【一级分区】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.parentLiveArea_comboBox)}➡️{GlobalVariableOfTheControl.parentLiveArea_comboBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.parentLiveArea_comboBox, GlobalVariableOfTheControl.parentLiveArea_comboBox_visible)
    # 设置 组合框【一级分区】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.parentLiveArea_comboBox) != GlobalVariableOfTheControl.parentLiveArea_comboBox_enabled:
        logSave(0, f"│组合框【一级分区】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.parentLiveArea_comboBox)}➡️{GlobalVariableOfTheControl.parentLiveArea_comboBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.parentLiveArea_comboBox, GlobalVariableOfTheControl.parentLiveArea_comboBox_enabled)
    # 判断 组合框【一级分区】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.parentLiveArea_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.parentLiveArea_comboBox))}:
        logSave(0, f"│组合框【一级分区】数据发生变动：{len({obs.obs_property_list_item_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.parentLiveArea_comboBox))})}个元素➡️{len(GlobalVariableOfTheControl.parentLiveArea_comboBox_dict)}个元素")
        # 清空 组合框【一级分区】
        logSave(0, f"│更新 组合框【一级分区】数据 第一步：清空 组合框【一级分区】")
        obs.obs_property_list_clear(GlobalVariableOfTheControl.parentLiveArea_comboBox)
        # 添加 组合框【一级分区】 列表选项  默认值会被设置在第一位
        logSave(0, f"│更新 组合框【一级分区】数据 第二步：添加 组合框【一级分区】 列表选项  如果有默认值，会被设置在第一位")
        for parentLiveAreaId in GlobalVariableOfTheControl.parentLiveArea_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, GlobalVariableOfTheControl.parentLiveArea_comboBox_dict[parentLiveAreaId], parentLiveAreaId) if parentLiveAreaId != GlobalVariableOfTheControl.parentLiveArea_comboBox_value else obs.obs_property_list_insert_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, 0, GlobalVariableOfTheControl.parentLiveArea_comboBox_string, GlobalVariableOfTheControl.parentLiveArea_comboBox_value)
        # 设置 组合框【一级分区】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        logSave(0, f"│更新 组合框【一级分区】数据 第三步：更新 组合框【一级分区】 文本")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'parentLiveArea_comboBox', obs.obs_property_list_item_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, 0))
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【确认一级分区】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【确认一级分区】 UI")
    # 设置 按钮【确认一级分区】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.parentLiveArea_true_button) != GlobalVariableOfTheControl.parentLiveArea_true_button_visible:
        logSave(0, f"│按钮【确认一级分区】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.parentLiveArea_true_button)}➡️{GlobalVariableOfTheControl.parentLiveArea_true_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.parentLiveArea_true_button, GlobalVariableOfTheControl.parentLiveArea_true_button_visible)
    # 设置 按钮【确认一级分区】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.parentLiveArea_true_button) != GlobalVariableOfTheControl.parentLiveArea_true_button_enabled:
        logSave(0, f"│按钮【确认一级分区】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.parentLiveArea_true_button)}➡️{GlobalVariableOfTheControl.parentLiveArea_true_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.parentLiveArea_true_button, GlobalVariableOfTheControl.parentLiveArea_true_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 组合框【二级分区】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│组合框【二级分区】 UI")
    # 设置 组合框【二级分区】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.subLiveArea_comboBox) != GlobalVariableOfTheControl.subLiveArea_comboBox_visible:
        logSave(0, f"│组合框【二级分区】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.subLiveArea_comboBox)}➡️{GlobalVariableOfTheControl.subLiveArea_comboBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_visible)
    # 设置 组合框【二级分区】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.subLiveArea_comboBox) != GlobalVariableOfTheControl.subLiveArea_comboBox_enabled:
        logSave(0, f"│组合框【二级分区】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.subLiveArea_comboBox)}➡️{GlobalVariableOfTheControl.subLiveArea_comboBox_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_enabled)
    # 判断 组合框【二级分区】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.subLiveArea_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))}:
        logSave(0, f"│组合框【二级分区】数据发生变动：{len({obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))})}个元素➡️{len(GlobalVariableOfTheControl.subLiveArea_comboBox_dict)}个元素")
        # 清空 组合框【二级分区】
        logSave(0, f"│更新 组合框【二级分区】数据 第一步：清空 组合框【二级分区】")
        obs.obs_property_list_clear(GlobalVariableOfTheControl.subLiveArea_comboBox)
        # 添加 组合框【二级分区】 列表选项  默认值会被设置在第一位
        logSave(0, f"│更新 组合框【二级分区】数据 第二步：添加 组合框【二级分区】 列表选项  如果有默认值，会被设置在第一位")
        for subLiveAreaId in GlobalVariableOfTheControl.subLiveArea_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_dict[subLiveAreaId], subLiveAreaId) if subLiveAreaId != GlobalVariableOfTheControl.subLiveArea_comboBox_value else obs.obs_property_list_insert_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0, GlobalVariableOfTheControl.subLiveArea_comboBox_string, GlobalVariableOfTheControl.subLiveArea_comboBox_value)
        # 设置 组合框【二级分区】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        logSave(0, f"│更新 组合框【二级分区】数据 第三步：更新 组合框【二级分区】 文本")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'subLiveArea_comboBox', obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0))
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【「确认分区」】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【「确认分区」】 UI")
    # 设置 按钮【「确认分区」】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.subLiveArea_true_button) != GlobalVariableOfTheControl.subLiveArea_true_button_visible:
        logSave(0, f"│按钮【「确认分区」】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.subLiveArea_true_button)}➡️{GlobalVariableOfTheControl.subLiveArea_true_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.subLiveArea_true_button, GlobalVariableOfTheControl.subLiveArea_true_button_visible)
    # 设置 按钮【「确认分区」】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.subLiveArea_true_button) != GlobalVariableOfTheControl.subLiveArea_true_button_enabled:
        logSave(0, f"│按钮【「确认分区」】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.subLiveArea_true_button)}➡️{GlobalVariableOfTheControl.subLiveArea_true_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.subLiveArea_true_button, GlobalVariableOfTheControl.subLiveArea_true_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # url按钮【跳转直播间后台网页】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│url按钮【跳转直播间后台网页】 UI")
    # 设置 url按钮【跳转直播间后台网页】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.jump_blive_web_button) != GlobalVariableOfTheControl.jump_blive_web_button_visible:
        logSave(0, f"│url按钮【跳转直播间后台网页】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.jump_blive_web_button)}➡️{GlobalVariableOfTheControl.jump_blive_web_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.jump_blive_web_button, GlobalVariableOfTheControl.jump_blive_web_button_visible)
    # 设置 url按钮【跳转直播间后台网页】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.jump_blive_web_button) != GlobalVariableOfTheControl.jump_blive_web_button_enabled:
        logSave(0, f"│url按钮【跳转直播间后台网页】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.jump_blive_web_button)}➡️{GlobalVariableOfTheControl.jump_blive_web_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.jump_blive_web_button, GlobalVariableOfTheControl.jump_blive_web_button_enabled)
    # 设置 url按钮【跳转直播间后台网页】 链接
    if obs.obs_property_button_url(GlobalVariableOfTheControl.jump_blive_web_button) != GlobalVariableOfTheControl.jump_blive_web_button_url:
        logSave(0, f"│url按钮【跳转直播间后台网页】 链接 发生变动: {obs.obs_property_button_url(GlobalVariableOfTheControl.jump_blive_web_button)}➡️{GlobalVariableOfTheControl.jump_blive_web_button_url}")
        obs.obs_property_button_set_url(GlobalVariableOfTheControl.jump_blive_web_button, GlobalVariableOfTheControl.jump_blive_web_button_url)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # ————————————————————————————————————————————————————————————————
    # 组合框【直播平台】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│组合框【直播平台】 UI")
    # 设置 组合框【直播平台】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.live_streaming_platform_comboBox) != GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible:
        logSave(0, f"│组合框【直播平台】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.live_streaming_platform_comboBox)}➡️{GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible)
    # 设置 组合框【直播平台】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.live_streaming_platform_comboBox) != GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled:
        logSave(0, f"│组合框【直播平台】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.live_streaming_platform_comboBox)}➡️{GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled)
    # 判断 组合框【直播平台】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.live_streaming_platform_comboBox))}:
        logSave(0, f"│组合框【直播平台】数据发生变动：{len({obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.live_streaming_platform_comboBox))})}个元素➡️{len(GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict)}个元素")
        # 清空 组合框【直播平台】
        logSave(0, f"│更新 组合框【直播平台】数据 第一步：清空 组合框【直播平台】")
        obs.obs_property_list_clear(GlobalVariableOfTheControl.live_streaming_platform_comboBox)
        # 添加 组合框【直播平台】 列表选项  默认值会被设置在第一位
        logSave(0, f"│更新 组合框【直播平台】数据 第二步：添加 组合框【直播平台】 列表选项  如果有默认值，会被设置在第一位")
        for LivePlatforms in GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict[LivePlatforms], LivePlatforms) if LivePlatforms != GlobalVariableOfTheControl.live_streaming_platform_comboBox_value else obs.obs_property_list_insert_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, 0, GlobalVariableOfTheControl.live_streaming_platform_comboBox_string, GlobalVariableOfTheControl.live_streaming_platform_comboBox_value)
        # 设置 组合框【直播平台】 文本 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        logSave(0, f"│更新 组合框【直播平台】数据 第三步：更新 组合框【直播平台】 文本")
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'live_streaming_platform_comboBox', obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, 0))
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【开始直播并复制推流码】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【开始直播并复制推流码】 UI")
    # 设置 按钮【开始直播并复制推流码】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.start_live_button) != GlobalVariableOfTheControl.start_live_button_visible:
        logSave(0, f"│按钮【开始直播并复制推流码】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.start_live_button)}➡️{GlobalVariableOfTheControl.start_live_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.start_live_button, GlobalVariableOfTheControl.start_live_button_visible)
    # 设置 按钮【开始直播并复制推流码】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.start_live_button) != GlobalVariableOfTheControl.start_live_button_enabled:
        logSave(0, f"│按钮【开始直播并复制推流码】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.start_live_button)}➡️{GlobalVariableOfTheControl.start_live_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.start_live_button, GlobalVariableOfTheControl.start_live_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【复制直播服务器】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【复制直播服务器】 UI")
    # 设置 按钮【复制直播服务器】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.rtmp_address_copy_button) != GlobalVariableOfTheControl.rtmp_address_copy_button_visible:
        logSave(0, f"│按钮【复制直播服务器】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.rtmp_address_copy_button)}➡️{GlobalVariableOfTheControl.rtmp_address_copy_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_address_copy_button, GlobalVariableOfTheControl.rtmp_address_copy_button_visible)
    # 设置 按钮【复制直播服务器】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.rtmp_address_copy_button) != GlobalVariableOfTheControl.rtmp_address_copy_button_enabled:
        logSave(0, f"│按钮【复制直播服务器】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.rtmp_address_copy_button)}➡️{GlobalVariableOfTheControl.rtmp_address_copy_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.rtmp_address_copy_button, GlobalVariableOfTheControl.rtmp_address_copy_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【复制直播推流码】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【复制直播推流码】 UI")
    # 设置 按钮【复制直播推流码】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.rtmp_stream_code_copy_button) != GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible:
        logSave(0, f"│按钮【复制直播推流码】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.rtmp_stream_code_copy_button)}➡️{GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_stream_code_copy_button, GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible)
    # 设置 按钮【复制直播推流码】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.rtmp_stream_code_copy_button) != GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled:
        logSave(0, f"│按钮【复制直播推流码】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.rtmp_stream_code_copy_button)}➡️{GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.rtmp_stream_code_copy_button, GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【更新推流码并复制】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【更新推流码并复制】 UI")
    # 设置 按钮【更新推流码并复制】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.rtmp_stream_code_update_button) != GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible:
        logSave(0, f"│按钮【更新推流码并复制】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.rtmp_stream_code_update_button)}➡️{GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_stream_code_update_button, GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible)
    # 设置 按钮【更新推流码并复制】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.rtmp_stream_code_update_button) != GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled:
        logSave(0, f"│按钮【更新推流码并复制】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.rtmp_stream_code_update_button)}➡️{GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.rtmp_stream_code_update_button, GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled)
    logSave(0, f"└─────────────────────────────────────────────────────────")

    # 按钮【结束直播】 UI
    logSave(0, f"┌─────────────────────────────────────────────────────────")
    logSave(0, f"│按钮【结束直播】 UI")
    # 设置 按钮【结束直播】 可见状态
    if obs.obs_property_visible(GlobalVariableOfTheControl.stop_live_button) != GlobalVariableOfTheControl.stop_live_button_visible:
        logSave(0, f"│按钮【结束直播】 可见状态 发生变动: {obs.obs_property_visible(GlobalVariableOfTheControl.stop_live_button)}➡️{GlobalVariableOfTheControl.stop_live_button_visible}")
        obs.obs_property_set_visible(GlobalVariableOfTheControl.stop_live_button, GlobalVariableOfTheControl.stop_live_button_visible)
    # 设置 按钮【结束直播】 可用状态
    if obs.obs_property_enabled(GlobalVariableOfTheControl.stop_live_button) != GlobalVariableOfTheControl.stop_live_button_enabled:
        logSave(0, f"│按钮【结束直播】 可用状态 发生变动: {obs.obs_property_enabled(GlobalVariableOfTheControl.stop_live_button)}➡️{GlobalVariableOfTheControl.stop_live_button_enabled}")
        obs.obs_property_set_enabled(GlobalVariableOfTheControl.stop_live_button, GlobalVariableOfTheControl.stop_live_button_enabled)
    logSave(0, f"└──────────────────────────────────────────────────────────────")

    logSave(0, f"│由于[Script_properties]而被调用[updateTheUIInterfaceData]   │")
    logSave(0, f"╲─────────────────────────────────────────────────────────╱")


def button_function_login(props, prop, settings=GlobalVariableOfTheControl.script_settings):
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
    uid = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'uid_comboBox')
    logSave(0, f"即将登录的账号：{uid}")
    if uid not in ["-1"]:
        logSave(0, f"将选定的账号：{uid}，在配置文件中转移到默认账号的位置")
        login_try(GlobalVariableOfData.scripts_config_filepath, int(uid))
    else:
        logSave(2, "请添加或选择一个账号登录")
        return None
    # ＝＝＝＝＝＝＝＝＝＝＝
    # ＝     更新      ＝
    # ＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.script_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    update_ui_interface_data()
    return True


def button_function_update_account_list(props=None, prop=None, settings=GlobalVariableOfTheControl.script_settings):
    """
    更新账号列表
    Args:
        props:
        prop:

    Returns:
    """
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
    userInterface_navByUid4Dict = {uid: BilibiliApiMaster(dict2cookie(b_u_l_c.get_cookies(int(uid)))).interface_nav() for uid in [x for x in b_u_l_c.get_users().values() if x]}
    # 获取 用户配置文件 中 每一个 用户 的 昵称
    AllUnameByUid4Dict = {uid: userInterface_navByUid4Dict[uid]["uname"] for uid in userInterface_navByUid4Dict}
    logSave(0, f"载入账号：{str(AllUnameByUid4Dict)}")
    # 获取 '默认账户' 导航栏用户信息
    DefaultUserInterfaceNav = BilibiliApiMaster(dict2cookie(
        b_u_l_c.get_cookies())).interface_nav() if b_u_l_c.get_cookies() else None
    # 获取默认账号的昵称
    DefaultUname = DefaultUserInterfaceNav["uname"] if b_u_l_c.get_cookies() else None
    """
    默认用户config["DefaultUser"]的昵称
    没有则为None
    """
    logSave(0, f"用户：{DefaultUname} 已登录" if b_u_l_c.get_cookies() else f"未登录账号")

    # 设置 只读文本框【登录状态】 可见状态
    GlobalVariableOfTheControl.login_status_textBox_visible = True
    logSave(0, f"设置 只读文本框【登录状态】 可见状态：{str(GlobalVariableOfTheControl.login_status_textBox_visible)}")
    # 设置 只读文本框【登录状态】 可用状态
    GlobalVariableOfTheControl.login_status_textBox_enabled = True
    logSave(0, f"设置 只读文本框【登录状态】 可用状态：{str(GlobalVariableOfTheControl.login_status_textBox_enabled)}")
    # 设置 只读文本框【登录状态】 信息类型
    GlobalVariableOfTheControl.login_status_textBox_type = obs.OBS_TEXT_INFO_NORMAL if b_u_l_c.get_cookies() else obs.OBS_TEXT_INFO_WARNING
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 只读文本框【登录状态】 信息类型：{textBox_type_name4textBox_type[GlobalVariableOfTheControl.login_status_textBox_type]}")
    # 设置 只读文本框【登录状态】 内容
    GlobalVariableOfTheControl.login_status_textBox_string = f'{DefaultUname} 已登录' if b_u_l_c.get_cookies() else '未登录，请登录后点击【更新账号列表】'
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 只读文本框【登录状态】 内容：{GlobalVariableOfTheControl.login_status_textBox_string}")

    # 设置 组合框【用户】 可见状态
    GlobalVariableOfTheControl.uid_comboBox_visible = True
    logSave(0, f"设置 组合框【用户】 可见状态：{str(GlobalVariableOfTheControl.uid_comboBox_visible)}")
    # 设置 组合框【用户】 可用状态
    GlobalVariableOfTheControl.uid_comboBox_enabled = True
    logSave(0, f"设置 组合框【用户】 可用状态：{str(GlobalVariableOfTheControl.uid_comboBox_enabled)}")
    # 设置 组合框【用户】 的数据字典
    GlobalVariableOfTheControl.uid_comboBox_dict = {uid or '-1': AllUnameByUid4Dict.get(uid, '添加或选择一个账号登录') for uid in b_u_l_c.get_users().values()}
    logSave(0, f"设置 组合框【用户】 数据字典：{str(GlobalVariableOfTheControl.uid_comboBox_dict)}")
    # 设置 组合框【用户】 默认显示内容
    GlobalVariableOfTheControl.uid_comboBox_string = DefaultUname if b_u_l_c.get_cookies() else '添加或选择一个账号登录'
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 组合框【用户】 内容：{GlobalVariableOfTheControl.uid_comboBox_string}")
    # 设置 组合框【用户】 默认显示内容 的 列表值
    GlobalVariableOfTheControl.uid_comboBox_value = b_u_l_c.get_users()[0] if b_u_l_c.get_cookies() else '-1'
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 设置 组合框【用户】 列表值：{GlobalVariableOfTheControl.uid_comboBox_value}")

    # 设置 按钮【登录账号】 可见状态
    GlobalVariableOfTheControl.login_button_visible = True if AllUnameByUid4Dict else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，设置 按钮【登录账号】 可见状态：{str(GlobalVariableOfTheControl.login_button_visible)}")
    # 设置 按钮【登录账号】 可用状态
    GlobalVariableOfTheControl.login_button_enabled = True if AllUnameByUid4Dict else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，设置 按钮【登录账号】 可用状态：{str(GlobalVariableOfTheControl.login_button_enabled)}")

    # 设置 按钮【更新账号列表】 可见状态
    GlobalVariableOfTheControl.update_account_list_button_visible = True
    logSave(0, f"设置 按钮【更新账号列表】 可见状态：{str(GlobalVariableOfTheControl.update_account_list_button_visible)}")
    # 设置 按钮【更新账号列表】 可用状态
    GlobalVariableOfTheControl.update_account_list_button_enabled = True
    logSave(0, f"设置 按钮【更新账号列表】 可用状态：{str(GlobalVariableOfTheControl.update_account_list_button_enabled)}")

    # 设置 按钮【二维码添加账户】 可见状态
    GlobalVariableOfTheControl.qr_add_account_button_visible = True
    logSave(0, f"设置 按钮【二维码添加账户】 可见状态：{str(GlobalVariableOfTheControl.qr_add_account_button_visible)}")
    # 设置 按钮【二维码添加账户】 可用状态
    GlobalVariableOfTheControl.qr_add_account_button_enabled = True
    logSave(0, f"设置 按钮【二维码添加账户】 可用状态：{str(GlobalVariableOfTheControl.qr_add_account_button_enabled)}")

    # 设置 按钮【显示二维码图片】 可见状态
    GlobalVariableOfTheControl.display_qr_picture_button_visible = True
    logSave(0, f"设置 按钮【显示二维码图片】 可见状态：{str(GlobalVariableOfTheControl.display_qr_picture_button_visible)}")
    # 设置 按钮【显示二维码图片】 可用状态
    GlobalVariableOfTheControl.display_qr_picture_button_enabled = True
    logSave(0, f"设置 按钮【显示二维码图片】 可用状态：{str(GlobalVariableOfTheControl.display_qr_picture_button_enabled)}")

    # 设置 按钮【删除账户】 可见状态
    GlobalVariableOfTheControl.delete_account_button_visible = True if AllUnameByUid4Dict else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，设置 按钮【删除账户】 可见状态：{str(GlobalVariableOfTheControl.delete_account_button_visible)}")
    # 设置 按钮【删除账户】 可用状态
    GlobalVariableOfTheControl.delete_account_button_enabled = True if AllUnameByUid4Dict else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，设置 按钮【删除账户】 可用状态：{str(GlobalVariableOfTheControl.delete_account_button_enabled)}")

    # 设置 按钮【备份账户】 可见状态
    GlobalVariableOfTheControl.backup_account_button_visible = False
    logSave(0, f"设置 按钮【备份账户】 可见状态：{str(GlobalVariableOfTheControl.backup_account_button_visible)}")
    # 设置 按钮【备份账户】 可用状态
    GlobalVariableOfTheControl.backup_account_button_enabled = False
    logSave(0, f"设置 按钮【备份账户】 可用状态：{str(GlobalVariableOfTheControl.backup_account_button_enabled)}")

    # 设置 按钮【恢复账户】 可见状态
    GlobalVariableOfTheControl.restore_account_button_visible = False
    logSave(0, f"设置 按钮【恢复账户】 可见状态：{str(GlobalVariableOfTheControl.restore_account_button_visible)}")
    # 设置 按钮【恢复账户】 可用状态
    GlobalVariableOfTheControl.restore_account_button_enabled = False
    logSave(0, f"设置 按钮【恢复账户】 可用状态：{str(GlobalVariableOfTheControl.restore_account_button_enabled)}")

    # 设置 按钮【登出账号】 可见状态
    GlobalVariableOfTheControl.logout_button_visible = True if AllUnameByUid4Dict and b_u_l_c.get_cookies() else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，是否登录：{str(bool(b_u_l_c.get_cookies()))}，设置 按钮【登出账号】 可见状态：{str(GlobalVariableOfTheControl.logout_button_visible)}")
    # 设置 按钮【登出账号】 可用状态
    GlobalVariableOfTheControl.logout_button_enabled = True if AllUnameByUid4Dict and b_u_l_c.get_cookies() else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，是否登录：{str(bool(b_u_l_c.get_cookies()))}，设置 按钮【登出账号】 可用状态：{str(GlobalVariableOfTheControl.logout_button_enabled)}")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 设置 只读文本框【登录状态】 信息类型
    obs.obs_property_text_set_info_type(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.login_status_textBox_type)
    # 使 只读文本框【登录状态】 显示
    obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'login_status_textBox', f'{GlobalVariableOfTheControl.login_status_textBox_string}')
    # 更新 只读文本框【登录状态】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.script_settings)

    # 判断组合框【用户】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.uid_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))} or obs.obs_property_visible(GlobalVariableOfTheControl.uid_comboBox) != GlobalVariableOfTheControl.uid_comboBox_visible:
        logSave(0, f"数据发生变动，组合框【用户】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.uid_comboBox_dict}")
        # 设置 组合框【用户】 可见状态
        obs.obs_property_set_visible(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.uid_comboBox_visible)
        # 清空组合框【用户】
        obs.obs_property_list_clear(GlobalVariableOfTheControl.uid_comboBox)
        # 为 组合框【用户】 添加选项  # 会排出字典数据中的 默认值 ，防止在后续操作默认值的时候重复添加，导致选项重复
        for uid in GlobalVariableOfTheControl.uid_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.uid_comboBox_dict[uid], uid) if uid != GlobalVariableOfTheControl.uid_comboBox_value else None
        # 为 组合框【用户】 添加默认选项 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.uid_comboBox, 0, GlobalVariableOfTheControl.uid_comboBox_string, GlobalVariableOfTheControl.uid_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'uid_comboBox', GlobalVariableOfTheControl.uid_comboBox_value)) if GlobalVariableOfTheControl.uid_comboBox_value in GlobalVariableOfTheControl.uid_comboBox_dict else None
        # 更新 组合框【用户】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.script_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【用户】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.uid_comboBox_dict}")

    # 设置 按钮【登录账号】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.login_button_visible)
    # 设置 按钮【登录账号】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.login_button_enabled)
    # 更新 按钮【登录账号】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【二维码添加账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.qr_add_account_button, GlobalVariableOfTheControl.qr_add_account_button_visible)
    # 设置 按钮【二维码添加账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.qr_add_account_button, GlobalVariableOfTheControl.qr_add_account_button_enabled)
    # 更新 按钮【二维码添加账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.qr_add_account_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【显示二维码图片】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.display_qr_picture_button, GlobalVariableOfTheControl.display_qr_picture_button_visible)
    # 设置 按钮【显示二维码图片】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.display_qr_picture_button, GlobalVariableOfTheControl.display_qr_picture_button_enabled)
    # 更新 按钮[显示二维码图片】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.display_qr_picture_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【删除账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.delete_account_button_visible)
    # 设置 按钮【删除账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.delete_account_button_enabled)
    # 更新 按钮[删除账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【备份账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.backup_account_button_visible)
    # 设置 按钮【备份账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.backup_account_button_enabled)
    # 更新 按钮[备份账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【恢复账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.restore_account_button_visible)
    # 设置 按钮【恢复账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.restore_account_button_enabled)
    # 更新 按钮[恢复账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【登出账号】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.logout_button_visible)
    # 设置 按钮【登出账号】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.logout_button_enabled)
    # 更新 按钮[登出账号】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.script_settings)

    return True


def button_function_qr_add_account(props, prop):
    """
    二维码添加账号
    Args:
        props:
        prop:
    Returns:
    """
    qr_add_user()
    return True


def button_function_show_qr_picture(props, prop):
    """
    显示二维码图片
    Args:
        props:
        prop:
    Returns:
    """
    if GlobalVariableOfData.LoginQRCodePillowImg:
        logSave(0, f"展示登录二维码图片")
        GlobalVariableOfData.LoginQRCodePillowImg.show()
    else:
        logSave(2, f"没有可展示的登录二维码图片，请点击按钮 【二维码添加账号】创建")
    pass


def button_function_del_user(props, prop):
    """
    删除用户
    Args:
        props:
        prop:
    Returns:
    """
    uid = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'uid_comboBox')
    if uid not in ["-1"]:
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
        b_u_l_c.delete_user(uid)
    else:
        logSave(2, "请选择一个账号")
        return None
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.script_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
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
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　登出        ＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 如果添加账户 移除默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    b_u_l_c.update_ser(None)
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　更新     　　＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.script_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    update_ui_interface_data()
    return True


def button_function_update_room_cover(props, prop):
    """
    上传直播间封面
    Args:
        props:
        prop:
    Returns:
    """
    # 获取文件对话框内容
    GlobalVariableOfTheControl.room_cover_fileDialogBox_string = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'room_cover_fileDialogBox')
    logSave(0, f"获得图片文件：{GlobalVariableOfTheControl.room_cover_fileDialogBox_string}")
    if GlobalVariableOfTheControl.room_cover_fileDialogBox_string:
        PIL_Image = Image.open(GlobalVariableOfTheControl.room_cover_fileDialogBox_string)
        logSave(0, f"图片文件PIL_Image实例化，当前文件大小(宽X高)：{PIL_Image.size}")
        PIL_Image1609 = pil_image2central_proportion_cutting(PIL_Image, 16 / 9)
        PIL_Image1609_w, PIL_Image1609_h = PIL_Image1609.size
        logSave(0, f"图片16:9裁切后大小(宽X高)：{PIL_Image1609.size}")
        PIL_Image1609ZoomingWidth1020 = PIL_Image1609 if PIL_Image1609_w < 1020 else pil_image2zooming(PIL_Image1609, 4,
                                                                                                       target_width=1020)
        logSave(0, f"限制宽<1020，进行缩放，缩放后大小：{PIL_Image1609ZoomingWidth1020.size}")
        PIL_Image1609 = pil_image2central_proportion_cutting(PIL_Image1609ZoomingWidth1020, 16 / 9)
        logSave(0, f"缩放后图片16:9裁切后大小(宽X高)：{PIL_Image1609.size}")
        PIL_Image0403 = pil_image2central_proportion_cutting(PIL_Image1609ZoomingWidth1020, 4 / 3)
        logSave(0, f"缩放后图片4:3裁切后大小(宽X高)：{PIL_Image0403.size}")
        logSave(0, f"展示图片")
        PIL_Image0403.show()
        PIL_Image1609.show()
        PIL_Image1609ZoomingWidth1020Binary = pil_image2binary(PIL_Image1609ZoomingWidth1020, img_format="JPEG",
                                                               compress_level=0)
        logSave(0, f"图片二进制化")
        # 创建用户配置文件实例
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
        # 获取 '默认账户' cookies
        DefaultUserCookies = b_u_l_c.get_cookies()
        coverUrl = BilibiliApiCsrfAuthentication(dict2cookie(DefaultUserCookies)).upload_cover(PIL_Image1609ZoomingWidth1020Binary)['data']['location']
        logSave(0, f"上传二进制图片，获得图片链接：{coverUrl}")
        BilibiliApiCsrfAuthentication(dict2cookie(DefaultUserCookies)).update_cover(coverUrl)
        logSave(0, f"更改封面结束")
    else:
        logSave(2, "未获取到图片")
    pass


def button_function_check_room_cover(props, prop):
    """
    查看直播间封面
    Args:
        props:
        prop:
    Returns:
    """
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    # 获取'默认账户'获取用户对应的直播间 状态
    RoomInfoOld = BilibiliApiGeneric().get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else {}
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 获取 登录账户 对应的直播间 状态：数据长度为{len(RoomInfoOld)}")
    # 获取 默认用户 的 直播间 状态
    DefaultRoomStatus = RoomInfoOld["roomStatus"] if b_u_l_c.get_cookies() else None
    # 获取默认用户的 直播间id
    DefaultRoomid = RoomInfoOld["roomid"] if bool(DefaultRoomStatus) else 0
    # 获取'默认账户'直播间的基础信息
    RoomBaseInfo = BilibiliApiGeneric().get_room_base_info(DefaultRoomid) if DefaultRoomStatus else {}
    # 获取直播间封面的链接
    LiveRoomCover_url = RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["cover"] if bool(DefaultRoomStatus) else ""
    """
    直播间封面URL
    """
    # # 获取'默认账户'直播间的基础信息
    roomCover_pillowImg = url2pillow_image(LiveRoomCover_url)
    logSave(0, f"现在的直播间封面URL：{LiveRoomCover_url}")
    if roomCover_pillowImg:
        logSave(0, f"封面已显示，格式: {roomCover_pillowImg.format}，尺寸: {roomCover_pillowImg.size}")
        roomCover_pillowImg.show()  # 显示图像（可选）
    pass


def button_function_change_live_room_title(props, prop):
    """
    更改直播间标题
    Args:
        props:
        prop:
    Returns:
    """
    liveRoom_title_textBox_string = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'liveRoom_title_textBox')
    if GlobalVariableOfTheControl.liveRoom_title_textBox_string != liveRoom_title_textBox_string:
        GlobalVariableOfTheControl.liveRoom_title_textBox_string = liveRoom_title_textBox_string
        logSave(0, "直播间标题改变")
        # 获取 '默认账户' cookie
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
        cookies = b_u_l_c.get_cookies()
        turn_title_return = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).room_v1_Room_update(liveRoom_title_textBox_string)
        logSave(0, f"更改直播间标题返回消息：{turn_title_return}")
    else:
        logSave(0, "直播间标题未改变")
    pass


def button_function_change_live_room_news(props, prop):
    """
    更改直播间公告
    Args:
        props:
        prop:
    Returns:
    """
    liveRoom_news_textBox_string = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'liveRoom_news_textBox')
    if GlobalVariableOfTheControl.liveRoom_news_textBox_string != liveRoom_news_textBox_string:
        GlobalVariableOfTheControl.liveRoom_news_textBox_string = liveRoom_news_textBox_string
        logSave(0, "直播间公告已改变")
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
        cookies = b_u_l_c.get_cookies()
        turn_news_return = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).updateRoomNews(liveRoom_news_textBox_string)
        logSave(0, f'更改直播间公告返回消息：{turn_news_return}')
    else:
        logSave(0, "直播间公告未改变")
    pass


def button_function_start_area1(props, prop, settings=GlobalVariableOfTheControl.script_settings):
    """
    确认一级分区
    Args:
        props:
        prop:
        settings:
    Returns:
    """
    # #获取 组合框【一级分区】 当前选项的值
    parentLiveArea_comboBox_value = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'parentLiveArea_comboBox')
    logSave(0, f"获取 组合框【一级分区】 当前选项的值{parentLiveArea_comboBox_value}")
    if parentLiveArea_comboBox_value not in ["-1"]:
        subLiveAreaNameByid4dict = {str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in BilibiliApiGeneric().getsub_live_area_obj_list(parentLiveArea_comboBox_value)} if parentLiveArea_comboBox_value else {"-1": "请选择一级分区"}
        logSave(0, f"选中的父分区id：{parentLiveArea_comboBox_value} 获取 登录账户 当前父分区对应的子分区数据{subLiveAreaNameByid4dict}")
        # 设置 组合框【二级分区】 数据字典
        GlobalVariableOfTheControl.subLiveArea_comboBox_dict = subLiveAreaNameByid4dict
    else:
        logSave(2, "请选择一级分区")
        return None

    # 判断字典数据 和 组合框 当前数据是否有变化
    if GlobalVariableOfTheControl.subLiveArea_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))} or obs.obs_property_visible(GlobalVariableOfTheControl.subLiveArea_comboBox) != GlobalVariableOfTheControl.subLiveArea_comboBox_visible:
        logSave(0, f"数据发生变动，组合框【二级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.subLiveArea_comboBox_dict}")
        # 设置 组合框【二级分区】 可见状态
        obs.obs_property_set_visible(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_visible)
        # 清空组合框【二级分区】
        obs.obs_property_list_clear(GlobalVariableOfTheControl.subLiveArea_comboBox)
        # 为 组合框【二级分区】 添加选项
        for subLiveAreaId in GlobalVariableOfTheControl.subLiveArea_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_dict[subLiveAreaId], subLiveAreaId) if subLiveAreaId != GlobalVariableOfTheControl.subLiveArea_comboBox_value else obs.obs_property_list_insert_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0, GlobalVariableOfTheControl.subLiveArea_comboBox_string, GlobalVariableOfTheControl.subLiveArea_comboBox_value)
        # # 为 组合框【二级分区】 添加默认选项
        # logSave(0, f"为 组合框【二级分区】 添加默认选项{GlobalVariableOfTheControl.subLiveArea_comboBox_string}, {GlobalVariableOfTheControl.subLiveArea_comboBox_value}")
        # obs.obs_property_list_insert_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0, GlobalVariableOfTheControl.subLiveArea_comboBox_string, GlobalVariableOfTheControl.subLiveArea_comboBox_value) if GlobalVariableOfTheControl.subLiveArea_comboBox_value in GlobalVariableOfTheControl.subLiveArea_comboBox_dict else None
        # 为 组合框【二级分区】 添加默认选项
        obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, "subLiveArea_comboBox", obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0))  # if GlobalVariableOfTheControl.subLiveArea_comboBox_value in GlobalVariableOfTheControl.subLiveArea_comboBox_dict else None
        # # 更新 组合框【二级分区】 显示
        # logSave(0, f"{obs.obs_property_modified(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.script_settings)}")
    else:
        logSave(0, f"数据未发生变动，组合框【二级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.subLiveArea_comboBox_dict}")
    return True


def button_function_start_area():
    # #获取 组合框【二级分区】 当前选项的值
    subLiveArea_comboBox_value = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'subLiveArea_comboBox')
    if subLiveArea_comboBox_value != GlobalVariableOfTheControl.subLiveArea_comboBox_value:
        logSave(0, f"子分区有变化{subLiveArea_comboBox_value}")
        # 获取默认账户
        b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
        cookies = b_u_l_c.get_cookies()
        # 获取二级分区id
        area2_id = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'subLiveArea_comboBox')
        ChangeRoomArea = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).AnchorChangeRoomArea(int(area2_id))
        logSave(0, f"更新直播间分区返回：{ChangeRoomArea}")
        if ChangeRoomArea["code"]:
            logSave(2, f"更新直播间分区失败：{ChangeRoomArea['message']}")
        else:
            GlobalVariableOfTheControl.subLiveArea_comboBox_value = subLiveArea_comboBox_value
            GlobalVariableOfTheControl.subLiveArea_comboBox_string = GlobalVariableOfTheControl.subLiveArea_comboBox_dict[subLiveArea_comboBox_value]
    else:
        logSave(0, "子分区没变化")
    pass


def button_function_jump_blive_web(props, prop):
    """
    跳转直播间后台网页
    Args:
        props:
        prop:
    Returns:
    """
    logSave(0, f"即将跳转到网页{GlobalVariableOfTheControl.jump_blive_web_button_url}")
    pass


# ____________________-------------------____________________---------------------_______________________---------------
def button_function_start_live(props, prop):
    """
    开始直播
    Args:
        props:
        prop:
    Returns:
    """
    logSave(0, 'start_live')
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    cookies = b_u_l_c.get_cookies()
    # 开播
    if cookies:
        # 获取二级分区id
        subLiveArea_id = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'subLiveArea_comboBox')
        live_streaming_platform = obs.obs_data_get_string(GlobalVariableOfTheControl.script_settings, 'live_streaming_platform_comboBox')
        logSave(0, f"使用【{live_streaming_platform}】开播")
        startLive = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).startLive(int(subLiveArea_id), live_streaming_platform)
        logSave(0, f"开播消息代码【{startLive['code']}】。消息内容：【{startLive['message']}】。")
        # 推流地址
        rtmpServer = startLive["data"]["rtmp"]["addr"]
        logSave(0, f"rtmp推流地址：{rtmpServer}")
        # 将 rtmp推流码 复制到剪贴板
        rtmpPushCode = startLive["data"]["rtmp"]["code"]
        logSave(0, f"将rtmp推流码复制到剪贴板，rtmp推流码：{rtmpPushCode}")
        cb.copy(rtmpPushCode)

        # 获取当前流服务
        streaming_service = obs.obs_frontend_get_streaming_service()
        # 获取当前流服务设置
        streaming_service_settings = obs.obs_service_get_settings(streaming_service)
        currentlyService_string = obs.obs_data_get_string(streaming_service_settings, "service")
        logSave(0, f"目前推流服务：【{currentlyService_string}】")
        currentlyRtmpServer = obs.obs_data_get_string(streaming_service_settings, "server")
        logSave(0, f"目前rtmp推流地址：【{currentlyRtmpServer}】")
        currentlyRtmpPushCode = obs.obs_data_get_string(streaming_service_settings, "key")
        logSave(0, f"目前rtmp推流码：【{currentlyRtmpPushCode}】")
        logSave(0, f"obs推流状态：{obs.obs_frontend_streaming_active()}")
        if currentlyService_string == "" and currentlyRtmpServer == rtmpServer and currentlyRtmpPushCode == rtmpPushCode:
            logSave(0, f"由于：推流信息未发生变化")
            if obs.obs_frontend_streaming_active():
                logSave(0, f"正处于推流状态中。。。")
                pass
            else:
                logSave(0, f"直接开始推流")
                obs.obs_frontend_streaming_start()
        else:
            logSave(0, f"由于：推流信息发生变化")
            # 写入推流服务
            obs.obs_data_set_string(streaming_service_settings, "service", None)
            logSave(0, f"写入推流服务：【】")
            # 写入推流地址
            obs.obs_data_set_string(streaming_service_settings, "server", rtmpServer)
            logSave(0, f"写入推流地址：【{rtmpServer}】")
            # 写入rtmp推流码
            obs.obs_data_set_string(streaming_service_settings, "key", rtmpPushCode)
            logSave(0, f"写入rtmp推流码：【{rtmpPushCode}】")
            # 应用更新
            obs.obs_service_update(streaming_service, streaming_service_settings)
            # 检查是否需要重启推流
            if obs.obs_frontend_streaming_active():
                logSave(0, f"由于：正处于推流状态中】➡️开始重启推流")
                # 停止推流
                logSave(0, f"重启推流第一步：停止推流")
                obs.obs_frontend_streaming_stop()

                # 设置定时器稍后重启
                def restart_streaming():
                    """重启推流"""
                    if not obs.obs_frontend_streaming_active():
                        logSave(0, f"重启推流第三步：开始推流")
                        obs.obs_frontend_streaming_start()
                        logSave(0, f"重启推流第4️⃣步：关闭重启推流的计时器")
                        obs.remove_current_callback()
                logSave(0, f"重启推流第二步：开启重启推流的计时器，3s间隔")
                obs.timer_add(restart_streaming, 3000)
            else:
                logSave(0, f"由于：当前并未正在推流】➡️直接开始推流")
                obs.obs_frontend_streaming_start()
        obs.obs_data_release(streaming_service_settings)
        # 保存到配置文件
        obs.obs_frontend_save_streaming_service()
    button_function_change_live_room_title(props, prop)
    button_function_change_live_room_news(props, prop)
    button_function_start_area1(props, prop, settings=GlobalVariableOfTheControl.script_settings)

    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.script_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    update_ui_interface_data()
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
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    cookies = b_u_l_c.get_cookies()
    StreamAddr = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).FetchWebUpStreamAddr()
    cb.copy(StreamAddr['data']['addr']['addr'])
    logSave(0, f"已将 直播服务器 复制到剪贴板：【{StreamAddr['data']['addr']['addr']}】")
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
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    cookies = b_u_l_c.get_cookies()
    StreamAddr = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).FetchWebUpStreamAddr()
    cb.copy(StreamAddr['data']['addr']['code'])
    logSave(0, f"已将 直播推流码 复制到剪贴板：【{StreamAddr['data']['addr']['code']}】")
    return True


def button_function_rtmp_stream_code_update(props, prop):
    """
    更新推流码并复制
    Args:
        props:
        prop:
    Returns:
    """
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    cookies = b_u_l_c.get_cookies()
    StreamAddr = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).FetchWebUpStreamAddr(True)
    cb.copy(StreamAddr['data']['addr']['code'])
    logSave(0, f"已更新推流码 并将 直播推流码 复制到剪贴板：【{StreamAddr['data']['addr']['code']}】")
    return True


def button_function_stop_live(props, prop, settings=GlobalVariableOfTheControl.script_settings):
    """
    结束直播
    Args:
        settings:
        props:
        prop:
    Returns:
    """
    logSave(0, 'stop_live')
    # 获取默认账户
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    cookies = b_u_l_c.get_cookies()
    # 停播
    if cookies:
        stopLive = BilibiliApiCsrfAuthentication(dict2cookie(cookies)).stopLive()
        logSave(0, f"下播消息代码【{stopLive['code']}】。消息内容：【{stopLive['message']}】。")
    # 设置组合框【用户】为'默认用户'
    obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'uid_comboBox', cookies["DedeUserID"])

    # 默认值-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=
    # 创建用户配置文件实例
    b_u_l_c = BilibiliUserLogsIn2ConfigFile(configPath=GlobalVariableOfData.scripts_config_filepath)
    # 获取'默认账户'获取用户对应的直播间 状态
    RoomInfoOld = BilibiliApiGeneric().get_room_info_old(int(b_u_l_c.get_users()[0])) if b_u_l_c.get_cookies() else {}
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 获取 登录账户 对应的直播间 状态：数据长度为{len(RoomInfoOld)}")
    # 获取 默认用户 的 直播间 状态
    DefaultRoomStatus = RoomInfoOld["roomStatus"] if b_u_l_c.get_cookies() else None
    """
    登录的用户的直播间存在状态
    """
    logSave(0, f"根据是否有账号登录：{bool(b_u_l_c.get_cookies())} 获取 登录账户 是否有直播间：{DefaultRoomStatus}")
    # 获取默认用户的 直播状态
    DefaultLiveStatus = RoomInfoOld["liveStatus"] if bool(DefaultRoomStatus) else None
    """
    直播状态
    0：未开播 1：直播中
    """
    logSave(0, f"根据 登录账户 直播间存在：{bool(DefaultRoomStatus)} 获取 登录账户 的 直播状态：{DefaultLiveStatus}")
    # 设置 组合框【直播平台】 可见状态
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 组合框【直播平台】 可见状态：{str(GlobalVariableOfTheControl.jump_blive_web_button_visible)}")
    # 设置 组合框【直播平台】 可用状态
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 组合框【直播平台】 可用状态：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_enabled)}")
    # 设置 组合框【直播平台】 的数据字典
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict = {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}
    logSave(0, f"设置 组合框【直播平台】 的数据字典：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict)}")
    # 设置 组合框【直播平台】 的内容
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_string = ""
    logSave(0, f"设置 组合框【直播平台】 的内容：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_string)}")
    # 设置 组合框【直播平台】 的内容 的 列表值
    GlobalVariableOfTheControl.live_streaming_platform_comboBox_value = ""
    logSave(0, f"设置 组合框【直播平台】 的内容 的 列表值：{str(GlobalVariableOfTheControl.live_streaming_platform_comboBox_value)}")

    # 设置 按钮【开始直播并复制推流码】 可见状态
    GlobalVariableOfTheControl.start_live_button_visible = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【开始直播并复制推流码】 可见状态：{str(GlobalVariableOfTheControl.start_live_button_visible)}")
    # 设置 按钮【开始直播并复制推流码】 可用状态
    GlobalVariableOfTheControl.start_live_button_enabled = True if ((not DefaultLiveStatus) and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【开始直播并复制推流码】 可用状态：{str(GlobalVariableOfTheControl.start_live_button_enabled)}")

    # 设置 按钮【复制直播服务器】 可见状态
    GlobalVariableOfTheControl.rtmp_address_copy_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播服务器】 可见状态：{str(GlobalVariableOfTheControl.rtmp_address_copy_button_visible)}")
    # 设置 按钮【复制直播服务器】 可用状态
    GlobalVariableOfTheControl.rtmp_address_copy_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播服务器】 可用状态：{str(GlobalVariableOfTheControl.rtmp_address_copy_button_enabled)}")

    # 设置 按钮【复制直播推流码】 可见状态
    GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播推流码】 可见状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible)}")
    # 设置 按钮【复制直播推流码】 可用状态
    GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【复制直播推流码】 可用状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_copy_button_enabled)}")

    # 设置 按钮【更新推流码并复制】 可见状态
    GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【更新推流码并复制】 可见状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible)}")
    # 设置 按钮【更新推流码并复制】 可用状态
    GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【更新推流码并复制】 可用状态：{str(GlobalVariableOfTheControl.rtmp_stream_code_update_button_enabled)}")

    # 设置 按钮【结束直播】 可见状态
    GlobalVariableOfTheControl.stop_live_button_visible = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【结束直播】 可见状态：{str(GlobalVariableOfTheControl.stop_live_button_visible)}")
    # 设置 按钮【结束直播】 可用状态
    GlobalVariableOfTheControl.stop_live_button_enabled = True if (DefaultLiveStatus and DefaultRoomStatus) else False
    logSave(0, f"根据直播间存在：{str(bool(DefaultRoomStatus))}，直播状态{str(bool(DefaultRoomStatus))}，设置 按钮【结束直播】 可用状态：{str(GlobalVariableOfTheControl.stop_live_button_enabled)}")

    # ————————————————————————————————————————————————————————————————
    # 判断组合框【直播平台】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.live_streaming_platform_comboBox))} or obs.obs_property_visible(GlobalVariableOfTheControl.live_streaming_platform_comboBox) != GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible:
        logSave(0, f"数据发生变动，组合框【直播平台】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.live_streaming_platform_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict}")
        # 设置 组合框【直播平台】 可见状态
        obs.obs_property_set_visible(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.live_streaming_platform_comboBox_visible)
        # 清空组合框【直播平台】
        obs.obs_property_list_clear(GlobalVariableOfTheControl.live_streaming_platform_comboBox)
        # 为 组合框【直播平台】 添加选项
        for LivePlatforms in GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict[LivePlatforms], LivePlatforms) if LivePlatforms != GlobalVariableOfTheControl.live_streaming_platform_comboBox_value else None
        # 为 组合框【直播平台】 添加默认选项 # 先判断设置的默认值是否在字典数据中，如果不在就不会设定默认选项，如果在，就将默认值设置到第一个选项并且强制设置为显示的选项
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, 0, GlobalVariableOfTheControl.live_streaming_platform_comboBox_string, GlobalVariableOfTheControl.live_streaming_platform_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.script_settings, 'live_streaming_platform_comboBox', GlobalVariableOfTheControl.live_streaming_platform_comboBox_value)) if GlobalVariableOfTheControl.live_streaming_platform_comboBox_value in GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict else None
        # 更新 组合框【直播平台】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.script_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【直播平台】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.live_streaming_platform_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict}")

    # 设置 按钮【开始直播并复制推流码】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.start_live_button, GlobalVariableOfTheControl.start_live_button_visible)
    # 更新 按钮【开始直播并复制推流码】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.start_live_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【复制直播服务器】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_address_copy_button, GlobalVariableOfTheControl.rtmp_address_copy_button_visible)
    # 更新 按钮【复制直播服务器】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.rtmp_address_copy_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【复制直播推流码】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_stream_code_copy_button, GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible)
    # 更新 按钮【复制直播推流码】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.rtmp_stream_code_copy_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【更新推流码并复制】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_stream_code_update_button, GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible)
    # 更新 按钮【更新推流码并复制】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.rtmp_stream_code_update_button, GlobalVariableOfTheControl.script_settings)

    # 设置 按钮【结束直播】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.stop_live_button, GlobalVariableOfTheControl.stop_live_button_visible)
    # 更新 按钮【结束直播】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.stop_live_button, GlobalVariableOfTheControl.script_settings)

    if obs.obs_frontend_streaming_active():
        # 停止推流
        logSave(0, f"停止推流")
        obs.obs_frontend_streaming_stop()
    obs.obs_properties_apply_settings(GlobalVariableOfTheControl.live_props, GlobalVariableOfTheControl.script_settings)
    return True


def script_unload():
    """
    在脚本被卸载时调用。
    """
    # """注销事件回调"""
    logSave(0, "╭—————————————————╮")
    logSave(0, "│　 停止监视obs事件  │")
    logSave(0, "╰—————————————————╯")
    obs.obs_frontend_remove_event_callback(on_event)
    logSave(0, "╔════════════════════════╗")
    logSave(0, "║  已卸载: bilibili-live  ║")
    logSave(0, "╚════════════════════════╝")
    with open(Path(GlobalVariableOfData.scripts_data_dirpath) / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", "w", encoding="utf-8") as f:
        f.write(str(GlobalVariableOfData.logRecording))


def test(t=""):
    if GlobalVariableOfTheControl.isScript_propertiesNum == 1:
        logSave(0, f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        logSave(0, f"┃　UI变动事件测试函数被调用（Script_properties）┃{t}")
        logSave(0, f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        return False
    logSave(0, f"┏━━━━━━━━━━━━━━━━━━━━━━━┓")
    logSave(0, f"┃　UI变动事件测试函数被调用  ┃{t}")
    logSave(0, f"┗━━━━━━━━━━━━━━━━━━━━━━━┛")
    return True
