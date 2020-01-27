from src.qasm_topology_mapper.dijkstra import Graph
import re


# array must consist of the index of qubits
def map_to_topology(array, qasm_code):
    qubit = re.compile(r'q\[\d+]')
    qubit_combo = re.compile(r'q\[\d+], q\[\d+]')
    qubit_toffoli = re.compile(r'q\[\d+], q\[\d+], q\[\d+]')

    graph = generate_graph_from_array(array)

    final_qasm = ''
    for line in qasm_code.splitlines():
        # toffoli check
        if qubit_toffoli.findall(line):
            parts = qubit_toffoli.split(line)

            qubits = re.findall(r'\d+', ''.join(qubit.findall(line)))

            # Find path
            path_c1 = graph.dijkstra(qubits[0], qubits[2])
            swaps_c1, reverse_c1, last_c1 = map_qubits(path_c1)

            # Find path
            path_c2 = graph.dijkstra(qubits[1], qubits[2])

            swaps_c2, reverse_c2, last_c2 = map_qubits(path_c2)

            if path_c1[len(path_c1) - 2] == path_c2[len(path_c2) - 2]:
                last_c1 = path_c1[len(path_c1) - 3]

            final_qasm += swaps_c1 + swaps_c2 + parts[0] + f'q[{last_c1}], q[{last_c2}], q[{qubits[2]}]' + parts[1] + '\n' + reverse_c2 + reverse_c1

            continue

        if not qubit_combo.findall(line):
            final_qasm += line + '\n'
            continue

        parts = qubit_combo.split(line)

        qubits = re.findall(r'\d+', ''.join(qubit.findall(line)))

        # Find path
        path = graph.dijkstra(qubits[0], qubits[1])
        swaps, reverse, last = map_qubits(path)
        final_qasm += swaps + parts[0] + f'q[{last}], q[{qubits[1]}]' + parts[1] + '\n' + reverse

    return final_qasm


def map_qubits(path):
    # They are next to each other
    if len(path) == 2:
        return '', '', path[len(path) - 2]

    swaps = []
    # make swaps per path point
    for index in range(1, len(path) - 1):
        d1 = path[index - 1]
        d2 = path[index]

        swaps.append(get_swap_code(d1, d2))

    return ''.join(swaps), ''.join(reversed(swaps)), path[len(path) - 2]

def get_swap_code(qubit1, qubit2):
    return f'SWAP q[{qubit1}], q[{qubit2}]\n'

def generate_graph_from_array(array):
    graph = Graph([])
    for edge in array:
        graph.add_edge(edge[0], edge[1], both_ends=True)

    return graph
