import os
from getpass import getpass
from quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication
from quantuminspire.api import QuantumInspireAPI
import matplotlib.pyplot as plt

from src.qpe.quantum_phase_estimation import generate_quantum_inspire_code

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
qi = QuantumInspireAPI(QI_URL, authentication)

## Variables
nancillas = 4
qubits = 2
unitary_operation = 'Z'

final_qasm = generate_quantum_inspire_code(nancillas, qubits, unitary_operation)

print(final_qasm)

backend_type = qi.get_backend_type_by_name('QX single-node simulator')
result = qi.execute_qasm(final_qasm, backend_type=backend_type, number_of_shots=512)

print(result['raw_text'])
print(result['execution_time_in_seconds'])
print(result['histogram'])

plt.bar(result['histogram'].keys(), result['histogram'].values())
plt.show()