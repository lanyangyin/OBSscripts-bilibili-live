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
import base64
import io
import json
# import os
import pathlib
import random
import string
# import pprint
import sys
import tempfile
# import threading
import time
import urllib
from datetime import datetime
from typing import Optional, Dict, Literal
# import zlib
from urllib.parse import quote
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
    obs.OBS_TEXT_INFO_NORMAL:'正常信息',
    obs.OBS_TEXT_INFO_WARNING:'警告信息',
    obs.OBS_TEXT_INFO_ERROR:'错误信息'
}
class GlobalVariableOfTheControl:
    # #记录obs插件中控件的数据
    current_settings = None

    # #分组框控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##【账号】分组框的实例
    setting_props = None
    setting_props_visible = None  # ###【账号】分组框的实例的【可见】
    setting_props_enabled = None  # ###【账号】分组框的实例的【可用】

    # ##【直播间】分组框的实例
    liveRoom_props = None
    liveRoom_props_visible = None  # ###【直播间】分组框的实例的【可见】
    liveRoom_props__enabled = None  # ###【直播间】分组框的实例的【可用】

    # ##【直播】分组框的实例
    live_props = None
    live_props_visible = None  # ###【直播】分组框的实例的【可见】
    live_props__enabled = None  # ###【直播】分组框的实例的【可用】

    # #【账号】分组框中的控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##只读文本框【登录状态】的实例
    login_status_textBox = None
    login_status_textBox_visible = None  # ###只读文本框【登录状态】的实例的【可见】
    login_status_textBox_enabled = None  # ###只读文本框【登录状态】的实例的【可用】
    login_status_textBox_type = None  # ###只读文本框【登录状态】的实例的【类型】
    login_status_textBox_string = ""  # ###只读文本框【登录状态】的实例的【显示】
    """
    obs.OBS_TEXT_INFO_NORMAL
    obs.OBS_TEXT_INFO_WARNING
    """

    # ##组合框【用户】的实例
    uid_comboBox = None
    uid_comboBox_visible = None
    uid_comboBox_enabled = None
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
    login_button_visible = None  # ###按钮【登录账号】的实例的【可见】
    login_button_enabled = None  # ###按钮【登录账号】的实例的【可用】

    # ##按钮【更新账号列表】的实例
    update_account_list_button = None
    update_account_list_button_visible = None  # ###按钮【更新账号列表】的实例的【可见】
    update_account_list_button_enabled = None  # ###按钮【更新账号列表】的实例的【可用】

    # ##按钮【二维码添加账户】的实例
    qr_code_add_account_button = None
    qr_code_add_account_button_visible = None
    qr_code_add_account_button_enabled = None

    # ##按钮【显示登录二维码图片】的实例
    display_qr_code_picture_button = None
    display_qr_code_picture_button_visible = None
    display_qr_code_picture_button_enabled = None

    # ##按钮【删除账户】的实例
    delete_account_button = None
    delete_account_button_visible = None
    delete_account_button_enabled = None

    # ##按钮【备份账户】的实例
    backup_account_button = None
    backup_account_button_visible = None
    backup_account_button_enabled = None

    # ##按钮【恢复账户】的实例
    restore_account_button = None
    restore_account_button_visible = None
    restore_account_button_enabled = None

    # ##按钮【退出登录】的实例
    logout_button = None
    logout_button_visible = None
    logout_button_enabled = None

    # #【直播间】分组框中的控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##只读文本框【直播间状态】的实例
    room_status_textBox = None
    room_status_textBox_visible = None
    room_status_textBox_enabled = None
    room_status_textBox_type = None
    room_status_textBox_string = ""

    # ##按钮【查看当前直播间封面】的实例
    viewLiveCover_button = None
    viewLiveCover_button_visible = None
    viewLiveCover_button_enabled = None

    # ##文件对话框【直播间封面】的实例
    room_cover_fileDialogBox = None
    room_cover_fileDialogBox_visible = None
    room_cover_fileDialogBox_enabled = None
    room_cover_fileDialogBox_string = ""

    # ##按钮【上传直播间封面】的实例
    room_cover_update_button = None
    room_cover_update_button_visible = None
    room_cover_update_button_enabled = None

    # ##普通文本框【直播间标题】的实例
    liveRoom_title_textBox = None
    liveRoom_title_textBox_visible = None
    liveRoom_title_textBox_enabled = None
    liveRoom_title_textBox_string = ""

    # ##按钮【更改直播间标题】的实例
    change_liveRoom_title_button = None
    change_liveRoom_title_button_visible = None
    change_liveRoom_title_button_enabled = None

    # ##普通文本框【直播间公告】的实例
    liveRoom_news_textBox = None
    liveRoom_news_textBox_visible = None
    liveRoom_news_textBox_enabled = None
    liveRoom_news_textBox_string = ""

    # ##按钮【更改直播间公告】的实例
    change_liveRoom_news_button = None
    change_liveRoom_news_button_visible = None  # ###按钮【更改直播间公告】的实例的【可见】
    change_liveRoom_news_button_enabled = None  # ###按钮【更改直播间公告】的实例的【可用】

    # ##组合框【一级分区】的实例
    parentLiveArea_comboBox = None
    parentLiveArea_comboBox_visible = None
    parentLiveArea_comboBox_enabled = None
    parentLiveArea_comboBox_string = ""
    parentLiveArea_comboBox_value = ""
    parentLiveArea_comboBox_dict = {}

    # ##按钮【确认一级分区】的实例
    parentLiveArea_true_button = None
    parentLiveArea_true_button_visible = None
    parentLiveArea_true_button_enabled = None

    # ##组合框【二级分区】的实例
    subLiveArea_comboBox = None
    subLiveArea_comboBox_visible = None
    subLiveArea_comboBox_enabled = None
    subLiveArea_comboBox_string = ""
    subLiveArea_comboBox_value = ""
    subLiveArea_comboBox_dict = {}

    # ##按钮【「确认分区」】的实例
    subLiveArea_true_button = None
    subLiveArea_true_button_visible = None
    subLiveArea_true_button_enabled = None

    # ##普通文本框【直播间标签】的实例
    liveRoom_Tags_textBox = None
    liveRoom_Tags_textBox_visible = None
    liveRoom_Tags_textBox_enabled = None
    liveRoom_Tags_textBox_string = ""

    # ##按钮【更改直播间标签】的实例
    change_liveRoom_Tags_button = None
    change_liveRoom_Tags_button_visible = None
    change_liveRoom_Tags_button_enabled = None

    # ##url按钮【跳转直播间后台网页】
    jump_blive_web_button = None
    jump_blive_web_button_visible = None
    jump_blive_web_button_enabled = None
    jump_blive_web_button_url = ""

    # #【直播】分组框中的控件-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ##组合框【直播平台】的实例
    live_streaming_platform_comboBox = None
    live_streaming_platform_comboBox_visible = None
    live_streaming_platform_comboBox_enabled = None
    live_streaming_platform_comboBox_string = ""
    live_streaming_platform_comboBox_value = ""
    live_streaming_platform_comboBox_dict = {}
    """
    {"pc_link": "直播姬（pc）", "web_link": "web在线直播", "android_link": "bililink"}
    """

    # ##按钮【开始直播并复制推流码】的实例
    start_live_button = None
    start_live_button_visible = None  # ###按钮【开始直播并复制推流码】的实例的【可见】
    start_live_button_enabled = None  # ###按钮【开始直播并复制推流码】的实例的【可用】

    # ##按钮【复制直播服务器】的实例
    rtmp_address_copy_button = None
    rtmp_address_copy_button_visible = None
    rtmp_address_copy_button_enabled = None

    # ##按钮【复制直播推流码】的实例
    rtmp_stream_code_copy_button = None
    rtmp_stream_code_copy_button_visible = None
    rtmp_stream_code_copy_button_enabled = None

    # ##按钮【更新推流码并复制】的实例
    rtmp_stream_code_update_button = None
    rtmp_stream_code_update_button_visible = None
    rtmp_stream_code_update_button_enabled = None

    # ##按钮【结束直播】的实例
    stop_live_button = None
    stop_live_button_visible = None
    stop_live_button_enabled = None


class globalVariableOfData:
    # #是否 操作 用户配置文件 中 每一个 用户 的 可用性
    accountAvailabilityDetectionSwitch = True
    # #日志记录
    logRecording = ""
    # #网络连接状态
    networkConnectionStatus = None
    # 文件配置类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # #脚本所在目录，末尾带/
    scripts_data_dirpath = None

    # #配置文件所在路径
    scripts_config_filepath = None

    # 用户类-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    loginQrCode_key = None

    loginQrCode_returnValue = None

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
    globalVariableOfData.logRecording += log_text + "\n"


def check_network_connection():
    """检查网络连接，通过多个服务提供者的链接验证"""
    logSave(0, "\n======= 开始网络连接检查 =======")

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
            logSave(1, f'脚本数据文件【{globalVariableOfData.scripts_data_dirpath}】不存在，尝试创建')
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

    def addUser(self, cookies: dict) -> None:
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

    def deleteUser(self, uid: int) -> None:
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

    def updateUser(self, cookies: Optional[dict], setDefaultUserIs: bool = True) -> None:
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

    def getCookies(self, uid: Optional[int] = None) -> Optional[dict]:
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

    def getUsers(self) -> Dict[int, Optional[str]]:
        """
        获取所有用户列表（包含默认用户占位）

        Returns:
            字典格式 {序号: 用户ID}，其中：
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


def url2pillowImage(url) -> Image.Image:
    """
    将url图片转换为pillow_image实例
    Args:
        url:
    Returns:pillow_image实例
    """
    try:
        # 添加请求头模拟浏览器访问，避免被拒绝
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
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


def dict2cookie(jsondict: Dict[str, str]) -> str:
    """
    将字典转换为符合HTTP标准的Cookie字符串格式
    Args:
        jsondict: 包含Cookie键值对的字典
            - 示例: {"name": "value", "age": "20"}
            - 键和值将自动进行URL编码处理
    Returns:
        str: 符合Cookie规范的字符串
            - 示例: "name=value; age=20"
    Raises:
        TypeError: 当输入不是字典时抛出
    """
    if not isinstance(jsondict, dict):
        raise TypeError("输入必须是字典类型")
    cookie_parts = [
        f"{url_decoded(key)}={url_decoded(value)}"
        for key, value in jsondict.items()
        if value is not None  # 过滤空值
    ]
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
        ValueError: 当输入不是字符串时抛出
    Features:
        - 自动处理URL解码
        - 兼容不同分隔符（; 或 ; ）
        - 过滤空值和无效条目
        - 保留重复键的最后出现值（符合HTTP规范）
    """
    if not isinstance(cookie, str):
        raise TypeError("输入必须是字符串类型")
    cookie_dict = {}
    # 处理空字符串和去除首尾空格
    cookie_str = cookie.strip()
    if not cookie_str:
        return cookie_dict
    # 兼容不同分隔符格式（支持 ; 和 ; ）
    for pair in cookie_str.split(';'):
        pair = pair.strip()
        if not pair:
            continue
        # 处理键值对（仅分割第一个等号）
        try:
            key, value = pair.split('=', 1)
        except ValueError:
            continue  # 跳过无效条目
        key = key.strip()
        value = value.strip()
        # 执行URL解码（仅值部分）
        try:
            decoded_value = urllib.parse.unquote(value)
        except Exception:
            decoded_value = value  # 解码失败保留原始值
        cookie_dict[key] = decoded_value
    return cookie_dict


def url_decoded(url_string: str) -> str:
    """
    将 UTF-8 解码成 URL编码
    @param url_string: 要解码的 UTF-8 编码字符串
    @return: URL编码
    """
    # 使用quote()函数将URL编码转换为UTF-8
    utf8_encoded = quote(url_string, encoding='utf-8')
    return utf8_encoded


def qr2str_b64_PilImg4dict(qr_str: str, border: int = 2, invert: bool = False):
    """
    字符串转二维码（返回包含 PIL 图像对象的字典）
    Args:
        qr_str: 二维码文本
        border: 边框大小（默认2）
        invert: 是否反转颜色（默认False）
    Returns:
        dict: 包含以下键的字典
            - str: ASCII 字符串形式的二维码
            - base64: Base64 编码的 PNG 图像
            - img: qrcode Image 对象 [并非PIL.Image.Image 对象]
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
    b64 = base64.b64encode(buf.getvalue()).decode()
    # 捕获 print 输出
    saveStdout = sys.stdout  # 保存了当前的标准输出（stdout）
    output = io.StringIO()  # 创建一个 StringIO 对象来捕获 print 输出
    sys.stdout = output  # 将系统的标准输出重定向到 output
    # 使用 qr 对象的 print_ascii 方法将二维码以 ASCII 字符串的形式打印出来，并根据 invert 参数的值决定是否反转黑白颜色
    qr.print_ascii(out=None, tty=False, invert=invert)
    # 重定向输出到变量中
    output_str = output.getvalue()
    sys.stdout = saveStdout  # 恢复 sys.stdout
    # 将登录图片保存到临时文件
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        # 1. 将 PyPNGImage 对象保存到临时文件
        img.save(tmp.name)
        qrPilImg = Image.open(tmp.name)  # 将临时文件打开为PIL.Image.Image 对象
        """
        qr的PIL.Image.Image 对象
        """
    return {"str": output_str, "base64": b64, "img": qrPilImg}


def PIL_Image2CentralProportionCutting(
        PIL_Image: Image.Image,
        target_WidthToHeightRatio: float
) -> Optional[Image.Image]:
    """
    对图像进行中心比例裁切，保持目标宽高比

    Args:
        PIL_Image: 要处理的 PIL 图像对象
        target_WidthToHeightRatio: 目标宽高比（宽度/高度的比值）
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
    if not isinstance(PIL_Image, Image.Image):
        raise TypeError("输入必须是有效的 PIL.Image.Image 对象")

    if target_WidthToHeightRatio <= 0:
        raise ValueError("目标比例必须是正数")

    # 获取原始尺寸
    original_width, original_height = PIL_Image.size
    original_ratio = original_width / original_height

    try:
        # 计算裁切区域
        if original_ratio > target_WidthToHeightRatio:
            # 过宽：固定高度，计算宽度
            crop_height = original_height
            crop_width = int(round(crop_height * target_WidthToHeightRatio))
        else:
            # 过高：固定宽度，计算高度
            crop_width = original_width
            crop_height = int(round(crop_width / target_WidthToHeightRatio))

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

        return PIL_Image.crop((left, top, right, bottom))

    except ValueError as e:
        raise ValueError(f"裁切失败: {str(e)}")
    except Exception as e:
        raise ValueError(f"未知错误: {str(e)}")


