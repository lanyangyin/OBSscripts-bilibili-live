import asyncio
import websockets
import json
import ssl
import pathlib
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketServer")


class WebSocketServer:
    def __init__(self, host='localhost', port=8765, use_ssl=False):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.connected_clients = set()

        if self.use_ssl:
            self.ssl_context = self._create_ssl_context()
        else:
            self.ssl_context = None

    def _create_ssl_context(self):
        """创建SSL上下文（用于wss://）"""
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        # 生成自签名证书（仅用于测试）
        # 生产环境请使用有效的CA签名证书
        try:
            ssl_context.load_cert_chain(
                pathlib.Path(__file__).with_name("localhost.pem"),
            )
        except Exception as e:
            logger.warning(f"无法加载SSL证书: {e}")
            logger.warning("将使用非加密连接")
            return None

        return ssl_context

    async def handle_connection(self, websocket):
        # path = websocket.path
        """处理WebSocket连接"""
        client_id = id(websocket)
        self.connected_clients.add(websocket)
        logger.info(f"客户端 {client_id} 已连接，总连接数: {len(self.connected_clients)}")

        try:
            # 发送欢迎消息
            welcome_msg = {
                "type": "system",
                "message": "连接成功！",
                "timestamp": datetime.now().isoformat(),
                "clients_count": len(self.connected_clients)
            }
            await websocket.send(json.dumps(welcome_msg))

            # 处理客户端消息
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_client_message(websocket, data, client_id)
                except json.JSONDecodeError:
                    error_msg = {
                        "type": "error",
                        "message": "无效的JSON格式",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(error_msg))

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"客户端 {client_id} 断开连接")
        finally:
            self.connected_clients.remove(websocket)
            logger.info(f"客户端 {client_id} 已移除，剩余连接数: {len(self.connected_clients)}")

    async def handle_client_message(self, websocket, data, client_id):
        """处理来自客户端的消息"""
        message_type = data.get("type", "unknown")

        if message_type == "ping":
            # 响应ping消息
            pong_msg = {
                "type": "pong",
                "timestamp": datetime.now().isoformat(),
                "client_id": client_id
            }
            await websocket.send(json.dumps(pong_msg))

        elif message_type == "broadcast":
            # 广播消息给所有客户端
            broadcast_msg = {
                "type": "broadcast",
                "from_client": client_id,
                "message": data.get("message", ""),
                "timestamp": datetime.now().isoformat()
            }
            await self.broadcast_message(broadcast_msg)

        elif message_type == "echo":
            # 回声消息
            echo_msg = {
                "type": "echo",
                "message": data.get("message", ""),
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(echo_msg))

        else:
            # 未知消息类型
            error_msg = {
                "type": "error",
                "message": f"未知的消息类型: {message_type}",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(error_msg))

    async def broadcast_message(self, message):
        """向所有连接的客户端广播消息"""
        if self.connected_clients:
            message_json = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_json) for client in self.connected_clients],
                return_exceptions=True
            )

    async def send_system_message(self, message):
        """发送系统消息"""
        system_msg = {
            "type": "system",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_message(system_msg)

    async def start_server(self):
        """启动WebSocket服务器"""
        if self.use_ssl and self.ssl_context:
            protocol = "wss"
            start_server = websockets.serve(
                self.handle_connection, self.host, self.port, ssl=self.ssl_context
            )
        else:
            protocol = "ws"
            start_server = websockets.serve(
                self.handle_connection, self.host, self.port
            )

        server = await start_server
        logger.info(f"WebSocket服务器启动在 {protocol}://{self.host}:{self.port}")

        # 定时发送示例消息
        asyncio.create_task(self.send_periodic_messages())

        return server

    async def send_periodic_messages(self):
        """定时发送示例消息"""
        counter = 0
        while True:
            await asyncio.sleep(30)  # 每30秒发送一次
            counter += 1

            periodic_msg = {
                "type": "periodic",
                "message": f"这是第 {counter} 条定时消息",
                "timestamp": datetime.now().isoformat(),
                "counter": counter
            }
            await self.broadcast_message(periodic_msg)


async def main():
    """主函数"""
    # 配置服务器
    server = WebSocketServer(
        host='localhost',  # 改为 '0.0.0.0' 允许外部访问
        port=8765,
        use_ssl=False  # 设为True启用wss://（需要SSL证书）
    )

    # 启动服务器
    await server.start_server()

    # 保持服务器运行
    await asyncio.Future()  # 永久运行


if __name__ == "__main__":
    asyncio.run(main())