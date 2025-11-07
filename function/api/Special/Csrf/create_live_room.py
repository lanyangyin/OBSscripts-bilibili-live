from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.EncodingConversion.parse_cookie import parse_cookie


class BilibiliCSRFAuthenticator:
    """
    B站CSRF认证管理器，用于处理需要CSRF令牌的API请求。

    该类专门用于B站直播相关的CSRF认证操作，特别是直播公告的更新。
    自动从Cookie中提取必要的认证信息，并提供简化的API调用接口。

    特性：
    - 自动从Cookie中解析CSRF令牌（bili_jct）
    - 自动提取用户ID（DedeUserID）
    - 支持SSL验证配置
    - 提供直播公告更新功能
    - 统一的错误处理和响应格式
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

    def create_live_room(self) -> Dict[str, Any]:
        """
        开通直播间（创建直播间房间）

        Returns:
            包含开通结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含room_id等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - api_code: B站API返回的错误码（如果有）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "开通直播间失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 检查必要的CSRF token
            if not self.csrf:
                return {
                    "success": False,
                    "message": "开通直播间失败",
                    "error": "缺少bili_jct值，无法进行CSRF验证",
                    "status_code": None,
                    "api_code": None
                }

            api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/preLive/CreateRoom"

            # 准备请求数据
            data = {
                "platform": "web",
                "visit_id": "",
                "csrf": self.csrf,
                "csrf_token": self.csrf,
            }

            # 发送POST请求
            response = requests.post(
                url=api_url,
                data=data,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "开通直播间失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            result = response.json()

            # 处理已知的成功和失败情况
            api_code = result.get("code", 0)

            # 成功情况
            if api_code == 0:
                return {
                    "success": True,
                    "message": "直播间开通成功",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }

            # 已知的失败情况
            elif api_code == 1531193016:  # 已经创建过直播间
                return {
                    "success": True,  # 虽然API返回错误码，但从业务角度看是成功的（已存在）
                    "message": "直播间已存在",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }

            # 其他失败情况
            else:
                return {
                    "success": False,
                    "message": "开通直播间失败",
                    "error": result.get("message", "未知错误"),
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "开通直播间失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "开通直播间失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "开通直播间失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "开通直播间过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
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
    if not authenticator.initialization_result["success"]:
        print(f"认证器初始化失败: {authenticator.initialization_result['error']}")
    else:
        # 开通直播间
        create_result = authenticator.create_live_room()

        if create_result["success"]:
            if create_result["api_code"] == 0:
                print("直播间开通成功")
                print(f"房间信息: {create_result['data']}")
            elif create_result["api_code"] == 1531193016:
                print("直播间已存在")
                print(f"房间信息: {create_result['data']}")
        else:
            print(f"开通直播间失败: {create_result['error']}")
            if create_result["api_code"] == -802:
                print("需要实名认证，请前往哔哩哔哩或直播姬app开播一次完成实名认证")
            if "status_code" in create_result and create_result["status_code"]:
                print(f"HTTP状态码: {create_result['status_code']}")
            if "api_code" in create_result:
                print(f"API错误码: {create_result['api_code']}")