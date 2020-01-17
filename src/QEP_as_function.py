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

from src.quantum_phase_estimation.generator import generate_quantum_inspire_code
from src.quantum_phase_estimation.error_estimation import error_estimate
from src.quantum_phase_estimation.plot_results import plot_results
from src.quantum_phase_estimation.classical_postprocessing import print_result, remove_degeneracy

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')


def find_qubits_from_unitary(unitary):
    if type(unitary) == np.ndarray:
        return int(np.log2(unitary.shape[0]))
    else:
        result = [e for e in re.split("[^0-9.]", unitary) if e != '' and not '.' in e]
        if len(result) == 0:
            return 1
        else:
            return max(map(int, result)) + 1


def get_authentication():
    """ Gets the authentication for connecting to the Quantum Inspire API."""
    token = load_account()
    if token is not None:
        return get_token_authentication(token)
    else:
        if QI_EMAIL is None or QI_PASSWORD is None:
            print('Enter email')
            email = input()
            print('Enter password')
            password = getpass()
        else:
            email, password = QI_EMAIL, QI_PASSWORD
        return get_basic_authentication(email, password)


def estimate_phase(unitary,
                   desired_bit_accuracy=3,
                   p_succes_min=0.5,
                   initial="# No initialization given",
                   print_qasm=False,
                   graph=False,
                   max_qubits=26,
                   shots=512,
                   mu=0,
                   sigma=0):
    """You can use this function if you want to use the QI backend. To use your own backend, combine generate_qasm() and
    classical_postprocessing() in the intended way."""

    # Get authentication
    authentication = get_authentication()
    qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')

    """The desired bit accuracy and minimal succes determine the number of ancillas used.
    A higher desired accuracy corresponds to a higher number of ancillas used"""
    qasm, qubits, nancillas, p_succes = generate_qasm(unitary,
                                                      mu,
                                                      sigma,
                                                      desired_bit_accuracy,
                                                      p_succes_min,
                                                      initial,
                                                      print_qasm,
                                                      max_qubits)

    """Calculate results using QuantumInspire"""
    backend_type = qi.get_backend_type_by_name('QX single-node simulator')
    result = qi.execute_qasm(qasm,
                             backend_type=backend_type,
                             number_of_shots=shots)

    """Generate graphs using the acquired data"""
    if graph:
        plot_results(result, nancillas, qubits, p_succes)

    # Classical postprocessing
    fraction, error = classical_postprocessing(result, nancillas, desired_bit_accuracy, shots)

    return fraction, error, 1 - (1 - p_succes) ** shots


def classical_postprocessing(result, nancillas, desired_bit_accuracy, shots):
    """Do classical postprocessing on the result. result['histogram'] contains an ordered dict of keys and values."""
    fraction, error = print_result(remove_degeneracy(result['histogram'], nancillas), desired_bit_accuracy, nancillas)
    return fraction, error


def generate_qasm(unitary,
                  mu,
                  sigma,
                  desired_bit_accuracy=3,
                  p_succes_min=0.5,
                  initial="# No initialization given",
                  print_qasm=False,
                  max_qubits=26):
    """Generate qasm to send to backend"""
    nancillas, p_succes = error_estimate(desired_bit_accuracy, p_succes_min)

    """"Specify the number of qubits in the initial state """

    qubits = find_qubits_from_unitary(unitary)  # int(np.log2(unitary_operation.shape[0]))

    if 2 * qubits + nancillas > max_qubits:
        raise ValueError(f"Need more qubits than allowed! (need {2 * qubits + nancillas}, maximum is {max_qubits})")

    """Generate and print QASM code"""
    final_qasm = generate_quantum_inspire_code(mu, sigma, nancillas, qubits, unitary, initial)

    if print_qasm:
        print(final_qasm)

    return final_qasm, qubits, nancillas, p_succes

if __name__ == "__main__":
    for i in range(1):
        print(estimate_phase("""QASM
Rz q[0], -3.141592""",
                             desired_bit_accuracy=10, graph=True, shots=1))
