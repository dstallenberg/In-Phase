import numpy as np
from src.quantum_phase_estimation.classical_postprocessing import remove_degeneracy

def to_array(result, bit):
    data = np.zeros(shape=(2**bit, 2**bit, 2))
    for i, r in enumerate(result):
        keys, values = remove_degeneracy(result, bit)
        keys = [int(x, 2) for x in keys]
        data[0, i, ::] = np.pad(keys, (0, 2**bit-keys.size), constant_values = 0)
        data[1, i, ::] = np.pad(values, (0, 2**bit-values.size), constant_values = 0)
    print(data)
    return(data)

def sort_array(data):
    ind = np.unravel_index(np.argsort(data[0,::,::], axis=1))
    data[0] = data[0][ind]
    data[1] = data[1][ind]
    return data

def find_keys(data):
    ind = np.argmax(data[1,::,::], axis=1)
    return data[1,::,::][ind]

def decimal_to_binary_fracion(list, bit):
    output = np.zeros_like(list)
    for dec in list:
        for i, bit in enumerate(str(bin(dec)[2:].rjust(bit, 0))):
            output[i] += 2**-i*int(bit)
    return output

