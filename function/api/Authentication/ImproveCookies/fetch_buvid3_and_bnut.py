from typing import Dict, Any

import requests


class ImproveCookies:
    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """完善浏览器headers"""
        self.headers = headers
        self.verify_ssl = verify_ssl

    def fetch_buvid3_and_bnut(self) -> Dict[str, Any]:
        """
        获取buvid3和b_nut认证信息

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含buvid3和b_nut）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            response = requests.get(
                url='https://www.bilibili.com/',
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取认证信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "response_text": response.text
                }

            cookies_dict = response.cookies.get_dict()

            # 检查是否成功获取到必要的cookies
            required_cookies = ["buvid3", "b_nut"]
            missing_cookies = [cookie for cookie in required_cookies if cookie not in cookies_dict]

            if missing_cookies:
                return {
                    "success": False,
                    "message": "获取认证信息不完整",
                    "error": f"缺少必要的cookies: {', '.join(missing_cookies)}",
                    "status_code": response.status_code,
                    "available_cookies": list(cookies_dict.keys())
                }

            return {
                "success": True,
                "message": "认证信息获取成功",
                "data": {
                    "buvid3": cookies_dict["buvid3"],
                    "b_nut": cookies_dict["b_nut"]
                },
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取认证信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取认证信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取认证信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取认证信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = ImproveCookies(headers, verify_ssl=True)
    result = api.fetch_buvid3_and_bnut()

    if result["success"]:
        print("✓ 认证信息获取成功")
        print(f"   buvid3: {result['data']['buvid3']}")
        print(f"   b_nut: {result['data']['b_nut']}")
    else:
        print("✗ 认证信息获取失败")
        print(f"   错误信息: {result['error']}")
        if result.get("status_code"):
            print(f"   HTTP状态码: {result['status_code']}")