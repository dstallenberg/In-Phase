from src.QEP_as_function import estimate_phase
import numpy as np
import matplotlib.pyplot as plt


def frequency_of_error(sample_size, phase, desired_bit_accuracy=3, p_succes=0.5):
    result = []
    print("Iteration	Result")
    for i in range(sample_size):
        print(f"{i+1}			",
              end='')
        unitary = f"QASM\n" \
                  f"Rz q[0], {-phase}"
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
    print("{0}+/-{1} within {2}".format(results[::, 0], phase/(2*np.pi), results[0, 1]))

    plt.hist(results[::,0])
    plt.show()

    return np.sum(np.isclose(results[::, 0], phase/(2*np.pi), atol=results[0, 1]))/results[::, 0].size


if __name__ == "__main__":
    phase = 0.25*2*np.pi
    results = frequency_of_error(100, phase, desired_bit_accuracy=5)

    # Plot the data
    print(f"Frequentistic probability is {calc_freq(results, phase, show=True)}.")
