from src.quantum_topology_mapping.dijkstra import Graph


def map_to_topology(graph):
    print(graph.dijkstra("a", "e"))

graph = Graph([
        ("a", "b", 7), ("a", "c", 9), ("a", "f", 14), ("b", "c", 10),
        ("b", "d", 15), ("c", "d", 11), ("c", "f", 2), ("d", "e", 6),
        ("e", "f", 9)])

map_to_topology(graph)