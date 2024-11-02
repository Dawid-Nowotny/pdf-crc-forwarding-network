from fastapi import HTTPException, status
import psutil

import subprocess
from typing import Dict, List

from src.constants import NODE_PORTS
from src.schemas.NodesRequest import NodesRequest

def get_open_ports() -> List[int]:
    active_ports = {conn.laddr.port for conn in psutil.net_connections(kind='tcp') if conn.status == psutil.CONN_LISTEN}
    open_ports = [port for port in NODE_PORTS.values() if port in active_ports]
    return open_ports

def start_websockets(admin_node: str) -> None: 
    open_ports = get_open_ports()

    if open_ports:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot start websockets: Ports already in use - {', '.join(map(str, open_ports))}"
        )

    for node_name, port in NODE_PORTS.items():
        subprocess.Popen(
            ["cmd", "/c", "start", "python", "domain/node_runner.py", node_name, str(port)]
            + (["--admin"] if node_name == admin_node else [])
        )

def check_if_ports_are_up():
    open_ports = get_open_ports()

    if not open_ports:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No active websocket ports available to send the PDF."
        )

def close_ports() -> None:
    failed_ports = []

    for port in NODE_PORTS.values():
        closed = False
        for conn in psutil.net_connections(kind='tcp'):
            if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                try:
                    process = psutil.Process(conn.pid)
                    process.terminate()
                    process.wait(timeout=3)
                    closed = True
                    break
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    failed_ports.append((port, str(e)))
                    closed = True
                except psutil.TimeoutExpired:
                    failed_ports.append((port, "Process did not terminate in the expected time."))
                    closed = True
        if not closed:
            failed_ports.append((port, "No listening process found."))

    if failed_ports:
        error_details = "; ".join([f"Port {port}: {error}" for port, error in failed_ports])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to close some ports: {error_details}"
        )
    
def validate_pdf_request(admin_node: str, target_node: str) -> NodesRequest:
    try:
        return NodesRequest(admin_node=admin_node, target_node=target_node)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )