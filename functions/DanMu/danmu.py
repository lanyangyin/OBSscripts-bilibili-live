import asyncio
import datetime
import hashlib
import json
import os
import re
import time
import zlib
from collections import OrderedDict
from collections import deque
from collections.abc import Callable
from pathlib import Path
from typing import Set, Optional, Union, Dict, Any

import websockets
from PIL import Image

from function.api.Authentication.Wbi.get_danmu_info import WbiSigna
from function.api.Special.Csrf import BilibiliCSRFAuthenticator
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
from function.tools.EncodingConversion.DanmuProtoDecoder import DanmuProtoDecoder
from function.tools.EncodingConversion.dict_to_cookie_string import dict_to_cookie_string
from function.tools.EncodingConversion.parse_cookie import parse_cookie


class OptimizedMessageDeduplication:
    """优化的消息去重类"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 5):
        """
        Args:
            max_size: 最大存储数量
            ttl_seconds: 消息存活时间（秒），None表示不过期
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        # 使用OrderedDict同时维护顺序和快速查找
        self.message_store = OrderedDict()  # {hash: timestamp}

    def add(self, message: str) -> bool:
        """添加消息，返回True如果是新消息"""
        message_hash = self._get_hash(message)
        current_time = time.time()

        # 清理过期消息
        if self.ttl_seconds:
            self._cleanup_expired(current_time)

        # 检查是否重复
        if message_hash in self.message_store:
            # 更新访问时间
            self.message_store.move_to_end(message_hash)
            return False

        # 添加新消息
        self.message_store[message_hash] = current_time

        # 限制大小
        if len(self.message_store) > self.max_size:
            self.message_store.popitem(last=False)

        return True

    def contains(self, message: str) -> bool:
        """检查消息是否重复"""
        message_hash = self._get_hash(message)

        if self.ttl_seconds:
            self._cleanup_expired(time.time())

        return message_hash in self.message_store

    def _get_hash(self, message: str) -> str:
        """获取消息哈希（使用更快的哈希算法）"""
        return hashlib.md5(message.encode()).hexdigest()
        # 或者使用更快的：return hashlib.sha1(message.encode()).hexdigest()

    def _cleanup_expired(self, current_time: float):
        """清理过期消息"""
        expired_hashes = []

        for msg_hash, timestamp in self.message_store.items():
            if current_time - timestamp > self.ttl_seconds:
                expired_hashes.append(msg_hash)
            else:
                break  # 由于是有序的，后面的都不会过期

        for msg_hash in expired_hashes:
            del self.message_store[msg_hash]

    def size(self) -> int:
        """返回当前消息数量"""
        if self.ttl_seconds:
            self._cleanup_expired(time.time())
        return len(self.message_store)

    def clear(self):
        """清空所有消息"""
        self.message_store.clear()

    def get_memory_usage(self) -> int:
        """估算内存使用（字节）"""
        # 每个条目大约：哈希(32字节) + 时间戳(8字节) + 字典开销
        return len(self.message_store) * 50  # 近似值

class DanmuWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.connected_clients: Set = set()
        self.server: Optional[websockets.WebSocketServer] = None
        self.danmu_processor = None
        self.running = False
        self._server_task: Optional[asyncio.Task] = None

    async def register(self, websocket):
        """注册新的客户端连接"""
        self.connected_clients.add(websocket)
        print(f"新的网页客户端连接，当前连接数: {len(self.connected_clients)}")

        # 发送欢迎消息
        welcome_msg = {
            "type": "system",
            "messageData": "弹幕服务器连接成功",
            "timestamp": time.time(),
            "clients_count": len(self.connected_clients)
        }
        await websocket.send(json.dumps(welcome_msg))

    async def unregister(self, websocket):
        """移除断开连接的客户端"""
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)
            print(f"网页客户端断开，当前连接数: {len(self.connected_clients)}")

    async def broadcast_message(self, message: Dict[str, Any]):
        """向所有连接的客户端广播消息"""
        if not self.connected_clients:
            return

        message_json = json.dumps(message, ensure_ascii=False)

        # 收集断开连接的客户端
        disconnected_clients = []

        # 使用 asyncio.gather 并行发送消息
        tasks = []
        for client in self.connected_clients:
            try:
                task = asyncio.create_task(client.send(message_json))
                tasks.append(task)
            except Exception:
                disconnected_clients.append(client)

        # 等待所有发送任务完成
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        # 移除断开连接的客户端
        for client in disconnected_clients:
            await self.unregister(client)

    async def handle_client(self, websocket):
        """处理客户端连接"""
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
                        "messageData": "无效的JSON格式",
                        "timestamp": time.time()
                    }
                    await websocket.send(json.dumps(error_msg))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def handle_client_message(self, websocket, data: Dict[str, Any]):
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

    async def send_danmu_message(self, danmu_data: Dict[str, Any]):
        """发送弹幕消息（异步版本）"""
        await self.broadcast_message(danmu_data)

    def send_danmu_message_sync(self, danmu_data: Dict[str, Any]):
        """同步方式发送弹幕消息（用于从其他线程调用）"""
        if self.running:
            # 如果从其他线程调用，使用 run_coroutine_threadsafe
            asyncio.run_coroutine_threadsafe(
                self.send_danmu_message(danmu_data),
                asyncio.get_event_loop()
            )

    async def start_server_async(self):
        """异步启动 WebSocket 服务器"""
        self.running = True
        self.server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        print(f"弹幕转发服务器启动在 ws://{self.host}:{self.port}")

        # 保持服务器运行
        await self.server.wait_closed()

    async def start_server(self):
        """启动服务器（包装方法）"""
        try:
            await self.start_server_async()
        except asyncio.CancelledError:
            print("WebSocket 服务器被取消")
        except Exception as e:
            print(f"WebSocket 服务器错误: {e}")
        finally:
            await self.stop_server_async()

    async def stop_server_async(self):
        """异步停止服务器"""
        self.running = False

        # 关闭所有客户端连接
        if self.connected_clients:
            close_tasks = []
            for client in list(self.connected_clients):
                close_tasks.append(asyncio.create_task(client.close()))
            if close_tasks:
                await asyncio.gather(*close_tasks, return_exceptions=True)
            self.connected_clients.clear()

        # 停止服务器
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        # 取消服务器任务
        if self._server_task and not self._server_task.done():
            self._server_task.cancel()

        print("WebSocket 服务器已停止")

    def stop_server(self):
        """同步停止服务器"""
        if self._server_task and not self._server_task.done():
            self._server_task.cancel()

    async def run_forever(self):
        """运行服务器直到停止"""
        self._server_task = asyncio.create_task(self.start_server())
        try:
            await self._server_task
        except asyncio.CancelledError:
            print("服务器任务被取消")

