import numpy as np
from src.quantum_phase_estimation.processing.classical_postprocessing import remove_degeneracy


def to_array(result, bit, nancilla):
    data = np.zeros(shape=(2, 2**nancilla, 2**nancilla))

    for i, r in enumerate(result):
        values, keys = remove_degeneracy(r['histogram'], nancilla)
        keys = np.array([int(x, 2) for x in keys])
        print(2**nancilla-keys.size)
        data[0, i, ::] = np.pad(keys, (0, 2**nancilla-keys.size), constant_values = 0, mode='constant')
        data[1, i, ::] = np.pad(values, (0, 2**nancilla-values.size), constant_values = 0, mode='constant')

    return data


def sort_array(data):
    ind = np.unravel_index(np.argsort(data[0,::,::], axis=1), shape=data[0].shape)

    data[0] = data[0][ind]
    data[1] = data[1][ind]

    return data


def find_keys(data):
    ind = np.argmax(data[1], axis=1)
    temp = np.zeros(shape=data.shape[1])
    for i in range(temp.size):
        temp[i] = data[0, i, ind[i]]

    return temp.astype(int)


def decimal_to_binary_fracion(list, bit):
    output = np.zeros(shape=list.size, dtype=np.float)

    for i, dec in enumerate(list):
        for j, b in enumerate( str(bin(dec))[2:].rjust(bit, '0') ):
            output[i] += 2**(-j-1)*int(b)

    return output

