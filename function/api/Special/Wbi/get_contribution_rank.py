from pathlib import Path
from typing import Dict, Any, Literal
from urllib.parse import quote
from functools import reduce
from hashlib import md5
import urllib.parse
import time

import requests

from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


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

    def wbi(self, data: dict):
        """
        WBI 签名
        @param data: 需要 wbi签名 的 params 参数
        @return: requests的 params 参数
        @rtype: dict
        """
        mixinKeyEncTab = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
            33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
            61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
            36, 20, 34, 44, 52
        ]

        def getMixinKey(orig: str):
            """对 imgKey 和 subKey 进行字符顺序打乱编码"""
            return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

        def encWbi(params: dict, img_key: str, sub_key: str):
            """为请求参数进行 wbi 签名"""
            mixin_key = getMixinKey(img_key + sub_key)
            curr_time = round(time.time())
            params['wts'] = curr_time  # 添加 wts 字段
            params = dict(sorted(params.items()))  # 按照 key 重排参数
            # 过滤 value 中的 "!'()*" 字符
            params = {
                k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
                for k, v
                in params.items()
            }
            query = urllib.parse.urlencode(params)  # 序列化参数
            wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
            params['w_rid'] = wbi_sign
            return params

        def getWbiKeys() -> tuple[str, str]:
            """获取最新的 img_key 和 sub_key"""
            resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=self.headers)
            resp.raise_for_status()
            json_content = resp.json()
            img_url: str = json_content['data']['wbi_img']['img_url']
            sub_url: str = json_content['data']['wbi_img']['sub_url']
            img_key = img_url.rsplit('/', 1)[1].split('.')[0]
            sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
            return img_key, sub_key

        img_key, sub_key = getWbiKeys()

        signed_params = encWbi(
            params=data,
            img_key=img_key,
            sub_key=sub_key
        )
        return signed_params

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
            signed_params = self.wbi(params)

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
    from _Input.function.api.Special import Room as DataInput

    # 初始化配置管理器
    BULC = BilibiliUserConfigManager(DataInput.cookie_file_path)
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