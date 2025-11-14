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

    def get_user_medal_info(self, uid: int, up_uid: int) -> Dict[str, Any]:
        """
        获取用户与特定主播的粉丝勋章详细信息

        Args:
            uid: 用户ID
            up_uid: 主播用户ID

        Returns:
            包含粉丝勋章详细信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（包含勋章详情等）
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查管理器是否正常初始化
            if not self.initialization_result["success"]:
                return {
                    "success": False,
                    "message": "获取粉丝勋章信息失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 检查参数是否有效
            if not uid or uid <= 0:
                return {
                    "success": False,
                    "message": "获取粉丝勋章信息失败",
                    "error": "用户ID无效",
                    "status_code": None
                }

            if not up_uid or up_uid <= 0:
                return {
                    "success": False,
                    "message": "获取粉丝勋章信息失败",
                    "error": "主播用户ID无效",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/user_medal_info"
            params = {
                'uid': uid,
                'up_uid': up_uid
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
                    "message": "获取粉丝勋章信息失败",
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
                "message": "粉丝勋章信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取粉丝勋章信息失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取粉丝勋章信息失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取粉丝勋章信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取粉丝勋章信息过程中发生未知错误",
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
        # 示例：获取用户与特定主播的粉丝勋章信息
        # 这里使用示例数据，你可以根据需要修改
        medal_info_result = api_manager.get_user_medal_info(DataInput.user_medal_info_user_id, DataInput.user_medal_info_up_user_id)

        if medal_info_result["success"]:
            print("粉丝勋章详细信息获取成功")
            medal_data = medal_info_result["data"]

            print(f"粉丝勋章总数: {medal_data.get('cnt', 0)}")
            print(f"是否获得该勋章: {'是' if medal_data.get('is_gain', False) else '否'}")
            print(f"是否佩戴该勋章: {'是' if medal_data.get('is_weared', False) else '否'}")

            # 当前佩戴的勋章信息
            curr_weared = medal_data.get('curr_weared')
            if curr_weared:
                print(f"\n=== 当前佩戴的勋章 ===")
                print(f"勋章名称: {curr_weared.get('medal_name', '未知')}")
                print(f"等级: Lv{curr_weared.get('level', 0)}")
                print(f"亲密度: {curr_weared.get('intimacy', 0)}/{curr_weared.get('next_intimacy', 0)}")
                print(f"今日获得: {curr_weared.get('today_feed', 0)} | 上限: {curr_weared.get('day_limit', 0)}")
                print(f"是否点亮: {'是' if curr_weared.get('is_lighted', 0) else '否'}")

            # 查询的勋章信息
            lookup_medal = medal_data.get('lookup_medal')
            if lookup_medal:
                print(f"\n=== 查询的勋章信息 ===")
                print(f"勋章名称: {lookup_medal.get('medal_name', '未知')}")
                print(f"勋章id: {lookup_medal.get('medal_id', '未知')}")
                print(f"等级: Lv{lookup_medal.get('level', 0)}")
                print(f"亲密度: {lookup_medal.get('intimacy', 0)}/{lookup_medal.get('next_intimacy', 0)}")
                print(f"今日获得: {lookup_medal.get('today_feed', 0)} | 上限: {lookup_medal.get('day_limit', 0)}")
                print(f"是否点亮: {'是' if lookup_medal.get('is_lighted', 0) else '否'}")

            # 主播勋章信息
            up_medal = medal_data.get('up_medal')
            if up_medal:
                print(f"\n=== 主播勋章信息 ===")
                print(f"勋章名称: {up_medal.get('medal_name', '未知')}")
                print(f"等级: Lv{up_medal.get('level', 0)}")

            # 房间信息
            room_info = medal_data.get('room_info')
            if room_info:
                print(f"\n=== 房间信息 ===")
                print(f"房间ID: {room_info.get('room_id', '未知')}")
                print(f"短ID: {room_info.get('short_id', '未知')}")

            # V2版本信息
            lookup_v2 = medal_data.get('lookup_v2')
            if lookup_v2:
                print(f"\n=== V2勋章信息 ===")
                print(f"名称: {lookup_v2.get('name', '未知')}")
                print(f"等级: Lv{lookup_v2.get('level', 0)}")
                print(f"颜色: {lookup_v2.get('v2_medal_color_start', '未知')}")
                print(f"文本颜色: {lookup_v2.get('v2_medal_color_text', '未知')}")

        else:
            print(f"获取粉丝勋章信息失败: {medal_info_result['error']}")
            if "status_code" in medal_info_result and medal_info_result["status_code"]:
                print(f"HTTP状态码: {medal_info_result['status_code']}")
            if "api_code" in medal_info_result:
                print(f"API错误码: {medal_info_result['api_code']}")