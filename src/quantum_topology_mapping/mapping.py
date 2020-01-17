from src.quantum_topology_mapping.dijkstra import Graph
import re


def map_to_topology(graph, qasm_code):
    qubit = re.compile(r'q\[\d]')
    qubit_combo = re.compile(r'q\[\d], q\[\d]')
    qubit_toffoli = re.compile(r'q\[\d], q\[\d], q\[\d]')

    for line in qasm_code.splitlines():
        # TODO toffoli check
        if not qubit_combo.findall(line):
            continue

        parts = qubit_combo.split(line)

        qubits = re.findall(r'\d+', ''.join(qubit.findall(line))) # [int(s) for s in re.findall(r'\d+', ''.join(qubit.findall(line)))]

        # Find path
        path = graph.dijkstra(qubits[0], qubits[1])

        # make swaps per path point
        for point in path:
            print(point)






graph = Graph([])
Graph.add_edge(graph,"0","1")
Graph.add_edge(graph,"0","3")
Graph.add_edge(graph,"1","2")
Graph.add_edge(graph,"1","4")
Graph.add_edge(graph,"2","5")
Graph.add_edge(graph,"3","4")
Graph.add_edge(graph,"3","6")
Graph.add_edge(graph,"4","5")
Graph.add_edge(graph,"4","7")
Graph.add_edge(graph,"5","8")
Graph.add_edge(graph,"6","7")
Graph.add_edge(graph,"7","8")

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

map_to_topology(graph, qasm_code)