class Danmu:

    def __init__(self, headers: dict):
        self.headers = headers
        self.cookie = headers['cookie']

    def _get_websocket_client(self, roomid: int):
        danmu_info = WbiSigna(self.headers).get_danmu_info(roomid)
        token = danmu_info['data']['token']
        host = danmu_info['data']['host_list'][-1]
        wss_url = f"wss://{host['host']}:{host['wss_port']}/sub"

        user_info = BilibiliCSRFAuthenticator(self.headers).get_user_live_info()['data']
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
            self.url = url
            self.auth_body = auth_body
            self.Callable_opt_code8: Callable[[str], None] = lambda a: None
            """接收认证包回复的回调函数"""
            self.Callable_opt_code5: Callable[[Dict[str, Any]], None] = lambda a: None
            """接收普通包 (命令)的回调函数"""
            self.wssCertificationAndHeartbeat: Callable[[bytes], None] = lambda a: None
            """发送认证包接收时的回调函数"""
            self.num_r = 20
            """同时连接多个弹幕减少丢包"""
            self.o_m_d = OptimizedMessageDeduplication(GlobalVariableOfData.number_of_cache_entries,
                                                  GlobalVariableOfData.cache_duration)

            self.connection_tasks = []  # 异步任务列表
            self.running = False
            self._stop_event = asyncio.Event()  # 用于等待停止信号
            self._loop = None  # 存储事件循环引用

        async def connect(self):
            base_delay = 3
            retry_count = 0
            max_retries = 5

            while self.running and retry_count < max_retries:
                try:
                    async with websockets.connect(
                            self.url,
                            ping_interval=20,
                            ping_timeout=10,
                            close_timeout=10
                    ) as ws:
                        await self.on_open(ws)
                        retry_count = 0  # 成功连接后重置重试计数

                        while self.running:
                            try:
                                message = await asyncio.wait_for(ws.recv(), timeout=10.0)
                                await self.on_message(message)
                            except asyncio.TimeoutError:
                                if not self.running:
                                    break
                                try:
                                    await ws.send(self.pack(None, 2))
                                except Exception:
                                    break
                            except websockets.exceptions.ConnectionClosed:
                                break

                except Exception as e:
                    if not self.running:
                        break
                    retry_count += 1
                    delay = base_delay * (2 ** retry_count)
                    print(f"连接失败，{delay}秒后重试... (重试次数: {retry_count})")
                    await asyncio.sleep(delay)

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
                    # 异步处理认证响应
                    asyncio.create_task(self._handle_certification_response(auth_response))
                    # 启动心跳任务
                    asyncio.create_task(self.send_heartbeat(ws))
                except asyncio.TimeoutError:
                    print("认证响应超时")
                    raise

            except Exception as e:
                print(f"认证失败: {e}")
                raise

        async def _handle_certification_response(self, auth_response: bytes):
            """异步处理认证响应"""
            self.wssCertificationAndHeartbeat(auth_response)

        async def send_heartbeat(self, ws):
            """发送心跳"""
            while self.running:
                try:
                    await ws.send(self.pack(None, 2))
                    await asyncio.sleep(self.HEARTBEAT_INTERVAL)
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    print(f"心跳发送失败: {e}")
                    break

        async def on_message(self, message):
            if isinstance(message, bytes):
                await self.unpack(message)

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

        async def unpack(self, byte_buffer: bytes):
            package_len = int.from_bytes(byte_buffer[0:4], 'big')
            head_length = int.from_bytes(byte_buffer[4:6], 'big')
            prot_ver = int.from_bytes(byte_buffer[6:8], 'big')
            opt_code = int.from_bytes(byte_buffer[8:12], 'big')
            sequence = int.from_bytes(byte_buffer[12:16], 'big')

            content_bytes = byte_buffer[16:package_len]

            if prot_ver == self.VERSION_NORMAL:
                pass
            elif prot_ver == self.VERSION_ZIP:
                content_bytes = zlib.decompress(content_bytes)
                await self.unpack(content_bytes)
                return
            elif prot_ver == self.VERSION_BTI:
                pass

            content = content_bytes.decode('utf-8')
            if not self.o_m_d.add(content):
                return

            if opt_code == 5:  # SEND_SMS_REPLY
                content_dict: dict = json.loads(content)
                if content_dict['cmd'] == "INTERACT_WORD_V2":
                    content_dict['data'] = DanmuProtoDecoder().decode_interact_word_v2_protobuf(
                        content_dict['data']['pb'])
                elif content_dict['cmd'] == "ONLINE_RANK_V3":
                    content_dict['data'] = DanmuProtoDecoder().decode_online_rank_v3_protobuf(
                        content_dict['data']['pb'])

                # 异步处理回调
                asyncio.create_task(self._handle_opt_code5(content_dict))
            elif opt_code == 8:  # AUTH_REPLY
                asyncio.create_task(self._handle_opt_code8(content))

            if len(byte_buffer) > package_len:
                await self.unpack(byte_buffer[package_len:])

        async def _handle_opt_code5(self, content_dict: dict):
            """异步处理 opt_code 5 回调"""
            self.Callable_opt_code5(content_dict)

        async def _handle_opt_code8(self, content: str):
            """异步处理 opt_code 8 回调"""
            self.Callable_opt_code8(content)

        async def start_async(self):
            """异步启动方法 - 会一直运行直到收到停止信号"""
            self.running = True
            self._stop_event.clear()
            self.connection_tasks.clear()
            self._loop = asyncio.get_running_loop()  # 获取当前运行的事件循环

            print(f"启动 {self.num_r} 个弹幕连接...")

            # 创建多个连接任务
            for i in range(self.num_r):
                task = asyncio.create_task(self.connect(), name=f"DanmuConn-{i}")
                self.connection_tasks.append(task)
                if i < self.num_r - 1:  # 最后一个连接不需要等待
                    await asyncio.sleep(0.3)  # 间隔连接

            print("所有弹幕连接已启动，等待停止信号...")

            # 等待停止信号
            await self._stop_event.wait()

            print("收到停止信号，正在关闭连接...")

        def start(self):
            """同步启动方法（包装异步方法）"""
            self.running = True
            try:
                # 运行异步启动方法
                asyncio.run(self.start_async())
            except KeyboardInterrupt:
                print("收到中断信号")
                self.stop()
            except Exception as e:
                print(f"启动异常: {e}")
                self.stop()

        async def stop_async(self):
            """异步停止方法"""
            if not self.running:
                return

            self.running = False
            self._stop_event.set()  # 触发停止信号

            print("正在停止弹幕连接...")

            # 取消所有连接任务
            for task in self.connection_tasks:
                if not task.done():
                    task.cancel()

            # 等待所有任务完成
            if self.connection_tasks:
                await asyncio.gather(*self.connection_tasks, return_exceptions=True)

            print("弹幕连接已停止")

        def stop(self):
            """同步停止方法"""
            # 如果已经有运行的事件循环，使用它
            try:
                loop = asyncio.get_running_loop()
                # 如果已经有运行的事件循环，创建任务来执行停止
                asyncio.create_task(self.stop_async())
            except RuntimeError:
                # 如果没有运行的事件循环，创建一个
                asyncio.run(self.stop_async())


