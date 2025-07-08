import json

import requests
from typing import Dict, Any


class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        }

    def get_room_base_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间基本信息

        Args:
            room_id: 直播间短ID

        Returns:
            包含直播间信息的字典，结构:
            {
                "room_id": int,       # 直播间长ID
                "uid": int,            # 主播用户mid
                "area_id": int,        # 直播间分区ID
                "live_status": int,    # 直播状态(0:未开播,1:直播中,2:轮播中)
                "live_url": str,       # 直播间网页url
                "parent_area_id": int, # 父分区ID
                "title": str,          # 直播间标题
                "parent_area_name": str, # 父分区名称
                "area_name": str,      # 分区名称
                "live_time": str,      # 开播时间(yyyy-MM-dd HH:mm:ss)
                "description": str,    # 直播间简介
                "tags": str,           # 直播间标签(逗号分隔)
                "attention": int,      # 关注数
                "online": int,         # 在线人数
                "short_id": int,       # 直播间短ID(0表示无短号)
                "uname": str,          # 主播用户名
                "cover": str,          # 直播间封面url
                "background": str,     # 直播间背景url
                # 其他字段: join_slide, live_id, live_id_str
            }

        Raises:
            RequestException: 网络请求失败
            ValueError: API返回错误或数据结构异常
        """
        api_url = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
        params = {
            "req_biz": "web_room_componet",
            "room_ids": room_id
        }

        try:
            # 发送API请求
            response = requests.get(
                api_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()  # 检查HTTP错误

            # 解析JSON响应
            data = response.json()

            # 验证API响应
            if data.get("code") != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                raise ValueError(f"API错误: {error_msg}")

            # 提取房间信息
            by_room_ids = data.get("data").get("by_room_ids")
            if not by_room_ids:
                raise ValueError("未找到房间信息")

            # 返回第一个房间信息（即使多个也取第一个）
            room_info = next(iter(by_room_ids.values()), None)
            if not room_info:
                raise ValueError("房间信息为空")

            return room_info

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"网络请求失败: {e}") from e
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"数据处理失败: {e}") from e


if __name__ == "__main__":
    # 创建API实例
    api = BilibiliApiGeneric()

    try:
        # 获取直播间信息（使用短ID）
        room_info = api.get_room_base_info(25322725)
        print(json.dumps(room_info, ensure_ascii=False, indent=2))

        # 打印基本信息
        print(f"直播间标题: {room_info['title']}")
        print(f"主播: {room_info['uname']}")
        print(f"状态: {'直播中' if room_info['live_status'] == 1 else '未开播'}")
        print(f"在线人数: {room_info['online']}")

    except Exception as e:
        print(f"获取直播间信息失败: {e}")
