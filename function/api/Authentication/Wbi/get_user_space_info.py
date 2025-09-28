from pathlib import Path

import requests

from function.tools.wbi import wbi
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


class WbiSigna:
    def __init__(self, headers: dict, verify_ssl: bool = True):
        """
        wbi签名的api
        Args:
            headers: 包含Cookie等认证信息的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
        """
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_user_space_info(self, mid: int) -> dict:
        """
        获取用户空间详细信息

        Args:
            mid: 目标用户mid

        Returns:
            包含用户空间信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的用户数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查用户ID是否有效
            if not mid or mid <= 0:
                return {
                    "success": False,
                    "message": "获取用户空间信息失败",
                    "error": "用户ID无效",
                    "status_code": None,
                    "data": None
                }

            # 构建API请求
            api_url = "https://api.bilibili.com/x/space/wbi/acc/info"
            params = wbi({"mid": mid})

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
                    "message": "获取用户空间信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "data": None,
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
                    "api_code": result.get("code"),
                    "data": None
                }

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "data": None,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "用户空间信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": "请求超时",
                "status_code": None,
                "data": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户空间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "data": None
            }


# 使用示例
if __name__ == '__main__':
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建实例
    wbi_signa = WbiSigna(Headers)

    # 获取用户空间信息（示例用户ID）
    user_info = wbi_signa.get_user_space_info(143474500)

    if user_info["success"]:
        print("用户空间信息获取成功")
        data = user_info["data"]
        print(f"用户昵称: {data.get('name', '未知')}")
        print(f"用户等级: {data.get('level', '未知')}")
        print(f"签名: {data.get('sign', '无签名')}")
        print(f"粉丝勋章: {data.get('fans_medal', {}).get('medal', {}).get('medal_name', '无')}")
    else:
        print(f"获取用户空间信息失败: {user_info['error']}")
        if "status_code" in user_info and user_info["status_code"]:
            print(f"HTTP状态码: {user_info['status_code']}")
        if "api_code" in user_info:
            print(f"API错误码: {user_info['api_code']}")