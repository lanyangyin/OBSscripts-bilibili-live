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

    def get_bilibili_user_card(self, mid: Union[int, str], photo: bool = False) -> Dict[str, Any]:
        """
        获取Bilibili用户名片信息

        Args:
            mid: 目标用户mid
            photo: 是否请求用户主页头图 (可选，默认为False)

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（用户信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not mid:
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": "用户MID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            # API地址
            url = "https://api.bilibili.com/x/web-interface/card"

            # 请求参数
            params = {
                'mid': mid,
                'photo': 'true' if photo else 'false'
            }

            # 发送GET请求
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            data = response.json()

            # 检查API返回状态
            api_code = data.get('code', -1)
            if api_code != 0:
                error_msg = data.get('message', '未知错误')
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 返回完整的API响应数据
            return {
                "success": True,
                "message": "获取用户信息成功",
                "data": data,  # 返回完整的API响应
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


# 使用示例
if __name__ == "__main__":
    from _Input.function.api import Generic as DataInput
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(Headers, verify_ssl=True)

    # 获取用户mid=143474500的信息，并请求主页头图
    result = api.get_bilibili_user_card(mid=DataInput.get_bilibili_user_card_for_uid, photo=True)

    if result["success"]:
        user_data = result["data"]
        print(json.dumps(user_data, ensure_ascii=False, indent=2))

        # 提取基本信息（可选）
        if 'data' in user_data and 'card' in user_data['data']:
            card = user_data['data']['card']
            print(f"\n用户基本信息:")
            print(f"UID: {card.get('mid')}")
            print(f"昵称: {card.get('name')}")
            print(f"性别: {card.get('sex')}")
            print(f"等级: LV{card.get('level_info', {}).get('current_level', 0)}")
            print(f"签名: {card.get('sign')}")
    else:
        print(f"获取用户信息失败: {result['error']}")
        if "response_data" in result:
            print(f"完整响应: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)}")