def PIL_Image2Zooming(
        PIL_Image: Image.Image,
        ZoomingQuality: Literal[1, 2, 3, 4],
        target_width: Optional[int] = None,  # Optional[int] 可以简写为 int | None
        scale_factor: Optional[int] = None  # Optional[int] 可以简写为 int | None
) -> Image.Image:
    """
    对 PIL 图像进行缩放操作，支持指定目标宽度或缩小倍数

    Args:
        PIL_Image: 要缩放的 PIL 图像对象
        ZoomingQuality: 缩放质量等级 (1-4)
            1 = 最近邻 (速度快质量低)
            2 = 双线性 (平衡模式)
            3 = 双三次 (高质量放大)
            4 = Lanczos (最高质量)
        target_width: 目标宽度（与 scale_factor 二选一）
        scale_factor: 缩小倍数（与 target_width 二选一）

    Returns:
        dict: 包含两种缩放结果的字典
            widthZoomingPIL_Image: 按宽度缩放的结果图像（如参数有效）
            timesZoomingPIL_Image: 按比例缩放的结果图像（如参数有效）

    Raises:
        ValueError: 参数不符合要求时抛出
        TypeError: 输入图像类型错误时抛出
    """
    # 参数验证
    if not isinstance(PIL_Image, Image.Image):
        raise TypeError("输入必须是 PIL.Image.Image 对象")
    if ZoomingQuality not in (1, 2, 3, 4):
        raise ValueError("缩放质量等级必须是 1-4 的整数")
    if not (False if bool(target_width) == bool(scale_factor) else True):
        raise ValueError("正确使用参数 target_width 或 scale_factor")
    # 选择重采样滤波器
    resampling_filter4ZoomingQuality = {
        1: Image.NEAREST,
        2: Image.BILINEAR,
        3: Image.BICUBIC,
        4: Image.LANCZOS,
    }
    resampling_filter = resampling_filter4ZoomingQuality[ZoomingQuality]
    # """
    # 滤波器名称	    质量	速度	适用场景
    # Image.NEAREST	低	最快	像素艺术/保留原始像素值
    # Image.BILINEAR	中	较快	通用缩放（默认选项）
    # Image.BICUBIC	高	较慢	高质量放大
    # Image.LANCZOS	最高	最慢	超高精度缩放（推荐选项）
    # """
    original_width, original_height = PIL_Image.size
    widthHeightRatio = original_width / original_height
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
    new_height = new_width / widthHeightRatio
    ZoomingPIL_Image = PIL_Image.resize((round(new_width), round(new_height)), resampling_filter)
    return ZoomingPIL_Image


