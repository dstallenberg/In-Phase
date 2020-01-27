import os
import time
import numpy as np

from src.connecting.quantum_inspire import get_authentication
from quantuminspire.api import QuantumInspireAPI

from examples.utils.mapping import generate_data
from src.quantum_phase_estimation.util_functions import error_estimate
from src.quantum_phase_estimation.util_functions import decimal_to_binary_fracion, find_max_value_keys, to_array
from src.quantum_phase_estimation.processing.plotting import heatmap, graph
from quantuminspire.credentials import load_account


if __name__ == "__main__":
    QI_EMAIL = os.getenv('QI_EMAIL')
    QI_PASSWORD = os.getenv('QI_PASSWORD')
    QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

    tokens = [load_account()]
    qis = list(map(lambda x: QuantumInspireAPI(QI_URL, get_authentication(qi_email=QI_EMAIL, qi_password=QI_PASSWORD, token=x), 'Quantum Phase Estimation matrix'), tokens))

    # variables
    desired_bit_accuracy = 6
    minimum_chance_of_success = 0.5
    mu = 0
    sigma = 0.05
    use_error_model = False
    use_multiple = True
    topology = None
    shots = 512

    name = f'heatmap_{desired_bit_accuracy}_{minimum_chance_of_success}_{topology is not None if "True" else "False"}_{use_error_model if f"{use_error_model}_{mu}_{sigma}" else f"{use_error_model}"}'
    file = f'generated/tests/mapping/{name}.npy'

    data = None
    if file is not None:
        print('testing file')

        try:
            data = np.load(file, allow_pickle=True)
            print(f"Loaded data from {file}")
        except:
            print(f"No file '{file}' found. Gathering from QI...")

    if data is None:
        arguments = []
        points = np.linspace(0, 2 * np.pi, 2 ** desired_bit_accuracy)

        print(f"Preparing to send {2 ** desired_bit_accuracy} jobs to QI")

        for i in range(len(points)):
            val = points[i]
            #unitary = f"QASM\n" \
            #          f"Rz q[0], {-val}"

            unitary = np.array([[np.exp(val * 0.5j), 0],
                                [0, np.exp(-val * 0.5j )]])

            use_qi = qis[0]

            if use_multiple:
                qi_num = i % len(qis)
                use_qi = qis[qi_num]

            arguments.append(
                [use_qi, unitary, desired_bit_accuracy, minimum_chance_of_success, 512, topology, use_error_model, mu, sigma])

        start = time.time()
        data = generate_data(arguments, True, file)
        total = time.time() - start
        print('Total time: ', total, ' seconds')

    nancilla, p_succes = error_estimate(desired_bit_accuracy, 0.5)
    data = to_array(data, desired_bit_accuracy, nancilla)
    binary_fractions = decimal_to_binary_fracion(find_max_value_keys(data), nancilla)

    heatmap(data[1], name)
    graph(binary_fractions)