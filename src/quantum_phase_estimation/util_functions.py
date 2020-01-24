# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:03:06 2020

@author: Mio
"""
import numpy as np
import re

from src.quantum_phase_estimation.processing.classical_postprocessing import remove_degeneracy


def error_estimate(desired_bit_accuracy, probability_of_succes):
	"""Given desired bit accuracy and desired probability of succes, returns
	the needed qubits and the calcuated probability of succes."""
	epsilon = 1-probability_of_succes
	t = desired_bit_accuracy + np.ceil(np.log2(2+1/(2*epsilon)))
	calc_probability_of_succes(2**(t-desired_bit_accuracy)-1)
	return int(t), calc_probability_of_succes(2**(t-desired_bit_accuracy)-1)
	

def calc_probability_of_succes(e):
	return 1-1/(2*(e-1))


def find_qubits_from_unitary(unitary, nancillas, topology=None, max_qubits=26):
	qubits_in_top = False
	if topology is not None:
		found_max = 0
		for edge in topology:
			found_max = max(found_max, int(edge[0]) + 1)
			found_max = max(found_max, int(edge[1]) + 1)

		qubits_in_top = found_max

	if type(unitary) == np.ndarray:
		qubits = int(np.log2(unitary.shape[0]))
	else:
		result = [e for e in re.split("[^0-9.]", unitary) if e != '' and not '.' in e]
		if len(result) == 0:
			qubits = 1
		else:
			qubits = max(map(int, result)) + 1

	extra_empty_bits = 0
	if qubits_in_top:
		extra_empty_bits = (qubits_in_top - 2 * qubits - nancillas)

	if extra_empty_bits < 0:
		raise ValueError(f"Need more qubits than your topology allows! (need {2 * qubits + nancillas}, maximum is {qubits_in_top})")


	if qubits_in_top and 2 * qubits + nancillas + extra_empty_bits > qubits_in_top:
		raise ValueError(f"Need more qubits than your topology allows! (need {2 * qubits + nancillas + extra_empty_bits}, maximum is {qubits_in_top})")


	if 2 * qubits + nancillas + extra_empty_bits > max_qubits:
		raise ValueError(f"Need more qubits than allowed! (need {2 * qubits + nancillas + extra_empty_bits}, maximum is {max_qubits})")

	return qubits, extra_empty_bits


def decimal_to_binary_fracion(list, ancilla):
	output = np.zeros(shape=list.size, dtype=np.float)

	for i, dec in enumerate(list):
		for j, b in enumerate( str(bin(dec))[2:].rjust(ancilla, '0') ):
			output[i] += 2**(-j-1)*int(b)

	return output


def find_max_value_keys(data):
	ind = np.argmax(data[1], axis=1)
	temp = np.zeros(shape=ind.size)

	for i in range(temp.size):
		temp[i] = data[0, i, ind[i]]

	return temp.astype(int)


def to_array(result, bit, nancilla):
	data = np.zeros(shape=(2, 2**bit, 2**nancilla))

	for i, r in enumerate(result):
		values, keys = remove_degeneracy(r['histogram'], nancilla)
		keys = np.array([int(x, 2) for x in keys])

		for j in range(2**nancilla):
			if np.sum(keys == j):
				data[0, i, j] = keys[keys == j]
				data[1, i, j] = values[keys == j]

	return data
