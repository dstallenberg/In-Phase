import os

from getpass import getpass
from quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication
from quantuminspire.api import QuantumInspireAPI

from src.QEP_as_function import estimate_phase

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

unitary = 'QASM\nRz q[0], 3.1415\n'

# Offset and standard deviation for phase errors enduced by gates
mu = 0
sigma = 0
error_toggle = 0

fraction, error, correct_chance = estimate_phase(unitary,
                   desired_bit_accuracy=5,
                   p_succes_min=0.8,
                   print_qasm=False,
                   graph=False,
                   max_qubits=26,
                   shots=512,
                   mu=0.25,
                   sigma=0.5,
                   error_toggle=0)
)

print('Fraction: ', fraction)
print('Error: ', error)
print('Correct chance: ', correct_chance)
