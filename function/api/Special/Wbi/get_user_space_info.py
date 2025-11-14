from pathlib import Path
from typing import Dict, Any
from urllib.parse import quote
from functools import reduce
from hashlib import md5
import urllib.parse
import time

import requests

from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager


class WbiSigna:
    def __init__(self, headers: dict, verify_ssl: bool = True):
        """
        wbi签名的api
        Args:
            headers: 包含Cookie等认证信息的请求头字典
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

    def get_user_space_info(self, mid: int) -> Dict[str, Any]:
        """
        获取用户空间详细信息

        Args:
            mid: 目标用户mid

        Returns:
            包含用户空间信息的字典：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的用户数据
            - error: 失败时的错误信息
            - status_code: HTTP状态码（如果有）
        """
        try:
            # 检查用户ID是否有效
            if not mid or mid <= 0:
                return {
                    "success": False,
                    "message": "获取用户空间信息失败",
                    "error": "用户ID无效",
                    "status_code": None,
                    "data": None
                }

            # 构建API请求
            api_url = "https://api.bilibili.com/x/space/wbi/acc/info"
            params = self.wbi({"mid": mid})

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
                    "message": "获取用户空间信息失败",
                    "error": f"HTTP错误: {response.status_code}",
                    "status_code": response.status_code,
                    "data": None,
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
                    "api_code": result.get("code"),
                    "data": None
                }

            # 检查数据是否存在
            if "data" not in result:
                return {
                    "success": False,
                    "message": "API响应格式异常",
                    "error": "响应中缺少必要的数据字段",
                    "status_code": response.status_code,
                    "data": None,
                    "response_data": result
                }

            # 成功返回
            return {
                "success": True,
                "message": "用户空间信息获取成功",
                "data": result["data"],
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": "请求超时",
                "status_code": None,
                "data": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": "网络连接错误",
                "status_code": None,
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "获取用户空间信息失败",
                "error": f"网络请求异常: {str(e)}",
                "status_code": None,
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "获取用户空间信息过程中发生未知错误",
                "error": str(e),
                "status_code": None,
                "data": None
            }


# 使用示例
if __name__ == '__main__':
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建实例
    wbi_signa = WbiSigna(Headers)

    # 获取用户空间信息（示例用户ID）
    user_info = wbi_signa.get_user_space_info(143474500)

    if user_info["success"]:
        print("用户空间信息获取成功")
        data = user_info["data"]
        print(f"用户昵称: {data.get('name', '未知')}")
        print(f"用户等级: {data.get('level', '未知')}")
        print(f"签名: {data.get('sign', '无签名')}")
        print(f"粉丝勋章: {data.get('fans_medal', {}).get('medal', {}).get('medal_name', '无')}")
    else:
        print(f"获取用户空间信息失败: {user_info['error']}")
        if "status_code" in user_info and user_info["status_code"]:
            print(f"HTTP状态码: {user_info['status_code']}")
        if "api_code" in user_info:
            print(f"API错误码: {user_info['api_code']}")