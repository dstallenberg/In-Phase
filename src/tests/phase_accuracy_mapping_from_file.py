from src.QEP_as_function import estimate_phase
import numpy as np
import matplotlib.pyplot as plt
from src.tests.phase_accuracy_mapping import map_phase, plot_results, plot_results_on_unit_cricle

if __name__ == "__main__":
	# Create points to map
	p=50
	t=3
	points = np.linspace(0, 2 * np.pi, p)

	# Some large results you probably want to save
	results = np.load(f"../../generated/tests/phase_mapping/results_{p}_points_{t}_times.npy")
	print(results)

	# Plot the data
	plot_results_on_unit_cricle(points, results[0], show=True)
