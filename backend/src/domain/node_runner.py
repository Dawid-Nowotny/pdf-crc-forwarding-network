import asyncio

import sys
import argparse

from NodeAdmin import NodeAdmin
from NodePC import NodePC
from CommunicationWebSocket import CommunicationWebSocket
from network import create_network

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("--admin", action="store_true")
    parser.add_argument("--communication", action="store_true")
    return parser.parse_args()

async def run_node() -> None:
    args = parse_args()
    network = create_network()

    if args.communication:
        communication_ws = CommunicationWebSocket(port=args.port)
        await communication_ws.start_server()
        return

    node_class = NodeAdmin if args.admin else NodePC
    node = node_class(args.name, args.port, network)
    await node.start_server()

if __name__ == "__main__":
    node_name = sys.argv[1]
    port = int(sys.argv[2])
    asyncio.run(run_node())