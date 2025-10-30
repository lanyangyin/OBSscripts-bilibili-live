import asyncio
import datetime
import hashlib
import json
import os
import re
import struct
import threading
import time
import zlib
from collections import deque
from collections.abc import Callable
from pathlib import Path
from typing import Set, Optional, Union, Dict, Any

from PIL import Image

from function.api.Authentication.Wbi.get_danmu_info import WbiSigna
from function.api.Special.Get.get_user_live_info import BilibiliCSRFAuthenticator
from function.tools.EncodingConversion.parse_cookie import parse_cookie
from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.EncodingConversion.DanmuProtoDecoder import DanmuProtoDecoder
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager

import websockets


class DanmuWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.connected_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        self.danmu_processor = None

    async def register(self, websocket):
        """注册新的客户端连接"""
        self.connected_clients.add(websocket)
        print(f"新的网页客户端连接，当前连接数: {len(self.connected_clients)}")

        # 发送欢迎消息
        welcome_msg = {
            "type": "system",
            "message": "弹幕服务器连接成功",
            "timestamp": time.time(),
            "clients_count": len(self.connected_clients)
        }
        await websocket.send(json.dumps(welcome_msg))

    async def unregister(self, websocket):
        """移除断开连接的客户端"""
        self.connected_clients.remove(websocket)
        print(f"网页客户端断开，当前连接数: {len(self.connected_clients)}")

    async def broadcast_message(self, message: Dict[str, Any]):
        """向所有连接的客户端广播消息"""
        if not self.connected_clients:
            return

        message_json = json.dumps(message, ensure_ascii=False)

        # 使用 gather 并行发送消息
        disconnected_clients = []

        for client in self.connected_clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(client)

        # 移除断开连接的客户端
        for client in disconnected_clients:
            self.connected_clients.remove(client)

    async def handle_client(self, websocket):
        """处理客户端连接"""
        # path = websocket.path  # 从 websocket 对象中获取路径
        await self.register(websocket)
        try:
            # 保持连接，等待客户端消息
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_client_message(websocket, data)
                except json.JSONDecodeError:
                    error_msg = {
                        "type": "error",
                        "message": "无效的JSON格式",
                        "timestamp": time.time()
                    }
                    await websocket.send(json.dumps(error_msg))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def handle_client_message(self, websocket, data):
        """处理来自客户端的消息"""
        message_type = data.get("type")

        if message_type == "ping":
            # 响应 ping 消息
            pong_msg = {
                "type": "pong",
                "timestamp": time.time()
            }
            await websocket.send(json.dumps(pong_msg))
        elif message_type == "get_stats":
            # 返回服务器统计信息
            stats_msg = {
                "type": "stats",
                "clients_count": len(self.connected_clients),
                "timestamp": time.time()
            }
            await websocket.send(json.dumps(stats_msg))

    def send_danmu_message(self, danmu_data: Dict[str, Any]):
        """从弹幕处理线程发送消息（线程安全）"""
        if self.server_loop and self.server_loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self.broadcast_message(danmu_data),
                self.server_loop
            )

    def start_server(self):
        """启动 WebSocket 服务器"""

        async def start():
            self.server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port
            )
            print(f"弹幕转发服务器启动在 ws://{self.host}:{self.port}")

        self.server_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.server_loop)
        self.server_loop.run_until_complete(start())
        self.server_loop.run_forever()

    def stop_server(self):
        """停止服务器"""
        if self.server:
            self.server.close()
            if self.server_loop and self.server_loop.is_running():
                self.server_loop.stop()


# 全局 WebSocket 服务器实例
danmu_ws_server = DanmuWebSocketServer()


