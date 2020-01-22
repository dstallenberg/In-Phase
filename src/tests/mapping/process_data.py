import numpy as np
from src.quantum_phase_estimation.classical_postprocessing import remove_degeneracy


def to_array(result, bit, nancilla):
    data = np.zeros(shape=(2, 2**bit, 2**nancilla))

    for i, r in enumerate(result):
        values, keys = remove_degeneracy(r['histogram'], nancilla)
        keys = np.array([int(x, 2) for x in keys])

        for j in range(2**nancilla):
            if np.sum(keys==j):
                data[0, i, j] = keys[keys==j]
                data[1, i, j] = values[keys==j]

    return data


def sort_array(data):
    ind = np.unravel_index(np.argsort(data[0,::,::], axis=1), shape=data[0].shape)

    data[0] = data[0][ind]
    data[1] = data[1][ind]

    return data


def find_keys(data):
    ind = np.argmax(data[1], axis=1)
    temp = np.zeros(shape=ind.size)

    for i in range(temp.size):
        temp[i] = data[0, i, ind[i]]

    return temp.astype(int)


def decimal_to_binary_fracion(list, bit):
    output = np.zeros(shape=list.size, dtype=np.float)

    for i, dec in enumerate(list):
        for j, b in enumerate( str(bin(dec))[2:].rjust(bit, '0') ):
            output[i] += 2**(-j-1)*int(b)

    return output

