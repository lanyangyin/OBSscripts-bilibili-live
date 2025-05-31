# coding=utf-8
#         Copyright (C) 2024  lanyangyin
#
#         This program is free software: you can redistribute it and/or modify
#         it under the terms of the GNU General Public License as published by
#         the Free Software Foundation, either version 3 of the License, or
#         (at your option) any later version.
#
#         This program is distributed in the hope that it will be useful,
#         but WITHOUT ANY WARRANTY; without even the implied warranty of
#         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#         GNU General Public License for more details.
#
#         You should have received a copy of the GNU General Public License
#         along with this program.  If not, see <https://www.gnu.org/licenses/>.
#         2436725966@qq.com
import asyncio
import base64
import io
import json
import os
import pprint
import sys
import threading
import time
import urllib
import zlib
from urllib.parse import quote
from pathlib import Path

import obspython as obs
import pypinyin
import qrcode
import requests
import pyperclip as cb
import websockets


def script_path():
    pass


# 工具类函数
class config_B:
    """
    配置文件 config.json 的 查找 和 更新
    """

    def __init__(self, uid: int, dirname: str):
        """
        @param uid: 用户id
        @param dirname: 配置文件 config.json 所在文件夹名
        """
        # 字符串化UID
        self.uid = str(uid)
        # 配置文件 config.json 路径
        self.configpath = Path(f'{dirname}') / "config.json"
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

    def update(self, cookies: dict):
        """
        记录uid和cookie到配置文件 config.json 中
        @param cookies: 登录获取的 cookies，字段来自 cookie
        """
        uid = self.uid
        # 配置文件 config.json 路径
        configpath = self.configpath
        # 判断配置文件 config.json 是否存在，不存在则创建一个初始配置文件
        try:
            with open(configpath, 'r', encoding='utf-8') as f:
                f.read()
        except:
            with open(configpath, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        # 判断配置文件 config.json 是否符合json格式，符合则更新 uid 对应的 cookie，不符合则备份违规文件并覆写 uid 对应的 cookie
        try:
            with open(configpath, 'r', encoding='utf-8') as f:
                config = json.load(f)
                config[uid] = cookies
                outputconfig = config
        except:
            with open(configpath, 'r', encoding='utf-8') as f:
                inputconfig = f.read()
                outputconfig = {uid: cookies}
            # 备份违规文件
            with open(str(time.strftime("%Y%m%d%H%M%S")) + '_config.json', 'w', encoding='utf-8') as f:
                f.write(inputconfig)
        # 更新uid和cookie到配置文件 config.json 中
        with open(configpath, 'w', encoding='utf-8') as f:
            json.dump(outputconfig, f, ensure_ascii=False, indent=4)

    def check(self) -> dict:
        """
        查询配置文件中保存的 uid 对应的 cookies，没有则为空字符
        @return: uid 对应的 cookies ，uid 不存在会返回{}
        """
        cookies = {}
        try:
            with open(self.configpath, 'r', encoding='utf-8') as f:
                cookies = json.load(f)[self.uid]
        except:
            pass
        return cookies


def split_by_n(seq, n):
    """
    每 n个字符 切分
    @param seq:切分字符串
    @type seq:str
    @param n:切分字数
    @type n: int
    @return:
    @rtype: list
    """
    return [seq[i:i + n] for i in range(0, len(seq), n)]


def split_of_list(txt: str, str_list: list):
    # 定义列表和字符串
    text = txt
    text = (text.replace("\"", "”").replace("'", "’").replace(",", "，")
            .replace("\n", ""))
    for ostr in str_list:
        text = text.replace(ostr, f"\', \'{ostr}\', \'")
    text = f"[\'{text}\']"
    split_text = eval(text)
    l = []
    for i in split_text:
        if i:
            l.append(i)
    return l


def dict2cookieformat(jsondict: dict) -> str:
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


def cookie2dict(cookie: str) -> dict:
    """
    将cookie字典化
    @param cookie:
    @return:
    """
    # 用分号分隔输入字符串
    key_value_pairs = cookie.split('; ')
    # 初始化空字典
    result_dict = {}
    # 遍历每个键值对
    for pair in key_value_pairs:
        # 将pair拆分为key和value
        key, value = pair.split('=')
        # 删除任何前导或尾随空格
        key = key.strip()
        value = value.strip()
        # 解码值中任何url编码的字符
        value = urllib.parse.unquote(value)
        # 将键值对添加到字典中
        result_dict[key] = value
    return result_dict


def url_decoded(url_string: str) -> str:
    """
    将 UTF-8 解码成 URL编码
    @param url_string: 要解码的 UTF-8 编码字符串
    @return: URL编码
    """
    # 使用quote()函数将URL编码转换为UTF-8
    utf8_encoded = quote(url_string, encoding='utf-8')
    return utf8_encoded


def qr_encode(qr_str: str, border: int = 2, invert: bool = False):
    """
    字符串转二维码
    @param qr_str: 二维码文本
    @param border: 边框大小
    @param invert: 黑白底转换
    @return: {"str": output_str, "base64": b64, "img": img}
    @rtype: dict[str, str, PilImage]
    """
    # 保存了当前的标准输出（stdout）
    savestdout = sys.stdout
    # 创建一个 StringIO 对象来捕获 print 输出
    output = io.StringIO()
    # 将系统的标准输出重定向到 output
    sys.stdout = output
    # 创建了一个 QRCode 对象 qr
    qr = qrcode.QRCode(
        version=1,  # 版本
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 纠错级别
        box_size=10,  # 方块大小
        border=border,  # 边框大小
    )
    # 将要转换的文本 qr_str 添加到二维码中
    qr.make(fit=True)
    qr.add_data(qr_str)
    # 生成二维码图像对象 img
    img = qr.make_image()
    # 将 Pillow 图像对象保存到一个内存中的字节流 buf 中
    buf = io.BytesIO()
    img.save(buf)  # , format='PNG'
    image_stream = buf.getvalue()
    # 将其转换为 PNG 格式的二进制流
    heximage = base64.b64encode(image_stream)
    # 使用 base64 编码转换成字符串 b64
    b64 = heximage.decode()
    # 使用 qr 对象的 print_ascii 方法将二维码以 ASCII 字符串的形式打印出来，并根据 invert 参数的值决定是否反转黑白颜色
    qr.print_ascii(out=None, tty=False, invert=invert)
    # 重定向输出到变量中
    output_str = output.getvalue()
    # 恢复 sys.stdout
    sys.stdout = savestdout
    out = {"str": output_str, "base64": b64, "img": img}
    return out


# end

# 不登录也能用的api
def getRoomInfoOld(mid: int) -> dict:
    """
    直接用Bid查询到的直播间基础信息<br>
    @param mid: B站UID
    @type mid: int
    @return:
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>roomStatus</td>
            <td>num</td>
            <td>直播间状态</td>
            <td>0：无房间<br>1：有房间</td>
        </tr>
        <tr>
            <td>roundStatus</td>
            <td>num</td>
            <td>轮播状态</td>
            <td>0：未轮播<br>1：轮播</td>
        </tr>
        <tr>
            <td>liveStatus</td>
            <td>num</td>
            <td>直播状态</td>
            <td>0：未开播<br>1：直播中</td>
        </tr>
        <tr>
            <td>url</td>
            <td>str</td>
            <td>直播间网页url</td>
            <td></td>
        </tr>
        <tr>
            <td>title</td>
            <td>str</td>
            <td>直播间标题</td>
            <td></td>
        </tr>
        <tr>
            <td>cover</td>
            <td>str</td>
            <td>直播间封面url</td>
            <td></td>
        </tr>
        <tr>
            <td>online</td>
            <td>num</td>
            <td>直播间人气</td>
            <td>值为上次直播时刷新</td>
        </tr>
        <tr>
            <td>roomid</td>
            <td>num</td>
            <td>直播间id（短号）</td>
            <td></td>
        </tr>
        <tr>
            <td>broadcast_type</td>
            <td>num</td>
            <td>0</td>
            <td></td>
        </tr>
        <tr>
            <td>online_hidden</td>
            <td>num</td>
            <td>0</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    @rtype: dict
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
    data = {
        "mid": mid,
    }
    RoomInfoOld = requests.get(api, headers=headers, params=data).json()
    return RoomInfoOld["data"]


def getRoomBaseInfo(room_id: int):
    """
    直播间的
    @param room_id:
    @return:
    "data": {
        "by_uids": {

        },
        "by_room_ids": {
            "25322725": {
                "room_id": 25322725,
                "uid": 143474500,
                "area_id": 192,
                "live_status": 0,
                "live_url": "https://live.bilibili.com/25322725",
                "parent_area_id": 5,
                "title": "obsのlua插件2测试",
                "parent_area_name": "电台",
                "area_name": "聊天电台",
                "live_time": "0000-00-00 00:00:00",
                "description": "个人简介测试",
                "tags": "我的个人标签测试",
                "attention": 35,
                "online": 0,
                "short_id": 0,
                "uname": "兰阳音",
                "cover": "http://i0.hdslb.com/bfs/live/new_room_cover/c17af2dbbbdfce33888e834bdb720edbf9515f95.jpg",
                "background": "",
                "join_slide": 1,
                "live_id": 0,
                "live_id_str": "0"
            }
        }
    }
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
    data = {
        'room_ids': room_id,
        'req_biz': "link-center"
    }
    RoomBaseInfo = requests.get(api, headers=headers, params=data).json()
    return RoomBaseInfo["data"]


def live_user_v1_Master_info(uid:int):
    """
    <h2 id="获取主播信息" tabindex="-1"><a class="header-anchor" href="#获取主播信息" aria-hidden="true">#</a> 获取主播信息</h2>
    <blockquote><p>https://api.live.bilibili.com/live_user/v1/Master/info</p></blockquote>
    <p><em>请求方式：GET</em></p>
    <p><strong>url参数：</strong></p>
    <table><thead><tr><th>参数名</th><th>类型</th><th>内容</th><th>必要性</th><th>备注</th></tr></thead><tbody><tr><td>uid</td><td>num</td><td>目标用户mid</td><td>必要</td><td></td></tr></tbody></table>
    <p><strong>json回复：</strong></p>
    <p>根对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>code</td><td>num</td><td>返回值</td><td>0：成功<br>1：参数错误</td></tr><tr><td>msg</td><td>str</td><td>错误信息</td><td>默认为空</td></tr><tr><td>message</td><td>str</td><td>错误信息</td><td>默认为空</td></tr><tr><td>data</td><td>obj</td><td>信息本体</td><td></td></tr></tbody></table>
    <p><code>data</code>对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>info</td><td>obj</td><td>主播信息</td><td></td></tr><tr><td>exp</td><td>obj</td><td>经验等级</td><td></td></tr><tr><td>follower_num</td><td>num</td><td>主播粉丝数</td><td></td></tr><tr><td>room_id</td><td>num</td><td>直播间id（短号）</td><td></td></tr><tr><td>medal_name</td><td>str</td><td>粉丝勋章名</td><td></td></tr><tr><td>glory_count</td><td>num</td><td>主播荣誉数</td><td></td></tr><tr><td>pendant</td><td>str</td><td>直播间头像框url</td><td></td></tr><tr><td>link_group_num</td><td>num</td><td>0</td><td><strong>作用尚不明确</strong></td></tr><tr><td>room_news</td><td>obj</td><td>主播公告</td><td></td></tr></tbody></table>
    <p><code>info</code>对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>uid</td><td>num</td><td>主播mid</td><td></td></tr><tr><td>uname</td><td>str</td><td>主播用户名</td><td></td></tr><tr><td>face</td><td>str</td><td>主播头像url</td><td></td></tr><tr><td>official_verify</td><td>obj</td><td>认证信息</td><td></td></tr><tr><td>gender</td><td>num</td><td>主播性别</td><td>-1：保密<br>0：女<br>1：男</td></tr></tbody></table>
    <p><code>info</code>中的<code>official_verify</code>对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>type</td><td>num</td><td>主播认证类型</td><td>-1：无<br>0：个人认证<br>1：机构认证</td></tr><tr><td>desc</td><td>str</td><td>主播认证信息</td><td></td></tr></tbody></table>
    <p><code>exp</code>对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>master_level</td><td>obj</td><td>主播等级</td><td></td></tr></tbody></table>
    <p><code>exp</code>中的<code>master_level</code>对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>level</td><td>num</td><td>当前等级</td><td></td></tr><tr><td>color</td><td>num</td><td>等级框颜色</td><td></td></tr><tr><td>current</td><td>array</td><td>当前等级信息</td><td></td></tr><tr><td>next</td><td>array</td><td>下一等级信息</td><td></td></tr></tbody></table>
    <p><code>master_level</code>中的<code>current</code>数组：</p>
    <table><thead><tr><th>项</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>0</td><td>num</td><td>升级积分</td><td></td></tr><tr><td>1</td><td>num</td><td>总积分</td><td></td></tr></tbody></table>
    <p><code>master_level</code>中的<code>next</code>数组：</p>
    <table><thead><tr><th>项</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>0</td><td>num</td><td>升级积分</td><td></td></tr><tr><td>1</td><td>num</td><td>总积分</td><td></td></tr></tbody></table>
    <p><code>room_news</code>对象：</p>
    <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>content</td><td>str</td><td>公告内容</td><td></td></tr><tr><td>ctime</td><td>str</td><td>公告时间</td><td></td></tr><tr><td>ctime_text</td><td>str</td><td>公告日期</td><td></td></tr></tbody></table>
    @param uid:目标用户mid
    @return:
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/live_user/v1/Master/info"
    data = {
        "uid": uid
    }
    live_user_v1_Master_info = requests.get(api, headers=headers, params=data).json()
    return live_user_v1_Master_info



def Area_getList():
    """
    获取直播分区
    @return:
    <table>
    <thead>
    <tr>
        <th>字段</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>code</td>
        <td>num</td>
        <td>返回值</td>
        <td>0：成功</td>
    </tr>
    <tr>
        <td>msg</td>
        <td>str</td>
        <td>错误信息</td>
        <td>默认为success</td>
    </tr>
    <tr>
        <td>message</td>
        <td>str</td>
        <td>错误信息</td>
        <td>默认为success</td>
    </tr>
    <tr>
        <td>data</td>
        <td>array</td>
        <td>父分区列表</td>
        <td></td>
    </tr>
    </tbody>
</table>
<p><code>data</code>数组：</p>
<table>
    <thead>
    <tr>
        <th>项</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>0</td>
        <td>obj</td>
        <td>父分区1</td>
        <td></td>
    </tr>
    <tr>
        <td>n</td>
        <td>obj</td>
        <td>父分区(n+1)</td>
        <td></td>
    </tr>
    <tr>
        <td>……</td>
        <td>obj</td>
        <td>……</td>
        <td>……</td>
    </tr>
    </tbody>
</table>
<p><code>data</code>数组中的对象：</p>
<table>
    <thead>
    <tr>
        <th>字段</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>num</td>
        <td>父分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>name</td>
        <td>name</td>
        <td>父分区名</td>
        <td></td>
    </tr>
    <tr>
        <td>list</td>
        <td>list</td>
        <td>子分区列表</td>
        <td></td>
    </tr>
    </tbody>
</table>
<p><code>data</code>数组中的对象中的<code>list</code>数组：</p>
<table>
    <thead>
    <tr>
        <th>项</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>0</td>
        <td>obj</td>
        <td>子分区1</td>
        <td></td>
    </tr>
    <tr>
        <td>n</td>
        <td>obj</td>
        <td>子分区(n+1)</td>
        <td></td>
    </tr>
    <tr>
        <td>……</td>
        <td>obj</td>
        <td>……</td>
        <td>……</td>
    </tr>
    </tbody>
</table>
<p><code>list</code>数组中的对象：</p>
<table>
    <thead>
    <tr>
        <th>字段</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>str</td>
        <td>子分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>parent_id</td>
        <td>str</td>
        <td>父分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>old_area_id</td>
        <td>str</td>
        <td>旧分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>name</td>
        <td>str</td>
        <td>子分区名</td>
        <td></td>
    </tr>
    <tr>
        <td>act_id</td>
        <td>str</td>
        <td>0</td>
        <td><strong>作用尚不明确</strong></td>
    </tr>
    <tr>
        <td>pk_status</td>
        <td>str</td>
        <td>？？？</td>
        <td><strong>作用尚不明确</strong></td>
    </tr>
    <tr>
        <td>hot_status</td>
        <td>num</td>
        <td>是否为热门分区</td>
        <td>0：否<br>1：是</td>
    </tr>
    <tr>
        <td>lock_status</td>
        <td>str</td>
        <td>0</td>
        <td><strong>作用尚不明确</strong></td>
    </tr>
    <tr>
        <td>pic</td>
        <td>str</td>
        <td>子分区标志图片url</td>
        <td></td>
    </tr>
    <tr>
        <td>parent_name</td>
        <td>str</td>
        <td>父分区名</td>
        <td></td>
    </tr>
    <tr>
        <td>area_type</td>
        <td>num</td>
        <td></td>
        <td></td>
    </tr>
    </tbody>
</table>

    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = "https://api.live.bilibili.com/room/v1/Area/getList"
    AreaList = requests.get(api, headers=headers).json()
    return AreaList["data"]


# end


# 登陆用函数
def generate() -> dict:
    """
    申请登录二维码
    @return: {'url': 二维码文本, 'qrcode_key': 扫描秘钥}
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
    url8qrcode_key = requests.get(api, headers=headers).json()
    # print(url8qrcode_key)
    data = url8qrcode_key['data']
    url = data['url']
    qrcode_key = data['qrcode_key']
    return {'url': url, 'qrcode_key': qrcode_key}


def poll(qrcode_key: str) -> dict[str, dict[str, str] | int]:
    """
    获取登陆状态，登陆成功获取 基础的 cookies
    @param qrcode_key: 扫描秘钥
    @return: {'code', 'cookies'}
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>code</td>
            <td>num</td>
            <td>0：扫码登录成功<br>86038：二维码已失效<br>86090：二维码已扫码未确认<br>86101：未扫码</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    @rtype: dict
    """
    global data
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    }
    api = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}'
    DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct = requests.get(api, data=qrcode_key, headers=headers).json()
    data = DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct['data']
    # print(data)
    cookies = {}
    code = data['code']
    if code == 0:
        def urldata_dict(url: str):
            """
            将 url参数 转换成 dict
            @param url: 带有参数的url
            @return: 转换成的dict
            @rtype: dict
            """
            urldata = url.split('?', 1)[1]
            data_list = urldata.split('&')
            data_dict = {}
            for data in data_list:
                data = data.split('=')
                data_dict[data[0]] = data[1]
            return data_dict

        data_dict = urldata_dict(data['url'])
        cookies["DedeUserID"] = data_dict['DedeUserID']
        cookies["DedeUserID__ckMd5"] = data_dict['DedeUserID__ckMd5']
        cookies["SESSDATA"] = data_dict['SESSDATA']
        cookies["bili_jct"] = data_dict['bili_jct']
        # 补充 cookie
        buvid3 = requests.get(f'https://www.bilibili.com/video/', headers=headers)
        cookies.update(buvid3.cookies.get_dict())
    return {'code': code, 'cookies': cookies}


# end


# 登陆后才能用的函数
class master:
    """登陆后才能用的函数"""
    def __init__(self, cookie: str):
        """
        完善 浏览器headers
        @param cookie: B站cookie
        """
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0")
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
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
            RankFans += FansMember
            # maxpage = math.ceil(num_FansMembersRank / 30) + 1
        return RankFans

    def dynamic_v1_feed_space(self, host_mid, all: bool = False) -> list:
        """

        @param host_mid:
        @param all:
        @return:
        <div><h1 id="获取动态列表" tabindex="-1"><a class="header-anchor" href="#获取动态列表" aria-hidden="true">#</a> 获取动态列表
        </h1>
            <blockquote><p>https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all</p></blockquote>
            <p>请求方式：<code>GET</code></p>
            <p>是否需要登录：<code>是</code></p>
            <h2 id="json回复" tabindex="-1"><a class="header-anchor" href="#json回复" aria-hidden="true">#</a> Json回复</h2>
            <h3 id="根对象" tabindex="-1"><a class="header-anchor" href="#根对象" aria-hidden="true">#</a> 根对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>code</td>
                    <td>num</td>
                    <td>响应码</td>
                    <td>0：成功<br>-101：账号未登录</td>
                </tr>
                <tr>
                    <td>message</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>ttl</td>
                    <td>num</td>
                    <td>1</td>
                    <td></td>
                </tr>
                <tr>
                    <td>data</td>
                    <td>obj</td>
                    <td>信息本体</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象" tabindex="-1"><a class="header-anchor" href="#data对象" aria-hidden="true">#</a> <code>data</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>has_more</td>
                    <td>bool</td>
                    <td>是否有更多数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>数据数组</td>
                    <td></td>
                </tr>
                <tr>
                    <td>offset</td>
                    <td>str</td>
                    <td>偏移量</td>
                    <td>等于<code>items</code>中最后一条记录的id<br>获取下一页时使用</td>
                </tr>
                <tr>
                    <td>update_baseline</td>
                    <td>str</td>
                    <td>更新基线</td>
                    <td>等于<code>items</code>中第一条记录的id</td>
                </tr>
                <tr>
                    <td>update_num</td>
                    <td>num</td>
                    <td>本次获取获取到了多少条新动态</td>
                    <td>在更新基线以上的动态条数</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象" tabindex="-1"><a class="header-anchor" href="#data对象-items数组中的对象"
                                                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>basic</td>
                    <td>obj</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>动态id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>modules</td>
                    <td>obj</td>
                    <td>动态信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>动态类型</td>
                    <td><a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%8A%A8%E6%80%81%E7%B1%BB%E5%9E%8B"
                           class="">动态类型</a></td>
                </tr>
                <tr>
                    <td>visible</td>
                    <td>bool</td>
                    <td>是否显示</td>
                    <td><code>true</code>：正常显示<br><code>false</code>：折叠动态</td>
                </tr>
                <tr>
                    <td>orig</td>
                    <td>obj</td>
                    <td>原动态信息</td>
                    <td>仅动态类型为<code>DYNAMIC_TYPE_FORWARD</code>的情况下存在</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-basic对象" tabindex="-1"><a class="header-anchor"
                                                                           href="#data对象-items数组中的对象-basic对象"
                                                                           aria-hidden="true">#</a> <code>data</code>对象 -&gt;
                <code>items</code>数组中的对象 -&gt; <code>basic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>comment_id_str</td>
                    <td>str</td>
                    <td></td>
                    <td><code>DYNAMIC_TYPE_AV</code>：视频AV号<br><code>DYNAMIC_TYPE_UGC_SEASON</code>：视频AV号<br><code>DYNAMIC_TYPE_PGC</code>：剧集分集AV号<br><code>DYNAMIC_TYPE_LIVE_RCMD</code>：动态本身id<br><code>DYNAMIC_TYPE_DRAW</code>：相簿id<br><code>DYNAMIC_TYPE_ARTICLE</code>：专栏cv号<br><code>DYNAMIC_TYPE_FORWARD</code>：动态本身id<br><code>DYNAMIC_TYPE_WORD</code>：动态本身id<br><code>DYNAMIC_TYPE_LIVE</code>:动态本身id<br><code>DYNAMIC_TYPE_MEDIALIST</code>:收藏夹ml号
                    </td>
                </tr>
                <tr>
                    <td>comment_type</td>
                    <td>num</td>
                    <td></td>
                    <td>1：<code>DYNAMIC_TYPE_AV</code> <code>DYNAMIC_TYPE_PGC</code> <code>DYNAMIC_TYPE_UGC_SEASON</code><br>11：<code>DYNAMIC_TYPE_DRAW</code><br>12：<code>DYNAMIC_TYPE_ARTICLE</code><br>17：<code>DYNAMIC_TYPE_LIVE_RCMD</code>
                        <code>DYNAMIC_TYPE_FORWARD</code> <code>DYNAMIC_TYPE_WORD</code> <code>DYNAMIC_TYPE_COMMON_SQUARE</code><br>19：<code>DYNAMIC_TYPE_MEDIALIST</code>
                    </td>
                </tr>
                <tr>
                    <td>like_icon</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>空串</code></td>
                </tr>
                <tr>
                    <td>rid_str</td>
                    <td>str</td>
                    <td></td>
                    <td><code>DYNAMIC_TYPE_AV</code>：视频AV号<br><code>DYNAMIC_TYPE_UGC_SEASON</code>：视频AV号 <code>DYNAMIC_TYPE_PGC</code>：剧集分集EP号<br><code>DYNAMIC_TYPE_DRAW</code>：相簿id<br><code>DYNAMIC_TYPE_ARTICLE</code>：专栏cv号<br><code>DYNAMIC_TYPE_LIVE_RCMD</code>：live_id<br><code>DYNAMIC_TYPE_FORWARD</code>：未知<br><code>DYNAMIC_TYPE_WORD</code>：未知<br><code>DYNAMIC_TYPE_COMMON_SQUARE</code>：未知<br><code>DYNAMIC_TYPE_LIVE</code>：直播间id<br><code>DYNAMIC_TYPE_MEDIALIST</code>：收藏夹ml号
                    </td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-basic对象-like-icon对象" tabindex="-1"><a class="header-anchor"
                                                                                         href="#data对象-items数组中的对象-basic对象-like-icon对象"
                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>basic</code>对象 -&gt;
                <code>like_icon</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>action_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>end_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>start_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象" tabindex="-1"><a class="header-anchor"
                                                                             href="#data对象-items数组中的对象-modules对象"
                                                                             aria-hidden="true">#</a> <code>data</code>对象 -&gt;
                <code>items</code>数组中的对象 -&gt; <code>modules</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>module_author</td>
                    <td>obj</td>
                    <td>UP主信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_dynamic</td>
                    <td>obj</td>
                    <td>动态内容信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_more</td>
                    <td>obj</td>
                    <td>动态右上角三点菜单</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_stat</td>
                    <td>obj</td>
                    <td>动态统计数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_interaction</td>
                    <td>obj</td>
                    <td>热度评论</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_fold</td>
                    <td>obj</td>
                    <td>动态折叠信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_dispute</td>
                    <td>obj</td>
                    <td>争议小黄条</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_tag</td>
                    <td>obj</td>
                    <td>置顶信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象" tabindex="-1"><a class="header-anchor"
                                                                                               href="#data对象-items数组中的对象-modules对象-module-author对象"
                                                                                               aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>face</td>
                    <td>str</td>
                    <td>头像</td>
                    <td></td>
                </tr>
                <tr>
                    <td>face_nft</td>
                    <td>bool</td>
                    <td>是否为NFT头像</td>
                    <td></td>
                </tr>
                <tr>
                    <td>following</td>
                    <td>bool</td>
                    <td>是否关注此UP主</td>
                    <td>自己的动态为<code>null</code></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转链接</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>名称前标签</td>
                    <td><code>合集</code><br><code>电视剧</code><br><code>番剧</code></td>
                </tr>
                <tr>
                    <td>mid</td>
                    <td>num</td>
                    <td>UP主UID<br>剧集SeasonId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>UP主名称<br>剧集名称<br>合集名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>official_verify</td>
                    <td>obj</td>
                    <td>UP主认证信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pendant</td>
                    <td>obj</td>
                    <td>UP主头像框</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pub_action</td>
                    <td>str</td>
                    <td>更新动作描述</td>
                    <td><code>投稿了视频</code><br><code>直播了</code><br><code>投稿了文章</code><br><code>更新了合集</code><br><code>与他人联合创作</code><br><code>发布了动态视频</code><br><code>投稿了直播回放</code>
                    </td>
                </tr>
                <tr>
                    <td>pub_location_text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>pub_time</td>
                    <td>str</td>
                    <td>更新时间</td>
                    <td><code>x分钟前</code><br><code>x小时前</code><br><code>昨天</code></td>
                </tr>
                <tr>
                    <td>pub_ts</td>
                    <td>num</td>
                    <td>更新时间戳</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>作者类型</td>
                    <td><a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E4%BD%9C%E8%80%85%E7%B1%BB%E5%9E%8B"
                           class="">作者类型</a></td>
                </tr>
                <tr>
                    <td>vip</td>
                    <td>obj</td>
                    <td>UP主大会员信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>decorate</td>
                    <td>obj</td>
                    <td>装扮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>nft_info</td>
                    <td>obj</td>
                    <td>NFT头像信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-official-verify对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-official-verify对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>official_verify</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>认证说明</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>认证类型</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-pendant对象" tabindex="-1"><a class="header-anchor"
                                                                                                           href="#data对象-items数组中的对象-modules对象-module-author对象-pendant对象"
                                                                                                           aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象
                -&gt; <code>pendant</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>expire</td>
                    <td>num</td>
                    <td>过期时间</td>
                    <td>此接口返回恒为<code>0</code></td>
                </tr>
                <tr>
                    <td>image</td>
                    <td>str</td>
                    <td>头像框图片url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>image_enhance</td>
                    <td>str</td>
                    <td>头像框图片url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>image_enhance_frame</td>
                    <td>str</td>
                    <td>头像框图片逐帧序列url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>头像框名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pid</td>
                    <td>num</td>
                    <td>头像框id</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-vip对象" tabindex="-1"><a class="header-anchor"
                                                                                                       href="#data对象-items数组中的对象-modules对象-module-author对象-vip对象"
                                                                                                       aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象
                -&gt; <code>vip</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>avatar_subscript</td>
                    <td>num</td>
                    <td>是否显示角标</td>
                    <td>0：不显示<br>1：显示</td>
                </tr>
                <tr>
                    <td>avatar_subscript_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>due_date</td>
                    <td>num</td>
                    <td>大会员过期时间戳</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>obj</td>
                    <td>大会员标签</td>
                    <td></td>
                </tr>
                <tr>
                    <td>nickname_color</td>
                    <td>str</td>
                    <td>名字显示颜色</td>
                    <td>大会员：<code>#FB7299</code></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td>大会员状态</td>
                    <td>0：无<br>1：有<br>2：？</td>
                </tr>
                <tr>
                    <td>theme_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>大会员类型</td>
                    <td>0：无<br>1：月大会员<br>2：年度及以上大会员</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-vip对象-label对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-vip对象-label对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>vip</code>对象 -&gt;
                <code>label</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>会员标签背景颜色</td>
                    <td><code>#FB7299</code></td>
                </tr>
                <tr>
                    <td>bg_style</td>
                    <td>num</td>
                    <td><code>0</code> <code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>border_color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>img_label_uri_hans</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>动态版 简体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hans_static</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>静态版 简体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hant</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>动态版 繁体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hant_static</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>静态版 繁体版</td>
                </tr>
                <tr>
                    <td>label_theme</td>
                    <td>str</td>
                    <td>会员标签</td>
                    <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员<br>fools_day_hundred_annual_vip：最强绿鲤鱼
                    </td>
                </tr>
                <tr>
                    <td>path</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>会员类型文案</td>
                    <td><code>大会员</code> <code>年度大会员</code> <code>十年大会员</code> <code>百年大会员</code>
                        <code>最强绿鲤鱼</code></td>
                </tr>
                <tr>
                    <td>text_color</td>
                    <td>str</td>
                    <td>用户名文字颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>use_img_label</td>
                    <td>bool</td>
                    <td><code>true</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-decorate对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-decorate对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>decorate</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>card_url</td>
                    <td>str</td>
                    <td>动态卡片小图标图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>fan</td>
                    <td>obj</td>
                    <td>粉丝装扮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>装扮ID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>装扮名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-decorate对象-fan对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-decorate对象-fan对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>decorate</code>对象 -&gt;
                <code>fan</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>编号颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>is_fan</td>
                    <td>bool</td>
                    <td>是否是粉丝装扮</td>
                    <td></td>
                </tr>
                <tr>
                    <td>num_str</td>
                    <td>str</td>
                    <td>装扮编号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>number</td>
                    <td>num</td>
                    <td>装扮编号</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-nft-info对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-nft-info对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>nft_info</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>region_icon</td>
                    <td>str</td>
                    <td>NFT头像角标URL</td>
                    <td>
                        类型1：https://i0.hdslb.com/bfs/activity-plat/static/20220506/334553dd7c506a92b88eaf4d59ac8b4d/j8AeXAkEul.gif
                        <br>类型2：https://i0.hdslb.com/bfs/activity-plat/static/20220506/334553dd7c506a92b88eaf4d59ac8b4d/IOHoVs1ebP.gif
                    </td>
                </tr>
                <tr>
                    <td>region_type</td>
                    <td>num</td>
                    <td>NFT头像角标类型</td>
                    <td>1,2</td>
                </tr>
                <tr>
                    <td>show_status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象" tabindex="-1"><a class="header-anchor"
                                                                                                href="#data对象-items数组中的对象-modules对象-module-dynamic对象"
                                                                                                aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>additional</td>
                    <td>obj</td>
                    <td>相关内容卡片信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>obj</td>
                    <td>动态文字内容</td>
                    <td>其他动态时为null</td>
                </tr>
                <tr>
                    <td>major</td>
                    <td>obj</td>
                    <td>动态主体对象</td>
                    <td>转发动态时为null</td>
                </tr>
                <tr>
                    <td>topic</td>
                    <td>obj</td>
                    <td>话题信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>common</td>
                    <td>obj</td>
                    <td>一般类型</td>
                    <td><code>ADDITIONAL_TYPE_COMMON</code>类型独有</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>卡片类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E7%9B%B8%E5%85%B3%E5%86%85%E5%AE%B9%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B"
                           class="">相关内容卡片类型</a></td>
                </tr>
                <tr>
                    <td>reserve</td>
                    <td>obj</td>
                    <td>预约信息</td>
                    <td><code>ADDITIONAL_TYPE_RESERVE</code>类型独有</td>
                </tr>
                <tr>
                    <td>goods</td>
                    <td>obj</td>
                    <td>商品内容</td>
                    <td><code>ADDITIONAL_TYPE_GOODS</code>类型独有</td>
                </tr>
                <tr>
                    <td>vote</td>
                    <td>obj</td>
                    <td>投票信息</td>
                    <td><code>ADDITIONAL_TYPE_VOTE</code>类型独有</td>
                </tr>
                <tr>
                    <td>ugc</td>
                    <td>obj</td>
                    <td>视频信息</td>
                    <td><code>ADDITIONAL_TYPE_UGC</code>类型独有</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>button</td>
                    <td>obj</td>
                    <td>按钮内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>左侧封面图</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc1</td>
                    <td>str</td>
                    <td>描述1</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc2</td>
                    <td>str</td>
                    <td>描述2</td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td>卡片头文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>相关id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_type</td>
                    <td>str</td>
                    <td>子类型</td>
                    <td><code>game</code><br><code>decoration</code><br><code>ogv</code></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>卡片标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_style</td>
                    <td>obj</td>
                    <td>跳转类型</td>
                    <td><code>game</code>和<code>decoration</code>类型特有</td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td></td>
                    <td>1：<code>game</code>和<code>decoration</code>类型<br>2：<code>ogv</code>类型</td>
                </tr>
                <tr>
                    <td>check</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>ogv</code>类型特有</td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>uncheck</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>ogv</code>类型特有</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-jump-style对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-jump-style对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>jump_style</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td>game：<code>进入</code><br>decoration：<code>去看看</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-check对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-check对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>check</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>按钮图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>ogv</code>：已追剧</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-uncheck对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-uncheck对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>uncheck</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>按钮图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>ogv</code>：追剧</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>button</td>
                    <td>obj</td>
                    <td>按钮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc1</td>
                    <td>obj</td>
                    <td>预约时间</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc2</td>
                    <td>obj</td>
                    <td>预约观看量</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>reserve_total</td>
                    <td>num</td>
                    <td>预约人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>num</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>state</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>stype</td>
                    <td>num</td>
                    <td><code>1</code> <code>2</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>预约标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>up_mid</td>
                    <td>num</td>
                    <td>预约发起人UID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc3</td>
                    <td>obj</td>
                    <td>预约有奖信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>check</td>
                    <td>obj</td>
                    <td>已预约状态显示内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td>预约状态</td>
                    <td>1：未预约，使用<code>uncheck</code><br>2：已预约，使用<code>check</code></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>1：视频预约，使用<code>jump_style</code><br>2：直播预约，使用<code>check</code>和<code>uncheck</code></td>
                </tr>
                <tr>
                    <td>uncheck</td>
                    <td>obj</td>
                    <td>未预约状态显示内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_style</td>
                    <td>obj</td>
                    <td>跳转按钮</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-check对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-check对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>check</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>已预约</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-uncheck对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-uncheck对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>uncheck</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>显示图标URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>toast</td>
                    <td>str</td>
                    <td>预约成功显示提示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable</td>
                    <td>num</td>
                    <td>是否不可预约</td>
                    <td>1：是</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-jump-style对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-jump-style对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>jump_style</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>去观看</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc1对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc1对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc1</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>0：<code>视频预约</code> <code>11-05 20:00 直播</code> <code>预计今天
                        17:05发布</code><br>1：<code>直播中</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc2对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc2对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc2</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td><code>2人预约</code><br><code>743观看</code><br><code>1.0万人看过</code><br><code>2151人气</code></td>
                </tr>
                <tr>
                    <td>visible</td>
                    <td>bool</td>
                    <td>是否显示</td>
                    <td>true：显示文案<br>false：显示已结束</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc3对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc3对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc3</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>开奖信息跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>奖品信息显示文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>goods</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>head_icon</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td>卡片头显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>商品信息列表</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象-items数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象-items数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>goods</code>对象
                -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>brief</td>
                    <td>str</td>
                    <td>商品副标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>商品封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>str</td>
                    <td>商品ID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_desc</td>
                    <td>str</td>
                    <td>跳转按钮显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>商品名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>price</td>
                    <td>str</td>
                    <td>商品价格</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-vote对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-vote对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>vote</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>choice_cnt</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>default_share</td>
                    <td>num</td>
                    <td>是否默认勾选<code>同时分享至动态</code></td>
                    <td>1：勾选</td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>投票标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>end_time</td>
                    <td>num</td>
                    <td>剩余时间</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>join_num</td>
                    <td>num</td>
                    <td>已参与人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>null</td>
                    <td><code>null</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>uid</td>
                    <td>num</td>
                    <td>发起人UID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>vote_id</td>
                    <td>num</td>
                    <td>投票ID</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-ugc对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-ugc对象" aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>additional</code>对象 -&gt; <code>ugc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_second</td>
                    <td>str</td>
                    <td>播放量与弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration</td>
                    <td>str</td>
                    <td>视频长度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>视频跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>multi_line</td>
                    <td>bool</td>
                    <td><code>true</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>desc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>动态的文字内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>orig_text</td>
                    <td>str</td>
                    <td>原始文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>替换后的文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>节点类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>emoji</td>
                    <td>obj</td>
                    <td>表情信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>str</td>
                    <td>关联id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>goods</td>
                    <td>obj</td>
                    <td>商品信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>icon_name</td>
                    <td>str</td>
                    <td>图标名称</td>
                    <td><code>taobao</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
                -&gt; <code>emoji</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>表情图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>表情尺寸</td>
                    <td><code>1</code> <code>2</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>表情的文字代码</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>表情类型</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-goods对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-goods对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
                -&gt; <code>goods</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象" tabindex="-1"><a class="header-anchor"
                                                                                                          href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象"
                                                                                                          aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>major</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>动态主体类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%8A%A8%E6%80%81%E4%B8%BB%E4%BD%93%E7%B1%BB%E5%9E%8B"
                           class="">动态主体类型</a></td>
                </tr>
                <tr>
                    <td>ugc_season</td>
                    <td>obj</td>
                    <td>合集信息</td>
                    <td><code>MAJOR_TYPE_UGC_SEASON</code></td>
                </tr>
                <tr>
                    <td>article</td>
                    <td>obj</td>
                    <td>专栏类型</td>
                    <td><code>MAJOR_TYPE_ARTICLE</code></td>
                </tr>
                <tr>
                    <td>draw</td>
                    <td>obj</td>
                    <td>带图动态</td>
                    <td><code>MAJOR_TYPE_DRAW</code></td>
                </tr>
                <tr>
                    <td>archive</td>
                    <td>obj</td>
                    <td>视频信息</td>
                    <td><code>MAJOR_TYPE_ARCHIVE</code></td>
                </tr>
                <tr>
                    <td>live_rcmd</td>
                    <td>obj</td>
                    <td>直播状态</td>
                    <td><code>MAJOR_TYPE_LIVE_RCMD</code></td>
                </tr>
                <tr>
                    <td>common</td>
                    <td>obj</td>
                    <td>一般类型</td>
                    <td><code>MAJOR_TYPE_COMMON</code></td>
                </tr>
                <tr>
                    <td>pgc</td>
                    <td>obj</td>
                    <td>剧集信息</td>
                    <td><code>MAJOR_TYPE_PGC</code></td>
                </tr>
                <tr>
                    <td>courses</td>
                    <td>obj</td>
                    <td>课程信息</td>
                    <td><code>MAJOR_TYPE_COURSES</code></td>
                </tr>
                <tr>
                    <td>music</td>
                    <td>obj</td>
                    <td>音频信息</td>
                    <td><code>MAJOR_TYPE_MUSIC</code></td>
                </tr>
                <tr>
                    <td>opus</td>
                    <td>obj</td>
                    <td>图文动态</td>
                    <td><code>MAJOR_TYPE_OPUS</code></td>
                </tr>
                <tr>
                    <td>live</td>
                    <td>obj</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>none</td>
                    <td>obj</td>
                    <td>动态失效</td>
                    <td><code>MAJOR_TYPE_NONE</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>aid</td>
                    <td>num</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>视频简介</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable_preview</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration_text</td>
                    <td>str</td>
                    <td>时长</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-badge对象" tabindex="-1">
                <a class="header-anchor"
                   href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-badge对象"
                   aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
                -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-stat对象" tabindex="-1">
                <a class="header-anchor"
                   href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-stat对象"
                   aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
                -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-article对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-article对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>article</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>covers</td>
                    <td>array</td>
                    <td>封面图数组</td>
                    <td>最多三张</td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>文章摘要</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>文章CV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>文章跳转地址</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>文章阅读量</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>文章标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>draw</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>对应相簿id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>图片信息列表</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象-items数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象-items数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>draw</code>对象 -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>height</td>
                    <td>num</td>
                    <td>图片高度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>图片大小</td>
                    <td>单位KB</td>
                </tr>
                <tr>
                    <td>src</td>
                    <td>str</td>
                    <td>图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>tags</td>
                    <td>array</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>width</td>
                    <td>num</td>
                    <td>图片宽度</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>aid</td>
                    <td>str</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>bvid</td>
                    <td>str</td>
                    <td>视频BVID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>视频简介</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable_preview</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration_text</td>
                    <td>str</td>
                    <td>视频长度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-stat对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-stat对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象 -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live-rcmd对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live-rcmd对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>live_rcmd</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>content</td>
                    <td>str</td>
                    <td>直播间内容JSON</td>
                    <td></td>
                </tr>
                <tr>
                    <td>reserve_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>common</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>biz_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>左侧图片封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>右侧描述信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转地址</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>sketch_id</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>右侧标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>common</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>epid</td>
                    <td>num</td>
                    <td>分集EpId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>season_id</td>
                    <td>num</td>
                    <td>剧集SeasonId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_type</td>
                    <td>num</td>
                    <td>剧集类型</td>
                    <td>1：番剧<br>2：电影<br>3：纪录片<br>4：国创<br>5：电视剧<br>6：漫画<br>7：综艺</td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>2</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-stat对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-stat对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象 -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>courses</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>封面图URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>更新状态描述</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>课程id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_title</td>
                    <td>str</td>
                    <td>课程副标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>课程标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>courses</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-music对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-music对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>music</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>音频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>音频AUID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>音频分类</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>音频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>opus</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>fold_action</td>
                    <td>array</td>
                    <td>展开收起</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pics</td>
                    <td>array</td>
                    <td>图片信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>summary</td>
                    <td>obj</td>
                    <td>动态内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>动态标题</td>
                    <td>没有标题时为null</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象-summary对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象-summary对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>opus</code>对象 -&gt; <code>summary</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>和<code>desc</code>对象中的<code>rich_text_nodes</code>数组结构一样</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>评论内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>live</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>直播封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_first</td>
                    <td>str</td>
                    <td>直播主分区名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_second</td>
                    <td>str</td>
                    <td>观看人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>直播间id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>直播间跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>live_state</td>
                    <td>num</td>
                    <td>直播状态</td>
                    <td>0：直播结束<br>1：正在直播</td>
                </tr>
                <tr>
                    <td>reserve_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>直播间标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>live</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-none对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-none对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>none</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>tips</td>
                    <td>str</td>
                    <td>动态失效显示文案</td>
                    <td>deprecated?</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-topic对象" tabindex="-1"><a class="header-anchor"
                                                                                                          href="#data对象-items数组中的对象-modules对象-module-dynamic对象-topic对象"
                                                                                                          aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>topic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>话题id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>话题名称</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-more对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_more</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>three_point_items</td>
                    <td>array</td>
                    <td>右上角三点菜单</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>显示文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>类型</td>
                    <td></td>
                </tr>
                <tr>
                    <td>modal</td>
                    <td>obj</td>
                    <td>弹出框信息</td>
                    <td>删除动态时弹出</td>
                </tr>
                <tr>
                    <td>params</td>
                    <td>obj</td>
                    <td>参数</td>
                    <td>置顶/取消置顶时使用</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-modal对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-modal对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象 -&gt;
                <code>modal</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cancel</td>
                    <td>str</td>
                    <td>取消按钮</td>
                    <td><code>我点错了</code></td>
                </tr>
                <tr>
                    <td>confirm</td>
                    <td>str</td>
                    <td>确认按钮</td>
                    <td><code>删除</code></td>
                </tr>
                <tr>
                    <td>content</td>
                    <td>str</td>
                    <td>提示内容</td>
                    <td><code>确定要删除此条动态吗？</code></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>标题</td>
                    <td><code>删除动态</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-params对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-params对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象 -&gt;
                <code>params</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>dynamic_id</td>
                    <td>str</td>
                    <td>当前动态ID</td>
                    <td>deprecated?</td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>bool</td>
                    <td>当前动态是否处于置顶状态</td>
                    <td>deprecated?</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-stat对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>comment</td>
                    <td>obj</td>
                    <td>评论数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forward</td>
                    <td>obj</td>
                    <td>转发数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>like</td>
                    <td>obj</td>
                    <td>点赞数据</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-comment对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-stat对象-comment对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>comment</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>评论数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>hidden</td>
                    <td>bool</td>
                    <td>是否隐藏</td>
                    <td>直播类型动态会隐藏回复功能</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-forward对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-stat对象-forward对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>forward</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>转发数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-like对象" tabindex="-1"><a class="header-anchor"
                                                                                                      href="#data对象-items数组中的对象-modules对象-module-stat对象-like对象"
                                                                                                      aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>like</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>点赞数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>bool</td>
                    <td>当前用户是否点赞</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象" tabindex="-1"><a class="header-anchor"
                                                                                                    href="#data对象-items数组中的对象-modules对象-module-interaction对象"
                                                                                                    aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_interaction</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>信息列表</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>obj</td>
                    <td>点赞/评论信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>0：点赞信息<br>1：评论信息</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>评论内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>orig_text</td>
                    <td>str</td>
                    <td>原始文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>str</td>
                    <td>关联ID</td>
                    <td>用户UID</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>替换后文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>富文本节点类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>emoji</td>
                    <td>obj</td>
                    <td>表情信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象 -&gt; <code>emoji</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>表情图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>表情尺寸</td>
                    <td><code>1</code> <code>2</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>表情的文字代码</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>表情类型</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-fold对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-fold对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_fold</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>ids</td>
                    <td>array</td>
                    <td>被折叠的动态id列表</td>
                    <td></td>
                </tr>
                <tr>
                    <td>statement</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td>例：展开x条相关动态</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>users</td>
                    <td>array</td>
                    <td><code>空数组</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dispute对象" tabindex="-1"><a class="header-anchor"
                                                                                                href="#data对象-items数组中的对象-modules对象-module-dispute对象"
                                                                                                aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dispute</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>提醒文案</td>
                    <td>例：视频内含有危险行为，请勿模仿</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-tag对象" tabindex="-1"><a class="header-anchor"
                                                                                            href="#data对象-items数组中的对象-modules对象-module-tag对象"
                                                                                            aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt;
                <code>module_tag</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>'置顶'</td>
                    <td>置顶动态出现这个对象，否则没有</td>
                </tr>
                </tbody>
            </table>
        </div>

        """
        api = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
        headers = self.headers
        data = {
            "offset": "",
            "host_mid": host_mid
        }
        dynamic = requests.get(api, headers=headers, params=data).json()
        if not all:
            dynamics = dynamic["data"]["items"]
        else:
            dynamics = dynamic["data"]["items"]
            while dynamic["data"]["has_more"]:
                data["offset"] = dynamic["data"]["offset"]
                dynamic = requests.get(api, headers=headers, params=data).json()
                for i in dynamic["data"]["items"]:
                    if i not in dynamics:
                        dynamics.append(i)
        dynamic = dynamics
        return dynamic

    def get_user_info(self) -> dict:
        """
        获得个人基础信息
        """
        url = "https://api.live.bilibili.com/xlive/web-ucenter/user/get_user_info"
        headers = self.headers
        response = requests.get(url, headers=headers).json()
        return response['data']

    def interface_nav(self):
        """
        获取登录后导航栏用户信息
        @return:
        <p><code>data</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>isLogin</td>
                <td>bool</td>
                <td>是否已登录</td>
                <td>false：未登录<br>true：已登录</td>
            </tr>
            <tr>
                <td>email_verified</td>
                <td>num</td>
                <td>是否验证邮箱地址</td>
                <td>0：未验证<br>1：已验证</td>
            </tr>
            <tr>
                <td>face</td>
                <td>str</td>
                <td>用户头像 url</td>
                <td></td>
            </tr>
            <tr>
                <td>level_info</td>
                <td>obj</td>
                <td>等级信息</td>
                <td></td>
            </tr>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>用户 mid</td>
                <td></td>
            </tr>
            <tr>
                <td>mobile_verified</td>
                <td>num</td>
                <td>是否验证手机号</td>
                <td>0：未验证<br>1：已验证</td>
            </tr>
            <tr>
                <td>money</td>
                <td>num</td>
                <td>拥有硬币数</td>
                <td></td>
            </tr>
            <tr>
                <td>moral</td>
                <td>num</td>
                <td>当前节操值</td>
                <td>上限为70</td>
            </tr>
            <tr>
                <td>official</td>
                <td>obj</td>
                <td>认证信息</td>
                <td></td>
            </tr>
            <tr>
                <td>officialVerify</td>
                <td>obj</td>
                <td>认证信息 2</td>
                <td></td>
            </tr>
            <tr>
                <td>pendant</td>
                <td>obj</td>
                <td>头像框信息</td>
                <td></td>
            </tr>
            <tr>
                <td>scores</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>uname</td>
                <td>str</td>
                <td>用户昵称</td>
                <td></td>
            </tr>
            <tr>
                <td>vipDueDate</td>
                <td>num</td>
                <td>会员到期时间</td>
                <td>毫秒 时间戳</td>
            </tr>
            <tr>
                <td>vipStatus</td>
                <td>num</td>
                <td>会员开通状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>vipType</td>
                <td>num</td>
                <td>会员类型</td>
                <td>0：无<br>1：月度大会员<br>2：年度及以上大会员</td>
            </tr>
            <tr>
                <td>vip_pay_type</td>
                <td>num</td>
                <td>会员开通状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>vip_theme_type</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>vip_label</td>
                <td>obj</td>
                <td>会员标签</td>
                <td></td>
            </tr>
            <tr>
                <td>vip_avatar_subscript</td>
                <td>num</td>
                <td>是否显示会员图标</td>
                <td>0：不显示<br>1：显示</td>
            </tr>
            <tr>
                <td>vip_nickname_color</td>
                <td>str</td>
                <td>会员昵称颜色</td>
                <td>颜色码</td>
            </tr>
            <tr>
                <td>wallet</td>
                <td>obj</td>
                <td>B币钱包信息</td>
                <td></td>
            </tr>
            <tr>
                <td>has_shop</td>
                <td>bool</td>
                <td>是否拥有推广商品</td>
                <td>false：无<br>true：有</td>
            </tr>
            <tr>
                <td>shop_url</td>
                <td>str</td>
                <td>商品推广页面 url</td>
                <td></td>
            </tr>
            <tr>
                <td>allowance_count</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>answer_status</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>is_senior_member</td>
                <td>num</td>
                <td>是否硬核会员</td>
                <td>0：非硬核会员<br>1：硬核会员</td>
            </tr>
            <tr>
                <td>wbi_img</td>
                <td>obj</td>
                <td>Wbi 签名实时口令</td>
                <td>该字段即使用户未登录也存在</td>
            </tr>
            <tr>
                <td>is_jury</td>
                <td>bool</td>
                <td>是否风纪委员</td>
                <td>true：风纪委员<br>false：非风纪委员</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>level_info</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>current_level</td>
                <td>num</td>
                <td>当前等级</td>
                <td></td>
            </tr>
            <tr>
                <td>current_min</td>
                <td>num</td>
                <td>当前等级经验最低值</td>
                <td></td>
            </tr>
            <tr>
                <td>current_exp</td>
                <td>num</td>
                <td>当前经验</td>
                <td></td>
            </tr>
            <tr>
                <td>next_exp</td>
                <td>小于6级时：num<br>6级时：str</td>
                <td>升级下一等级需达到的经验</td>
                <td>当用户等级为Lv6时，值为<code>--</code>，代表无穷大</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>role</td>
                <td>num</td>
                <td>认证类型</td>
                <td>见<a href="/bilibili-API-collect/docs/user/official_role.html" class="">用户认证类型一览</a></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证备注</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：认证</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official_verify</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：认证</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>pendant</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>pid</td>
                <td>num</td>
                <td>挂件id</td>
                <td></td>
            </tr>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>挂件名称</td>
                <td></td>
            </tr>
            <tr>
                <td>image</td>
                <td>str</td>
                <td>挂件图片url</td>
                <td></td>
            </tr>
            <tr>
                <td>expire</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>vip_label</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>path</td>
                <td>str</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>text</td>
                <td>str</td>
                <td>会员名称</td>
                <td></td>
            </tr>
            <tr>
                <td>label_theme</td>
                <td>str</td>
                <td>会员标签</td>
                <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>wallet</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>登录用户mid</td>
                <td></td>
            </tr>
            <tr>
                <td>bcoin_balance</td>
                <td>num</td>
                <td>拥有B币数</td>
                <td></td>
            </tr>
            <tr>
                <td>coupon_balance</td>
                <td>num</td>
                <td>每月奖励B币数</td>
                <td></td>
            </tr>
            <tr>
                <td>coupon_due_time</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>wbi_img</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>img_url</td>
                <td>str</td>
                <td>Wbi 签名参数 <code>imgKey</code>的伪装 url</td>
                <td>详见文档 <a href="/bilibili-API-collect/docs/misc/sign/wbi.html" class="">Wbi 签名</a></td>
            </tr>
            <tr>
                <td>sub_url</td>
                <td>str</td>
                <td>Wbi 签名参数 <code>subKey</code>的伪装 url</td>
                <td>详见文档 <a href="/bilibili-API-collect/docs/misc/sign/wbi.html" class="">Wbi 签名</a></td>
            </tr>
            </tbody>
        </table>

        """
        api = "https://api.bilibili.com/x/web-interface/nav"
        headers = self.headers
        nav = requests.get(api, headers=headers).json()
        return nav["data"]

    def getRoomHighlightState(self):
        """
        获取直播间号
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/highlight/getRoomHighlightState"
        headers = self.headers
        room_id = requests.get(api, headers=headers).json()["data"]["room_id"]
        return room_id

    def GetEmoticons(self, roomid: int):
        """
        获取表情
        @return:
        @rtype: list
        """
        api = "https://api.live.bilibili.com/xlive/web-ucenter/v2/emoticon/GetEmoticons"
        headers = self.headers
        params = {
            "platform": "pc",
            "room_id": roomid
        }
        Emoticons = requests.get(api, headers=headers, params=params).json()["data"]["data"]
        return Emoticons

    def getDanmuInfo(self, roomid: int) -> dict:
        """
        获取信息流认证秘钥
        @param roomid: 直播间真实id
        @return:
        <p>根对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>code</td><td>num</td><td>返回值</td><td>0：成功<br>65530：token错误（登录错误）<br>1：错误<br>60009：分区不存在<br><strong>（其他错误码有待补充）</strong></td></tr><tr><td>message</td><td>str</td><td>错误信息</td><td>默认为空</td></tr><tr><td>ttl</td><td>num</td><td>1</td><td></td></tr><tr><td>data</td><td>obj</td><td>信息本体</td><td></td></tr></tbody></table>
        <p><code>data</code>对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>group</td><td>str</td><td>live</td><td></td></tr><tr><td>business_id</td><td>num</td><td>0</td><td></td></tr><tr><td>refresh_row_factor</td><td>num</td><td>0.125</td><td></td></tr><tr><td>refresh_rate</td><td>num</td><td>100</td><td></td></tr><tr><td>max_delay</td><td>num</td><td>5000</td><td></td></tr><tr><td>token</td><td>str</td><td>认证秘钥</td><td></td></tr><tr><td>host_list</td><td>array</td><td>信息流服务器节点列表</td><td></td></tr></tbody></table>
        <p><code>host_list</code>数组中的对象：</p>
        <table><thead><tr><th>字段</th><th>类型</th><th>内容</th><th>备注</th></tr></thead><tbody><tr><td>host</td><td>str</td><td>服务器域名</td><td></td></tr><tr><td>port</td><td>num</td><td>tcp端口</td><td></td></tr><tr><td>wss_port</td><td>num</td><td>wss端口</td><td></td></tr><tr><td>ws_port</td><td>num</td><td>ws端口</td><td></td></tr></tbody></table>
        """
        headers = self.headers
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo?id={roomid}'
        response = requests.get(url, headers=headers).json()
        return response

    def getRoomNews(self):
        # 获取直播公告
        headers = self.headers
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getRoomNews"
        params = {
            'room_id': self.getRoomHighlightState(),
            'uid': cookie2dict(self.headers["cookie"])["DedeUserID"]
        }
        getRoomNews_ReturnValue = requests.get(api, headers=headers, params=params).json()
        return getRoomNews_ReturnValue["data"]["content"]


class CsrfAuthenticationL:
    """Csrf鉴权"""
    def __init__(self, cookie: str):
        """
        需要Csrf
        :param cookie:
        :param UA:
        :type UA: str
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

    def AnchorChangeRoomArea(self, area_id: int):
        """
        更改直播分区
        @param area_id:二级分区id
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v2/room/AnchorChangeRoomArea"
        headers = self.headers
        csrf = self.csrf
        data = {
            "platform": "pc",
            "room_id": master(self.cookie).getRoomHighlightState(),
            "area_id": area_id,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        changeroomarea_ReturnValue = requests.post(api, headers=headers, params=data).json()
        return changeroomarea_ReturnValue

    def startLive(self, area_id: int):
        """
        开始直播
        @param area_id: 二级分区id
        @return:
        """
        api = "https://api.live.bilibili.com/room/v1/Room/startLive"
        headers = self.headers
        csrf = self.csrf
        data = {
            "platform": "web_link",
            "room_id": master(self.cookie).getRoomHighlightState(),
            "area_v2": area_id,
            "backup_stream": 0,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        startLive_ReturnValue = requests.post(api, headers=headers, params=data).json()
        return startLive_ReturnValue

    def stopLive(self):
        """
        结束直播
        @return:
        """
        api = "https://api.live.bilibili.com/room/v1/Room/stopLive"
        headers = self.headers
        csrf = self.csrf
        data = {
            "platform": "pc",
            "room_id": master(self.cookie).getRoomHighlightState(),
            "csrf": csrf,
            "csrf_token": csrf,
        }
        stopLive_ReturnValue = requests.post(api, headers=headers, params=data).json()
        return stopLive_ReturnValue

    def FetchWebUpStreamAddr(self, reset_key: bool = False):
        """
        推流信息
        @param reset_key: 布尔值，是否更新
        @return:
        """
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/live/FetchWebUpStreamAddr"
        headers = self.headers
        csrf = self.csrf
        data = {
            "platform": "pc",
            "backup_stream": 0,
            "reset_key": reset_key,
            "csrf": csrf,
            "csrf_token": csrf,
        }
        FetchWebUpStreamAddre_ReturnValue = requests.post(api, headers=headers, params=data).json()
        return FetchWebUpStreamAddre_ReturnValue

    def send(self, roomid: int, msg: str):
        api = "https://api.live.bilibili.com/msg/send"
        headers = self.headers
        csrf = self.csrf
        data = {
            'msg': msg,
            'color': 16777215,
            'fontsize': 25,
            'rnd': str(time.time())[:8],
            'roomid': roomid,
            'csrf': csrf,
            'csrf_token': csrf
        }
        send_ReturnValue = requests.post(api, headers=headers, params=data).json()
        return send_ReturnValue

    def room_v1_Room_update(self, title:str):
        """
        更新直播标题
        @return:
        """
        headers = self.headers
        csrf = self.csrf
        api = "https://api.live.bilibili.com/room/v1/Room/update"
        data = {
            'room_id': master(self.cookie).getRoomHighlightState(),
            'title': title,
            'csrf_token': csrf,
            'csrf': csrf
        }
        room_v1_Room_update_ReturnValue = requests.post(api, headers=headers, data=data).json()
        return room_v1_Room_update_ReturnValue

    def updateRoomNews(self, content: str):
        """
        更新直播公告
        @return:
        """
        headers = self.headers
        csrf = self.csrf
        api = "https://api.live.bilibili.com/xlive/app-blink/v1/index/updateRoomNews"
        data = {
            'room_id': master(self.cookie).getRoomHighlightState(),
            'uid': self.cookies["DedeUserID"],
            'content': content,
            'csrf_token': csrf,
            'csrf': csrf
        }
        updateRoomNews_ReturnValue = requests.post(api, headers=headers, data=data).json()
        return updateRoomNews_ReturnValue


# end


# 整合类函数
def start_login(uid: int = 0, dirname: str = "Biliconfig"):
    """
    扫码登陆获得cookies
    :param uid: 登陆的账号的uid，为0时使用记录中默认的，会使用上一次正常登陆的账号作为默认
    :param dirname: 文件保存目录
    :return: {'uid': int(cookies['DedeUserID']), 'cookies': cookies, 'cookie': dict2cookieformat(cookies)}
    :rtype:dict
    """
    global code
    # 获取uid对应的cookies
    configb = config_B(uid=uid, dirname=dirname)
    cookies = configb.check()
    # 尝试使用存录的cookies登录
    islogin = master(dict2cookieformat(cookies)).interface_nav()["isLogin"]
    if islogin:
        # 记录到默认登录字段
        configb = config_B(uid=0, dirname=dirname)
        configb.update(cookies)
        return {'uid': int(cookies['DedeUserID']), 'cookies': cookies, 'cookie': dict2cookieformat(cookies)}
    else:  # cookies无法登录或者没有记录所填的uid
        # 申请登录二维码
        url8qrcode_key = generate()
        url = url8qrcode_key['url']
        # 获取二维码
        qr = qr_encode(url)
        # 输出二维码图形字符串
        obs.script_log(obs.LOG_WARNING, qr["str"])
        # 获取二维码key
        qrcode_key = url8qrcode_key['qrcode_key']
        # 获取二维码扫描登陆状态
        code = poll(qrcode_key)['code']

        def code_t(code):
            if code == 0:
                return "登录成功"
            elif code == 86101:
                return "未扫码"
            elif code == 86090:
                return "二维码已扫码未确认"
            elif code == 86038:
                return "二维码已失效"

        obs.script_log(obs.LOG_WARNING, str(code_t(code)))

        # 轮询二维码扫描登录状态
        def check_poll():
            global code
            """
            二维码扫描登录状态检测
            @param code: 一个初始的状态，用于启动轮询
            @return: cookies，超时为{}
            """
            code_ = code
            poll_ = poll(qrcode_key)
            code = poll_['code']
            if code_ != code:
                # 二维码扫描登陆状态改变时，输出改变后状态
                obs.script_log(obs.LOG_WARNING, str(code_t(code)))
                pass
            if code == 0 or code == 86038:
                # 二维码扫描登陆状态为成功或者超时时获取cookies结束[轮询二维码扫描登陆状态]
                cookies = poll_['cookies']
                if cookies:
                    # 获取登陆账号cookies中携带的uid
                    uid = int(cookies['DedeUserID'])
                    # 记录
                    configb = config_B(uid=uid, dirname=dirname)
                    configb.update(cookies)
                    # # 记录到默认登录字段
                    # configb = config_B(uid=0, dirname=dirname)
                    # configb.update(cookies)
                obs.remove_current_callback()

        obs.timer_add(check_poll, 1000)
        # cookies = await check_poll(code)
        #
        # return {'uid': int(cookies['DedeUserID']), 'cookies': cookies, 'cookie': dict2cookieformat(cookies)}


class Danmu:

    def __init__(self, cookie: str):
        self.cookie = cookie

    def _get_websocket_client(self, roomid: int):
        danmu_info = master(self.cookie).getDanmuInfo(roomid)
        token = danmu_info['data']['token']
        host = danmu_info['data']['host_list'][-1]
        wss_url = f"wss://{host['host']}:{host['wss_port']}/sub"

        user_info = master(self.cookie).get_user_info()
        cookie = cookie2dict(self.cookie)
        auth_body = {
            "uid": user_info["uid"],
            "roomid": roomid,
            "protover": 2,
            "buvid": cookie['buvid3'],
            "platform": "web",
            "type": 3,
            "key": token
        }
        return wss_url, auth_body

    def connect_room(self, roomid: int):
        obs.script_log(obs.LOG_INFO,
                       f"尝试连接【{getRoomBaseInfo(roomid)['by_room_ids'][str(roomid)]['uname']}】的直播间")
        wss_url, auth_body = self._get_websocket_client(roomid)
        return self._WebSocketClient(wss_url, auth_body)

    class _WebSocketClient:
        danmu_start_is = True
        danmu_working_is = True
        HEARTBEAT_INTERVAL = 30
        VERSION_NORMAL = 0
        VERSION_ZIP = 2

        def __init__(self, url: str, auth_body: dict):
            self.url = url
            self.auth_body = auth_body
            # pprint.pprint(auth_body)
            # self.saved_danmudata = set()

        async def connect(self):
            async with websockets.connect(self.url) as ws:
                await self.on_open(ws)
                while self.danmu_start_is:
                    self.danmu_working_is = True
                    message = await ws.recv()
                    await self.on_message(message)
                self.danmu_working_is = False

        async def on_open(self, ws):
            print("Connected to server...")
            await ws.send(self.pack(self.auth_body, 7))
            asyncio.create_task(self.send_heartbeat(ws))  # 这里不能加await

        async def send_heartbeat(self, ws):
            while True:
                await ws.send(self.pack(None, 2))
                await asyncio.sleep(self.HEARTBEAT_INTERVAL)

        async def on_message(self, message):
            if isinstance(message, bytes):
                self.unpack(message)

        def pack(self, content: dict|None, code: int) -> bytes:
            content_bytes = json.dumps(content).encode('utf-8') if content else b''
            header = (len(content_bytes) + 16).to_bytes(4, 'big') + \
                     (16).to_bytes(2, 'big') + \
                     self.VERSION_NORMAL.to_bytes(2, 'big') + \
                     code.to_bytes(4, 'big') + \
                     (1).to_bytes(4, 'big')
            return header + content_bytes

        def unpack(self, byte_buffer: bytes):
            package_len = int.from_bytes(byte_buffer[0:4], 'big')
            head_length = int.from_bytes(byte_buffer[4:6], 'big')
            prot_ver = int.from_bytes(byte_buffer[6:8], 'big')
            opt_code = int.from_bytes(byte_buffer[8:12], 'big')

            content_bytes = byte_buffer[16:package_len]
            if prot_ver == self.VERSION_ZIP:
                content_bytes = zlib.decompress(content_bytes)
                self.unpack(content_bytes)
                return

            content = content_bytes.decode('utf-8')
            if opt_code == 8:  # AUTH_REPLY
                obs.script_log(obs.LOG_INFO, f"身份验证回复: {content}\n")
            elif opt_code == 5:  # SEND_SMS_REPLY
                # if content not in self.saved_danmudata:
                #     self.saved_danmudata.add(content)
                #     # print(f"Danmu message at {datetime.datetime.now()}: {content}")
                if json.loads(content)['cmd'] == "DANMU_MSG":
                    pass
                    contentinfo = json.loads(content)['info']
                    contentinfo[0][15]['extra'] = json.loads(contentinfo[0][15]['extra'])
                    tfo = contentinfo[0][15]['extra']['content']
                    afo = ""
                    if contentinfo[0][15]['extra']['reply_uname']:
                        afo = f" @{contentinfo[0][15]['extra']['reply_uname']} "
                    ufo = contentinfo[0][15]['user']['base']['name']
                    mfo = ''
                    if contentinfo[0][15]['user']['medal']:
                        fmedal = contentinfo[0][15]['user']['medal']
                        mfo = f"【{fmedal['name']}|{fmedal['level']}】"
                    wfo = ''
                    if contentinfo[-2] != [0]:
                        wfo = str(contentinfo[-2])
                    obs.script_log(obs.LOG_INFO, f"{wfo}{mfo}{ufo}：{afo}{tfo}")
                elif json.loads(content)['cmd'] == "WIDGET_BANNER":
                    pass
                elif json.loads(content)['cmd'] == "INTERACT_WORD":
                    pass
                    contentdata = json.loads(content)['data']
                    # pprint.pprint(contentdata)
                    tfo = "进入直播间或关注消息"
                    if contentdata['msg_type'] == 1:
                        tfo = "进入直播间"
                    elif contentdata['msg_type'] == 2:
                        tfo = "关注直播间"
                    ufo = contentdata['uname']
                    mfo = ""
                    if contentdata['fans_medal']:
                        fmedal = contentdata['fans_medal']
                        mfo = f"【{fmedal['medal_name']}|{fmedal['medal_level']}】"
                    wfo = ''
                    try:
                        if json.loads(content)['data']['uinfo']['wealth']['level']:
                            wfo = f"[{json.loads(content)['data']['uinfo']['wealth']['level']}]"
                    except:
                        pass
                    obs.script_log(obs.LOG_INFO, f"{tfo}：\t{wfo}{mfo}{ufo}")
                elif json.loads(content)['cmd'] == "DM_INTERACTION":
                    pass
                    contentdata = json.loads(content)['data']
                    contentdata['data'] = json.loads(contentdata['data'])
                    tfo = "连续发送弹幕或点赞"
                    if contentdata['type'] == 102:
                        tfo = ""
                        for contentdatacombo in contentdata['data']['combo'][:-1]:
                            tfo += f"热词：\t{contentdatacombo['cnt']}\t人{contentdatacombo['guide']}{contentdatacombo['content']}\n"
                        tfo += f"连续弹幕：\t{contentdata['data']['combo'][-1]['cnt']}\t人{contentdata['data']['combo'][-1]['guide']}{contentdata['data']['combo'][-1]['content']}"
                    elif contentdata['type'] == 106:
                        tfo = f"连续点赞：\t{contentdata['data']['cnt']}\t{contentdata['data']['suffix_text']}"
                    obs.script_log(obs.LOG_INFO, f"{tfo}")
                elif json.loads(content)['cmd'] == "GUARD_BUY":
                    pass
                    contentdata = json.loads(content)['data']
                    tfo = f"上舰：\t{contentdata['username']}\t购买{contentdata['num']}个\t【{contentdata['gift_name']}】"
                    obs.script_log(obs.LOG_INFO, f"{tfo}")
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_CLICK":
                    pass
                    contentdata = json.loads(content)['data']
                    tfo = contentdata['like_text']
                    ufo = contentdata['uname']
                    mfo = ""
                    if contentdata['fans_medal']:
                        fmedal = contentdata['fans_medal']
                        mfo = f"【{fmedal['medal_name']}|{fmedal['guard_level']}】"
                    wfo = ''
                    try:
                        if contentdata['uinfo']['wealth']['level']:
                            wfo = f"[{contentdata['uinfo']['wealth']['level']}]"
                    except:
                        pass
                    obs.script_log(obs.LOG_INFO, f"点赞：\t{wfo}{mfo}{ufo}\t{tfo}")
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_UPDATE":
                    pass
                    contentdata = json.loads(content)['data']
                    obs.script_log(obs.LOG_INFO, f"点赞数：\t{contentdata['click_count']}")
                elif json.loads(content)['cmd'] == "ONLINE_RANK_COUNT":
                    pass
                    contentdata = json.loads(content)['data']
                    obs.script_log(obs.LOG_INFO, f"高能用户数：\t{contentdata['count']}")
                elif json.loads(content)['cmd'] == "WATCHED_CHANGE":
                    pass
                    contentdata = json.loads(content)['data']
                    obs.script_log(obs.LOG_INFO,
                                   f"直播间看过人数：\t{contentdata['num']}\t{contentdata['text_large']}")
                elif json.loads(content)['cmd'] == "ONLINE_RANK_V2":
                    pass
                elif json.loads(content)['cmd'] == "STOP_LIVE_ROOM_LIST":
                    pass
                elif json.loads(content)['cmd'] == "PK_BATTLE_PRE_NEW":
                    pass
                elif json.loads(content)['cmd'] == "PK_BATTLE_PRE":
                    pass
                elif json.loads(content)['cmd'] == "PK_BATTLE_START":
                    pass
                elif json.loads(content)['cmd'] == "RECOMMEND_CARD":
                    pass
                elif json.loads(content)['cmd'] == "SEND_GIFT":
                    pass
                    contentdata = json.loads(content)['data']
                    # pprint.pprint(contentdata)
                    ufo = contentdata['uname']
                    mfo = ""
                    if contentdata['medal_info']['medal_name']:
                        medali = contentdata['medal_info']
                        mfo = f"【{medali['medal_name']}|{medali['medal_level']}】"
                    wfo = ''
                    if contentdata['wealth_level'] != 0:
                        wfo = f"[{contentdata['wealth_level']}]"
                    tfo = ''
                    if contentdata['batch_combo_send']:
                        tfo += contentdata['batch_combo_send']['action']
                        if contentdata['batch_combo_send']['blind_gift']:
                            contentdata_bcsb_g = contentdata['batch_combo_send']['blind_gift']
                            tfo += f"\t【{contentdata_bcsb_g['original_gift_name']}】{contentdata_bcsb_g['gift_action']}"
                            coin = f"{contentdata_bcsb_g['gift_tip_price'] / 1000}￥\t{(contentdata_bcsb_g['gift_tip_price'] - contentdata['total_coin']) / 1000}￥"
                        else:
                            coin = f"{contentdata['total_coin'] / 1000}￥"
                        tfo += f"{contentdata['num']}个《{contentdata['batch_combo_send']['gift_name']}》\t{coin}"
                    else:
                        tfo += f"{contentdata['action']}{contentdata['num']}个《{contentdata['giftName']}》"
                    obs.script_log(obs.LOG_INFO, f'礼物：\t{wfo}{mfo}{ufo}\t{tfo}')
                elif json.loads(content)['cmd'] == "NOTICE_MSG":
                    pass
                else:
                    pprint.pprint(json.loads(content)['cmd'])

            if len(byte_buffer) > package_len:
                self.unpack(byte_buffer[package_len:])

        def start(self):
            asyncio.run(self.connect())


# end

# ================================================================================================


# -----------------------------------------------------------
# OBS Script Functions                                      -
# -----------------------------------------------------------

# --- 设置默认值
def script_defaults(settings):
    """
    调用以设置与脚本关联的默认设置(如果有的话)。为了设置其默认值，您通常会调用默认值函数。
    :param settings:与脚本关联的设置。
    """
    global scripts_data_dirpath, scripts_config_filepath, scripts_roomid_filepath
    global Default_roomStatus, DefaultArea, DefaultliveStatus, \
        allAreaList, \
        uid_list_dict_elements, login_button_enabled, \
        login_status_text_value, login_status_text_type, \
        Default_uname, \
        room_status_text_type, \
        live_group_enabled, \
        start_live_button_visible, stop_live_button_visible, \
        live_title_text_visible, change_live_title_button_visible, \
        live_news_text_visible, change_live_news_button_visible, \
        rtmp_copy_button_visible, stream_copy_button_visible, stream_updata_button_visible, \
        area1_true_button_visible, area2_true_button_visible, \
        area1_list_visible, area2_list_visible, \
        SentUid_list_dict_elements, SentRoom_list_set_elements, \
        SentRoom_list_enabled, emoji_face_list_visible, \
        emoji_face_list_dict_elements, \
        send_button_enabled, show_danmu_button_enabled
    # 路径变量
    scripts_data_dirpath = f"{script_path()}bilibili-live"
    scripts_config_filepath = Path(scripts_data_dirpath) / "config.json"
    scripts_roomid_filepath = Path(scripts_data_dirpath) / "roomid_set_data.json"
    # 创建 插件数据 文件夹
    try:
        os.makedirs(scripts_data_dirpath, exist_ok=True)
    except:
        obs.script_log(obs.LOG_WARNING, "权限不足！")
    # 获取 '默认账户' cookie
    Default_cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    # 获取 '默认账户' 登录信息
    interface_nav_Default = master(dict2cookieformat(Default_cookies)).interface_nav()
    # 检测 '默认账户' 可用性
    Default_islogin = interface_nav_Default["isLogin"]

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 设置 只读文本框[登录状态] 内容
    if Default_islogin:
        login_status_text_value = f'{interface_nav_Default["uname"]} 已登录'
    else:
        login_status_text_value = "未登录，\n请登录后点击⟳重新载入插件\n重新选择登录用户"
    obs.obs_data_set_string(settings, 'login_status_text', login_status_text_value)
    # 设置 只读文本框[登录状态] 类型
    if Default_islogin:
        login_status_text_type = obs.OBS_TEXT_INFO_NORMAL
    else:
        login_status_text_type = obs.OBS_TEXT_INFO_WARNING

    # 为 组合框[用户] 添加选项
    uid_list_dict_elements = {}
    if os.path.exists(scripts_config_filepath):
        with open(scripts_config_filepath, "r", encoding="utf-8") as j:
            config = json.load(j)
            # 从 "所有账户"配置 中 删除 '默认用户'配置，获得"全部账户"
            if "0" in config:
                del config["0"]
                for uid in config:
                    cookies = config_B(uid=int(uid), dirname=scripts_data_dirpath).check()
                    interface_nav = master(dict2cookieformat(cookies)).interface_nav()
                    islogin = interface_nav["isLogin"]
                    if islogin:
                        uid_list_dict_elements[uid] = interface_nav["uname"]
    uid_list_dict_elements = uid_list_dict_elements
    # 设置 组合框[用户] 内容
    if Default_islogin:
        Default_uname = interface_nav_Default["uname"]

    # 根据{弹幕输出状态}更改 按钮[登录] 可用状态
    try:
        DanMu_danmu_working_is = DanMu.danmu_working_is
    except:
        DanMu_danmu_working_is = False
    login_button_enabled = not DanMu_danmu_working_is

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 获取'默认账户'直播间基础信息
    Default_roomStatus = "_"
    RoomInfoOld = {}
    if Default_islogin:
        RoomInfoOld = getRoomInfoOld(Default_cookies['DedeUserID'])
        Default_roomStatus = RoomInfoOld["roomStatus"]

    # 设置 只读文本框[直播间状态] 的内容
    Defaultroomid = 0
    if Default_roomStatus == 0:
        room_status_text_value = "无"
    elif Default_roomStatus == 1:
        Defaultroomid = RoomInfoOld["roomid"]
        DefaultliveStatus = RoomInfoOld["liveStatus"]
        room_status_text_value = str(Defaultroomid)
        if DefaultliveStatus:
            live_Status = "直播中"
        else:
            live_Status = "未开播"
        room_status_text_value += f"【{live_Status}】"
    else:
        room_status_text_value = f"未登录"
    obs.obs_data_set_string(settings, 'room_status_text', room_status_text_value)
    # 设置 只读文本框[直播间状态] 的类型
    if Default_roomStatus == 0:
        room_status_text_type = obs.OBS_TEXT_INFO_WARNING
    elif Default_roomStatus == 1:
        room_status_text_type = obs.OBS_TEXT_INFO_NORMAL
    else:
        room_status_text_type = obs.OBS_TEXT_INFO_ERROR
    room_status_text_type = room_status_text_type

    # 获取'默认账号'直播间分区
    DefaultArea = {}
    RoomBaseInfo = {}
    if Default_roomStatus == 1:
        RoomBaseInfo = getRoomBaseInfo(Defaultroomid)
        DefaultArea = {
            "id": RoomBaseInfo["by_room_ids"][str(Defaultroomid)]["parent_area_id"],
            "name": RoomBaseInfo["by_room_ids"][str(Defaultroomid)]["parent_area_name"],
            "data": {
                "id": RoomBaseInfo["by_room_ids"][str(Defaultroomid)]["area_id"],
                "name": RoomBaseInfo["by_room_ids"][str(Defaultroomid)]["area_name"],
            }
        }
    DefaultArea = DefaultArea
    # 设置 组合框[一级分区] 内容
    if DefaultArea:
        obs.obs_data_set_string(settings, 'area1_list', str(DefaultArea["id"]))
    # 根据直播间存在更改 组合框[一级分区] 可见状态
    if Default_roomStatus == 1:
        area1_list_visible = True
    else:
        area1_list_visible = False

    # 根据直播间存在更改 按钮[确认一级分区] 可见状态
    area1_true_button_visible = area1_list_visible

    # 获取完整直播分区
    allAreaList = Area_getList()
    # 设置 组合框[二级分区] 的内容
    if DefaultArea:
        obs.obs_data_set_string(settings, 'area2_list', str(DefaultArea["data"]["id"]))
    # 根据直播间存在更改 组合框[二级分区] 可见状态
    area2_list_visible = area1_list_visible

    # 根据直播间存在更改 按钮[{确认分区}] 可见状态
    area2_true_button_visible = area1_list_visible

    # 根据直播状态更改 按钮[开播] 可见状态
    if Default_roomStatus == 1:
        if DefaultliveStatus:
            start_live_button_visible = False
        else:
            start_live_button_visible = True
    else:
        start_live_button_visible = False

    # 根据直播状态更改 按钮[直播服务器] 可见状态
    if Default_roomStatus == 1:
        rtmp_copy_button_visible = not start_live_button_visible
    else:
        rtmp_copy_button_visible = False

    # 根据直播状态更改 按钮[直播推流码] 可见状态
    if Default_roomStatus == 1:
        stream_copy_button_visible = not start_live_button_visible
    else:
        stream_copy_button_visible = False

    # 根据直播状态更改 按钮[更新推流码] 可见状态
    if Default_roomStatus == 1:
        stream_updata_button_visible = not start_live_button_visible
    else:
        stream_updata_button_visible = False

    # 根据直播状态更改 按钮[结束直播] 可见状态
    if Default_roomStatus == 1:
        stop_live_button_visible = not start_live_button_visible
    else:
        stop_live_button_visible = False

    # 设置 普通文本框[直播标题] 的内容
    if Default_roomStatus == 1:
        obs.obs_data_set_string(settings, 'live_title_text',
                                RoomBaseInfo["by_room_ids"][str(Defaultroomid)]["title"]
                                )
    # 根据直播间存在更改 普通文本框[直播标题] 可见状态
    live_title_text_visible = area1_list_visible

    # 根据直播间存在更改 按钮[更改直播标题] 可见状态
    change_live_title_button_visible = area1_list_visible

    # 设置 普通文本框[直播公告] 的内容
    if Default_roomStatus == 1:
        obs.obs_data_set_string(settings, 'live_news_text', master(dict2cookieformat(Default_cookies)).getRoomNews())
    # 根据直播间存在更改 普通文本框[直播公告] 可见状态
    live_news_text_visible = area1_list_visible

    # 根据直播间存在更改 按钮[更改直播公告] 可见状态
    change_live_news_button_visible = area1_list_visible

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 为组合框[发出弹幕的用户]添加选项
    SentUid_list_dict_elements = uid_list_dict_elements

    # 为组合框[弹幕发送到]添加选项
    SentRoom_list_set_elements = set()
    if os.path.exists(scripts_roomid_filepath):
        with open(scripts_roomid_filepath, "r", encoding="utf-8") as j:
            SentRoom_list_set_elements = eval(j.read())
    SentRoom_list_set_elements = SentRoom_list_set_elements
    # 为组合框[弹幕发送到]设置内容
    if SentRoom_list_set_elements:
        obs.obs_data_set_string(settings, 'SentRoom_list', list(SentRoom_list_set_elements)[0])

    # 根据弹幕输出状态更改 组合框【弹幕发送到】的可用性
    SentRoom_list_enabled = login_button_enabled

    # 为组合框[emoji表情]添加选项
    emoji_face_list_dict_elements = {}
    if Default_islogin and len(SentRoom_list_set_elements):
        SentRoom_list_value = obs.obs_data_get_string(settings, 'SentRoom_list')
        Emoticons = master(dict2cookieformat(Default_cookies)).GetEmoticons(int(SentRoom_list_value))
        for emoji_face in Emoticons[0]['emoticons']:
            emoji_face_list_dict_elements[emoji_face["emoji"]] = emoji_face["descript"]
    emoji_face_list_dict_elements = emoji_face_list_dict_elements
    # 根据直播状态更改 组合框[emoji表情] 可见状态
    if Default_islogin and len(SentRoom_list_set_elements):
        emoji_face_list_visible = True
    else:
        emoji_face_list_visible = False

    # 清空文本框[弹幕内容]
    obs.obs_data_set_string(settings, 'danmu_msg_text', "")

    # 设置[发送弹幕]按钮可用状态
    if SentUid_list_dict_elements:
        send_button_enabled = True
    else:
        send_button_enabled = False

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # 设置 [显示弹幕]按钮 可用状态
    if Default_islogin and len(SentRoom_list_set_elements):
        show_danmu_button_enabled = True
    else:
        show_danmu_button_enabled = False

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# --- 一个名为script_description的函数返回显示给的描述
def script_description():
    """
    调用以检索要在“脚本”窗口中显示给用户的描述字符串。
    """
    t = ('<html lang="zh-CN"><body><pre>\
本插件基于python3<br>\
    如果未安装python3，请前往<br>\
        <a href="https://www.python.org/">python官网</a><br>\
        或者<br>\
        <a href="https://python.p2hp.com/">python中文网 官网</a>下载安装<br>\
        不同操作系统请查看<br>\
            菜鸟教程<a href="https://www.runoob.com/python3/python3-install.html">Python3 环境搭建</a><br>\
<font color=yellow>!脚本路径中尽量不要有中文</font><br>\
<font color=green size=4>请在认为完成操作后点击<font color="white" size=5>⟳</font>重新载入插件</font><br>\
配置cookie：<br>\
<font color=yellow>！请看着脚本日志操作</font><br>\
扫描配置cookie请 提前增加<br>\
   脚本日志窗口 宽高<br>\
手动配置cookie请前往<br>\
   <a href="https://link.bilibili.com/p/center/index#/my-room/start-live">B站直播设置后台</a> 使用<br>\
       浏览器的开发人员工具获取cookie<br><br>\
<font color="#ee4343">【cookie！为账号的{极重要}的隐私信息!】</font><br>\
<font color="#ee4343">【！不要泄露给他人!】</font><br>\
<br>\
如果报错：<br>\
   请关闭梯子和加速器<br>\
   Windows请尝试使用<font color="#ee4343">管理员</font>权限运行obs<br>\
   其它系统请联系开发者<br>\
</pre></body></html>')
    t = ('<html lang="zh-CN"><body><pre>\
本插件基于<font color="#ee4343" size=5>python3.10</font><br>\
<font color=yellow>!脚本路径中尽量不要有中文</font><br>\
<font color="white" size=5>⟳</font><font color=green size=4>为重新载入插件按钮</font><br>\
如果报错：<br>\
   关闭梯子或加速器<br>\
   Windows请尝试使用<font color="#ee4343">管理员权限</font>运行obs<br>\
   其它问题请前往<a href="https://github.com/lanyangyin/OBSscripts-bilibili-live/issues">Github</a>提问<br>\
</pre></body></html>')
    return t


# --- 一个名为script_load的函数将在启动时调用

def script_load(settings):
    """
    在脚本启动时调用与脚本相关的特定设置。所提供的设置参数通常不用于由用户设置的设置;
    相反，该参数用于脚本中可能使用的任何额外的内部设置数据。
    :param settings:与脚本关联的设置。
    """
    global current_settings, emoji_face_list_value, SentRoom_list_value
    # obs_data_t 类型的数据对象。这个数据对象可以用来存储和管理设置项，例如场景、源或过滤器的配置信息
    # settings = obs.obs_data_create()
    current_settings = settings
    obs.script_log(obs.LOG_INFO, "已载入：bilibili-live")
    # 获得 组合框【emoji表情】 的内容
    emoji_face_list_value = obs.obs_data_get_string(current_settings, "emoji_face_list")
    # 获得 组合框【弹幕发送到】 的内容
    SentRoom_list_value = obs.obs_data_get_string(current_settings, "SentRoom_list")


# 控件状态更新时调用
def script_update(settings):
    """
    当用户更改了脚本的设置(如果有的话)时调用。
    :param settings:与脚本关联的设置。
    """
    global emoji_face_list_value, SentRoom_list_value, DanMu
    # 当 组合框【emoji表情】 的内容 更改时 将 组合框【emoji表情】 的内容 载入剪贴板
    if emoji_face_list_value != obs.obs_data_get_string(current_settings, "emoji_face_list"):
        emoji_face_list_value = obs.obs_data_get_string(current_settings, "emoji_face_list")
        cb.copy(emoji_face_list_value)
    # 当 组合框【弹幕发送到】 的内容 更改时 将 刷新弹幕输出的直播间
    if SentRoom_list_value != obs.obs_data_get_string(current_settings, "SentRoom_list"):
        SentRoom_list_value = obs.obs_data_get_string(current_settings, "SentRoom_list")
        # 获得组合框[选择账号]的内容
        uid_list_value = obs.obs_data_get_string(current_settings, 'uid_list')
        # 获取[选择账号]的内容对应的账户cookies
        cookies = config_B(uid=int(uid_list_value), dirname=scripts_data_dirpath).check()
        # # 获得组合框[发出弹幕的用户]的内容
        # SentUid_list_value = obs.obs_data_get_string(current_settings, 'SentUid_list')
        # # 获取[发出弹幕的用户]的内容对应的账户cookies
        # cookies = config_B(uid=int(SentUid_list_value), dirname=scripts_data_dirpath).check()
        # 获得组合框【弹幕发送到】 的内容
        SentRoom = obs.obs_data_get_string(current_settings, 'SentRoom_list')
        # 当  弹幕正在输出时 将 刷新弹幕输出的直播间
        try:
            if DanMu.danmu_working_is:
                # 关闭当前正在输出的弹幕
                DanMu.danmu_start_is = False

                # 为 新的直播间 开启新输出的弹幕
                def danmu_s():
                    global DanMu
                    DanMu = Danmu(dict2cookieformat(cookies)).connect_room(int(SentRoom))
                    DanMu.start()
                t1 = threading.Thread(target=danmu_s)
                t1.start()
        except:
            pass


# --- 一个名为script_properties的函数定义了用户可以使用的属性
def script_properties():
    """
    调用以定义与脚本关联的用户属性。这些属性用于定义如何向用户显示设置属性。
    :return:通过 obs_properties_create() 创建的 Obs_properties_t 对象
    """
    props = obs.obs_properties_create()  # 创建一个 OBS 属性集对象，他将包含所有控件对应的属性对象
    # obs_properties_t 类型的属性对象。这个属性对象通常用于枚举 libobs 对象的可用设置，
    # 通常用于自动生成用户界面小部件，也可以用来枚举特定设置的可用值或有效值。
    global setting_props, \
        live_props, \
        send_danmu_group, \
        show_danmu_group
    global login_status_text, \
        uid_list, login_button
    global room_status_text, \
        area1_list, \
        area1_true_button, \
        area2_list, \
        area2_true_button, \
        start_live_button, rtmp_address_copy_button, rtmp_stream_code_copy_button, rtmp_stream_code_updata_button, \
        stop_live_button, \
        live_title_text, change_live_title_button, live_news_text, change_live_news_button
    global SentUid_list, \
        SentRoom_list, \
        emoji_face_list, \
        send_button, \
        show_danmu_button

    # 为 分组框【配置】 建立属性集
    setting_props = obs.obs_properties_create()
    # 为 分组框【直播】 建立属性集
    live_props = obs.obs_properties_create()
    # 为 分组框【发送弹幕】 建立属性集
    send_danmu_group = obs.obs_properties_create()
    # 为 分组框【输出弹幕】 建立属性集
    show_danmu_group = obs.obs_properties_create()
    # —————————————————————————————————————————————————————————————————————————————————————————————————————
    # 添加 分组框【配置】
    obs.obs_properties_add_group(props, 'setting_group', '配置', obs.OBS_GROUP_NORMAL, setting_props)

    # 添加 只读文本框[登录状态]
    login_status_text = obs.obs_properties_add_text(
        setting_props, 'login_status_text', "登录状态：", obs.OBS_TEXT_INFO
    )
    # 设置 只读文本框[登录状态] 类型
    obs.obs_property_text_set_info_type(login_status_text, login_status_text_type)

    # 添加 组合框[用户]
    uid_list = obs.obs_properties_add_list(
        setting_props, 'uid_list', '用户：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    # 为 组合框[用户] 添加选项
    for i in uid_list_dict_elements:
        try:
            if uid_list_dict_elements[i] == Default_uname:
                obs.obs_property_list_insert_string(uid_list, 0, uid_list_dict_elements[i], i)
            else:
                obs.obs_property_list_add_string(uid_list, uid_list_dict_elements[i], i)
        except:
            obs.obs_property_list_add_string(uid_list, uid_list_dict_elements[i], i)
    # 为 组合框[用户] 添加 添加新的账号 选项
    obs.obs_property_list_add_string(uid_list, '添加新的账号', "-1")

    # 添加 按钮[登录]
    login_button = obs.obs_properties_add_button(setting_props, "login_button", "登录", login)
    # 设置 按钮[登录] 可用状态
    obs.obs_property_set_enabled(login_button, login_button_enabled)

    # ————————————————————————————————————————————————————————————————
    # 添加 分组框【直播】
    obs.obs_properties_add_group(props, 'live_group', '直播', obs.OBS_GROUP_NORMAL, live_props)

    # 添加 只读文本框[直播间状态]
    room_status_text = obs.obs_properties_add_text(
        live_props, 'room_status_text', f'直播间：', obs.OBS_TEXT_INFO
    )
    # 设置 只读文本框[直播间状态] 类型
    obs.obs_property_text_set_info_type(room_status_text, room_status_text_type)

    # 添加 组合框[一级分区]
    area1_list = obs.obs_properties_add_list(
        live_props, 'area1_list', '一级分区：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    # 为 组合框[一级分区] 添加选项
    for area in allAreaList:
        try:
            if area["name"] == DefaultArea["name"]:
                obs.obs_property_list_insert_string(area1_list, 0, area["name"], str(area["id"]))
            else:
                obs.obs_property_list_add_string(area1_list, area["name"], str(area["id"]))
        except:
            obs.obs_property_list_add_string(area1_list, area["name"], str(area["id"]))
    # 设置 组合框[一级分区] 可见状态
    obs.obs_property_set_visible(area1_list, area1_list_visible)

    # 添加 按钮[确认一级分区]
    area1_true_button = obs.obs_properties_add_button(live_props, "area1_true_button", "确认一级分区", start_area1)
    # 设置 按钮[确认一级分区] 可见状态
    obs.obs_property_set_visible(area1_true_button, area1_true_button_visible)

    # 添加 组合框[二级分区]
    area2_list = obs.obs_properties_add_list(
        live_props, 'area2_list', '二级分区：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    # 获取 组合框[一级分区] 内容
    area1_id = obs.obs_data_get_string(current_settings, 'area1_list')
    # 为 组合框[二级分区] 添加选项
    for area in allAreaList:
        if area1_id == str(area["id"]):
            for area2 in area["list"]:
                try:
                    if area2["name"] == DefaultArea["data"]["name"]:
                        obs.obs_property_list_insert_string(area2_list, 0, area2["name"], str(area2["id"]))
                    else:
                        obs.obs_property_list_add_string(area2_list, area2["name"], str(area2["id"]))
                except:
                    obs.obs_property_list_add_string(area2_list, area2["name"], str(area2["id"]))
            break
    # 设置 组合框[二级分区] 可见状态
    obs.obs_property_set_visible(area2_list, area2_list_visible)

    # 添加 按钮[{确认分区}]
    area2_true_button = obs.obs_properties_add_button(live_props, "area2_true_button", "{确认分区}",
                                                      lambda ps, p: start_area())
    # 设置 按钮[{确认分区}] 可见状态
    obs.obs_property_set_visible(area2_true_button, area2_true_button_visible)

    # 添加 按钮[开播]
    start_live_button = obs.obs_properties_add_button(live_props, "start_live_button", "开始直播", start_live)
    # 设置 按钮[开播] 可见状态
    obs.obs_property_set_visible(start_live_button, start_live_button_visible)

    # 添加 按钮[直播服务器]
    rtmp_address_copy_button = obs.obs_properties_add_button(live_props, "rtmp_address_copy_button", "rtmp直播服务器",
                                                             rtmp_address_copy)
    # 设置 按钮[直播服务器] 可见状态
    obs.obs_property_set_visible(rtmp_address_copy_button, rtmp_copy_button_visible)

    # 添加 按钮[直播推流码]
    rtmp_stream_code_copy_button = obs.obs_properties_add_button(live_props, "rtmp_stream_code_copy_button",
                                                                 "rtmp直播推流码", rtmp_stream_code_copy)
    # 设置 按钮[直播推流码] 可见状态
    obs.obs_property_set_visible(rtmp_stream_code_copy_button, stream_copy_button_visible)

    # 添加 按钮[更新推流码]
    rtmp_stream_code_updata_button = obs.obs_properties_add_button(live_props, "rtmp_stream_code_updata_button",
                                                                   "更新rtmp直播推流码", rtmp_stream_code_updata)
    # 设置 按钮[更新推流码] 可见状态
    obs.obs_property_set_visible(rtmp_stream_code_updata_button, stream_updata_button_visible)

    # 添加 按钮[结束直播]
    stop_live_button = obs.obs_properties_add_button(live_props, "stop_live_button", "结束直播", stop_live)
    # 设置 按钮[结束直播] 可见状态
    obs.obs_property_set_visible(stop_live_button, stop_live_button_visible)

    # 添加 普通文本框[直播标题]
    live_title_text = obs.obs_properties_add_text(live_props, "live_title_text", "直播标题", obs.OBS_TEXT_DEFAULT)
    # 设置 普通文本框[直播标题] 可见状态
    obs.obs_property_set_visible(live_title_text, live_title_text_visible)

    # 添加 按钮[更改直播标题]
    change_live_title_button = obs.obs_properties_add_button(live_props, "change_live_title_button", "更改直播标题", change_live_title)
    # 设置 按钮[更改直播标题] 可见状态
    obs.obs_property_set_visible(change_live_title_button, change_live_title_button_visible)

    # 添加 普通文本框[直播公告]
    live_news_text = obs.obs_properties_add_text(live_props, "live_news_text", "直播公告", obs.OBS_TEXT_DEFAULT)
    # 设置 普通文本框[直播公告] 可见状态
    obs.obs_property_set_visible(live_news_text, live_news_text_visible)

    # 添加 按钮[更改直播公告]
    change_live_news_button = obs.obs_properties_add_button(live_props, "change_live_news_button", "更改直播公告", change_live_news)
    # 设置 按钮[更改直播公告] 可见状态
    obs.obs_property_set_visible(change_live_news_button, change_live_news_button_visible)

    # ————————————————————————————————————————————————————————————————————————————————
    # 添加 分组框【发送弹幕】
    obs.obs_properties_add_group(props, 'send_danmu_group', '发送弹幕', obs.OBS_GROUP_NORMAL, send_danmu_group)

    # 添加 组合框[发出弹幕的用户]
    SentUid_list = obs.obs_properties_add_list(
        send_danmu_group, 'SentUid_list', '发出弹幕的用户：'
        , obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    # 为 组合框[发出弹幕的用户] 添加选项
    for SentUid in SentUid_list_dict_elements:
        obs.obs_property_list_add_string(SentUid_list, SentUid_list_dict_elements[SentUid], SentUid)

    # 添加 组合框[弹幕发送到]
    SentRoom_list = obs.obs_properties_add_list(
        send_danmu_group, 'SentRoom_list', '弹幕发送到：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    # 为 组合框[弹幕发送到] 添加选项
    for SentRoomid in SentRoom_list_set_elements:
        # 获得 保存到直播间 的 信息
        RoomBaseInfo = getRoomBaseInfo(int(SentRoomid))
        obs.obs_property_list_add_string(
            SentRoom_list, RoomBaseInfo["by_room_ids"][str(SentRoomid)]["uname"] + "_的直播间", str(SentRoomid)
        )
    # 设置 按钮[弹幕发送到] 可用状态
    obs.obs_property_set_enabled(SentRoom_list, SentRoom_list_enabled)

    # 添加 组合框[emoji表情]
    emoji_face_list = obs.obs_properties_add_list(
        send_danmu_group, 'emoji_face_list', 'emoji表情：', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    # 为 组合框[emoji表情] 添加选项
    for emoji_face in emoji_face_list_dict_elements:
        obs.obs_property_list_add_string(
            emoji_face_list, emoji_face_list_dict_elements[emoji_face], emoji_face
        )
    # 设置 组合框[emoji表情] 可见状态
    obs.obs_property_set_visible(emoji_face_list, emoji_face_list_visible)

    # 添加 换行文本框[弹幕内容]
    obs.obs_properties_add_text(send_danmu_group, 'danmu_msg_text', '弹幕内容：', obs.OBS_TEXT_MULTILINE)

    # 添加 按钮[发送弹幕]
    send_button = obs.obs_properties_add_button(send_danmu_group, 'send_button', '发送弹幕', send)
    # 设置 按钮[发送弹幕] 可用状态
    obs.obs_property_set_enabled(send_button, send_button_enabled)

    # 添加 按钮[更改屏蔽词]
    correct_mask_word_button = obs.obs_properties_add_button(send_danmu_group, 'correct_mask_word_button', '更改屏蔽词',
                                                             lambda ps, p: correct_mask_word())

    # ————————————————————————————————————————————————————————————————————————————————
    # 添加 分组框【输出弹幕】
    obs.obs_properties_add_group(props, 'show_danmu_group', '输出弹幕', obs.OBS_GROUP_NORMAL, show_danmu_group)

    # 添加 按钮[显示弹幕]
    show_danmu_button = obs.obs_properties_add_button(show_danmu_group, 'show_danmu_button', '显示弹幕', show_danmu)
    # 设置 按钮[显示弹幕] 可用状态
    obs.obs_property_set_enabled(show_danmu_button, show_danmu_button_enabled)

    # ————————————————————————————————————————————————————————————————————————————————
    # 添加 按钮[直播间后台网页]
    Blive_web_button = obs.obs_properties_add_button(props, 'Blive_web_button', f'直播间后台网页', Blive_web)
    obs.obs_property_button_set_type(Blive_web_button, obs.OBS_BUTTON_URL)
    obs.obs_property_button_set_url(Blive_web_button, "https://link.bilibili.com/p/center/index#/my-room/start-live")

    return props


def login(props, prop):
    # ＝＝＝＝＝＝＝＝＝
    # 　　　登录　　　＝
    # ＝＝＝＝＝＝＝＝＝
    uid = obs.obs_data_get_string(current_settings, 'uid_list')
    if uid == "-1":
        # 如果添加账户 移除默认账户
        config_B(uid=0, dirname=scripts_data_dirpath).update({})
    start_login(int(uid), dirname=scripts_data_dirpath)
    # 更新OBS配置信息
    script_defaults(current_settings)
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # 　　　　更新脚本用户小部件　　　　　＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    #####################################################################
    # 设置只读文本框[登录状态]的类型
    obs.obs_property_text_set_info_type(login_status_text, login_status_text_type)

    # 清空组合框[选择账号]
    obs.obs_property_list_clear(uid_list)
    # 为组合框[选择账号]添加选项
    for i in uid_list_dict_elements:
        try:
            if uid_list_dict_elements[i] == Default_uname:
                obs.obs_property_list_insert_string(uid_list, 0, uid_list_dict_elements[i], i)
            else:
                obs.obs_property_list_add_string(uid_list, uid_list_dict_elements[i], i)
        except:
            obs.obs_property_list_add_string(uid_list, uid_list_dict_elements[i], i)
    # 为 组合框[用户] 添加 添加新的账号 选项
    obs.obs_property_list_add_string(uid_list, '添加新的账号', "-1")

    # 设置 按钮[登录] 可用状态
    obs.obs_property_set_enabled(login_button, login_button_enabled)

    ######################################################################
    # 设置只读文本框[直播间状态]的类型
    obs.obs_property_text_set_info_type(room_status_text, room_status_text_type)

    # 清空组合框[一级分区]
    obs.obs_property_list_clear(area1_list)
    # 为组合框[一级分区]添加选项
    for area in allAreaList:
        try:
            if area["name"] == DefaultArea["name"]:
                obs.obs_property_list_insert_string(area1_list, 0, area["name"], str(area["id"]))
            else:
                obs.obs_property_list_add_string(area1_list, area["name"], str(area["id"]))
        except:
            obs.obs_property_list_add_string(area1_list, area["name"], str(area["id"]))
    # 根据直播状态更改 组合框[一级分区] 可见状态
    obs.obs_property_set_visible(area1_list, area1_list_visible)

    # 根据直播间存在更改 按钮[确认一级分区] 可见状态
    obs.obs_property_set_visible(area1_true_button, area1_true_button_visible)

    # 清空组合框[二级分区]
    obs.obs_property_list_clear(area2_list)
    # 从组合框[一级分区]获取一级分组id
    area1_id = obs.obs_data_get_string(current_settings, 'area1_list')
    # 为组合框[二级分区]添加选项
    for area in allAreaList:
        if area1_id == str(area["id"]):
            for area2 in area["list"]:
                try:
                    if area2["name"] == DefaultArea["data"]["name"]:
                        obs.obs_property_list_insert_string(area2_list, 0, area2["name"], str(area2["id"]))
                    else:
                        obs.obs_property_list_add_string(area2_list, area2["name"], str(area2["id"]))
                except:
                    obs.obs_property_list_add_string(area2_list, area2["name"], str(area2["id"]))
            break
    # 根据直播状态更改 组合框[二级分区] 可见状态
    obs.obs_property_set_visible(area2_list, area2_list_visible)

    # 根据直播间存在更改 按钮[{确认分区}] 可见状态
    obs.obs_property_set_visible(area2_true_button, area2_true_button_visible)

    # 根据直播状态更改 按钮[开播] 可见状态
    obs.obs_property_set_visible(start_live_button, start_live_button_visible)

    # 根据直播状态更改 按钮[直播服务器] 可见状态
    obs.obs_property_set_visible(rtmp_address_copy_button, rtmp_copy_button_visible)

    # 根据直播状态更改 按钮[直播推流码] 可见状态
    obs.obs_property_set_visible(rtmp_stream_code_copy_button, stream_copy_button_visible)

    # 根据直播状态更改 按钮[更新推流码] 可见状态
    obs.obs_property_set_visible(rtmp_stream_code_updata_button, stream_updata_button_visible)

    # 根据直播状态更改 按钮[停播] 可见状态
    obs.obs_property_set_visible(stop_live_button, stop_live_button_visible)

    # 设置 普通文本框[直播标题] 可见状态
    obs.obs_property_set_visible(live_title_text, live_title_text_visible)

    # 设置 按钮[更改直播标题] 可见状态
    obs.obs_property_set_visible(change_live_title_button, change_live_title_button_visible)

    # 设置 普通文本框[直播公告] 可见状态
    obs.obs_property_set_visible(live_news_text, live_news_text_visible)

    # 设置 按钮[更改直播公告] 可见状态
    obs.obs_property_set_visible(change_live_news_button, change_live_news_button_visible)

    ###########################################################################
    # 清空组合框[发出弹幕的用户]
    obs.obs_property_list_clear(SentUid_list)
    # 为组合框[发出弹幕的用户]添加选项
    for SentUid in SentUid_list_dict_elements:
        obs.obs_property_list_add_string(SentUid_list, SentUid_list_dict_elements[SentUid], SentUid)

    # 清空组合框[emoji表情]
    obs.obs_property_list_clear(emoji_face_list)
    # 为组合框[emoji表情]添加选项
    for emoji_face in emoji_face_list_dict_elements:
        obs.obs_property_list_add_string(
            emoji_face_list, emoji_face_list_dict_elements[emoji_face], emoji_face
        )
    # 根据直播状态更改 组合框[emoji表情] 可见状态
    obs.obs_property_set_visible(emoji_face_list, emoji_face_list_visible)

    # 清空组合框[弹幕发送到]
    obs.obs_property_list_clear(SentRoom_list)
    # 为组合框[弹幕发送到]添加选项
    for roomid in SentRoom_list_set_elements:
        # 获得 保存到直播间 的 信息
        RoomBaseInfo = getRoomBaseInfo(int(roomid))
        obs.obs_property_list_add_string(
            SentRoom_list, RoomBaseInfo["by_room_ids"][str(roomid)]["uname"] + "_的直播间", str(roomid)
        )
    # 设置按钮[弹幕发送到]的可用状态
    obs.obs_property_set_enabled(SentRoom_list, SentRoom_list_enabled)

    # 设置按钮[发送弹幕]的可用状态
    obs.obs_property_set_enabled(send_button, send_button_enabled)

    ###########################################################################
    # 设置按钮[显示弹幕]的可用状态
    obs.obs_property_set_enabled(show_danmu_button, show_danmu_button_enabled)

    return True


def start_area1(props, prop):
    area2_list = obs.obs_properties_get(live_props, "area2_list")
    obs.obs_property_list_clear(area2_list)
    # 获取一级分组id
    area1_id = obs.obs_data_get_string(current_settings, 'area1_list')
    # 更新【二级分区】的组合框
    for area in allAreaList:
        if area1_id == str(area["id"]):
            for area2 in area["list"]:
                try:
                    if str(area2["id"]) == str(DefaultArea["data"]["id"]):
                        obs.obs_property_list_insert_string(area2_list, 0, area2["name"], str(area2["id"]))
                    else:
                        obs.obs_property_list_add_string(area2_list, area2["name"], str(area2["id"]))
                except:
                    obs.obs_property_list_add_string(area2_list, area2["name"], str(area2["id"]))
            break
    return True


def start_area():
    # 获取默认账户
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    # 获取二级分区id
    area2_id = obs.obs_data_get_string(current_settings, 'area2_list')
    CsrfAuthenticationL(dict2cookieformat(cookies)).AnchorChangeRoomArea(int(area2_id))
    pass


def start_live(props, prop):
    obs.script_log(obs.LOG_INFO, 'start_live')
    # 获取默认账户
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    # 开播
    if cookies:
        # 获取二级分区id
        area2_id = obs.obs_data_get_string(current_settings, 'area2_list')
        startlive = CsrfAuthenticationL(dict2cookieformat(cookies)).startLive(int(area2_id))
        # 将 rtmp推流码 复制到剪贴板
        cb.copy(startlive["data"]["rtmp"]["code"])
    # 设置组合框[用户]为'默认用户'
    obs.obs_data_set_string(current_settings, 'uid_list', cookies["DedeUserID"])

    login(props, prop)
    return True


def rtmp_address_copy(props, prop):
    # 获取默认账户
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    cb.copy(CsrfAuthenticationL(dict2cookieformat(cookies)).FetchWebUpStreamAddr()['data']['addr']['addr'])
    pass


def rtmp_stream_code_copy(props, prop):
    # 获取默认账户
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    cb.copy(CsrfAuthenticationL(dict2cookieformat(cookies)).FetchWebUpStreamAddr()['data']['addr']['code'])
    pass


def rtmp_stream_code_updata(props, prop):
    # 获取默认账户
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    cb.copy(CsrfAuthenticationL(dict2cookieformat(cookies)).FetchWebUpStreamAddr(True)['data']['addr']['code'])
    pass


def stop_live(props, prop):
    obs.script_log(obs.LOG_INFO, 'stop_live')
    # 获取默认账户
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    # 停播
    if cookies:
        CsrfAuthenticationL(dict2cookieformat(cookies)).stopLive()
    # 设置组合框[用户]为'默认用户'
    obs.obs_data_set_string(current_settings, 'uid_list', cookies["DedeUserID"])
    login(props, prop)
    return True


# 设定 计时器 中的 弹幕消息切片 元素序号
danmu_msg_list_num = 0
# 弹幕字数等级
send_danmu_msg_word_num = 40
# 设定 计时器 的使用状态
send_danmu_msg_list_clock = False


def send(props, prop):
    # 获得组合框[发出弹幕的用户]的内容
    SentUid = obs.obs_data_get_string(current_settings, 'SentUid_list')
    # 获取[发出弹幕的用户]账户cookies
    cookies = config_B(uid=int(SentUid), dirname=scripts_data_dirpath).check()
    # 获得组合框【弹幕发送到】 的内容
    SentRoom = obs.obs_data_get_string(current_settings, 'SentRoom_list')
    # 获得 文本框【弹幕内容】 的内容
    danmu_msg = obs.obs_data_get_string(current_settings, 'danmu_msg_text')
    # 如果字符串为空，则不发送弹幕
    if danmu_msg.strip() == "":
        obs.script_log(obs.LOG_INFO, "弹幕内容为空，不发送弹幕")

    # # 清空 文本框【弹幕内容】 的内容
    # obs.obs_data_set_string(current_settings, 'danmu_msg_text', "")
    # 当以 \n 开头 执行 添加或者减少发送的直播间
    try:
        DanMu_danmu_working_is = DanMu.danmu_working_is
    except:
        DanMu_danmu_working_is = False
    if str(danmu_msg).startswith("\n") and not DanMu_danmu_working_is:  # 添加直播间或删除直播间
        roomid_set_data = set()
        danmu_room_add_or_delet = str(danmu_msg).strip()
        if danmu_room_add_or_delet in ["-", "－"]:
            # 获得组合框【弹幕发送到】的内容
            danmu_room_delet = SentRoom
            if os.path.exists(scripts_roomid_filepath):
                with open(scripts_roomid_filepath, "r", encoding="utf-8") as j:
                    roomid_set_data = eval(j.read())
                with open(scripts_roomid_filepath, "w", encoding="utf-8") as j:
                    roomid_set_data.discard(danmu_room_delet)
                    j.write(str(roomid_set_data))
                obs.script_log(obs.LOG_INFO, "删除直播间")
            obs.obs_data_set_string(current_settings, 'danmu_msg_text', "")
            # 设置组合框[用户]为'默认用户'
            obs.obs_data_set_string(current_settings, 'uid_list', cookies["DedeUserID"])
            login(props, prop)
        else:
            try:
                danmu_room_add = int(danmu_room_add_or_delet)
            except:
                obs.obs_data_set_string(current_settings, 'danmu_msg_text', "请输入正常直播间号")
            else:
                RoomBaseInfo = getRoomBaseInfo(int(danmu_room_add))
                for long_roomid in RoomBaseInfo["by_room_ids"]:
                    if os.path.exists(scripts_roomid_filepath):
                        with open(scripts_roomid_filepath, "r", encoding="utf-8") as j:
                            roomid_set_data = eval(j.read())
                    with open(scripts_roomid_filepath, "w", encoding="utf-8") as j:
                        roomid_set_data.add(long_roomid)
                        j.write(str(roomid_set_data))
                obs.script_log(obs.LOG_INFO, "添加直播间")
                obs.obs_data_set_string(current_settings, 'danmu_msg_text', "")
                # 设置 组合框[用户] 内容为'默认用户'
                obs.obs_data_set_string(current_settings, 'uid_list', cookies["DedeUserID"])
                login(props, prop)

    # 将弹幕发送到直播间
    if not str(danmu_msg).startswith("\n") and obs.obs_property_list_item_count(SentRoom_list):
        global danmu_msg_list_num, send_danmu_msg_list_clock, \
            send_danmu_msg_split_list_dict, send_danmu_msg_word_num
        try:
            DanMu_danmu_working_is = DanMu.danmu_working_is
        except:
            DanMu_danmu_working_is = False
        if not DanMu_danmu_working_is:
            obs.script_log(obs.LOG_INFO, "发送弹幕")
        # 弹幕切分
        if not send_danmu_msg_list_clock:
            danmu_msg_list_split = split_of_list(danmu_msg, list(emoji_face_list_dict_elements.keys()))
            # print(9, danmu_msg_list_split)
            danmu_msg_word_num_max_lever_list = [40, 30, 20]
            send_danmu_msg_split_list_dict = {}
            for danmu_msg_word_num_max in danmu_msg_word_num_max_lever_list:
                # 根据不同等级的弹幕字数，制造 弹幕内容切分 列表
                danmu_msg_split_word_num = 0
                send_danmu_msg_split_list = []
                send_danmu_msg_split_t = ''
                for danmu_msg_list_split_element in danmu_msg_list_split:
                    # print(danmu_msg_list_split_element)
                    # 使用表情切分弹幕内容，将文字和表情分开, 获得列表
                    send_danmu_msg_split_t += danmu_msg_list_split_element
                    if danmu_msg_list_split_element in emoji_face_list_dict_elements:
                        # print(0)
                        # 若是表情则 弹幕字数 +1
                        danmu_msg_split_word_num += 1
                        # 根据 弹幕字数，组合 发送弹幕切分列表
                        if danmu_msg_split_word_num == danmu_msg_word_num_max:
                            # 当 弹幕字数 为 可发送最大字数 时， 重置弹幕计数
                            danmu_msg_split_word_num = 0
                            # 添加入 发送弹幕切分列表
                            send_danmu_msg_split_list.append(send_danmu_msg_split_t)
                            # 重置 这次从 表情切分弹幕内容 获取的 弹幕内容
                            send_danmu_msg_split_t = ''
                    elif danmu_msg_list_split_element not in emoji_face_list_dict_elements:
                        # print(1)
                        # 若是普通弹幕则 弹幕字数 +普通弹幕字数
                        danmu_msg_split_word_num += len(danmu_msg_list_split_element)
                        # print("len", len(danmu_msg_list_split_element))
                        # 根据 弹幕字数，组合发送弹幕切分列表
                        if danmu_msg_split_word_num == danmu_msg_word_num_max:
                            # 当 弹幕字数 为 可发送最大字数 时， 重置弹幕计数
                            danmu_msg_split_word_num = 0
                            # 添加入 发送弹幕切分列表
                            send_danmu_msg_split_list.append(send_danmu_msg_split_t)
                            # 重置 这次从 表情切分弹幕内容 获取的 弹幕内容
                            send_danmu_msg_split_t = ''
                        elif danmu_msg_split_word_num > danmu_msg_word_num_max:
                            # 将在 开头的 可发送最大字数 添加入 发送弹幕切分列表，避免后续将 表情重定符 算入弹幕字数
                            ll_danmu_msg_word_max_num = danmu_msg_word_num_max - danmu_msg_split_word_num
                            # print(send_danmu_msg_split_t[:ll_danmu_msg_word_max_num], ll_danmu_msg_word_max_num)
                            send_danmu_msg_split_list.append(send_danmu_msg_split_t[:ll_danmu_msg_word_max_num])
                            # 重置弹幕计数
                            danmu_msg_split_word_num = 0
                            # 将 除了 开头的 可发送最大字数 的 弹幕内容
                            send_danmu_msg_split_t = send_danmu_msg_split_t[ll_danmu_msg_word_max_num:]
                            # print(send_danmu_msg_split_t)
                            # 弹幕计数 除了 开头的 可发送最大字数 的 弹幕内容
                            danmu_msg_split_word_num += len(send_danmu_msg_split_t)
                            if danmu_msg_split_word_num == danmu_msg_word_num_max:
                                # 当 弹幕字数 为 可发送最大字数 时， 重置弹幕计数
                                danmu_msg_split_word_num = 0
                                # 添加入 发送弹幕切分列表
                                send_danmu_msg_split_list.append(send_danmu_msg_split_t)
                                # 重置 这次从 表情切分弹幕内容 获取的 弹幕内容
                                send_danmu_msg_split_t = ''
                            elif danmu_msg_split_word_num > danmu_msg_word_num_max:
                                send_danmu_msg_split_t_split = split_by_n(send_danmu_msg_split_t,
                                                                          danmu_msg_word_num_max)
                                # print(101, send_danmu_msg_split_t_split)
                                for send_danmu_msg_split_t in send_danmu_msg_split_t_split[:-1]:
                                    send_danmu_msg_split_list.append(send_danmu_msg_split_t)
                                send_danmu_msg_split_t = send_danmu_msg_split_t_split[-1]
                                # print(111, send_danmu_msg_split_t)
                                danmu_msg_split_word_num = len(send_danmu_msg_split_t)
                                if danmu_msg_split_word_num == danmu_msg_word_num_max:
                                    danmu_msg_split_word_num = 0
                                    send_danmu_msg_split_list.append(send_danmu_msg_split_t)
                send_danmu_msg_split_list.append(send_danmu_msg_split_t)
                send_danmu_msg_split_list_dict.update({danmu_msg_word_num_max: send_danmu_msg_split_list})

        def send_danmu_msg_list():
            """
            发送弹幕
            :return:
            """
            global danmu_msg_list_num, send_danmu_msg_list_clock, \
                send_danmu_msg_split_list_dict, send_danmu_msg_word_num
            # pprint.pprint(send_danmu_msg_split_list_dict)
            if danmu_msg_list_num < len(send_danmu_msg_split_list_dict[send_danmu_msg_word_num]):
                send_danmu_msg_list_clock = True
                # 发送弹幕
                danmu_send_info = CsrfAuthenticationL(dict2cookieformat(cookies)).send(
                    int(SentRoom), send_danmu_msg_split_list_dict[send_danmu_msg_word_num][danmu_msg_list_num]
                )
                # 检测弹幕是否发送成功
                send_success = danmu_send_info['data']['mode_info']['user']['title']
                if send_success:
                    try:
                        DanMu_danmu_working_is = DanMu.danmu_working_is
                    except:
                        DanMu_danmu_working_is = False
                    if not DanMu_danmu_working_is:
                        obs.script_log(obs.LOG_INFO,
                                       f"弹幕发送成功：{send_danmu_msg_split_list_dict[send_danmu_msg_word_num][danmu_msg_list_num]}"
                                       )
                else:
                    obs.script_log(obs.LOG_INFO,
                                   f"弹幕发送失败：{send_danmu_msg_split_list_dict[send_danmu_msg_word_num][danmu_msg_list_num]}，{danmu_send_info['message']}"
                                   )
                if danmu_send_info['message'] == "超出限制长度":
                    if send_danmu_msg_word_num != 20:
                        send_danmu_msg_word_num -= 10
                        danmu_msg_list_num = 0
                    else:
                        danmu_msg_list_num += 1
                elif danmu_send_info['message'] == "您发送弹幕的频率过快":
                    pass
                elif danmu_send_info['message'] == "f":
                    erro_msg = send_danmu_msg_split_list_dict[send_danmu_msg_word_num][danmu_msg_list_num]
                    danmu_msg_list_nume = danmu_msg_list_num
                    danmu_msg_list_num = len(send_danmu_msg_split_list_dict[send_danmu_msg_word_num])
                    while danmu_msg_list_nume < len(send_danmu_msg_split_list_dict[send_danmu_msg_word_num]):
                        danmu_msg_list_nume += 1
                        if danmu_msg_list_nume < len(send_danmu_msg_split_list_dict[send_danmu_msg_word_num]) - 1:
                            erro_msg += send_danmu_msg_split_list_dict[send_danmu_msg_word_num][danmu_msg_list_nume]
                    cb.copy(erro_msg)
                else:
                    danmu_msg_list_num += 1
            else:
                send_danmu_msg_list_clock = False
                danmu_msg_list_num = 0
                send_danmu_msg_word_num = 40
                obs.remove_current_callback()

        # 当 输出弹幕计时器 未开启， 发送弹幕
        if not send_danmu_msg_list_clock:
            obs.timer_add(send_danmu_msg_list, 1000)
            # 清空 文本框【弹幕内容】 的内容
            obs.obs_data_set_string(current_settings, 'danmu_msg_text', "")

    if not obs.obs_property_list_item_count(SentRoom_list):
        obs.obs_data_set_string(current_settings, 'danmu_msg_text', "组合框【弹幕发送到】 无选项")

    return True


def correct_mask_word():
    correct_word = str(pypinyin.pinyin(cb.paste(), style=pypinyin.Style.TONE2))
    # obs.script_log(obs.LOG_INFO, correct_word)
    cb.copy(correct_word.replace("[", "").replace("]", "").replace(", ", "_").replace("'", ""))
    pass


def change_live_title(props, prop):
    live_title_text_value = obs.obs_data_get_string(current_settings, 'live_title_text')
    # 获取 '默认账户'cookie
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    turn_title_return = CsrfAuthenticationL(dict2cookieformat(cookies)).room_v1_Room_update(live_title_text_value)
    # print(turn_title_return)
    pass


def change_live_news(props, prop):
    live_news_text_value = obs.obs_data_get_string(current_settings, 'live_news_text')
    # 获取 '默认账户'cookie
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    turn_news_return = CsrfAuthenticationL(dict2cookieformat(cookies)).updateRoomNews(live_news_text_value)
    # print(turn_news_return)
    pass


def show_danmu(props, prop):
    global DanMu
    # 获取 '默认账户'cookie
    cookies = config_B(uid=0, dirname=scripts_data_dirpath).check()
    # # 获得 组合框[发出弹幕的用户]的内容
    # SentUid_list_value = obs.obs_data_get_string(current_settings, 'SentUid_list')
    # # 获取 [发出弹幕的用户]账户cookies
    # cookies = config_B(uid=int(SentUid_list_value), dirname=scripts_data_dirpath).check()
    # 获得 组合框【弹幕发送到】 的内容
    SentRoom = obs.obs_data_get_string(current_settings, 'SentRoom_list')

    def danmu_s():
        global DanMu
        DanMu = Danmu(dict2cookieformat(cookies)).connect_room(int(SentRoom))
        print(DanMu.danmu_start_is)
        DanMu.start()
    try:
        if DanMu.danmu_working_is:
            DanMu.danmu_start_is = False
            # 设置 按钮[登录] 可用状态
            obs.obs_property_set_enabled(login_button, True)
            # 更改 组合框【弹幕发送到】的可用性
            obs.obs_property_set_enabled(SentRoom_list, True)
        else:
            # 更改 组合框【弹幕发送到】的可用性
            obs.obs_property_set_enabled(SentRoom_list, False)
            # 设置 按钮[登录] 可用状态
            obs.obs_property_set_enabled(login_button, False)
            t1 = threading.Thread(target=danmu_s)
            t1.start()
    except:
        # 更改 组合框【弹幕发送到】的可用性
        obs.obs_property_set_enabled(SentRoom_list, False)
        # 设置 按钮[登录] 可用状态
        obs.obs_property_set_enabled(login_button, False)
        t1 = threading.Thread(target=danmu_s)
        t1.start()

    return True


def Blive_web(props, prop):
    pass


def script_unload():
    """
    在脚本被卸载时调用。
    """
    obs.script_log(obs.LOG_INFO, "已卸载：bilibili-live")