def PIL_Image2Binary(
        PIL_Image: Image.Image,
        ImgFormat: Literal["PNG", "JPEG"],
        compress_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
) -> bytes:
    """
    将 PIL 图像对象转换为指定格式的二进制数据

    Args:
        PIL_Image: PIL 图像对象
        ImgFormat: 输出图像格式
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
    if not isinstance(PIL_Image, Image.Image):
        raise ValueError("输入必须是有效的 PIL.Image.Image 对象")
    if ImgFormat not in ("PNG", "JPEG"):
        raise ValueError(f"不支持的图像格式: {ImgFormat}，只支持 PNG/JPEG")
    if compress_level not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        raise ValueError(f"不支持的压缩级别: {compress_level}，只支持 0～9")
    # 准备保存参数
    save_kwargs = {}

    match ImgFormat:
        case "PNG":
            save_kwargs = {
                "format": "PNG",
                "compress_level": compress_level  # 将压缩级别映射到质量参数 (0=最高压缩，9=最高质量)
            }
        case "JPEG":
            quality = 95 - (compress_level * 10)
            quality = max(5, min(95, quality))  # 确保在有效范围内
            # 转换图像模式为 RGB
            if PIL_Image.mode != "RGB":
                PIL_Image = PIL_Image.convert("RGB")
            save_kwargs = {
                "format": "JPEG",
                "quality": quality,
                "subsampling": 0 if quality >= 90 else 1  # 高质量使用全采样
            }
    # 执行转换
    buffer = io.BytesIO()
    try:
        PIL_Image.save(buffer, **save_kwargs)
    except Exception as e:
        raise OSError(f"图像保存失败: {str(e)}") from e
    image_bytes = buffer.getvalue()  # 转换为字节流
    return image_bytes


# end

# 不登录也能用的api
def getRoomInfoOld(mid: int) -> dict:
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
            <td>直播间状态</td>
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
    @rtype: dict
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
    data = {
        "mid": mid,
    }
    RoomInfoOld = requests.get(api, headers=headers, params=data).json()
    return RoomInfoOld["data"]


def getRoomBaseInfo(room_id: int):
    """
    直播间的
    @param room_id:
    @return:
    "data": {
        "by_uids": {

        },
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
    data = {
        'room_ids': room_id,
        'req_biz': "link-center"
    }
    RoomBaseInfo = requests.get(api, headers=headers, params=data).json()
    return RoomBaseInfo["data"]


def live_user_v1_Master_info(uid: int):
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/live_user/v1/Master/info"
    data = {
        "uid": uid
    }
    live_user_v1_Master_info = requests.get(api, headers=headers, params=data).json()
    return live_user_v1_Master_info


def getAreaObjList():
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/room/v1/Area/getList"
    AreaList = requests.get(api, headers=headers).json()
    return AreaList["data"]


def getsubLiveAreaObjList(ParentLiveAreaId: str) -> Optional[list[dict[str, str | int]]]:
    """
    返回父分区对应的子分区对象列表
    Args:
        ParentLiveAreaId: 父分区id
    Returns:子分区对象列表或None
    """
    AreaObjList = getAreaObjList()
    """
    所有分区的对象列表
    """
    for AreaObj in AreaObjList:
        if str(ParentLiveAreaId) == str(AreaObj["id"]):
            subLiveAreaObjList = AreaObj["list"]
            """
            对应一级分区的二级分区对象列表
            """
            return subLiveAreaObjList
    return None


# end


# 登陆用函数
def generate() -> dict:
    """
    申请登录二维码
    @return: {'url': 二维码文本, 'qrcode_key': 扫描秘钥}
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
    url8qrcode_key = requests.get(api, headers=headers).json()
    # print(url8qrcode_key)
    data = url8qrcode_key['data']
    url = data['url']
    qrcode_key = data['qrcode_key']
    return {'url': url, 'qrcode_key': qrcode_key}


def poll(qrcode_key: str) -> dict[str, dict[str, str] | int]:
    """
    获取登陆状态，登陆成功获取 基础的 cookies
    @param qrcode_key: 扫描秘钥
    @return: {'code', 'cookies'}
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
            <td>0：扫码登录成功<br>86038：二维码已失效<br>86090：二维码已扫码未确认<br>86101：未扫码</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    @rtype: dict
    """
    global data
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}'
    DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct = requests.get(api, data=qrcode_key, headers=headers).json()
    data = DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct['data']
    # print(data)
    cookies = {}
    code = data['code']
    if code == 0:
        def urldata_dict(url: str):
            """
            将 url参数 转换成 dict
            @param url: 带有参数的url
            @return: 转换成的dict
            @rtype: dict
            """
            urldata = url.split('?', 1)[1]
            data_list = urldata.split('&')
            data_dict = {}
            for data in data_list:
                data = data.split('=')
                data_dict[data[0]] = data[1]
            return data_dict

        data_dict = urldata_dict(data['url'])
        cookies["DedeUserID"] = data_dict['DedeUserID']
        cookies["DedeUserID__ckMd5"] = data_dict['DedeUserID__ckMd5']
        cookies["SESSDATA"] = data_dict['SESSDATA']
        cookies["bili_jct"] = data_dict['bili_jct']
        # 补充 cookie
        buvid3 = requests.get(f'https://www.bilibili.com/video/', headers=headers)
        cookies.update(buvid3.cookies.get_dict())
    return {'code': code, 'cookies': cookies}


# end


# 登陆后才能用的函数
class master:
    """登陆后才能用的函数"""

    def __init__(self, cookie: str):
        """
        完善 浏览器headers
        @param cookie: B站cookie
        """
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0")
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
        }

    def getFansMembersRank(self, uid: int) -> list:
        """
        通过用户的B站uid查看他的粉丝团成员列表
        :param uid:B站uid
        :return: list元素：[{face：头像url，guard_icon：舰队职位图标url，guard_level：舰队职位 1|2|3->总督|提督|舰长，honor_icon：""，level：粉丝牌等级，medal_color_border：粉丝牌描边颜色数值为 10 进制的 16 进制值，medal_color_start：勋章起始颜色，medal_color_end：勋章结束颜色，medal_name：勋章名，name：用户昵称，score：勋章经验值，special：""，target_id：up主mid，uid：用户mid，user_rank：在粉丝团的排名}]
        """
        api = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank"
        headers = self.headers
        page = 0
        # maxpage = 1
        RankFans = []
        FansMember = True
        while FansMember:
            # while page <= maxpage:
            page += 1
            data = {
                "ruid": uid,
                "page": page,
                "page_size": 30,
            }
            try:
                FansMembersRank = requests.get(api, headers=headers, params=data).json()
            except:
                time.sleep(5)
                FansMembersRank = requests.get(api, headers=headers, params=data).json()
            # num_FansMembersRank = FansMembersRank["data"]["num"]
            # print(FansMembersRank)
            FansMember = FansMembersRank["data"]["item"]
            RankFans += FansMember
            # maxpage = math.ceil(num_FansMembersRank / 30) + 1
        return RankFans

    def dynamic_v1_feed_space(self, host_mid, all: bool = False) -> list:
        """

        @param host_mid:
        @param all:
        @return:
        <div><h1 id="获取动态列表" tabindex="-1"><a class="header-anchor" href="#获取动态列表" aria-hidden="true">#</a> 获取动态列表
        </h1>
            <blockquote><p>https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all</p></blockquote>
            <p>请求方式：<code>GET</code></p>
            <p>是否需要登录：<code>是</code></p>
            <h2 id="json回复" tabindex="-1"><a class="header-anchor" href="#json回复" aria-hidden="true">#</a> Json回复</h2>
            <h3 id="根对象" tabindex="-1"><a class="header-anchor" href="#根对象" aria-hidden="true">#</a> 根对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>code</td>
                    <td>num</td>
                    <td>响应码</td>
                    <td>0：成功<br>-101：账号未登录</td>
                </tr>
                <tr>
                    <td>message</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>ttl</td>
                    <td>num</td>
                    <td>1</td>
                    <td></td>
                </tr>
                <tr>
                    <td>data</td>
                    <td>obj</td>
                    <td>信息本体</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象" tabindex="-1"><a class="header-anchor" href="#data对象" aria-hidden="true">#</a> <code>data</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>has_more</td>
                    <td>bool</td>
                    <td>是否有更多数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>数据数组</td>
                    <td></td>
                </tr>
                <tr>
                    <td>offset</td>
                    <td>str</td>
                    <td>偏移量</td>
                    <td>等于<code>items</code>中最后一条记录的id<br>获取下一页时使用</td>
                </tr>
                <tr>
                    <td>update_baseline</td>
                    <td>str</td>
                    <td>更新基线</td>
                    <td>等于<code>items</code>中第一条记录的id</td>
                </tr>
                <tr>
                    <td>update_num</td>
                    <td>num</td>
                    <td>本次获取获取到了多少条新动态</td>
                    <td>在更新基线以上的动态条数</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象" tabindex="-1"><a class="header-anchor" href="#data对象-items数组中的对象"
                                                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>basic</td>
                    <td>obj</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>动态id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>modules</td>
                    <td>obj</td>
                    <td>动态信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>动态类型</td>
                    <td><a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%8A%A8%E6%80%81%E7%B1%BB%E5%9E%8B"
                           class="">动态类型</a></td>
                </tr>
                <tr>
                    <td>visible</td>
                    <td>bool</td>
                    <td>是否显示</td>
                    <td><code>true</code>：正常显示<br><code>false</code>：折叠动态</td>
                </tr>
                <tr>
                    <td>orig</td>
                    <td>obj</td>
                    <td>原动态信息</td>
                    <td>仅动态类型为<code>DYNAMIC_TYPE_FORWARD</code>的情况下存在</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-basic对象" tabindex="-1"><a class="header-anchor"
                                                                           href="#data对象-items数组中的对象-basic对象"
                                                                           aria-hidden="true">#</a> <code>data</code>对象 -&gt;
                <code>items</code>数组中的对象 -&gt; <code>basic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>comment_id_str</td>
                    <td>str</td>
                    <td></td>
                    <td><code>DYNAMIC_TYPE_AV</code>：视频AV号<br><code>DYNAMIC_TYPE_UGC_SEASON</code>：视频AV号<br><code>DYNAMIC_TYPE_PGC</code>：剧集分集AV号<br><code>DYNAMIC_TYPE_LIVE_RCMD</code>：动态本身id<br><code>DYNAMIC_TYPE_DRAW</code>：相簿id<br><code>DYNAMIC_TYPE_ARTICLE</code>：专栏cv号<br><code>DYNAMIC_TYPE_FORWARD</code>：动态本身id<br><code>DYNAMIC_TYPE_WORD</code>：动态本身id<br><code>DYNAMIC_TYPE_LIVE</code>:动态本身id<br><code>DYNAMIC_TYPE_MEDIALIST</code>:收藏夹ml号
                    </td>
                </tr>
                <tr>
                    <td>comment_type</td>
                    <td>num</td>
                    <td></td>
                    <td>1：<code>DYNAMIC_TYPE_AV</code> <code>DYNAMIC_TYPE_PGC</code> <code>DYNAMIC_TYPE_UGC_SEASON</code><br>11：<code>DYNAMIC_TYPE_DRAW</code><br>12：<code>DYNAMIC_TYPE_ARTICLE</code><br>17：<code>DYNAMIC_TYPE_LIVE_RCMD</code>
                        <code>DYNAMIC_TYPE_FORWARD</code> <code>DYNAMIC_TYPE_WORD</code> <code>DYNAMIC_TYPE_COMMON_SQUARE</code><br>19：<code>DYNAMIC_TYPE_MEDIALIST</code>
                    </td>
                </tr>
                <tr>
                    <td>like_icon</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>空串</code></td>
                </tr>
                <tr>
                    <td>rid_str</td>
                    <td>str</td>
                    <td></td>
                    <td><code>DYNAMIC_TYPE_AV</code>：视频AV号<br><code>DYNAMIC_TYPE_UGC_SEASON</code>：视频AV号 <code>DYNAMIC_TYPE_PGC</code>：剧集分集EP号<br><code>DYNAMIC_TYPE_DRAW</code>：相簿id<br><code>DYNAMIC_TYPE_ARTICLE</code>：专栏cv号<br><code>DYNAMIC_TYPE_LIVE_RCMD</code>：live_id<br><code>DYNAMIC_TYPE_FORWARD</code>：未知<br><code>DYNAMIC_TYPE_WORD</code>：未知<br><code>DYNAMIC_TYPE_COMMON_SQUARE</code>：未知<br><code>DYNAMIC_TYPE_LIVE</code>：直播间id<br><code>DYNAMIC_TYPE_MEDIALIST</code>：收藏夹ml号
                    </td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-basic对象-like-icon对象" tabindex="-1"><a class="header-anchor"
                                                                                         href="#data对象-items数组中的对象-basic对象-like-icon对象"
                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>basic</code>对象 -&gt;
                <code>like_icon</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>action_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>end_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>start_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象" tabindex="-1"><a class="header-anchor"
                                                                             href="#data对象-items数组中的对象-modules对象"
                                                                             aria-hidden="true">#</a> <code>data</code>对象 -&gt;
                <code>items</code>数组中的对象 -&gt; <code>modules</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>module_author</td>
                    <td>obj</td>
                    <td>UP主信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_dynamic</td>
                    <td>obj</td>
                    <td>动态内容信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_more</td>
                    <td>obj</td>
                    <td>动态右上角三点菜单</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_stat</td>
                    <td>obj</td>
                    <td>动态统计数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_interaction</td>
                    <td>obj</td>
                    <td>热度评论</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_fold</td>
                    <td>obj</td>
                    <td>动态折叠信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_dispute</td>
                    <td>obj</td>
                    <td>争议小黄条</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_tag</td>
                    <td>obj</td>
                    <td>置顶信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象" tabindex="-1"><a class="header-anchor"
                                                                                               href="#data对象-items数组中的对象-modules对象-module-author对象"
                                                                                               aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>face</td>
                    <td>str</td>
                    <td>头像</td>
                    <td></td>
                </tr>
                <tr>
                    <td>face_nft</td>
                    <td>bool</td>
                    <td>是否为NFT头像</td>
                    <td></td>
                </tr>
                <tr>
                    <td>following</td>
                    <td>bool</td>
                    <td>是否关注此UP主</td>
                    <td>自己的动态为<code>null</code></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转链接</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>名称前标签</td>
                    <td><code>合集</code><br><code>电视剧</code><br><code>番剧</code></td>
                </tr>
                <tr>
                    <td>mid</td>
                    <td>num</td>
                    <td>UP主UID<br>剧集SeasonId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>UP主名称<br>剧集名称<br>合集名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>official_verify</td>
                    <td>obj</td>
                    <td>UP主认证信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pendant</td>
                    <td>obj</td>
                    <td>UP主头像框</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pub_action</td>
                    <td>str</td>
                    <td>更新动作描述</td>
                    <td><code>投稿了视频</code><br><code>直播了</code><br><code>投稿了文章</code><br><code>更新了合集</code><br><code>与他人联合创作</code><br><code>发布了动态视频</code><br><code>投稿了直播回放</code>
                    </td>
                </tr>
                <tr>
                    <td>pub_location_text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>pub_time</td>
                    <td>str</td>
                    <td>更新时间</td>
                    <td><code>x分钟前</code><br><code>x小时前</code><br><code>昨天</code></td>
                </tr>
                <tr>
                    <td>pub_ts</td>
                    <td>num</td>
                    <td>更新时间戳</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>作者类型</td>
                    <td><a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E4%BD%9C%E8%80%85%E7%B1%BB%E5%9E%8B"
                           class="">作者类型</a></td>
                </tr>
                <tr>
                    <td>vip</td>
                    <td>obj</td>
                    <td>UP主大会员信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>decorate</td>
                    <td>obj</td>
                    <td>装扮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>nft_info</td>
                    <td>obj</td>
                    <td>NFT头像信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-official-verify对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-official-verify对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>official_verify</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>认证说明</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>认证类型</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-pendant对象" tabindex="-1"><a class="header-anchor"
                                                                                                           href="#data对象-items数组中的对象-modules对象-module-author对象-pendant对象"
                                                                                                           aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象
                -&gt; <code>pendant</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>expire</td>
                    <td>num</td>
                    <td>过期时间</td>
                    <td>此接口返回恒为<code>0</code></td>
                </tr>
                <tr>
                    <td>image</td>
                    <td>str</td>
                    <td>头像框图片url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>image_enhance</td>
                    <td>str</td>
                    <td>头像框图片url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>image_enhance_frame</td>
                    <td>str</td>
                    <td>头像框图片逐帧序列url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>头像框名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pid</td>
                    <td>num</td>
                    <td>头像框id</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-vip对象" tabindex="-1"><a class="header-anchor"
                                                                                                       href="#data对象-items数组中的对象-modules对象-module-author对象-vip对象"
                                                                                                       aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象
                -&gt; <code>vip</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>avatar_subscript</td>
                    <td>num</td>
                    <td>是否显示角标</td>
                    <td>0：不显示<br>1：显示</td>
                </tr>
                <tr>
                    <td>avatar_subscript_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>due_date</td>
                    <td>num</td>
                    <td>大会员过期时间戳</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>obj</td>
                    <td>大会员标签</td>
                    <td></td>
                </tr>
                <tr>
                    <td>nickname_color</td>
                    <td>str</td>
                    <td>名字显示颜色</td>
                    <td>大会员：<code>#FB7299</code></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td>大会员状态</td>
                    <td>0：无<br>1：有<br>2：？</td>
                </tr>
                <tr>
                    <td>theme_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>大会员类型</td>
                    <td>0：无<br>1：月大会员<br>2：年度及以上大会员</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-vip对象-label对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-vip对象-label对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>vip</code>对象 -&gt;
                <code>label</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>会员标签背景颜色</td>
                    <td><code>#FB7299</code></td>
                </tr>
                <tr>
                    <td>bg_style</td>
                    <td>num</td>
                    <td><code>0</code> <code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>border_color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>img_label_uri_hans</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>动态版 简体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hans_static</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>静态版 简体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hant</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>动态版 繁体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hant_static</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>静态版 繁体版</td>
                </tr>
                <tr>
                    <td>label_theme</td>
                    <td>str</td>
                    <td>会员标签</td>
                    <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员<br>fools_day_hundred_annual_vip：最强绿鲤鱼
                    </td>
                </tr>
                <tr>
                    <td>path</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>会员类型文案</td>
                    <td><code>大会员</code> <code>年度大会员</code> <code>十年大会员</code> <code>百年大会员</code>
                        <code>最强绿鲤鱼</code></td>
                </tr>
                <tr>
                    <td>text_color</td>
                    <td>str</td>
                    <td>用户名文字颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>use_img_label</td>
                    <td>bool</td>
                    <td><code>true</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-decorate对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-decorate对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>decorate</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>card_url</td>
                    <td>str</td>
                    <td>动态卡片小图标图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>fan</td>
                    <td>obj</td>
                    <td>粉丝装扮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>装扮ID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>装扮名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-decorate对象-fan对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-decorate对象-fan对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>decorate</code>对象 -&gt;
                <code>fan</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>编号颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>is_fan</td>
                    <td>bool</td>
                    <td>是否是粉丝装扮</td>
                    <td></td>
                </tr>
                <tr>
                    <td>num_str</td>
                    <td>str</td>
                    <td>装扮编号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>number</td>
                    <td>num</td>
                    <td>装扮编号</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-nft-info对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-nft-info对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>nft_info</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>region_icon</td>
                    <td>str</td>
                    <td>NFT头像角标URL</td>
                    <td>
                        类型1：https://i0.hdslb.com/bfs/activity-plat/static/20220506/334553dd7c506a92b88eaf4d59ac8b4d/j8AeXAkEul.gif
                        <br>类型2：https://i0.hdslb.com/bfs/activity-plat/static/20220506/334553dd7c506a92b88eaf4d59ac8b4d/IOHoVs1ebP.gif
                    </td>
                </tr>
                <tr>
                    <td>region_type</td>
                    <td>num</td>
                    <td>NFT头像角标类型</td>
                    <td>1,2</td>
                </tr>
                <tr>
                    <td>show_status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象" tabindex="-1"><a class="header-anchor"
                                                                                                href="#data对象-items数组中的对象-modules对象-module-dynamic对象"
                                                                                                aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>additional</td>
                    <td>obj</td>
                    <td>相关内容卡片信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>obj</td>
                    <td>动态文字内容</td>
                    <td>其他动态时为null</td>
                </tr>
                <tr>
                    <td>major</td>
                    <td>obj</td>
                    <td>动态主体对象</td>
                    <td>转发动态时为null</td>
                </tr>
                <tr>
                    <td>topic</td>
                    <td>obj</td>
                    <td>话题信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>common</td>
                    <td>obj</td>
                    <td>一般类型</td>
                    <td><code>ADDITIONAL_TYPE_COMMON</code>类型独有</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>卡片类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E7%9B%B8%E5%85%B3%E5%86%85%E5%AE%B9%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B"
                           class="">相关内容卡片类型</a></td>
                </tr>
                <tr>
                    <td>reserve</td>
                    <td>obj</td>
                    <td>预约信息</td>
                    <td><code>ADDITIONAL_TYPE_RESERVE</code>类型独有</td>
                </tr>
                <tr>
                    <td>goods</td>
                    <td>obj</td>
                    <td>商品内容</td>
                    <td><code>ADDITIONAL_TYPE_GOODS</code>类型独有</td>
                </tr>
                <tr>
                    <td>vote</td>
                    <td>obj</td>
                    <td>投票信息</td>
                    <td><code>ADDITIONAL_TYPE_VOTE</code>类型独有</td>
                </tr>
                <tr>
                    <td>ugc</td>
                    <td>obj</td>
                    <td>视频信息</td>
                    <td><code>ADDITIONAL_TYPE_UGC</code>类型独有</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>button</td>
                    <td>obj</td>
                    <td>按钮内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>左侧封面图</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc1</td>
                    <td>str</td>
                    <td>描述1</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc2</td>
                    <td>str</td>
                    <td>描述2</td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td>卡片头文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>相关id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_type</td>
                    <td>str</td>
                    <td>子类型</td>
                    <td><code>game</code><br><code>decoration</code><br><code>ogv</code></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>卡片标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_style</td>
                    <td>obj</td>
                    <td>跳转类型</td>
                    <td><code>game</code>和<code>decoration</code>类型特有</td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td></td>
                    <td>1：<code>game</code>和<code>decoration</code>类型<br>2：<code>ogv</code>类型</td>
                </tr>
                <tr>
                    <td>check</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>ogv</code>类型特有</td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>uncheck</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>ogv</code>类型特有</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-jump-style对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-jump-style对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>jump_style</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td>game：<code>进入</code><br>decoration：<code>去看看</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-check对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-check对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>check</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>按钮图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>ogv</code>：已追剧</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-uncheck对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-uncheck对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>uncheck</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>按钮图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>ogv</code>：追剧</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>button</td>
                    <td>obj</td>
                    <td>按钮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc1</td>
                    <td>obj</td>
                    <td>预约时间</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc2</td>
                    <td>obj</td>
                    <td>预约观看量</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>reserve_total</td>
                    <td>num</td>
                    <td>预约人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>num</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>state</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>stype</td>
                    <td>num</td>
                    <td><code>1</code> <code>2</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>预约标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>up_mid</td>
                    <td>num</td>
                    <td>预约发起人UID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc3</td>
                    <td>obj</td>
                    <td>预约有奖信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>check</td>
                    <td>obj</td>
                    <td>已预约状态显示内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td>预约状态</td>
                    <td>1：未预约，使用<code>uncheck</code><br>2：已预约，使用<code>check</code></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>1：视频预约，使用<code>jump_style</code><br>2：直播预约，使用<code>check</code>和<code>uncheck</code></td>
                </tr>
                <tr>
                    <td>uncheck</td>
                    <td>obj</td>
                    <td>未预约状态显示内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_style</td>
                    <td>obj</td>
                    <td>跳转按钮</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-check对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-check对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>check</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>已预约</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-uncheck对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-uncheck对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>uncheck</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>显示图标URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>toast</td>
                    <td>str</td>
                    <td>预约成功显示提示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable</td>
                    <td>num</td>
                    <td>是否不可预约</td>
                    <td>1：是</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-jump-style对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-jump-style对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>jump_style</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>去观看</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc1对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc1对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc1</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>0：<code>视频预约</code> <code>11-05 20:00 直播</code> <code>预计今天
                        17:05发布</code><br>1：<code>直播中</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc2对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc2对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc2</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td><code>2人预约</code><br><code>743观看</code><br><code>1.0万人看过</code><br><code>2151人气</code></td>
                </tr>
                <tr>
                    <td>visible</td>
                    <td>bool</td>
                    <td>是否显示</td>
                    <td>true：显示文案<br>false：显示已结束</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc3对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc3对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc3</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>开奖信息跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>奖品信息显示文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>goods</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>head_icon</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td>卡片头显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>商品信息列表</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象-items数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象-items数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>goods</code>对象
                -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>brief</td>
                    <td>str</td>
                    <td>商品副标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>商品封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>str</td>
                    <td>商品ID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_desc</td>
                    <td>str</td>
                    <td>跳转按钮显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>商品名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>price</td>
                    <td>str</td>
                    <td>商品价格</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-vote对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-vote对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>vote</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>choice_cnt</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>default_share</td>
                    <td>num</td>
                    <td>是否默认勾选<code>同时分享至动态</code></td>
                    <td>1：勾选</td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>投票标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>end_time</td>
                    <td>num</td>
                    <td>剩余时间</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>join_num</td>
                    <td>num</td>
                    <td>已参与人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>null</td>
                    <td><code>null</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>uid</td>
                    <td>num</td>
                    <td>发起人UID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>vote_id</td>
                    <td>num</td>
                    <td>投票ID</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-ugc对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-ugc对象" aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>additional</code>对象 -&gt; <code>ugc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_second</td>
                    <td>str</td>
                    <td>播放量与弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration</td>
                    <td>str</td>
                    <td>视频长度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>视频跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>multi_line</td>
                    <td>bool</td>
                    <td><code>true</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>desc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>动态的文字内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>orig_text</td>
                    <td>str</td>
                    <td>原始文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>替换后的文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>节点类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>emoji</td>
                    <td>obj</td>
                    <td>表情信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>str</td>
                    <td>关联id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>goods</td>
                    <td>obj</td>
                    <td>商品信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>icon_name</td>
                    <td>str</td>
                    <td>图标名称</td>
                    <td><code>taobao</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
                -&gt; <code>emoji</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>表情图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>表情尺寸</td>
                    <td><code>1</code> <code>2</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>表情的文字代码</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>表情类型</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-goods对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-goods对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
                -&gt; <code>goods</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象" tabindex="-1"><a class="header-anchor"
                                                                                                          href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象"
                                                                                                          aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>major</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>动态主体类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%8A%A8%E6%80%81%E4%B8%BB%E4%BD%93%E7%B1%BB%E5%9E%8B"
                           class="">动态主体类型</a></td>
                </tr>
                <tr>
                    <td>ugc_season</td>
                    <td>obj</td>
                    <td>合集信息</td>
                    <td><code>MAJOR_TYPE_UGC_SEASON</code></td>
                </tr>
                <tr>
                    <td>article</td>
                    <td>obj</td>
                    <td>专栏类型</td>
                    <td><code>MAJOR_TYPE_ARTICLE</code></td>
                </tr>
                <tr>
                    <td>draw</td>
                    <td>obj</td>
                    <td>带图动态</td>
                    <td><code>MAJOR_TYPE_DRAW</code></td>
                </tr>
                <tr>
                    <td>archive</td>
                    <td>obj</td>
                    <td>视频信息</td>
                    <td><code>MAJOR_TYPE_ARCHIVE</code></td>
                </tr>
                <tr>
                    <td>live_rcmd</td>
                    <td>obj</td>
                    <td>直播状态</td>
                    <td><code>MAJOR_TYPE_LIVE_RCMD</code></td>
                </tr>
                <tr>
                    <td>common</td>
                    <td>obj</td>
                    <td>一般类型</td>
                    <td><code>MAJOR_TYPE_COMMON</code></td>
                </tr>
                <tr>
                    <td>pgc</td>
                    <td>obj</td>
                    <td>剧集信息</td>
                    <td><code>MAJOR_TYPE_PGC</code></td>
                </tr>
                <tr>
                    <td>courses</td>
                    <td>obj</td>
                    <td>课程信息</td>
                    <td><code>MAJOR_TYPE_COURSES</code></td>
                </tr>
                <tr>
                    <td>music</td>
                    <td>obj</td>
                    <td>音频信息</td>
                    <td><code>MAJOR_TYPE_MUSIC</code></td>
                </tr>
                <tr>
                    <td>opus</td>
                    <td>obj</td>
                    <td>图文动态</td>
                    <td><code>MAJOR_TYPE_OPUS</code></td>
                </tr>
                <tr>
                    <td>live</td>
                    <td>obj</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>none</td>
                    <td>obj</td>
                    <td>动态失效</td>
                    <td><code>MAJOR_TYPE_NONE</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>aid</td>
                    <td>num</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>视频简介</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable_preview</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration_text</td>
                    <td>str</td>
                    <td>时长</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-badge对象" tabindex="-1">
                <a class="header-anchor"
                   href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-badge对象"
                   aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
                -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-stat对象" tabindex="-1">
                <a class="header-anchor"
                   href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-stat对象"
                   aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
                -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-article对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-article对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>article</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>covers</td>
                    <td>array</td>
                    <td>封面图数组</td>
                    <td>最多三张</td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>文章摘要</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>文章CV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>文章跳转地址</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>文章阅读量</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>文章标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>draw</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>对应相簿id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>图片信息列表</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象-items数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象-items数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>draw</code>对象 -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>height</td>
                    <td>num</td>
                    <td>图片高度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>图片大小</td>
                    <td>单位KB</td>
                </tr>
                <tr>
                    <td>src</td>
                    <td>str</td>
                    <td>图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>tags</td>
                    <td>array</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>width</td>
                    <td>num</td>
                    <td>图片宽度</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>aid</td>
                    <td>str</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>bvid</td>
                    <td>str</td>
                    <td>视频BVID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>视频简介</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable_preview</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration_text</td>
                    <td>str</td>
                    <td>视频长度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-stat对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-stat对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象 -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live-rcmd对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live-rcmd对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>live_rcmd</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>content</td>
                    <td>str</td>
                    <td>直播间内容JSON</td>
                    <td></td>
                </tr>
                <tr>
                    <td>reserve_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>common</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>biz_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>左侧图片封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>右侧描述信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转地址</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>sketch_id</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>右侧标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>common</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>epid</td>
                    <td>num</td>
                    <td>分集EpId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>season_id</td>
                    <td>num</td>
                    <td>剧集SeasonId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_type</td>
                    <td>num</td>
                    <td>剧集类型</td>
                    <td>1：番剧<br>2：电影<br>3：纪录片<br>4：国创<br>5：电视剧<br>6：漫画<br>7：综艺</td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>2</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-stat对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-stat对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象 -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>courses</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>封面图URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>更新状态描述</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>课程id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_title</td>
                    <td>str</td>
                    <td>课程副标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>课程标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>courses</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-music对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-music对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>music</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>音频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>音频AUID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>音频分类</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>音频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>opus</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>fold_action</td>
                    <td>array</td>
                    <td>展开收起</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pics</td>
                    <td>array</td>
                    <td>图片信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>summary</td>
                    <td>obj</td>
                    <td>动态内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>动态标题</td>
                    <td>没有标题时为null</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象-summary对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象-summary对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>opus</code>对象 -&gt; <code>summary</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>和<code>desc</code>对象中的<code>rich_text_nodes</code>数组结构一样</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>评论内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>live</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>直播封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_first</td>
                    <td>str</td>
                    <td>直播主分区名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_second</td>
                    <td>str</td>
                    <td>观看人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>直播间id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>直播间跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>live_state</td>
                    <td>num</td>
                    <td>直播状态</td>
                    <td>0：直播结束<br>1：正在直播</td>
                </tr>
                <tr>
                    <td>reserve_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>直播间标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>live</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-none对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-none对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>none</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>tips</td>
                    <td>str</td>
                    <td>动态失效显示文案</td>
                    <td>deprecated?</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-topic对象" tabindex="-1"><a class="header-anchor"
                                                                                                          href="#data对象-items数组中的对象-modules对象-module-dynamic对象-topic对象"
                                                                                                          aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>topic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>话题id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>话题名称</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-more对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_more</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>three_point_items</td>
                    <td>array</td>
                    <td>右上角三点菜单</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>显示文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>类型</td>
                    <td></td>
                </tr>
                <tr>
                    <td>modal</td>
                    <td>obj</td>
                    <td>弹出框信息</td>
                    <td>删除动态时弹出</td>
                </tr>
                <tr>
                    <td>params</td>
                    <td>obj</td>
                    <td>参数</td>
                    <td>置顶/取消置顶时使用</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-modal对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-modal对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象 -&gt;
                <code>modal</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cancel</td>
                    <td>str</td>
                    <td>取消按钮</td>
                    <td><code>我点错了</code></td>
                </tr>
                <tr>
                    <td>confirm</td>
                    <td>str</td>
                    <td>确认按钮</td>
                    <td><code>删除</code></td>
                </tr>
                <tr>
                    <td>content</td>
                    <td>str</td>
                    <td>提示内容</td>
                    <td><code>确定要删除此条动态吗？</code></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>标题</td>
                    <td><code>删除动态</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-params对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-params对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象 -&gt;
                <code>params</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>dynamic_id</td>
                    <td>str</td>
                    <td>当前动态ID</td>
                    <td>deprecated?</td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>bool</td>
                    <td>当前动态是否处于置顶状态</td>
                    <td>deprecated?</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-stat对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>comment</td>
                    <td>obj</td>
                    <td>评论数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forward</td>
                    <td>obj</td>
                    <td>转发数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>like</td>
                    <td>obj</td>
                    <td>点赞数据</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-comment对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-stat对象-comment对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>comment</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>评论数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>hidden</td>
                    <td>bool</td>
                    <td>是否隐藏</td>
                    <td>直播类型动态会隐藏回复功能</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-forward对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-stat对象-forward对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>forward</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>转发数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-like对象" tabindex="-1"><a class="header-anchor"
                                                                                                      href="#data对象-items数组中的对象-modules对象-module-stat对象-like对象"
                                                                                                      aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>like</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>点赞数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>bool</td>
                    <td>当前用户是否点赞</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象" tabindex="-1"><a class="header-anchor"
                                                                                                    href="#data对象-items数组中的对象-modules对象-module-interaction对象"
                                                                                                    aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_interaction</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>信息列表</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>obj</td>
                    <td>点赞/评论信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>0：点赞信息<br>1：评论信息</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>评论内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>orig_text</td>
                    <td>str</td>
                    <td>原始文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>str</td>
                    <td>关联ID</td>
                    <td>用户UID</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>替换后文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>富文本节点类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>emoji</td>
                    <td>obj</td>
                    <td>表情信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象 -&gt; <code>emoji</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>表情图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>表情尺寸</td>
                    <td><code>1</code> <code>2</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>表情的文字代码</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>表情类型</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-fold对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-fold对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_fold</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>ids</td>
                    <td>array</td>
                    <td>被折叠的动态id列表</td>
                    <td></td>
                </tr>
                <tr>
                    <td>statement</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td>例：展开x条相关动态</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>users</td>
                    <td>array</td>
                    <td><code>空数组</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dispute对象" tabindex="-1"><a class="header-anchor"
                                                                                                href="#data对象-items数组中的对象-modules对象-module-dispute对象"
                                                                                                aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dispute</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>提醒文案</td>
                    <td>例：视频内含有危险行为，请勿模仿</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-tag对象" tabindex="-1"><a class="header-anchor"
                                                                                            href="#data对象-items数组中的对象-modules对象-module-tag对象"
                                                                                            aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt;
                <code>module_tag</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>'置顶'</td>
                    <td>置顶动态出现这个对象，否则没有</td>
                </tr>
                </tbody>
            </table>
        </div>

        """
        api = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
        headers = self.headers
        data = {
            "offset": "",
            "host_mid": host_mid
        }
        dynamic = requests.get(api, headers=headers, params=data).json()
        if not all:
            dynamics = dynamic["data"]["items"]
        else:
            dynamics = dynamic["data"]["items"]
            while dynamic["data"]["has_more"]:
                data["offset"] = dynamic["data"]["offset"]
                dynamic = requests.get(api, headers=headers, params=data).json()
                for i in dynamic["data"]["items"]:
                    if i not in dynamics:
                        dynamics.append(i)
        dynamic = dynamics
        return dynamic

    def get_user_info(self) -> dict:
        """
        获得个人基础信息
        """
        url = "https://api.live.bilibili.com/xlive/web-ucenter/user/get_user_info"
        headers = self.headers
        response = requests.get(url, headers=headers).json()
        return response['data']

    def interface_nav(self) -> dict:
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

    def getRoomHighlightState(self):
        """
        获取直播间号
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/highlight/getRoomHighlightState"
        headers = self.headers
        room_id = requests.get(api, headers=headers).json()["data"]["room_id"]
        return room_id

    def GetEmoticons(self, roomid: int):
        """
        获取表情
        @return:
        @rtype: list
        """
        api = "https://api.live.bilibili.com/xlive/web-ucenter/v2/emoticon/GetEmoticons"
        headers = self.headers
        params = {
            "platform": "pc",
            "room_id": roomid
        }
        Emoticons = requests.get(api, headers=headers, params=params).json()["data"]["data"]
        return Emoticons

    def getDanmuInfo(self, roomid: int) -> dict:
        """
        获取信息流认证秘钥
        @param roomid: 直播间真实id
        @return:
        <p>根对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>code</td><td>num</td><td>返回值</td><td>0：成功<br>65530：token错误（登录错误）<br>1：错误<br>60009：分区不存在<br><strong>（其他错误码有待补充）</strong></td></tr><tr><td>message</td><td>str</td><td>错误信息</td><td>默认为空</td></tr><tr><td>ttl</td><td>num</td><td>1</td><td></td></tr><tr><td>data</td><td>obj</td><td>信息本体</td><td></td></tr></tbody></table>
        <p><code>data</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>group</td><td>str</td><td>live</td><td></td></tr><tr><td>business_id</td><td>num</td><td>0</td><td></td></tr><tr><td>refresh_row_factor</td><td>num</td><td>0.125</td><td></td></tr><tr><td>refresh_rate</td><td>num</td><td>100</td><td></td></tr><tr><td>max_delay</td><td>num</td><td>5000</td><td></td></tr><tr><td>token</td><td>str</td><td>认证秘钥</td><td></td></tr><tr><td>host_list</td><td>array</td><td>信息流服务器节点列表</td><td></td></tr></tbody></table>
        <p><code>host_list</code>数组中的对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>host</td><td>str</td><td>服务器域名</td><td></td></tr><tr><td>port</td><td>num</td><td>tcp端口</td><td></td></tr><tr><td>wss_port</td><td>num</td><td>wss端口</td><td></td></tr><tr><td>ws_port</td><td>num</td><td>ws端口</td><td></td></tr></tbody></table>
        """
        headers = self.headers
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo?id={roomid}'
        response = requests.get(url, headers=headers).json()
        return response

    def getRoomNews(self):
        # 获取直播公告
        headers = self.headers
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getRoomNews"
        params = {
            'room_id': self.getRoomHighlightState(),
            'uid': cookie2dict(self.headers["cookie"])["DedeUserID"]
        }
        getRoomNews_ReturnValue = requests.get(api, headers=headers, params=params).json()
        return getRoomNews_ReturnValue["data"]["content"]


class CsrfAuthentication:
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
            "room_id": master(self.cookie).getRoomHighlightState(),
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
            "room_id": master(self.cookie).getRoomHighlightState(),
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
            "room_id": master(self.cookie).getRoomHighlightState(),
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
            'room_id': master(self.cookie).getRoomHighlightState(),
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
            'room_id': master(self.cookie).getRoomHighlightState(),
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
def logInTry(configPath: Path, uid: Optional[int]):
    try:
        BUCF = BilibiliUserLogsIn2ConfigFile(configPath=configPath)
        uid = str(uid)
        logSave(0, f"尝试登录用户: {uid}")
        # 验证cookies完整性
        cookies = BUCF.getCookies(int(uid))
        if cookies is None:
            raise ValueError(f"缺少该用户: {uid}")
        required_keys = {"DedeUserID", "SESSDATA", "bili_jct"}
        missing = required_keys - cookies.keys()
        if missing:
            raise ValueError(f"cookies缺少必要字段: {', '.join(missing)}")
        isLogin = master(dict2cookie(cookies)).interface_nav()["isLogin"]
        if not isLogin:
            logSave(3, f"用户 {uid} 的cookies已过期")
            return False
        BUCF.updateUser(cookies)
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
    BUCF = BilibiliUserLogsIn2ConfigFile(globalVariableOfData.scripts_config_filepath)
    UserListDict = BUCF.getUsers()
    code_ = globalVariableOfData.loginQrCode_returnValue
    poll_ = poll(globalVariableOfData.loginQrCode_key)
    globalVariableOfData.loginQrCode_returnValue = poll_['code']
    logIn2QRCode2ReturnInformation4code = {
        0: "登录成功",
        86101: "未扫码",
        86090: "二维码已扫码未确认",
        86038: "二维码已失效",
    }
    # 二维码扫描登陆状态改变时，输出改变后状态
    logSave(2, str(logIn2QRCode2ReturnInformation4code[globalVariableOfData.loginQrCode_returnValue])) if code_ != globalVariableOfData.loginQrCode_returnValue else None
    if globalVariableOfData.loginQrCode_returnValue == 0 or globalVariableOfData.loginQrCode_returnValue == 86038:
        globalVariableOfData.LoginQRCodePillowImg = None
        # 二维码扫描登陆状态为成功或者超时时获取cookies结束[轮询二维码扫描登陆状态]
        cookies = poll_['cookies']
        if cookies:
            # 获取登陆账号cookies中携带的uid
            uid = int(cookies['DedeUserID'])
            if str(uid) in UserListDict.values():
                logSave(1, "已有该用户，正在更新用户登录信息")
                BUCF.updateUser(cookies, False)
            else:
                BUCF.addUser(cookies)
                logSave(0, "添加用户成功")
                # 启动帧计时器，更新用户列表
                logSave(0, "启动帧计时器，更新用户列表")
        else:
            logSave(0, "添加用户失败")
        # 结束计时器
        obs.remove_current_callback()


def qrAddUser():
    """
    扫码登陆记录用户cookies
    """
    # 申请登录二维码
    url8qrcode_key = generate()
    # 获取二维码url
    url = url8qrcode_key['url']
    logSave(0, f"获取登录二维码链接{url}")
    # 获取二维码key
    globalVariableOfData.loginQrCode_key = url8qrcode_key['qrcode_key']
    logSave(0, f"获取登录二维码密钥{globalVariableOfData.loginQrCode_key}")
    # 获取二维码对象
    qr = qr2str_b64_PilImg4dict(url)
    # 获取登录二维码的pillow img实例
    globalVariableOfData.LoginQRCodePillowImg = qr["img"]
    # 输出二维码图形字符串
    logSave(2, qr["str"])
    logSave(0, f"字符串二维码已输出，如果乱码或者扫描不上，建议点击 按钮【显示登录二维码图片】")
    # 获取二维码扫描登陆状态
    globalVariableOfData.loginQrCode_returnValue = poll(globalVariableOfData.loginQrCode_key)['code']
    logIn2QRCode2ReturnInformation4code = {
        0: "登录成功",
        86101: "未扫码",
        86090: "二维码已扫码未确认",
        86038: "二维码已失效",
    }
    logSave(0, f"开始轮询登录状态")
    # 轮询登录状态
    logSave(2, str(logIn2QRCode2ReturnInformation4code[globalVariableOfData.loginQrCode_returnValue]))
    # 开始计时器
    obs.timer_add(check_poll, 1000)


# end

# ================================================================================================


# -----------------------------------------------------------
# OBS Script Functions                                      -
# -----------------------------------------------------------

# --- 设置默认值
def script_defaults(settings):  # 设置其默认值
    """
    调用以设置与脚本关联的默认设置(如果有的话)。为了设置其默认值，您通常会调用默认值函数。
    :param settings:与脚本关联的设置。
    """
    # 路径变量
    # #脚本数据保存目录
    globalVariableOfData.scripts_data_dirpath = f"{script_path()}bilibili-live"
    logSave(0, f"脚本用户数据文件夹路径：{globalVariableOfData.scripts_data_dirpath}")
    # #脚本用户数据路径
    globalVariableOfData.scripts_config_filepath = Path(globalVariableOfData.scripts_data_dirpath) / "config.json"
    logSave(0, f"脚本用户数据路径：{globalVariableOfData.scripts_config_filepath}")

    globalVariableOfData.networkConnectionStatus = check_network_connection()
    if not globalVariableOfData.networkConnectionStatus:
        logSave(1, f"\n======= 最终结果: 网络{'可用' if globalVariableOfData.networkConnectionStatus else '不可用'} =======\n")
        return None
    if globalVariableOfData.accountAvailabilityDetectionSwitch:
        logSave(1, f"执行账号可用性检测")
        # 创建用户配置文件实例
        BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
        # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
        userInterface_navByUid4Dict = {uid: master(dict2cookie(BULC.getCookies(int(uid)))).interface_nav() for uid in [x for x in BULC.getUsers().values() if x]}
        # 获取 用户配置文件 中 每一个 用户 的 可用性
        userIsLoginByUid4Dict = {uid: userInterface_navByUid4Dict[uid]["isLogin"] for uid in userInterface_navByUid4Dict}
        # 删除 用户配置文件 中 不可用 用户
        [BULC.deleteUser(int(uid)) for uid in userIsLoginByUid4Dict if not userIsLoginByUid4Dict[uid]]
        # 获取 用户配置文件 中 每一个 可用 用户 的 昵称
        AllUnameByUid4Dict = {uid: userInterface_navByUid4Dict[uid]["uname"] for uid in userIsLoginByUid4Dict if userIsLoginByUid4Dict[uid]}
        """
        全部账户的数据
        {uid: uname}
        """
        # 输出日志
        [logSave(1, f"账号：{uid} {'不可用，已删除' if not userIsLoginByUid4Dict[uid] else '可用'}") for uid in userIsLoginByUid4Dict]
        logSave(1, f"可用账号：{str(AllUnameByUid4Dict)}")
        globalVariableOfData.accountAvailabilityDetectionSwitch = False
        logSave(1, f"关闭账号可用性检测")

    # 创建用户配置文件实例
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
    userInterface_navByUid4Dict = {uid: master(dict2cookie(BULC.getCookies(int(uid)))).interface_nav() for uid in [x for x in BULC.getUsers().values() if x]}
    # 获取 用户配置文件 中 每一个 用户 的 昵称
    AllUnameByUid4Dict = {uid: userInterface_navByUid4Dict[uid]["uname"] for uid in userInterface_navByUid4Dict}
    logSave(0, f"载入账号：{str(AllUnameByUid4Dict)}")
    DefaultUserInterfaceNav = master(dict2cookie(BULC.getCookies())).interface_nav() if BULC.getCookies() else None  # 获取 '默认账户' 导航栏用户信息
    DefaultUname = DefaultUserInterfaceNav["uname"] if BULC.getCookies() else None  # 获取默认账号的昵称
    """
    默认用户config["DefaultUser"]的昵称
    没有则为None
    """
    logSave(0, f"用户：{DefaultUname} 已登录" if BULC.getCookies() else f"未登录账号")
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 设置 只读文本框【登录状态】 可见状态
    GlobalVariableOfTheControl.login_status_textBox_visible = True
    logSave(0, f"设置 只读文本框【登录状态】 可见状态：{str(GlobalVariableOfTheControl.login_status_textBox_visible)}")
    # 设置 只读文本框【登录状态】 可用状态
    GlobalVariableOfTheControl.login_status_textBox_enabled = True
    logSave(0, f"设置 只读文本框【登录状态】 可用状态：{str(GlobalVariableOfTheControl.login_status_textBox_enabled)}")
    # 设置 只读文本框【登录状态】 类型
    GlobalVariableOfTheControl.login_status_textBox_type = obs.OBS_TEXT_INFO_NORMAL if BULC.getCookies() else obs.OBS_TEXT_INFO_WARNING
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 设置 只读文本框【登录状态】 类型：{textBox_type_name4textBox_type[GlobalVariableOfTheControl.login_status_textBox_type]}")
    # 设置 只读文本框【登录状态】 内容
    GlobalVariableOfTheControl.login_status_textBox_string = f'{DefaultUname} 已登录' if BULC.getCookies() else '未登录，请登录后点击【更新账号列表】'
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 设置 只读文本框【登录状态】 内容：{GlobalVariableOfTheControl.login_status_textBox_string}")

    # 设置 组合框【用户】 可见状态
    GlobalVariableOfTheControl.uid_comboBox_visible = True
    logSave(0, f"设置 组合框【用户】 可见状态：{str(GlobalVariableOfTheControl.uid_comboBox_visible)}")
    # 设置 组合框【用户】 可用状态
    GlobalVariableOfTheControl.uid_comboBox_enabled = True
    logSave(0, f"设置 组合框【用户】 可用状态：{str(GlobalVariableOfTheControl.uid_comboBox_enabled)}")
    # 设置 组合框【用户】 的数据字典
    GlobalVariableOfTheControl.uid_comboBox_dict = {uid or '-1': AllUnameByUid4Dict.get(uid, '添加或选择一个账号登录') for uid in BULC.getUsers().values()}
    logSave(0, f"设置 组合框【用户】 数据字典：{str(GlobalVariableOfTheControl.uid_comboBox_dict)}")
    # 设置 组合框【用户】 默认显示内容
    GlobalVariableOfTheControl.uid_comboBox_string = DefaultUname if BULC.getCookies() else '添加或选择一个账号登录'
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 设置 组合框【用户】 内容：{GlobalVariableOfTheControl.uid_comboBox_string}")
    # 设置 组合框【用户】 默认显示内容 的 列表值
    GlobalVariableOfTheControl.uid_comboBox_value = BULC.getUsers()[0] if BULC.getCookies() else '-1'
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 设置 组合框【用户】 列表值：{GlobalVariableOfTheControl.uid_comboBox_value}")

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
    GlobalVariableOfTheControl.qr_code_add_account_button_visible = True
    logSave(0, f"设置 按钮【二维码添加账户】 可见状态：{str(GlobalVariableOfTheControl.qr_code_add_account_button_visible)}")
    # 设置 按钮【二维码添加账户】 可用状态
    GlobalVariableOfTheControl.qr_code_add_account_button_enabled = True
    logSave(0, f"设置 按钮【二维码添加账户】 可用状态：{str(GlobalVariableOfTheControl.qr_code_add_account_button_enabled)}")

    # 设置 按钮【显示二维码图片】 可见状态
    GlobalVariableOfTheControl.display_qr_code_picture_button_visible = True
    logSave(0, f"设置 按钮【显示二维码图片】 可见状态：{str(GlobalVariableOfTheControl.display_qr_code_picture_button_visible)}")
    # 设置 按钮【显示二维码图片】 可用状态
    GlobalVariableOfTheControl.display_qr_code_picture_button_enabled = True
    logSave(0, f"设置 按钮【显示二维码图片】 可用状态：{str(GlobalVariableOfTheControl.display_qr_code_picture_button_enabled)}")

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
    GlobalVariableOfTheControl.logout_button_visible = True if AllUnameByUid4Dict and BULC.getCookies() else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，是否登录：{str(bool(BULC.getCookies()))}，设置 按钮【登出账号】 可见状态：{str(GlobalVariableOfTheControl.logout_button_visible)}")
    # 设置 按钮【登出账号】 可用状态
    GlobalVariableOfTheControl.logout_button_enabled = True if AllUnameByUid4Dict and BULC.getCookies() else False
    logSave(0, f"根据 是否有账户：{str(bool(AllUnameByUid4Dict))}，是否登录：{str(bool(BULC.getCookies()))}，设置 按钮【登出账号】 可用状态：{str(GlobalVariableOfTheControl.logout_button_enabled)}")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 创建用户配置文件实例
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    # 获取'默认账户'获取用户对应的直播间状态
    RoomInfoOld = getRoomInfoOld(int(BULC.getUsers()[0])) if BULC.getCookies() else {}
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 获取 登录账户 对应的直播间状态：数据长度为{len(RoomInfoOld)}")
    # 获取 默认用户 的 直播间状态
    DefaultRoomStatus = RoomInfoOld["roomStatus"] if BULC.getCookies() else None
    """
    登录的用户的直播间存在状态
    """
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 获取 登录账户 是否有直播间：{DefaultRoomStatus}")
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
    RoomBaseInfo = getRoomBaseInfo(DefaultRoomid) if DefaultRoomStatus else {}
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
    parentLiveAreaNameByid4dict = {str(AreaObj["id"]): AreaObj["name"] for AreaObj in getAreaObjList()} | {} if DefaultArea else {"-1": "请选择一级分区"}
    logSave(0, f"根据 登录账户 当前直播间分区数据存在：{bool(DefaultArea)} 获取 直播间父分区数据{parentLiveAreaNameByid4dict}")
    subLiveAreaNameByid4dict = {str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in getsubLiveAreaObjList(DefaultArea['id'])} if DefaultArea else {"-1": "请选择一级分区"}
    logSave(0, f"根据 登录账户 当前直播间分区数据存在：{bool(DefaultArea)} 获取 登录账户 当前父分区对应的子分区数据{subLiveAreaNameByid4dict}")

    # 设置 只读文本框【直播间状态】 可见状态
    GlobalVariableOfTheControl.room_status_textBox_visible = True
    logSave(0, f"设置 按钮【查看直播间封面】 可见状态：{str(GlobalVariableOfTheControl.room_status_textBox_visible)}")
    # 设置 只读文本框【直播间状态】 可用状态
    GlobalVariableOfTheControl.room_status_textBox_enabled = True
    logSave(0, f"设置 按钮【查看直播间封面】 可用状态：{str(GlobalVariableOfTheControl.room_status_textBox_enabled)}")
    # 设置 只读文本框【直播间状态】 的类型
    GlobalVariableOfTheControl.room_status_textBox_type = (obs.OBS_TEXT_INFO_NORMAL if bool(DefaultRoomStatus) else obs.OBS_TEXT_INFO_WARNING) if BULC.getCookies() else obs.OBS_TEXT_INFO_ERROR
    logSave(0, f"根据 登录状态：{bool(BULC.getCookies())} 和 直播间存在：{bool(DefaultRoomStatus)} 设置 只读文本框【直播间状态】 的类型{textBox_type_name4textBox_type[GlobalVariableOfTheControl.room_status_textBox_type]}")
    # 设置 只读文本框【直播间状态】 的内容
    GlobalVariableOfTheControl.room_status_textBox_string = (f"{str(DefaultRoomid)}{'直播中' if DefaultLiveStatus else '未开播'}" if DefaultRoomStatus else "无直播间") if BULC.getCookies() else "未登录"
    logSave(0, f"根据 登录状态：{bool(BULC.getCookies())} 和 直播间存在：{bool(DefaultRoomStatus)} 设置 只读文本框【直播间状态】 的内容{GlobalVariableOfTheControl.room_status_textBox_type}")

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
    GlobalVariableOfTheControl.room_cover_fileDialogBox_string = "" if bool(GlobalVariableOfTheControl.liveRoom_title_textBox_visible) else ""
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
    GlobalVariableOfTheControl.liveRoom_news_textBox_string = master(dict2cookie(BULC.getCookies())).getRoomNews() if bool(DefaultRoomStatus) else ""
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
    GlobalVariableOfTheControl.jump_blive_web_button_visible = False
    logSave(0, f"设置 url按钮【跳转直播间后台网页】 可见状态：{str(bool(GlobalVariableOfTheControl.jump_blive_web_button_visible))}")
    # 设置 url按钮【跳转直播间后台网页】 可用状态
    GlobalVariableOfTheControl.jump_blive_web_button_enabled = False
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
    if not globalVariableOfData.networkConnectionStatus:
        return "<font color=yellow>网络不可用</font>"

    t = ('<html lang="zh-CN"><body><pre>\
本插件基于python3<br>\
    如果未安装python3，请前往<br>\
        <a href="https://www.python.org/">python官网</a><br>\
        或者<br>\
        <a href="https://python.p2hp.com/">python中文网 官网</a>下载安装<br>\
        不同操作系统请查看<br>\
            菜鸟教程<a href="https://www.runoob.com/python3/python3-install.html">Python3 环境搭建</a><br>\
<font color=yellow>!脚本路径中尽量不要有中文</font><br>\
<font color=green size=4>请在认为完成操作后点击<font color="white" size=5>⟳</font>重新载入插件</font><br>\
配置cookie：<br>\
<font color=yellow>！请看着脚本日志操作</font><br>\
扫描配置cookie请 提前增加<br>\
   脚本日志窗口 宽高<br>\
手动配置cookie请前往<br>\
   <a href="https://link.bilibili.com/p/center/index#/my-room/start-live">B站直播设置后台</a> 使用<br>\
       浏览器的开发人员工具获取cookie<br><br>\
<font color="#ee4343">【cookie！为账号的{极重要}的隐私信息!】</font><br>\
<font color="#ee4343">【！不要泄露给他人!】</font><br>\
<br>\
如果报错：<br>\
   请关闭梯子和加速器<br>\
   Windows请尝试使用<font color="#ee4343">管理员</font>权限运行obs<br>\
   其它系统请联系开发者<br>\
</pre></body></html>')
    t = ('<html lang="zh-CN"><body><pre>\
本插件基于<font color="#ee4343" size=5>python3.10</font><br>\
<font color=yellow>!脚本路径中尽量不要有中文</font><br>\
<font color="white" size=5>⟳</font><font color=green size=4>为重新载入插件按钮</font><br>\
如果报错：<br>\
   关闭梯子或加速器<br>\
   Windows请尝试使用<font color="#ee4343">管理员权限</font>运行obs<br>\
   其它问题请前往<a href="https://github.com/lanyangyin/OBSscripts-bilibili-live/issues">Github</a>提问<br>\
</pre></body></html>')
    return t


# --- 一个名为script_load的函数将在启动时调用
def script_load(settings):
    """
    在脚本启动时调用与脚本相关的特定设置。所提供的设置参数通常不用于由用户设置的设置;
    相反，该参数用于脚本中可能使用的任何额外的内部设置数据。
    :param settings:与脚本关联的设置。
    """
    # obs_data_t 类型的数据对象。这个数据对象可以用来存储和管理设置项，例如场景、源或过滤器的配置信息
    # settings = obs.obs_data_create()
    GlobalVariableOfTheControl.current_settings = settings
    logSave(0, "已载入：bilibili_live")


# 控件状态更新时调用
def script_update(settings):
    """
    当用户更改了脚本的设置(如果有的话)时调用。
    这里更改控件属性不会实时显示，
    不要在这里控制控件的【可见】、【可用】、【值】和【名称】
    :param settings:与脚本关联的设置。
    """
    GlobalVariableOfTheControl.current_settings = settings
    logSave(0, "监测到控件数据变动")
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
    if not globalVariableOfData.networkConnectionStatus:
        return None
    props = obs.obs_properties_create()  # 创建一个 OBS 属性集对象，他将包含所有控件对应的属性对象
    # 为 分组框【配置】 建立属性集
    GlobalVariableOfTheControl.setting_props = obs.obs_properties_create()
    # 为 分组框【直播间】 建立属性集
    GlobalVariableOfTheControl.liveRoom_props = obs.obs_properties_create()
    # 为 分组框【直播】 建立属性集
    GlobalVariableOfTheControl.live_props = obs.obs_properties_create()

    # —————————————————————————————————————————————————————————————————————————————————————————————————————
    # 添加 分组框【配置】
    obs.obs_properties_add_group(props, 'setting_group', "【账号】", obs.OBS_GROUP_NORMAL, GlobalVariableOfTheControl.setting_props)

    # 添加 只读文本框【登录状态】
    GlobalVariableOfTheControl.login_status_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.setting_props, 'login_status_textBox', "登录状态：", obs.OBS_TEXT_INFO)

    # 添加 组合框【用户】
    GlobalVariableOfTheControl.uid_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.setting_props, 'uid_comboBox', '用户：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    # # 添加 组合框【用户】变动后事件
    # obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.uid_comboBox, login_buttonC)

    # 添加 按钮【登录账号】
    GlobalVariableOfTheControl.login_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "login_button", "登录账号", login_buttonC)

    # 添加 按钮【更新账号列表】
    GlobalVariableOfTheControl.update_account_list_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "update_account_list_button", "更新账号列表", updateAccountList_buttonC)

    # 添加 按钮【二维码添加账户】
    GlobalVariableOfTheControl.qr_code_add_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "qr_code_add_account_button", "二维码添加账户", qrCodeAddAccount_buttonC)

    # 添加 按钮【显示登录二维码图片】
    GlobalVariableOfTheControl.display_qr_code_picture_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "display_qr_code_picture_button", "显示登录二维码图片", show_qr_code_picture_buttonC)

    # 添加 按钮【删除账户】
    GlobalVariableOfTheControl.delete_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "delete_account_button", "删除账户", del_user_buttonC)

    # 添加 按钮【备份账户】
    GlobalVariableOfTheControl.backup_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "backup_account_button", "备份账户", backupUsers_buttonC)

    # 添加 按钮【恢复账户】
    GlobalVariableOfTheControl.restore_account_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "restore_account_button", "恢复账户", restoreUser_buttonC)

    # 添加 按钮【登出账号】
    GlobalVariableOfTheControl.logout_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.setting_props, "logout_button", "登出账号", logOut_buttonC)

    # ————————————————————————————————————————————————————————————————
    # 添加 分组框【直播间】
    obs.obs_properties_add_group(props, 'liveRoom_group', '【直播间】', obs.OBS_GROUP_NORMAL, GlobalVariableOfTheControl.liveRoom_props)

    # 添加 只读文本框【直播间状态】
    GlobalVariableOfTheControl.room_status_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.liveRoom_props, 'room_status_textBox', f'直播间状态', obs.OBS_TEXT_INFO)

    # 添加 按钮【查看直播间封面】
    GlobalVariableOfTheControl.viewLiveCover_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, 'viewLiveCover_button', f'查看直播间封面', check_roomCover_buttonC)

    # 添加 文件对话框【直播间封面】
    GlobalVariableOfTheControl.room_cover_fileDialogBox = obs.obs_properties_add_path(GlobalVariableOfTheControl.liveRoom_props, 'room_cover_fileDialogBox', f'直播间封面', obs.OBS_PATH_FILE, '*jpg *jpeg *.png', None)

    # 添加 按钮【上传直播间封面】
    GlobalVariableOfTheControl.room_cover_update_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "room_cover_update_button", "上传直播间封面", update_roomCover_buttonC)

    # 添加 普通文本框【直播间标题】
    GlobalVariableOfTheControl.liveRoom_title_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.liveRoom_props, "liveRoom_title_textBox", "直播间标题", obs.OBS_TEXT_DEFAULT)

    # 添加 按钮【更改直播间标题】
    GlobalVariableOfTheControl.change_liveRoom_title_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "change_liveRoom_title_button", "更改直播间标题", change_liveRoom_title_buttonC)

    # 添加 普通文本框【直播间公告】
    GlobalVariableOfTheControl.liveRoom_news_textBox = obs.obs_properties_add_text(GlobalVariableOfTheControl.liveRoom_props, "liveRoom_news_textBox", "直播间公告", obs.OBS_TEXT_DEFAULT)

    # 添加 按钮【更改直播间公告】
    GlobalVariableOfTheControl.change_liveRoom_news_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "change_liveRoom_news_button", "更改直播间公告", change_liveRoom_news_buttonC)

    # 添加 组合框【一级分区】
    GlobalVariableOfTheControl.parentLiveArea_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.liveRoom_props, 'parentLiveArea_comboBox', '一级分区：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    # # 添加 组合框【一级分区】变动后事件
    # obs.obs_property_set_modified_callback(GlobalVariableOfTheControl.parentLiveArea_comboBox, start_area1_buttonC)

    # 添加 按钮【确认一级分区】
    GlobalVariableOfTheControl.parentLiveArea_true_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "parentLiveArea_true_button", "确认一级分区", start_area1_buttonC)

    # 添加 组合框【二级分区】
    GlobalVariableOfTheControl.subLiveArea_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.liveRoom_props, 'subLiveArea_comboBox', '二级分区：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)

    # 添加 按钮【「确认分区」】
    GlobalVariableOfTheControl.subLiveArea_true_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, "subLiveArea_true_button", "「确认分区」", lambda ps, p: start_area_buttonC())

    # 添加 url按钮【跳转直播间后台网页】
    GlobalVariableOfTheControl.jump_blive_web_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.liveRoom_props, 'jump_blive_web_button', f'跳转直播间后台网页', jump_Blive_web_buttonC)

    # ————————————————————————————————————————————————————————————————
    # 添加 分组框【直播】
    obs.obs_properties_add_group(props, 'live_group', '【直播】', obs.OBS_GROUP_NORMAL, GlobalVariableOfTheControl.live_props)

    # 添加 组合框【直播平台】
    GlobalVariableOfTheControl.live_streaming_platform_comboBox = obs.obs_properties_add_list(GlobalVariableOfTheControl.live_props, 'live_streaming_platform_comboBox', '直播平台：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)

    # 添加 按钮【开始直播并复制推流码】
    GlobalVariableOfTheControl.start_live_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "start_live_button", "开始直播并复制推流码", start_live_buttonC)

    # 添加 按钮【复制直播服务器】
    GlobalVariableOfTheControl.rtmp_address_copy_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "rtmp_address_copy_button", "复制直播服务器", rtmp_address_copy_buttonC)

    # 添加 按钮【复制直播推流码】
    GlobalVariableOfTheControl.rtmp_stream_code_copy_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "rtmp_stream_code_copy_button", "复制直播推流码", rtmp_stream_code_copy_buttonC)

    # 添加 按钮【更新推流码并复制】
    GlobalVariableOfTheControl.rtmp_stream_code_update_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "rtmp_stream_code_update_button", "更新推流码并复制", rtmp_stream_code_update_buttonC)

    # 添加 按钮【结束直播】
    GlobalVariableOfTheControl.stop_live_button = obs.obs_properties_add_button(GlobalVariableOfTheControl.live_props, "stop_live_button", "结束直播", stop_live_buttonC)

    # ————————————————————————————————————————————————————————————————————————————————
    # 更新UI界面数据#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
    updateTheUIInterfaceData()
    return props


