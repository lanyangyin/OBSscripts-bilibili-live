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

    def get_medal_wall(self, target_id: int) -> Dict[str, Any]:
        """
        获取指定用户的所有粉丝勋章信息（最多200个）

        Args:
            target_id: 目标用户ID

        Returns:
            包含粉丝勋章信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含勋章列表等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取粉丝勋章墙失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 检查目标ID是否有效
            if not target_id or target_id <= 0:
                return {
                    "success": False,
                    "message": "获取粉丝勋章墙失败",
                    "error": "目标用户ID无效",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall"
            params = {
                'target_id': target_id
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
                    "message": "获取粉丝勋章墙失败",
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
                "message": "粉丝勋章墙获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取粉丝勋章墙失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取粉丝勋章墙失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取粉丝勋章墙失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取粉丝勋章墙过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


# 使用示例
if __name__ == '__main__':
    from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
    from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
    from _Input.function.api.Special import Room as DataInput

    # 初始化配置管理器
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建管理器实例
    api_manager = BilibiliSpecialApiManager(Headers)

    # 检查管理器是否初始化成功
    if not api_manager.initialization_result["success"]:
        print(f"管理器初始化失败: {api_manager.initialization_result['error']}")
    else:
        # 获取粉丝勋章墙信息（这里使用当前用户ID作为示例）
        target_user_id = DataInput.medal_wall_uid
        medal_result = api_manager.get_medal_wall(target_user_id)

        if medal_result["success"]:
            print("粉丝勋章墙获取成功")
            medal_data = medal_result["data"]

            print(f"(我的UID: {medal_data.get('uid', '未知')})")
            print(f"用户: {medal_data.get('name', '未知')} (UID: {DataInput.medal_wall_uid})")
            print(f"勋章总数: {medal_data.get('count', 0)}")
            print(f"关闭空间显示: {'是' if medal_data.get('close_space_medal', 0) else '否'}")
            print(f"只显示佩戴: {'是' if medal_data.get('only_show_wearing', 0) else '否'}")

            medal_list = medal_data.get("list", [])
            if medal_list:
                print(f"\n=== 粉丝勋章列表 ({len(medal_list)}个) ===")
                for i, medal in enumerate(medal_list, 1):
                    medal_info = medal.get("medal_info", {})
                    target_name = medal.get("target_name", "未知主播")
                    live_status = medal.get("live_status", 0)
                    wearing_status = medal_info.get("wearing_status", 0)

                    # 直播状态文本
                    live_status_text = {
                        0: "未直播",
                        1: "直播中",
                        2: "轮播中"
                    }.get(live_status, "未知")

                    # 佩戴状态文本
                    wearing_text = "✅佩戴中" if wearing_status == 1 else "❌未佩戴"

                    print(f"{i}. {target_name} - {medal_info.get('medal_name', '未知勋章')}")
                    print(f"   等级: Lv{medal_info.get('level', 0)} | {wearing_text}")
                    print(f"   亲密度: {medal_info.get('intimacy', 0)}/{medal_info.get('next_intimacy', 0)}")
                    print(f"   今日获得: {medal_info.get('today_feed', 0)} | 上限: {medal_info.get('day_limit', 0)}")
                    print(f"   直播状态: {live_status_text}")
                    print(f"   主播主页: {medal.get('link', '无')}")
                    print()
            else:
                print("没有找到任何粉丝勋章")
        else:
            print(f"获取粉丝勋章墙失败: {medal_result['error']}")
            if "status_code" in medal_result and medal_result["status_code"]:
                print(f"HTTP状态码: {medal_result['status_code']}")
            if "api_code" in medal_result:
                print(f"API错误码: {medal_result['api_code']}")