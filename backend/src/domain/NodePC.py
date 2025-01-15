from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError

import json
import base64

from Node import Node
from Graph import Graph

class NodePC(Node):
    def __init__(self, name: str, port: int, graph: Graph):
        super().__init__(name, port, graph)
        print(f"Server started at ws://localhost:{port}")

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        try:
            async for message in websocket:
                data = json.loads(message)
                pdf_encoded = data.get("pdf_content")
                target_node = data.get("target_node")
                polynomial = data.get("polynomial")
                received_crc_value = data.get("crc_value")

                if received_crc_value is None:
                    error_message = {
                        "node": self.name,
                        "status": "ERROR",
                        "details": {
                            "message": "The PDF has not been signed by the administrator.",
                            "suggestion": "Select a proper administrator to sign the PDF."
                        }
                    }
                    await self.send_to_communication_port(error_message)
                    print("Error: Received PDF without administrator's signature.")
                    return

                pdf_bytes = base64.b64decode(pdf_encoded)
                crc_success = self.verify_and_calculate_crc(pdf_bytes, polynomial, received_crc_value)

                message_to_send = {
                    "node": self.name,
                    "status": "CRC_SUCCESS" if crc_success else "CRC_ERROR",
                    "details": {
                        "crc_value": received_crc_value,
                        "polynomial": polynomial,
                        "message": "Verification successful." if crc_success else "Verification failed."
                    }
                }
                await self.send_to_communication_port(message_to_send)

                if not crc_success:
                    return

                if self.name == target_node:
                    self.read_pdf_content(pdf_bytes)
                    print("Final destination reached, PDF received successfully.")
                    return
                
                path = self.graph.dijkstra(self.name, target_node)
                if path and len(path) > 1:
                    next_node = path[1]
                    await self.send_to_next_node(pdf_encoded, target_node, next_node, polynomial, received_crc_value)
                else:
                    print("Error: No valid path found from this node.")
        except ConnectionClosedError:
            message_to_send = {
                "node": self.name,
                "status": "ERROR",
                "details": {
                    "message": "Uploaded file is too large."
                }
            }
            await self.send_to_communication_port(message_to_send)