import heapq

class Graph:
    def __init__(self):
        self.nodes = {}
    
    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.nodes:
            self.nodes[node1] = []
        if node2 not in self.nodes:
            self.nodes[node2] = []
        self.nodes[node1].append((node2, weight))
        self.nodes[node2].append((node1, weight))
    
    def dijkstra(self, start, end):
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