# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:41:06 2020

@author: Mio
"""
import numpy as np
from collections import OrderedDict


def remove_degeneracy_projectq(result, nancillas):
	res = dict()

	for r in result:
		if r[0] not in res:
			res[r[0]] = r[1]
		else:
			res[r[0]] += r[1]

	print(res)

	bin_string_processed = np.array([str(bin(int(k)))[2::].rjust(nancillas, '0')[-nancillas::] for k in res.keys() ])
	vals = np.array([val for val in res.values()])

	bin_string_processed, vals = (np.array(list(t)) for t in zip(*sorted(zip(bin_string_processed, vals))))

	current = ''
	final_keys = []
	final_values = []

	for index in range(len(bin_string_processed)):
		if bin_string_processed[index] != current:
			final_keys.append(bin_string_processed[index])
			current = bin_string_processed[index]
			final_values.append(vals[index])
		else:
			final_values[len(final_values) - 1] += vals[index]

	return np.array(final_values), final_keys

def remove_degeneracy(result, nancillas):
	if result == OrderedDict():
		raise ValueError("Received empty dict from QI, there is likely a syntax error in the qasm.")

	bin_string_processed = np.array([str(bin(int(k)))[2::].rjust(nancillas, '0')[-nancillas::] for k in result.keys() ])
	vals = np.array([val for val in result.values()])

	bin_string_processed, vals = (np.array(list(t)) for t in zip(*sorted(zip(bin_string_processed, vals))))

	current = ''
	final_keys = []
	final_values = []

	for index in range(len(bin_string_processed)):
		if bin_string_processed[index] != current:
			final_keys.append(bin_string_processed[index])
			current = bin_string_processed[index]
			final_values.append(vals[index])
		else:
			final_values[len(final_values) - 1] += vals[index]

	return np.array(final_values), final_keys


def binary_fraction_to_decimal(processed_tuple, desired_accuracy, nancillas):
	"""Returns the decimal fraction of a binary fraction formatted as a binary 
	number."""
	processed_list, keys = processed_tuple
	frac = 0
	bin_string = keys[np.argmax(processed_list)]
	for i in range(desired_accuracy):
		frac += 2**(-i-1)*int(bin_string[i])
	return frac


def decimal_accuracy(desired_accuracy):
	return int(-np.floor(np.log10(2**-desired_accuracy)))


def print_result(processed_tuple, desired_accuracy, nancillas):
	"""Prints the phase shift."""
	print("Phase shift is {0:0.{accuracy}f}+/-{1:0.{accuracy}f} times two pi for binary string {2}".format(
			binary_fraction_to_decimal(processed_tuple, desired_accuracy, nancillas),
			2**(-desired_accuracy+1), 
			processed_tuple[1][processed_tuple[0].argmax()],
			accuracy=decimal_accuracy(desired_accuracy)
			)
		)
	return binary_fraction_to_decimal(processed_tuple, desired_accuracy, nancillas)+2**(-desired_accuracy)/2, 2**(-desired_accuracy)
