import asyncio
import aiohttp
import websockets
from pypdf import PdfReader

import base64
from io import BytesIO

from Graph import Graph

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.constants import NODE_PORTS

class Node:
    def __init__(self, name: str, port: int, graph: Graph):
        self.name = name
        self.port = port
        self.graph = graph

    async def start_server(self) -> None:
        async with websockets.serve(self.handle_connection, "localhost", self.port):
            await asyncio.Future()

    async def send_to_next_node(self, pdf_encoded: str, target_node: str, next_node: str) -> None:
        node_port = NODE_PORTS[next_node]
        ws_url = f"ws://localhost:{node_port}/pdf-transfer"
        
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(ws_url) as ws:
                await ws.send_json({
                    "pdf_content": pdf_encoded,
                    "target_node": target_node
                })
                print(f"Sent PDF to next node: {next_node}")
    
    def read_pdf_content(self, pdf_encoded: str) -> bytes:
        pdf_bytes = base64.b64decode(pdf_encoded)

        with BytesIO(pdf_bytes) as pdf_file:
            reader = PdfReader(pdf_file)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text()

        print(f"Received PDF content: {text_content}")