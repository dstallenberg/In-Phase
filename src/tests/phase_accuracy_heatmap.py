from src.QEP_as_function import generate_qasm, get_authentication
import numpy as np
import matplotlib.pyplot as plt
from src.runner import async_calls
from src.quantum_phase_estimation.classical_postprocessing import remove_degeneracy, binary_fraction_to_decimal
from src.quantum_phase_estimation.error_estimation import error_estimate
from getpass import getpass
from quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication
from quantuminspire.api import QuantumInspireAPI
import os
from collections import OrderedDict
from src.runner import async_calls

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

def remove_degeneracy(result, nancillas):
	if result == OrderedDict():
		print("Received empty dict from QI, there is a syntax error in the qasm.")
		raise

	bin_string_processed = np.array(
		[int(str(bin(int(k)))[2::].rjust(nancillas, '0')[-nancillas::], 2) for k in result.keys()])
	vals = np.array([val for val in result.values()])

	processed_list = []
	keys = []

	temp = np.zeros(shape=vals.shape)

	for s in bin_string_processed:
		if np.sum((bin_string_processed == s) * temp) == False:
			index = bin_string_processed == s
			temp += index
			processed_list.append(np.sum(vals[index]))
			keys.append(s)

	# print(bin_string_processed.size, '\n', processed_list.size, '\n',np.sum(processed_list), '\n', temp)
	return np.array(processed_list), np.array(keys)

def make_heatmap(desired_bit_accuracy):
	"""making a heatmap"""
	x = np.linspace(0, 2*np.pi, (2**desired_bit_accuracy))
	print(x)

	result = []
	for i in x:
		print(i)
		unitary = f"QASM\n" \
				  f"Rz q[0], {-i}"
		qasm, qubits, nancillas, p_succes = generate_qasm(unitary,
														  desired_bit_accuracy,
														  0.5,
														  max_qubits=26)
		result.append(get_results(qasm))

	np.save(f"heatmap_{desired_bit_accuracy}.npy", result)
	return result


def make_heatmap_multi(desired_bit_accuracy):
	"""making a heatmap"""
	x = np.linspace(0, 2 * np.pi, (2 ** desired_bit_accuracy))
	print(x)

	arguments = []
	for i in x:
		#print(i)
		unitary = f"QASM\n" \
				  f"Rz q[0], {-i}"
		qasm, qubits, nancillas, p_succes = generate_qasm(unitary,
														  desired_bit_accuracy,
														  0.5)
		arguments.append([qasm, None])
	print(f"Sending {len(arguments)} jobs to QI")
	res = async_calls(get_results, arguments)
	np.save(f"heatmap_{desired_bit_accuracy}.npy", res)
	return res

def to_bin_frac(key, bits):
	for x in range(2**bits):
		if x not in key:
			#print(x)
			key = np.append(key, x)
	fracs = np.zeros(shape=2**bits)

	for i, k in enumerate(key):
		for j, bit in enumerate(str(bin(k))[2:].rjust(bits, '0')):
			fracs[i] += (2**(-j-1))*int(bit)
	return fracs

def plot_heatmap(result, bits):
	#print(result[0])
	keys = np.zeros(shape=(len(result), 2**bits))
	vals = np.zeros(shape=(len(result), 2**bits))
	#print(keys.shape)

	frac = np.zeros(shape = (2**bits, 2**bits))
	for i, r in enumerate(result):
		v, k = remove_degeneracy(r, bits)
		frac[i,::] = to_bin_frac(k, bits)
		for x in range(2**bits-len(v)):
			v = np.append(v, 0)
		vals[i,::] = v
		"""frac = 0
		bin_string = str(bin(k[np.argmax(v)]))[2:].rjust(bits, '0')
		for m in range(bits):
			frac += 2 ** (-m - 1) * int(bin_string[m])
		print(frac)"""

	fig = plt.figure(figsize=(7,7))
	ax = plt.gca()
	index = np.argsort(frac, axis=1)
	ind = np.argmax(vals, axis=1)
	#ind = np.unravel_index(np.argsort(x, axis=None), x.shape)
	#print(np.take_along_axis(vals, ind, axis=1))
	print(frac[ind][0,::])
	cs = ax.imshow(np.take_along_axis(vals, index, axis=1), aspect='auto')
	fig.colorbar(cs)
	ax.set_ylabel("Key")
	ax.set_xlabel("Input phase")
	#x = np.linspace(0, 2 * np.pi, 6)
	#ax.set_xticks(x)
	#ax.set_xticklabels(np.round(x, 3))
	fig.tight_layout()
	plt.show()


def get_results(qasm, none=None):
	"""Calculate results using QuantumInspire"""
	# Get authentication
	try:
		authentication = get_authentication()
		qi = QuantumInspireAPI(QI_URL, authentication, 'Quantum Phase Estimation')
		backend_type = qi.get_backend_type_by_name('QX single-node simulator')
		result = qi.execute_qasm(qasm, backend_type=backend_type)
		print("One done")
		return result['histogram']
	except:
		return get_results(qasm)

if __name__ == "__main__":
	bit=12
	p=0.5
	try:
		result = np.load(f"heatmap_{bit}.npy", allow_pickle = True)
	except:
		result = make_heatmap_multi(bit)
	plot_heatmap(result, bits=bit)
