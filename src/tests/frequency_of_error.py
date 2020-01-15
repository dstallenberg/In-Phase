from src.QEP_as_function import estimate_phase
import numpy as np
import matplotlib.pyplot as plt


def frequency_of_error(sample_size, phase, desired_bit_accuracy=3, p_succes=0.5):
    result = []
    print("Iteration	Result")
    for i in range(sample_size):
        print(f"{(phase / (2 * np.pi)):0.{int(-np.floor(np.log10(2 ** -desired_bit_accuracy)))}f}			",
              end='')
        unitary = f"QASM\n" \
                  f"Rz q[0], {phase}"
        try:
            result.append(
                estimate_phase(unitary=unitary,
                               desired_bit_accuracy=desired_bit_accuracy,
                               p_succes_min=p_succes,
                               shots=1)
            )
        except:
            result.append(np.array([np.nan, np.nan, np.nan]))

    return np.array(result)


def calc_freq(results, phase, show=0):
    # Plot with error
    return np.sum(np.isclose(results[0], phase, results[1]))/results[0].size


if __name__ == "__main__":
    # Create points to map
    p = 50
    t = 3

    # Some large results you probably want to save
    results = frequency_of_error(10, 0.25*2*np.pi)
    print(results)

    # Plot the data
    calc_freq(results, 0.25*2*np.pi, show=True)
