import aiohttp
from websockets import WebSocketServerProtocol

import json

from Node import Node
from Graph import Graph

class NodePC(Node):
    def __init__(self, name: str, port: int, graph: Graph):
        super().__init__(name, port, graph)
        print(f"Server started at ws://localhost:{port}")

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        async for message in websocket:
            data = json.loads(message)
            pdf_encoded = data.get("pdf_content")
            target_node = data.get("target_node")

            if self.name == target_node:
                self.read_pdf_content(pdf_encoded)
                print("Final destination reached, PDF received successfully.")
                return
            
            path = self.graph.dijkstra(self.name, target_node)
            if path and len(path) > 1:
                next_node = path[1]
                await self.send_to_next_node(pdf_encoded, target_node, next_node)
            else:
                print("Error: No valid path found from this node.")