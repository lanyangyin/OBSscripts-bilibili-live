from typing import Dict, Any, Union, Optional, List

import requests


class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_area_obj_list(self) -> Dict[str, Any]:
        """
        获取B站直播分区信息

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（分区信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            api_url = "https://api.live.bilibili.com/room/v1/Area/getList"

            # 发送API请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            data = response.json()

            # 验证API响应
            api_code = data.get("code", -1)
            if api_code != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 检查核心数据结构
            if "data" not in data or not isinstance(data["data"], list):
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "返回数据缺少分区列表",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            return {
                "success": True,
                "message": "获取分区信息成功",
                "data": data["data"],
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取分区信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def get_bilibili_user_card(self, mid: Union[int, str], photo: bool = False) -> Dict[str, Any]:
        """
        获取Bilibili用户名片信息

        Args:
            mid: 目标用户mid
            photo: 是否请求用户主页头图 (可选，默认为False)

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（用户信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not mid:
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": "用户MID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            # API地址
            url = "https://api.bilibili.com/x/web-interface/card"

            # 请求参数
            params = {
                'mid': mid,
                'photo': 'true' if photo else 'false'
            }

            # 发送GET请求
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=10,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            data = response.json()

            # 检查API返回状态
            api_code = data.get('code', -1)
            if api_code != 0:
                error_msg = data.get('message', '未知错误')
                return {
                    "success": False,
                    "message": "获取用户信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 返回完整的API响应数据
            return {
                "success": True,
                "message": "获取用户信息成功",
                "data": data,  # 返回完整的API响应
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

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

    def get_live_user_info(self, uid: int) -> Dict[str, Any]:
        """
        获取主播信息

        Args:
            uid: 目标用户mid

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（主播信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not uid or uid <= 0:
                return {
                    "success": False,
                    "message": "获取主播信息失败",
                    "error": "用户ID无效",
                    "status_code": None,
                    "api_code": None
                }

            api_url = "https://api.live.bilibili.com/live_user/v1/Master/info"
            params = {
                "uid": uid
            }

            # 发送请求
            response = requests.get(
                url=api_url,
                headers=self.headers,
                params=params,
                verify=self.verify_ssl,
                timeout=10
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取主播信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析响应
            result = response.json()

            # 根据B站API返回的状态码判断成功与否
            api_code = result.get("code", -1)
            if api_code == 0:
                return {
                    "success": True,
                    "message": "获取主播信息成功",
                    "data": result.get("data", {}),
                    "status_code": response.status_code,
                    "api_code": api_code
                }
            else:
                # 提取错误信息
                error_msg = result.get("msg") or result.get("message", "未知错误")
                return {
                    "success": False,
                    "message": "获取主播信息失败",
                    "error": error_msg,
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取主播信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取主播信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取主播信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取主播信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def get_anchor_common_areas(self, room_id: Union[str, int]) -> Dict[str, Any]:
        """
        获取主播常用分区信息

        参数:
            room_id: 直播间ID（整数或字符串）

        返回:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（分区列表）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not room_id:
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "房间ID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            # API配置
            api_url = "https://api.live.bilibili.com/room/v1/Area/getMyChooseArea"
            params = {"roomid": str(room_id)}

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
                    "message": "获取分区信息失败",
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
                    "message": "获取分区信息失败",
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
                    "message": "获取分区信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], list):
                return {
                    "success": False,
                    "message": "获取分区信息失败",
                    "error": "API返回数据格式无效",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证分区数据
            for area in result["data"]:
                required_keys = {"id", "name", "parent_id", "parent_name"}
                if not required_keys.issubset(area.keys()):
                    return {
                        "success": False,
                        "message": "获取分区信息失败",
                        "error": "分区数据缺少必需字段",
                        "status_code": response.status_code,
                        "api_code": api_code,
                        "response_data": result
                    }

            return {
                "success": True,
                "message": "获取分区信息成功",
                "data": result["data"],
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取分区信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取分区信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def get_room_base_info(self, room_id: int) -> Dict[str, Any]:
        """
        获取直播间基本信息

        Args:
            room_id: 直播间短ID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（直播间信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not room_id or room_id <= 0:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "房间ID无效",
                    "status_code": None,
                    "api_code": None
                }

            api_url = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
            params = {
                "req_biz": "web_room_componet",
                "room_ids": room_id
            }

            # 发送API请求
            response = requests.get(
                api_url,
                headers=self.headers,
                params=params,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            data = response.json()

            # 验证API响应
            api_code = data.get("code", -1)
            if api_code != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 提取房间信息
            by_room_ids = data.get("data", {}).get("by_room_ids", {})
            if not by_room_ids:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "未找到房间信息",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 返回第一个房间信息（即使多个也取第一个）
            room_info = next(iter(by_room_ids.values()), None)
            if not room_info:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "房间信息为空",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            return {
                "success": True,
                "message": "获取房间信息成功",
                "data": room_info,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取房间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def get_room_info_old(self, mid: int) -> Dict[str, Any]:
        """
        通过B站UID查询直播间基础信息

        Args:
            mid: B站用户UID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（直播间信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 参数验证
            if not isinstance(mid, int) or mid <= 0:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "mid 必须是正整数",
                    "status_code": None,
                    "api_code": None
                }

            api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
            params = {"mid": mid}

            # 发送请求
            response = requests.get(
                url=api,
                headers=self.headers,
                params=params,
                timeout=5.0,
                verify=self.verify_ssl
            )

            # 检查HTTP状态码
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "api_code": None,
                    "response_text": response.text
                }

            # 解析JSON响应
            try:
                data = response.json()
            except ValueError as e:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"解析API响应失败: {str(e)}",
                    "status_code": response.status_code,
                    "api_code": None
                }

            # 检查API返回状态码
            api_code = data.get("code", -1)
            if api_code != 0:
                error_msg = data.get("message") or data.get("msg") or "未知错误"
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 检查数据是否存在
            result = data.get("data")
            if not result:
                return {
                    "success": False,
                    "message": "获取房间信息失败",
                    "error": "API返回数据为空",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": data
                }

            # 确保返回完整字段结构
            room_info = {
                "roomStatus": result.get("roomStatus"),
                "roundStatus": result.get("roundStatus"),
                "liveStatus": result.get("liveStatus"),
                "url": result.get("url"),
                "title": result.get("title"),
                "cover": result.get("cover"),
                "online": result.get("online"),
                "roomid": result.get("roomid"),
                "broadcast_type": result.get("broadcast_type"),
                "online_hidden": result.get("online_hidden"),
                "link": result.get("link")  # 添加link字段
            }

            return {
                "success": True,
                "message": "获取房间信息成功",
                "data": room_info,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取房间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取房间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }





if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(headers)