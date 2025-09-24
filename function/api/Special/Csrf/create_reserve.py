import json
import random
import string
from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.parse_cookie import parse_cookie
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.BilibiliUserConfigManager import BilibiliUserConfigManager


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

    def create_reserve(self, title: str, live_plan_start_time: int, create_dynamic: bool = False,
                       business_type: int = 10) -> Dict[str, Any]:
        """
        创建直播预约

        Args:
            title: 预约标题
            live_plan_start_time: 直播计划开始时间(Unix时间戳)
            create_dynamic: 是否同步发布动态(默认False)
            business_type: 业务类型(默认10)

        Returns:
            包含预约结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含sid等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的code
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "创建预约失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 验证必要参数
            if not self.csrf:
                return {
                    "success": False,
                    "message": "创建预约失败",
                    "error": "缺少bili_jct参数，无法获取csrf token",
                    "status_code": None,
                    "api_code": None
                }

            if not title or not live_plan_start_time:
                return {
                    "success": False,
                    "message": "创建预约失败",
                    "error": "标题和开始时间为必填参数",
                    "status_code": None,
                    "api_code": None
                }

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

            response = requests.post(
                verify=self.verify_ssl,
                url=api_url,
                headers=self.headers,
                data=payload,
                timeout=10
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "创建预约失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 根据B站API返回的code判断是否成功
            api_code = result.get("code", -1)
            if api_code == 0:
                # 成功创建预约
                return {
                    "success": True,
                    "message": "预约创建成功",
                    "data": {
                        "sid": result.get("data", {}).get("sid"),
                        "api_response": result
                    },
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # 预约创建失败
                error_message = result.get("message", "未知错误")
                common_errors = {
                    75876: "已超出预约发起上限",
                    75882: "发起直播预约开播时间不可早于当前时间后5分钟",
                    10016: "创建预约失败"
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
                    "api_response": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "创建预约失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "创建预约失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "创建预约失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "创建预约过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


# 使用示例
if __name__ == "__main__":
    # 示例用法
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()
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

            # 创建预约（使用未来的时间戳，例如当前时间+1小时）
            import time

            future_time = int(time.time()) + 3600  # 当前时间+1小时

            reserve_result = authenticator.create_reserve("测试预约标题", future_time)

            if reserve_result["success"]:
                print(f"预约创建成功! 预约ID: {reserve_result['data']['sid']}")
            else:
                print(f"预约创建失败: {reserve_result['error']}")
                if reserve_result.get("api_code"):
                    print(f"B站错误代码: {reserve_result['api_code']}")
        else:
            print("获取用户信息失败:", user_info.get("error", "未知错误"))
    else:
        print("认证器初始化失败:", authenticator.initialization_result.get("error", "未知错误"))