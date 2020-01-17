import random
import numpy as np

rotation = ["Rx", "Ry", "Rz"]
arg_gates = ["Rx", "Ry", "Rz", "CR"]
no_arg_gates = ["H", "X", "Y", "Z", "CNOT", "Toffoli", "CZ", ]
def introduce_error(qasm_code, mu, sigma):

    lines = qasm_code.splitlines()
    final_qasm = ''
    for single_line in lines:
        for j in no_arg_gates:
            if j in single_line:
                target_qubit = single_line[single_line.rfind("[") + 1]
                final_qasm += single_line + "\n"
                final_qasm += "%s q[%s], %f\n" % (random.choice(rotation), target_qubit, np.random.normal(mu, sigma))
                break
            else:
                if j == "CZ":
                    for j in arg_gates:
                        if j in single_line:
                            val = single_line[single_line.rfind(",") + 2:]
                            final_qasm += single_line.replace(val, str(float(val) + np.random.normal(mu, sigma))) + "\n"
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


