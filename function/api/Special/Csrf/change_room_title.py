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

    def change_room_title(self, room_id: int, title: str) -> Dict[str, Any]:
        """
        更新直播标题

        Args:
            room_id: 直播间ID
            title: 新的直播标题

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "更改标题失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 验证输入参数
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "更改标题失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            if not title or len(title.strip()) == 0:
                return {
                    "success": False,
                    "message": "更改标题失败",
                    "error": "标题不能为空",
                    "status_code": None,
                    "api_code": None
                }

            # 准备请求参数
            headers = self.headers.copy()
            csrf = self.csrf
            api_url = "https://api.live.bilibili.com/room/v1/Room/update"
            data = {
                'room_id': room_id,
                'title': title,
                'csrf_token': csrf,
                'csrf': csrf
            }

            # 发送请求
            response = requests.post(
                url=api_url,
                headers=headers,
                data=data,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "更改标题失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 根据B站API返回的状态码判断成功与否
            api_code = result.get("code", -1)
            if api_code == 0:
                return {
                    "success": True,
                    "message": "标题更改成功",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # 提取错误信息
                error_msg = result.get("msg") or result.get("message", "未知错误")
                return {
                    "success": False,
                    "message": "标题更改失败",
                    "error": error_msg,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "更改标题失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "更改标题失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "更改标题失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "更改标题过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


# 使用示例
if __name__ == "__main__":
    from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
    from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
    from function.api.Special.Default import BilibiliSpecialApiManager as GetRoomHighlightInfo
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

    # 创建房间信息管理器实例
    ghi = GetRoomHighlightInfo(Headers)

    # 检查初始化结果
    if authenticator.initialization_result["success"]:
        # 获取用户信息
        user_info = authenticator.get_user_info()
        if user_info["success"]:
            # 获取房间高亮信息
            highlight_info = ghi.get_room_highlight_info()

            if highlight_info["success"]:
                room_id = highlight_info["data"]["room_id"]
                result = authenticator.change_room_title(room_id, DataInput.change_room_title)

                if result["success"]:
                    print(f"标题更改成功: {result['message']}")
                    print(f"审核信息: {result['data'].get('audit_info', {})}")
                else:
                    print(f"标题更改失败: {result['error']}")
                    print(f"API错误码: {result.get('api_code', '未知')}")
                    if "response_data" in result:
                        print(f"完整响应: {result['response_data']}")
            else:
                print(f"获取房间信息失败: {highlight_info['error']}")
        else:
            print(f"获取用户信息失败: {user_info['error']}")
    else:
        print(f"认证器初始化失败: {authenticator.initialization_result['error']}")