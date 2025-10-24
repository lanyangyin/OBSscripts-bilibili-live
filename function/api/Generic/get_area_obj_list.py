import requests
from typing import Dict, Any


class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_area_obj_list(self) -> Dict[str, Any]:
        """
        获取B站直播分区信息

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（分区信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            api_url = "https://api.live.bilibili.com/room/v1/Area/getList"

            # 发送API请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
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
            data = response.json()

            # 验证API响应
            api_code = data.get("code", -1)
            if api_code != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 检查核心数据结构
            if "data" not in data or not isinstance(data["data"], list):
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "返回数据缺少分区列表",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            return {
                "success": True,
                "message": "获取分区信息成功",
                "data": data["data"],
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(headers)

    # 获取分区信息
    result = api.get_area_obj_list()

    if result["success"]:
        print("获取分区信息成功")
        area_data = result["data"]
        print(f"共有 {len(area_data)} 个父分区")

        # 打印每个父分区及其子分区数量
        for parent_area in area_data:
            parent_id = parent_area["id"]
            parent_name = parent_area["name"]
            sub_areas_count = len(parent_area.get("list", []))
            print(f"父分区: {parent_name} (ID: {parent_id}), 子分区数量: {sub_areas_count}")

            # 可选：打印前几个子分区
            for i, sub_area in enumerate(parent_area.get("list", [])[:3]):  # 只显示前3个
                print(f"  - {sub_area['name']} (ID: {sub_area['id']})")
            if sub_areas_count > 3:
                print(f"  - ... 还有 {sub_areas_count - 3} 个子分区")
            print()
    else:
        print(f"获取分区信息失败: {result['error']}")
        if "response_data" in result:
            print(f"完整响应: {result['response_data']}")