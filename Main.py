from copy import deepcopy
from pathlib import Path

from Graph import Graph

def get_graph_files(dir):
    graph_dir = Path(dir)
    return [f for f in graph_dir.iterdir() if f.is_file()]

def run_edmonds_karp(graph):
    max_flows, subgraphs = [], []
    for target in graph[1].targets:
        mf, subgraph = graph[1].edmonds_karp(0, target, graph[0])
        max_flows.append(mf)
        subgraphs.append(subgraph)
    return max_flows, subgraphs

def delete_path(g, subgraph, method, index):
    copy = deepcopy(subgraph)
    if method == 'first':
        copy[index] = g.orchestrate_deletion(copy[index], 'first')
    elif method == 'longest':
        copy[index] = g.orchestrate_deletion(copy[index], 'longest')
    elif method == 'random':
        copy[index] = g.orchestrate_deletion(copy[index], 'random')
    return list(map(g.build_subgraph, copy))

def multicast_graph(g, subgraphs, method, name):
    multicast_graph = g.build_multicast_graph(subgraphs)
    with open(f'logs/{name}.txt', 'a', encoding='utf-8') as f:
        f.write(f'Multicast Graph Matrix after {method} path deletion method:\n')
        for row in multicast_graph:
            f.write(f'{row}\n')
        f.write('\n')
    return multicast_graph

if __name__ == '__main__':
    logs_path = Path('logs')
    logs_path.mkdir(parents=True, exist_ok=True)

    ignored_files = ('example_01', 'example_02', 'example_03')
    graphs = [[file.stem, Graph(file.absolute())] for file in get_graph_files('./graph_examples') if file.stem not in ignored_files]

    print("Running Modified Edmonds-Karp Algorithm...")

    for graph in graphs:
        print(f"Running graph {graph[0]}...")
        with open(f'{logs_path/graph[0]}.txt', 'w', encoding='utf-8') as f:
            f.write('Modified Edmonds-Karp Algorithm\n\n')
        max_flows, subgraphs = run_edmonds_karp(graph)
        min_max_flow = min(max_flows)
        with open(f'{logs_path/graph[0]}.txt', 'a', encoding='utf-8') as f:
            f.write(f'Maximun flows: {max_flows}, minimal maximun flow: {min_max_flow}\n\n')

        index = next((i for i, max_flow in enumerate(max_flows) if max_flow > min_max_flow), -1)
        if index != -1:
            for i, subgraph in enumerate(subgraphs):
                if max_flows[i] > min_max_flow:
                    f_subgraph = delete_path(graph[1], subgraphs, 'first', i)
                    l_subgraph = delete_path(graph[1], subgraphs, 'longest', i)
                    r_subgraph = delete_path(graph[1], subgraphs, 'random', i)

                    with open(f'{logs_path/graph[0]}.txt', 'a', encoding='utf-8') as f:
                        f.write("Deletion Methods\n\n")
                        f.write(f'Subgraph with s: {0} and t: {graph[1].targets[i]} after first path deletion:\n')
                        for row in f_subgraph[i]:
                            f.write(f'{row}\n')
                        f.write('\n')
                        f.write(f'Subgraph with s: {0} and t: {graph[1].targets[i]} after longest path deletion:\n')
                        for row in l_subgraph[i]:
                            f.write(f'{row}\n')
                        f.write('\n')
                        f.write(f'Subgraph with s: {0} and t: {graph[1].targets[i]} after random path deletion:\n')
                        for row in r_subgraph[i]:
                            f.write(f'{row}\n')
                        f.write('\n')

            with open(f'{logs_path/graph[0]}.txt', 'a', encoding='utf-8') as f:
                f.write('Multicast Graphs\n\n')

            d_first_path_multicast_graph = multicast_graph(graph[1], f_subgraph, 'first', graph[0])
            d_longest_path_multicast_graph = multicast_graph(graph[1], l_subgraph, 'longest', graph[0])
            d_random_path_multicast_graph = multicast_graph(graph[1], r_subgraph, 'random', graph[0])

            graph[1].multicast_graph_to_file(f'{graph[0]}-PrimerCamino', d_first_path_multicast_graph, min_max_flow)
            graph[1].multicast_graph_to_file(f'{graph[0]}-CaminoMasLargo', d_longest_path_multicast_graph, min_max_flow)
            graph[1].multicast_graph_to_file(f'{graph[0]}-CaminoAleatorio', d_random_path_multicast_graph, min_max_flow)
        else:
            no_del_multicast_graph = graph[1].build_multicast_graph(list(map(graph[1].build_subgraph, subgraphs)))
            with open(f'{logs_path/graph[0]}.txt', 'a', encoding='utf-8') as f:
                f.write('Multicast Graphs\n\n')
                f.write('Multicast Graph Matrix without deletion method:\n')
                for row in no_del_multicast_graph:
                    f.write(f'{row}\n')
                f.write('\n')
            graph[1].multicast_graph_to_file(f'{graph[0]}-NoAplica', no_del_multicast_graph, min_max_flow)
        print(f"Graph {graph[0]} finished!")