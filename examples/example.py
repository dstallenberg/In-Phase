import os

from src.connecting.quantum_inspire import get_authentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.credentials import load_account

from src.quantum_phase_estimation.util_functions import error_estimate, find_qubits_from_unitary
from src.quantum_phase_estimation.generator.generator import generate_qasm_code
from src.qasm_optimizer.optimizer import optimize
from src.qasm_error_introducer.error_introducer import introduce_error
from src.qasm_topology_mapper.mapping import map_to_topology
from src.quantum_phase_estimation.processing.classical_postprocessing import print_result, remove_degeneracy
from src.quantum_phase_estimation.plot_results import plot_results

import numpy as np

if __name__ == "__main__":
    QI_EMAIL = os.getenv('QI_EMAIL')
    QI_PASSWORD = os.getenv('QI_PASSWORD')
    QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

    authentication = get_authentication(qi_email=QI_EMAIL, qi_password=QI_PASSWORD, token=load_account())
    qi = QuantumInspireAPI(QI_URL, authentication, 'matrix')

    # variables
    phase = 0.08
    print(phase)
    unitary_qasm = f"QASM\nRz q[0], {-phase*2*np.pi}"
    unitary_matrix = np.array([[np.exp(phase*1j*np.pi), 0],
                               [0, np.exp(-phase*1j*np.pi)]])
    unitary = unitary_matrix
    custom_prepare = "prep_z q[0]\n X q[0]"
    desired_bit_accuracy = 5
    minimum_chance_of_success = 0.5
    mu = 0.5
    sigma = 0.5
    error_toggle = 0
    topology = None
    shots = 512

    # process
    nancillas, p_succes = error_estimate(desired_bit_accuracy, minimum_chance_of_success)
    qubits, extra_empty_bits = find_qubits_from_unitary(unitary, nancillas, topology=topology)

    final_qasm = generate_qasm_code(nancillas, qubits, unitary, extra_empty_bits=extra_empty_bits, custom_prepare=custom_prepare)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if topology is not None:
        final_qasm = map_to_topology(topology, final_qasm)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    if error_toggle:
        final_qasm = introduce_error(final_qasm, mu, sigma)

    final_qasm = optimize(final_qasm, nancillas, qubits, extra_empty_bits)

    backend_type = qi.get_backend_type_by_name('QX single-node simulator')
    result = qi.execute_qasm(final_qasm,
                             backend_type=backend_type,
                             number_of_shots=shots)

    # Classical postprocessing
    fraction, error = print_result(remove_degeneracy(result['histogram'], nancillas), desired_bit_accuracy, nancillas)

    print('Fraction: ', fraction)
    print('Error: ', error)
    print('Correct chance: ', 1 - (1 - p_succes) ** shots)
