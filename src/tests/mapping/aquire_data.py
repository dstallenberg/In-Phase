import numpy as np
from src.runner import async_calls
from src.QEP_as_function import estimate_phase

def get_results(bit=5, try_from_file = True):
    if try_from_file:
        try:
            fname = f"generated/tests/mapping/heatmap_{bit}.npy"
            data = np.load(fname, allow_pickle=True)
            print(f"Loaded data from {fname}")
            return data
        except:
            print(f"No file '{fname}' found. Gathering from QI...")
    return from_qi(bit)

def from_qi(bit, save=True, succes=0.5):
    arguments = []
    points = np.linspace(0, 2*np.pi, 2**bit)
    print(f"Preparing to send {2**bit} jobs to QI")
    for i in points:
        #print(f"{(i / (2 * np.pi)):0.{int(-np.floor(np.log10(2 ** -bit)))}f}	{1}			")
        unitary = f"QASM\n" \
                  f"Rz q[0], {-i}"

        arguments.append(
            [unitary, bit, succes, "# No initialization given", False, False, 26, 1])

    print("QASM is generated. Sending jobs...")
    result = async_calls(estimate_phase, arguments)
    print("Recieved all jobs!")
    if save:
        fname = f"generated/tests/mapping/heatmap_{bit}.npy"
        print(f"Saving to {fname}")
        np.save(fname, result)
    return np.array(result)[::, 0]

if __name__ == "__main__":
    np.load("generated/tests/mapping/heatmap_4.npy", allow_pickle=True)
    get_results(4)