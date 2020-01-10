# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:03:06 2020

@author: Mio
"""
import numpy as np

def error_estimate(desired_bit_accuracy, probability_of_succes):
	"""Given desired bit accuracy and desired probability of succes, returns
	the needed qubits and the calcuated probability of succes."""
	epsilon = 1-probability_of_succes
	t = desired_bit_accuracy + np.ceil(np.log2(2+1/(2*epsilon)))
	calc_probability_of_succes(2**(t-desired_bit_accuracy)-1)
	return t, calc_probability_of_succes(2**(t-desired_bit_accuracy)-1)
	

def calc_probability_of_succes(e):
	return 1-1/(2*(e-1))

if __name__ == '__main__':
	print(error_estimate(10, 0.96))