def updateTheUIInterfaceData():
    """
    更新UI界面数据
    Returns:

    """
    # 设置 只读文本框【登录状态】 类型
    obs.obs_property_text_set_info_type(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.login_status_textBox_type)
    # 使 只读文本框【登录状态】 显示
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, 'login_status_textBox', f'{GlobalVariableOfTheControl.login_status_textBox_string}')
    # 更新 只读文本框【登录状态】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.login_status_textBox, GlobalVariableOfTheControl.current_settings)

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
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.uid_comboBox, 0, GlobalVariableOfTheControl.uid_comboBox_string, GlobalVariableOfTheControl.uid_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, 'uid_comboBox', GlobalVariableOfTheControl.uid_comboBox_value)) if GlobalVariableOfTheControl.uid_comboBox_value in GlobalVariableOfTheControl.uid_comboBox_dict else None
        # 更新 组合框【用户】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.current_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【用户】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.uid_comboBox_dict}")

    # 设置 按钮[登录账号] 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.login_button_visible)
    # 设置 按钮【登录账号】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.login_button_enabled)
    # 更新 按钮【登录账号】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.login_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【二维码添加账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.qr_code_add_account_button, GlobalVariableOfTheControl.qr_code_add_account_button_visible)
    # 设置 按钮【二维码添加账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.qr_code_add_account_button, GlobalVariableOfTheControl.qr_code_add_account_button_enabled)
    # 更新 按钮【二维码添加账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.qr_code_add_account_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【显示二维码图片】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.display_qr_code_picture_button, GlobalVariableOfTheControl.display_qr_code_picture_button_visible)
    # 设置 按钮【显示二维码图片】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.display_qr_code_picture_button, GlobalVariableOfTheControl.display_qr_code_picture_button_enabled)
    # 更新 按钮[显示二维码图片】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.display_qr_code_picture_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【删除账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.delete_account_button_visible)
    # 设置 按钮【删除账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.delete_account_button_enabled)
    # 更新 按钮[删除账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.delete_account_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【备份账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.backup_account_button_visible)
    # 设置 按钮【备份账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.backup_account_button_enabled)
    # 更新 按钮[备份账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.backup_account_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【恢复账户】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.restore_account_button_visible)
    # 设置 按钮【恢复账户】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.restore_account_button_enabled)
    # 更新 按钮[恢复账户】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.restore_account_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【登出账号】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.logout_button_visible)
    # 设置 按钮【登出账号】 可用状态
    obs.obs_property_set_enabled(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.logout_button_enabled)
    # 更新 按钮[登出账号】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.logout_button, GlobalVariableOfTheControl.current_settings)

    # ————————————————————————————————————————————————————————————————
    # 设置 只读文本框【直播间状态】 类型
    obs.obs_property_text_set_info_type(GlobalVariableOfTheControl.room_status_textBox, GlobalVariableOfTheControl.room_status_textBox_type)
    # 使 只读文本框【直播间状态】 显示
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "room_status_textBox", GlobalVariableOfTheControl.room_status_textBox_string)
    # 更新 只读文本框【直播间状态】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.room_status_textBox, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【查看直播间封面】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.viewLiveCover_button, GlobalVariableOfTheControl.viewLiveCover_button_visible)
    # 更新 按钮【查看直播间封面】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.viewLiveCover_button, GlobalVariableOfTheControl.current_settings)

    # 设置 文件对话框【直播间封面】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.room_cover_fileDialogBox, GlobalVariableOfTheControl.room_cover_fileDialogBox_visible)
    # 使 文件对话框【直播间封面】 显示
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "room_cover_fileDialogBox", GlobalVariableOfTheControl.room_cover_fileDialogBox_string)
    # 更新 文件对话框【直播间封面】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.room_cover_fileDialogBox, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【上传直播间封面】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.room_cover_update_button, GlobalVariableOfTheControl.room_cover_update_button_visible)
    # 更新 按钮【上传直播间封面】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.room_cover_update_button, GlobalVariableOfTheControl.current_settings)

    # 设置 普通文本框【直播间标题】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.liveRoom_title_textBox, GlobalVariableOfTheControl.liveRoom_title_textBox_visible)
    # 使 普通文本框【直播间标题】 显示
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "liveRoom_title_textBox", GlobalVariableOfTheControl.liveRoom_title_textBox_string)
    # 更新 普通文本框【直播间标题】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.liveRoom_title_textBox, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【更改直播间标题】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.change_liveRoom_title_button, GlobalVariableOfTheControl.change_liveRoom_title_button_visible)
    # 更新 按钮【更改直播间标题】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.change_liveRoom_title_button, GlobalVariableOfTheControl.current_settings)

    # 设置 普通文本框【直播间公告】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.liveRoom_news_textBox, GlobalVariableOfTheControl.liveRoom_news_textBox_visible)
    # 使 普通文本框【直播间公告】 显示
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "liveRoom_news_textBox", GlobalVariableOfTheControl.liveRoom_news_textBox_string)
    # 更新 普通文本框【直播间公告】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.liveRoom_news_textBox, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【更改直播间公告】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.change_liveRoom_news_button, GlobalVariableOfTheControl.change_liveRoom_news_button_visible)
    # 更新 按钮【更改直播间公告】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.change_liveRoom_news_button, GlobalVariableOfTheControl.current_settings)

    # 判断组合框【一级分区】字典数据 和 当前数据是否有变化
    if GlobalVariableOfTheControl.parentLiveArea_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.parentLiveArea_comboBox))} or obs.obs_property_visible(GlobalVariableOfTheControl.parentLiveArea_comboBox) != GlobalVariableOfTheControl.parentLiveArea_comboBox_visible:
        logSave(0, f"数据发生变动，组合框【一级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.parentLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.parentLiveArea_comboBox_dict}")
        # 设置 组合框【一级分区】 可见状态
        obs.obs_property_set_visible(GlobalVariableOfTheControl.parentLiveArea_comboBox, GlobalVariableOfTheControl.parentLiveArea_comboBox_visible)
        # 清空组合框【一级分区】
        obs.obs_property_list_clear(GlobalVariableOfTheControl.parentLiveArea_comboBox)
        # 为 组合框【一级分区】 添加选项
        for parentLiveAreaId in GlobalVariableOfTheControl.parentLiveArea_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, GlobalVariableOfTheControl.parentLiveArea_comboBox_dict[parentLiveAreaId], parentLiveAreaId) if parentLiveAreaId != GlobalVariableOfTheControl.parentLiveArea_comboBox_value else None
        # 为 组合框【一级分区】 添加默认选项
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, 0, GlobalVariableOfTheControl.parentLiveArea_comboBox_string, GlobalVariableOfTheControl.parentLiveArea_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "parentLiveArea_comboBox", GlobalVariableOfTheControl.parentLiveArea_comboBox_value)) if GlobalVariableOfTheControl.parentLiveArea_comboBox_value in GlobalVariableOfTheControl.parentLiveArea_comboBox_dict else None
        # 更新 组合框【一级分区】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.parentLiveArea_comboBox, GlobalVariableOfTheControl.current_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【一级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.parentLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.parentLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.parentLiveArea_comboBox_dict}")

    # 设置 按钮【确认一级分区】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.parentLiveArea_true_button, GlobalVariableOfTheControl.parentLiveArea_true_button_visible)
    # 更新 按钮【确认一级分区】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.parentLiveArea_true_button, GlobalVariableOfTheControl.current_settings)

    # 判断字典数据 和 组合框 当前数据是否有变化
    if GlobalVariableOfTheControl.subLiveArea_comboBox_dict != {obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))} or obs.obs_property_visible(GlobalVariableOfTheControl.subLiveArea_comboBox) != GlobalVariableOfTheControl.subLiveArea_comboBox_visible:
        logSave(0, f"数据发生变动，组合框【二级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.subLiveArea_comboBox_dict}")
        # 设置 组合框【二级分区】 可见状态
        obs.obs_property_set_visible(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_visible)
        # 清空组合框【二级分区】
        obs.obs_property_list_clear(GlobalVariableOfTheControl.subLiveArea_comboBox)
        # 为 组合框【二级分区】 添加选项
        for subLiveAreaId in GlobalVariableOfTheControl.subLiveArea_comboBox_dict:
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_dict[subLiveAreaId], subLiveAreaId) if subLiveAreaId != GlobalVariableOfTheControl.subLiveArea_comboBox_value else None
        # 为 组合框【二级分区】 添加默认选项
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0, GlobalVariableOfTheControl.subLiveArea_comboBox_string, GlobalVariableOfTheControl.subLiveArea_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "subLiveArea_comboBox", GlobalVariableOfTheControl.subLiveArea_comboBox_value)) if GlobalVariableOfTheControl.subLiveArea_comboBox_value in GlobalVariableOfTheControl.subLiveArea_comboBox_dict else None
        # 更新 组合框【二级分区】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.current_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【二级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.subLiveArea_comboBox_dict}")

    # 设置 按钮【「确认分区」】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.subLiveArea_true_button, GlobalVariableOfTheControl.subLiveArea_true_button_visible)
    # 更新 按钮【「确认分区」】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.subLiveArea_true_button, GlobalVariableOfTheControl.current_settings)

    # 设置 url按钮【跳转直播间后台网页】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.jump_blive_web_button, GlobalVariableOfTheControl.jump_blive_web_button_visible)
    # 设置 url按钮【跳转直播间后台网页】 类型
    obs.obs_property_button_set_type(GlobalVariableOfTheControl.jump_blive_web_button, obs.OBS_BUTTON_URL)
    # 设置 url按钮【跳转直播间后台网页】 链接
    obs.obs_property_button_set_url(GlobalVariableOfTheControl.jump_blive_web_button, GlobalVariableOfTheControl.jump_blive_web_button_url)
    # 更新 url按钮【跳转直播间后台网页】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.jump_blive_web_button, GlobalVariableOfTheControl.current_settings)

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
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, 0, GlobalVariableOfTheControl.live_streaming_platform_comboBox_string, GlobalVariableOfTheControl.live_streaming_platform_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, 'live_streaming_platform_comboBox', GlobalVariableOfTheControl.live_streaming_platform_comboBox_value)) if GlobalVariableOfTheControl.live_streaming_platform_comboBox_value in GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict else None
        # 更新 组合框【直播平台】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.live_streaming_platform_comboBox, GlobalVariableOfTheControl.current_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【直播平台】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.live_streaming_platform_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.live_streaming_platform_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.live_streaming_platform_comboBox_dict}")

    # 设置 按钮【开始直播并复制推流码】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.start_live_button, GlobalVariableOfTheControl.start_live_button_visible)
    # 更新 按钮【开始直播并复制推流码】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.start_live_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【复制直播服务器】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_address_copy_button, GlobalVariableOfTheControl.rtmp_address_copy_button_visible)
    # 更新 按钮【复制直播服务器】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.rtmp_address_copy_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【复制直播推流码】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_stream_code_copy_button, GlobalVariableOfTheControl.rtmp_stream_code_copy_button_visible)
    # 更新 按钮【复制直播推流码】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.rtmp_stream_code_copy_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【更新推流码并复制】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.rtmp_stream_code_update_button, GlobalVariableOfTheControl.rtmp_stream_code_update_button_visible)
    # 更新 按钮【更新推流码并复制】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.rtmp_stream_code_update_button, GlobalVariableOfTheControl.current_settings)

    # 设置 按钮【结束直播】 可见状态
    obs.obs_property_set_visible(GlobalVariableOfTheControl.stop_live_button, GlobalVariableOfTheControl.stop_live_button_visible)
    # 更新 按钮【结束直播】 显示
    obs.obs_property_modified(GlobalVariableOfTheControl.stop_live_button, GlobalVariableOfTheControl.current_settings)


