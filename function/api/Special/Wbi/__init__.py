from pathlib import Path
from typing import Literal, Dict, Any
from urllib.parse import quote
from functools import reduce
from hashlib import md5
import urllib.parse
import time

import requests

from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


class WbiSigna:
    def __init__(self, headers: dict, verify_ssl: bool = True):
        """
        wbi签名的api
        @param headers: 包含Cookie和User-Agent的请求头字典
        @param verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
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

    def get_contribution_rank(self, ruid: int, room_id: int,
                              rank_type: Literal["online_rank", "daily_rank", "weekly_rank", "monthly_rank"],
                              switch: Literal["contribution_rank", "entry_time_rank", "today_rank", "yesterday_rank",
                              "current_week_rank", "last_week_rank", "current_month_rank", "last_month_rank"],
                              page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        获取直播间观众贡献排名

        Args:
            ruid: 直播间主播 mid
            room_id: 直播间 id
            rank_type: 排名类型
                - "online_rank": 在线榜
                - "daily_rank": 日榜
                - "weekly_rank": 周榜
                - "monthly_rank": 月榜
            switch: 具体排名类型
                "online_rank": 在线榜
                    - "contribution_rank": 贡献值
                    - "entry_time_rank": 进房时间
                "daily_rank": 日榜
                    - "today_rank": 当日
                    - "yesterday_rank": 昨日
                "weekly_rank": 周榜
                    - "current_week_rank": 本周
                    - "last_week_rank": 上周
                "monthly_rank": 月榜
                    - "current_month_rank": 本月
                    - "last_month_rank": 上月
            page: 页码，page_size*page<100
            page_size: 每页元素数，page_size*page<100

        Returns:
            包含排名信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的排名数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - api_code: B站API错误码（如果有）
        """
        try:
            # 参数验证
            if not ruid or ruid <= 0:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": "主播ID无效",
                    "status_code": None
                }

            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            if page <= 0 or page_size <= 0 or page * page_size > 100:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": "页码或每页数量无效（总数不能超过100）",
                    "status_code": None
                }

            # 构建API请求参数
            api_url = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/queryContributionRank"
            params = {
                "ruid": ruid,
                "room_id": room_id,
                "page": page,
                "page_size": page_size,
                "type": rank_type,
                "switch": switch,
                "platform": "web"
            }

            # WBI签名
            signed_params = self.wbi(params)

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                params=signed_params,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 检查B站API返回状态
            if result.get("code") != 0:
                return {
                    "success": False,
                    "message": "B站API返回错误",
                    "error": result.get("message", "未知错误"),
                    "status_code": response.status_code,
                    "api_code": result.get("code")
                }

            # 成功返回
            return {
                "success": True,
                "message": "贡献排名获取成功",
                "data": result.get("data", {}),
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取贡献排名失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取贡献排名失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取贡献排名失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取贡献排名过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_danmu_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间弹幕服务器信息

        Args:
            room_id: 直播间真实ID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含弹幕服务器信息等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - api_code: B站API返回的错误码（如果有）
        """
        try:
            # 检查房间ID是否有效
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取弹幕服务器信息失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            # 构建API请求
            url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo'
            params = {
                "id": room_id,
            }

            # 使用wbi签名参数
            signed_params = self.wbi(params)

            # 发送请求
            response = requests.get(
                url=url,
                headers=self.headers,
                params=signed_params,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取弹幕服务器信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 检查B站API返回状态
            if result.get("code") != 0:
                return {
                    "success": False,
                    "message": "B站API返回错误",
                    "error": result.get("message", "未知错误"),
                    "status_code": response.status_code,
                    "api_code": result.get("code"),
                    "response_data": result
                }

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "api_code": result.get("code"),
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "弹幕服务器信息获取成功",
                "data": result["data"],
                "status_code": response.status_code,
                "api_code": result.get("code")
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取弹幕服务器信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取弹幕服务器信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取弹幕服务器信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取弹幕服务器信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def get_user_space_info(self, mid: int) -> Dict[str, Any]:
        """
        获取用户空间详细信息

        Args:
            mid: 目标用户mid

        Returns:
            包含用户空间信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的用户数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查用户ID是否有效
            if not mid or mid <= 0:
                return {
                    "success": False,
                    "message": "获取用户空间信息失败",
                    "error": "用户ID无效",
                    "status_code": None,
                    "data": None
                }

            # 构建API请求
            api_url = "https://api.bilibili.com/x/space/wbi/acc/info"
            params = self.wbi({"mid": mid})

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                params=params,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取用户空间信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "data": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 检查B站API返回状态
            if result.get("code") != 0:
                return {
                    "success": False,
                    "message": "B站API返回错误",
                    "error": result.get("message", "未知错误"),
                    "status_code": response.status_code,
                    "api_code": result.get("code"),
                    "data": None
                }

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "data": None,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "用户空间信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": "请求超时",
                "status_code": None,
                "data": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户空间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "data": None
            }

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



if __name__ == '__main__':
    from _Input.function.api.Special import Room as DataInput

    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    wsa = WbiSigna(Headers)
    print(wsa.wbi({}))