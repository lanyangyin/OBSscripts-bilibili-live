import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Literal

import requests

from function.tools.EncodingConversion.parse_cookie import parse_cookie



class BilibiliCSRFAuthenticator:
    """
    B站CSRF认证管理器，用于处理需要CSRF令牌的API请求。

    该类专门用于B站直播相关的CSRF认证操作，特别是直播公告的更新。
    自动从Cookie中提取必要的认证信息，并提供简化的API调用接口。

    特性：
    - 自动从Cookie中解析CSRF令牌（bili_jct）
    - 自动提取用户ID（DedeUserID）
    - 支持SSL验证配置
    - 提供直播公告更新功能
    - 统一的错误处理和响应格式
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化CSRF认证管理器

        Args:
            headers: 包含Cookie等认证信息的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）

        Returns:
            包含操作结果的字典，包含以下键：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（如认证器实例）
            - error: 失败时的错误信息
        """
        self.headers = headers.copy()  # 避免修改原始headers
        self.verify_ssl = verify_ssl
        self.initialization_result = self._initialize_authenticator()

    def _initialize_authenticator(self) -> Dict[str, Any]:
        """
        初始化认证器的内部实现

        Returns:
            包含初始化结果的字典
        """
        try:
            # 解析Cookie
            if "cookie" not in self.headers:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": "请求头中缺少cookie字段"
                }

            self.cookie = self.headers["cookie"]
            self.cookies = parse_cookie(self.cookie)

            # 提取必要字段
            required_fields = ["bili_jct", "DedeUserID"]
            missing_fields = [field for field in required_fields if field not in self.cookies]
            if missing_fields:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": f"Cookie中缺少必要字段: {', '.join(missing_fields)}"
                }

            self.user_id = self.cookies["DedeUserID"]
            self.csrf = self.cookies["bili_jct"]

            return {
                "success": True,
                "message": "认证器初始化成功",
                "data": {
                    "user_id": self.user_id,
                    "csrf_token": self.csrf
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": "初始化过程中发生异常",
                "error": str(e)
            }

    def validate_csrf_token(self) -> Dict[str, Any]:
        """
        验证CSRF令牌是否有效

        Returns:
            包含验证结果的字典：
            - success: 验证是否成功
            - valid: CSRF令牌是否有效
            - message: 结果描述信息
        """
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "valid": False,
                "message": "认证器未正确初始化"
            }

        is_valid = bool(self.csrf and len(self.csrf) == 32)

        return {
            "success": True,
            "valid": is_valid,
            "message": "CSRF令牌有效" if is_valid else "CSRF令牌无效"
        }

    def get_user_info(self) -> Dict[str, Any]:
        """
        获取用户基本信息

        Returns:
            包含用户信息的字典：
            - success: 操作是否成功
            - data: 用户信息字典（包含user_id, csrf_token, has_valid_csrf）
            - message: 结果描述信息
        """
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "message": "无法获取用户信息，认证器未正确初始化",
                "error": self.initialization_result.get("error", "未知错误")
            }

        validation_result = self.validate_csrf_token()

        return {
            "success": True,
            "data": {
                "user_id": self.user_id,
                "csrf_token": self.csrf,
                "has_valid_csrf": validation_result["valid"]
            },
            "message": "用户信息获取成功"
        }

    def start_live(self, room_id: int, area_id: int, platform: Literal["pc_link", "web_link", "android_link"]) -> Dict:
        """
        开始直播

        Args:
            room_id: 直播间ID
            area_id: 二级分区id
            platform: 直播平台

        Returns:
            包含开播结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含直播流信息等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的code
        """
        try:
            # 检查认证器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "认证器未正确初始化",
                    "status_code": None,
                    "api_code": None
                }

            # 参数验证
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            if not area_id or area_id <= 0:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "分区ID无效",
                    "status_code": None,
                    "api_code": None
                }

            if platform not in ["pc_link", "web_link", "android_link"]:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": "平台参数无效",
                    "status_code": None,
                    "api_code": None
                }

            api = "https://api.live.bilibili.com/room/v1/Room/startLive"
            headers = self.headers
            csrf = self.csrf

            # 构建请求参数
            startLivedata = {
                "access_key": "",  # 留空
                "appkey": "aae92bc66f3edfab",  # 固定应用密钥
                "platform": platform,
                "room_id": room_id,
                "area_v2": area_id,
                "build": "9343",  # 客户端版本号
                "backup_stream": 0,
                "csrf": csrf,
                "csrf_token": csrf,
                "ts": str(int(time.time()))  # 当前UNIX时间戳
            }

            # 对参数按字典序排序
            sorted_params = sorted(startLivedata.items(), key=lambda x: x[0])

            # 生成签名字符串 (参数串 + 固定盐值)
            query_string = "&".join(f"{k}={v}" for k, v in sorted_params)
            sign_string = query_string + "af125a0d5279fd576c1b4418a3e8276d"

            # 计算MD5签名
            md5_sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

            # 添加签名到参数
            startLivedata["sign"] = md5_sign

            # 发送请求
            response = requests.post(
                url=api,
                headers=headers,
                params=startLivedata,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()
            api_code = result.get("code")

            # 判断开播结果
            if api_code == 0:
                # 开播成功或重复开播
                change_status = result.get("data", {}).get("change", 0)
                if change_status == 1:
                    message = "开播成功"
                else:
                    message = result.get("message", "重复开播")

                return {
                    "success": True,
                    "message": message,
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # 开播失败
                error_msg = result.get("message", "未知错误")
                return {
                    "success": False,
                    "message": "开播失败",
                    "error": error_msg,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "开播失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "开播失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "开播失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "开播过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }



# 使用示例
if __name__ == "__main__":
    from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
    from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
    from function.api.Special.Default import BilibiliSpecialApiManager as GetRoomHighlightInfo
    from _Input.function.api.Special import Csrf as DataInput

    # 示例用法
    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建认证器实例
    authenticator = BilibiliCSRFAuthenticator(Headers)

    # 创建房间信息管理器实例
    ghi = GetRoomHighlightInfo(Headers)

    # 检查初始化结果
    if authenticator.initialization_result["success"]:
        # 获取用户信息
        user_info = authenticator.get_user_info()
        if user_info["success"]:
            # 获取房间高亮信息
            highlight_info = ghi.get_room_highlight_info()

            if highlight_info["success"]:
                room_id = highlight_info["data"]["room_id"]
                start_result = authenticator.start_live(room_id, 255, "pc_link")

                if start_result["success"]:
                    print(f"开播成功: {start_result['message']}")
                    if "rtmp" in start_result["data"]:
                        rtmp_info = start_result["data"]["rtmp"]
                        print(f"RTMP地址: {rtmp_info['addr']}{rtmp_info['code']}")
                else:
                    print(f"开播失败: {start_result['error']}")
                    if start_result["api_code"]:
                        print(f"API错误码: {start_result['api_code']}")
            else:
                print(f"获取房间信息失败: {highlight_info['error']}")
        else:
            print("获取用户信息失败")
    else:
        print(f"认证器初始化失败: {authenticator.initialization_result['error']}")