import json
import requests
import time
from typing import Dict, Any, List, Union, Optional


class BilibiliApiGeneric:
    """
    不登录也能使用的Bilibili API集合

    提供不需要认证即可访问的Bilibili API功能
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def get_fans_members_rank(self, ruid: Union[int, str], page: int = 1,
                              page_size: int = 20, rank_type: Optional[int] = None,
                              include_total_list: bool = False) -> Dict[str, Any]:
        """
        获取粉丝团成员排名

        Args:
            ruid: 主播UID
            page: 页数（默认1）
            page_size: 每页返回数量（默认20，最大30）
            rank_type: 排序方式（1=按粉丝牌亮着的成员亲密度，2=按没上过舰的成员亲密度）
            include_total_list: 是否获取并返回完整的粉丝团成员列表（默认为False）

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（粉丝团成员信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not ruid:
                return {
                    "success": False,
                    "message": "获取粉丝团成员失败",
                    "error": "主播UID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            if page <= 0:
                return {
                    "success": False,
                    "message": "获取粉丝团成员失败",
                    "error": "页数必须大于0",
                    "status_code": None,
                    "api_code": None
                }

            # 限制page_size在有效范围内
            if page_size <= 0 or page_size > 30:
                page_size = 20  # 使用默认值

            # API配置
            api_url = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank"

            # 构建请求参数
            params = {
                "ruid": str(ruid),
                "page": page,
                "page_size": page_size
            }

            # 添加排序参数
            if rank_type in [1, 2]:
                params["rank_type"] = rank_type
                # 当rank_type=2时需要ts参数
                if rank_type == 2:
                    params["ts"] = int(time.time() * 1000)  # 13位时间戳

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
                    "message": "获取粉丝团成员失败",
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
                    "message": "获取粉丝团成员失败",
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
                    "message": "获取粉丝团成员失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], dict):
                return {
                    "success": False,
                    "message": "获取粉丝团成员失败",
                    "error": "API返回数据格式无效",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            data = result["data"]

            # 基础返回数据
            response_data = {
                "item": data.get("item", []),  # 粉丝团成员列表
                "num": data.get("num", 0),  # 粉丝团成员总数
                "medal_status": data.get("medal_status", 0),  # 粉丝牌状态
                "page_info": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_members": data.get("num", 0)
                }
            }

            # 如果需要获取完整列表
            if include_total_list:
                total_list = self._get_complete_fans_list(ruid, rank_type)
                response_data["total_list"] = total_list

            return {
                "success": True,
                "message": "获取粉丝团成员成功",
                "data": response_data,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取粉丝团成员失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取粉丝团成员失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取粉丝团成员失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取粉丝团成员过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }

    def _get_complete_fans_list(self, ruid: Union[int, str],
                                rank_type: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取完整的粉丝团成员列表（内部方法）

        Args:
            ruid: 主播UID
            rank_type: 排序方式

        Returns:
            完整的粉丝团成员列表
        """
        complete_list = []
        page = 1

        while True:
            # 构建请求参数
            params = {
                "ruid": str(ruid),
                "page": page,
                "page_size": 30  # 使用最大页大小
            }

            # 添加排序参数
            if rank_type in [1, 2]:
                params["rank_type"] = rank_type
                if rank_type == 2:
                    params["ts"] = int(time.time() * 1000)

            try:
                # 发送API请求
                response = requests.get(
                    "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank",
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
                current_list = data.get("item", [])
                complete_list.extend(current_list)

                # 检查是否还有更多页
                total_members = data.get("num", 0)
                if not current_list or len(complete_list) >= total_members:
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
        # 获取粉丝团成员排名（包含完整列表）
        ruid = DataInput.get_emoticons_for_uid
        result = api.get_fans_members_rank(
            ruid=ruid,
            page=1,
            page_size=20,
            rank_type=1,  # 按粉丝牌亮着的成员亲密度排序
            include_total_list=True  # 设置为True获取完整列表
        )

        if result["success"]:
            fans_data = result["data"]
            print(json.dumps(fans_data, ensure_ascii=False, indent=2))

            # 处理结果
            page_info = fans_data["page_info"]
            print(f"\n粉丝团统计信息:")
            print(f"总成员数: {page_info['total_members']}")
            print(f"当前页: {page_info['current_page']}")
            print(f"每页大小: {page_info['page_size']}")

            # 显示当前页成员
            print(f"\n📋 当前页成员 (前{len(fans_data['item'])}名):")
            for member in fans_data["item"]:
                rank = member["user_rank"]
                name = member["name"]
                score = member["score"]
                medal_level = member["level"]
                guard_level = member.get("guard_level", 0)

                guard_names = {1: "总督", 2: "提督", 3: "舰长", 0: "无"}
                guard_name = guard_names.get(guard_level, "未知")

                print(f"第{rank}名: {name} - 粉丝牌Lv{medal_level} - 亲密度{score} - {guard_name}")

            # 如果包含完整列表，显示统计信息
            if "total_list" in fans_data:
                total_list = fans_data["total_list"]
                print(f"\n📊 完整粉丝团列表统计 ({len(total_list)} 名成员):")

                # 粉丝牌等级统计
                level_count = {}
                for member in total_list:
                    level = member["level"]
                    level_count[level] = level_count.get(level, 0) + 1

                print(f"粉丝牌等级分布:")
                for level, count in sorted(level_count.items()):
                    print(f"  Lv{level}: {count}人")

                # 大航海等级统计
                guard_count = {}
                for member in total_list:
                    guard_level = member.get("guard_level", 0)
                    guard_count[guard_level] = guard_count.get(guard_level, 0) + 1

                print(f"大航海等级分布:")
                for level, count in sorted(guard_count.items()):
                    guard_names = {1: "总督", 2: "提督", 3: "舰长", 0: "无"}
                    guard_name = guard_names.get(level, "未知")
                    print(f"  {guard_name}: {count}人")

                # 亲密度统计
                scores = [member["score"] for member in total_list]
                if scores:
                    print(f"亲密度: 最高{max(scores)}, 平均{sum(scores) // len(scores)}")

        else:
            print(f"获取粉丝团成员失败: {result['error']}")
            if "response_data" in result:
                print(f"完整响应: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)}")

    except Exception as e:
        print(f"错误: {e}")