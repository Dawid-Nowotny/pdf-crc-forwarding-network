import psutil
import asyncio
from fastapi import HTTPException, status

import subprocess
from typing import List

from src.constants import NODE_PORTS, COMMUNICATION_PORT
from src.schemas.PDFRequest import PDFRequest

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

    subprocess.Popen(
        ["cmd", "/c", "start", "python", "domain/node_runner.py", "Node_communication", str(COMMUNICATION_PORT), "--communication"]
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
    all_ports = list(NODE_PORTS.values()) + [COMMUNICATION_PORT]

    for port in all_ports:
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

def close_single_node(node_name: str) -> None:
    if node_name not in NODE_PORTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node '{node_name}' not found."
        )
    
    port = NODE_PORTS[node_name]
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
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to terminate process for {node_name} on port {port}: {str(e)}"
                )
            except psutil.TimeoutExpired:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Process for {node_name} on port {port} did not terminate in the expected time."
                )
    
    if not closed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No listening process found for {node_name} on port {port}."
        )

def validate_pdf_request(admin_node: str, target_node: str, polynomial: str) -> PDFRequest:
    try:
        return PDFRequest(admin_node=admin_node, target_node=target_node, polynomial=polynomial)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )