import networkx as nx
import pandas as pd

# Example distance matrix (symmetric)
distance_matrix = {
    ('Distribution_Center', 'Store1'): 10,
    ('Distribution_Center', 'Store2'): 15,
    ('Store1', 'Home1'): 5,
    ('Store1', 'Home2'): 8,
    ('Store2', 'Home1'): 6,
    ('Store2', 'Home2'): 7
}

# Create a graph
G = nx.Graph()

# Add edges with weights (distances)
for (source, target), weight in distance_matrix.items():
    G.add_edge(source, target, weight=weight)

# Function to find the shortest path
def find_best_route(home):
    # Determine the shortest path from distribution center and each store
    routes = {}
    for source in ['Distribution_Center', 'Store1', 'Store2']:
        try:
            path = nx.shortest_path(G, source=source, target=home, weight='weight')
            length = nx.shortest_path_length(G, source=source, target=home, weight='weight')
            routes[source] = (path, length)
        except nx.NetworkXNoPath:
            routes[source] = (None, float('inf'))

    # Find the best route with the minimum distance
    best_source = min(routes, key=lambda k: routes[k][1])
    return best_source, routes[best_source]

# Example usage for Home1
best_source, (path, distance) = find_best_route('Home1')
print(f"Best source for Home1: {best_source}")
print(f"Path: {path}, Distance: {distance}")
