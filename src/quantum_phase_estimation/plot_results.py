# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:54:18 2020

@author: Mio
"""

import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

def plot_results(result, nancillas, qubits, p_succes):
	if result['raw_text'] and len(result['raw_text']) > 1:
		raise Exception(result['raw_text'])

	correction_number = 0
	for i in range(qubits):
		correction_number+=2**(nancillas+i)

	print("Given the desired bit accuracy and probability of succes, {0} ancillas will be used resulting in a {1:0.3f} probability of succes.".format(nancillas, p_succes))
	binary_keys = [str(bin(int(k)))[2+qubits::] for k in result['histogram'].keys()]
	
	fig = plt.figure(figsize=(8,3))
	ax = plt.gca()
	
	ax.set_title("Phase estimation with {0}-bit accuracy and probability {1:0.3f}".format(nancillas, p_succes))
	
	ax.bar(binary_keys, result['histogram'].values())
	plt.xticks(rotation = 'vertical')
	fig.show()
	
	
result = OrderedDict([('id', 6747326), ('url', 'https://api.quantum-inspire.com/results/6747326/'), ('job', 'https://api.quantum-inspire.com/jobs/6749903/'), ('created_at', '2020-01-10T13:02:43.137646Z'), ('number_of_qubits', 8), ('execution_time_in_seconds', 0.01200270652771), ('raw_text', ''), ('raw_data_url', 'https://api.quantum-inspire.com/results/6747326/raw-data/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('histogram', OrderedDict([('197', 0.001953125), ('207', 0.029296875), ('223', 0.12890625), ('195', 0.015625), ('222', 0.103515625), ('228', 0.01953125), ('215', 0.017578125), ('254', 0.03125), ('240', 0.0234375), ('251', 0.005859375), ('232', 0.02734375), ('249', 0.001953125), ('226', 0.015625), ('224', 0.05859375), ('239', 0.015625), ('206', 0.021484375), ('231', 0.015625), ('244', 0.01171875), ('194', 0.013671875), ('220', 0.03125), ('253', 0.009765625), ('204', 0.0078125), ('252', 0.017578125), ('242', 0.009765625), ('192', 0.013671875), ('255', 0.09375), ('219', 0.021484375), ('205', 0.001953125), ('199', 0.01171875), ('211', 0.013671875), ('225', 0.013671875), ('216', 0.015625), ('250', 0.013671875), ('237', 0.009765625), ('221', 0.021484375), ('230', 0.015625), ('247', 0.01171875), ('209', 0.005859375), ('234', 0.013671875), ('210', 0.00390625), ('246', 0.001953125), ('241', 0.01171875), ('238', 0.0078125), ('229', 0.009765625), ('248', 0.015625), ('217', 0.0078125), ('200', 0.009765625), ('214', 0.001953125), ('233', 0.005859375), ('236', 0.001953125), ('218', 0.001953125), ('245', 0.001953125), ('243', 0.001953125), ('235', 0.00390625)])), ('histogram_url', 'https://api.quantum-inspire.com/results/6747326/histogram/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('measurement_mask', 0), ('quantum_states_url', 'https://api.quantum-inspire.com/results/6747326/quantum-states/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('measurement_register_url', 'https://api.quantum-inspire.com/results/6747326/measurement-register/b2bcf5e9e6874e1b5dd25b4368d958fdd73e069fbc0eced8f4e8057dfb224418/'), ('calibration', None)])

if __name__ == '__main__':
	plot_results(result, 6, 2, 0.9)