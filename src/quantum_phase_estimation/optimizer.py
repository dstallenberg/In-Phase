import re

def optimize(qasm_code, total_qubits):

    # qasm_code = re.sub(r'(H q\[\d]\n){2}', qasm_code)

    for i in range(total_qubits):
        qasm_code = qasm_code.replace(f'H q[{i}]\nH q[{i}]\n', '\n')

    return qasm_code