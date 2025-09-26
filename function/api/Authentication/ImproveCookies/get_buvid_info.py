from typing import Dict, Any

import requests


class ImproveCookies:
    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """完善浏览器headers"""
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_buvid_info(self) -> Dict[str, Any]:
        """
        获取B站buvid3和buvid4信息

        Returns:
            包含buvid信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含b_3和b_4字段）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 发送API请求获取buvid信息
            response = requests.get(
                url="https://api.bilibili.com/x/frontend/finger/spi",
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取buvid信息失败",
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
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "buvid信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取buvid信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取buvid信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取buvid信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取buvid信息过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


if __name__ == '__main__':
    # 配置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    # 创建实例并获取buvid信息
    cookie_improver = ImproveCookies(headers)
    result = cookie_improver.get_buvid_info()

    # 美化输出结果
    if result["success"]:
        print("✓ buvid信息获取成功")
        print(f"   状态码: {result['status_code']}")
        print(f"   buvid3: {result['data'].get('b_3', '未获取到')}")
        print(f"   buvid4: {result['data'].get('b_4', '未获取到')}")
    else:
        print("✗ buvid信息获取失败")
        print(f"   错误信息: {result['error']}")
        if result.get("status_code"):
            print(f"   HTTP状态码: {result['status_code']}")
        if result.get("api_code"):
            print(f"   API错误码: {result['api_code']}")