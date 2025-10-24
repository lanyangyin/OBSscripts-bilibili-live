import time
from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.EncodingConversion.parse_cookie import parse_cookie
from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


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

    def get_fans_members_rank(self, uid: int) -> Dict[str, Any]:
        """
        获取指定用户的粉丝团成员列表

        Args:
            uid: 要查询的B站用户UID

        Returns:
            包含查询结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的粉丝团成员列表数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - total_count: 总成员数量（成功时）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取粉丝团成员列表失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 验证UID参数
            if not uid or uid <= 0:
                return {
                    "success": False,
                    "message": "获取粉丝团成员列表失败",
                    "error": "无效的用户UID",
                    "status_code": None
                }

            api_url = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank"
            headers = self.headers
            page = 1
            fans_members = []
            has_more_data = True
            max_retries = 3

            while has_more_data:
                params = {
                    "ruid": uid,
                    "page": page,
                    "page_size": 30,
                }

                # 添加重试机制
                for attempt in range(max_retries):
                    try:
                        response = requests.get(
                            api_url,
                            headers=headers,
                            params=params,
                            verify=self.verify_ssl,
                            timeout=30
                        )

                        # 检查HTTP状态码
                        if response.status_code != 200:
                            if attempt < max_retries - 1:
                                time.sleep(2)  # 等待后重试
                                continue
                            else:
                                return {
                                    "success": False,
                                    "message": "获取粉丝团成员列表失败",
                                    "error": f"HTTP错误: {response.status_code}",
                                    "status_code": response.status_code
                                }

                        result = response.json()

                        # 检查API返回状态
                        if result.get("code") != 0:
                            return {
                                "success": False,
                                "message": "B站API返回错误",
                                "error": result.get("message", "未知错误"),
                                "status_code": response.status_code,
                                "api_code": result.get("code")
                            }

                        # 处理数据
                        current_page_items = result["data"].get("item", [])
                        if current_page_items:
                            fans_members.extend(current_page_items)
                            page += 1
                        else:
                            has_more_data = False

                        break  # 成功获取数据，跳出重试循环

                    except requests.exceptions.Timeout:
                        if attempt < max_retries - 1:
                            time.sleep(5)  # 超时后等待5秒重试
                            continue
                        else:
                            return {
                                "success": False,
                                "message": "获取粉丝团成员列表失败",
                                "error": "请求超时",
                                "status_code": None
                            }
                    except requests.exceptions.RequestException as e:
                        if attempt < max_retries - 1:
                            time.sleep(5)  # 网络错误后等待5秒重试
                            continue
                        else:
                            return {
                                "success": False,
                                "message": "获取粉丝团成员列表失败",
                                "error": f"网络请求异常: {str(e)}",
                                "status_code": None
                            }

            # 成功返回
            return {
                "success": True,
                "message": "粉丝团成员列表获取成功",
                "data": fans_members,
                "total_count": len(fans_members),
                "status_code": 200
            }

        except Exception as e:
            return {
                "success": False,
                "message": "获取粉丝团成员列表过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


# 使用示例
if __name__ == "__main__":
    # 示例用法
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
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

            # 获取粉丝团成员列表
            fans_result = authenticator.get_fans_members_rank(7062987)

            if fans_result["success"]:
                print(f"成功获取 {fans_result['total_count']} 名粉丝团成员")
                print("粉丝团成员列表:", fans_result["data"])
            else:
                print(f"获取粉丝团成员列表失败: {fans_result['error']}")
        else:
            print("获取用户信息失败:", user_info.get("error", "未知错误"))
    else:
        print("认证器初始化失败:", authenticator.initialization_result.get("error", "未知错误"))