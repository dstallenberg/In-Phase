import random
import numpy as np

rotation = ["Rx", "Ry", "Rz"]
arg_gates = ["Rx", "Ry", "Rz", "CR"]
no_arg_gates = ["H", "X", "Y", "Z", "CNOT", "Toffoli", "CZ", ]

def introduce_error(qasm_code, mu, sigma):
    # This function takes the generated QASM code and adds errors. These errors get randomly generated with a Gaussian distribution and get applied to each
    # gate in the QASM code. For gates who don't take in an argument, an extra Rx, Ry or Rz gate gets added with a random argument. Which rotation gate it is gets
    # chosen randomly. For gates who take an argument, e.g. Rx, Ry etc, this error gets added to the original argument.

    lines = qasm_code.splitlines()
    final_qasm = ''
    for single_line in lines:
        for j in no_arg_gates:
            if j in single_line:
                final_qasm += single_line + "\n"
                if "|" in single_line:
                    start = 0
                    for x in range(single_line.count("|")+1):
                        if x < single_line.count("|"):
                            end = single_line.find("|", start)
                            begin_target = single_line.rfind("[", start, end)
                            end_target = single_line.rfind("]", start, end)
                            target_qubit = single_line[begin_target+1:end_target]
                            start = single_line.find("|", start)
                        else:
                            target_qubit = single_line[single_line.rfind("[", start)+1:single_line.rfind("]", start)]
                        final_qasm += "%s q[%s], %f\n" % (
                        random.choice(rotation), target_qubit, np.random.normal(mu, sigma))
                else:
                    target_qubit = single_line[single_line.rfind("[") + 1:single_line.rfind("]")]
                    final_qasm += "%s q[%s], %f\n" % (random.choice(rotation), target_qubit, np.random.normal(mu, sigma))
                break
            else:
                if j == "CZ":
                    for j in arg_gates:
                        if j in single_line:
                            val = single_line[single_line.rfind(",") + 1:]
                            final_qasm += single_line.replace(val, ' ' + str( +float(val) + np.random.normal(mu, sigma))) + "\n"
                            break
                        else:
                            if j == "CR":
                                final_qasm += single_line + "\n"
    return final_qasm

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


