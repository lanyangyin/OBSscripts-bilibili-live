from typing import Dict, Any

import requests

from function.tools.EncodingConversion.parse_cookie import parse_cookie
from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


class BilibiliRoomInfoManager:
    """
    B站直播间信息管理器，用于获取直播间相关状态信息。

    该类专门用于获取B站直播间的各种状态信息，如房间ID、高亮状态等。
    自动从Cookie中提取必要的认证信息，并提供简化的API调用接口。

    特性：
    - 自动从Cookie中解析必要认证信息
    - 支持SSL验证配置
    - 提供直播间状态信息获取功能
    - 统一的错误处理和响应格式
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化直播间信息管理器

        Args:
            headers: 包含Cookie等认证信息的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
        """
        self.headers = headers.copy()  # 避免修改原始headers
        self.verify_ssl = verify_ssl
        self.initialization_result = self._initialize_manager()

    def _initialize_manager(self) -> Dict[str, Any]:
        """
        初始化管理器的内部实现

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
            required_fields = ["DedeUserID"]
            missing_fields = [field for field in required_fields if field not in self.cookies]
            if missing_fields:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": f"Cookie中缺少必要字段: {', '.join(missing_fields)}"
                }

            self.user_id = self.cookies["DedeUserID"]

            return {
                "success": True,
                "message": "直播间信息管理器初始化成功",
                "data": {
                    "user_id": self.user_id
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": "初始化过程中发生异常",
                "error": str(e)
            }

    def get_live_stream_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间推流信息

        Args:
            room_id: 直播间房间ID

        Returns:
            包含推流信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含推流地址等信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取推流信息失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 检查房间ID是否有效
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取推流信息失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/live_stream/v1/StreamList/get_stream_by_roomId"
            params = {"room_id": room_id}

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
                    "message": "获取推流信息失败",
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
                "message": "推流信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取推流信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取推流信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取推流信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取推流信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_nav_info(self) -> Dict[str, Any]:
        """
        获取导航栏用户信息（需要登录）

        Returns:
            包含用户信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含用户信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": "管理器未正确初始化",
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
                    "message": "获取用户信息失败",
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

            # 检查用户是否已登录
            if not result.get("data", {}).get("isLogin", False):
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": "用户未登录",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "用户信息获取成功",
                "data": result.get("data", {}),
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_reserve_list(self) -> Dict[str, Any]:
        """
        获取用户直播预约列表

        Returns:
            包含预约列表结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含预约列表）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取预约列表失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/app-ucenter/v2/schedule/GetReserveList"

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
                    "message": "获取预约列表失败",
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

            # 成功返回 - 处理list为None的情况
            list_data = result.get("data", {}).get("list")
            if list_data is None:
                # 当list为None时，转换为空列表
                list_data = []

            return {
                "success": True,
                "message": "预约列表获取成功",
                "data": {
                    "list": list_data,
                    "full_response": result  # 包含完整的API响应
                },
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取预约列表失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取预约列表失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取预约列表失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取预约列表过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_room_highlight_info(self) -> Dict[str, Any]:
        """
        获取直播间高亮状态信息，包括房间ID

        Returns:
            包含房间信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含room_id等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/highlight/getRoomHighlightState"

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
                    "message": "获取房间信息失败",
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
            if "data" not in result or "room_id" not in result["data"]:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的房间信息字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "房间信息获取成功",
                "data": {
                    "room_id": result["data"]["room_id"],
                    "highlight_info": result["data"]  # 包含所有高亮状态信息
                },
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取房间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def get_room_news(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间公告信息

        Args:
            room_id: 直播间ID

        Returns:
            包含公告信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含公告内容等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取直播间公告失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 检查房间ID是否有效
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取直播间公告失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getRoomNews"
            params = {
                'room_id': room_id,
                'uid': self.cookies["DedeUserID"]
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
                    "message": "获取直播间公告失败",
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
                "message": "直播间公告获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取直播间公告失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取直播间公告失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取直播间公告失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取直播间公告过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }



# 使用示例
if __name__ == '__main__':
    from _Input.function.api.Special import Room as DataInput
    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建管理器实例
    room_manager = BilibiliRoomInfoManager(Headers)

    # 检查管理器是否初始化成功
    if not room_manager.initialization_result["success"]:
        print(f"管理器初始化失败: {room_manager.initialization_result['error']}")
    else:
        print(room_manager.initialization_result)
