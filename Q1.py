from collections import defaultdict
import sys

#graph class represents a directed weighted graph using adjacency lists and distance mapping
class Graph:
    def __init__(self):
        self.nodes = set()                       # Set to hold all unique nodes
        self.edges = defaultdict(list)           # Dictionary to hold outgoing edges for each node
        self.distances = {}                      # Dictionary to store weights: (from_node, to_node) → weight

    #adds a node to the graph
    def add_node(self, value):
        self.nodes.add(value)

    #adds a directed edge from 'from_node' to 'to_node' with a given weight
    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, start):
    visited = {start: 0}       # Dictionary to hold shortest known distance from start to each node
    path = {}                  # Dictionary to track the previous node (π) for each node
    nodes = set(graph.nodes)   # Set of all unvisited nodes
    history = []               # List to log every step of the algorithm (for debugging/output)

    #loop until all nodes have been visited or are unreachable
    while nodes:
        min_node = None

        #select the unvisited node with the smallest known distance
        for node in nodes:
            if node in visited:
                if min_node is None or visited[node] < visited[min_node]:
                    min_node = node

        #if all remaining nodes are unreachable, exit loop
        if min_node is None:
            break

        #log the selected node and its current distance
        history.append(f"\nNode({min_node}) with Weight: {visited[min_node]} is added to the 'Visited' {set(visited.keys())}")

        #mark node as visited by removing it from the unvisited set
        nodes.remove(min_node)
        current_weight = visited[min_node]  # Get the current best-known distance

        # If there are no neighbors, log that and skip relaxation
        if not graph.edges[min_node]:
            history.append(f"  No unvisited outgoing edge from the node, {min_node}")
            continue

        # Check all neighbors of the current node
        for neighbor in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, neighbor)]  # Calculate new potential distance

            # Case 1: First time reaching this neighbor (no current distance exists)
            if neighbor not in visited:
                visited[neighbor] = weight             # Record new distance
                path[neighbor] = min_node              # Record previous node in path
                history.append(f"  Relaxed: vertex[{neighbor}]: OLD: Infinity, NEW: {weight}, Paths: {path}")

            # Case 2: Found a shorter path to this neighbor
            elif weight < visited[neighbor]:
                old = visited[neighbor]                # Store old distance for logging
                visited[neighbor] = weight             # Update to shorter distance
                path[neighbor] = min_node              # Update previous node
                history.append(f"  Relaxed: vertex[{neighbor}]: OLD: {old}, NEW: {weight}, Paths: {path}")

            # Case 3: No better path found
            else:
                history.append(f"  No edge relaxation is needed for node, {neighbor}")

    # Return final distance table, path table, and full history log
    return visited, path, history

def main():
   
    g = Graph()

    # Add graph nodes
    for node in ['A', 'B', 'C', 'D', 'E']:
        g.add_node(node)

   
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 4)
    g.add_edge('C', 'E', 5)
    g.add_edge('E', 'D', 1)

    visited, path, history = dijkstra(g, 'A')

    print("==== Relaxation History ====")
    for line in history:
        print(line)

    print("\n==== Final Results ====")
    print("Distances:", visited)
    print("Paths:", path)


if __name__ == "__main__":
    main()
