import matplotlib.pyplot as plt
import numpy as np

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

    ax.plot(np.linspace(0, 2*np.pi, data.size), data)

    ax.set_xlabel("Input")
    ax.set_ylabel("Output")

    fig.savefig(f"../../../img/heatmap_{np.log2(data.shape[0])}.png")

    if show:
        plt.show()