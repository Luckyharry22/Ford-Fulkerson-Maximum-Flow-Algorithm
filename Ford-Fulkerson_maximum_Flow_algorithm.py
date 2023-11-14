# Importing libraries
from queue import Queue
import time

# ---------------------------------------------------- #
### Implementing Graph class
# ---------------------------------------------------- #
class Graph:
    # General functions

    # Initializing the graph
    def __init__(self, vertices = 0, matrix = None):
        self.vertices = vertices
        if matrix == None:
            self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        else:
            self.graph = [row[:] for row in matrix]

    # Get the number of vertices in the graph
    def length(self):
        return self.vertices
    
    # Add an edge to the graph
    def add_edge(self, u, v, weight):
        u = int(u) - 1
        v = int(v) - 1
        weight = int(weight)
        self.graph[u][v] = self.graph[v][u] = weight

    # Print the graph
    def print(self):
        for row in self.graph:
            for col in row:
                print(col, end=" ")
            print()
    
    # Get the path from source node to destination node (by using BFS or DFS)
    def getPath(self, source, destination, useBfs = True):
        if useBfs:
            return self.bfs(source, destination)
        else:
            return self.dfs(source, destination)

    # BFS search for path from source node to destination node
    def bfs(self, source, destination):
        visited = List(self.vertices, False)
        parent = List(self.vertices, -1)
        q = Queue()
        q.put(source)
        visited.list[source] = True
        while not q.empty():
            u = q.get()
            for v in range(self.vertices):
                if self.graph[u][v] > 0 and not visited.list[v]:
                    visited.list[v] = True
                    parent.list[v] = u
                    q.put(v)
                    if v == destination:
                        path = List(0, 0)
                        while v != -1:
                            path.append(v)
                            v = parent.list[v]
                        path.list.reverse()
                        return path.list
        return []
    
    # DFS search for path from source node to destination node
    def dfs(self, source, destination):
        visited = List(self.vertices, False)
        path = []
        res = self.dfsUtil(source, destination, visited, path)
        # print(res)
        return res

    # Util fuction to recursively find path in DFS search method
    def dfsUtil(self, source, destination, visited, path):
        visited.list[source] = True
        path.append(source)
        if source == destination:
            return path
        for v in range(self.vertices):
            if self.graph[source][v] > 0 and not visited.list[v]:
                new_path = self.dfsUtil(v, destination, visited, path)
                if len(new_path):
                    return new_path
        path.pop()
        return []
    
    # Util functio to remove negative edges from the graph
    def removeNegativeEdges(self):
        for i in range(self.vertices):
            for j in range(self.vertices):
                if self.graph[i][j] < 0:
                    self.graph[i][j] = 0



# ------------------------------------------------------------
# Define a general List class
# ------------------------------------------------------------
class List:
    def __init__(self, size, val):
        self.size = size
        self.list = [val] * size
    
    def append(self, val):
        self.list.append(val)
        self.size += 1

    def print_list(self):
        for i in range(self.size):
            print(self.list[i], end=" ")
        print()



# ------------------------------------------------------------
# Ford-Fulkerson Algorithm (to find maximum flow in a directed weighted graph)
# ------------------------------------------------------------
def FordFulkerson(graph, source, sink, useBfs = True):
 
        # Initially, the total flow is set to zero
        max_flow = 0

        # Array used to store path from source to sink
        path = []

        # Create a residual graph to store the final flow output graph
        res_flow_graph = Graph(graph.vertices)

        # Augment the flow while there is path from source to sink
        while True:
            # Get path from source to sink using BFS or DFS
            path = graph.getPath(source, sink, useBfs)
            if len(path) == 0:
                break

            # Find minimum capacity of the current path (determined by the minimum edge weight in the path)
            path_flow = float("Inf")
            i = len(path) - 1
            while(i != 0):
                path_flow = min (path_flow, graph.graph[path[i-1]][path[i]])
                i-=1
 
            # Add path flow to overall flow
            max_flow +=  path_flow
 
            # update residual capacities of the edges and reverse edges along the path
            v = 0
            while(v != len(path) - 1):
                # print(path[v])
                graph.graph[path[v]][path[v+1]] -= path_flow
                graph.graph[path[v+1]][path[v]] += path_flow

                # Update the residual graph
                res_flow_graph.graph[path[v]][path[v+1]] += path_flow
                res_flow_graph.graph[path[v+1]][path[v]] -= path_flow
                v += 1
        
        # Remove negative edges from the residual graph (as it would cotain negative edges due to adjustment of flow)
        res_flow_graph.removeNegativeEdges()

        # Return the maximum flow and the residual graph
        return [max_flow, res_flow_graph]



# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------
if __name__ == "__main__":

    # Taking input from file
    inp = open("input.txt", "r")
    n = int(inp.readline().split()[0])
    matrix = [[int(i) for i in line.split()] for line in inp.readlines()]

    # Creating the graphs
    g1 = Graph(vertices = n, matrix = matrix)
    g2 = Graph(vertices = n, matrix = matrix)

    # Initializing the start time
    start = time.time()

    # Get the maximum flow and residual flow graph (using BFS)
    max_flow_BFS, res_flow_graph_BFS = FordFulkerson(g1, 0, n-1, True)

    # Checkpoint the time for BFS algorithm
    check1 = time.time()

    # Get the maximum flow and residual flow graph (using DFS)
    max_flow_DFS, res_flow_graph_DFS = FordFulkerson(g2, 0, n-1, False)

    # Checkpoint the time for DFS algorithm
    check2 = time.time()

    # Print the results
    print(f"BFS (maximum flow value: {max_flow_BFS}; rutime: {(check1 - start) * 1000}ms)")
    res_flow_graph_BFS.print()
    
    print(f"DFS (maximum flow value: {max_flow_DFS}; rutime: {(check2 - check1) * 1000}ms)")
    res_flow_graph_DFS.print()