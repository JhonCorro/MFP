from math import floor, log
class Graph:
    """
    A class representing a graph.

    Attributes:
    - vertex: a list of vertices in the graph
    - edge: a dictionary representing the edges in the graph

    Methods:
    - __init__(self, matrix_path=None): initializes the Graph object
    - add_vertex(self, vertex): adds a vertex to the graph
    - add_neighbour(self, vertex, neighbour): adds a neighbour to a vertex in the graph
    - add_edge(self, source, target, capacity): adds an edge to the graph
    - build_graph_from_matrix(self, path): builds a graph from a matrix
    - breath_first_search(self, source, target): performs a breath first search on the graph
    - edmonds_karp(self, source, target): performs the Edmonds-Karp algorithm on the graph
    - __str__(self): returns a string representation of the graph
    """

    def __init__(self, matrix_path=None):
        """
        Initializes the Graph object.

        Args:
        - matrix_path (str): the path to the matrix file (default: None)
        """
        self.vertices = []
        self.edges = {}

        if matrix_path:
            self.build_graph_from_matrix(matrix_path)

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph.

        Args:
        - vertex (int): the name of the vertex to add
        """
        self.vertices.append({'name': vertex, 'neighbours': []})

    def add_neighbour(self, vertex, neighbour):
        """
        Adds a neighbour to a vertex in the graph.

        Args:
        - vertex (int): the name of the vertex to add the neighbour to
        - neighbour (int): the name of the neighbour to add
        """
        [v['neighbours'].append(neighbour) for v in self.vertices if v['name'] == vertex]

    def add_edge(self, source, target, capacity, flow=0, backward=False):
        """
        Adds an edge to the graph.

        Args:
        - source (int): the name of the source vertex
        - target (int): the name of the target vertex
        - capacity (int): the capacity of the edge
        - flow (int): the flow of the edge (default: 0)
        """
        if source == target: return
        if not any(vertex['name'] == source for vertex in self.vertices):
            self.add_vertex(source)
        if not any(vertex['name'] == target for vertex in self.vertices):
            self.add_vertex(target)
        self.edges[(source, target)] = [capacity, flow]
        if not backward: self.add_neighbour(source, target)

    def build_graph_from_matrix(self, path):
        """
        Builds a graph from a matrix.

        Args:
        - path (str): the path to the matrix file
        """
        with open(path, 'r', encoding='utf-8') as f:
            matrix = [list(map(int, lines.split(','))) for lines in f.readlines()]

        names = [i for i in range(len(matrix))]

        list(map(self.add_vertex, names))
        edges = [(names[i], names[j], c) for i, row in enumerate(matrix) for j, c in enumerate(row) if c > 0]
        list(map(lambda edge: self.add_edge(*edge), edges))
        backward_edges = [(names[j], names[i], 0) for i, row in enumerate(matrix) for j, c in enumerate(row) if c > 0]
        list(map(lambda edge: self.add_edge(*edge, backward=True), backward_edges))

    # TODO: Modify to search for augmented paths with minimun capacity I
    def breath_first_search(self, source, target):
        """
        Performs a breath first search on the graph.

        Args:
        - source (int): the name of the source vertex
        - target (int): the name of the target vertex

        Returns:
        - path (list): the path from the source to the target
        """
        visited = {vertex['name']: False for vertex in self.vertices}
        queue = [(source, [source])]
        visited[source] = True

        while queue:
            (current_vertex, path) = queue.pop(0)
            for next_vertex in set(next(vertex for vertex in self.vertices if vertex['name'] == current_vertex)['neighbours']) - set(path):
                edge_capacity = self.edges[(current_vertex, next_vertex)][0]
                edge_flow = self.edges[(current_vertex, next_vertex)][1]
                if not visited[next_vertex] and edge_capacity > edge_flow:
                    visited[next_vertex] = True
                    if next_vertex == target:
                        return path + [next_vertex]
                    else:
                        queue.append((next_vertex, path + [next_vertex]))
        return None

    def edmonds_karp(self, source, target):
        """
        Performs the Edmonds-Karp algorithm on the graph.

        Args:
        - source (int): the name of the source vertex
        - target (int): the name of the target vertex

        Returns:
        - max_flow (int): the maximum flow of the graph
        """
        max_flow = 0
        while True:
            path = self.breath_first_search(source, target)
            if not path:
                break
            flow = min(self.edges[(path[i], path[i+1])][0] - self.edges[(path[i], path[i+1])][1] for i in range(len(path) - 1))
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                self.edges[(u, v)][1] += flow
                self.edges[(v, u)][1] -= flow
            max_flow += flow
            print(path)
        return max_flow

    def __str__(self):
        """
        Returns a string representation of the graph.
        """
        return f'Vertices: {self.vertices}\nEdges: {self.edges}'


if __name__ == '__main__':
    graph = Graph('./graph_examples/example_01.txt')
    print(f"El flujo maximo del grafo 1 es de: {graph.edmonds_karp(0, 8)}") # Debe ser 72
    graph = Graph('./graph_examples/example_02.txt') # Debe ser 19
    print(f"El flujo maximo del grafo 2 es de: {graph.edmonds_karp(0, 5)}")
    graph = Graph('./graph_examples/example_03.txt') # Debe ser 15
    print(f"El flujo maximo del grafo 3 es de: {graph.edmonds_karp(0, 5)}")