# 运行整合版本
if __name__ == '__main__':
    from _Input.functions.DanMu import Danmu as DataInput
    from _Input.functions.DanMu import Danmu as DataInput
    from function.tools.EncodingConversion.url2pillow_image import url2pillow_image
    from function.api.Generic import BilibiliApiGeneric
    import signal
    import sys

    class GlobalVariableOfData:
        # 弹幕显示
        number_of_cache_entries = 500
        """防重复的缓存条数"""
        cache_duration = 6
        """防重复的缓存时长秒"""
        number_of_comments_client = 30
        """弹幕客户端创建数"""
        is_enter_room_display = True
        """是否显示进房消息"""
        face_picture_s = (40, 40)
        """头像大小"""
        is_medal_display = True
        """是否显示粉丝徽章"""
        is_medal_other_display = False
        """是否显示其他的粉丝徽章"""
        is_medal_un_light_display = True
        """是否显示未点亮的粉丝徽章"""
        fan_medal_text_size = '14px'
        """粉丝勋章文字大小"""
        message_text_size = '16px'
        """内容文字大小"""
        time_text_size = '11px'
        """时间文字大小"""
        own_big_expression = {"额": "./img/emoji/emoji_208.png"}
        """自定义的大图片的名称和位置"""
        line_break_display = True
        """换行显示"""
        is_tag_administrator = False
        """是否标记管理员，is_admin不受影响"""
        is_timestamp_display = False


    async def show_danmu():
        BULC = BilibiliUserConfigManager(Path('../../cookies/config.json'))
        cookies = BULC.get_user_cookies()['data']
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'cookie': dict_to_cookie_string(cookies)
        }
        b_a_g = BilibiliApiGeneric(Headers)
        get_room_base = b_a_g.get_room_base_info(DataInput.room_id)

        def get_guard_dict(api, roomid, ruid, **kwargs):
            """
            获取大航海成员字典的包装函数

            Args:
                api: BilibiliApiGeneric 实例
                roomid: 直播间号
                ruid: 主播UID
                **kwargs: 其他参数传递给 get_guard_list

            Returns:
                包含操作结果的字典，其中data字段包含guard_dict
            """
            # 确保获取完整列表
            kwargs['include_total_list'] = True

            # 调用原函数
            result = api.get_guard_list(roomid, ruid, **kwargs)

            if result["success"]:
                # 转换列表为字典
                guard_dict = {}
                total_list = result["data"].get("total_list", [])

                for guard in total_list:
                    uid = guard["uinfo"]["uid"]
                    guard_level = guard["uinfo"]["guard"]["level"]
                    guard_dict[uid] = guard_level

                # 将字典添加到返回数据中
                result["data"]["guard_dict"] = guard_dict

            return result

        result = get_guard_dict(b_a_g, DataInput.room_id, get_room_base["data"]["uid"], page=1, typ=5,
                                include_total_list=True)
        guard_dict = result["data"]["guard_dict"]
        danmu_ws_server = DanmuWebSocketServer()

        dm = Danmu(Headers)
        cdm = dm.connect_room(DataInput.room_id)
        cdm.num_r = GlobalVariableOfData.number_of_comments_client

        # 1. 启动 WebSocket 服务器
        server_task = asyncio.create_task(danmu_ws_server.run_forever())
        await asyncio.sleep(1)  # 等待服务器启动
        print("WebSocket 服务器启动完成")


        # 2. 设置弹幕处理器
        def danmu_processing(content: dict):
            """

            Args:
                content: 直播间消息

            Returns:

            """
            if content['cmd'] == "LIVE":
                # 直播开始 (LIVE)
                contentdata = content
                roomid = contentdata['roomid']
                if 'live_time' in contentdata:
                    live_time = contentdata['live_time']
                    live_platform = contentdata['live_platform']

                    print(f'🔴直播开始：房间{roomid} 时间{live_time} 平台[{live_platform}]')
                    # 转发到 WebSocket
                    asyncio.create_task(danmu_ws_server.send_danmu_message({
                        "type": "live_start",
                        "messageData": f'🔴直播开始：房间{roomid} 平台[{live_platform}]',
                        "roomid": roomid,
                        "live_time": live_time,
                        "live_platform": live_platform,
                        "timestamp": live_time
                    }))

            elif content['cmd'] == "LIKE_INFO_V3_UPDATE":
                # 直播间点赞数更新 (LIKE_INFO_V3_UPDATE)
                contentdata = content['data']
                print(f"👍🔢点赞数：\t{contentdata['click_count']}")
                pass
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "like_update",
                    "click_count": contentdata['click_count'],
                    "timestamp": time.time()
                }))

            elif content['cmd'] == "ONLINE_RANK_COUNT":
                contentdata = content['data']
                print(f"🧑🔢高能用户数：\t{contentdata['count']}")
                pass
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "online_rank_count",
                    "count": contentdata['count'],
                    "timestamp": time.time()
                }))

            elif content['cmd'] == "WATCHED_CHANGE":
                contentdata = content['data']
                print(f"👀🔢直播间看过人数：\t{contentdata['num']}|\t{contentdata['text_large']}")
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "watched_change",
                    "num": contentdata['num'],
                    "text_large": contentdata['text_large'],
                    "timestamp": time.time()
                }))
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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "popular_rank_changed",
                    "rank": rank,
                    "uid": uid,
                    "rank_name": rank_name,
                    "on_rank_name": on_rank_name,
                    "message": f"{on_rank_name}{rank_name} {rank_display}",
                    "timestamp": time.time()
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "super_chat",
                    "user": uname,
                    "uid": uid,
                    "medal": mfo,
                    "price": price,
                    "message": message,
                    "duration": duration,
                    "timestamp": time.time()
                }))

            elif content['cmd'] == "SUPER_CHAT_MESSAGE_DELETE":
                contentdata = content['data']
                # 删除的SC ID列表
                ids = contentdata['ids']
                ids_str = "、".join(str(sc_id) for sc_id in ids)

                print(f'🗑️醒目留言删除：SC[{ids_str}]')
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "super_chat_delete",
                    "ids": ids,
                    "message": f"SC[{ids_str}]",
                    "timestamp": time.time()
                }))

            elif content['cmd'] == "DANMU_MSG":
                user_name = ''  # 昵称
                """发送者昵称"""
                user_face_picture = ''  # 头像
                """头像"""
                face_picture_x = '40'  # 头像宽度
                """头像宽度"""
                face_picture_y = '40'  # 头像高度
                """头像高度"""
                user_id = ''  # id
                """发送者id"""
                identity_title = ''  # 身份头衔：管理员 moderator，船员 member，主播 owner，普通为空
                """身份头衔"""
                privilege_level = '0'  # 特权级别 1,2,3,0
                """特权级别"""
                fleet_title = ''  # 舰队称号
                """舰队称号"""
                fan_medal_name = ''
                """粉丝勋章名称"""
                fan_medal_level = '0'
                """粉丝勋章等级"""
                fan_medal_color_start = ''
                """粉丝勋章开始颜色"""
                fan_medal_color_end = ''
                """粉丝勋章结束颜色"""
                fan_medal_color_border = ''
                """粉丝勋章边框颜色"""
                fan_medal_color_text = ''
                """粉丝勋章文本色"""
                fan_medal_color_level = ''
                """粉丝勋章等级颜色"""
                fleet_badge = ''  # 舰队徽章
                """舰队徽章"""
                message_data = []  # 消息数据
                """消息数据"""
                timestamp = '0'  # 发送时间
                """发送时间"""
                is_admin = False  # 是否管理员
                """是否管理员"""
                is_fan_group = False  # 是否有粉丝勋章
                """是否有粉丝勋章"""

                # 弹幕 (DANMU_MSG)
                content_info = content['info']

                user_name = content_info[0][15]["user"]['base']["name"]

                user_face_picture = f'./img/face/{re.split("/", content_info[0][15]["user"]["base"]["face"])[-1]}'
                if not os.path.exists(user_face_picture):
                    # 先检查返回值
                    result = url2pillow_image(content_info[0][15]["user"]["base"]["face"], Headers)
                    if result and "PilImg" in result and result["PilImg"] is not None:
                        pillow_img = result["PilImg"]
                        pillow_img.save(user_face_picture)
                        face_picture_x, face_picture_y = pillow_img.size
                    else:
                        print(f"无法获取图片: {result['Message']}")
                else:
                    pillow_img = Image.open(user_face_picture)
                    face_picture_x, face_picture_y = pillow_img.size
                if GlobalVariableOfData.face_picture_s:
                    face_picture_x, face_picture_y = GlobalVariableOfData.face_picture_s

                user_id = content_info[0][15]["user"]["uid"]

                if user_id in guard_dict:
                    identity_title = "member"  # 舰长
                    privilege_level = guard_dict[user_id]
                    fleet_title = {'1': '总督', '2': '提督', '3': '舰长'}[
                        str(privilege_level)]  # if is_medal_other_display:
                    #     fleet_badge = f'https://blc.huixinghao.cn/static/img/icons/guard-level-{privilege_level}.png'
                if user_id == get_room_base["data"]["uid"]:
                    identity_title = "owner"  # 房主
                elif content_info[2][2]:
                    if GlobalVariableOfData.is_tag_administrator:
                        identity_title = "moderator"  # 管理员

                medal = content_info[0][15]["user"]['medal']
                """勋章基础信息"""
                if medal:
                    # 检查点亮条件
                    light_ok = GlobalVariableOfData.is_medal_un_light_display or medal.get("is_light", False)
                    # 检查归属条件
                    owner_ok = GlobalVariableOfData.is_medal_other_display or medal.get("ruid") == get_room_base["data"]["uid"]
                    # 同时满足两个条件才显示
                    if light_ok and owner_ok:
                        fan_medal_name = medal["name"]
                        """粉丝勋章名称"""
                        fan_medal_level = medal["level"]
                        """粉丝勋章等级"""
                        fan_medal_color_start = medal["v2_medal_color_start"]
                        """粉丝勋章开始颜色"""
                        fan_medal_color_end = medal["v2_medal_color_end"]
                        """粉丝勋章结束颜色"""
                        fan_medal_color_border = medal["v2_medal_color_border"]
                        """粉丝勋章边框颜色"""
                        fan_medal_color_text = medal["v2_medal_color_text"]
                        """粉丝勋章文本色"""
                        fan_medal_color_level = medal["v2_medal_color_level"]
                        """粉丝勋章等级颜色"""
                        if fleet_title:
                            fleet_badge_path = f"./img/fleet/{fleet_title}.png"
                            if not os.path.exists(fleet_badge_path):
                                pillow_img = url2pillow_image(medal['guard_icon'], Headers)["PilImg"]
                                pillow_img.save(fleet_badge_path)
                            fleet_badge = fleet_badge_path
                            """舰长勋章图标url"""

                danmu_extra = json.loads(content_info[0][15]['extra'])
                """弹幕额外信息"""
                if danmu_extra['reply_uname']:
                    message_data.append({
                        'type': 'text',
                        'color': danmu_extra['reply_uname_color'],
                        'text': f"@{danmu_extra['reply_uname']}  "
                    })
                image_information = content_info[0][13]
                """表情信息，没有时为‘{}’"""
                if image_information != "{}":  # 大表情
                    image_information_path = f"./img/image_information/{image_information['emoticon_unique']}.png"
                    if not os.path.exists(image_information_path):
                        pillow_img = url2pillow_image(image_information["url"], Headers)["PilImg"]
                        pillow_img.save(image_information_path)
                    else:
                        pillow_img = Image.open(image_information_path)
                    image_information_path_width, image_information_path_height = pillow_img.size
                    message_data.append({
                        'type': 'image',
                        'alt': danmu_extra['content'],
                        'width': f'{image_information_path_width}px',
                        'height': f'{image_information_path_height}px',
                        'src': image_information_path
                    })
                else:
                    damu_text = content_info[1]
                    """弹幕文本"""
                    pattern = r'(\[.*?\])'
                    emoji_name_text_separation_list = re.split(pattern, damu_text)
                    """分离的带‘[]’的表情名称和普通文本"""
                    pattern = r'(' + '|'.join([re.escape(sep) for sep in list(GlobalVariableOfData.own_big_expression.keys()) + list(
                        danmu_extra['emots'] if danmu_extra['emots'] else [])]) + ')'
                    emoji_text_own_separation_list = re.split(pattern, damu_text)
                    for damu_split in emoji_text_own_separation_list:
                        if not damu_split:
                            continue
                        # emoji
                        if danmu_extra['emots']:
                            if damu_split in danmu_extra['emots']:
                                file_path = f"./img/emoji/{danmu_extra['emots'][damu_split]['emoticon_unique']}.png"
                                if not os.path.exists(file_path):
                                    pillow_img = url2pillow_image(danmu_extra['emots'][damu_split]['url'], Headers)[
                                        "PilImg"]
                                    pillow_img.save(file_path)
                                message_data.append({
                                    'type': 'emoji',
                                    'alt': damu_split,
                                    'src': file_path
                                })
                                continue
                        # 自定表情
                        if GlobalVariableOfData.own_big_expression:
                            if damu_split in GlobalVariableOfData.own_big_expression:
                                pillow_img = Image.open(GlobalVariableOfData.own_big_expression[damu_split])
                                width, height = pillow_img.size
                                message_data.append({
                                    'type': 'image',
                                    'alt': damu_split,
                                    'height': f'{height}px',
                                    'width': f'{width}px',
                                    'src': GlobalVariableOfData.own_big_expression[damu_split]
                                })
                                continue
                        # 普通文本
                        message_data.append({
                            'type': 'text',
                            'text': damu_split
                        })

                timestamp = content_info[9]['ts']

                is_admin = content_info[2][2]

                if fan_medal_name and GlobalVariableOfData.is_medal_display:
                    is_fan_group = True

                print(
                    f"{f'[{content_info[16][0]}]' if content_info[16][0] else ''}{f'【{fan_medal_name}|{fan_medal_level}】' if fan_medal_name else ''}{user_name} 《{identity_title}|{fleet_title}》:")
                print(
                    f"\t>>>  {'@' if danmu_extra['reply_uname'] else ''}{(danmu_extra['reply_uname'] + '    ') if danmu_extra['reply_uname'] else ''}{content_info[1]}    |\t{timestamp}")
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "danmu",
                    "uName": user_name,
                    "facePicture": user_face_picture,
                    "facePictureX": face_picture_x,
                    "facePictureY": face_picture_y,
                    "uId": user_id,
                    "identityTitle": identity_title,
                    "privilegeLevel": privilege_level,
                    "fleetTitle": fleet_title,
                    "fanMedalName": fan_medal_name,
                    "fanMedalLevel": fan_medal_level,
                    "fanMedalColorStart": fan_medal_color_start,
                    "fanMedalColorEnd": fan_medal_color_end,
                    "fanMedalColorBorder": fan_medal_color_border,
                    "fanMedalColorText": fan_medal_color_text,
                    "fanMedalColorLevel": fan_medal_color_level,
                    "fanMedalTextSize": GlobalVariableOfData.fan_medal_text_size,
                    "fleetBadge": fleet_badge,
                    "messageData": message_data,
                    "messageTextSize": GlobalVariableOfData.message_text_size,
                    "timestamp": timestamp,
                    "timeTextSize": GlobalVariableOfData.time_text_size,
                    "isAdmin": is_admin,
                    "isFanGroup": is_fan_group,
                    "lineBreakDisplay": GlobalVariableOfData.line_break_display,
                    "isTimestampDisplay": GlobalVariableOfData.is_timestamp_display,

                    "user": user_name,
                    "medal": f'【{fan_medal_name}|{fan_medal_level}】' if fan_medal_name else None,
                    "wealth": f'[{content_info[16][0]}]' if content_info[16][0] else None,
                    "content": content_info[1],
                    "reply_to": f"{'@' if danmu_extra['reply_uname'] else None}{(danmu_extra['reply_uname'] if danmu_extra['reply_uname'] else None)}",
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "combo_gift",
                    "user": ufo,
                    "medal": mfo,
                    "wealth": wfo,
                    "gift_name": contentdata['gift_name'],
                    "combo_num": contentdata['batch_combo_num'],
                    "total_coin": contentdata['combo_total_coin'],
                    "message": tfo,
                    "timestamp": time.time()
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "user_toast",
                    "user": username,
                    "uid": uid,
                    "guard_level": guard_level,
                    "guard_name": guard_name,
                    "price": price,
                    "unit": unit,
                    "message": f"{username}开通{guard_name} {price}元/{unit}",
                    "timestamp": time.time()
                }))

            elif content['cmd'] == "USER_TOAST_MSG_V2":
                u_name = ""
                u_id = ""
                user_face_picture = ""
                face_picture_x = ""
                face_picture_y = ""
                timestamp = ""
                message_data = ""
                privilege_level = ""
                fleet_title = ""
                fleet_badge = ""
                membership_header_color = ""
                identity_title = ""

                contentdata = content['data']
                u_name = contentdata["sender_uinfo"]["base"]["name"]
                u_id = contentdata["sender_uinfo"]["uid"]
                user_card = b_a_g.get_bilibili_user_card(u_id, True)
                user_face_picture = f'./img/face/{re.split("/", user_card["data"]["card"]["face"])[-1]}'
                if not os.path.exists(user_face_picture):
                    # 先检查返回值
                    result = url2pillow_image(user_card["data"]["card"]["face"], Headers)
                    if result and "PilImg" in result and result["PilImg"] is not None:
                        pillow_img = result["PilImg"]
                        pillow_img.save(user_face_picture)
                        face_picture_x, face_picture_y = pillow_img.size
                    else:
                        print(f"无法获取图片: {result['Message']}")
                else:
                    pillow_img = Image.open(user_face_picture)
                    face_picture_x, face_picture_y = pillow_img.size
                if GlobalVariableOfData.face_picture_s:
                    face_picture_x, face_picture_y = GlobalVariableOfData.face_picture_s
                timestamp = content["send_time"]
                message_data = contentdata["toast_msg"]
                privilege_level = contentdata["guard_info"]["guard_level"]
                guard_dict[u_id] = privilege_level
                identity_title = "member"  # 舰长
                fleet_title = {'1': '总督', '2': '提督', '3': '舰长'}[str(privilege_level)]
                if GlobalVariableOfData.is_medal_other_display:
                    fleet_badge = f'https://blc.huixinghao.cn/static/img/icons/guard-level-{privilege_level}.png'
                fleet_badge_path = f"./img/fleet/{fleet_title}.png"
                if not os.path.exists(fleet_badge_path):
                    pillow_img = url2pillow_image(fleet_badge, Headers)["PilImg"]
                    pillow_img.save(fleet_badge_path)
                fleet_badge = fleet_badge_path
                membership_header_color = contentdata["option"]["color"]

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "user_toast_v2",
                    "uName": u_name,
                    "uId": u_id,
                    "facePicture": user_face_picture,
                    "facePictureX": face_picture_x,
                    "facePictureY": face_picture_y,
                    "timestamp": timestamp,
                    "messageData": message_data,
                    "fleetBadge": fleet_badge,
                    "membershipHeaderColor": membership_header_color,
                    "identityTitle": identity_title,
                    "privilegeLevel": privilege_level,
                    "fleetTitle": fleet_title,

                    "user": username,
                    "uid": uid,
                    "guard_level": guard_level,
                    "guard_name": guard_name,
                    "price": price,
                    "unit": unit,
                    "message": f"{username}开通{guard_name} {price}元/{unit}",
                }))

            elif content['cmd'] == "GUARD_BUY":
                # 上舰通知 (GUARD_BUY)
                contentdata = content['data']

                tfo = f"🚢上舰：\t{contentdata['username']}\t购买{contentdata['num']}个\t【{contentdata['gift_name']}】"
                print(f"{tfo}")
                pass
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "guard_buy",
                    "user": contentdata['username'],
                    "guard_name": contentdata['gift_name'],
                    "guard_count": contentdata['num'],
                    "price": contentdata['price'],
                    "message": tfo,
                }))

            elif content['cmd'] == "INTERACT_WORD_V2":
                if not GlobalVariableOfData.is_enter_room_display:
                    return
                user_name = ''  # 昵称
                """发送者昵称"""
                user_face_picture = ''  # 头像
                """头像"""
                face_picture_x = '40'  # 头像宽度
                """头像宽度"""
                face_picture_y = '40'  # 头像高度
                """头像高度"""
                user_id = ''  # id
                """发送者id"""
                identity_title = ''  # 身份头衔：管理员 moderator，船员 member，主播 owner，普通为空
                """身份头衔"""
                privilege_level = '0'  # 特权级别 1,2,3,0
                """特权级别"""
                fleet_title = ''  # 舰队称号
                """舰队称号"""
                fan_medal_name = ''
                """粉丝勋章名称"""
                fan_medal_level = '0'
                """粉丝勋章等级"""
                fan_medal_color_start = ''
                """粉丝勋章开始颜色"""
                fan_medal_color_end = ''
                """粉丝勋章结束颜色"""
                fan_medal_color_border = ''
                """粉丝勋章边框颜色"""
                fan_medal_color_text = ''
                """粉丝勋章文本色"""
                fan_medal_color_level = ''
                """粉丝勋章等级颜色"""
                fleet_badge = ''  # 舰队徽章
                """舰队徽章"""
                message_data = []  # 消息数据
                """消息数据"""
                timestamp = '0'  # 发送时间
                """发送时间"""
                is_admin = False  # 是否管理员
                """是否管理员"""
                is_fan_group = False  # 是否有粉丝勋章
                """是否有粉丝勋章"""

                # 用户交互消息【Proto格式】
                contentdata = content['data']

                user_name = contentdata['uname']

                user_face_picture = f'./img/face/{re.split("/", contentdata["uinfo"]["base"]["face"])[-1]}'
                if not os.path.exists(user_face_picture):
                    # 先检查返回值
                    result = url2pillow_image(contentdata["uinfo"]["base"]["face"], Headers)
                    if result and "PilImg" in result and result["PilImg"] is not None:
                        pillow_img = result["PilImg"]
                        pillow_img.save(user_face_picture)
                        face_picture_x, face_picture_y = pillow_img.size
                    else:
                        print(f"无法获取图片: {result['Message']}")
                else:
                    pillow_img = Image.open(user_face_picture)
                    face_picture_x, face_picture_y = pillow_img.size
                if GlobalVariableOfData.face_picture_s:
                    face_picture_x, face_picture_y = GlobalVariableOfData.face_picture_s

                user_id = contentdata["uinfo"]["uid"]

                if user_id in guard_dict:
                    identity_title = "member"  # 舰长
                    privilege_level = guard_dict[user_id]
                    fleet_title = {'1': '总督', '2': '提督', '3': '舰长'}[
                        str(privilege_level)]  # if is_medal_other_display:
                    #     fleet_badge = f'https://blc.huixinghao.cn/static/img/icons/guard-level-{privilege_level}.png'
                if user_id == get_room_base["data"]["uid"]:
                    identity_title = "owner"  # 房主

                medal = contentdata["uinfo"]["medal"]
                if medal["level"]:
                    # 检查点亮条件
                    light_ok = GlobalVariableOfData.is_medal_un_light_display or medal.get("is_light", False)
                    # 检查归属条件
                    owner_ok = GlobalVariableOfData.is_medal_other_display or medal.get("ruid") == get_room_base["data"]["uid"]
                    # 同时满足两个条件才显示
                    if light_ok and owner_ok:
                        fan_medal_name = medal["name"]
                        """粉丝勋章名称"""
                        fan_medal_level = medal["level"]
                        """粉丝勋章等级"""
                        fan_medal_color_start = medal["v2_medal_color_start"]
                        """粉丝勋章开始颜色"""
                        fan_medal_color_end = medal["v2_medal_color_end"]
                        """粉丝勋章结束颜色"""
                        fan_medal_color_border = medal["v2_medal_color_border"]
                        """粉丝勋章边框颜色"""
                        fan_medal_color_text = medal["v2_medal_color_text"]
                        """粉丝勋章文本色"""
                        fan_medal_color_level = medal["v2_medal_color_level"]
                        """粉丝勋章等级颜色"""
                        if fleet_title:
                            fleet_badge_path = f"./img/fleet/{fleet_title}.png"
                            if not os.path.exists(fleet_badge_path):
                                pillow_img = url2pillow_image(medal['guard_icon'], Headers)["PilImg"]
                                pillow_img.save(fleet_badge_path)
                            fleet_badge = fleet_badge_path
                            """舰长勋章图标url"""

                message_data = [
                    {
                        'type': 'text',
                        'color': contentdata["uinfo"]["base"]["name_color_str"],
                        'shadow': "rgb(0 0 0) 0px 0px 5px, rgb(255 0 0) 0px 0px 10px, rgb(51, 204, 255) 0px 0px 15px, rgb(255 196 0) 0px 0px 20px, rgb(72 255 0) 0px 0px 25px",
                        'text': f"{contentdata['msg_type']}❓进入直播间或关注消息或分享直播间"
                    }
                ]
                if contentdata['msg_type'] == 1:
                    message_data = [
                        {
                            'type': 'text',
                            'color': contentdata["uinfo"]["base"]["name_color_str"],
                            'shadow': "rgb(0 0 0) 0px 0px 5px, rgb(255 0 0) 0px 0px 10px, rgb(51, 204, 255) 0px 0px 15px, rgb(255 196 0) 0px 0px 20px, rgb(72 255 0) 0px 0px 25px",
                            'text': f"🏠进入直播间"
                        }
                    ]
                elif contentdata['msg_type'] == 2:
                    message_data = [
                        {
                            'type': 'text',
                            'color': contentdata["uinfo"]["base"]["name_color_str"],
                            'shadow': "rgb(0 0 0) 0px 0px 5px, rgb(255 0 0) 0px 0px 10px, rgb(51, 204, 255) 0px 0px 15px, rgb(255 196 0) 0px 0px 20px, rgb(72 255 0) 0px 0px 25px",
                            'text': f"⭐关注直播间"
                        }
                    ]
                elif contentdata['msg_type'] == 3:
                    message_data = [
                        {
                            'type': 'text',
                            'color': contentdata["uinfo"]["base"]["name_color_str"],
                            'shadow': "rgb(0 0 0) 0px 0px 5px, rgb(255 0 0) 0px 0px 10px, rgb(51, 204, 255) 0px 0px 15px, rgb(255 196 0) 0px 0px 20px, rgb(72 255 0) 0px 0px 25px",
                            'text': f"💫分享直播间"
                        }
                    ]

                timestamp = contentdata["timestamp"]

                if fan_medal_name and GlobalVariableOfData.is_medal_display:
                    is_fan_group = True

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

                print(f"{message_data}：\t{wfo}{mfo}{ufo}")
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "interact",
                    "uName": user_name,
                    "facePicture": user_face_picture,
                    "facePictureX": face_picture_x,
                    "facePictureY": face_picture_y,
                    "uId": user_id,
                    "identityTitle": identity_title,
                    "privilegeLevel": privilege_level,
                    "fleetTitle": fleet_title,
                    "fanMedalName": fan_medal_name,
                    "fanMedalLevel": fan_medal_level,
                    "fanMedalColorStart": fan_medal_color_start,
                    "fanMedalColorEnd": fan_medal_color_end,
                    "fanMedalColorBorder": fan_medal_color_border,
                    "fanMedalColorText": fan_medal_color_text,
                    "fanMedalColorLevel": fan_medal_color_level,
                    "fanMedalTextSize": GlobalVariableOfData.fan_medal_text_size,
                    "fleetBadge": fleet_badge,
                    "messageData": message_data,
                    "messageTextSize": GlobalVariableOfData.message_text_size,
                    "timestamp": timestamp,
                    "timeTextSize": GlobalVariableOfData.time_text_size,
                    "isAdmin": is_admin,
                    "isFanGroup": is_fan_group,
                    "lineBreakDisplay": GlobalVariableOfData.line_break_display,

                    "user": ufo,
                    "medal": mfo,
                    "wealth": wfo,
                    "action": message_data,
                    "msg_type": contentdata['msg_type'],
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "like_click",
                    "user": ufo,
                    "medal": mfo,
                    "wealth": wfo,
                    "like_text": tfo,
                    "timestamp": time.time()
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "red_pocket",
                    "user": ufo,
                    "medal": mfo,
                    "wealth": wfo,
                    "action": contentdata['action'],
                    "price": coin,
                    "message": tfo,
                    "timestamp": time.time()
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "red_pocket_v2",
                    "user": ufo,
                    "medal": mfo,
                    "wealth": wfo,
                    "action": contentdata['action'],
                    "price": coin,
                    "message": tfo,
                    "timestamp": time.time()
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "red_pocket_winners",
                    "lot_id": lot_id,
                    "total_num": total_num,
                    "winners": winner_list,
                    "message": f"红包{lot_id} 共{total_num}个礼物 {winners_str}",
                    "timestamp": time.time()
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "red_pocket_winners",
                    "lot_id": lot_id,
                    "total_num": total_num,
                    "winners": winner_list,
                    "message": f"红包{lot_id} 共{total_num}个礼物 {winners_str}",
                    "timestamp": time.time()
                }))

            elif content['cmd'] == "SEND_GIFT":
                u_name = ""
                u_id = ""
                user_face_picture = ""
                face_picture_x = ""
                face_picture_y = ""
                timestamp = ""
                price = ""
                price_level = ""
                message_primary_color = ""
                message_secondary_color = ""
                message_header_color = ""
                message_author_name_color = ""
                message_timestamp_color = ""
                message_color = ""
                message_data = ""
                show_only_header = False

                def get_color_by_amount(amount):
                    """
                    根据金额获取对应的颜色信息

                    参数:
                        amount: 金额数值

                    返回:
                        字典格式的颜色信息，包含color_name、css_color、primary_color和secondary_color
                    """
                    coin_color = {
                        0: {
                            'color_name': '蓝色',
                            'css_color': '#0000FF',
                            'primary_color': 'rgba(0, 123, 255, 1)',  # 较亮的蓝色
                            'secondary_color': 'rgba(0, 86, 179, 1)'  # 较暗的蓝色
                        },
                        30: {
                            'color_name': '浅蓝色',
                            'css_color': '#87CEEB',
                            'primary_color': 'rgba(135, 206, 235, 1)',  # 较亮的浅蓝色
                            'secondary_color': 'rgba(102, 178, 214, 1)'  # 较暗的浅蓝色
                        },
                        50: {
                            'color_name': '绿色',
                            'css_color': '#008000',
                            'primary_color': 'rgba(76, 175, 80, 1)',  # 较亮的绿色
                            'secondary_color': 'rgba(56, 142, 60, 1)'  # 较暗的绿色
                        },
                        100: {
                            'color_name': '黄色',
                            'css_color': '#FFFF00',
                            'primary_color': 'rgba(255, 235, 59, 1)',  # 较亮的黄色
                            'secondary_color': 'rgba(253, 216, 53, 1)'  # 较暗的黄色
                        },
                        500: {
                            'color_name': '橘色',
                            'css_color': '#FFA500',
                            'primary_color': 'rgba(255, 152, 0, 1)',  # 较亮的橘色
                            'secondary_color': 'rgba(245, 124, 0, 1)'  # 较暗的橘色
                        },
                        1000: {
                            'color_name': '洋红色',
                            'css_color': '#FF00FF',
                            'primary_color': 'rgba(233, 30, 99, 1)',  # 较亮的洋红色
                            'secondary_color': 'rgba(194, 24, 91, 1)'  # 较暗的洋红色
                        },
                        2000: {
                            'color_name': '红色',
                            'css_color': '#FF0000',
                            'primary_color': 'rgba(244, 67, 54, 1)',  # 较亮的红色
                            'secondary_color': 'rgba(229, 57, 53, 1)'  # 较暗的红色
                        }
                    }
                    thresholds = sorted(coin_color.keys())
                    matching_threshold = 0

                    for threshold in thresholds:
                        if amount >= threshold:
                            matching_threshold = threshold
                        else:
                            break

                    return coin_color[matching_threshold], matching_threshold

                # 送礼 (SEND_GIFT)
                contentdata = content['data']
                u_name = contentdata['uname']

                u_id = contentdata['uid']

                user_face_picture = f'./img/face/{re.split("/", contentdata["sender_uinfo"]["base"]["face"])[-1]}'
                if not os.path.exists(user_face_picture):
                    # 先检查返回值
                    result = url2pillow_image(contentdata["sender_uinfo"]["base"]["face"], Headers)
                    if result and "PilImg" in result and result["PilImg"] is not None:
                        pillow_img = result["PilImg"]
                        pillow_img.save(user_face_picture)
                        face_picture_x, face_picture_y = pillow_img.size
                    else:
                        print(f"无法获取图片: {result['Message']}")
                else:
                    pillow_img = Image.open(user_face_picture)
                    face_picture_x, face_picture_y = pillow_img.size
                if GlobalVariableOfData.face_picture_s:
                    face_picture_x, face_picture_y = GlobalVariableOfData.face_picture_s

                timestamp = contentdata["timestamp"]

                price = contentdata['total_coin'] / 1000

                message_bg_color, price_level = get_color_by_amount(int(price))

                message_primary_color = message_bg_color["primary_color"]

                message_secondary_color = message_bg_color["secondary_color"]

                message_header_color = 'rgba(0,0,0,1)'

                message_author_name_color = 'rgba(0,0,0,0.541176)'

                message_timestamp_color = 'rgba(0,0,0,0.501961)'

                message_color = 'rgba(0,0,0,1)'

                message_data = ""
                if contentdata['batch_combo_send']:  # 盲盒
                    message_data += contentdata['batch_combo_send']['action']  # 投喂
                    if contentdata['batch_combo_send']['blind_gift']:
                        contentdata_bcsb_g = contentdata['batch_combo_send']['blind_gift']
                        message_data += f"\t【{contentdata_bcsb_g['original_gift_name']}】"  # 盲盒名称
                        message_data += f"{contentdata_bcsb_g['gift_action']}"  # 爆出
                        actual_amount = contentdata_bcsb_g['gift_tip_price'] * contentdata['num'] / 1000  # 实际金额
                        consumption_amount = contentdata['total_coin'] / 1000  # 消费金额
                        profit_and_loss = f"\t({round((actual_amount - consumption_amount), 3)}￥)"  # 盲盒盈亏
                        message_data += f"《{contentdata['batch_combo_send']['gift_name']}》X {contentdata['num']}个\t{profit_and_loss}"
                    else:
                        message_data += f"《{contentdata['batch_combo_send']['gift_name']}》X {contentdata['num']}个"
                else:
                    message_data += f"{contentdata['action']}《{contentdata['giftName']}》X {contentdata['num']}个"

                show_only_header = False

                # -=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
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
                        coin = f"{contentdata_bcsb_g['gift_tip_price'] * contentdata['num'] / 1000}￥\t{(contentdata_bcsb_g['gift_tip_price'] * contentdata['num'] - contentdata['total_coin']) / 1000}￥"
                    else:
                        coin = f"{contentdata['total_coin'] * contentdata['num'] / 1000}￥"

                    tfo += f"{contentdata['num']}个《{contentdata['batch_combo_send']['gift_name']}》\t{coin}"
                else:
                    tfo += f"{contentdata['action']}{contentdata['num']}个《{contentdata['giftName']}》"
                print(f'🎁礼物：\t{wfo}{mfo}{ufo}\t{tfo}')
                # 转发到 WebSocket
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "gift",
                    "uName": u_name,
                    "uId": u_id,
                    "facePicture": user_face_picture,
                    "facePictureX": face_picture_x,
                    "facePictureY": face_picture_y,
                    "timestamp": timestamp,
                    "price": price,
                    "priceLevel": price_level,
                    "messagePrimaryColor": message_primary_color,
                    "messageSecondaryColor": message_secondary_color,
                    "messageHeaderColor": message_header_color,
                    "messageAuthorNameColor": message_author_name_color,
                    "messageTimestampColor": message_timestamp_color,
                    "messageColor": message_color,
                    "messageData": message_data,
                    "showOnlyHeader": show_only_header,

                    "user": ufo,
                    "medal": mfo,
                    "wealth": wfo,
                    "gift_name": contentdata.get('giftName', ''),
                    "gift_count": contentdata['num'],
                    "total_coin": contentdata['total_coin'],
                    "message": tfo
                }))

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "super_chat_jpn",
                    "user": uname,
                    "uid": uid,
                    "medal": mfo,
                    "price": price,
                    "message": message,
                    "duration": duration,
                    "timestamp": time.time()
                }))

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
                # asyncio.create_task(danmu_ws_server.send_danmu_message({
                #     "type": "playurl_reload",
                #     "room_id": room_id,
                #     "cid": cid,
                #     "protocols": protocol_list,
                #     "p2p_enabled": p2p_enabled,
                #     "scatter_time": scatter_time,
                #     "timestamp": time.time()
                # }))
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

                print(
                    f'🌟礼物星球：进度[{progress_str}] 状态[{finished}] 截止{datetime.datetime.fromtimestamp(ddl_time)}')

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
                asyncio.create_task(danmu_ws_server.send_danmu_message({
                    "type": "unknown",
                    "cmd": content['cmd'],
                    "data": content,
                    "timestamp": time.time()
                }))

        # 3. 启动弹幕客户端
        try:
            cdm.Callable_opt_code5 = danmu_processing

            # 启动弹幕客户端
            danmu_task = asyncio.create_task(cdm.start_async())

            print("弹幕系统启动完成，等待消息...")

            # 等待任意任务完成（通常是永久运行，直到被中断）
            await asyncio.gather(server_task, danmu_task)

        except KeyboardInterrupt:
            print("收到中断信号，正在关闭...")
        except Exception as e:
            print(f"程序异常: {e}")
        finally:
            # 清理资源
            await danmu_ws_server.stop_server_async()
            # 如果有弹幕客户端，也需要停止
            await cdm.stop_async()

    asyncio.run(show_danmu())











