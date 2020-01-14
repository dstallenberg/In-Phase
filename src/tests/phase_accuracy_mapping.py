from src.QEP_as_function import estimate_phase
import numpy as np
import matplotlib.pyplot as plt


def map_phase(points, desired_bit_accuracy=3, p_succes=0.5, estimations_per_point=1):
	result = []
	print("Phase	Iteration	Result")
	for i in points:
		for j in range(estimations_per_point):
			print(f"{(i/(2*np.pi)):0.{int(-np.floor(np.log10(2**-desired_bit_accuracy)))}f}	{j+1}			", end='')
			unitary = f"QASM\n" \
					  f"Rz q[0], {-i}"
			# print(unitary)
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


def plot_results(points, results, show=0):
	plt.errorbar(np.repeat(points, int(results.shape[0] / points.size)), results[::, 0] * 2 * np.pi,
				 yerr=results[::, 1] * 2 * np.pi, label="QPE", fmt='.')
	plt.plot(points, points, label="Actual phase")
	plt.legend()
	plt.savefig(f"../../img/phase_map_{points.size}_points.png")
	if show:
		plt.show()


if __name__ == "__main__":
	points = np.linspace(0, 2 * np.pi, 50)
	results = map_phase(points, 10, 0.5, estimations_per_point=3)
	if True:
		times = int(results.shape[0] / points.size)
		np.save(
			f"../../generated/tests/phase_mapping/results_{points.size}_points_{times}_times.npy",
			(results, points))
	plot_results(points, results)
