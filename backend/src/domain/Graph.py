import heapq

from typing import Optional, List

class Graph:
    def __init__(self):
        self.nodes = {}
    
    def add_edge(self, node1: str, node2: str, weight:int = 1) -> None:
        if node1 not in self.nodes:
            self.nodes[node1] = []
        if node2 not in self.nodes:
            self.nodes[node2] = []
        self.nodes[node1].append((node2, weight))
        self.nodes[node2].append((node1, weight))
    
    def dijkstra(self, start: str, end: str) -> Optional[List[str]]:
        queue = [(0, start, [])]
        visited = set()
        
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node in visited:
                continue
            path = path + [node]
            visited.add(node)
            if node == end:
                return path
            for (adjacent, weight) in self.nodes.get(node, []):
                if adjacent not in visited:
                    heapq.heappush(queue, (cost + weight, adjacent, path))
        
        return None