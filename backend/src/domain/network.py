from Graph import Graph

def create_network():
    network = Graph()
    network.add_edge('Node1', 'Node2')
    network.add_edge('Node1', 'Node3')
    network.add_edge('Node2', 'Node4')
    network.add_edge('Node3', 'Node5')
    network.add_edge('Node4', 'Node5')
    network.add_edge('Node5', 'Node6')
    network.add_edge('Node6', 'Node7')
    network.add_edge('Node7', 'Node8')
    network.add_edge('Node8', 'Node9')
    network.add_edge('Node9', 'Node10')
    network.add_edge('Node4', 'Node6')
    network.add_edge('Node5', 'Node7')
    network.add_edge('Node2', 'Node8')
    return network