from typing import Dict, Any

import requests


class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_room_info_old(self, mid: int) -> Dict[str, Any]:
        """
        通过B站UID查询直播间基础信息

        Args:
            mid: B站用户UID

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
            # 参数验证
            if not isinstance(mid, int) or mid <= 0:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "mid 必须是正整数",
                    "status_code": None,
                    "api_code": None
                }

            api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
            params = {"mid": mid}

            # 发送请求
            response = requests.get(
                url=api,
                headers=self.headers,
                params=params,
                timeout=5.0,
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
            try:
                data = response.json()
            except ValueError as e:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"解析API响应失败: {str(e)}",
                    "status_code": response.status_code,
                    "api_code": None
                }

            # 检查API返回状态码
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

            # 检查数据是否存在
            result = data.get("data")
            if not result:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "API返回数据为空",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 确保返回完整字段结构
            room_info = {
                "roomStatus": result.get("roomStatus"),
                "roundStatus": result.get("roundStatus"),
                "liveStatus": result.get("liveStatus"),
                "url": result.get("url"),
                "title": result.get("title"),
                "cover": result.get("cover"),
                "online": result.get("online"),
                "roomid": result.get("roomid"),
                "broadcast_type": result.get("broadcast_type"),
                "online_hidden": result.get("online_hidden"),
                "link": result.get("link")  # 添加link字段
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(headers, verify_ssl=True)

    # 获取房间信息
    result = api.get_room_info_old(143474500)

    if result["success"]:
        print("获取房间信息成功:")
        print(f"房间状态: {result['data']['roomStatus']}")
        print(f"直播状态: {result['data']['liveStatus']}")
        print(f"标题: {result['data']['title']}")
        print(f"在线人数: {result['data']['online']}")
        print(f"房间ID: {result['data']['roomid']}")
        print(result)
    else:
        print(f"获取房间信息失败: {result['error']}")
        if "response_data" in result:
            print(f"完整响应: {result['response_data']}")