def login_buttonC(props, prop, settings=GlobalVariableOfTheControl.current_settings):
    """
    登录并刷新控件状态
    Args:
        props:
        prop:
    Returns:
    """
    # ＝＝＝＝＝＝＝＝＝
    # 　　　登录　　　＝
    # ＝＝＝＝＝＝＝＝＝
    uid = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'uid_comboBox')
    logSave(0, f"即将登录的账号：{uid}")
    if uid not in ["-1"]:
        logSave(0, f"将选定的账号：{uid}，在配置文件中转移到默认账号的位置")
        logInTry(globalVariableOfData.scripts_config_filepath, int(uid))
    else:
        logSave(2, "请添加或选择一个账号登录")
        return None
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　更新     　　＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.current_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    updateTheUIInterfaceData()
    return True


def updateAccountList_buttonC(props=None, prop=None, settings=GlobalVariableOfTheControl.current_settings):
    """
    更新账号列表
    Args:
        props:
        prop:

    Returns:
    """
    # 创建用户配置文件实例
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    # 获取 用户配置文件 中 每一个用户 导航栏用户信息 排除空值
    userInterface_navByUid4Dict = {uid: master(dict2cookie(BULC.getCookies(int(uid)))).interface_nav() for uid in [x for x in BULC.getUsers().values() if x]}
    # 获取 用户配置文件 中 每一个 用户 的 昵称
    AllUnameByUid4Dict = {uid: userInterface_navByUid4Dict[uid]["uname"] for uid in userInterface_navByUid4Dict}
    logSave(0, f"载入账号：{str(AllUnameByUid4Dict)}")
    DefaultUserInterfaceNav = master(dict2cookie(BULC.getCookies())).interface_nav() if BULC.getCookies() else None  # 获取 '默认账户' 导航栏用户信息
    DefaultUname = DefaultUserInterfaceNav["uname"] if BULC.getCookies() else None  # 获取默认账号的昵称
    """
    默认用户config["DefaultUser"]的昵称
    没有则为None
    """
    logSave(0, f"用户：{DefaultUname} 已登录" if BULC.getCookies() else f"未登录账号")

    # 设置 组合框【用户】 可见状态
    GlobalVariableOfTheControl.uid_comboBox_visible = True
    logSave(0, f"设置 组合框【用户】 可见状态：{str(GlobalVariableOfTheControl.uid_comboBox_visible)}")
    # 设置 组合框【用户】 可用状态
    GlobalVariableOfTheControl.uid_comboBox_enabled = True
    logSave(0, f"设置 组合框【用户】 可用状态：{str(GlobalVariableOfTheControl.uid_comboBox_enabled)}")
    # 设置 组合框【用户】 的数据字典
    GlobalVariableOfTheControl.uid_comboBox_dict = {uid or '-1': AllUnameByUid4Dict.get(uid, '添加或选择一个账号登录') for uid in BULC.getUsers().values()}
    logSave(0, f"设置 组合框【用户】 数据字典：{str(GlobalVariableOfTheControl.uid_comboBox_dict)}")
    # 设置 组合框【用户】 默认显示内容
    GlobalVariableOfTheControl.uid_comboBox_string = DefaultUname if BULC.getCookies() else '添加或选择一个账号登录'
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 设置 组合框【用户】 内容：{GlobalVariableOfTheControl.uid_comboBox_string}")
    # 设置 组合框【用户】 默认显示内容 的 列表值
    GlobalVariableOfTheControl.uid_comboBox_value = BULC.getUsers()[0] if BULC.getCookies() else '-1'
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 设置 组合框【用户】 列表值：{GlobalVariableOfTheControl.uid_comboBox_value}")

    # 判断字典数据 和 组合框 当前数据是否有变化
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
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.uid_comboBox, 0, GlobalVariableOfTheControl.uid_comboBox_string, GlobalVariableOfTheControl.uid_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, 'uid_comboBox', GlobalVariableOfTheControl.uid_comboBox_value)) if GlobalVariableOfTheControl.uid_comboBox_value in GlobalVariableOfTheControl.uid_comboBox_dict else None
        # 更新 组合框【用户】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.uid_comboBox, GlobalVariableOfTheControl.current_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【用户】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.uid_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.uid_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.uid_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.uid_comboBox_dict}")
    return True


