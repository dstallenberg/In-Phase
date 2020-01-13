from src.quantum_phase_estimation.circuit.fourier_transform import generate_inverse_qft
from src.quantum_phase_estimation.operator.unitary_operators import get_unitary_operators_array, find_controlled_equivalent
from src.quantum_phase_estimation.optimizer import optimize

def generate_quantum_inspire_code(nancillas, qubits, unitary_operation):
    # Check if QASM en then replace q[i] with q[i + nancilla] etc

    print(unitary_operation)
    print(nancillas)
    if isinstance(unitary_operation, str) and 'QASM' in unitary_operation:
        for i in range(20, 0, -1):
            #print(i)
            if f'q[{i}]' in unitary_operation:
                unitary_operation = unitary_operation.replace(f'q[{i}]', f'q[{i + nancillas}]')

    total = nancillas + qubits

    final_qasm = f"""version 1.0

qubits {total + qubits}

# Prepare qubits
prep_z q[0:{total - 1}]

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

    final_qasm += '\n# Apply controlled unitary operations\n'

    unitary_operations = get_unitary_operators_array(unitary_operation, nancillas, qubits)
    print(unitary_operations)
    for i in range(nancillas):
        operation = unitary_operations[i]
        if operation == 'I':
            continue

        # If the operation is more complex we make sure to put QASM on the first line of the operation (arbitrary unitary operation)
        if 'QASM' in operation:
            operation = '\n'.join(operation.split('\n')[1:])
            final_qasm += operation
            continue

        # If there are multiple qubits
        # if qubits > 1:
        #     controls = []
        #     controls.extend(range(nancillas - 1, total - 1))
        #     final_qasm += transform_controlled_unitary_to_toffoli(operation, controls, total - 1)
        # else:

        if qubits > 2:
            # This is weird why do we have multiple qubits while the operation is a single non controlled operation
            raise Exception('This is weird why do we have more than 3 qubits while the operation is a single non controlled operation')

        # If the operation is a single or double quantum unitary operation
        controls = [i]
        controls.extend(range(nancillas - 1, total - 1))
        print(controls)
        final_qasm += find_controlled_equivalent(operation, controls, total - 1)

    final_qasm += '\n# Apply inverse quantum phase estimation\n'

    final_qasm += generate_inverse_qft(nancillas) + '\n'

    final_qasm = optimize(final_qasm, nancillas + qubits + qubits)

    # for i in range(total - 1):
    #     if i != 0:
    #         final_qasm += f'H q[{i}]\n'
    #     final_qasm += f'Measure_{unitary_operation.lower()} q[{i}]\n'

    print(final_qasm)
    return final_qasm
