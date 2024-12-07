import json
from websockets.server import serve, WebSocketServerProtocol

class CommunicationWebSocket:
    def __init__(self, port: int):
        self.port = port
        self.messages = []
        self.clients = set()

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")

        try:
            async for message in websocket:
                self.messages.append(message)
                print(f"Received: {message}")
                await self.broadcast(message)
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected: {websocket.remote_address}")

    async def broadcast(self, message: str):
        # Rozsyłaj wiadomość do wszystkich podłączonych klientów
        if self.clients:  # Jeśli są aktywni klienci
            for client in self.clients:
                try:
                    await client.send(json.dumps({"log": message}))
                except Exception as e:
                    print(f"Error sending message to client: {e}")

    async def start_server(self):
        server = await serve(self.handle_connection, "localhost", self.port)
        print(f"Communication WebSocket started at ws://localhost:{self.port}")
        await server.wait_closed()