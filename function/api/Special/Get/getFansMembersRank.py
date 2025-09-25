import time
from pathlib import Path
from typing import Dict, Any

import requests

from function.tools.parse_cookie import parse_cookie
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.BilibiliUserConfigManager import BilibiliUserConfigManager


class BilibiliCSRFAuthenticator:
    """
    B站CSRF认证管理器，用于处理需要CSRF令牌的API请求。

    该类专门用于B站直播相关的CSRF认证操作，特别是直播公告的更新。
    自动从Cookie中提取必要的认证信息，并提供简化的API调用接口。

    特性：
    - 自动从Cookie中解析CSRF令牌（bili_jct）
    - 自动提取用户ID（DedeUserID）
    - 支持SSL验证配置
    - 提供直播公告更新功能
    - 统一的错误处理和响应格式
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化CSRF认证管理器

        Args:
            headers: 包含Cookie等认证信息的请求头字典
            verify_ssl: 是否验证SSL证书（默认True，生产环境建议开启）

        Returns:
            包含操作结果的字典，包含以下键：
            - success: 操作是否成功
            - message: 结果描述信息
            - data: 成功时的数据（如认证器实例）
            - error: 失败时的错误信息
        """
        self.headers = headers.copy()  # 避免修改原始headers
        self.verify_ssl = verify_ssl
        self.initialization_result = self._initialize_authenticator()

    def _initialize_authenticator(self) -> Dict[str, Any]:
        """
        初始化认证器的内部实现

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
            required_fields = ["bili_jct", "DedeUserID"]
            missing_fields = [field for field in required_fields if field not in self.cookies]
            if missing_fields:
                return {
                    "success": False,
                    "message": "初始化失败",
                    "error": f"Cookie中缺少必要字段: {', '.join(missing_fields)}"
                }

            self.user_id = self.cookies["DedeUserID"]
            self.csrf = self.cookies["bili_jct"]

            return {
                "success": True,
                "message": "认证器初始化成功",
                "data": {
                    "user_id": self.user_id,
                    "csrf_token": self.csrf
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": "初始化过程中发生异常",
                "error": str(e)
            }

    def validate_csrf_token(self) -> Dict[str, Any]:
        """
        验证CSRF令牌是否有效

        Returns:
            包含验证结果的字典：
            - success: 验证是否成功
            - valid: CSRF令牌是否有效
            - message: 结果描述信息
        """
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "valid": False,
                "message": "认证器未正确初始化"
            }

        is_valid = bool(self.csrf and len(self.csrf) == 32)

        return {
            "success": True,
            "valid": is_valid,
            "message": "CSRF令牌有效" if is_valid else "CSRF令牌无效"
        }

    def get_user_info(self) -> Dict[str, Any]:
        """
        获取用户基本信息

        Returns:
            包含用户信息的字典：
            - success: 操作是否成功
            - data: 用户信息字典（包含user_id, csrf_token, has_valid_csrf）
            - message: 结果描述信息
        """
        if not self.initialization_result["success"]:
            return {
                "success": False,
                "message": "无法获取用户信息，认证器未正确初始化",
                "error": self.initialization_result.get("error", "未知错误")
            }

        validation_result = self.validate_csrf_token()

        return {
            "success": True,
            "data": {
                "user_id": self.user_id,
                "csrf_token": self.csrf,
                "has_valid_csrf": validation_result["valid"]
            },
            "message": "用户信息获取成功"
        }

    def getFansMembersRank(self, uid: int) -> list:
        """
        通过用户的B站uid查看他的粉丝团成员列表
        :param uid:B站uid
        :return: list元素：[{face：头像url，guard_icon：舰队职位图标url，guard_level：舰队职位 1|2|3->总督|提督|舰长，honor_icon：""，level：粉丝牌等级，medal_color_border：粉丝牌描边颜色数值为 10 进制的 16 进制值，medal_color_start：勋章起始颜色，medal_color_end：勋章结束颜色，medal_name：勋章名，name：用户昵称，score：勋章经验值，special：""，target_id：up主mid，uid：用户mid，user_rank：在粉丝团的排名}]
        """
        api = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank"
        headers = self.headers
        page = 0
        # maxpage = 1
        RankFans = []
        FansMember = True
        while FansMember:
            # while page <= maxpage:
            page += 1
            data = {
                "ruid": uid,
                "page": page,
                "page_size": 30,
            }
            try:
                FansMembersRank = requests.get(api, headers=headers, params=data).json()
            except:
                time.sleep(5)
                FansMembersRank = requests.get(api, headers=headers, params=data).json()
            # num_FansMembersRank = FansMembersRank["data"]["num"]
            # print(FansMembersRank)
            FansMember = FansMembersRank["data"]["item"]
            # RankFans.append(FansMember)
            if FansMember:
                RankFans += FansMember
            # maxpage = math.ceil(num_FansMembersRank / 30) + 1
        return RankFans


# 使用示例
if __name__ == "__main__":
    # 示例用法
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    # 创建认证器实例
    authenticator = BilibiliCSRFAuthenticator(Headers)

    # 检查初始化结果
    if authenticator.initialization_result["success"]:
        # 获取用户信息
        user_info = authenticator.get_user_info()
        if user_info["success"]:
            print("# 在这里处理成功的用户信息",user_info)
            fmr = authenticator.getFansMembersRank(1639389144)
            print(len(fmr), fmr)
            pass
        else:
            print("# 在这里处理获取用户信息失败的情况")
            pass
    else:
        print("# 在这里处理初始化失败的情况")
        pass