import json
import requests
from typing import Dict, Any, List, Union, Optional


class BilibiliApiGeneric:
    """
    不登录也能使用的Bilibili API集合

    提供不需要认证即可访问的Bilibili API功能
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_guard_list(self, roomid: Union[int, str], ruid: Union[int, str], page: int = 1,
                       page_size: int = 20, typ: Optional[int] = None,
                       include_total_list: bool = False) -> Dict[str, Any]:
        """
        获取直播间大航海成员列表

        Args:
            roomid: 直播间号
            ruid: 主播UID
            page: 页数（默认1）
            page_size: 页大小（默认20，最大30）
            typ: 排序方式（可选，3=按周，4=按月，5=按总航海亲密度）
            include_total_list: 是否获取并返回完整的大航海列表（默认为False）

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（大航海成员信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not roomid or not ruid:
                return {
                    "success": False,
                    "message": "获取大航海列表失败",
                    "error": "房间ID和主播UID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            if page <= 0:
                return {
                    "success": False,
                    "message": "获取大航海列表失败",
                    "error": "页数必须大于0",
                    "status_code": None,
                    "api_code": None
                }

            # 限制page_size在有效范围内
            if page_size <= 0 or page_size > 30:
                page_size = 20  # 使用默认值

            # API配置
            api_url = "https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topListNew"

            # 构建请求参数
            params = {
                "roomid": str(roomid),
                "ruid": str(ruid),
                "page": page,
                "page_size": page_size
            }

            # 添加可选的排序参数
            if typ in [3, 4, 5]:
                params["typ"] = typ

            # 发送API请求
            response = requests.get(
                api_url,
                headers=self.headers,
                params=params,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取大航海列表失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            result = response.json()

            # 验证基本结构
            if not isinstance(result, dict) or "code" not in result:
                return {
                    "success": False,
                    "message": "获取大航海列表失败",
                    "error": "API返回无效的响应格式",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_data": result
                }

            # 检查API错误码
            api_code = result.get("code", -1)
            if api_code != 0:
                error_msg = result.get("message") or result.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取大航海列表失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], dict):
                return {
                    "success": False,
                    "message": "获取大航海列表失败",
                    "error": "API返回数据格式无效",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            data = result["data"]

            # 基础返回数据
            response_data = {
                "info": data.get("info", {}),  # 统计信息
                "top3": data.get("top3", []),  # 前三名
                "list": data.get("list", []),  # 当前页列表
                "total_info": {
                    "num": data.get("info", {}).get("num", 0),  # 总人数
                    "page": data.get("info", {}).get("page", 0),  # 总页数
                    "now": data.get("info", {}).get("now", 0)  # 当前页
                }
            }

            # 如果需要获取完整列表
            if include_total_list:
                total_list = self._get_complete_guard_list(roomid, ruid, typ)
                response_data["total_list"] = total_list

            return {
                "success": True,
                "message": "获取大航海列表成功",
                "data": response_data,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取大航海列表失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取大航海列表失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取大航海列表失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取大航海列表过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def _get_complete_guard_list(self, roomid: Union[int, str], ruid: Union[int, str],
                                 typ: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取完整的大航海成员列表（内部方法）

        Args:
            roomid: 直播间号
            ruid: 主播UID
            typ: 排序方式

        Returns:
            完整的大航海成员列表
        """
        complete_list = []
        page = 1

        while True:
            # 构建请求参数
            params = {
                "roomid": str(roomid),
                "ruid": str(ruid),
                "page": page,
                "page_size": 30  # 使用最大页大小
            }

            if typ in [3, 4, 5]:
                params["typ"] = typ

            try:
                # 发送API请求
                response = requests.get(
                    "https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topListNew",
                    headers=self.headers,
                    params=params,
                    timeout=10,
                    verify=self.verify_ssl
                )

                if response.status_code != 200:
                    break

                result = response.json()
                if result.get("code") != 0:
                    break

                data = result["data"]

                # 如果是第一页，包含top3
                if page == 1:
                    complete_list.extend(data.get("top3", []))

                # 添加当前页列表
                current_list = data.get("list", [])
                complete_list.extend(current_list)

                # 检查是否还有更多页
                info = data.get("info", {})
                total_pages = info.get("page", 0)
                if page >= total_pages or not current_list:
                    break

                page += 1

            except Exception:
                break

        return complete_list


# 使用示例
if __name__ == "__main__":
    from _Input.function.api import Generic as DataInput

    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(Headers, verify_ssl=True)

    try:
        # 获取大航海成员列表（包含完整列表）
        room_id, ruid = DataInput.get_guard_list_for_room_id0uid
        result = api.get_guard_list(
            roomid=room_id,
            ruid=ruid,
            page=1,
            page_size=20,
            include_total_list=True  # 设置为True获取完整列表
        )

        if result["success"]:
            guard_data = result["data"]

            # 将完整列表转换为 {uid: guard_level} 字典
            if "total_list" in guard_data:
                guard_dict = {}
                for guard in guard_data["total_list"]:
                    uid = guard["uinfo"]["uid"]
                    guard_level = guard["uinfo"]["guard"]["level"]
                    guard_dict[uid] = guard_level

                # 现在 guard_dict 就是你要的 {uid: guard_level} 字典
                print("大航海成员字典:", guard_dict)

                # 如果你需要，可以将这个字典添加回原数据
                guard_data["guard_dict"] = guard_dict

        if result["success"]:
            guard_data = result["data"]
            print(json.dumps(guard_data, ensure_ascii=False, indent=2))

            # 处理结果
            total_info = guard_data["total_info"]
            print(f"\n大航海统计信息:")
            print(f"总人数: {total_info['num']}")
            print(f"总页数: {total_info['page']}")
            print(f"当前页: {total_info['now']}")

            # 显示前三名
            print(f"\n🏆 大航海前三名:")
            for guard in guard_data["top3"]:
                user_info = guard["uinfo"]["base"]
                guard_level = guard["uinfo"]["guard"]["level"]
                accompany_days = guard["accompany"]
                rank = guard["rank"]

                level_names = {1: "总督", 2: "提督", 3: "舰长"}
                level_name = level_names.get(guard_level, f"未知({guard_level})")

                print(f"第{rank}名: {user_info['name']} - {level_name} - 陪伴{accompany_days}天")

            # 显示当前页成员
            print(f"\n📋 当前页成员 (第{total_info['now']}页):")
            for guard in guard_data["list"]:
                user_info = guard["uinfo"]["base"]
                guard_level = guard["uinfo"]["guard"]["level"]
                accompany_days = guard["accompany"]
                rank = guard["rank"]

                level_names = {1: "总督", 2: "提督", 3: "舰长"}
                level_name = level_names.get(guard_level, f"未知({guard_level})")

                print(f"第{rank}名: {user_info['name']} - {level_name} - 陪伴{accompany_days}天")

            # 如果包含完整列表，显示统计信息
            if "total_list" in guard_data:
                total_list = guard_data["total_list"]
                print(f"\n📊 完整大航海列表统计 ({len(total_list)} 名成员):")

                # 等级统计
                level_count = {}
                for guard in total_list:
                    guard_level = guard["uinfo"]["guard"]["level"]
                    level_count[guard_level] = level_count.get(guard_level, 0) + 1

                print(f"等级分布:")
                for level, count in sorted(level_count.items()):
                    level_names = {1: "总督", 2: "提督", 3: "舰长"}
                    level_name = level_names.get(level, f"未知({level})")
                    print(f"  {level_name}: {count}人")

                # 陪伴天数统计
                accompany_days = [guard["accompany"] for guard in total_list]
                if accompany_days:
                    print(f"陪伴天数: 最长{max(accompany_days)}天, 平均{sum(accompany_days) // len(accompany_days)}天")

        else:
            print(f"获取大航海列表失败: {result['error']}")
            if "response_data" in result:
                print(f"完整响应: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)}")

        def get_guard_dict(api, roomid, ruid, **kwargs):
            """
            获取大航海成员字典的包装函数

            Args:
                api: BilibiliApiGeneric 实例
                roomid: 直播间号
                ruid: 主播UID
                **kwargs: 其他参数传递给 get_guard_list

            Returns:
                包含操作结果的字典，其中data字段包含guard_dict
            """
            # 确保获取完整列表
            kwargs['include_total_list'] = True

            # 调用原函数
            result = api.get_guard_list(roomid, ruid, **kwargs)

            if result["success"]:
                # 转换列表为字典
                guard_dict = {}
                total_list = result["data"].get("total_list", [])

                for guard in total_list:
                    uid = guard["uinfo"]["uid"]
                    guard_level = guard["uinfo"]["guard"]["level"]
                    guard_dict[uid] = guard_level

                # 将字典添加到返回数据中
                result["data"]["guard_dict"] = guard_dict

            return result


        # 使用示例
        result = get_guard_dict(api, room_id, ruid, page=1)
        if result["success"]:
            guard_dict = result["data"]["guard_dict"]
            print("大航海成员字典:", guard_dict)

    except Exception as e:
        print(f"错误: {e}")




