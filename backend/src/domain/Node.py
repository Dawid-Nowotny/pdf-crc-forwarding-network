import asyncio
import aiohttp
import websockets
from pypdf import PdfReader

from io import BytesIO

from Graph import Graph
from CRC import CRC

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.constants import NODE_PORTS

class Node:
    def __init__(self, name: str, port: int, graph: Graph):
        self.name = name
        self.port = port
        self.graph = graph
        self.crc_calculator = CRC()

    async def start_server(self) -> None:
        async with websockets.serve(self.handle_connection, "localhost", self.port):
            await asyncio.Future()

    async def send_to_next_node(self, pdf_encoded: str, target_node: str, next_node: str, polynomial: str, crc_value: int) -> None:
        node_port = NODE_PORTS[next_node]
        ws_url = f"ws://localhost:{node_port}/pdf-transfer"
        
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(ws_url) as ws:
                await ws.send_json({
                    "pdf_content": pdf_encoded,
                    "target_node": target_node,
                    "polynomial": polynomial,
                    "crc_value": crc_value
                })
                print(f"Sent PDF to next node: {next_node}")

    def verify_and_calculate_crc(self, pdf_bytes: bytes, polynomial: str, received_crc_value: int = None) -> bool:
        crc_function = self.crc_calculator.get_crc_function(polynomial)
        calculated_crc_value = crc_function(polynomial, pdf_bytes)
        
        if received_crc_value is not None:
            if calculated_crc_value != received_crc_value:
                print(f"Error: CRC verification failed at node {self.name}. The PDF content may be corrupted.")
                return False
            print(f"CRC verification successful at node {self.name}.")
        
        return calculated_crc_value
    
    def read_pdf_content(self, pdf_bytes: bytes) -> None:
        with BytesIO(pdf_bytes) as pdf_file:
            reader = PdfReader(pdf_file)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text()

        print(f"Received PDF content: {text_content}")