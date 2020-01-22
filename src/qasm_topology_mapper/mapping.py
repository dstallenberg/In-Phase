from src.qasm_topology_mapper.dijkstra import Graph
import re


# array must consist of the index of qubits
def map_to_topology(array, qasm_code):
    qubit = re.compile(r'q\[\d]')
    qubit_combo = re.compile(r'q\[\d], q\[\d]')
    qubit_toffoli = re.compile(r'q\[\d], q\[\d], q\[\d]')

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
    return f'''CNOT q[{qubit1}], q[{qubit2}]
CNOT q[{qubit2}], q[{qubit1}]
CNOT q[{qubit1}], q[{qubit2}]
'''

def generate_graph_from_array(array):
    graph = Graph([])
    for edge in array:
        graph.add_edge(edge[0], edge[1], both_ends=True)

    return graph


graph = [['0', '1'],
         ['0', '3'],
         ['1', '2'],
         ['2', '5'],
         ['3', '4'],
         ['4', '5'],
         ['3', '6'],
         ['4', '7'],
         ['5', '8'],
         ['6', '7'],
         ['7', '8']]

qasm_code = '''
version 1.0

qubits 10

# Prepare qubits 
.preparation

prep_z q[0:8]

# Custom prepare
# No initialization given

# Create superposition
{ H q[0:7] | X q[8] }
# Apply controlled unitary operations
.controlled_unitary_operations
CNOT q[7], q[8]

# Apply inverse quantum phase estimation
.Inverse_Quantum_Fourier_Transform
CR q[7], q[0], -0.02454369260617026
CR q[7], q[1], -0.04908738521234052
CR q[7], q[2], -0.09817477042468103
CR q[7], q[3], -0.19634954084936207
CR q[7], q[4], -0.39269908169872414
CR q[7], q[5], -0.7853981633974483
CR q[7], q[6], -1.5707963267948966
CR q[6], q[0], -0.04908738521234052
CR q[6], q[1], -0.09817477042468103
CR q[6], q[2], -0.19634954084936207
CR q[6], q[3], -0.39269908169872414
CR q[6], q[4], -0.7853981633974483
CR q[6], q[5], -1.5707963267948966
CR q[5], q[0], -0.09817477042468103
CR q[5], q[1], -0.19634954084936207
CR q[5], q[2], -0.39269908169872414
CR q[5], q[3], -0.7853981633974483
CR q[5], q[4], -1.5707963267948966
CR q[4], q[0], -0.19634954084936207
CR q[4], q[1], -0.39269908169872414
CR q[4], q[2], -0.7853981633974483
CR q[4], q[3], -1.5707963267948966
CR q[3], q[0], -0.39269908169872414
CR q[3], q[1], -0.7853981633974483
CR q[3], q[2], -1.5707963267948966
CR q[2], q[0], -0.7853981633974483
CR q[2], q[1], -1.5707963267948966
CR q[1], q[0], -1.5707963267948966
H q[0:7]
'''

# map_to_topology(graph, qasm_code, 9)

