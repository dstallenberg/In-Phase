import re

single_operators = ['H', 'X', 'Y', 'Z', 'prep_x', 'prep_y', 'prep_z']
single_operators_arg = ['Rx', 'Ry', 'Rz']

double_operators = ['CNOT', 'CX', 'CY', 'CZ']


def two_to_one(code):
    parts = code.split('\n')

    parts_1 = parts[0].split(',')
    parts_2 = parts[1].split(',')

    final_arg = float(parts_1[1]) + float(parts_2[1])

    return f'{parts_1[0]}, {final_arg}\n'


def optimize(qasm_code, total_qubits):

    # qasm_code = re.sub(r'(H q\[\d]\n){2}', qasm_code)
    while can_optimize(qasm_code, total_qubits):
        for i in range(total_qubits):
            for single in single_operators:
                qasm_code = qasm_code.replace(f'{single} q[{i}]\n{single} q[{i}]\n', '')
                qasm_code = qasm_code.replace(f'{{{single} q[{i}]}}\n{{{single} q[{i}]}}\n', '')

            for single in single_operators_arg:
                matches = re.findall(rf'({single} q\[{i}], -?\d.?\d*\n{single} q\[{i}], -?\d.?\d*\n)', qasm_code)
                for match in matches:
                    qasm_code = qasm_code.replace(match, two_to_one(match))


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

        for single in single_operators_arg:
            matches = re.findall(rf'({single} q\[{i}], -?\d.?\d*\n{single} q\[{i}], -?\d.?\d*\n)', qasm_code)
            if len(matches):
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
