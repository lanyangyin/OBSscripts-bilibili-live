import json
import requests
from typing import Dict, Any


class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_room_base_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间基本信息

        Args:
            room_id: 直播间短ID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（直播间信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            api_url = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
            params = {
                "req_biz": "web_room_componet",
                "room_ids": room_id
            }

            # 发送API请求
            response = requests.get(
                api_url,
                headers=self.headers,
                params=params,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            data = response.json()

            # 验证API响应
            api_code = data.get("code", -1)
            if api_code != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 提取房间信息
            by_room_ids = data.get("data", {}).get("by_room_ids", {})
            if not by_room_ids:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "未找到房间信息",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 返回第一个房间信息（即使多个也取第一个）
            room_info = next(iter(by_room_ids.values()), None)
            if not room_info:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "房间信息为空",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            return {
                "success": True,
                "message": "获取房间信息成功",
                "data": room_info,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取房间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


if __name__ == "__main__":
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(Headers, verify_ssl=True)

    # 获取直播间信息（使用短ID）
    result = api.get_room_base_info(25322725)

    if result["success"]:
        room_info = result["data"]
        print(json.dumps(room_info, ensure_ascii=False, indent=2))

        # 打印基本信息
        print(f"直播间标题: {room_info['title']}")
        print(f"主播: {room_info['uname']}")
        print(f"状态: {'直播中' if room_info['live_status'] == 1 else '未开播'}")
        print(f"在线人数: {room_info['online']}")
    else:
        print(f"获取直播间信息失败: {result['error']}")
        if "response_data" in result:
            print(f"完整响应: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)}")