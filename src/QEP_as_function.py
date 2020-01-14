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
				   desired_bit_accuracy = 3, 
				   p_succes_min = 0.5, 
				   initial = "# No initialization given",
				   print_qasm = False,
				   graph = False,
				   max_qubits = 26,
				   shots = 512):
	
	
	
	authentication = get_authentication()
	qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')
	
	"""The desired bit accuracy and minimal succes determine the number of ancillas used.
	A higher desired accuracy corresponds to a higher number of ancillas used"""
	
	nancillas, p_succes = error_estimate(desired_bit_accuracy, p_succes_min)
	
	""""Specify the number of qubits in the initial state """
	
	qubits = find_qubits_from_unitary(unitary)#int(np.log2(unitary_operation.shape[0]))
	
	
	if 2*qubits + nancillas > max_qubits:
		raise ValueError(f"Need more qubits than allowed! (need {2*qubits + nancillas}, maximum is {max_qubits})")
	
	"""Generate and print QASM code"""
	
	final_qasm = generate_quantum_inspire_code(nancillas, qubits, unitary, initial)
	
	if print_qasm:
		print(final_qasm)
	
	""""Calculate results using QuantumInspire"""
	backend_type = qi.get_backend_type_by_name('QX single-node simulator')
	result = qi.execute_qasm(final_qasm, backend_type=backend_type, number_of_shots=shots)
	
	"""Generate graphs using the acquired data"""
	if graph:
	    plot_results(result, nancillas, qubits, p_succes)
	
	fraction, error = print_result(remove_degeneracy(result, nancillas), 
			  desired_bit_accuracy,
			  nancillas)
	return fraction, error, p_succes
	
if __name__ == "__main__":
	for i in range(1):
		print(estimate_phase("""QASM
Rz q[0], 1.57075""",
					desired_bit_accuracy = 10))