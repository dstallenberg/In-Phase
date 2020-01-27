import numpy as np

from src.quantum_phase_estimation.util_functions import error_estimate, find_qubits_from_unitary
from src.quantum_phase_estimation.generator.generator import generate_qasm_code
from src.qasm_optimizer.optimizer import optimize
from src.qasm_error_introducer.error_introducer import introduce_error
from src.qasm_topology_mapper.mapping import map_to_topology
from src.quantum_phase_estimation.processing.classical_postprocessing import print_result, remove_degeneracy_projectq
from src.quantum_phase_estimation.plot_results import plot_results_projectq
from src.qasm_to_projectq.converter import qasm_to_projectq


if __name__ == "__main__":
    # variables
    unitary = 'QASM\nRz q[0], -1.6'#np.array([[0.7071, -0.7071j], [-0.7071j, 0.7071]])
    desired_bit_accuracy = 5
    minimum_chance_of_success = 0.5
    mu = 0
    sigma = 0.01
    error_toggle = False
    topology = [['0', '1'],
                ['0', '3'],
                ['1', '2'],
                ['1', '4'],
                ['2', '5'],
                ['3', '4'],
                ['3', '6'],
                ['4', '5'],
                ['4', '7'],
                ['5', '8'],
                ['6', '7'],
                ['7', '8']]
    shots = 100
    topology = None

    # process
    nancillas, p_succes = error_estimate(desired_bit_accuracy, minimum_chance_of_success)
    qubits, extra_empty_bits = find_qubits_from_unitary(unitary, nancillas, topology=topology)

    final_qasm = generate_qasm_code(nancillas, qubits, unitary, extra_empty_bits=extra_empty_bits)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if topology is not None:
        final_qasm = map_to_topology(topology, final_qasm)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if error_toggle:
        final_qasm = introduce_error(final_qasm, mu, sigma)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    projecq_code = qasm_to_projectq(final_qasm)

    file = open('generated/code/generated.py', 'w')
    file.write(projecq_code)
    file.close()

    from generated.code.generated import calc_probs

    result = calc_probs()

    print(result)

    plot_results_projectq(result, nancillas, qubits, p_succes)

    # Classical postprocessing
    fraction, error = print_result(remove_degeneracy_projectq(result, nancillas), desired_bit_accuracy, nancillas)

    print('Fraction: ', fraction)
    print('Error: ', error)
    print('Correct chance: ', 1 - (1 - p_succes) ** shots)
