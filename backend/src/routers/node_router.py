from fastapi import APIRouter, UploadFile, Form, status

from src.services import node_service, pdf_service
from src.schemas.AdminNodeRequest import AdminNodeRequest

router = APIRouter()

@router.post("/start-websockets", status_code=status.HTTP_204_NO_CONTENT)
async def start_websockets(admin_node_request: AdminNodeRequest):
    node_service.start_websockets(admin_node_request.admin_node)

@router.delete("/stop-websockets", status_code=status.HTTP_204_NO_CONTENT)
def stop_websockets():
    node_service.close_ports()

@router.post("/send-pdf", status_code=status.HTTP_204_NO_CONTENT)
async def send_pdf_to_node(
    file: UploadFile,
    admin_node: str = Form(...),
    target_node: str = Form(...)
):
    node_request = node_service.validate_pdf_request(admin_node, target_node)
    await pdf_service.validate_pdf(file)