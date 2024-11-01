from fastapi import APIRouter, status

from src.services import node_service

router = APIRouter()

@router.post("/start-websockets", status_code=status.HTTP_204_NO_CONTENT)
async def start_websockets(admin_node: str):
    node_service.start_websockets(admin_node)

@router.delete("/stop-websockets", status_code=status.HTTP_204_NO_CONTENT)
def stop_websockets():
    node_service.close_ports()