from src.QEP_as_function import estimate_phase
import numpy as np
import matplotlib.pyplot as plt
from src.runner import async_calls


def map_phase(points, desired_bit_accuracy=3, p_succes=0.5, estimations_per_point=1):
	print("Phase	Iteration	Result")

	# Create arguments
	arguments = []
	for i in points:
		for j in range(estimations_per_point):
			print(f"{(i/(2*np.pi)):0.{int(-np.floor(np.log10(2**-desired_bit_accuracy)))}f}	{j+1}			", end='')
			unitary = f"QASM\n" \
					  f"Rz q[0], {-i}"

			arguments.append([unitary, desired_bit_accuracy, p_succes, "# No initialization given", True, False, 26, 1])


	#print('\n', arguments)
	result = async_calls(estimate_phase, arguments)
	#print(result)
	# for i in points:
	# 	for j in range(estimations_per_point):
	# 		print(f"{(i/(2*np.pi)):0.{int(-np.floor(np.log10(2**-desired_bit_accuracy)))}f}	{j+1}			", end='')
	# 		unitary = f"QASM\n" \
	# 				  f"Rz q[0], {-i}"
	# 		try:
	# 			result.append(
	# 				estimate_phase(unitary=unitary,
	# 							   desired_bit_accuracy=desired_bit_accuracy,
	# 							   p_succes_min=p_succes,
	# 							   shots=1)
	# 			)
	# 		except:
	# 			result.append(np.array([np.nan, np.nan, np.nan]))

	return np.array(result)


def plot_results(points, results, show=0):
	# Plot with error
	plt.errorbar(np.repeat(points, int(results.shape[0] / points.size)), results[::, 0] * 2 * np.pi,
				 yerr=results[::, 1] * 2 * np.pi, label="QPE", fmt='.')
	plt.plot(points, points, label="Actual phase")

	# Formatting
	plt.xlabel("Input phase [rad]")
	plt.ylabel("Output phase [rad]")
	plt.title("Phase mapping with $p_{succes}=%s$"%results[0, 2])
	plt.legend()

	# Saving and displaying
	plt.savefig(f"../../img/phase_map_{points.size}_points.png")
	if show:
		plt.show()

def plot_results_on_unit_cricle(points, results, show=0, size=7):
	# Plot with error
	fig = plt.figure(figsize=(size,size))
	ax = fig.gca()
	ax.errorbar(np.real(np.exp(results[::, 0] * 2 * np.pi*1j)),
				np.imag(np.exp(results[::, 0] * 2 * np.pi*1j)),
				label="QPE",
				fmt='.')
	ax.plot(np.real(np.exp(points*1j)), np.imag(np.exp(points*1j)), '.-', label="Actual phase")

	# Formatting
	ax.set_xlabel("Input phase [rad]")
	ax.set_ylabel("Output phase [rad]")
	ax.set_title("Phase mapping with $p_{succes}=%s$"%results[0, 2])
	plt.legend()

	# Saving and displaying
	plt.savefig(f"../../img/phase_map_{points.size}_points_on_circle.png")
	if show:
		plt.show()


if __name__ == "__main__":
	# Create points to map
	desired_bit_accuracy = 5
	p = 1/(2**-desired_bit_accuracy)
	print(p)
	points = np.linspace(0, 2 * np.pi, p)

	results = map_phase(points, desired_bit_accuracy, 0.5, estimations_per_point=3)

	# Some large results you probably want to save
	if True:
		times = int(results.shape[0] / points.size)
		np.save(f"../../generated/tests/phase_mapping/results_{points.size}_points_{times}_times.npy", results)

	# Plot the data
	plot_results(points, results, show=True)
