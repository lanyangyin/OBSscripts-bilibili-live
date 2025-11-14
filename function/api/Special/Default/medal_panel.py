from pathlib import Path
from typing import Dict, Any, Optional

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

    def get_medal_panel(self, page: int = 1, page_size: int = 10, room_id: Optional[int] = None,
                        target_id: Optional[int] = None, get_all_pages: bool = False) -> Dict[str, Any]:
        """
        获取用户粉丝勋章面板信息

        Args:
            page: 页码（默认1）
            page_size: 每页数量（默认10）
            room_id: 房间ID（可选）
            target_id: 目标用户ID（可选，默认使用当前用户）
            get_all_pages: 是否获取全部页数据（默认False）

        Returns:
            包含粉丝勋章面板信息的字典：
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
                    "message": "获取粉丝勋章面板失败",
                    "error": "管理器未正确初始化",
                    "status_code": None
                }

            # 设置默认目标ID
            if target_id is None:
                target_id = int(self.user_id)

            # 检查参数有效性
            if page <= 0:
                return {
                    "success": False,
                    "message": "获取粉丝勋章面板失败",
                    "error": "页码必须大于0",
                    "status_code": None
                }

            if page_size <= 0 or page_size > 50:
                return {
                    "success": False,
                    "message": "获取粉丝勋章面板失败",
                    "error": "每页数量必须在1-50之间",
                    "status_code": None
                }

            # 构建API请求
            api_url = "https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/panel"
            params = {
                'page': page,
                'page_size': page_size
            }

            # 添加可选参数
            if room_id:
                params['room_id'] = room_id
            if target_id:
                params['target_id'] = target_id

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
                    "message": "获取粉丝勋章面板失败",
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

            data = result["data"]

            # 如果需要获取全部页数据
            if get_all_pages:
                all_pages_data = self._get_all_pages_medal_data(
                    initial_data=data,
                    room_id=room_id,
                    target_id=target_id,
                    page_size=page_size
                )

                if not all_pages_data["success"]:
                    return all_pages_data

                data = all_pages_data["data"]

            # 成功返回
            return {
                "success": True,
                "message": "粉丝勋章面板获取成功",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取粉丝勋章面板失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取粉丝勋章面板失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取粉丝勋章面板失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取粉丝勋章面板过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }

    def _get_all_pages_medal_data(self, initial_data: Dict[str, Any], room_id: Optional[int] = None,
                                  target_id: Optional[int] = None, page_size: int = 10) -> Dict[str, Any]:
        """
        获取所有页的勋章数据

        Args:
            initial_data: 第一页的数据
            room_id: 房间ID
            target_id: 目标用户ID
            page_size: 每页数量

        Returns:
            包含所有页数据的字典
        """
        try:
            page_info = initial_data.get("page_info", {})
            total_pages = page_info.get("total_page", 1)
            current_page = page_info.get("current_page", 1)

            # 如果只有一页，直接返回
            if total_pages <= 1:
                return {
                    "success": True,
                    "message": "已获取所有页数据",
                    "data": initial_data
                }


            all_list_data = initial_data.get("list", [])
            all_special_list_data = initial_data.get("special_list", [])

            # 从第二页开始获取
            for page in range(2, total_pages + 1):

                # 构建API请求
                api_url = "https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/panel"
                params = {
                    'page': page,
                    'page_size': page_size
                }

                # 添加可选参数
                if room_id:
                    params['room_id'] = room_id
                if target_id:
                    params['target_id'] = target_id

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
                        "message": f"获取第 {page} 页数据失败",
                        "error": f"HTTP错误: {response.status_code}",
                        "status_code": response.status_code
                    }

                # 解析响应
                result = response.json()

                # 检查B站API返回状态
                if result.get("code") != 0:
                    return {
                        "success": False,
                        "message": f"获取第 {page} 页数据失败",
                        "error": result.get("message", "未知错误"),
                        "status_code": response.status_code,
                        "api_code": result.get("code")
                    }

                page_data = result.get("data", {})

                # 合并数据
                all_list_data.extend(page_data.get("list", []))
                # 特殊列表通常只有第一页有，但为了完整性也合并
                if page == 2:  # 只在第二页合并特殊列表，避免重复
                    all_special_list_data.extend(page_data.get("special_list", []))

                # 添加小延迟，避免请求过快
                import time
                time.sleep(0.5)

            # 更新数据
            initial_data["list"] = all_list_data
            if all_special_list_data:
                initial_data["special_list"] = all_special_list_data

            # 更新分页信息
            initial_data["page_info"] = {
                "number": len(all_list_data),
                "current_page": 1,
                "has_more": False,
                "next_page": None,
                "next_light_status": page_info.get("next_light_status", 0),
                "total_page": 1,
                "is_all_pages": True,  # 标记为已获取所有页
                "original_total_pages": total_pages
            }

            return {
                "success": True,
                "message": f"成功获取所有 {total_pages} 页数据",
                "data": initial_data
            }

        except Exception as e:
            return {
                "success": False,
                "message": "获取所有页数据过程中发生错误",
                "error": str(e)
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
        # 获取粉丝勋章面板信息 - 单页模式
        print("=== 单页模式 ===")
        medal_panel_result = api_manager.get_medal_panel(
            page=1,
            page_size=10,
            room_id=DataInput.get_medal_panel_roomid,  # 示例房间ID
            target_id=DataInput.get_medal_panel_user_id,  # 示例用户ID
            get_all_pages=False  # 只获取第一页
        )

        if medal_panel_result["success"]:
            panel_data = medal_panel_result["data"]
            page_info = panel_data.get("page_info", {})
            medal_list = panel_data.get("list", [])
            print(f"单页模式: 获取到 {len(medal_list)} 个普通勋章")
            print(f"分页信息: 第 {page_info.get('current_page', 1)}/{page_info.get('total_page', 1)} 页")
            if page_info.get('has_more'):
                print("还有更多页数据可用")
        else:
            print(f"获取粉丝勋章面板失败: {medal_panel_result['error']}")

        print("\n" + "=" * 50 + "\n")

        # 获取粉丝勋章面板信息 - 全部页模式
        print("=== 全部页模式 ===")
        medal_panel_all_result = api_manager.get_medal_panel(
            page=1,
            page_size=10,
            room_id=DataInput.get_medal_panel_roomid,  # 示例房间ID
            target_id=DataInput.get_medal_panel_user_id,  # 示例用户ID
            get_all_pages=True  # 获取所有页
        )

        if medal_panel_all_result["success"]:
            print(medal_panel_all_result["message"])
            panel_data = medal_panel_all_result["data"]
            page_info = panel_data.get("page_info", {})
            medal_list = panel_data.get("list", [])
            special_list = panel_data.get("special_list", [])

            print(f"\n=== 统计信息 ===")
            print(f"普通勋章总数: {len(medal_list)}")
            print(f"特殊勋章总数: {len(special_list)}")
            print(f"总勋章数: {len(medal_list) + len(special_list)}")

            if page_info.get('is_all_pages'):
                print(f"已获取所有 {page_info.get('original_total_pages', 1)} 页数据")

            # 显示全部勋章
            if medal_list:
                print(f"\n=== 普通勋章 ===")
                for i, medal_item in enumerate(medal_list, 1):
                    medal = medal_item.get("medal", {})
                    anchor_info = medal_item.get("anchor_info", {})
                    print(
                        f"{i}. {anchor_info.get('nick_name', '未知主播')} - {medal.get('medal_name', '未知勋章')} (Lv{medal.get('level', 0)})")

            if special_list:
                print(f"\n=== 特殊勋章列表 ===")
                for i, special_item in enumerate(special_list, 1):
                    medal = special_item.get("medal", {})
                    anchor_info = special_item.get("anchor_info", {})
                    superscript = special_item.get("superscript", {})
                    wearing_text = "✅佩戴中" if medal.get("wearing_status", 0) == 1 else "❌未佩戴"
                    print(
                        f"{i}. {anchor_info.get('nick_name', '未知主播')} - {medal.get('medal_name', '未知勋章')} (Lv{medal.get('level', 0)}) | {wearing_text}")
                    if superscript:
                        print(f"   特殊标记: {superscript.get('content', '')}")
        else:
            print(f"获取全部页粉丝勋章面板失败: {medal_panel_all_result['error']}")
            if "status_code" in medal_panel_all_result and medal_panel_all_result["status_code"]:
                print(f"HTTP状态码: {medal_panel_all_result['status_code']}")
            if "api_code" in medal_panel_all_result:
                print(f"API错误码: {medal_panel_all_result['api_code']}")