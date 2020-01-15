import os

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

## Variables
desired_bit_accuracy = 8
p_succes_min = 0.5

nancillas, p_succes = error_estimate(desired_bit_accuracy, p_succes_min)

qubits = 1
unitary_operation = 'QASM\nRz q[0], 3.1415\n'

final_qasm = generate_quantum_inspire_code(nancillas, qubits, unitary_operation)

print(final_qasm)

backend_type = qi.get_backend_type_by_name('QX single-node simulator')

result = qi.execute_qasm(final_qasm, backend_type=backend_type, number_of_shots=512)

if nancillas < 5:
    plot_results(result, nancillas, qubits, p_succes)

print_result(remove_degeneracy(result, nancillas), desired_bit_accuracy, nancillas)