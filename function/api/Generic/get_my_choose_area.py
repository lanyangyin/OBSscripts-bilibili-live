import json
import requests
from typing import Dict, Any, List, Union, Optional


class BilibiliApiGeneric:
    """
    不登录也能使用的Bilibili API集合

    提供不需要认证即可访问的Bilibili API功能
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_anchor_common_areas(self, room_id: Union[str, int]) -> Dict[str, Any]:
        """
        获取主播常用分区信息

        参数:
            room_id: 直播间ID（整数或字符串）

        返回:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（分区列表）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not room_id:
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "房间ID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            # API配置
            api_url = "https://api.live.bilibili.com/room/v1/Area/getMyChooseArea"
            params = {"roomid": str(room_id)}

            # 发送API请求
            response = requests.get(
                api_url,
                headers=self.headers,
                params=params,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            result = response.json()

            # 验证基本结构
            if not isinstance(result, dict) or "code" not in result:
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "API返回无效的响应格式",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_data": result
                }

            # 检查API错误码
            api_code = result.get("code", -1)
            if api_code != 0:
                error_msg = result.get("message") or result.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], list):
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "API返回数据格式无效",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证分区数据
            for area in result["data"]:
                required_keys = {"id", "name", "parent_id", "parent_name"}
                if not required_keys.issubset(area.keys()):
                    return {
                        "success": False,
                        "message": "获取分区信息失败",
                        "error": "分区数据缺少必需字段",
                        "status_code": response.status_code,
                        "api_code": api_code,
                        "response_data": result
                    }

            return {
                "success": True,
                "message": "获取分区信息成功",
                "data": result["data"],
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取分区信息过程中发生未知错误",
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

    try:
        # 获取主播常用分区
        room_id = 25322725
        result = api.get_anchor_common_areas(room_id)

        if result["success"]:
            print(json.dumps(result["data"], ensure_ascii=False, indent=2))

            # 处理结果
            print(f"\n主播房间 {room_id} 的常用分区:")
            for area in result["data"]:
                print(f"- {area['name']} (ID: {area['id']}, 父分区: {area['parent_name']})")

            # 生成分区映射
            area_mapping = {area['id']: f"⭐{area['name']}" for area in result["data"]}
            print(f"\n分区映射: {area_mapping}")

            # 生成父分区到子分区的映射
            parent_child_mapping = {}
            for area in result["data"]:
                parent_id = area['parent_id']
                child_id = area['id']
                if parent_id not in parent_child_mapping:
                    parent_child_mapping[parent_id] = []
                parent_child_mapping[parent_id].append(child_id)

            print(f"父分区到子分区映射: {parent_child_mapping}")

        else:
            print(f"获取分区信息失败: {result['error']}")
            if "response_data" in result:
                print(f"完整响应: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)}")

    except Exception as e:
        print(f"错误: {e}")