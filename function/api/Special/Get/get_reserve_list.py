from pathlib import Path
from typing import Dict, Any, List

import requests

from function.tools.parse_cookie import parse_cookie
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.BilibiliUserConfigManager import BilibiliUserConfigManager


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


# 使用示例
if __name__ == '__main__':
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()
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
        # 获取预约列表
        reserve_result = room_manager.get_reserve_list()

        if reserve_result["success"]:
            print("预约列表获取成功")
            reserve_list = reserve_result["data"]["list"]
            if reserve_list:
                print(f"找到 {len(reserve_list)} 个预约:")
                for i, reserve in enumerate(reserve_list, 1):
                    reserve_info = reserve.get("reserve_info", {})
                    print(f"{i}. {reserve_info.get('name', '未知预约')} (ID: {reserve_info.get('sid', '未知')})")
            else:
                print("没有找到任何预约")
        else:
            print(f"获取预约列表失败: {reserve_result['error']}")
            if "status_code" in reserve_result and reserve_result["status_code"]:
                print(f"HTTP状态码: {reserve_result['status_code']}")
            if "api_code" in reserve_result:
                print(f"API错误码: {reserve_result['api_code']}")