from typing import Dict, Any

import requests


class ImproveCookies:
    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """完善浏览器headers"""
        self.headers = headers.copy()
        self.verify_ssl = verify_ssl

    def fetch_buvid3_info(self) -> Dict[str, Any]:
        """
        获取B站BUVID3信息

        Returns:
            包含BUVID3信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含buvid3等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 发送API请求获取buvid3
            response = requests.get(
                url='https://api.bilibili.com/x/web-frontend/getbuvid',
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取BUVID3失败",
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

            # 检查数据是否存在
            if "data" not in result or "buvid" not in result["data"]:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的buvid字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "BUVID3获取成功",
                "data": {
                    "buvid3": result["data"]["buvid"]
                },
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取BUVID3失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取BUVID3失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取BUVID3失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取BUVID3过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


if __name__ == '__main__':
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    # 创建实例并获取BUVID3信息
    cookie_improver = ImproveCookies(Headers)
    buvid_result = cookie_improver.fetch_buvid3_info()

    # 美化输出
    if buvid_result["success"]:
        print("✓ BUVID3获取成功")
        print(f"  BUVID3: {buvid_result['data']['buvid3']}")
        print(f"  状态码: {buvid_result['status_code']}")
    else:
        print("✗ BUVID3获取失败")
        print(f"  错误信息: {buvid_result['error']}")
        if buvid_result.get("status_code"):
            print(f"  HTTP状态码: {buvid_result['status_code']}")
        if buvid_result.get("api_code"):
            print(f"  API错误码: {buvid_result['api_code']}")