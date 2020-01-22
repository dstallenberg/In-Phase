from src.tests.mapping.aquire_data import get_results
from src.tests.mapping.process_data import to_array, find_keys, decimal_to_binary_fracion
from src.tests.mapping.plotting import heatmap, graph
from src.quantum_phase_estimation.util_functions import error_estimate

if __name__ == "__main__":
    bit = 10

    result = get_results(bit, try_from_file=True)
    nancilla, p_succes = error_estimate(bit, 0.5)
    data = to_array(result, bit, nancilla)
    binary_fractions = decimal_to_binary_fracion(find_keys(data), nancilla)

    heatmap(data[1])
    graph(binary_fractions)
