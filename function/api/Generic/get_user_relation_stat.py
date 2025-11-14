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

    def get_user_relation_stat(self, vmid: Union[int, str]) -> Dict[str, Any]:
        """
        获取用户关注数和粉丝数统计

        Args:
            vmid: 用户MID

        Returns:
            包含操作结果的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（关注粉丝统计信息）
            - error: 失败时的错误信息
            - status_code: HTTP状态码
            - api_code: B站API返回的状态码
        """
        try:
            # 验证输入参数
            if not vmid:
                return {
                    "success": False,
                    "message": "获取用户关系统计失败",
                    "error": "用户MID不能为空",
                    "status_code": None,
                    "api_code": None
                }

            # API配置
            api_url = "https://api.bilibili.com/x/relation/stat"

            # 构建请求参数
            params = {
                "vmid": str(vmid)
            }

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
                    "message": "获取用户关系统计失败",
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
                    "message": "获取用户关系统计失败",
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
                    "message": "获取用户关系统计失败",
                    "error": f"API错误: {error_msg}",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            # 验证数据格式
            if "data" not in result or not isinstance(result["data"], dict):
                return {
                    "success": False,
                    "message": "获取用户关系统计失败",
                    "error": "API返回数据格式无效",
                    "status_code": response.status_code,
                    "api_code": api_code,
                    "response_data": result
                }

            data = result["data"]

            # 提取关键信息
            response_data = {
                "mid": data.get("mid"),  # 用户MID
                "following": data.get("following", 0),  # 关注数
                "follower": data.get("follower", 0),  # 粉丝数
                "black": data.get("black", 0),  # 黑名单数
                "whisper": data.get("whisper", 0),  # 悄悄关注数
                "raw_data": data  # 原始数据
            }

            return {
                "success": True,
                "message": "获取用户关系统计成功",
                "data": response_data,
                "status_code": response.status_code,
                "api_code": api_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户关系统计失败",
                "error": "请求超时",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户关系统计失败",
                "error": "网络连接错误",
                "status_code": None,
                "api_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户关系统计失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "api_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户关系统计过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "api_code": None
            }


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
        # 获取用户关系统计
        # 这里假设DataInput.get_user_relation_stat_for_uid包含用户MID
        vmid = DataInput.get_user_relation_stat_for_uid

        result = api.get_user_relation_stat(vmid=vmid)

        if result["success"]:
            relation_data = result["data"]
            print(json.dumps(relation_data, ensure_ascii=False, indent=2))

            # 显示关键信息
            print(f"\n📊 用户关系统计 (MID: {relation_data['mid']}):")
            print(f"👥 关注数: {relation_data['following']}")
            print(f"❤️  粉丝数: {relation_data['follower']}")
            print(f"🚫 黑名单数: {relation_data['black']}")
            print(f"🤫 悄悄关注数: {relation_data['whisper']}")

            # 计算粉丝关注比（如果有粉丝）
            if relation_data['follower'] > 0 and relation_data['following'] > 0:
                ratio = relation_data['follower'] / relation_data['following']
                print(f"📈 粉丝关注比: {ratio:.2f}")

        else:
            print(f"获取用户关系统计失败: {result['error']}")
            if "response_data" in result:
                print(f"完整响应: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)}")

    except Exception as e:
        print(f"错误: {e}")