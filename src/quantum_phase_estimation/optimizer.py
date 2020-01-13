import re

def optimize(qasm_code, total_qubits):

    # qasm_code = re.sub(r'(H q\[\d]\n){2}', qasm_code)

    while can_optimize(qasm_code, total_qubits):
        for i in range(total_qubits):
            qasm_code = qasm_code.replace(f'H q[{i}]\nH q[{i}]\n', '')

        for i in range(total_qubits):
            for j in range(total_qubits):
                if i == j:
                    continue
                qasm_code = qasm_code.replace(f'CNOT q[{i}], q[{j}]\nCNOT q[{i}], q[{j}]\n', '')

    return qasm_code

def can_optimize(qasm_code, total_qubits):

    for i in range(total_qubits):
        if f'H q[{i}]\nH q[{i}]\n' in qasm_code:
            return True

    for i in range(total_qubits):
        for j in range(total_qubits):
            if i == j:
                continue
            if f'CNOT q[{i}], q[{j}]\nCNOT q[{i}], q[{j}]\n' in qasm_code:
                return True

    return False