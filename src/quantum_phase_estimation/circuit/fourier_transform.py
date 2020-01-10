import math


def generate_qft(qubits):
    if qubits < 1:
        raise Exception('For QFT generation qubits must be larger or equal to 1!')

    QFT = []
    for i in range(qubits):
        QFT.append(f'H q[{i}]')
        for j in range(i + 1, qubits):
            QFT.append(f'CRk q[{j}], q[{i}], {j - i}')



    return '\n'.join(QFT)


def generate_inverse_qft(qubits):
    if qubits < 1:
        raise Exception('For inverse QFT generation qubits must be larger or equal to 1!')

    iQFT = []
    for i in range(qubits):
        k = (qubits - 1) - i
        for j in range(k):
            iQFT.append(f'CR q[{k}], q[{j}], {-math.pi/float(2**(k - j))}')
        iQFT.append(f'H q[{k}]')

    return '\n'.join(iQFT)
