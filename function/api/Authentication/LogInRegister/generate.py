from typing import Dict, Any

import requests


class BilibiliLogInRegister:
    """
    B站登录注册相关API
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化登录注册管理器

        Args:
            headers: 请求头字典
            verify_ssl: 是否验证SSL证书
        """
        self.headers = headers
        self.verify_ssl = verify_ssl

    def generate(self) -> Dict[str, Any]:
        """
        申请登录二维码

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含url和qrcode_key）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'

            # 发送请求
            response = requests.get(
                url=api,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=10
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "申请二维码失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            try:
                result = response.json()
            except ValueError as e:
                return {
                    "success": False,
                    "message": "申请二维码失败",
                    "error": f"解析响应失败: {str(e)}",
                    "status_code": response.status_code,
                    "api_code": None
                }

            # 检查API返回状态码
            api_code = result.get("code", -1)
            if api_code != 0:
                error_msg = result.get("message") or result.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "申请二维码失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 检查数据是否存在
            data = result.get("data")
            if not data:
                return {
                    "success": False,
                    "message": "申请二维码失败",
                    "error": "API返回数据为空",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 提取必要字段
            url = data.get("url")
            qrcode_key = data.get("qrcode_key")

            if not url or not qrcode_key:
                return {
                    "success": False,
                    "message": "申请二维码失败",
                    "error": "响应中缺少必要的二维码数据",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            return {
                "success": True,
                "message": "二维码申请成功",
                "data": {
                    "url": url,
                    "qrcode_key": qrcode_key
                },
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "申请二维码失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "申请二维码失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "申请二维码失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "申请二维码过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


# 使用示例
if __name__ == "__main__":
    # 创建请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建登录注册实例
    login_register = BilibiliLogInRegister(headers, verify_ssl=True)

    # 申请二维码
    result = login_register.generate()

    if result["success"]:
        print("二维码申请成功:")
        print(f"二维码URL: {result['data']['url']}")
        print(f"二维码密钥: {result['data']['qrcode_key']}")
    else:
        print(f"二维码申请失败: {result['error']}")
        if "response_data" in result:
            print(f"完整响应: {result['response_data']}")