# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:41:06 2020

@author: Mio
"""
import numpy as np
from collections import OrderedDict

def find_maximum(result):
	val = 0
	key = 0
	for i in result['histogram'].keys():
		if result['histogram'][i] > val:
			val = result['histogram'][i]
			key = i
	
	return key

def binary_fraction_to_decimal(bin_frac, desired_accuracy, qubits):
	"""Returns the decimal fraction of a binary fraction formatted as a binary 
	number."""
	frac = 0
	bin_string = str(bin(int(bin_frac)))[qubits+2::]
	print(bin_string)
	for i in range(desired_accuracy):
		frac += 2**(-i-1)*int(bin_string[i])
	return frac

def decimal_accuracy(desired_accuracy):
	return int(-np.floor(np.log10(2**-desired_accuracy)))

def print_result(bin_frac, desired_accuracy, qubits):
	"""Prints the phase shift in radians."""
	print("Phase shift is {0:0.{accuracy}f}+/-{1:0.{accuracy}f} radians".format(
			binary_fraction_to_decimal(bin_frac, desired_accuracy, qubits)*2*np.pi,
			2**-desired_accuracy*np.pi, 
			accuracy=decimal_accuracy(desired_accuracy)
			)
		)
	
if __name__ == '__main__':
	result = OrderedDict([('id', 6747326), ('url', 'https://api.quantum-inspire.com/results/6747326/'), ('job', 'https://api.quantum-inspire.com/jobs/6749903/'), ('created_at', '2020-01-10T13:02:43.137646Z'), ('number_of_qubits', 8), ('execution_time_in_seconds', 0.01200270652771), ('raw_text', ''), ('raw_data_url', 'https://api.quantum-inspire.com/results/6747326/raw-data/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('histogram', OrderedDict([('197', 0.001953125), ('207', 0.029296875), ('223', 0.12890625), ('195', 0.015625), ('222', 0.103515625), ('228', 0.01953125), ('215', 0.017578125), ('254', 0.03125), ('240', 0.0234375), ('251', 0.005859375), ('232', 0.02734375), ('249', 0.001953125), ('226', 0.015625), ('224', 0.05859375), ('239', 0.015625), ('206', 0.021484375), ('231', 0.015625), ('244', 0.01171875), ('194', 0.013671875), ('220', 0.03125), ('253', 0.009765625), ('204', 0.0078125), ('252', 0.017578125), ('242', 0.009765625), ('192', 0.013671875), ('255', 0.09375), ('219', 0.021484375), ('205', 0.001953125), ('199', 0.01171875), ('211', 0.013671875), ('225', 0.013671875), ('216', 0.015625), ('250', 0.013671875), ('237', 0.009765625), ('221', 0.021484375), ('230', 0.015625), ('247', 0.01171875), ('209', 0.005859375), ('234', 0.013671875), ('210', 0.00390625), ('246', 0.001953125), ('241', 0.01171875), ('238', 0.0078125), ('229', 0.009765625), ('248', 0.015625), ('217', 0.0078125), ('200', 0.009765625), ('214', 0.001953125), ('233', 0.005859375), ('236', 0.001953125), ('218', 0.001953125), ('245', 0.001953125), ('243', 0.001953125), ('235', 0.00390625)])), ('histogram_url', 'https://api.quantum-inspire.com/results/6747326/histogram/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('measurement_mask', 0), ('quantum_states_url', 'https://api.quantum-inspire.com/results/6747326/quantum-states/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('measurement_register_url', 'https://api.quantum-inspire.com/results/6747326/measurement-register/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('calibration', None)])
	qubits = 2
	res = bin(int(find_maximum(result)))
	print(res)
	desired_accuracy = 3
	print(binary_fraction_to_decimal(res, desired_accuracy, qubits))
	print_result(res, desired_accuracy, qubits)