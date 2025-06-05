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

import requests
from PIL import Image


class BilibiliUserLogsIn2ConfigFile:
    """
    管理B站用户登录配置文件的增删改查操作
    配置文件结构示例：
    {
        "DefaultUser": "12345",
        "12345": {
            "DedeUserID": "12345",
            "SESSDATA": "xxxxx",
            "bili_jct": "xxxxx",
            ...
        }
    }
    """

    def __init__(self, configPath: pathlib.Path):
        """
        初始化配置文件管理器
        Args:
            configPath: 配置文件路径对象
        Raises:
            IOError: 文件读写失败时抛出
            json.JSONDecodeError: 配置文件内容格式错误时抛出
        """
        self.configPath = configPath
        self._ensure_config_file()

    def _ensure_config_file(self):
        """确保配置文件存在且结构有效"""
        if not self.configPath.exists():
            self.configPath.parent.mkdir(parents=True, exist_ok=True)
            self._write_config({"DefaultUser": None})

        config = self._read_config()
        if "DefaultUser" not in config:
            config["DefaultUser"] = None
            self._write_config(config)

    def _read_config(self) -> Dict:
        """读取配置文件内容"""
        try:
            with open(self.configPath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"配置文件损坏或格式错误: {str(e)}") from e

    def _write_config(self, config: Dict):
        """写入配置文件"""
        try:
            with open(self.configPath, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise RuntimeError(f"配置文件写入失败: {str(e)}") from e

    def addUser(self, cookies: dict) -> None:
        """
        添加新用户配置
        Args:
            cookies: 包含完整cookie信息的字典，必须包含以下字段：
                     DedeUserID, DedeUserID__ckMd5, SESSDATA,
                     bili_jct, buvid3, b_nut
        Raises:
            ValueError: 缺少必要字段或用户已存在时抛出
        """
        required_keys = {
            "DedeUserID", "DedeUserID__ckMd5", "SESSDATA",
            "bili_jct", "buvid3", "b_nut"
        }
        if not required_keys.issubset(cookies.keys()):
            missing = required_keys - cookies.keys()
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")

        uid = str(cookies["DedeUserID"])
        config = self._read_config()

        if uid in config:
            raise ValueError(f"用户 {uid} 已存在")

        config[uid] = cookies
        self._write_config(config)

    def deleteUser(self, uid: int) -> None:
        """
        删除用户配置
        Args:
            uid: 要删除的用户ID
        Raises:
            ValueError: 用户不存在时抛出
        """
        config = self._read_config()
        uid_str = str(uid)

        if uid_str not in config:
            raise ValueError(f"用户 {uid} 不存在")

        # 处理默认用户
        if config["DefaultUser"] == uid_str:
            config["DefaultUser"] = None

        del config[uid_str]
        self._write_config(config)

    def updateUser(self, cookies: Optional[dict], setDefaultUserIs: bool = True) -> None:
        """
        更新用户配置或清空默认用户
        Args:
            cookies: 包含完整cookie信息的字典，传 None 表示清空默认用户
                - 示例: {"DedeUserID": "123", "SESSDATA": "xxx"...}
                - 传 None 时需配合 set_default_user=True 使用
            setDefaultUserIs: 是否设为默认用户
                - 当 cookies=None 时必须为 True
        Raises:
            ValueError: 以下情况时抛出
                - cookies 不完整或用户不存在
                - cookies=None 但 set_default_user=False
        """
        config = self._read_config()

        # 处理清空默认用户场景
        if cookies is None:
            if not setDefaultUserIs:
                raise ValueError("cookies=None 时必须设置 set_default_user=True")
            config["DefaultUser"] = None
            self._write_config(config)
            return

        # 原始验证逻辑
        required_keys = {"DedeUserID", "SESSDATA", "bili_jct"}
        if not required_keys.issubset(cookies.keys()):
            missing = required_keys - cookies.keys()
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")

        uid = str(cookies["DedeUserID"])
        if uid not in config:
            raise ValueError(f"用户 {uid} 不存在")

        # 更新用户数据
        config[uid].update(cookies)

        # 设置默认用户
        if setDefaultUserIs:
            config["DefaultUser"] = uid

        self._write_config(config)

    def getCookies(self, uid: Optional[int] = None) -> Optional[dict]:
        """
        获取指定用户的cookie信息
        Args:
            uid: 用户ID，None表示获取默认用户
        Returns:
            用户cookie字典，未找到返回None
        """
        config = self._read_config()
        # 如果uid是None表示获取默认用户
        if uid is None:
            uid = config.get("DefaultUser")
        # 如果默认用户是None输出None
        if uid is None:
            return None

        uid_str = str(uid)
        return config.get(uid_str)

    def getUsers(self) -> Dict[int, Optional[str]]:
        """
        获取所有用户列表（包含默认用户占位）
        Returns:
            字典格式 {序号: 用户ID}，其中：
            - 键 0: 默认用户ID（若未设置则为 None）
            - 键 1~N: 其他用户ID（按插入顺序编号）
        """
        config = self._read_config()
        # 获取所有用户ID（排除系统字段）
        user_ids = [
            uid for uid in config.keys()
            if uid not in {"DefaultUser", "0"}  # 过滤系统保留字段
               and uid.isdigit()  # 确保是数字型用户ID
        ]
        # 构建字典（强制包含 0: None）
        users = {
            0: config.get("DefaultUser")  # 允许 None
        }
        # 添加其他用户（过滤掉默认用户避免重复）
        default_uid = config.get("DefaultUser")
        if default_uid and default_uid in user_ids:
            user_ids.remove(default_uid)  # 避免重复
        for idx, uid in enumerate(user_ids, start=1):
            users[idx] = uid
        return users


def url_decoded(url_string: str) -> str:
    """
    将 UTF-8 解码成 URL编码
    @param url_string: 要解码的 UTF-8 编码字符串
    @return: URL编码
    """
    # 使用quote()函数将URL编码转换为UTF-8
    utf8_encoded = quote(url_string, encoding='utf-8')
    return utf8_encoded


def cookie2dict(cookie: str) -> Dict[str, str]:
    """
    将符合HTTP标准的Cookie字符串转换为字典
    Args:
        cookie: Cookie字符串
            示例: "name=value; age=20; token=abc%20123"
    Returns:
        解析后的字典，键值均为字符串类型
        示例: {'name': 'value', 'age': '20', 'token': 'abc 123'}
    Raises:
        ValueError: 当输入不是字符串时抛出
    Features:
        - 自动处理URL解码
        - 兼容不同分隔符（; 或 ; ）
        - 过滤空值和无效条目
        - 保留重复键的最后出现值（符合HTTP规范）
    """
    if not isinstance(cookie, str):
        raise TypeError("输入必须是字符串类型")
    cookie_dict = {}
    # 处理空字符串和去除首尾空格
    cookie_str = cookie.strip()
    if not cookie_str:
        return cookie_dict
    # 兼容不同分隔符格式（支持 ; 和 ; ）
    for pair in cookie_str.split(';'):
        pair = pair.strip()
        if not pair:
            continue
        # 处理键值对（仅分割第一个等号）
        try:
            key, value = pair.split('=', 1)
        except ValueError:
            continue  # 跳过无效条目
        key = key.strip()
        value = value.strip()
        # 执行URL解码（仅值部分）
        try:
            decoded_value = urllib.parse.unquote(value)
        except Exception:
            decoded_value = value  # 解码失败保留原始值
        cookie_dict[key] = decoded_value
    return cookie_dict


def dict2cookie(jsondict: dict) -> str:
    """
    将 dict 转换为 cookie格式
    @param jsondict: 字典
    @return: cookie格式的字典
    """
    cookie = ''
    for json_dictK in jsondict:
        json_dictki = json_dictK
        json_dictVi = jsondict[json_dictki]
        cookie += url_decoded(str(json_dictki)) + '=' + url_decoded(str(json_dictVi)) + '; '
    cookie = cookie.strip()
    if cookie.endswith(";"):
        cookie = cookie[:-1]
    return cookie


def PIL_Image2CentralProportionCutting(
        PIL_Image: Image.Image,
        target_WidthToHeightRatio: float
) -> Optional[Image.Image]:
    """
    对图像进行中心比例裁切，保持目标宽高比

    Args:
        PIL_Image: 要处理的 PIL 图像对象
        target_WidthToHeightRatio: 目标宽高比（宽度/高度的比值）
            示例：
            - 16:9 → 16/9 ≈ 1.778
            - 1:1 → 1.0
            - 4:3 → 1.333

    Returns:
        Image.Image: 裁切后的新图像对象，如果裁切失败返回 None

    Raises:
        TypeError: 输入不是有效的 PIL 图像对象
        ValueError: 目标比例不是正数或裁切尺寸无效
    """
    # 参数验证
    if not isinstance(PIL_Image, Image.Image):
        raise TypeError("输入必须是有效的 PIL.Image.Image 对象")

    if target_WidthToHeightRatio <= 0:
        raise ValueError("目标比例必须是正数")

    # 获取原始尺寸
    original_width, original_height = PIL_Image.size
    original_ratio = original_width / original_height

    try:
        # 计算裁切区域
        if original_ratio > target_WidthToHeightRatio:
            # 过宽：固定高度，计算宽度
            crop_height = original_height
            crop_width = int(round(crop_height * target_WidthToHeightRatio))
        else:
            # 过高：固定宽度，计算高度
            crop_width = original_width
            crop_height = int(round(crop_width / target_WidthToHeightRatio))

        # 验证裁切尺寸
        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("计算出的裁切尺寸无效")
        if crop_width > original_width or crop_height > original_height:
            raise ValueError("原始图片尺寸不足以完成裁切")

        # 计算裁切坐标
        left = (original_width - crop_width) // 2
        top = (original_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        return PIL_Image.crop((left, top, right, bottom))

    except ValueError as e:
        raise ValueError(f"裁切失败: {str(e)}")
    except Exception as e:
        raise ValueError(f"未知错误: {str(e)}")


def PIL_Image2Zooming(
        PIL_Image: Image.Image,
        ZoomingQuality: Literal[1, 2, 3, 4],
        target_width: Optional[int] = None,  # Optional[int] 可以简写为 int | None
        scale_factor: Optional[int] = None  # Optional[int] 可以简写为 int | None
) -> Image.Image:
    """
    对 PIL 图像进行缩放操作，支持指定目标宽度或缩小倍数

    Args:
        PIL_Image: 要缩放的 PIL 图像对象
        ZoomingQuality: 缩放质量等级 (1-4)
            1 = 最近邻 (速度快质量低)
            2 = 双线性 (平衡模式)
            3 = 双三次 (高质量放大)
            4 = Lanczos (最高质量)
        target_width: 目标宽度（与 scale_factor 二选一）
        scale_factor: 缩小倍数（与 target_width 二选一）

    Returns:
        dict: 包含两种缩放结果的字典
            widthZoomingPIL_Image: 按宽度缩放的结果图像（如参数有效）
            timesZoomingPIL_Image: 按比例缩放的结果图像（如参数有效）

    Raises:
        ValueError: 参数不符合要求时抛出
        TypeError: 输入图像类型错误时抛出
    """
    # 参数验证
    if not isinstance(PIL_Image, Image.Image):
        raise TypeError("输入必须是 PIL.Image.Image 对象")
    if ZoomingQuality not in (1, 2, 3, 4):
        raise ValueError("缩放质量等级必须是 1-4 的整数")
    if not (False if bool(target_width) == bool(scale_factor) else True):
        raise ValueError("正确使用参数 target_width 或 scale_factor")
    # 选择重采样滤波器
    resampling_filter4ZoomingQuality = {
        1: Image.NEAREST,
        2: Image.BILINEAR,
        3: Image.BICUBIC,
        4: Image.LANCZOS,
    }
    resampling_filter = resampling_filter4ZoomingQuality[ZoomingQuality]
    # """
    # 滤波器名称	    质量	速度	适用场景
    # Image.NEAREST	低	最快	像素艺术/保留原始像素值
    # Image.BILINEAR	中	较快	通用缩放（默认选项）
    # Image.BICUBIC	高	较慢	高质量放大
    # Image.LANCZOS	最高	最慢	超高精度缩放（推荐选项）
    # """
    original_width, original_height = PIL_Image.size
    widthHeightRatio = original_width / original_height
    new_width = None
    if target_width:
        if target_width > original_width:
            raise ValueError("目标宽度必须小于原宽度")
        new_width = target_width
    elif scale_factor:
        if scale_factor < original_height:
            raise ValueError("比例因子必须小于原高度")
        if 1 < scale_factor:
            raise ValueError("比例因子必须大于1")
        new_width = original_width / scale_factor
    new_height = new_width / widthHeightRatio
    ZoomingPIL_Image = PIL_Image.resize((round(new_width), round(new_height)), resampling_filter)
    return ZoomingPIL_Image


def PIL_Image2Binary(
        PIL_Image: Image.Image,
        ImgFormat: Literal["PNG", "JPEG"],
        compress_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
) -> bytes:
    """
    将 PIL 图像对象转换为指定格式的二进制数据

    Args:
        PIL_Image: PIL 图像对象
        ImgFormat: 输出图像格式
            "PNG" - 使用无损压缩
            "JPEG" - 使用有损压缩
        compress_level: 压缩等级 (不同格式有不同表现)
            对于 PNG: 压缩级别 0-9 (0=无压缩，9=最大压缩)
            对于 JPEG: 质量等级 5-95 (自动映射压缩级别到质量参数)

    Returns:
        bytes: 图像二进制数据

    Raises:
        ValueError: 参数不合法时抛出
        OSError: 图像保存失败时抛出
    """
    # 参数验证
    if not isinstance(PIL_Image, Image.Image):
        raise ValueError("输入必须是有效的 PIL.Image.Image 对象")
    if ImgFormat not in ("PNG", "JPEG"):
        raise ValueError(f"不支持的图像格式: {ImgFormat}，只支持 PNG/JPEG")
    if compress_level not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        raise ValueError(f"不支持的压缩级别: {compress_level}，只支持 0～9")
    # 准备保存参数
    save_kwargs = {}

    match ImgFormat:
        case "PNG":
            save_kwargs = {
                "format": "PNG",
                "compress_level": compress_level  # 将压缩级别映射到质量参数 (0=最高压缩，9=最高质量)
            }
        case "JPEG":
            quality = 95 - (compress_level * 10)
            quality = max(5, min(95, quality))  # 确保在有效范围内
            # 转换图像模式为 RGB
            if PIL_Image.mode != "RGB":
                PIL_Image = PIL_Image.convert("RGB")
            save_kwargs = {
                "format": "JPEG",
                "quality": quality,
                "subsampling": 0 if quality >= 90 else 1  # 高质量使用全采样
            }
    # 执行转换
    buffer = BytesIO()
    try:
        PIL_Image.save(buffer, **save_kwargs)
    except Exception as e:
        raise OSError(f"图像保存失败: {str(e)}") from e
    image_bytes = buffer.getvalue()  # 转换为字节流
    return image_bytes


class CsrfAuthentication:
    """需要Csrf鉴权的"""

    def __init__(self, cookie: str):
        """
        需要Csrf
        :param cookie:
        """
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0")
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
        }
        self.cookies = cookie2dict(cookie)
        self.cookie = cookie
        self.csrf = self.cookies["bili_jct"]

    def upload_cover(self, image_binary: bytes):
        """
        上传直播间封面到B站(符合官方请求格式)
        :param image_binary: png/jpeg图像的二进制格式数据
        """
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
              "537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        # 构建请求参数
        api_url = "https://api.bilibili.com/x/upload/web/image"
        # 准备multipart/form-data数据
        boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        headers = {
            "User-Agent": UA,
            "Cookie": self.cookie,
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
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
        print("[上传结果]", result)
        return result

    def update_cover(self, CoverUrl: str):
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
              "537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        headers = {
            "User-Agent": UA,
            "cookie": self.cookie,
        }
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
        print(update_cover_ReturnValue)


PIL_Image = Image.open('/Volumes/Movies/系统录屏/明日方舟.png')
PIL_Image0403 = PIL_Image2CentralProportionCutting(PIL_Image, 4 / 3)
PIL_Image1609 = PIL_Image2CentralProportionCutting(PIL_Image, 16 / 9)
PIL_Image1609ZoomingWidth1020 = PIL_Image2Zooming(PIL_Image1609, 4, target_width=1020)
PIL_Image1609ZoomingWidth1020.save("output.png")
PIL_Image1609ZoomingWidth1020Binary = PIL_Image2Binary(PIL_Image1609ZoomingWidth1020, ImgFormat="JPEG", compress_level=0)
BULC = BilibiliUserLogsIn2ConfigFile(
    Path(
        '/Applications/OBS.app/Contents/PlugIns/frontend-tools.plugin/Contents/Resources/scripts/bilibili-live/config.json'
    )
)
cookies = BULC.getCookies()

coverUrl = CsrfAuthentication(dict2cookie(cookies)).upload_cover(PIL_Image1609ZoomingWidth1020Binary)['data']['location']
CsrfAuthentication(dict2cookie(cookies)).update_cover(coverUrl)
