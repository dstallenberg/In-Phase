single_operators = ['H', 'X', 'Y', 'Z', 'prep_x', 'prep_y', 'prep_z']
double_operators = ['CNOT', 'CX', 'CY', 'CZ']

def optimize(qasm_code, total_qubits):

    # qasm_code = re.sub(r'(H q\[\d]\n){2}', qasm_code)

    while can_optimize(qasm_code, total_qubits):
        for i in range(total_qubits):
            for single in single_operators:
                qasm_code = qasm_code.replace(f'{single} q[{i}]\n{single} q[{i}]\n', '')
                qasm_code = qasm_code.replace(f'{{{single} q[{i}]}}\n{{{single} q[{i}]}}\n', '')

            for j in range(total_qubits):
                for single in single_operators:
                    qasm_code = qasm_code.replace(f'{{{single} q[{i},{j}]}}\n{{{single} q[{i},{j}]}}\n', '')

                for double in double_operators:
                    qasm_code = qasm_code.replace(f'{double} q[{i}], q[{j}]\n{double} q[{i}], q[{j}]\n', '')

                qasm_code = qasm_code.replace(f'CNOT q[{i}], q[{j}]\nCNOT q[{j}], q[{i}]\nCNOT q[{i}], q[{j}]\nCNOT q[{i}], q[{j}]\nCNOT q[{j}], q[{i}]\nCNOT q[{i}], q[{j}]\n', '')

                for k in range(total_qubits):
                    # SWAP gate
                    qasm_code = qasm_code.replace(f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n', '')
                    qasm_code = qasm_code.replace(f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n', '')

    return qasm_code


def can_optimize(qasm_code, total_qubits):
    for i in range(total_qubits):
        for single in single_operators:
            if f'{single} q[{i}]\n{single} q[{i}]\n' in qasm_code:
                return True
            if f'{{{single} q[{i}]}}\n{{{single} q[{i}]}}\n' in qasm_code:
                return True
        for j in range(total_qubits):
            for k in range(total_qubits):
                # SWAP gate
                if f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n' in qasm_code:
                    return True

                if f'Toffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n\nToffoli q[{k}], q[{j}], q[{i}]\nToffoli q[{k}], q[{i}], q[{j}]\nToffoli q[{k}], q[{j}], q[{i}]\n' in qasm_code:
                    return True

            if f'CNOT q[{i}], q[{j}]\nCNOT q[{j}], q[{i}]\nCNOT q[{i}], q[{j}]\nCNOT q[{i}], q[{j}]\nCNOT q[{j}], q[{i}]\nCNOT q[{i}], q[{j}]\n' in qasm_code:
                return True
            
            for double in double_operators:
                if f'{double} q[{i}], q[{j}]\n{double} q[{i}], q[{j}]\n' in qasm_code:
                    return True

    return False
