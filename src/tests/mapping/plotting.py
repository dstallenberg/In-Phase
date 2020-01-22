import matplotlib.pyplot as plt
import numpy as np

from src.quantum_phase_estimation.util_functions import error_estimate

def heatmap(data, show=True):
    fig = plt.figure(figsize=(7,7))
    ax = plt.gca()

    cs = ax.imshow(data)
    fig.colorbar(cs)

    ax.set_xlabel("Input phase")
    ax.set_ylabel("Output phase")

    fig.savefig(f"../../../img/heatmap_{np.log2(data.shape[0])}.png")

    if show:
        plt.show()

def graph(data, show=True):
    fig = plt.figure(figsize=(7, 7))
    ax = plt.gca()

    ax.errorbar(np.linspace(0, 1, data.size),
                data,
                yerr=(np.repeat(0, data.shape[0]),
                      np.repeat(2**(-np.log2(data.shape[0])), data.shape[0])),
                fmt='.',
                label="From QI")

    ax.plot(np.linspace(0, 1, data.size), np.linspace(0, 1, data.size), label="Expected")

    ax.set_xlabel("Input")
    ax.set_ylabel("Output")
    plt.legend()

    fig.savefig(f"../../../img/heatmap_{np.log2(data.shape[0])}.png")

    if show:
        plt.show()