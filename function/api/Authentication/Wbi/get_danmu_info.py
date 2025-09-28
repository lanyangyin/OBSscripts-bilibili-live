from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.wbi import wbi
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


class WbiSigna:
    def __init__(self, headers: dict, verify_ssl: bool = True):
        """
        wbi签名的api
        @param headers: 包含Cookie和User-Agent的请求头字典
        @param verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
        """
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_danmu_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间弹幕服务器信息

        Args:
            room_id: 直播间真实ID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含弹幕服务器信息等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - api_code: B站API返回的错误码（如果有）
        """
        try:
            # 检查房间ID是否有效
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取弹幕服务器信息失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            # 构建API请求
            url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo'
            params = {
                "id": room_id,
            }

            # 使用wbi签名参数
            signed_params = wbi(params)

            # 发送请求
            response = requests.get(
                url=url,
                headers=self.headers,
                params=signed_params,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取弹幕服务器信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
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
                    "response_data": result
                }

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "api_code": result.get("code"),
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "弹幕服务器信息获取成功",
                "data": result["data"],
                "status_code": response.status_code,
                "api_code": result.get("code")
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取弹幕服务器信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取弹幕服务器信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取弹幕服务器信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取弹幕服务器信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


if __name__ == '__main__':
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    wsa = WbiSigna(Headers)
    result = wsa.get_danmu_info(203227)

    if result["success"]:
        print("弹幕服务器信息获取成功")
        print(f"Token: {result['data'].get('token', '无token')}")
        print(f"Host列表: {result['data'].get('host_list', [])}")
    else:
        print(f"获取弹幕服务器信息失败: {result['error']}")
        if result.get("status_code"):
            print(f"HTTP状态码: {result['status_code']}")
        if result.get("api_code"):
            print(f"API错误码: {result['api_code']}")