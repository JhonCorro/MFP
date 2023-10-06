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
        - vertex (str): the name of the vertex to add
        """
        self.vertices.append({'name': vertex, 'neighbours': []})

    def add_neighbour(self, vertex, neighbour):
        """
        Adds a neighbour to a vertex in the graph.

        Args:
        - vertex (str): the name of the vertex to add the neighbour to
        - neighbour (str): the name of the neighbour to add
        """
        for v in self.vertices:
            if v['name'] == vertex:
                v['neighbours'].append(neighbour)

    def add_edge(self, source, target, capacity):
        """
        Adds an edge to the graph.

        Args:
        - source (str): the name of the source vertex
        - target (str): the name of the target vertex
        - capacity (int): the capacity of the edge
        """
        renamed_source = f'v_{source}' if source.isdigit() else source
        renamed_target = f'v_{target}' if target.isdigit() else target
        if source == target: return
        if not any(vertex['name'] == renamed_source for vertex in self.vertices):
            self.add_vertex(renamed_source)
        if not any(vertex['name'] == renamed_target for vertex in self.vertices):
            self.add_vertex(renamed_target)
        self.edges[(renamed_source, renamed_target)] = capacity
        self.add_neighbour(renamed_source, renamed_target)

    def build_graph_from_matrix(self, path):
        """
        Builds a graph from a matrix.

        Args:
        - path (str): the path to the matrix file
        """
        with open(path, 'r', encoding='utf-8') as f:
            names = [f'v_{name.strip()}' if name.strip().isdigit() else name.strip() for name in f.readline().split(',')]
            matrix = [list(map(int, lines.split(','))) for lines in f.readlines()]

        list(map(self.add_vertex, names))
        edges = [(names[i], names[j], c) for i, row in enumerate(matrix) for j, c in enumerate(row) if c > 0]
        list(map(lambda edge: self.add_edge(*edge), edges))

    def breath_first_search(self, source, target):
        """
        Performs a breath first search on the graph.

        Args:
        - source (str): the name of the source vertex
        - target (str): the name of the target vertex

        Returns:
        - path (list): the path from the source to the target
        """
        queue = [(source, [source])]
        while queue:
            (current_vertex, path) = queue.pop(0)
            for next_vertex in set(next(vertex for vertex in self.vertices if vertex['name'] == current_vertex)['neighbours']) - set(path):
                if next_vertex == target:
                    return path + [next_vertex]
                else:
                    queue.append((next_vertex, path + [next_vertex]))

    def __str__(self):
        """
        Returns a string representation of the graph.
        """
        return f'Vertices: {self.vertices}\nEdges: {self.edges}'


if __name__ == '__main__':
    graph = Graph('./graph_examples/example_01.txt')
    print(graph.breath_first_search('s', 't'))