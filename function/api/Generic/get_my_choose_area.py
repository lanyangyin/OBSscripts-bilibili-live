import requests
from typing import Dict, Any, List, Union, Optional


class BilibiliApiGeneric:
    """
    不登录也能使用的Bilibili API集合

    提供不需要认证即可访问的Bilibili API功能
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        }

    def get_anchor_common_areas(self, room_id: Union[str, int]) -> Dict[str, Any]:
        """
        获取主播常用分区信息

        该API返回主播设置的常用分区列表（通常为3个分区）

        参数:
            room_id: 直播间ID（整数或字符串）

        返回数据结构:
        {
            "code": int,        # 0表示成功
            "msg": str,         # 状态消息
            "message": str,     # 状态消息（通常与msg相同）
            "data": [           # 常用分区列表
                {
                    "id": str,             # 分区ID
                    "pic": str,             # 分区图标URL
                    "hot_status": str,      # 热门状态（0:非热门）
                    "name": str,            # 分区名称
                    "parent_id": str,       # 父分区ID
                    "parent_name": str,     # 父分区名称
                    "act_flag": int         # 活动标志（通常为0）
                },
                ...  # 更多分区（通常最多3个）
            ]
        }

        Raises:
            ValueError: 输入参数无效
            requests.RequestException: 网络请求失败
            RuntimeError: API返回错误或无效数据
        """
        # 验证房间ID
        if not room_id:
            raise ValueError("房间ID不能为空")

        # API配置
        api_url = "https://api.live.bilibili.com/room/v1/Area/getMyChooseArea"
        params = {"roomid": str(room_id)}

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
            result = response.json()

            # 验证基本结构
            if not isinstance(result, dict) or "code" not in result:
                raise RuntimeError("API返回无效的响应格式")

            # 检查API错误码
            if result.get("code") != 0:
                error_msg = result.get("message") or result.get("msg") or "未知错误"
                raise RuntimeError(f"API返回错误: {error_msg} (code: {result['code']})")

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], list):
                raise RuntimeError("API返回数据格式无效")

            # 验证分区数据
            for area in result["data"]:
                required_keys = {"id", "name", "parent_id", "parent_name"}
                if not required_keys.issubset(area.keys()):
                    raise RuntimeError("分区数据缺少必需字段")

            return result

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"获取主播分区信息失败: {e}"
            ) from e
        except (ValueError, TypeError) as e:
            raise ValueError(f"数据处理失败: {e}") from e


if __name__ == "__main__":
    # 创建API实例
    api = BilibiliApiGeneric()

    try:
        # 获取主播常用分区
        room_id = 25322725
        result = api.get_anchor_common_areas(room_id)

        # 处理结果
        print(f"主播房间 {room_id} 的常用分区:")
        for area in result["data"]:
            print(f"- {area['name']} (ID: {area['id']}, 父分区: {area['parent_name']})")

        # 示例输出:
        # 主播房间 25322725 的常用分区:
        # - 生活杂谈 (ID: 646, 父分区: 生活)
        # - 无畏契约 (ID: 329, 父分区: 网游)
        # - 聊天电台 (ID: 192, 父分区: 电台)
        print({area['id']: f"⭐{area['name']}" for area in BilibiliApiGeneric().get_anchor_common_areas(room_id)["data"]})
    except Exception as e:
        print(f"错误: {e}")