def qrCodeAddAccount_buttonC(props, prop):
    """
    二维码添加账号
    Args:
        props:
        prop:
    Returns:
    """
    qrAddUser()
    return True


def show_qr_code_picture_buttonC(props, prop):
    """
    显示二维码图片
    Args:
        props:
        prop:
    Returns:
    """
    if globalVariableOfData.LoginQRCodePillowImg:
        logSave(0, f"展示登录二维码图片")
        globalVariableOfData.LoginQRCodePillowImg.show()
    else:
        logSave(2, f"没有可展示的登录二维码图片，请点击按钮 【二维码添加账号】创建")
    pass


def del_user_buttonC(props, prop):
    """
    删除用户
    Args:
        props:
        prop:
    Returns:
    """
    uid = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'uid_comboBox')
    if uid not in ["-1"]:
        BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
        BULC.deleteUser(uid)
    else:
        logSave(2, "请选择一个账号")
        return None
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.current_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    updateTheUIInterfaceData()
    return True


def backupUsers_buttonC(props, prop):
    """
    备份用户
    Args:
        props:
        prop:
    Returns:
    """
    pass


def restoreUser_buttonC(props, prop):
    """
    恢复用户
    Args:
        props:
        prop:
    Returns:
    """
    pass


def logOut_buttonC(props, prop):
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
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    BULC.updateUser(None)
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　更新     　　＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.current_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    updateTheUIInterfaceData()
    return True


