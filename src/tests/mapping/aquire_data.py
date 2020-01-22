import numpy as np
from src.quantum_phase_estimation.runner import async_calls
from src.quantum_phase_estimation.QEP_as_function import get_authentication, generate_qasm
from quantuminspire.api import QuantumInspireAPI
import os


QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')


def get_from_qi(unitary,
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
                                                      0,
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

    print(unitary)

    return result


def get_results(bit=5, try_from_file = True):
    if try_from_file:
        print('testing file')

        try:
            fname = f"generated/tests/mapping/heatmap_{bit}.npy"
            data = np.load(fname, allow_pickle=True)
            print(f"Loaded data from {fname}")

            return data

        except:
            print(f"No file '{fname}' found. Gathering from QI...")

    return from_qi(bit, multi=True)


def from_qi(bit, save=True, succes=0.5, multi=True):
    arguments = []
    points = np.linspace(0, 2*np.pi, 2**bit)

    print(f"Preparing to send {2**bit} jobs to QI")

    for i in points:
        unitary = f"QASM\n" \
                  f"Rz q[0], {-i}"

        arguments.append(
            [unitary, bit, succes, "# No initialization given", False, False, 26, 512, 0, 0])

    print("QASM is generated. Sending jobs...")
    if multi:
        result = async_calls(get_from_qi, arguments)

    else:
        result = []

        for i in range(2**bit):
            result.append(get_from_qi(*arguments[i]))

    print("Received all jobs!")

    if save:
        fname = f"generated/tests/mapping/heatmap_{bit}.npy"
        print(f"Saving to {fname}")

        np.save(fname, result)

    return result


if __name__ == "__main__":
    np.load("generated/tests/mapping/heatmap_4.npy", allow_pickle=True)
    get_results(4)