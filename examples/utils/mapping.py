import numpy as np

from src.quantum_phase_estimation.runner import async_calls
from src.quantum_phase_estimation.util_functions import error_estimate, find_qubits_from_unitary
from src.quantum_phase_estimation.generator.generator import generate_qasm_code
from src.qasm_optimizer.optimizer import optimize
from src.qasm_error_introducer.error_introducer import introduce_error
from src.qasm_topology_mapper.mapping import map_to_topology


def execute_example(qi, unitary, desired_bit_accuracy, minimum_chance_of_success, shots=512, topology=None, create_errors=False, mu=0.5, sigma=0.5):
    nancillas, p_succes = error_estimate(desired_bit_accuracy, minimum_chance_of_success)
    qubits, extra_empty_bits = find_qubits_from_unitary(unitary, nancillas, topology=topology)

    final_qasm = generate_qasm_code(nancillas, qubits, unitary, extra_empty_bits=extra_empty_bits, custom_prepare="X q[0]")

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if topology is not None:
        final_qasm = map_to_topology(topology, final_qasm)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if create_errors:
        final_qasm = introduce_error(final_qasm, mu, sigma)

    backend_type = qi.get_backend_type_by_name('QX single-node simulator')
    return qi.execute_qasm(final_qasm,
                             backend_type=backend_type,
                             number_of_shots=shots)


def generate_data(arguments, multi, file=None):
    print("QASM is generated. Sending jobs...")
    if multi:
        result = async_calls(execute_example, arguments)

    else:
        result = []

        for i in range(len(arguments)):
            result.append(execute_example(*arguments[i]))

    print("Received all jobs!")

    if file is not None:
        print(f"Saving to {file}")
        np.save(file, result)

    return result