import asyncio
import websockets

# 存储所有连接的客户端
connected_clients = set()

async def echo(websocket):
    # 添加客户端到集合
    connected_clients.add(websocket)
    try:
        # 持续接收消息
        async for message in websocket:
            # 广播消息给所有客户端
            await broadcast(message)
    finally:
        # 客户端断开连接时移除
        connected_clients.remove(websocket)

async def broadcast(message):
    # 向所有连接的客户端发送消息
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

async def main():
    # 启动 WebSocket 服务器
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket 服务器已启动，地址: ws://localhost:8765")
        await asyncio.Future()  # 保持服务器运行

if __name__ == "__main__":
    asyncio.run(main())
