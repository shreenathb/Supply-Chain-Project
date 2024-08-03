import networkx as nx
import pandas as pd

df = pd.read_csv('dist_matrix.csv')
G = nx.Graph()


for index , row in df.iterrows():
    if(row["From"]==row["To"]):
        continue
    if (row["From"] >= 8 and row["From"]<= 12):
        continue
    G.add_edge(row["From"], row["To"], weight=row["Time"])

def find_best_route(home):
    # Determine the shortest path from distribution center and each store
    routes = {}
    for source in range(1,8):
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
best_source, (path, distance) = find_best_route(10)
print(f"Best source: {best_source}")
print(f"Path: {path}, Distance: {distance}")