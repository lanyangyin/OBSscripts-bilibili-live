import time
from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.EncodingConversion.parse_cookie import parse_cookie


class BilibiliCSRFAuthenticator:
    """
    B站CSRF认证管理器，用于处理需要CSRF令牌的API请求。

    该类专门用于B站直播相关的CSRF认证操作，包括发送弹幕功能。
    自动从Cookie中提取必要的认证信息，并提供简化的API调用接口。

    特性：
    - 自动从Cookie中解析CSRF令牌（bili_jct）
    - 自动提取用户ID（DedeUserID）
    - 支持SSL验证配置
    - 提供弹幕发送功能
    - 统一的错误处理和响应格式
    - 特殊处理屏蔽词导致的发送失败
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化CSRF认证管理器

        Args:
            headers: 包含Cookie等认证信息的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）

        Returns:
            包含操作结果的字典，包含以下键：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（如认证器实例）
            - error: 失败时的错误信息
        """
        self.headers = headers.copy()  # 避免修改原始headers
        self.verify_ssl = verify_ssl
        self.initialization_result = self._initialize_authenticator()

    def _initialize_authenticator(self) -> Dict[str, Any]:
        """
        初始化认证器的内部实现

        Returns:
            包含初始化结果的字典
        """
        try:
            # 解析Cookie
            if "cookie" not in self.headers:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": "请求头中缺少cookie字段"
                }

            self.cookie = self.headers["cookie"]
            self.cookies = parse_cookie(self.cookie)

            # 提取必要字段
            required_fields = ["bili_jct", "DedeUserID"]
            missing_fields = [field for field in required_fields if field not in self.cookies]
            if missing_fields:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": f"Cookie中缺少必要字段: {', '.join(missing_fields)}"
                }

            self.user_id = self.cookies["DedeUserID"]
            self.csrf = self.cookies["bili_jct"]

            return {
                "success": True,
                "message": "认证器初始化成功",
                "data": {
                    "user_id": self.user_id,
                    "csrf_token": self.csrf
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": "初始化过程中发生异常",
                "error": str(e)
            }

    def validate_csrf_token(self) -> Dict[str, Any]:
        """
        验证CSRF令牌是否有效

        Returns:
            包含验证结果的字典：
            - success: 验证是否成功
            - valid: CSRF令牌是否有效
            - message: 结果描述信息
        """
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "valid": False,
                "message": "认证器未正确初始化"
            }

        is_valid = bool(self.csrf and len(self.csrf) == 32)

        return {
            "success": True,
            "valid": is_valid,
            "message": "CSRF令牌有效" if is_valid else "CSRF令牌无效"
        }

    def get_user_info(self) -> Dict[str, Any]:
        """
        获取用户基本信息

        Returns:
            包含用户信息的字典：
            - success: 操作是否成功
            - data: 用户信息字典（包含user_id, csrf_token, has_valid_csrf）
            - message: 结果描述信息
        """
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "message": "无法获取用户信息，认证器未正确初始化",
                "error": self.initialization_result.get("error", "未知错误")
            }

        validation_result = self.validate_csrf_token()

        return {
            "success": True,
            "data": {
                "user_id": self.user_id,
                "csrf_token": self.csrf,
                "has_valid_csrf": validation_result["valid"]
            },
            "message": "用户信息获取成功"
        }

    def send_danmaku(self, room_id: int, message: str, font_size: int = 25,
                     color: int = 16777215, mode: int = 1, bubble: int = 0,
                     reply_mid: int = 0, reply_uname: str = "") -> Dict[str, Any]:
        """
        发送直播间弹幕

        Args:
            room_id: 直播间ID
            message: 弹幕内容
            font_size: 字体大小，默认25
            color: 十进制颜色值，默认16777215（白色）
            mode: 展示模式，默认1
            bubble: 气泡，默认0
            reply_mid: 要@的用户mid，默认0（不@）
            reply_uname: 要@的用户名称，默认空字符串

        Returns:
            包含发送结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含弹幕信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的code
            - blocked_reason: 屏蔽原因（如果被屏蔽）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None,
                    "blocked_reason": None
                }

            # 验证必要参数
            if not self.csrf:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "缺少bili_jct参数，无法获取csrf token",
                    "status_code": None,
                    "api_code": None,
                    "blocked_reason": None
                }

            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None,
                    "blocked_reason": None
                }

            if not message or len(message.strip()) == 0:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "弹幕内容不能为空",
                    "status_code": None,
                    "api_code": None,
                    "blocked_reason": None
                }

            # 检查弹幕长度限制（B站限制通常为20个字符）
            if len(message) > 20:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": "弹幕内容过长，最多20个字符",
                    "status_code": None,
                    "api_code": None,
                    "blocked_reason": None
                }

            # 构建请求负载
            payload = {
                "roomid": room_id,
                "msg": message,
                "rnd": int(time.time()),  # 当前Unix时间戳
                "fontsize": font_size,
                "color": color,
                "mode": mode,
                "bubble": bubble,
                "room_type": 0,
                "jumpfrom": 0,
                "reply_mid": reply_mid,
                "reply_attr": 0,
                "reply_uname": reply_uname,
                "replay_dmid": "",
                "statistics": '{"appId":100,"platform":5}',
                "csrf": self.csrf,
                "csrf_token": self.csrf
            }

            api_url = "https://api.live.bilibili.com/msg/send"

            response = requests.post(
                url=api_url,
                headers=self.headers,
                data=payload,
                verify=self.verify_ssl,
                timeout=10
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "发送弹幕失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text,
                    "blocked_reason": None
                }

            # 解析响应
            result = response.json()

            # 根据B站API返回的code判断是否成功
            api_code = result.get("code", -1)
            api_message = result.get("message", "")
            api_msg = result.get("msg", "")

            # 处理特殊情况：code为0但实际发送失败（屏蔽词等情况）
            if api_code == 0:
                # 检查是否为屏蔽词导致的失败
                if api_message == "f" or api_msg == "f":
                    return {
                        "success": False,
                        "message": "发送弹幕失败",
                        "error": "弹幕内容包含B站屏蔽词",
                        "status_code": response.status_code,
                        "api_code": api_code,
                        "api_response": result,
                        "blocked_reason": "bilibili_sensitive_words"
                    }
                elif api_message == "k" or api_msg == "k":
                    return {
                        "success": False,
                        "message": "发送弹幕失败",
                        "error": "弹幕内容被主播设置的屏蔽词拦截",
                        "status_code": response.status_code,
                        "api_code": api_code,
                        "api_response": result,
                        "blocked_reason": "streamer_blocked_words"
                    }
                else:
                    # 真正成功的情况
                    return {
                        "success": True,
                        "message": "弹幕发送成功",
                        "data": {
                            "mode_info": result.get("data", {}).get("mode_info", {}),
                            "dm_v2": result.get("data", {}).get("dm_v2"),
                            "api_response": result
                        },
                        "status_code": response.status_code,
                        "api_code": api_code,
                        "blocked_reason": None
                    }
            else:
                # 弹幕发送失败
                error_message = result.get("message", "未知错误")
                common_errors = {
                    -101: "账号未登录",
                    -111: "CSRF校验失败",
                    -400: "请求参数错误",
                    1003212: "弹幕内容超出限制长度",
                    10031: "发送频率过快",
                    10030: "重复弹幕",
                    10032: "弹幕包含敏感词"
                }

                # 使用预定义的错误消息或API返回的消息
                if api_code in common_errors:
                    error_message = common_errors[api_code]

                return {
                    "success": False,
                    "message": "B站API返回错误",
                    "error": error_message,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "api_response": result,
                    "blocked_reason": None
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "发送弹幕失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None,
                "blocked_reason": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "发送弹幕失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None,
                "blocked_reason": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "发送弹幕失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None,
                "blocked_reason": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "发送弹幕过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None,
                "blocked_reason": None
            }


# 使用示例
if __name__ == "__main__":
    from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
    from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
    from _Input.function.api.Special import Csrf as DataInput

    # 示例用法
    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建认证器实例
    authenticator = BilibiliCSRFAuthenticator(Headers)

    # 检查初始化结果
    if authenticator.initialization_result["success"]:
        # 获取用户信息
        user_info = authenticator.get_user_info()
        if user_info["success"]:
            print("用户信息:", user_info)

            # 示例：发送弹幕到指定直播间
            room_id = 1899237171  # 示例房间ID，请替换为实际房间ID
            danmaku_message = "测试弹幕"

            send_result = authenticator.send_danmaku(room_id, danmaku_message)

            if send_result["success"]:
                print("弹幕发送成功!")
                print(f"弹幕ID: {send_result['data'].get('mode_info', {}).get('id_str', '未知')}")
            else:
                print(f"弹幕发送失败: {send_result['error']}")

                # 特别处理屏蔽词情况
                if send_result.get("blocked_reason"):
                    blocked_reason = send_result["blocked_reason"]
                    if blocked_reason == "bilibili_sensitive_words":
                        print("原因: 弹幕包含B站屏蔽词，请修改内容后重试")
                    elif blocked_reason == "streamer_blocked_words":
                        print("原因: 弹幕被主播设置的屏蔽词拦截")

                if send_result.get("api_code"):
                    print(f"B站错误代码: {send_result['api_code']}")
        else:
            print("获取用户信息失败:", user_info.get("error", "未知错误"))
    else:
        print("认证器初始化失败:", authenticator.initialization_result.get("error", "未知错误"))