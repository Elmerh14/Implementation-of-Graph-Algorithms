import sys
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Graph class represents a directed weighted graph using adjacency lists and distance mapping
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        # Add edges in both directions since it's an undirected graph
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

    def initializeDistances(self):
        #initialize all pairs with maxsize for future use
        for i in self.nodes:
            for j in self.nodes:
                self.distances[(i, j)] = sys.maxsize
            self.distances[(i, "")] = 0

def dijkstra(graph, start):
    visited = {start: 0}
    path = {}
    nodes = set(graph.nodes)
    output = []

    while nodes:
        #find unvisited node with smallest distance
        min_node = None
        for node in nodes:
            if node in visited and (min_node is None or visited[node] < visited[min_node]):
                min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        #reconstruct the path from start to min_node
        route = [min_node]
        while route[-1] in path:
            route.append(path[route[-1]])
        route.reverse()

        output.append(f"Distance from {start} to '{min_node}': {visited[min_node]} with path({ ' to '.join(route) })")

        #update distances to neighbors
        for neighbor in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, neighbor)]
            if neighbor not in visited or weight < visited[neighbor]:
                visited[neighbor] = weight
                path[neighbor] = min_node

    return output

def primMST(graph, start):
    key = {node: sys.maxsize for node in graph.nodes} #min edge weight to node
    parent = {node: None for node in graph.nodes}     #parent node in MST
    mstSet = {node: False for node in graph.nodes}    #MST inclusion flag

    key[start] = 0
    total_cost = 0
    mst_edges = []

    for _ in range(len(graph.nodes)):
        # pick a node not yet in MST with minimum key value
        u = min((node for node in graph.nodes if not mstSet[node]), key=lambda x: key[x], default=None)
        if u is None:
            break
        mstSet[u] = True

        #add edge to MST if its not the starting node
        if parent[u] is not None:
            mst_edges.append((parent[u], u, graph.distances[(parent[u], u)]))
            total_cost += graph.distances[(parent[u], u)]

        #update key values for adjacent vertices
        for v in graph.edges[u]:
            if not mstSet[v] and graph.distances[(u, v)] < key[v]:
                key[v] = graph.distances[(u, v)]
                parent[v] = u

    return mst_edges, total_cost

def build_graph():
    g = Graph()
    cities = [
        'Atlanta', 'Boston', 'Chicago', 'Dallas', 'Denver', 'Houston',
        'LA', 'Memphis', 'Miami', 'NY', 'Philadelphia', 'Phoenix', 'SF', 'Seattle', 'Washington'
    ]
    for city in cities:
        g.add_node(city)
    g.initializeDistances()

    edges = [
        ('Seattle', 'SF', 1092), ('Seattle', 'LA', 1544), ('LA', 'SF', 559), ('LA', 'Houston', 2205),
        ('LA', 'Denver', 1335), ('LA', 'NY', 3933), ('LA', 'Miami', 3755), ('Denver', 'Dallas', 1064),
        ('Denver', 'Boston', 2839), ('Denver', 'Memphis', 1411), ('Denver', 'Chicago', 1474),
        ('Chicago', 'Boston', 1367), ('Chicago', 'NY', 1145), ('Boston', 'NY', 306), ('Boston', 'Atlanta', 1505),
        ('Atlanta', 'Dallas', 1157), ('Dallas', 'Houston', 362), ('Atlanta', 'Miami', 973), ('Atlanta', 'SF', 3434),
        ('Dallas', 'Memphis', 675), ('Memphis', 'Philadelphia', 1413), ('Miami', 'Phoenix', 3182),
        ('Miami', 'Washington', 1487), ('Phoenix', 'NY', 3441), ('Phoenix', 'Chicago', 2332), ('Phoenix', 'Dallas', 1422),
        ('Philadelphia', 'Washington', 199), ('Philadelphia', 'Phoenix', 3342), ('Washington', 'Dallas', 1900),
        ('Washington', 'Denver', 2395)
    ]
    for from_city, to_city, dist in edges:
        g.add_edge(from_city, to_city, dist)
    return g

#optional plotting of city graph for a visualization
def plot_mst(mst_edges):
    city_positions = {
        'Seattle': (-123, 48), 'SF': (-122, 37), 'LA': (-118, 34), 'Phoenix': (-112, 33),
        'Denver': (-104, 39), 'Dallas': (-96.8, 32.8), 'Houston': (-95, 29.7), 'Chicago': (-87.6, 41.8),
        'Memphis': (-90, 35), 'Atlanta': (-84.4, 33.7), 'Miami': (-80.2, 25.8),
        'Washington': (-77, 38.9), 'Philadelphia': (-75.1, 39.9), 'NY': (-74, 40.7), 'Boston': (-71, 42.3)
    }

    G = nx.Graph()
    G.add_nodes_from(city_positions)
    G.add_edges_from([(u, v) for u, v, _ in mst_edges])

    plt.figure(figsize=(14, 10))
    nx.draw(
        G,
        pos=city_positions,
        with_labels=True,
        node_color='skyblue',
        edge_color='red',
        node_size=800,
        font_size=9,
        font_weight='bold'
    )
    plt.title("Minimum Spanning Tree from Denver (Prim's Algorithm) on USA Map")
    plt.axis('off')
    plt.show()

def main():
    graph = build_graph()

    print("==== Dijkstra's SSSP from Denver ====")
    for line in dijkstra(graph, "Denver"):
        print(line)

    print("\n==== Prim's MST from Denver ====")
    mst_edges, mst_cost = primMST(graph, "Denver")
    print(f"{'From':<15} {'To':<15} {'Weight'}")
    for from_city, to_city, weight in mst_edges:
        print(f"{from_city:<15} {to_city:<15} {weight}")
    print(f"\nTotal MST Cost: {mst_cost}")

    plot_mst(mst_edges)

if __name__ == "__main__":
    main()
