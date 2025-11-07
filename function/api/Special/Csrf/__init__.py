import hashlib
import json
import random
import string
import time
from pathlib import Path
from typing import Dict, Any, Literal

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

    def cancel_reserve(self, sid: int, from_value: int = 13) -> Dict[str, Any]:
        """
        取消直播预约

        Args:
            sid: 预约活动ID
            from_value: 来源标识（默认13）

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功（基于API返回的code）
            - message: 结果描述信息
            - data: API返回的完整数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: API返回的code
        """
        # 检查认证器是否正常初始化
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": "认证器未正确初始化",
                "status_code": None,
                "api_code": None,
                "data": None
            }

        # 检查CSRF token
        if not self.csrf:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": "缺少bili_jct值，无法进行身份验证",
                "status_code": None,
                "api_code": None,
                "data": None
            }

        # 检查sid参数
        if not sid or sid <= 0:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": "无效的预约活动ID",
                "status_code": None,
                "api_code": None,
                "data": None
            }

        try:
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

            # 发送POST请求
            response = requests.post(
                url="https://api.live.bilibili.com/xlive/app-ucenter/v2/schedule/CancelReserve",
                headers=self.headers,
                data=payload,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "取消预约失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            result = response.json()

            # 根据API返回的code判断操作是否成功
            api_code = result.get("code", -1)
            is_success = (api_code == 0)

            return {
                "success": is_success,
                "message": result.get("message", "操作完成"),
                "data": result,
                "error": None if is_success else result.get("message", "未知错误"),
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None,
                "data": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None,
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None,
                "data": None
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "message": "取消预约失败",
                "error": f"解析响应失败: {str(e)}",
                "status_code": None,
                "api_code": None,
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "取消预约过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None,
                "data": None
            }

    def change_room_area(self, room_id: int, area_id: int) -> Dict[str, Any]:
        """
        更改直播分区

        Args:
            room_id: 直播间ID
            area_id: 二级分区ID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（如sub_session_key）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的code
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "更改分区失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 构建API请求
            api = "https://api.live.bilibili.com/xlive/app-blink/v2/room/AnchorChangeRoomArea"
            headers = self.headers.copy()
            csrf = self.csrf

            params = {
                "platform": "pc",
                "room_id": room_id,
                "area_id": area_id,
                "csrf": csrf,
                "csrf_token": csrf,
            }

            # 发送请求
            response = requests.post(
                url=api,
                headers=headers,
                params=params,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "更改分区失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()
            api_code = result.get("code", -1)

            # 根据API返回的code判断操作结果
            if api_code == 0:
                return {
                    "success": True,
                    "message": "分区更改成功",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                error_message = result.get("message", "未知错误")
                return {
                    "success": False,
                    "message": f"分区更改失败: {error_message}",
                    "error": error_message,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "更改分区失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "更改分区失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "更改分区失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "更改分区过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def change_room_news(self, room_id: int, content: str) -> Dict[str, Any]:
        """
        更新直播公告

        Args:
            room_id: 直播间ID
            content: 公告内容

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（API返回的data字段）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "更新直播公告失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 验证输入参数
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "更新直播公告失败",
                    "error": "直播间ID无效",
                    "status_code": None
                }

            if not content or len(content.strip()) == 0:
                return {
                    "success": False,
                    "message": "更新直播公告失败",
                    "error": "公告内容不能为空",
                    "status_code": None
                }

            headers = self.headers.copy()
            csrf = self.csrf

            api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/updateRoomNews"
            updateRoomNews_data = {
                'room_id': room_id,
                'uid': self.cookies["DedeUserID"],
                'content': content,
                'csrf_token': csrf,
                'csrf': csrf
            }

            # 发送请求
            response = requests.post(
                verify=self.verify_ssl,
                url=api,
                headers=headers,
                data=updateRoomNews_data,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "更新直播公告失败",
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
                "message": "直播公告更新成功",
                "data": result.get("data", {}),
                "status_code": response.status_code,
                "api_response": result  # 包含完整的API响应
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "更新直播公告失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "更新直播公告失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "更新直播公告失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "更新直播公告过程中发生未知错误",
                "error": str(e),
                "status_code": None
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

    def get_dynamic(self, host_mid: int, all: bool = False) -> Dict[str, Any]:
        """
        获取用户动态列表

        Args:
            host_mid: 用户ID
            all: 是否获取全部动态（分页获取）

        Returns:
            包含动态列表的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的动态数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取动态列表失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 检查用户ID是否有效
            if not host_mid or host_mid <= 0:
                return {
                    "success": False,
                    "message": "获取动态列表失败",
                    "error": "用户ID无效",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
            params = {
                "offset": "",
                "host_mid": host_mid
            }

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
                    "message": "获取动态列表失败",
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

            # 检查数据是否存在
            if "data" not in result or "items" not in result["data"]:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 获取动态数据
            dynamics = result["data"]["items"]

            # 如果需要获取全部动态，则继续分页请求
            if all and result["data"].get("has_more", False):
                while result["data"].get("has_more", False):
                    params["offset"] = result["data"].get("offset", "")

                    # 发送分页请求
                    response = requests.get(
                        url=api_url,
                        headers=self.headers,
                        params=params,
                        verify=self.verify_ssl,
                        timeout=30
                    )

                    # 检查HTTP状态码
                    if response.status_code != 200:
                        break

                    # 解析响应
                    result = response.json()

                    # 检查B站API返回状态
                    if result.get("code") != 0:
                        break

                    # 检查数据是否存在
                    if "data" not in result or "items" not in result["data"]:
                        break

                    # 添加新获取的动态
                    for item in result["data"]["items"]:
                        if item not in dynamics:
                            dynamics.append(item)

            # 成功返回
            return {
                "success": True,
                "message": "动态列表获取成功",
                "data": dynamics,
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取动态列表失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取动态列表失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取动态列表失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取动态列表过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_emoticons(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间表情列表

        Args:
            room_id: 直播间ID

        Returns:
            包含表情列表的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（表情列表）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取表情列表失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 检查房间ID是否有效
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取表情列表失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/web-ucenter/v2/emoticon/GetEmoticons"
            params = {
                "platform": "pc",
                "room_id": room_id
            }

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
                    "message": "获取表情列表失败",
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

            # 检查数据是否存在
            if "data" not in result or "data" not in result["data"]:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "表情列表获取成功",
                "data": result["data"]["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取表情列表失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取表情列表失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取表情列表失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取表情列表过程中发生未知错误",
                "error": str(e),
                "status_code": None
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

    def get_navigation_info(self) -> Dict[str, Any]:
        """
        获取登录后导航栏用户信息

        Returns:
            包含导航信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含用户详细信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取导航信息失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.bilibili.com/x/web-interface/nav"

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取导航信息失败",
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

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "导航信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取导航信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取导航信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取导航信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取导航信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_user_live_info(self) -> Dict[str, Any]:
        """
        获取用户直播相关信息

        Returns:
            包含用户直播信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含用户直播信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取用户直播信息失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/web-ucenter/user/get_user_info"

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取用户直播信息失败",
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

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "用户直播信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户直播信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户直播信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户直播信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户直播信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def rename_fans_medal(self, medal_name: str) -> Dict[str, Any]:
        """
        修改粉丝勋章名称

        Args:
            medal_name: 新的粉丝勋章名称

        Returns:
            包含操作结果的字典，固定键名：
            - success: 操作是否成功（布尔值）
            - message: 操作结果消息
            - data: 附加数据（字典）
            - error: 错误信息（失败时存在）
            - status_code: HTTP状态码
            - api_code: B站API返回的代码
        """
        # 检查认证器是否正常初始化
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "message": "操作失败",
                "error": "认证器未正确初始化",
                "status_code": None,
                "api_code": None
            }

        api_url = "https://api.live.bilibili.com/fans_medal/v1/medal/rename"

        try:
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

            # 发送POST请求
            response = requests.post(
                api_url,
                headers=headers,
                data=params,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "请求失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 尝试解析JSON响应
            try:
                result = response.json()
            except ValueError:
                return {
                    "success": False,
                    "message": "响应解析失败",
                    "error": "无法解析JSON响应",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 根据B站API返回的code判断操作结果
            api_code = result.get("code", -1)
            api_message = result.get("message", result.get("msg", "未知错误"))

            if api_code == 0:
                return {
                    "success": True,
                    "message": "粉丝勋章名称修改成功",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                return {
                    "success": False,
                    "message": f"B站API返回错误: {api_message}",
                    "error": api_message,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "请求超时",
                "error": "网络请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "网络连接错误",
                "error": "无法连接到服务器",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "网络请求异常",
                "error": f"请求失败: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "操作过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def start_live(self, room_id: int, area_id: int, platform: Literal["pc_link", "web_link", "android_link"]) -> Dict:
        """
        开始直播

        Args:
            room_id: 直播间ID
            area_id: 二级分区id
            platform: 直播平台

        Returns:
            包含开播结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含直播流信息等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的code
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 参数验证
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            if not area_id or area_id <= 0:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "分区ID无效",
                    "status_code": None,
                    "api_code": None
                }

            if platform not in ["pc_link", "web_link", "android_link"]:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "平台参数无效",
                    "status_code": None,
                    "api_code": None
                }

            api = "https://api.live.bilibili.com/room/v1/Room/startLive"
            headers = self.headers
            csrf = self.csrf

            # 构建请求参数
            startLivedata = {
                "access_key": "",  # 留空
                "appkey": "aae92bc66f3edfab",  # 固定应用密钥
                "platform": platform,
                "room_id": room_id,
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

            # 发送请求
            response = requests.post(
                url=api,
                headers=headers,
                params=startLivedata,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()
            api_code = result.get("code")

            # 判断开播结果
            if api_code == 0:
                # 开播成功或重复开播
                change_status = result.get("data", {}).get("change", 0)
                if change_status == 1:
                    message = "开播成功"
                else:
                    message = result.get("message", "重复开播")

                return {
                    "success": True,
                    "message": message,
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # 开播失败
                error_msg = result.get("message", "未知错误")
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": error_msg,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "开播失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "开播失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "开播失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "开播过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def stop_live(self, room_id: int, platform: Literal["pc_link", "web_link", "android_link"]) -> Dict[str, Any]:
        """
        结束直播

        Args:
            room_id: 直播间ID
            platform: 平台类型

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的代码
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "结束直播失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/room/v1/Room/stopLive"
            headers = self.headers.copy()
            csrf = self.csrf

            data = {
                "platform": platform,
                "room_id": room_id,
                "csrf": csrf,
                "csrf_token": csrf,
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
                    "message": "结束直播失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()
            api_code = result.get("code")

            # 判断操作是否成功
            if api_code == 0:
                # 成功结束直播（包括重复关播的情况）
                return {
                    "success": True,
                    "message": result.get("message", "结束直播成功"),
                    "data": {
                        "change": result.get("data", {}).get("change", 0),
                        "status": result.get("data", {}).get("status", ""),
                        "raw_response": result
                    },
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # API返回错误
                return {
                    "success": False,
                    "message": "结束直播失败",
                    "error": result.get("message", "未知错误"),
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "结束直播失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "结束直播失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "结束直播失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "结束直播过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def update_cover(self, cover_url: str) -> Dict[str, Any]:
        """
        更新直播间封面

        Args:
            cover_url: 通过上传接口获取的封面图片URL

        Returns:
            包含更新结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "更新封面失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 检查封面URL是否有效
            if not cover_url or not cover_url.startswith(('http://', 'https://')):
                return {
                    "success": False,
                    "message": "更新封面失败",
                    "error": "封面URL无效",
                    "status_code": None
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

            # 发送请求
            response = requests.post(
                api_url,
                headers=self.headers,
                data=update_cover_data,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "更新封面失败",
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
                "message": "直播间封面更新成功",
                "data": result.get("data", {}),
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "更新封面失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "更新封面失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "更新封面失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "更新封面过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def upload_cover(self, image_binary: bytes) -> Dict[str, Any]:
        """
        上传直播间封面到B站(符合官方请求格式)

        Args:
            image_binary: png/jpeg图像的二进制格式数据

        Returns:
            包含上传结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（如图片URL）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "上传失败",
                    "error": "认证器未正确初始化",
                    "status_code": None
                }

            # 检查图片数据是否有效
            if not image_binary or len(image_binary) == 0:
                return {
                    "success": False,
                    "message": "上传失败",
                    "error": "图片数据为空或无效",
                    "status_code": None
                }

            # 构建请求参数
            api_url = "https://api.bilibili.com/x/upload/web/image"

            # 准备multipart/form-data数据
            boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            headers = self.headers.copy()  # 复制headers避免修改原始数据
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

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
            response = requests.post(
                url=api_url,
                headers=headers,
                data=body,
                verify=self.verify_ssl,
                timeout=30  # 添加超时设置
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "上传失败",
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

            # 成功返回 - 修正为使用location字段
            if 'data' in result and 'location' in result['data']:
                return {
                    "success": True,
                    "message": "封面上传成功",
                    "data": {
                        "location": result['data']['location'],
                        "etag": result['data'].get('etag', ''),
                        "image_url": result['data']['location']  # 使用location作为图片URL
                    },
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "message": "上传响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "上传失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "上传失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "上传失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "上传过程中发生未知错误",
                "error": str(e),
                "status_code": None
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
            error_message = user_info.get("data", "未知错误")
        else:
            # 处理获取用户信息失败的情况
            error_message = user_info.get("error", "未知错误")
            # 在这里处理错误
    else:
        # 处理初始化失败的情况
        error_message = authenticator.initialization_result.get("error", "未知错误")
        # 在这里处理错误
    print(error_message)
