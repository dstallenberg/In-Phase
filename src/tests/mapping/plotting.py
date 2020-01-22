import matplotlib.pyplot as plt
import numpy as np

from src.quantum_phase_estimation.error_estimation import error_estimate

def heatmap(data, show=True):
    fig = plt.figure(figsize=(7,7))
    ax = plt.gca()

    cs = ax.imshow(np.rot90(data), aspect='auto')
    fig.colorbar(cs)

    ax.set_xlabel(r"Input phase $\varphi/2\pi$")
    xticks = ax.get_xticks()
    print(xticks)
    x_labels = ['{0:0.3f}'.format(x) for x in np.linspace(xticks[0]/xticks[-1], xticks[-1]/data.shape[0], len(xticks))]
    ax.set_xticklabels(x_labels)



    ax.set_ylabel(r"Output phase $\varphi/2\pi$")
    yticks = ax.get_yticks()
    print(yticks)
    y_labels = ['{0:0.3f}'.format(y) for y in np.linspace(yticks[0]/yticks[-1], yticks[-1]/data.shape[1], len(yticks))]
    ax.set_yticklabels(reversed(y_labels))

    fig.savefig(f"img/heatmap_{np.log2(data.shape[0])}.png")

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

    ax.set_xlabel("Input phase [$\cdot 2\pi$]")
    ax.set_ylabel("Output phase [$\cdot 2\pi$]")
    plt.legend()

    fig.savefig(f"img/graph_{np.log2(data.shape[0])}.png")

    if show:
        plt.show()