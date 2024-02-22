import os
from pathlib import Path
import shutil
import subprocess
import argparse

def get_cli_args():
    parser = argparse.ArgumentParser('Run solver script')
    parser.add_argument('input_dir', nargs='?', help='Directory with input files for the solver' )
    parser.add_argument('solver_name', nargs='?', help='Solver script name with extension')
    args = parser.parse_args()
    return args

def make_report(path):
    with open('report.csv', 'w') as report:
        report.write('Grafo;Metodo de eliminacion;Solucion;TieneSolucion?\n')
        for file in path.iterdir():
            graph_name, elimination_method, solution = file.name.replace('.out', '').split('-')[:-1]
            solution = 'Simple' if solution == 'sim' else 'Combinado'
            new_line = f'{graph_name};{elimination_method};{solution};'
            with open(file, 'r') as f:
                for line in f:
                    if 'ok' in line:
                        new_line += 'o'
                        break
                report.write(new_line + '\n')

if __name__ == '__main__':
    args = get_cli_args()

    INPUT_DIR = args.input_dir
    SOLVER_NAME = args.solver_name
    OUTPUT_DIR = Path('solver_output')

    os.chdir(INPUT_DIR)
    # shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # options = [['1', '0'], ['1', '1']]

    # print('Running solver...')

    # multicast_graph_files = [f.name for f in Path('.').iterdir() if f.is_file() and f.suffix == '.txt']
    # for graph in multicast_graph_files:
    #     for option in options:
    #         inputs = [graph, *option]
    #         process = subprocess.Popen([SOLVER_NAME], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #         stdout, stderr = process.communicate(input='\n'.join(inputs).encode())

    #         if process.returncode != 0:
    #             print(f"Error executing command: {stderr.decode()}")

    # print('Solver finished!')

    # output_files = [f for f in Path('.').iterdir() if f.is_file() and f.suffix == '.out']
    # list(map(lambda file: shutil.move(file, OUTPUT_DIR / file.name.replace('.txt', '')), output_files))

    print('Writing report...')
    make_report(OUTPUT_DIR)
    print('Report written successfully!')