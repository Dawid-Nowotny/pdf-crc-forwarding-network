from websockets import WebSocketServerProtocol

import json
import base64

from Node import Node
from Graph import Graph

class NodeAdmin(Node):
    def __init__(self, name: str, port: int, graph: Graph):
        super().__init__(name, port, graph)
        print(f"Server started at ws://localhost:{port}")

    async def handle_connection(self, websocket: WebSocketServerProtocol) -> None:
        async for message in websocket:
            data = json.loads(message)
            pdf_encoded = data.get("pdf_content")
            target_node = data.get("target_node")
            polynomial = data.get("polynomial")

            pdf_bytes = base64.b64decode(pdf_encoded)
            self.read_pdf_content(pdf_bytes)

            crc_value = self.verify_and_calculate_crc(pdf_bytes, polynomial)

            path = self.graph.dijkstra(self.name, target_node)
            if path and len(path) > 1:
                next_node = path[1]
                await self.send_to_next_node(pdf_encoded, target_node, next_node, polynomial, crc_value)
            else:
                print("Error: No valid path found to the target node.")