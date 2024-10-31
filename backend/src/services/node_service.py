from fastapi import HTTPException, status
import psutil

import subprocess

from src.constants import NODE_PORTS

def start_websockets() -> None:
    for node_name, port in NODE_PORTS.items():
        subprocess.Popen(["cmd", "/c", "start", "python", "domain/node_runner.py", node_name, str(port)])
        #subprocess.Popen(["cmd", "/k", "python", "domain/Node.py", node_name, str(port)])

def close_ports() -> None:
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
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to terminate process on port {port}: {e}"
                    )
                except psutil.TimeoutExpired:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Process on port {port} did not terminate in the expected time."
                    )
        if not closed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No listening processes found on port {port}."
            )