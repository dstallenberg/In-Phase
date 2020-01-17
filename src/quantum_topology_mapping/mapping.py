from src.quantum_topology_mapping.dijkstra import Graph
import numpy as np

def map_to_topology(graph):
    return graph.dijkstra("8", "0")

graph = Graph([])
Graph.add_edge(graph,"0","1")
Graph.add_edge(graph,"0","3")
Graph.add_edge(graph,"1","2")
Graph.add_edge(graph,"1","4")
Graph.add_edge(graph,"2","5")
Graph.add_edge(graph,"3","4")
Graph.add_edge(graph,"3","6")
Graph.add_edge(graph,"4","5")
Graph.add_edge(graph,"4","7")
Graph.add_edge(graph,"5","8")
Graph.add_edge(graph,"6","7")
Graph.add_edge(graph,"7","8")


path = list(map_to_topology(graph))
print(path)