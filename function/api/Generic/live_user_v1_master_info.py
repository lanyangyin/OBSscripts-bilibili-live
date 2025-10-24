import requests
from typing import Dict, Any


class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def live_user_v1_master_info(self, uid: int) -> Dict[str, Any]:
        """
        获取主播信息

        Args:
            uid: 目标用户mid

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（主播信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not uid or uid <= 0:
                return {
                    "success": False,
                    "message": "获取主播信息失败",
                    "error": "用户ID无效",
                    "status_code": None,
                    "api_code": None
                }

            api_url = "https://api.live.bilibili.com/live_user/v1/Master/info"
            params = {
                "uid": uid
            }

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                params=params,
                verify=self.verify_ssl,
                timeout=10
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取主播信息失败",
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
                    "message": "获取主播信息成功",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # 提取错误信息
                error_msg = result.get("msg") or result.get("message", "未知错误")
                return {
                    "success": False,
                    "message": "获取主播信息失败",
                    "error": error_msg,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取主播信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取主播信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取主播信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取主播信息过程中发生未知错误",
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

    # 获取主播信息
    result = api.live_user_v1_master_info(143474500)

    if result["success"]:
        print("获取主播信息成功:")
        data = result["data"]
        print(f"主播用户名: {data.get('info', {}).get('uname', '未知')}")
        print(f"粉丝数: {data.get('follower_num', 0)}")
        print(f"直播间ID: {data.get('room_id', '未知')}")
        print(f"主播等级: {data.get('exp', {}).get('master_level', {}).get('level', '未知')}")
    else:
        print(f"获取主播信息失败: {result['error']}")
        if "response_data" in result:
            print(f"完整响应: {result['response_data']}")