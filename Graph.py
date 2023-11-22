from math import floor, log
import random
class Graph:
    """
    A class representing a graph.

    Attributes:
    - matrix: a matrix representing the graph
    - vertex: a list of vertices in the graph
    - edge: a dictionary representing the edges in the graph
    - target: a list of target vertices in the graph

    Methods:
    - __init__(self, matrix_path=None): initializes the Graph object
    - add_vertex(self, vertex): adds a vertex to the graph
    - add_neighbour(self, vertex, neighbour): adds a neighbour to a vertex in the graph
    - add_edge(self, source, target, capacity, flow=0, backward=False): adds an edge to the graph
    - build_graph_from_matrix(self, path): builds a graph from a matrix
    - breath_first_search(self, source, target): performs a breath first search on the graph
    - build_subgraph(self, paths): builds a subgraph matrix based on the given paths
    - build_multicast_graph(self, matrices): builds a multicast graph matrix based on the given matrices
    - delete_first_path(self, paths): deletes the first path of the list
    - delete_longest_path(self, paths): deletes the longest path of the list
    - delete_random_path(self, paths): deletes a random path of the list
    - edmonds_karp(self, source, target): performs the Edmonds-Karp algorithm on the graph
    - __str__(self): returns a string representation of the graph
    """

    def __init__(self, matrix_path=None):
        """
        Initializes the Graph object.

        Args:
        - matrix_path (str): the path to the matrix file (default: None)
        """
        self.matrix = []
        self.vertices = []
        self.edges = []
        self.targets = []

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
        self.vertices[vertex]['neighbours'].append(neighbour)

    def add_edge(self, source, target, capacity, flow=0, backward=False):
        """
        Adds an edge to the graph.

        Args:
        - source (int): the name of the source vertex
        - target (int): the name of the target vertex
        - capacity (int): the capacity of the edge
        - flow (int): the flow of the edge (default: 0)
        - backward (bool): whether the edge is backward or not (default: False)
        """
        if source == target: return
        if not any(vertex['name'] == source for vertex in self.vertices):
            self.add_vertex(source)
        if not any(vertex['name'] == target for vertex in self.vertices):
            self.add_vertex(target)
        self.edges.append({'source': source, 'target': target, 'capacity': capacity, 'flow': flow})
        if not backward: self.add_neighbour(source, target)

    def build_graph_from_matrix(self, path):
        """
        Builds a graph from a matrix.

        Args:
        - path (str): the path to the matrix file
        """
        with open(path, 'r', encoding='utf-8') as f:
            _ = f.readline()
            self.targets = list(map(lambda n: n - 1, map(int, f.readline().split())))
            self.matrix = [list(map(int, lines.split())) for lines in f.readlines()]

        names = [i for i in range(len(self.matrix))]

        list(map(self.add_vertex, names))
        edges = [(names[i], names[j], c) for i, row in enumerate(self.matrix) for j, c in enumerate(row) if c > 0]
        list(map(lambda edge: self.add_edge(*edge), edges))
        backward_edges = [(names[j], names[i], 0) for i, row in enumerate(self.matrix) for j, c in enumerate(row) if c > 0]
        list(map(lambda edge: self.add_edge(*edge, backward=True), backward_edges))

    def breath_first_search(self, source, target, I=0):
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
                edge = next(edge for edge in self.edges if edge['source'] == current_vertex and edge['target'] == next_vertex)
                edge_capacity, edge_flow = edge['capacity'], edge['flow']
                residual_capacity = edge_capacity - edge_flow
                if not visited[next_vertex] and residual_capacity >= I:
                    visited[next_vertex] = True
                    if next_vertex == target:
                        return path + [next_vertex]
                    else:
                        queue.append((next_vertex, path + [next_vertex]))
        return None

    def build_subgraph(self, paths):
            """
            Builds a subgraph matrix based on the given paths.

            Args:
                paths (list): A list of paths.

            Returns:
                list: A subgraph matrix.
            """
            V = len(self.vertices)
            subgraph_matrix = [[0 for _ in range(V)] for _ in range(V)]
            for path in paths:
                for i in range(len(path) - 1):
                    u, v = path[i], path[i+1]
                    edge = next(edge for edge in self.edges if edge['source'] == u and edge['target'] == v)
                    subgraph_matrix[u][v] = edge['capacity']
            return subgraph_matrix

    def build_multicast_graph(self, matrices):
        """
        Builds a multicast graph from a list of matrices.

        Args:
            matrices (List[List[int]]): A list of matrices.

        Returns:
            List[List[int]]: The multicast graph.
        """
        return [[max(row) for row in zip(*matrix)] for matrix in zip(*matrices)]

    def delete_first_path(self, paths):
        """
        Deletes the first path of the list.

        Args:
            paths (list): A list of paths.

        Returns:
            list: A list of paths without the first path.
        """
        return paths[1:]

    def delete_longest_path(self, paths):
        """
        Deletes the longest path of the list.

        Args:
            paths (list): A list of paths.

        Returns:
            list: A list of paths without the longest path.
        """
        return sorted(paths, key=len)[1:]

    def delete_random_path(self, paths):
        """
        Deletes a random path of the list.

        Args:
            paths (list): A list of paths.

        Returns:
            list: A list of paths without a random path.
        """
        random.shuffle(paths)
        return paths[1:]

    def orchestrate_deletion(self, paths, method):
        """
        Orchestrates the deletion of a path.

        Args:
            paths (list): A list of paths.
            method (str): The method to use for deletion.

        Returns:
            list: A list of paths without a path.
        """
        if method == 'first':
            return self.delete_first_path(paths)
        elif method == 'longest':
            return self.delete_longest_path(paths)
        elif method == 'random':
            return self.delete_random_path(paths)
        else:
            return paths

    # TODO: Modified Edmonds-Karp algorithm is finding more paths than it should. Fix it.
    def edmonds_karp(self, source, target):
        """
        Performs the Edmonds-Karp algorithm on the graph.

        Args:
        - source (int): the name of the source vertex
        - target (int): the name of the target vertex

        Returns:
        - max_flow (int): the maximum flow of the graph
        """
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f'Subgraph with s: {source} and t: {target}\n')
        for edge in self.edges:
            edge['flow'] = 0
        subgraph = []
        max_flow = 0
        C = max([edge['capacity'] for edge in self.edges])
        I = 3 ** floor(log(C, 3))
        iteration = 0
        while I >= 1:
            path = self.breath_first_search(source, target, I)
            if not path:
                I //= 3
                continue
            subgraph.append(path)
            residual_capacity = []
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge = next(edge for edge in self.edges if edge['source'] == u and edge['target'] == v)
                residual_capacity.append(edge['capacity'] - edge['flow'])
            flow = min(residual_capacity)
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge = next(edge for edge in self.edges if edge['source'] == u and edge['target'] == v)
                backward_edge = next(edge for edge in self.edges if edge['source'] == v and edge['target'] == u)
                edge['flow'] += flow
                backward_edge['flow'] -= flow
            max_flow += flow
            iteration += 1
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(f'I: {I}, flow: {flow}, max_flow: {max_flow}, path # {iteration}: {path}\n')
            print(f'I: {I}, flow: {flow}, max_flow: {max_flow}, path # {iteration}: {path}')
        log_mat = self.build_subgraph(subgraph)
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f'Subgraph with s: {source} and t: {target} matrix:\n')
            for row in log_mat:
                f.write(f'{row}\n')
            f.write('\n')
        return max_flow, subgraph

    def __str__(self):
        """
        Returns a string representation of the graph.
        """
        return f'Vertices: {self.vertices}\nEdges: {self.edges}'


if __name__ == '__main__':
    # graph = Graph('./graph_examples/example_01.txt')
    # print(f"El flujo maximo del grafo 1 es de: {graph.edmonds_karp(0, 8)}") # Debe ser 72
    test_graph = Graph('./graph_examples/12grafo2fm1v3des.txt')
    with open('logs.txt', 'w', encoding='utf-8') as f:
            f.write('Modified Edmonds-Karp Algorithm\n\n')
    max_flows, subgraphs = [], []
    for target in test_graph.targets:
        mf, subgraph = test_graph.edmonds_karp(0, target)
        max_flows.append(mf)
        subgraphs.append(test_graph.build_subgraph(subgraph))
    min_max_flow = min(max_flows)
    print(f'Flujos maximos: {max_flows}, minimo flujo maximo: {min_max_flow}')
    for subgraph in subgraphs:
        if len(subgraphs) > min_max_flow:
            subgraph = test_graph.orchestrate_deletion(subgraph, 'first')
    multicast_graph = test_graph.build_multicast_graph(subgraphs)
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(f'Flujos maximos: {max_flows}, minimo flujo maximo: {min_max_flow}\n')
        f.write('Multicast Graph Matrix\n')
        for row in multicast_graph:
            f.write(f'{row}\n')