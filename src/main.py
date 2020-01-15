import os
import numpy as np

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

authentication = get_authentication()
qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')

"""The desired bit accuracy and minimal succes determine the number of ancillas used.
A higher desired accuracy corresponds to a higher number of ancillas used"""

desired_bit_accuracy = 3
p_succes_min = 0.5
nancillas, p_succes = error_estimate(desired_bit_accuracy, p_succes_min)

""""Specify the number of qubits in the initial state """


""""The unitary operator U is specified below. This can be done with QASM code describing the unitary's circuit, 
 or with a matrix respresentation of U."""

unitary_operation = np.array([[1,0],[0, 1]])
print(unitary_operation)
qubits = int(np.log2(unitary_operation.shape[0]))

initial = """prep_z q[0]
x q[0]
"""
"""Generate and print QASM code"""

final_qasm = generate_quantum_inspire_code(nancillas, qubits, unitary_operation)
print(final_qasm)
""""Calculate results using QuantumInspire"""
backend_type = qi.get_backend_type_by_name('QX single-node simulator')
result = qi.execute_qasm(final_qasm, backend_type=backend_type, number_of_shots=512)

"""Generate graphs using the acquired data"""
if nancillas < 5:
    plot_results(result, nancillas, qubits, p_succes)

print_result(remove_degeneracy(result, nancillas), desired_bit_accuracy, nancillas)