import os

from src.connecting.quantum_inspire import get_authentication
from quantuminspire.api import QuantumInspireAPI

from src.quantum_phase_estimation.QEP_as_function import estimate_phase

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

authentication = get_authentication(qi_email=QI_EMAIL, qi_password=QI_PASSWORD)
qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')

unitary = 'QASM\nRz q[0], -0.8377580409572781\n'

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

# Offset and standard deviation for phase errors enduced by gates
mu = 0
sigma = 0
error_toggle = 0

fraction, error, correct_chance = estimate_phase(unitary,
                   desired_bit_accuracy=3,
                   p_succes_min=0.8,
                   print_qasm=True,
                   graph=False,
                   max_qubits=26,
                   shots=512,
                   mu=0.25,
                   sigma=0.5,
                   error_toggle=0)

print('Fraction: ', fraction)
print('Error: ', error)
print('Correct chance: ', correct_chance)
