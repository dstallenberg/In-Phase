import os
import numpy as np

from src.connecting.quantum_inspire import get_authentication
from quantuminspire.api import QuantumInspireAPI

from src.quantum_phase_estimation.util_functions import error_estimate, find_qubits_from_unitary
from src.quantum_phase_estimation.generator.generator import generate_qasm_code
from src.qasm_optimizer.optimizer import optimize
from src.qasm_error_introducer.error_introducer import introduce_error
from src.qasm_topology_mapper.mapping import map_to_topology
from src.quantum_phase_estimation.processing.classical_postprocessing import print_result, remove_degeneracy
from src.quantum_phase_estimation.plot_results import plot_results

if __name__ == "__main__":
    QI_EMAIL = os.getenv('QI_EMAIL')
    QI_PASSWORD = os.getenv('QI_PASSWORD')
    QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

    authentication = get_authentication(qi_email=QI_EMAIL, qi_password=QI_PASSWORD)
    qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')

    # variables
    w = np.exp((2j / 3) * np.pi)
    unitary = np.array([[1, 1, 1, 0],
                        [1, w, w * w, 0],
                        [1, w * w, w, 0],
                        [0, 0, 0, -1j * np.sqrt(3)]]) / np.sqrt(3)
    desired_bit_accuracy = 5
    minimum_chance_of_success = 0.5
    mu = 0
    sigma = 0.01
    error_toggle = False
    topology = None
    shots = 512

    # process
    nancillas, p_succes = error_estimate(desired_bit_accuracy, minimum_chance_of_success)
    qubits, extra_empty_bits = find_qubits_from_unitary(unitary, nancillas, topology=topology)

    final_qasm = generate_qasm_code(nancillas, qubits, unitary, extra_empty_bits=extra_empty_bits)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if error_toggle:
        final_qasm = introduce_error(final_qasm, mu, sigma)

    if topology is not None:
        final_qasm = map_to_topology(topology, final_qasm)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    backend_type = qi.get_backend_type_by_name('QX single-node simulator')
    result = qi.execute_qasm(final_qasm,
                             backend_type=backend_type,
                             number_of_shots=shots)

    plot_results(result, nancillas, qubits, p_succes)

    # Classical postprocessing
    fraction, error = print_result(remove_degeneracy(result['histogram'], nancillas), desired_bit_accuracy, nancillas)

    print('Fraction: ', fraction)
    print('Error: ', error)
    print('Correct chance: ', 1 - (1 - p_succes) ** shots)
