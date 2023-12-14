import os
from pathlib import Path
import shutil
import subprocess

INPUT_DIR = 'multicast_graphs'
os.chdir(INPUT_DIR)

OUTPUT_DIR = Path('solver_output')
shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SOLVER_NAME = 'multicast_graph_solver.exe'

def make_report(path):
    with open('report.csv', 'w') as report:
        report.write('Grafo;Metodo de eliminacion;Representacion;Simple o Combinado\n')
        for file in path.iterdir():
            text = file.name.replace('.out', '').split('_')
            last_elem = text.pop(-1).split('-')
            text[1] = f'{text[1]}_{last_elem.pop(0)}'
            text.extend(last_elem)

            graph_name = text[0]
            elimination_method = 'Primer camino' if text[1] == 'first_path' else 'Camino mas largo' if text[1] == 'longest_path' else 'Camino aleatorio'
            simple_combination = 'Simple' if text[2] == 'sim' else 'Combinado'
            representation = 'Letras' if text[3] == 'let' else 'Vectores binarios'

            print(f'{graph_name};{elimination_method};{representation};{simple_combination}')
            report.write(f'{graph_name};{elimination_method};{representation};{simple_combination}\n')

options = ['0', '1']
options_permutation = [[i, j] for i in options for j in options]

multicast_graph_files = [f.name for f in Path('.').iterdir() if f.is_file() and f.suffix == '.txt']
for graph in multicast_graph_files:
    for option in options_permutation:
        inputs = [graph, *option]
        process = subprocess.Popen([SOLVER_NAME], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input='\n'.join(inputs).encode())

        if process.returncode != 0:
            print(f"Error executing command: {stderr.decode()}")

output_files = [f for f in Path('.').iterdir() if f.is_file() and f.suffix == '.out']
list(map(lambda file: shutil.move(file, OUTPUT_DIR / file.name.replace('.txt', '')), output_files))

make_report(OUTPUT_DIR)