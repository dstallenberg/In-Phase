single_operators = ['H', 'X', 'Y', 'Z']
double_operators = ['CNOT', 'CX', 'CY', 'CZ']

def optimize(qasm_code, total_qubits):

    # qasm_code = re.sub(r'(H q\[\d]\n){2}', qasm_code)

    while can_optimize(qasm_code, total_qubits):
        for i in range(total_qubits):
            for single in single_operators:
                qasm_code = qasm_code.replace(f'{single} q[{i}]\n{single} q[{i}]\n', '')

            for j in range(total_qubits):
                if i == j:
                    continue

                for double in double_operators:
                    qasm_code = qasm_code.replace(f'{double} q[{i}], q[{j}]\n{double} q[{i}], q[{j}]\n', '')


    return qasm_code


def can_optimize(qasm_code, total_qubits):

    for i in range(total_qubits):
        for single in single_operators:
            if f'{single} q[{i}]\n{single} q[{i}]\n' in qasm_code:
                return True

    for i in range(total_qubits):
        for j in range(total_qubits):
            if i == j:
                continue
            for double in double_operators:
                if f'{double} q[{i}], q[{j}]\n{double} q[{i}], q[{j}]\n' in qasm_code:
                    return True

    return False