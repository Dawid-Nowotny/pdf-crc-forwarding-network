from fastapi import HTTPException, UploadFile, status
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import aiohttp

import io
import base64

from src.constants import NODE_PORTS

async def validate_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are allowed."
        )

    file_content = await file.read()
    if not file_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded PDF file is empty."
        )
    
    try:
        PdfReader(io.BytesIO(file_content))
    except PdfReadError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF."
        )
    
async def pdf_transfer(file: UploadFile, admin_node: str, target_node: str) -> None:
    admin_port = NODE_PORTS[admin_node]
    ws_url = f"ws://localhost:{admin_port}/pdf-transfer"
    
    file_content = await file.read()
    encoded_pdf = base64.b64encode(file_content).decode('utf-8')

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            await ws.send_json({
                "pdf_content": encoded_pdf,
                "target_node": target_node
            })