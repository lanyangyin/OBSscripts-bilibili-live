from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.EncodingConversion.parse_cookie import parse_cookie


class BilibiliSpecialApiManager:
    """
    B站需要登陆的API管理器，用于获取直播间相关状态信息。

    特性：
    - 自动从Cookie中解析必要认证信息
    - 支持SSL验证配置
    - 提供直播间状态信息获取功能
    - 统一的错误处理和响应格式
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化管理器

        Args:
            headers: 包含Cookie等认证信息的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
        """
        self.headers = headers.copy()  # 避免修改原始headers
        self.verify_ssl = verify_ssl
        self.initialization_result = self._initialize_manager()

    def _initialize_manager(self) -> Dict[str, Any]:
        """
        初始化管理器的内部实现

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
            required_fields = ["DedeUserID"]
            missing_fields = [field for field in required_fields if field not in self.cookies]
            if missing_fields:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": f"Cookie中缺少必要字段: {', '.join(missing_fields)}"
                }

            self.user_id = self.cookies["DedeUserID"]

            return {
                "success": True,
                "message": "直播间信息管理器初始化成功",
                "data": {
                    "user_id": self.user_id
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": "初始化过程中发生异常",
                "error": str(e)
            }

    def get_room_emoticons(self, room_id: int, platform: str = "pc") -> Dict[str, Any]:
        """
        获取直播间表情包信息

        Args:
            room_id: 直播间ID（长号）
            platform: 平台类型，可选值：pc, android, ios（默认：pc）

        Returns:
            包含表情包信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含表情包列表等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取直播间表情包失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 检查房间ID是否有效
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取直播间表情包失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            # 验证平台参数
            valid_platforms = ["pc", "android", "ios"]
            if platform not in valid_platforms:
                return {
                    "success": False,
                    "message": "获取直播间表情包失败",
                    "error": f"平台参数无效，必须是: {', '.join(valid_platforms)}",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/web-ucenter/v2/emoticon/GetEmoticons"
            params = {
                'room_id': room_id,
                'platform': platform
            }

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
                    "message": "获取直播间表情包失败",
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

            # 处理表情包数据，确保list字段不为None
            emoticon_data = result.get("data", {})
            if "data" in emoticon_data and emoticon_data["data"] is None:
                emoticon_data["data"] = []

            # 成功返回
            return {
                "success": True,
                "message": "直播间表情包获取成功",
                "data": emoticon_data,
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取直播间表情包失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取直播间表情包失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取直播间表情包失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取直播间表情包过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


# 使用示例
if __name__ == '__main__':
    from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
    from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
    from _Input.function.api.Special import Room as DataInput

    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建管理器实例
    room_manager = BilibiliSpecialApiManager(Headers)

    # 检查管理器是否初始化成功
    if not room_manager.initialization_result["success"]:
        print(f"管理器初始化失败: {room_manager.initialization_result['error']}")
    else:
        # 获取直播间表情包
        emoticons_result = room_manager.get_room_emoticons(DataInput.cc_room_id, "pc")

        if emoticons_result["success"]:
            print("直播间表情包获取成功")
            emoticon_data = emoticons_result["data"]

            # 打印基本信息
            print(f"粉丝品牌标识: {emoticon_data.get('fans_brand', '未知')}")
            print(f"购买链接: {emoticon_data.get('purchase_url', '无')}")

            # 打印表情包列表
            emoticon_packages = emoticon_data.get("data", [])
            print(f"\n找到 {len(emoticon_packages)} 个表情包:")

            for i, package in enumerate(emoticon_packages, 1):
                print(f"\n{i}. {package.get('pkg_name', '未知包名')} (ID: {package.get('pkg_id', '未知')})")
                print(f"   描述: {package.get('pkg_descript', '无描述')}")
                print(f"   类型: {package.get('pkg_type', '未知')}")
                print(f"   权限: {package.get('pkg_perm', '未知')}")

                # 打印表情列表
                emoticons = package.get("emoticons", [])
                print(f"   包含 {len(emoticons)} 个表情:")

                for j, emoticon in enumerate(emoticons[:5], 1):  # 只显示前5个表情
                    print(f"     {j}. {emoticon.get('emoji', '未知')} - {emoticon.get('url', '无URL')}")

                if len(emoticons) > 5:
                    print(f"     ... 还有 {len(emoticons) - 5} 个表情")
        else:
            print(f"获取直播间表情包失败: {emoticons_result['error']}")
            if "status_code" in emoticons_result and emoticons_result["status_code"]:
                print(f"HTTP状态码: {emoticons_result['status_code']}")
            if "api_code" in emoticons_result:
                print(f"API错误码: {emoticons_result['api_code']}")