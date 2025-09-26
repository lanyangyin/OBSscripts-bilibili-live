from pathlib import Path
from typing import Dict, Any, Literal

import requests

from function.tools.wbi import wbi
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.BilibiliUserConfigManager import BilibiliUserConfigManager


class WbiSigna:
    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        wbi签名的api
        Args:
            headers: 包含Cookie和User-Agent的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）
        """
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_contribution_rank(self, ruid: int, room_id: int,
                              rank_type: Literal["online_rank", "daily_rank", "weekly_rank", "monthly_rank"],
                              switch: Literal["contribution_rank", "entry_time_rank", "today_rank", "yesterday_rank",
                              "current_week_rank", "last_week_rank", "current_month_rank", "last_month_rank"],
                              page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        获取直播间观众贡献排名

        Args:
            ruid: 直播间主播 mid
            room_id: 直播间 id
            rank_type: 排名类型
                - "online_rank": 在线榜
                - "daily_rank": 日榜
                - "weekly_rank": 周榜
                - "monthly_rank": 月榜
            switch: 具体排名类型
                "online_rank": 在线榜
                    - "contribution_rank": 贡献值
                    - "entry_time_rank": 进房时间
                "daily_rank": 日榜
                    - "today_rank": 当日
                    - "yesterday_rank": 昨日
                "weekly_rank": 周榜
                    - "current_week_rank": 本周
                    - "last_week_rank": 上周
                "monthly_rank": 月榜
                    - "current_month_rank": 本月
                    - "last_month_rank": 上月
            page: 页码，page_size*page<100
            page_size: 每页元素数，page_size*page<100

        Returns:
            包含排名信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的排名数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
            - api_code: B站API错误码（如果有）
        """
        try:
            # 参数验证
            if not ruid or ruid <= 0:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": "主播ID无效",
                    "status_code": None
                }

            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": "房间ID无效",
                    "status_code": None
                }

            if page <= 0 or page_size <= 0 or page * page_size > 100:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
                    "error": "页码或每页数量无效（总数不能超过100）",
                    "status_code": None
                }

            # 构建API请求参数
            api_url = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/queryContributionRank"
            params = {
                "ruid": ruid,
                "room_id": room_id,
                "page": page,
                "page_size": page_size,
                "type": rank_type,
                "switch": switch,
                "platform": "web"
            }

            # WBI签名
            signed_params = wbi(params)

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                params=signed_params,
                verify=self.verify_ssl,
                timeout=30
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取贡献排名失败",
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

            # 成功返回
            return {
                "success": True,
                "message": "贡献排名获取成功",
                "data": result.get("data", {}),
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取贡献排名失败",
                "error": "请求超时",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取贡献排名失败",
                "error": "网络连接错误",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取贡献排名失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取贡献排名过程中发生未知错误",
                "error": str(e),
                "status_code": None
            }


# 使用示例
if __name__ == '__main__':
    # 初始化配置管理器
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']

    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建贡献排名管理器实例
    rank_manager = WbiSigna(Headers)

    # 获取贡献排名
    rank_result = rank_manager.get_contribution_rank(
        ruid=3821157,
        room_id=21692711,
        rank_type="online_rank",
        switch="entry_time_rank",
        page=1,
        page_size=100
    )

    # 美化输出结果
    if rank_result["success"]:
        print("✅ 贡献排名获取成功")
        print(f"📊 排名数据条目数: {len(rank_result['data'].get('item', []))}")

        # 显示排名信息
        items = rank_result['data'].get('item', [])
        if items:
            print("\n🏆 排名列表:")
            for item in items:
                print(f"  第{item.get('rank', 'N/A')}名: {item.get('name', '未知用户')} "
                      f"(UID: {item.get('uid', 'N/A')})")

        # 显示自己的排名信息
        own_info = rank_result['data'].get('own_info', {})
        if own_info:
            print(f"\n👤 我的排名: {own_info.get('rank_text', '未知')}")
            if own_info.get('rank', -1) > 0:
                print(f"   排名位置: 第{own_info.get('rank')}名")
            print(f"   贡献值: {own_info.get('score', 0)}")

        print(f"\n📋 总计数: {rank_result['data'].get('count', 0)}")

    else:
        print("❌ 获取贡献排名失败")
        print(f"   错误信息: {rank_result['error']}")
        if rank_result.get('status_code'):
            print(f"   HTTP状态码: {rank_result['status_code']}")
        if rank_result.get('api_code'):
            print(f"   API错误码: {rank_result['api_code']}")