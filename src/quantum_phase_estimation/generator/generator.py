import math

from src.quantum_phase_estimation.generator.unitary_operators import get_unitary_operators_array, find_controlled_equivalent


def generate_qasm_code(nancillas, qubits, unitary_operation, custom_prepare='# No custom preparation given by user', extra_empty_bits=0):
    # Check if QASM en then replace q[i] with q[i + nancilla] etc

    if isinstance(unitary_operation, str) and 'QASM' in unitary_operation and not unitary_operation.endswith('\n'):
        unitary_operation += "\n"

    for i in range(nancillas+2*qubits, -1, -1):
        if isinstance(unitary_operation, str) and 'QASM' in unitary_operation:
            if f'q[{i}]' in unitary_operation:
                unitary_operation = unitary_operation.replace(f'q[{i}]', f'q[{i + nancillas}]')

        if f'q[{i}]' in custom_prepare:
            custom_prepare = custom_prepare.replace(f'q[{i}]', f'q[{i + nancillas}]')

    total = nancillas + qubits
    final_qasm = f"""version 1.0

qubits {total + qubits + extra_empty_bits}

# Prepare qubits \n.preparation\n
prep_z q[0:{total - 1}]
{ '' if extra_empty_bits == 0 else f'prep_z q[{total + qubits + extra_empty_bits - 1}]' if extra_empty_bits == 1 else f'prep_z q[{total + qubits}:{total + qubits + extra_empty_bits - 1}]' }

# Custom prepare
{custom_prepare}

# Create superposition
"""
    if nancillas == 1 and qubits == 1:
        final_qasm += f'{{ H q[0] | X q[1] }}'
    elif nancillas == 1:
        final_qasm += f'{{ H q[0] | X q[1:{total - 1}] }}'
    elif qubits == 1:
        final_qasm += f'{{ H q[0:{nancillas - 1}] | X q[{total - 1}] }}'
    else:
        final_qasm += f'{{ H q[0:{nancillas - 1}] | X q[{nancillas}:{total - 1}] }}'

    final_qasm += '\n# Apply controlled unitary operations\n.controlled_unitary_operations\n'

    unitary_operations = get_unitary_operators_array(unitary_operation, nancillas, qubits)
    for i in range(nancillas):
        operation = unitary_operations[i]
        if operation == 'I':
            continue

        # If the operation is more complex we make sure to put QASM on the first line of the operation (arbitrary unitary operation)
        if 'QASM' in operation:
            operation = '\n'.join(operation.split('\n')[1:])
            final_qasm += operation
            continue

        if qubits > 2:
            # This is weird why do we have multiple qubits while the operation is a single non controlled operation
            raise Exception('This is weird why do we have more than 2 qubits while the operation is a single non controlled operation')

        # If the operation is a single or double quantum unitary operation
        controls = [i]

        # controls.extend(range(nancillas - 1, total - 1))

        final_qasm += find_controlled_equivalent(operation, controls, total - 1, nancillas, qubits)

    final_qasm += '\n# Apply inverse quantum phase estimation\n.Inverse_Quantum_Fourier_Transform\n'

    final_qasm += generate_inverse_qft(nancillas) + '\n'

    # for i in range(total - 1):
    #     if i != 0:
    #         final_qasm += f'H q[{i}]\n'
    #     final_qasm += f'Measure_{unitary_operation.lower()} q[{i}]\n'

    return final_qasm


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
    iQFT.append(f'H q[0:{qubits-1}]')

    return '\n'.join(iQFT)
