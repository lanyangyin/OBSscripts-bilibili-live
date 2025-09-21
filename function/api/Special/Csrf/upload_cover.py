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
from function.tools.crop_image_to_aspect_ratio import crop_image_to_aspect_ratio
from function.tools.resize_image import resize_image
from function.tools.convert_pil_image_to_bytes import convert_pil_image_to_bytes
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

    def upload_cover(self, image_binary: bytes):
        """
        上传直播间封面到B站(符合官方请求格式)
        :param image_binary: png/jpeg图像的二进制格式数据
        """
        # 构建请求参数
        api_url = "https://api.bilibili.com/x/upload/web/image"
        # 准备multipart/form-data数据
        boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        headers = self.headers
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        # 构建multipart body
        data_parts = []
        # 添加普通字段
        fields = {
            "bucket": "live",
            "dir": "new_room_cover",
            "csrf": self.cookies["bili_jct"]
        }
        for name, value in fields.items():
            data_parts.append(
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f'{value}\r\n'
            )
        data_parts.append(
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="blob"\r\n'
            f'Content-Type: image/jpeg\r\n\r\n'
        )
        data_parts.append(image_binary)
        data_parts.append(f'\r\n--{boundary}--\r\n')
        # 构建最终body
        body = b''
        for part in data_parts:
            if isinstance(part, str):
                body += part.encode('utf-8')
            else:
                body += part
        # 发送请求
        response = requests.post(url=api_url, headers=headers, data=body).json()
        # 处理响应
        result = response
        return result


if __name__ == '__main__':
    PIL_Image = Image.open('..\..\TestOutput\直播背景.png')
    PIL_Image0403 = crop_image_to_aspect_ratio(PIL_Image, 4 / 3)
    PIL_Image1609 = crop_image_to_aspect_ratio(PIL_Image, 16 / 9)
    PIL_Image1609ZoomingWidth1020 = resize_image(PIL_Image1609, 4, target_width=1020)
    PIL_Image1609ZoomingWidth1020.save("../../TestOutput/upload_cover/output.png")
    PIL_Image1609ZoomingWidth1020Binary = convert_pil_image_to_bytes(PIL_Image1609ZoomingWidth1020, "JPEG", 0)
    BULC = BilibiliUserConfigManager(Path('../../../../cookies/config.json'))
    cookies = BULC.get_user_cookies()
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict2cookie(cookies)
    }

    coverUrl = CsrfAuthentication(Headers).upload_cover(PIL_Image1609ZoomingWidth1020Binary)['data']['location']
    print(coverUrl)