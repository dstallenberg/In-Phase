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

                for k in range(total_qubits):
                    # SWAP gate
                    qasm_code = qasm_code.replace(f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n', '')


                for double in double_operators:
                    qasm_code = qasm_code.replace(f'{double} q[{i}], q[{j}]\n{double} q[{i}], q[{j}]\n', '')


    return qasm_code


def can_optimize(qasm_code, total_qubits):
    for i in range(total_qubits):
        for single in single_operators:
            if f'{single} q[{i}]\n{single} q[{i}]\n' in qasm_code:
                return True
        for j in range(total_qubits):
            if i == j:
                continue

            for k in range(total_qubits):
                # SWAP gate
                if k == 0 and j == 10 and i == 11:
                    print(k, j, i)
                    print(f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n')
                    print(qasm_code)
                if f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n' in qasm_code:
                    return True

            for double in double_operators:
                if f'{double} q[{i}], q[{j}]\n{double} q[{i}], q[{j}]\n' in qasm_code:
                    return True

    return False