def update_roomCover_buttonC(props, prop):
    """
    上传直播间封面
    Args:
        props:
        prop:
    Returns:
    """
    # 获取文件对话框内容
    GlobalVariableOfTheControl.room_cover_fileDialogBox_string = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'room_cover_fileDialogBox')
    logSave(0, f"获得图片文件：{GlobalVariableOfTheControl.room_cover_fileDialogBox_string}")
    if GlobalVariableOfTheControl.room_cover_fileDialogBox_string:
        PIL_Image = Image.open(GlobalVariableOfTheControl.room_cover_fileDialogBox_string)
        logSave(0, f"图片文件PIL_Image实例化，当前文件大小(宽X高)：{PIL_Image.size}")
        PIL_Image1609 = PIL_Image2CentralProportionCutting(PIL_Image, 16 / 9)
        PIL_Image1609_w, PIL_Image1609_h = PIL_Image1609.size
        logSave(0, f"图片16:9裁切后大小(宽X高)：{PIL_Image1609.size}")
        PIL_Image1609ZoomingWidth1020 = PIL_Image1609 if PIL_Image1609_w < 1020 else PIL_Image2Zooming(PIL_Image1609, 4, target_width=1020)
        logSave(0, f"限制宽<1020，进行缩放，缩放后大小：{PIL_Image1609ZoomingWidth1020.size}")
        PIL_Image1609 = PIL_Image2CentralProportionCutting(PIL_Image1609ZoomingWidth1020, 16 / 9)
        logSave(0, f"缩放后图片16:9裁切后大小(宽X高)：{PIL_Image1609.size}")
        PIL_Image0403 = PIL_Image2CentralProportionCutting(PIL_Image1609ZoomingWidth1020, 4 / 3)
        logSave(0, f"缩放后图片4:3裁切后大小(宽X高)：{PIL_Image0403.size}")
        logSave(0, f"展示图片")
        PIL_Image0403.show()
        PIL_Image1609.show()
        PIL_Image1609ZoomingWidth1020Binary = PIL_Image2Binary(PIL_Image1609ZoomingWidth1020, ImgFormat="JPEG", compress_level=0)
        logSave(0, f"图片二进制化")
        # 创建用户配置文件实例
        BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
        # 获取 '默认账户' cookies
        DefaultUserCookies = BULC.getCookies()
        coverUrl = CsrfAuthentication(dict2cookie(DefaultUserCookies)).upload_cover(PIL_Image1609ZoomingWidth1020Binary)['data']['location']
        logSave(0, f"上传二进制图片，获得图片链接：{coverUrl}")
        CsrfAuthentication(dict2cookie(DefaultUserCookies)).update_cover(coverUrl)
        logSave(0, f"更改封面结束")
    else:
        logSave(2, "未获取到图片")
    pass


