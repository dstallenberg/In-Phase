# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 14:42:47 2020

@author: Mio
"""

import os
import numpy as np
import re

from getpass import getpass
from quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication
from quantuminspire.api import QuantumInspireAPI

from src.quantum_phase_estimation.generator.generator import generate_qasm_code
from src.quantum_phase_estimation.util_functions import error_estimate
from src.quantum_phase_estimation.plot_results import plot_results
from src.quantum_phase_estimation.processing.classical_postprocessing import print_result, remove_degeneracy
from src.qasm_topology_mapper.mapping import map_to_topology, graph
from src.qasm_optimizer.optimizer import optimize
from src.quantum_phase_estimation.util_functions import find_qubits_from_unitary
from src.connecting.quantum_inspire import get_authentication

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')


def estimate_phase(unitary,
                   desired_bit_accuracy=3,
                   p_succes_min=0.5,
                   initial="# No initialization given",
                   print_qasm=False,
                   graph=False,
                   max_qubits=26,
                   shots=512,
                   mu=0,
                   sigma=0,
                   error_toggle=0,
                   topology=None):
    """You can use this function if you want to use the QI backend. To use your own backend, combine generate_qasm() and
    classical_postprocessing() in the intended way."""

    # Get authentication
    authentication = get_authentication(QI_EMAIL, QI_PASSWORD)
    qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')

    """The desired bit accuracy and minimal succes determine the number of ancillas used.
    A higher desired accuracy corresponds to a higher number of ancillas used"""
    qasm, qubits, nancillas, p_succes = generate_qasm(unitary,
                                                      mu,
                                                      sigma,
                                                      error_toggle,
                                                      desired_bit_accuracy,
                                                      p_succes_min,
                                                      initial,
                                                      print_qasm,
                                                      max_qubits,
                                                      topology=topology)


    """Calculate results using QuantumInspire"""
    backend_type = qi.get_backend_type_by_name('QX single-node simulator')
    result = qi.execute_qasm(qasm,
                             backend_type=backend_type,
                             number_of_shots=shots)

    """Generate graphs using the acquired data"""
    if graph:
        plot_results(result, nancillas, qubits, p_succes)

    # Classical postprocessing
    fraction, error = print_result(remove_degeneracy(result['histogram'], nancillas), desired_bit_accuracy, nancillas)

    return fraction, error, 1 - (1 - p_succes) ** shots


def generate_qasm(unitary,
                  mu,
                  sigma,
                  error_toggle,
                  desired_bit_accuracy=3,
                  p_succes_min=0.5,
                  initial="# No initialization given",
                  print_qasm=True,
                  max_qubits=26,
                  topology=None,
                  use_optimizer=True):
    """Generate qasm to send to backend"""
    qubits_in_top = False
    if topology is not None:
        found_max = 0
        for edge in topology:
            found_max = max(found_max, int(edge[0]) + 1)
            found_max = max(found_max, int(edge[1]) + 1)

        qubits_in_top = found_max
        max_qubits = qubits_in_top

    nancillas, p_succes = error_estimate(desired_bit_accuracy, p_succes_min)

    """"Specify the number of qubits in the initial state """

    qubits = find_qubits_from_unitary(unitary)  # int(np.log2(unitary_operation.shape[0]))

    extra_empty_bits = 0
    if qubits_in_top:
        extra_empty_bits = (qubits_in_top - 2 * qubits - nancillas)

    if 2 * qubits + nancillas > max_qubits:
        raise ValueError(f"Need more qubits than allowed! (need {2 * qubits + nancillas}, maximum is {max_qubits})")

    """Generate and print QASM code"""
    final_qasm = generate_qasm_code(mu, sigma, error_toggle, nancillas, qubits, unitary, initial, extra_empty_bits=extra_empty_bits)

    if topology is not None:
        final_qasm = map_to_topology(topology, final_qasm)

    if use_optimizer:
        final_qasm = optimize(final_qasm, nancillas + qubits + qubits + extra_empty_bits)

    if print_qasm:
        print(final_qasm)

    return final_qasm, qubits, nancillas, p_succes
