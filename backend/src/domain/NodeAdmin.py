import json
import base64
from pypdf import PdfReader

from io import BytesIO
from Node import Node
from Graph import Graph

class NodeAdmin(Node):
    def __init__(self, name: str, port: int, graph: Graph):
        super().__init__(name, port, graph)
        print(port)

    async def handle_connection(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            pdf_encoded = data.get("pdf_content")
            target_node = data.get("target_node")

            pdf_bytes = base64.b64decode(pdf_encoded)

            with BytesIO(pdf_bytes) as pdf_file:
                reader = PdfReader(pdf_file)
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text()

            print(text_content)
            print(target_node)