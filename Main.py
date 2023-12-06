from copy import deepcopy
from Graph import Graph

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
        subgraphs.append(subgraph)
    min_max_flow = min(max_flows)
    print(f'Maximun flows: {max_flows}, minimal maximun flow: {min_max_flow}')
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(f'Maximun flows: {max_flows}, minimal maximun flow: {min_max_flow}\n\n')
        f.write("Deletion Methods\n\n")
    f_subgraphs = deepcopy(subgraphs)
    l_subgraphs = deepcopy(subgraphs)
    r_subgraphs = deepcopy(subgraphs)
    for i, subgraph in enumerate(subgraphs):
        if max_flows[i] > min_max_flow:
            f_subgraphs[i] = test_graph.orchestrate_deletion(subgraph, 'first')
            d_first_path_subgraph = list(map(test_graph.build_subgraph, f_subgraphs))
            # d_first_path_subgraph = test_graph.build_subgraph(f_subgraphs)
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(f'Subgraph with s: {0} and t: {test_graph.targets[i]} after first path deletion:\n')
                for row in d_first_path_subgraph[i]:
                    f.write(f'{row}\n')
                f.write('\n')
            l_subgraphs[i] = test_graph.orchestrate_deletion(subgraph, 'longest')
            d_longest_path_subgraph = list(map(test_graph.build_subgraph, l_subgraphs))
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(f'Subgraph with s: {0} and t: {test_graph.targets[i]} after longest path deletion:\n')
                for row in d_longest_path_subgraph[i]:
                    f.write(f'{row}\n')
                f.write('\n')
            r_subgraphs[i] = test_graph.orchestrate_deletion(subgraph, 'random')
            d_random_path_subgraph = list(map(test_graph.build_subgraph, r_subgraphs))
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(f'Subgraph with s: {0} and t: {test_graph.targets[i]} after random path deletion:\n')
                for row in d_random_path_subgraph[i]:
                    f.write(f'{row}\n')
                f.write('\n')
    # TODO: Save multicast graph to text file with the testing app format
    d_first_path_multicast_graph = test_graph.build_multicast_graph(d_first_path_subgraph)
    d_longest_path_multicast_graph = test_graph.build_multicast_graph(d_longest_path_subgraph)
    d_random_path_multicast_graph = test_graph.build_multicast_graph(d_random_path_subgraph)
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write('Multicast Graphs\n\n')
        f.write('Multicast Graph Matrix with first path deletion method:\n')
        for row in d_first_path_multicast_graph:
            f.write(f'{row}\n')
        f.write('\n')
        f.write('Multicast Graph Matrix with longest path deletion method:\n')
        for row in d_longest_path_multicast_graph:
            f.write(f'{row}\n')
        f.write('\n')
        f.write('Multicast Graph Matrix with random path deletion method:\n')
        for row in d_random_path_multicast_graph:
            f.write(f'{row}\n')
    test_graph.multicast_graph_to_file('12grafo2fm1v3des_first_path', d_first_path_multicast_graph, min_max_flow)
    test_graph.multicast_graph_to_file('12grafo2fm1v3des_longest_path', d_longest_path_multicast_graph, min_max_flow)
    test_graph.multicast_graph_to_file('12grafo2fm1v3des_random_path', d_random_path_multicast_graph, min_max_flow)