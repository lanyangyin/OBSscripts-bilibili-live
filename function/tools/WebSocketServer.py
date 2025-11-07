import asyncio
import json
import time
from typing import Set, Optional, Dict, Any, Callable

import websockets


class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.connected_clients: Set = set()
        self.server: Optional[websockets.WebSocketServer] = None
        self.danmu_processor = None
        self.running = False
        self._server_task: Optional[asyncio.Task] = None
        self.registerCallback: Callable = lambda clients_count : None
        """注册新的客户端连接回调, 参数为注册用户数量"""
        self.unregisterCallback: Callable = lambda clients_count : None
        """客户端断开回调, 参数为注册用户数量"""
        self.startServerCallback: Callable = lambda host, port: None
        """服务器启动回调, 参数为注册用户数量"""
        self.serverCancelledCallback: Callable = lambda : None
        """服务器取消回调, 无参"""
        self.serverErroCallback: Callable = lambda erroMessage: None
        """服务器错误回调, 参数为错误信息"""
        self.serverStopCallback: Callable = lambda : None
        """服务器停止回调, 无参"""


    async def register(self, websocket):
        """注册新的客户端连接"""
        self.connected_clients.add(websocket)
        self.registerCallback(len(self.connected_clients))

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
            self.unregisterCallback(len(self.connected_clients))

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
        self.startServerCallback(self.host, self.port)

        # 保持服务器运行
        await self.server.wait_closed()

    async def start_server(self):
        """启动服务器（包装方法）"""
        try:
            await self.start_server_async()
        except asyncio.CancelledError:
            self.serverCancelledCallback()
        except Exception as e:
            self.serverErroCallback(e)
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

        self.serverStopCallback()

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
            self.serverCancelledCallback()
