# 上传 和 更新 直播间封面
import json
import os
import pathlib
import random
import string
import time
import urllib
from io import BytesIO
from pathlib import Path
from typing import Literal, Optional, Dict
from urllib.parse import quote
from function.tools.parse_cookie import parse_cookie as cookie2dict
from function.tools.dict_to_cookie_string import dict_to_cookie_string as dict2cookie
from function.tools.BilibiliUserConfigManager import BilibiliUserConfigManager

import requests
from PIL import Image


class CsrfAuthentication:
    """需要Csrf鉴权的"""

    def __init__(self, headers: Dict[str, str]):
        """
        需要 Csrf
        :param headers:
        """
        self.headers = headers
        self.cookie = self.headers["cookie"]
        self.cookies = cookie2dict(self.cookie)
        self.csrf = self.cookies["bili_jct"]

    def update_cover(self, CoverUrl: str):
        headers = self.headers
        # 构建请求参数
        api_url = "https://api.live.bilibili.com/xlive/app-blink/v1/preLive/UpdatePreLiveInfo"
        update_cover_data = {
            "platform": "web",
            "mobi_app": "web",
            "build": 1,
            "cover": CoverUrl,
            "coverVertical": "",
            "liveDirectionType": 1,
            "csrf_token": self.cookies["bili_jct"],
            "csrf": self.cookies["bili_jct"],
        }
        update_cover_ReturnValue = requests.post(api_url, headers=headers, params=update_cover_data).json()
        return update_cover_ReturnValue


if __name__ == '__main__':
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict2cookie(cookies)
    }

    update_cover_ReturnValue = CsrfAuthentication(Headers).update_cover("http://i0.hdslb.com/bfs/live/new_room_cover/ea06f7092d34e9d563c950d1b0df41cc4da46c6b.jpg")
    print(update_cover_ReturnValue)
