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

    def poll(self, qrcode_key: str) -> Dict[str, Any]:
        """
        获取扫码登陆状态，登陆成功获取基础的cookies

        Args:
            qrcode_key: 扫描秘钥

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含扫码状态和cookies信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not qrcode_key or not isinstance(qrcode_key, str):
                return {
                    "success": False,
                    "message": "查询扫码状态失败",
                    "error": "二维码密钥无效",
                    "status_code": None,
                    "api_code": None
                }

            api = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}'

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
                    "message": "查询扫码状态失败",
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
                    "message": "查询扫码状态失败",
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
                    "message": "查询扫码状态失败",
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
                    "message": "查询扫码状态失败",
                    "error": "API返回数据为空",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 提取扫码状态码和消息
            scan_code = data.get("code")
            scan_message = data.get("message", "")

            # 根据扫码状态码判断扫码状态
            status_mapping = {
                0: "扫码登录成功",
                86038: "二维码已失效",
                86090: "二维码已扫码未确认",
                86101: "未扫码"
            }

            status_message = status_mapping.get(scan_code, f"未知状态码: {scan_code}")

            # 构建返回数据
            result_data = {
                "scan_code": scan_code,
                "scan_message": scan_message,
                "status_description": status_message,
                "url": data.get("url", ""),
                "refresh_token": data.get("refresh_token", ""),
                "timestamp": data.get("timestamp", 0)
            }

            # 如果扫码成功，提取cookies信息
            if scan_code == 0:
                url = data.get("url", "")
                # 从URL中提取cookies参数
                cookies_info = self._extract_cookies_from_url(url)
                result_data.update(cookies_info)

            return {
                "success": True,
                "message": status_message,
                "data": result_data,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "查询扫码状态失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "查询扫码状态失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "查询扫码状态失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "查询扫码状态过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def _extract_cookies_from_url(self, url: str) -> Dict[str, str]:
        """
        从URL中提取cookies参数

        Args:
            url: 包含cookies参数的URL

        Returns:
            包含cookies信息的字典
        """
        cookies = {}
        try:
            from urllib.parse import urlparse, parse_qs

            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)

            # 提取关键cookies字段
            cookies_fields = ["DedeUserID", "DedeUserID__ckMd5", "SESSDATA", "bili_jct"]

            for field in cookies_fields:
                if field in query_params:
                    cookies[field] = query_params[field][0] if query_params[field] else ""

        except Exception:
            # 如果解析失败，返回空字典
            pass

        return cookies


# 使用示例
if __name__ == "__main__":
    # 创建请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建登录注册实例
    login_register = BilibiliLogInRegister(headers, verify_ssl=True)