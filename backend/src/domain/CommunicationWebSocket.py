from websockets.server import serve, WebSocketServerProtocol

class CommunicationWebSocket:
    def __init__(self, port: int):
        self.port = port
        self.messages = []

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        async for message in websocket:
            self.messages.append(message)
            print(f"{message}")

    async def start_server(self):
        server = await serve(self.handle_connection, "localhost", self.port)
        print(f"Communication WebSocket started at ws://localhost:{self.port}")
        await server.wait_closed()