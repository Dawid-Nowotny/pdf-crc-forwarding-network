import asyncio

import sys

from Node import Node
from network import create_network

async def run_node(node_name, port):
    network = create_network()
    node = Node(node_name, port, network)
    await node.start_server()

if __name__ == "__main__":
    node_name = sys.argv[1]
    port = int(sys.argv[2])
    asyncio.run(run_node(node_name, port))