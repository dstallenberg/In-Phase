from src.qpe.QFT import generate_inverse_qft
from src.qpe.unitary_operators import get_unitary_operators_array, transform_controlled_unitary_to_toffoli

def generate_quantum_inspire_code(nancillas, qubits, unitary_operation):
    total = nancillas + qubits

    final_qasm = f"""version 1.0

qubits {total}

# Prepare qubits
prep_z q[0:{total - 1}]

# Create superposition
{{ H q[0:{nancillas - 1}] | X q[{nancillas}:{total - 1}] }}
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

    unitary_operations = get_unitary_operators_array(unitary_operation, nancillas)

    for i in range(nancillas):
        operation = unitary_operations[i]
        if operation == 'I':
            continue

        if qubits > 1:
            controls = []
            controls.extend(range(nancillas - 1, total - 1))
            final_qasm += transform_controlled_unitary_to_toffoli(operation, controls, total - 1)
        else:
            final_qasm += f'C{operation} q[{i}], q[{total - 1}]\n'

    final_qasm += '\n# Apply inverse quantum phase estimation\n'

    final_qasm += generate_inverse_qft(nancillas) + '\n'

    if nancillas == 1:
        final_qasm += f'Measure q[0]'
    else:
        final_qasm += f'Measure q[0:{nancillas - 1}]'

    # for i in range(total - 1):
    #     if i != 0:
    #         final_qasm += f'H q[{i}]\n'
    #     final_qasm += f'Measure_{unitary_operation.lower()} q[{i}]\n'

    return final_qasm