def check_roomCover_buttonC(props, prop):
    """
    查看直播间封面
    Args:
        props:
        prop:
    Returns:
    """
    # 创建用户配置文件实例
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    # 获取'默认账户'获取用户对应的直播间状态
    RoomInfoOld = getRoomInfoOld(int(BULC.getUsers()[0])) if BULC.getCookies() else {}
    logSave(0, f"根据是否有账号登录：{bool(BULC.getCookies())} 获取 登录账户 对应的直播间状态：数据长度为{len(RoomInfoOld)}")
    # 获取 默认用户 的 直播间状态
    DefaultRoomStatus = RoomInfoOld["roomStatus"] if BULC.getCookies() else None
    # 获取默认用户的 直播间id
    DefaultRoomid = RoomInfoOld["roomid"] if bool(DefaultRoomStatus) else 0
    # 获取'默认账户'直播间的基础信息
    RoomBaseInfo = getRoomBaseInfo(DefaultRoomid) if DefaultRoomStatus else {}
    # 获取直播间封面的链接
    LiveRoomCover_url = RoomBaseInfo["by_room_ids"][str(DefaultRoomid)]["cover"] if bool(DefaultRoomStatus) else ""
    """
    直播间封面URL
    """
    # # 获取'默认账户'直播间的基础信息
    roomCover_pillowImg = url2pillowImage(LiveRoomCover_url)
    logSave(0, f"现在的直播间封面URL：{LiveRoomCover_url}")
    if roomCover_pillowImg:
        logSave(0, f"封面已显示，格式: {roomCover_pillowImg.format}，尺寸: {roomCover_pillowImg.size}")
        roomCover_pillowImg.show()  # 显示图像（可选）
    pass


def change_liveRoom_title_buttonC(props, prop):
    """
    更改直播间标题
    Args:
        props:
        prop:
    Returns:
    """
    liveRoom_title_textBox_string = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'liveRoom_title_textBox')
    if GlobalVariableOfTheControl.liveRoom_title_textBox_string != liveRoom_title_textBox_string:
        GlobalVariableOfTheControl.liveRoom_title_textBox_string = liveRoom_title_textBox_string
        logSave(0, "直播间标题改变")
        # 获取 '默认账户' cookie
        BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
        cookies = BULC.getCookies()
        turn_title_return = CsrfAuthentication(dict2cookie(cookies)).room_v1_Room_update(liveRoom_title_textBox_string)
        logSave(0, f"更改直播间标题返回消息：{turn_title_return}")
    else:
        logSave(0, "直播间标题未改变")
    pass


def change_liveRoom_news_buttonC(props, prop):
    """
    更改直播间公告
    Args:
        props:
        prop:
    Returns:
    """
    liveRoom_news_textBox_string = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'liveRoom_news_textBox')
    if GlobalVariableOfTheControl.liveRoom_news_textBox_string != liveRoom_news_textBox_string:
        GlobalVariableOfTheControl.liveRoom_news_textBox_string = liveRoom_news_textBox_string
        logSave(0, "直播间公告已改变")
        BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
        cookies = BULC.getCookies()
        turn_news_return = CsrfAuthentication(dict2cookie(cookies)).updateRoomNews(liveRoom_news_textBox_string)
        logSave(0, f'更改直播间公告返回消息：{turn_news_return}')
    else:
        logSave(0, "直播间公告未改变")
    pass


def start_area1_buttonC(props, prop, settings=GlobalVariableOfTheControl.current_settings):
    """
    确认一级分区
    Args:
        props:
        prop:
        settings:
    Returns:
    """
    # #获取 组合框【一级分区】 当前选项的值
    parentLiveArea_comboBox_value = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'parentLiveArea_comboBox')
    logSave(0, f"获取 组合框【一级分区】 当前选项的值{parentLiveArea_comboBox_value}")
    if parentLiveArea_comboBox_value not in ["-1"]:
        subLiveAreaNameByid4dict = {str(subAreaObj["id"]): subAreaObj["name"] for subAreaObj in getsubLiveAreaObjList(parentLiveArea_comboBox_value)} if parentLiveArea_comboBox_value else {"-1": "请选择一级分区"}
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
            obs.obs_property_list_add_string(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.subLiveArea_comboBox_dict[subLiveAreaId], subLiveAreaId) if subLiveAreaId != GlobalVariableOfTheControl.subLiveArea_comboBox_value else None
        # 为 组合框【二级分区】 添加默认选项
        (obs.obs_property_list_insert_string(GlobalVariableOfTheControl.subLiveArea_comboBox, 0, GlobalVariableOfTheControl.subLiveArea_comboBox_string, GlobalVariableOfTheControl.subLiveArea_comboBox_value) or obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, "subLiveArea_comboBox", GlobalVariableOfTheControl.subLiveArea_comboBox_value)) if GlobalVariableOfTheControl.subLiveArea_comboBox_value in GlobalVariableOfTheControl.subLiveArea_comboBox_dict else None
        # 更新 组合框【二级分区】 显示
        obs.obs_property_modified(GlobalVariableOfTheControl.subLiveArea_comboBox, GlobalVariableOfTheControl.current_settings)
    else:
        logSave(0, f"数据未发生变动，组合框【二级分区】数据：{str({obs.obs_property_list_item_string(GlobalVariableOfTheControl.subLiveArea_comboBox, idx): obs.obs_property_list_item_name(GlobalVariableOfTheControl.subLiveArea_comboBox, idx) for idx in range(obs.obs_property_list_item_count(GlobalVariableOfTheControl.subLiveArea_comboBox))})}，新的字典数据：{GlobalVariableOfTheControl.subLiveArea_comboBox_dict}")
    return True


def start_area_buttonC():
    # #获取 组合框【二级分区】 当前选项的值
    subLiveArea_comboBox_value = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'subLiveArea_comboBox')
    if subLiveArea_comboBox_value != GlobalVariableOfTheControl.subLiveArea_comboBox_value:
        GlobalVariableOfTheControl.subLiveArea_comboBox_value = subLiveArea_comboBox_value
        logSave(0, "子分区有变化")
        # 获取默认账户
        BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
        cookies = BULC.getCookies()
        # 获取二级分区id
        area2_id = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'subLiveArea_comboBox')
        ChangeRoomArea = CsrfAuthentication(dict2cookie(cookies)).AnchorChangeRoomArea(int(area2_id))
        logSave(0, f"更新直播间分区返回：{ChangeRoomArea}")
    else:
        logSave(0, "子分区没变化")
    pass


def jump_Blive_web_buttonC(props, prop):
    """
    跳转直播间后台网页
    Args:
        props:
        prop:
    Returns:
    """
    logSave(0, f"即将跳转到网页{GlobalVariableOfTheControl.jump_blive_web_button_url}")
    pass


# ____________________-------------------____________________---------------------_____________
def start_live_buttonC(props, prop):
    """
    开始直播
    Args:
        props:
        prop:
    Returns:
    """
    logSave(0, 'start_live')
    # 获取默认账户
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    cookies = BULC.getCookies()
    # 开播
    if cookies:
        # 获取二级分区id
        subLiveArea_id = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'subLiveArea_comboBox')
        live_streaming_platform = obs.obs_data_get_string(GlobalVariableOfTheControl.current_settings, 'live_streaming_platform_comboBox')
        logSave(0, f"使用【{live_streaming_platform}】开播")
        startLive = CsrfAuthentication(dict2cookie(cookies)).startLive(int(subLiveArea_id), live_streaming_platform)
        logSave(0, f"开播消息代码【{startLive['code']}】。消息内容：【{startLive['message']}】。")
        # 将 rtmp推流码 复制到剪贴板
        rtmpPushCode = startLive["data"]["rtmp"]["code"]
        logSave(0, f"将rtmp推流码复制到剪贴板，rtmp推流码长度{len(rtmpPushCode)}")
        cb.copy(rtmpPushCode)
    # 设置组合框【用户】为'默认用户'
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, 'uid_comboBox', cookies["DedeUserID"])

    change_liveRoom_title_buttonC(props, prop)
    change_liveRoom_news_buttonC(props, prop)
    start_area1_buttonC(props, prop, settings=GlobalVariableOfTheControl.current_settings)

    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.current_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    updateTheUIInterfaceData()
    return True


def rtmp_address_copy_buttonC(props, prop):
    """
    复制直播服务器
    Args:
        props:
        prop:
    Returns:
    """
    # 获取默认账户
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    cookies = BULC.getCookies()
    StreamAddr = CsrfAuthentication(dict2cookie(cookies)).FetchWebUpStreamAddr()
    cb.copy(StreamAddr['data']['addr']['addr'])
    logSave(0, f"已将 直播服务器 复制到剪贴板：【{StreamAddr['data']['addr']['addr']}】")
    pass


def rtmp_stream_code_copy_buttonC(props, prop):
    """
    复制直播推流码
    Args:
        props:
        prop:
    Returns:
    """
    # 获取默认账户
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    cookies = BULC.getCookies()
    StreamAddr = CsrfAuthentication(dict2cookie(cookies)).FetchWebUpStreamAddr()
    cb.copy(StreamAddr['data']['addr']['code'])
    logSave(0, f"已将 直播推流码 复制到剪贴板：【{StreamAddr['data']['addr']['code']}】")
    pass


def rtmp_stream_code_update_buttonC(props, prop):
    """
    更新推流码并复制
    Args:
        props:
        prop:
    Returns:
    """
    # 获取默认账户
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    cookies = BULC.getCookies()
    StreamAddr = CsrfAuthentication(dict2cookie(cookies)).FetchWebUpStreamAddr(True)
    cb.copy(StreamAddr['data']['addr']['code'])
    logSave(0, f"已更新推流码 并将 直播推流码 复制到剪贴板：【{StreamAddr['data']['addr']['code']}】")
    pass


def stop_live_buttonC(props, prop):
    """
    结束直播
    Args:
        props:
        prop:
    Returns:
    """
    logSave(0, 'stop_live')
    # 获取默认账户
    BULC = BilibiliUserLogsIn2ConfigFile(configPath=globalVariableOfData.scripts_config_filepath)
    cookies = BULC.getCookies()
    # 停播
    if cookies:
        stopLive = CsrfAuthentication(dict2cookie(cookies)).stopLive()
        logSave(0, f"下播消息代码【{stopLive['code']}】。消息内容：【{stopLive['message']}】。")
    # 设置组合框【用户】为'默认用户'
    obs.obs_data_set_string(GlobalVariableOfTheControl.current_settings, 'uid_comboBox', cookies["DedeUserID"])
    # 调用script_defaults更新obs默认配置信息
    logSave(0, f"更新控件配置信息")
    script_defaults(GlobalVariableOfTheControl.current_settings)
    # 更新脚本用户小部件
    logSave(0, f"更新控件UI")
    updateTheUIInterfaceData()
    return True


def script_unload():
    """
    在脚本被卸载时调用。
    """
    logSave(0, "已卸载：bilibili-live")
    with open(Path(globalVariableOfData.scripts_data_dirpath) / f"{datetime.now().strftime("%Y%m%d_%H%M%S")}.log", "w", encoding="utf-8") as f:
        f.write(str(globalVariableOfData.logRecording))