class Danmu:

    def __init__(self, headers: dict, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl
        self.cookie = headers['cookie']

    def _get_websocket_client(self, roomid: int):
        danmu_info = WbiSigna(self.headers, self.verify_ssl).get_danmu_info(roomid)
        token = danmu_info['data']['token']
        host = danmu_info['data']['host_list'][-1]
        wss_url = f"wss://{host['host']}:{host['wss_port']}/sub"

        user_info = BilibiliCSRFAuthenticator(self.headers, self.verify_ssl).get_user_live_info()['data']
        cookies = parse_cookie(self.cookie)
        auth_body = {
            "uid": user_info["uid"],
            "roomid": roomid,
            "protover": 2,
            "buvid": cookies['buvid3'],
            "platform": "web",
            "type": 3,
            "key": token
        }
        return wss_url, auth_body

    def connect_room(self, roomid: int):
        wss_url, auth_body = self._get_websocket_client(roomid)
        return self._WebSocketClient(wss_url, auth_body)

    class _WebSocketClient:
        HEARTBEAT_INTERVAL = 30
        """心跳间隔"""
        VERSION_NORMAL = 0
        """协议版本:0: 普通包 (正文不使用压缩)"""
        VERSION_ZIP = 2
        """协议版本:2: 普通包 (正文使用 zlib 压缩)"""
        VERSION_BTI = 3
        """协议版本:3: 普通包 (使用 brotli 压缩的多个带文件头的普通包)"""

        def __init__(self, url: str, auth_body: dict[str, Union[str, int]]):
            self.danmu_working_event = threading.Event()
            self.url = url
            self.auth_body = auth_body
            self.Callable_opt_code8: Callable[[str], None] = lambda a: a
            """接收认证包回复的回调函数"""
            self.Callable_opt_code5: Callable[[Dict[str, Any]], None] = lambda a: a
            """接收普通包 (命令)的回调函数"""
            self.wssCertificationAndHeartbeat: Callable[[bytes], None] = lambda a: a
            """发送认证包接收时的回调函数"""
            self.saved_danmu_data = deque(maxlen=1000)  # 固定大小队列
            self.message_hashes = set()  # 使用哈希去重
            """排除相同弹幕"""
            self.num_r = 20
            """同时连接多个弹幕减少丢包"""
            self.connection_threads = []  # 新增：管理所有连接线程
            self.running = False  # 新增：运行状态标志

        async def connect(self):
            retry_count = 0
            max_retries = 5
            base_delay = 3
            self.danmu_working_event.set()

            # 使用 running 标志而不是只依赖事件
            while self.running and self.danmu_working_event.is_set() and retry_count < max_retries:
                try:
                    async with websockets.connect(
                            self.url,
                            ping_interval=20,
                            ping_timeout=10,
                            close_timeout=10
                    ) as ws:
                        await self.on_open(ws)
                        retry_count = 0

                        while self.running and self.danmu_working_event.is_set():
                            try:
                                # 使用较短的超时时间，以便更频繁地检查停止信号
                                message = await asyncio.wait_for(ws.recv(), timeout=10.0)
                                await self.on_message(message)
                            except asyncio.TimeoutError:
                                # 检查是否应该停止
                                if not self.running:
                                    break
                                try:
                                    await ws.send(self.pack(None, 2))
                                except Exception:
                                    break
                            except websockets.exceptions.ConnectionClosed:
                                break

                except Exception as e:
                    if not self.running:  # 如果是主动停止，立即退出
                        break
                    retry_count += 1
                    delay = base_delay * (2 ** retry_count)
                    # 在等待期间也检查停止信号
                    for _ in range(int(delay * 10)):
                        if not self.running:
                            break
                        await asyncio.sleep(0.1)

        async def on_open(self, ws):
            """
            wss 认证和心跳
            Args:
                ws: wss 对象
            """
            try:
                # 先发送认证包
                await ws.send(self.pack(self.auth_body, 7))

                # 等待认证响应
                try:
                    auth_response: bytes = await asyncio.wait_for(ws.recv(), timeout=10)
                    """
                    16 字节 认证回复
                        [0:4]包总长度
                            (头部大小 + 正文大小)
                        [4:6]头部长度
                            (一般为 0x0010, 即 16 字节)
                        [6:8]协议版本
                            - 0: 普通包 (正文不使用压缩)
                            - 1: 心跳及认证包 (正文不使用压缩)
                            - 2: 普通包 (正文使用 zlib 压缩)
                            - 3: 普通包 (使用 brotli 压缩的多个带文件头的普通包)
                        [8:12]操作码
                            - 2	心跳包
                            - 3	心跳包回复 (人气值)
                            - 5	普通包 (命令)
                            - 7	认证包
                            - 8	认证包回复
                        [12:16]序列号
                        
                        [16:]正文内容
                    """
                    threading.Thread(self.wssCertificationAndHeartbeat(auth_response))
                    # 启动心跳任务
                    asyncio.create_task(self.send_heartbeat(ws))
                except asyncio.TimeoutError:
                    raise

            except Exception as e:
                raise

        async def send_heartbeat(self, ws):
            """发送心跳"""
            while self.running and self.danmu_working_event.is_set():
                try:
                    await ws.send(self.pack(None, 2))
                    # 使用更短的心跳间隔检查停止信号
                    for _ in range(30):  # 30 * 0.1 = 3秒
                        if not self.running:
                            return
                        await asyncio.sleep(0.1)
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    break

        async def on_message(self, message):
            if isinstance(message, bytes):
                threading.Thread(self.unpack(message)).start()

        def pack(self, content: Optional[dict], code: int) -> bytes:
            """
            wss 消息打包
            Args:
                content: 消息内容
                code:
                    操作码 (封包类型)

                        - 2	心跳包
                        - 3	心跳包回复 (人气值)
                        - 5	普通包 (命令)
                        - 7	认证包
                        - 8	认证包回复


            Returns:打包后待发送的 wss 消息

            """
            content_bytes = json.dumps(content).encode('utf-8') if content else b''
            header = (len(content_bytes) + 16).to_bytes(4, 'big') + \
                     (16).to_bytes(2, 'big') + \
                     self.VERSION_NORMAL.to_bytes(2, 'big') + \
                     code.to_bytes(4, 'big') + \
                     (1).to_bytes(4, 'big')
            return header + content_bytes

        def unpack(self, byte_buffer: bytes):
            # 头部格式:
            package_len = int.from_bytes(byte_buffer[0:4], 'big')
            """
            封包总大小 (头部大小 + 正文大小)
            """
            head_length = int.from_bytes(byte_buffer[4:6], 'big')
            """
            头部大小 (一般为 0x0010, 即 16 字节)
            """
            prot_ver = int.from_bytes(byte_buffer[6:8], 'big')
            """
            协议版本:
                - 0: 普通包 (正文不使用压缩)
                - 1: 心跳及认证包 (正文不使用压缩)
                - 2: 普通包 (正文使用 zlib 压缩)
                - 3: 普通包 (使用 brotli 压缩的多个带文件头的普通包)
            """
            opt_code = int.from_bytes(byte_buffer[8:12], 'big')
            """
            操作码 (封包类型)
                - 2	心跳包
                - 3	心跳包回复 (人气值)
                - 5	普通包 (命令)
                - 7	认证包
                - 8	认证包回复
            """
            sequence = int.from_bytes(byte_buffer[12:16], 'big')
            """
            sequence, 每次发包时向上递增
            """

            content_bytes = byte_buffer[16:package_len]

            # print(f"头部长度: {head_length} 字节")
            if prot_ver == self.VERSION_NORMAL:
                pass
            elif prot_ver == self.VERSION_ZIP:
                content_bytes = zlib.decompress(content_bytes)
                thread = threading.Thread(target=self.unpack, args=(content_bytes,))
                thread.daemon = True  # 设置为守护线程
                thread.start()
                return
            elif prot_ver == self.VERSION_BTI:
                pass

            # print(f"序列号: {sequence}")

            content = content_bytes.decode('utf-8')
            content_hash = hashlib.md5(content.encode()).hexdigest()
            if content_hash in self.message_hashes:
                return  # 快速去重

            self.message_hashes.add(content_hash)
            if len(self.message_hashes) > 10000:  # 定期清理
                self.message_hashes.clear()

            if opt_code == 5:  # SEND_SMS_REPLY
                content_dict: dict = json.loads(content)
                if content_dict['cmd'] == "INTERACT_WORD_V2":
                    content_dict['data'] = DanmuProtoDecoder().decode_interact_word_v2_protobuf(
                        content_dict['data']['pb'])
                elif content_dict['cmd'] == "ONLINE_RANK_V3":
                    content_dict['data'] = DanmuProtoDecoder().decode_online_rank_v3_protobuf(
                        content_dict['data']['pb'])
                thread = threading.Thread(target=self.Callable_opt_code5, args=(content_dict,))
                thread.daemon = True
                thread.start()
                pass
            elif opt_code == 8:  # AUTH_REPLY
                self.Callable_opt_code8(content)
                pass

            if len(byte_buffer) > package_len:
                thread = threading.Thread(target=self.unpack, args=(byte_buffer[package_len:],))
                thread.daemon = True
                thread.start()

        def start(self):
            try:
                self.running = True  # 设置运行状态
                self.connection_threads.clear()  # 清空线程列表

                def connection_task():
                    asyncio.run(self.connect())

                for i in range(self.num_r):
                    thread = threading.Thread(target=connection_task, name=f"DanmuConn-{i}")
                    thread.daemon = True  # 设置为守护线程
                    self.connection_threads.append(thread)
                    thread.start()
                    time.sleep(1)

            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                self.stop()

        def stop(self):
            """优雅停止连接"""
            self.running = False  # 设置停止标志
            self.danmu_working_event.clear()  # 清除事件

            # 等待所有线程结束，设置超时时间
            for thread in self.connection_threads:
                if thread.is_alive():
                    thread.join(timeout=2.0)  # 最多等待2秒


if __name__ == "__main__":
    from _Input.functions.DanMu import Danmu as Dm
    from function.tools.EncodingConversion.url2pillow_image import url2pillow_image
    import signal
    import sys


    # 在 main 部分添加
    def signal_handler(signum, frame):
        print("\n正在停止弹幕连接和WebSocket服务器...")
        cdm.stop()
        danmu_ws_server.stop_server()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)

    # 启动 WebSocket 服务器
    ws_thread = threading.Thread(target=danmu_ws_server.start_server, daemon=True)
    ws_thread.start()
    print("WebSocket 服务器启动中...")
    time.sleep(2)  # 等待服务器启动

    BULC = BilibiliUserConfigManager(Path('../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    dm = Danmu(Headers)
    cdm = dm.connect_room(Dm.room_id)
    cdm.num_r = 30


    def reply_with_a_callback_after_verification(auth_response: bytes):
        """

        Args:
            auth_response:
                16 字节 认证回复

                    [0:4]包总长度
                        (头部大小 + 正文大小)
                    [4:6]头部长度
                        (一般为 0x0010, 即 16 字节)
                    [6:8]协议版本
                        - 0: 普通包 (正文不使用压缩)
                        - 1: 心跳及认证包 (正文不使用压缩)
                        - 2: 普通包 (正文使用 zlib 压缩)
                        - 3: 普通包 (使用 brotli 压缩的多个带文件头的普通包)
                    [8:12]操作码
                        - 2	心跳包
                        - 3	心跳包回复 (人气值)
                        - 5	普通包 (命令)
                        - 7	认证包
                        - 8	认证包回复
                    [12:16]序列号

                    [16:]正文内容
        Returns:

        """
        print(f"认证成功，连接已建立")
        # 解析头部 (16 字节)
        package_len = struct.unpack('>I', auth_response[0:4])[0]  # 包总长度
        head_length = struct.unpack('>H', auth_response[4:6])[0]  # 头部长度
        prot_ver = struct.unpack('>H', auth_response[6:8])[0]  # 协议版本
        opt_code = struct.unpack('>I', auth_response[8:12])[0]  # 操作码
        sequence = struct.unpack('>I', auth_response[12:16])[0]  # 序列号

        # 解析正文
        content_bytes: bytes = auth_response[16:package_len]  # 正文
        content_str = content_bytes.decode('utf-8')

        print(f"包总长度: {package_len} 字节\t头部长度: {head_length} 字节\t协议版本: {prot_ver}\t操作码: {opt_code} (8 = 认证回复)\t序列号: {sequence}\t正文内容: {content_str}\t")


    cdm.wssCertificationAndHeartbeat = reply_with_a_callback_after_verification


    def authentication_package_reply_processing(content: str):
        print(f"身份验证回复: {content}\n")


    cdm.Callable_opt_code8 = authentication_package_reply_processing


    def danmu_processing(content: dict):
        if content['cmd'] == "LIVE":
            # 直播开始 (LIVE)
            contentdata = content
            roomid = contentdata['roomid']
            if 'live_time' in contentdata:
                live_time = contentdata['live_time']
                live_platform = contentdata['live_platform']

                print(f'🔴直播开始：房间{roomid} 时间{live_time} 平台[{live_platform}]')
                # 转发到 WebSocket
                danmu_ws_server.send_danmu_message({
                    "type": "live_start",
                    "roomid": roomid,
                    "live_time": live_time,
                    "live_platform": live_platform,
                    "timestamp": time.time()
                })

        elif content['cmd'] == "LIKE_INFO_V3_UPDATE":
            # 直播间点赞数更新 (LIKE_INFO_V3_UPDATE)
            contentdata = content['data']
            print(f"👍🔢点赞数：\t{contentdata['click_count']}")
            pass
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "like_update",
                "click_count": contentdata['click_count'],
                "timestamp": time.time()
            })

        elif content['cmd'] == "ONLINE_RANK_COUNT":
            contentdata = content['data']
            print(f"🧑🔢高能用户数：\t{contentdata['count']}")
            pass
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "online_rank_count",
                "count": contentdata['count'],
                "timestamp": time.time()
            })

        elif content['cmd'] == "WATCHED_CHANGE":
            contentdata = content['data']
            print(f"👀🔢直播间看过人数：\t{contentdata['num']}|\t{contentdata['text_large']}")
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "watched_change",
                "num": contentdata['num'],
                "text_large": contentdata['text_large'],
                "timestamp": time.time()
            })
            pass

        elif content['cmd'] == "POPULAR_RANK_CHANGED":
            contentdata = content['data']
            # 排名信息
            rank = contentdata['rank']
            uid = contentdata['uid']
            rank_name = contentdata['rank_name_by_type']
            on_rank_name = contentdata['on_rank_name_by_type']

            # 格式化排名显示
            rank_display = f"第{rank}名" if rank > 0 else "未上榜"

            print(f'🏆排名变化：{on_rank_name}{rank_name} {rank_display} 主播{uid}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "popular_rank_changed",
                "rank": rank,
                "uid": uid,
                "rank_name": rank_name,
                "on_rank_name": on_rank_name,
                "message": f"{on_rank_name}{rank_name} {rank_display}",
                "timestamp": time.time()
            })

        elif content['cmd'] == "SUPER_CHAT_MESSAGE":
            contentdata = content['data']
            # 用户信息
            uname = contentdata['user_info']['uname']
            uid = contentdata['uid']
            price = contentdata['price']
            message = contentdata['message']
            duration = contentdata['time']

            # 粉丝牌信息
            medal_info = contentdata['medal_info']
            mfo = ""
            if medal_info['medal_name']:
                mfo = f"【{medal_info['medal_name']}|{medal_info['medal_level']}】"

            print(f'💬醒目留言：{mfo}{uname}({uid}) {price}元 {duration}秒 "{message}"')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "super_chat",
                "user": uname,
                "uid": uid,
                "medal": mfo,
                "price": price,
                "message": message,
                "duration": duration,
                "timestamp": time.time()
            })

        elif content['cmd'] == "SUPER_CHAT_MESSAGE_DELETE":
            contentdata = content['data']
            # 删除的SC ID列表
            ids = contentdata['ids']
            ids_str = "、".join(str(sc_id) for sc_id in ids)

            print(f'🗑️醒目留言删除：SC[{ids_str}]')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "super_chat_delete",
                "ids": ids,
                "message": f"SC[{ids_str}]",
                "timestamp": time.time()
            })

        elif content['cmd'] == "DANMU_MSG":
            # 弹幕 (DANMU_MSG)
            contentinfo = content['info']
            danmu_extra = json.loads(contentinfo[0][15]['extra'])
            """弹幕额外信息"""

            is_housing_management = contentinfo[2][2]
            """是不是直播间管理员"""

            danmu_extra_emots = danmu_extra['emots']
            """表情相关信息"""

            expression_information = contentinfo[0][13]
            """表情信息，没有时为‘{}’"""
            if expression_information != "{}":
                expression_url = expression_information["url"]
                """表情图片url"""
                expression_emoticon_unique = expression_information["emoticon_unique"]
                """表情特殊昵称"""
                expression_height = expression_information["height"]
                """表情图片高度"""
                expression_width = expression_information["width"]
                """表情图片宽度"""

            reply_uname = danmu_extra['reply_uname']
            """@对象的昵称"""
            reply_uname_color = danmu_extra['reply_uname_color']
            """@对象的昵称在弹幕中的颜色"""

            damu_text = contentinfo[1]
            """弹幕文本"""

            own_big_expression = {}
            """自定义的大图片的名称和位置"""
            pattern = r'(\[.*?\])'
            emoji_name_text_separation_list = [emoji_name_text_separation for emoji_name_text_separation in re.split(pattern, damu_text) if emoji_name_text_separation]
            """分离的带‘[]’的表情名称和普通文本"""
            message_list = []
            """弹幕消息格式化成的列表"""
            if reply_uname:
                afo = f"@{reply_uname}  "
                message_list.append({
                    'type': 'text',
                    'color': reply_uname_color,
                    'text': afo
                })
            for emoji_name_text_separation in emoji_name_text_separation_list:
                if expression_information != "{}":  # 大表情
                    file_path = f"./blivechat_files/{expression_information['emoticon_unique']}.png"
                    if not os.path.exists(file_path):
                        pillow_img = url2pillow_image(expression_information["url"], Headers)["PilImg"]
                        pillow_img.save(file_path)
                    else:
                        pillow_img = Image.open(file_path)
                    width, height = pillow_img.size
                    message_list.append({
                        'type': 'image',
                        'height': height,
                        'width': width,
                        'src': file_path
                    })
                    continue
                # 检查是否是表情
                if emoji_name_text_separation.startswith('[') and emoji_name_text_separation.endswith(']'):
                    if emoji_name_text_separation in danmu_extra_emots:  # 小表情
                        file_path = f"./blivechat_files/{danmu_extra_emots[emoji_name_text_separation]['emoticon_unique']}.png"
                        if not os.path.exists(file_path):
                            pillow_img = url2pillow_image(danmu_extra_emots[emoji_name_text_separation]['url'], Headers)["PilImg"]
                            pillow_img.save(file_path)
                        message_list.append({
                            'type': 'emoji',
                            'alt': emoji_name_text_separation,
                            'src': file_path
                        })
                        continue

                if own_big_expression:
                    pattern = r'(' + '|'.join([re.escape(sep) for sep in list(own_big_expression.keys())]) + ')'
                    parts = re.split(pattern, emoji_name_text_separation)
                    for own_big_expression_name_text_separation in [part for part in parts if part]:
                        if own_big_expression_name_text_separation in own_big_expression:
                            message_list.append({
                                'type': 'image',
                                'src': own_big_expression[own_big_expression_name_text_separation]
                            })
                        else:
                            # 普通文本
                            message_list.append({
                                'type': 'text',
                                'text': emoji_name_text_separation
                            })
                else:
                    # 普通文本
                    message_list.append({
                        'type': 'text',
                        'text': emoji_name_text_separation
                    })

            wealth_level = contentinfo[16][0]
            """消费等级"""
            file_path = f'./blivechat_files/{re.split("/", contentinfo[0][15]["user"]["base"]["face"])[-1]}'
            if not os.path.exists(file_path):
                pillow_img = url2pillow_image(contentinfo[0][15]["user"]["base"]["face"], Headers)["PilImg"]
                pillow_img.save(file_path)
            face_url = file_path
            """头像图片url"""
            uname = contentinfo[0][15]["user"]['base']["name"]
            """发送者昵称"""
            medal = contentinfo[0][15]["user"]['medal']
            """勋章基础信息"""
            guard_level = 0
            guard_icon = ""
            if medal:
                guard_level = medal['guard_level']
                """舰长等级"""
                guard_icon = medal['guard_icon']
                """舰长勋章图标url"""
                medal_is_light = medal["is_light"]
                """粉丝勋章点亮状态"""
                fans_medal_name = medal["name"]
                """粉丝勋章名称"""
                fans_medal_level = medal["level"]
                """粉丝勋章等级0.普通 1.总督 2.提督 3，舰长"""
                fans_medal_from_uid = medal["ruid"]
                """粉丝勋章创建者id"""
                fans_medal_id = medal["id"]
                """粉丝勋章id"""
                fans_medal_color_start = medal["v2_medal_color_start"]
                """粉丝勋章开始颜色"""
                fans_medal_color_end = medal["v2_medal_color_end"]
                """粉丝勋章结束颜色"""
                fans_medal_color_border = medal["v2_medal_color_border"]
                """粉丝勋章边框颜色"""
                fans_medal_color_text = medal["v2_medal_color_text"]
                """粉丝勋章文本色"""
                fans_medal_color_level = medal["v2_medal_color_level"]
                """粉丝勋章等级颜色"""
            if contentinfo[3]:
                guard_level = contentinfo[3][10]
            if guard_icon:
                file_path = f'./blivechat_files/{re.split("/", guard_icon)[-1]}'
                if not os.path.exists(file_path):
                    pillow_img = url2pillow_image(guard_icon, Headers)["PilImg"]
                    pillow_img.save(file_path)
                guard_icon = file_path

            fans_medal = contentinfo[3]
            """勋章信息列表，没有的话为空"""
            fans_medal_from_uname = ""
            """粉丝勋章创建者昵称"""
            if fans_medal:
                fans_medal_from_uname = contentinfo[3][2]

            send_time = contentinfo[9]['ts']
            """弹幕发送时间戳"""
            wfo = ''
            if wealth_level != 0:
                wfo = f"[{wealth_level}]"

            mfo = ''
            # if contentinfo[0][15]['user']['medal']:
            #     fmedal = contentinfo[0][15]['user']['medal']
            #     mfo = f"【{fmedal['name']}|{fmedal['level']}】"
            if contentinfo[3]:
                medal = contentinfo[3]
                mfo = f"【{medal[1]}|{medal[0]}】"

            afo = ""
            if reply_uname:
                afo = f"@{reply_uname}  "

            tfo = damu_text

            print(f"{wfo}{mfo}{uname}:\n\t>>>{afo}{tfo}")
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "danmu",
                "authorType": "moderator" if contentinfo[2][2] else "member" if guard_level else "",
                "message_list": message_list,
                "user": uname,
                "face": face_url,
                "guard_level": guard_level,
                "guard_icon": guard_icon,
                "medal": mfo,
                "wealth": wfo,
                "content": tfo,
                "reply_to": afo.strip(),
                "timestamp": send_time
            })

        elif content['cmd'] == "COMBO_SEND":
            contentdata = content['data']
            ufo = contentdata['uname']
            mfo = ""
            if contentdata['medal_info']['medal_name']:
                medali = contentdata['medal_info']
                mfo = f"【{medali['medal_name']}|{medali['medal_level']}】"
            wfo = ''
            if contentdata['wealth_level'] != 0:
                wfo = f"[{contentdata['wealth_level']}]"
            tfo = f""
            tfo += contentdata['action']
            coin = f"{contentdata['combo_total_coin'] / 1000}￥"
            tfo += f"{contentdata['batch_combo_num']}个《{contentdata['gift_name']}》\t{coin}"
            print(f'⛓🎁连续礼物：{wfo}{mfo}{ufo}\t{tfo}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "combo_gift",
                "user": ufo,
                "medal": mfo,
                "wealth": wfo,
                "gift_name": contentdata['gift_name'],
                "combo_num": contentdata['batch_combo_num'],
                "total_coin": contentdata['combo_total_coin'],
                "message": tfo,
                "timestamp": time.time()
            })

        elif content['cmd'] == "GUARD_BUY":
            # 上舰通知 (GUARD_BUY)
            contentdata = content['data']
            tfo = f"🚢上舰：\t{contentdata['username']}\t购买{contentdata['num']}个\t【{contentdata['gift_name']}】"
            print(f"{tfo}")
            pass
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "guard_buy",
                "user": contentdata['username'],
                "guard_name": contentdata['gift_name'],
                "guard_count": contentdata['num'],
                "price": contentdata['price'],
                "message": tfo,
                "timestamp": time.time()
            })

        elif content['cmd'] == "INTERACT_WORD_V2":
            # 用户交互消息【Proto格式】
            contentdata = content['data']
            tfo = "❓进入直播间或关注消息或分享直播间"
            if contentdata['msg_type'] == 1:
                tfo = "🏠进入直播间"
            elif contentdata['msg_type'] == 2:
                tfo = "⭐关注直播间"
            elif contentdata['msg_type'] == 2:
                tfo = "💫分享直播间"
            ufo = contentdata['uname']
            mfo = ""
            if contentdata['fans_medal']:
                fmedal = contentdata['fans_medal']
                mfo = f"【{fmedal['medal_name']}|{fmedal['medal_level']}】"
            wfo = ''
            try:
                if content['data']['uinfo']['wealth']['level']:
                    wfo = f"[{content['data']['uinfo']['wealth']['level']}]"
            except:
                pass
            pass
            print(f"{tfo}：\t{wfo}{mfo}{ufo}")
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "interact",
                "user": ufo,
                "medal": mfo,
                "wealth": wfo,
                "action": tfo,
                "msg_type": contentdata['msg_type'],
                "timestamp": time.time()
            })

        elif content['cmd'] == "LIKE_INFO_V3_CLICK":
            # 直播间用户点赞 (LIKE_INFO_V3_CLICK)
            contentdata = content['data']
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
            print(f"👍点赞：\t{wfo}{mfo}{ufo}\t{tfo}")
            pass
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "like_click",
                "user": ufo,
                "medal": mfo,
                "wealth": wfo,
                "like_text": tfo,
                "timestamp": time.time()
            })

        elif content['cmd'] == "POPULARITY_RED_POCKET_NEW":
            contentdata = content['data']
            ufo = contentdata['uname']
            mfo = ""
            if contentdata['medal_info']['medal_name']:
                medali = contentdata['medal_info']
                mfo = f"【{medali['medal_name']}|{medali['medal_level']}】"
            wfo = ''
            if contentdata['wealth_level'] != 0:
                wfo = f"[{contentdata['wealth_level']}]"
            tfo = ''
            tfo += contentdata['action']
            coin = contentdata['price'] / 10
            tfo += f"\t{coin}"
            print(f'🔖红包：\t{wfo}{mfo}{ufo}\t{tfo}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "red_pocket",
                "user": ufo,
                "medal": mfo,
                "wealth": wfo,
                "action": contentdata['action'],
                "price": coin,
                "message": tfo,
                "timestamp": time.time()
            })

        elif content['cmd'] == "POPULARITY_RED_POCKET_V2_NEW":
            contentdata = content['data']
            ufo = contentdata['uname']
            mfo = ""
            if contentdata['medal_info']['medal_name']:
                medali = contentdata['medal_info']
                mfo = f"【{medali['medal_name']}|{medali['medal_level']}】"
            wfo = ''
            if contentdata['wealth_level'] != 0:
                wfo = f"[{contentdata['wealth_level']}]"
            tfo = ''
            tfo += contentdata['action']
            coin = contentdata['price'] / 10
            tfo += f"\t{coin}"
            print(f'🔖红包：\t{wfo}{mfo}{ufo}\t{tfo}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "red_pocket_v2",
                "user": ufo,
                "medal": mfo,
                "wealth": wfo,
                "action": contentdata['action'],
                "price": coin,
                "message": tfo,
                "timestamp": time.time()
            })

        elif content['cmd'] == "POPULARITY_RED_POCKET_V2_WINNER_LIST":
            contentdata = content['data']

            # 红包信息
            lot_id = contentdata['lot_id']
            total_num = contentdata['total_num']

            # 中奖用户信息
            winner_list = []
            for winner in contentdata['winner_info']:
                user_mid = winner[0]
                user_name = winner[1]
                gift_id = winner[3]

                # 获取礼物信息
                gift_info = contentdata['awards'].get(str(gift_id), {})
                gift_name = gift_info.get('award_name', '未知礼物')
                gift_price = gift_info.get('award_price', 0)

                winner_info = f"{user_name}({user_mid})获得[{gift_name}]({gift_price / 1000}￥)"
                winner_list.append(winner_info)

            display_winners = winner_list
            winners_str = "、".join(display_winners)

            print(f'🧧红包中奖：红包{lot_id} 共{total_num}个礼物 {winners_str}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "red_pocket_winners",
                "lot_id": lot_id,
                "total_num": total_num,
                "winners": winner_list,
                "message": f"红包{lot_id} 共{total_num}个礼物 {winners_str}",
                "timestamp": time.time()
            })

        elif content['cmd'] == "POPULARITY_RED_POCKET_WINNER_LIST":
            contentdata = content['data']

            # 红包信息
            lot_id = contentdata['lot_id']
            total_num = contentdata['total_num']

            # 中奖用户信息
            winner_list = []
            for winner in contentdata['winner_info']:
                user_mid = winner[0]
                user_name = winner[1]
                gift_id = winner[3]

                # 获取礼物信息
                gift_info = contentdata['awards'].get(str(gift_id), {})
                gift_name = gift_info.get('award_name', '未知礼物')
                gift_price = gift_info.get('award_price', 0)

                winner_info = f"{user_name}({user_mid})获得[{gift_name}]({gift_price / 1000}￥)"
                winner_list.append(winner_info)

            display_winners = winner_list
            winners_str = "、".join(display_winners)

            print(f'🧧红包中奖：红包{lot_id} 共{total_num}个礼物 {winners_str}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "red_pocket_winners",
                "lot_id": lot_id,
                "total_num": total_num,
                "winners": winner_list,
                "message": f"红包{lot_id} 共{total_num}个礼物 {winners_str}",
                "timestamp": time.time()
            })

        elif content['cmd'] == "SEND_GIFT":
            # 送礼 (SEND_GIFT)
            contentdata = content['data']
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
            print(f'🎁礼物：\t{wfo}{mfo}{ufo}\t{tfo}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "gift",
                "user": ufo,
                "medal": mfo,
                "wealth": wfo,
                "gift_name": contentdata.get('giftName', ''),
                "gift_count": contentdata['num'],
                "total_coin": contentdata['total_coin'],
                "message": tfo,
                "timestamp": time.time()
            })

        elif content['cmd'] == "SUPER_CHAT_MESSAGE_JPN":
            contentdata = content['data']

            # 用户信息
            uname = contentdata['user_info']['uname']
            uid = contentdata['uid']
            price = contentdata['price']
            message = contentdata['message']
            duration = contentdata['time']

            # 粉丝牌信息
            medal_info = contentdata['medal_info']
            mfo = ""
            if medal_info['medal_name']:
                mfo = f"【{medal_info['medal_name']}|{medal_info['medal_level']}】"

            print(f'💬🗾醒目留言：{mfo}{uname}({uid}) {price}元 {duration}秒 "{message}"')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "super_chat_jpn",
                "user": uname,
                "uid": uid,
                "medal": mfo,
                "price": price,
                "message": message,
                "duration": duration,
                "timestamp": time.time()
            })

        elif content['cmd'] == "USER_TOAST_MSG":
            contentdata = content['data']

            # 用户信息
            username = contentdata['username']
            uid = contentdata['uid']
            guard_level = contentdata['guard_level']
            role_name = contentdata['role_name']
            price = contentdata['price'] / 1000  # 转换为元
            unit = contentdata['unit']

            # 格式化大航海等级显示
            guard_map = {1: "总督", 2: "提督", 3: "舰长"}
            guard_name = guard_map.get(guard_level, f"未知({guard_level})")

            print(f'🚢大航海：{username}({uid}) 开通{guard_name} {price}元/{unit}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "user_toast",
                "user": username,
                "uid": uid,
                "guard_level": guard_level,
                "guard_name": guard_name,
                "price": price,
                "unit": unit,
                "message": f"{username}开通{guard_name} {price}元/{unit}",
                "timestamp": time.time()
            })

        elif content['cmd'] == "USER_TOAST_MSG_V2":
            contentdata = content['data']

            # 用户信息
            username = contentdata['sender_uinfo']['base']['name']
            uid = contentdata['sender_uinfo']['uid']
            guard_level = contentdata['guard_info']['guard_level']
            role_name = contentdata['guard_info']['role_name']
            price = contentdata['pay_info']['price'] / 1000  # 转换为元
            unit = contentdata['pay_info']['unit']

            # 格式化大航海等级显示
            guard_map = {1: "总督", 2: "提督", 3: "舰长"}
            guard_name = guard_map.get(guard_level, f"未知({guard_level})")

            print(f'🚢大航海：{username}({uid}) 开通{guard_name} {price}元/{unit}')
            # 转发到 WebSocket
            danmu_ws_server.send_danmu_message({
                "type": "user_toast_v2",
                "user": username,
                "uid": uid,
                "guard_level": guard_level,
                "guard_name": guard_name,
                "price": price,
                "unit": unit,
                "message": f"{username}开通{guard_name} {price}元/{unit}",
                "timestamp": time.time()
            })

        elif content['cmd'] == "COMMON_NOTICE_DANMAKU":
            # 广播通知弹幕信息
            pass

        elif content['cmd'] == "DM_INTERACTION":
            # 交互信息合并 (DM_INTERACTION)
            contentdata = content['data']
            contentdata['data'] = json.loads(contentdata['data'])
            tfo = f"❓连续发送弹幕或点赞{contentdata['type']}"
            if contentdata['type'] == 101:
                tfo = f"⛓🍭连续投票：\t{contentdata['data']['result_text']}"
            elif contentdata['type'] == 102:
                tfo = ""
                for contentdatacombo in contentdata['data']['combo'][:-1]:
                    tfo += f"热词：\t{contentdatacombo['cnt']}\t人{contentdatacombo['guide']}{contentdatacombo['content']}\n"
                tfo += f"⛓🔠连续弹幕：\t{contentdata['data']['combo'][-1]['cnt']}\t人{contentdata['data']['combo'][-1]['guide']}{contentdata['data']['combo'][-1]['content']}"
            elif contentdata['type'] == 103:
                tfo = f"⛓⭐连续关注：\t{contentdata['data']['cnt']}\t{contentdata['data']['suffix_text']}"
            elif contentdata['type'] == 105:
                tfo = f"⛓💫连续分享：\t{contentdata['data']['cnt']}\t{contentdata['data']['suffix_text']}"
            elif contentdata['type'] == 106:
                tfo = f"⛓👍连续点赞：\t{contentdata['data']['cnt']}\t{contentdata['data']['suffix_text']}"
            print(f"{tfo}")
            pass

        elif content['cmd'] == "ENTRY_EFFECT":
            # # 用户进场特效 (ENTRY_EFFECT)
            # # 注: 有进场特效的用户进入直播间
            # contentdata = content['data']
            # print(contentdata)
            pass

        elif content['cmd'] == "ENTRY_EFFECT_MUST_RECEIVE":
            # # 必须接受的用户进场特效 (ENTRY_EFFECT_MUST_RECEIVE)
            # # 注: 在部分主播进入自己的直播间时下发。
            # contentdata = content['data']
            # print(contentdata)
            pass

        elif content['cmd'] == "HOT_ROOM_NOTIFY":
            contentdata = content['data']
            tfo = ""
            if contentdata["exit_no_refresh"]:
                tfo += f"退出不刷新"
            else:
                tfo += f"退出刷新"
            print(f"{tfo}")

        elif content['cmd'] == "INTERACT_WORD":
            # # 用户交互消息(INTERACT_WORD)
            # # 注: 有用户进入直播间、关注主播、分享直播间时触发
            # contentdata = content['data']
            # tfo = "❓进入直播间或关注消息"
            # if contentdata['msg_type'] == 1:
            #     tfo = "🏠进入直播间"
            # elif contentdata['msg_type'] == 2:
            #     tfo = "⭐关注直播间"
            # ufo = contentdata['uname']
            # mfo = ""
            # if contentdata['fans_medal']:
            #     fmedal = contentdata['fans_medal']
            #     mfo = f"【{fmedal['medal_name']}|{fmedal['medal_level']}】"
            # wfo = ''
            # try:
            #     if content['data']['uinfo']['wealth']['level']:
            #         wfo = f"[{content['data']['uinfo']['wealth']['level']}]"
            # except:
            #     pass
            # print(f"{tfo}：\t{wfo}{mfo}{ufo}")
            pass

        elif content['cmd'] == "LIKE_INFO_V3_NOTICE":
            # # 通知消息
            # contentdata = content['content_segments'] ['data']
            # content_segments_font_color = contentdata['content_segments'] ['font_color']
            # content_segments_text = contentdata['content_segments'] ['text']
            # content_segments_type = contentdata['content_segments'] ['type']
            # print(content_segments_font_color, content_segments_text, content_segments_type)
            pass

        elif content['cmd'] == "LIVE_ROOM_TOAST_MESSAGE":
            # # ?视频连线
            # contentdata = content['data']
            # print(contentdata)
            pass

        elif content['cmd'] == "master_qn_strategy_chg":
            # # ???
            # contentdata = content['data']  # 字符串'{"mtime":1758875819,"scatter":[0,300]}'
            # contentdata = json.loads(contentdata)
            # mtime = contentdata["mtime"]
            # """
            # ?
            # """
            # scatter = contentdata["scatter"]
            # """
            # ?
            # """
            # print(mtime, scatter)
            pass

        elif content['cmd'] == "MESSAGEBOX_USER_GAIN_MEDAL":
            # # 获得粉丝勋章 (MESSAGEBOX_USER_GAIN_MEDAL)
            # # 获得时下发。
            # contentdata = content['data']
            # print(contentdata)
            pass

        elif content['cmd'] == "MESSAGEBOX_USER_MEDAL_CHANGE":
            # # 粉丝勋章更新 (MESSAGEBOX_USER_MEDAL_CHANGE)
            # # 升级或点亮时下发
            # contentdata = content['data']
            # print(contentdata)
            pass

        elif content['cmd'] == "NOTICE_MSG":
            # # 通知消息
            # contentdata = content
            # print(contentdata)
            pass

        elif content['cmd'] == "ONLINE_RANK_V2":
            # # 直播间高能榜(ONLINE_RANK_V2)
            # # 注: 直播间高能用户数据刷新
            # contentdata = content['data']
            # high_energy_users_in_the_live_streaming_room_list = contentdata["list"]
            # """
            # 在直播间高能用户中的用户信息
            # """
            # rank_type = contentdata["rank_type"]
            # """
            # 待调查
            # """
            # print(high_energy_users_in_the_live_streaming_room_list, rank_type)
            pass

        elif content['cmd'] == "ONLINE_RANK_V3":
            # # 直播间高能用户相关【Proto格式】
            # contentdata = content['data']
            # # # print(contentdata['pb'])
            # # contentdata = DanmuProtoDecoder().decode_online_rank_v3_protobuf(contentdata['pb'])
            # try:
            #     high_energy_users_in_the_live_streaming_room_list = contentdata["list"]
            #     """
            #     在直播间高能用户中的用户信息
            #     """
            #     rank_type = contentdata["rank_type"]
            #     """
            #     待调查
            #     """
            #     print("📖", high_energy_users_in_the_live_streaming_room_list, rank_type)
            # except:
            #     print(contentdata)
            pass

        elif content['cmd'] == "PLAYURL_RELOAD":
            # contentdata = content['data']
            # playurldata = contentdata['playurl']
            #
            # # 基本信息
            # room_id = contentdata['room_id']
            # cid = playurldata['cid']
            #
            # # 流媒体协议和质量信息
            # protocol_list = []
            # for stream in playurldata['stream']:
            #     protocol_name = stream['protocol_name']
            #
            #     formats_info = []
            #     for fmt in stream['format']:
            #         format_name = fmt['format_name']
            #
            #         # 获取支持的画质
            #         quality_codes = []
            #         for codec in fmt['codec']:
            #             quality_codes.extend(codec['accept_qn'])
            #
            #         # 将质量代码转换为描述
            #         quality_descs = []
            #         for qn in set(quality_codes):  # 去重
            #             for quality in playurldata['g_qn_desc']:
            #                 if quality['qn'] == qn:
            #                     quality_descs.append(quality['desc'])
            #                     break
            #
            #         format_info = f"{format_name}({','.join(quality_descs)})"
            #         formats_info.append(format_info)
            #
            #     protocol_info = f"{protocol_name}[{';'.join(formats_info)}]"
            #     protocol_list.append(protocol_info)
            #
            # protocol_str = " | ".join(protocol_list)
            #
            # # P2P信息
            # p2p_enabled = "是" if playurldata['p2p_data']['p2p'] else "否"
            #
            # # 重载选项
            # reload_info = contentdata['reload_option']
            # scatter_time = reload_info['scatter']
            #
            # print(
            #     f'📺视频信息：房间{room_id} 内容{cid} 协议[{protocol_str}] P2P[{p2p_enabled}] 重载间隔[{scatter_time}ms]')
            # # 转发到 WebSocket
            # danmu_ws_server.send_danmu_message({
            #     "type": "playurl_reload",
            #     "room_id": room_id,
            #     "cid": cid,
            #     "protocols": protocol_list,
            #     "p2p_enabled": p2p_enabled,
            #     "scatter_time": scatter_time,
            #     "timestamp": time.time()
            # })
            pass

        elif content['cmd'] == "PREPARING":
            # # 主播准备中 (PREPARING)
            # contentdata = content
            # print(contentdata)
            pass

        elif content['cmd'] == "RANK_CHANGED":
            # # 榜单排名
            # contentdata = content['data']
            # print("RANK_CHANGED", contentdata)
            pass

        elif content['cmd'] == "RANK_CHANGED_V2":
            # # 榜单排名
            # contentdata = content['data']
            # print("RANK_CHANGED_V2", contentdata)
            pass

        elif content['cmd'] == "ROOM_REAL_TIME_MESSAGE_UPDATE":
            # # 主播信息更新 (ROOM_REAL_TIME_MESSAGE_UPDATE)
            # contentdata = content['data']
            # print(contentdata)
            pass

        elif content['cmd'] == "VOICE_JOIN_LIST":
            # # ?语音加入列表
            # contentdata = content['data']
            # print("语音加入列表", contentdata)
            pass

        elif content['cmd'] == "VOICE_JOIN_ROOM_COUNT_INFO":
            # # ?语音加入房间计数信息
            # contentdata = content['data']
            # print("语音加入房间计数信息", contentdata)
            pass

        elif content['cmd'] == "WIDGET_BANNER":
            # # 顶部横幅 (WIDGET_BANNER)
            # # 注: 网页端在直播间标题下面的横幅, 例如 限时任务 等
            # contentdata = content['data']
            # widget_list = contentdata['widget_list']
            # print(widget_list)
            pass

        elif content['cmd'] == "WIDGET_GIFT_STAR_PROCESS":
            contentdata = content['data']

            # 基本信息
            finished = "已完成" if contentdata['finished'] else "未完成"
            ddl_time = contentdata['ddl_timestamp']

            # 进度信息
            progress_list = []
            for process in contentdata['process_list']:
                completed = process['completed_num']
                target = process['target_num']
                progress = f"{completed}/{target}"
                progress_list.append(progress)

            progress_str = "、".join(progress_list)

            print(f'🌟礼物星球：进度[{progress_str}] 状态[{finished}] 截止{datetime.datetime.fromtimestamp(ddl_time)}')

        elif content['cmd'] == "STOP_LIVE_ROOM_LIST":
            # # 下播的直播间 (STOP_LIVE_ROOM_LIST)
            # # 注: 估计是更新关注的主播直播状态的
            # contentdata = content['data']
            # stop_live_room_list = contentdata['room_id_list']
            # print(stop_live_room_list)
            pass

        else:
            print("❌未收录：", content['cmd'])
            contentdata = content
            print(json.dumps(contentdata))
            # 转发未处理的消息类型
            danmu_ws_server.send_danmu_message({
                "type": "unknown",
                "cmd": content['cmd'],
                "data": content,
                "timestamp": time.time()
            })

    cdm.Callable_opt_code5 = danmu_processing

    try:
        threading.Thread(target=cdm.start).start()
        print("弹幕连接已启动，WebSocket 服务器运行中...")
        print(f"网页客户端可以连接到: ws://localhost:8765")

        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序被用户中断")
        cdm.stop()
        danmu_ws_server.stop_server()
