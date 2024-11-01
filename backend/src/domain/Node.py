import asyncio
import websockets

from Graph import Graph

class Node:
    def __init__(self, name: str, port: int, graph: Graph):
        self.name = name
        self.port = port
        self.graph = graph
        self.neighbors = [n for (n, _) in self.graph.nodes.get(self.name, [])]

    async def start_server(self) -> None:
        async with websockets.serve(self.handle_connection, "localhost", self.port):
            print(f"Server started at ws://localhost:{self.port}")
            await asyncio.Future()