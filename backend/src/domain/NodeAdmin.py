from Node import Node
from Graph import Graph

class NodeAdmin(Node):
    def __init__(self, name: str, port: int, graph: Graph):
        super().__init__(name, port, graph)
        print(port)

    async def handle_connection(self):
        pass