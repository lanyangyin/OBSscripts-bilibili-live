import json
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import quote
from functools import reduce
from hashlib import md5
import urllib.parse
import time
import random

import requests

from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


class WbiSigna:
    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        wbi签名的api
        Args:
            headers: 包含Cookie和User-Agent的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
        """
        self.headers = headers
        self.verify_ssl = verify_ssl

    def wbi(self, data: dict):
        """
        WBI 签名
        @param data: 需要 wbi签名 的 params 参数
        @return: requests的 params 参数
        @rtype: dict
        """
        mixinKeyEncTab = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
            33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
            61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
            36, 20, 34, 44, 52
        ]

        def getMixinKey(orig: str):
            """对 imgKey 和 subKey 进行字符顺序打乱编码"""
            return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

        def encWbi(params: dict, img_key: str, sub_key: str):
            """为请求参数进行 wbi 签名"""
            mixin_key = getMixinKey(img_key + sub_key)
            curr_time = round(time.time())
            params['wts'] = curr_time  # 添加 wts 字段
            params = dict(sorted(params.items()))  # 按照 key 重排参数
            # 过滤 value 中的 "!'()*" 字符
            params = {
                k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
                for k, v
                in params.items()
            }
            query = urllib.parse.urlencode(params)  # 序列化参数
            wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
            params['w_rid'] = wbi_sign
            return params

        def getWbiKeys() -> tuple[str, str]:
            """获取最新的 img_key 和 sub_key"""
            resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=self.headers)
            resp.raise_for_status()
            json_content = resp.json()
            img_url: str = json_content['data']['wbi_img']['img_url']
            sub_url: str = json_content['data']['wbi_img']['sub_url']
            img_key = img_url.rsplit('/', 1)[1].split('.')[0]
            sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
            return img_key, sub_key

        img_key, sub_key = getWbiKeys()

        signed_params = encWbi(
            params=data,
            img_key=img_key,
            sub_key=sub_key
        )
        return signed_params

    def send_danmu(self, room_id: int, message: str,
                   fontsize: int = 25, color: int = 16777215, mode: int = 1,
                   bubble: int = 0, reply_mid: int = 0, reply_uname: str = "",
                   dm_type: int = 0, emoticon_unique: str = "") -> Dict[str, Any]:
        """
        发送直播弹幕

        Args:
            room_id: 直播间ID
            message: 弹幕内容
            fontsize: 字体大小，默认25
            color: 颜色值，默认16777215（白色）
            mode: 展示模式，默认1
            bubble: 气泡，默认0
            reply_mid: 要@的用户mid，默认0
            reply_uname: 要@的用户名，默认空
            dm_type: 弹幕类型，0为文字，1为表情，默认0
            emoticon_unique: 表情唯一标识，dm_type=1时使用

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的返回数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - api_code: B站API错误码（如果有）
        """
        try:
            # 参数验证
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            if not message or len(message.strip()) == 0:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "弹幕内容不能为空",
                    "status_code": None
                }

            # 从cookie中获取csrf token
            cookie_dict = {}
            if 'cookie' in self.headers:
                cookie_items = self.headers['cookie'].split('; ')
                for item in cookie_items:
                    if '=' in item:
                        key, value = item.split('=', 1)
                        cookie_dict[key] = value

            csrf_token = cookie_dict.get('bili_jct')
            if not csrf_token:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "未找到CSRF token (bili_jct)",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/msg/send"

            # URL参数（WBI签名）
            url_params = {
                "web_location": "444.8"
            }
            signed_url_params = self.wbi(url_params)

            # 表单数据
            form_data = {
                "bubble": bubble,
                "msg": message,
                "color": color,
                "mode": mode,
                "room_type": 0,
                "jumpfrom": 0,
                "reply_mid": reply_mid,
                "reply_attr": 0,
                "replay_dmid": "",
                "statistics": '{"appId":100,"platform":5}',
                "reply_type": 0,
                "reply_uname": reply_uname,
                "data_extend": '{"trackid":"-99998"}',
                "fontsize": fontsize,
                "rnd": int(time.time()),
                "roomid": room_id,
                "csrf": csrf_token,
                "csrf_token": csrf_token
            }

            # 如果是表情弹幕，添加相关参数
            if dm_type == 1:
                form_data["dm_type"] = dm_type
                form_data["emoticonOptions"] = "[object Object]"

            # 发送请求
            response = requests.post(
                url=api_url,
                headers=self.headers,
                params=signed_url_params,
                data=form_data,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 检查B站API返回状态
            api_code = result.get("code")
            if api_code != 0:
                error_message = result.get("message", "未知错误")

                # 特殊处理常见的错误码
                if api_code == 10030:
                    error_message = "发送弹幕频率过快，请稍后再试"
                elif api_code == -101:
                    error_message = "账号未登录或登录已过期"
                elif api_code == -111:
                    error_message = "CSRF token校验失败"
                elif api_code == 1003212:
                    error_message = "弹幕内容超出长度限制"

                return {
                    "success": False,
                    "message": "B站API返回错误",
                    "error": error_message,
                    "status_code": response.status_code,
                    "api_code": api_code
                }

            # 检查屏蔽词导致的发送失败
            msg_content = result.get("msg", "")
            if msg_content in ["f", "k"]:
                error_msg = "因屏蔽词导致发送失败"
                if msg_content == "f":
                    error_msg += "（B站屏蔽词）"
                else:
                    error_msg += "（直播间屏蔽词）"

                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": error_msg,
                    "status_code": response.status_code,
                    "api_code": api_code
                }

            # 成功返回
            return {
                "success": True,
                "message": "弹幕发送成功",
                "data": result.get("data", {}),
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "发送弹幕失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "发送弹幕失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "发送弹幕失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "发送弹幕过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


# 使用示例
if __name__ == '__main__':
    from _Input.function.api.Special import Room as DataInput

    # 初始化配置管理器
    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
    cookies = BULC.get_user_cookies()['data']

    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies),
        'Referer': 'https://live.bilibili.com/',
        'Origin': 'https://live.bilibili.com'
    }

    # 创建弹幕发送器实例
    danmu_sender = WbiSigna(Headers)

    # 示例1：发送普通文字弹幕
    print("🚀 发送普通文字弹幕...")
    result1 = danmu_sender.send_danmu(
        room_id=25322725,
        message="测试弹幕，这是一条普通文字弹幕"
    )

    if result1["success"]:
        print("✅ 普通弹幕发送成功")
        if result1.get("data"):
            print(f"📊 弹幕ID: {json.loads(result1['data'].get('mode_info', {}).get('extra', {})).get('id_str', '未知')}")
    else:
        print(f"❌ 普通弹幕发送失败: {result1['error']}")
        if result1.get('api_code'):
            print(f"   API错误码: {result1['api_code']}")

    # 等待2秒避免频率限制
    time.sleep(2)

    # 示例2：发送表情弹幕（需要知道具体表情代码）
    print("\n🎭 发送表情弹幕...")
    result2 = danmu_sender.send_danmu(
        room_id=25322725,
        message="upower_[蛆音娘_害怕]",  # 表情代码
        dm_type=1
    )

    if result2["success"]:
        print("✅ 表情弹幕发送成功")
    else:
        print(f"❌ 表情弹幕发送失败: {result2['error']}")

    # 等待2秒避免频率限制
    time.sleep(2)

    # 示例3：带@的弹幕
    print("\n👥 发送带@的弹幕...")
    result3 = danmu_sender.send_danmu(
        room_id=25322725,
        message="你好！这是一条测试弹幕",
        reply_mid=143474500,  # 要@的用户mid
        reply_uname="兰阳音"  # 要@的用户名
    )

    if result3["success"]:
        print("✅ @弹幕发送成功")
    else:
        print(f"❌ @弹幕发送失败: {result3['error']}")