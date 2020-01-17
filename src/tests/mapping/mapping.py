from src.tests.mapping.aquire_data import get_results
from src.tests.mapping.process_data import to_array, sort_array, find_keys, decimal_to_binary_fracion
from src.tests.mapping.plotting import heatmap, graph

if __name__ == "__main__":
    bit = 4
    result = get_results(bit, try_from_file=True)
    data = to_array(result, bit)
    print(data)
    heatmap(sort_array(data))
    graph(decimal_to_binary_fracion(find_keys(data)))