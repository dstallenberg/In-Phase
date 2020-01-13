import numpy as np
from src.quantum_phase_estimation.quantumdecomp.quantum_decomp import matrix_to_qsharp
from src.quantum_phase_estimation.quantumdecomp.quantum_decomp import U_to_CU
w = np.exp((2j / 3) * np.pi)
A = np.array([[1, 1, 1, 0],
                  [1, w, w * w, 0],
                  [1, w * w, w, 0],
                  [0, 0, 0, -1j*np.sqrt(3)]]) / np.sqrt(3)


print(U_to_CU(2,1,2, "Test1\nTest2\nTest3"))