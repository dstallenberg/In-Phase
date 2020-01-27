# In-Phase
> A quantum phase estimation tool

This README introduces In-Phase: a tool to implement Quantum Phase Estimation (QPE) for Quantum Inspire, a quantum circuit simulator. 
In-Phase creates a quantum circuit to estimate the phase of any given unitary matrix. 
This tool takes two limitations of real quantum circuits into account: phase errors caused by quantum gates and the fixed topology of mapped qubits on a real quantum circuit.

Collaborators:
* Beer de Zoeten
* Daniel Vlaardingerbroek
* Dimitri Stallenberg
* Mio Poortvliet
    
## Installing from source

Clone the project
```
git clone https://github.com/dstallenberg/QEP-PhaseEstimation.git
```

Open the project in your favorite IDE

Gather requirements
```
pip install .
```

Run main.py

## Usage
The most important function to use is as follows:
```python
qasm_code = generate_qasm_code(nancillas, qubits, unitary)
```
This function has several possible arguments:
* The first argument is the amount of nancillas these dictate the accuracy of the output phase.
* The second argument is the amount of qubits that your unitary uses.
* The third and most important argument is the unitary which is also the only required argument. This unitary can be one of the following:
    * A string containing a singular gate and one argument if the gate requires it.
    ```python
    unitary = 'Rz 0.5'
    ```
    > Note: Do not add anything to the format: "[gate] [argument]".
     If there is no argument the format is "[gate]".
    * A string containing a circuit in qasm code prefixed by the QASM key word.
    ```python
    unitary = '''
    QASM
    H q[0]
    X q[1]
    CNOT q[0], q[1]
    '''
    ```
    > Note: Make sure to not add any additional spaces or enters to the qasm code, otherwise the tool won't be able to optimise the resulting qasm code. 
    * A unitary numpy matrix where the dimensions are given by d = 2**q where q is the amount of qubits.
    ```python
    unitary = np.array([[1, 0], 
                        [0, -1]])
    ```
    > Note: Make sure that the dimensions follow the given formula and make sure that the matrix is unitary.

Look at the examples in the examples directory for a more explicit explanation.

## Features
In-Phase also contains several other functionalities, most of which can be found in the examples directory

#### Error Estimation

Example:
```python
from src.quantum_phase_estimation.util_functions import error_estimate

desired_bit_accuracy = 5
minimum_chance_of_success = 0.5

nancillas, p_succes = error_estimate(desired_bit_accuracy, minimum_chance_of_success)
```
Expected outcome:
```python
nancillas == 7
p_succes == 0.75
```

#### Finding amount of qubits

Example:
```python
from src.quantum_phase_estimation.util_functions import find_qubits_from_unitary

unitary = 'Z'
nancillas = 3

qubits, extra_empty_bits = find_qubits_from_unitary(unitary, nancillas)
```
Expected outcome:
```python
qubits == 1
extra_empty_bits == 0
```
> Note: extra_empty_bits is always zero unless the optional argument 'topology' is given

#### Optimizing cQASM

Example:
```python
from src.qasm_optimizer.optimizer import optimize

qasm_code = '''
X q[0]
X q[0]
H q[0]
'''
nancillas = 3
qubits = 1
extra_empty_bits = 0

qasm_code = optimize(qasm_code, nancillas, qubits, extra_empty_bits)
```
Expected outcome:
```python
qasm_code == '''
H q[0]
'''
```

#### Topology mapping

Example:
```python
from src.qasm_topology_mapper.mapping import map_to_topology

topology = [[0, 1],
            [0, 2]
            [1, 3]
            [2, 3]]
qasm_code = '''
CNOT q[0], q[3]
'''

qasm_code = map_to_topology(topology, qasm_code)
```
Expected outcome:
```python
qasm_code == '''
SWAP q[0], q[1]
CNOT q[1], q[3]
SWAP q[0], q[1]
'''
```

#### Error introduction

Example:
```python
from src.qasm_error_introducer.error_introducer import introduce_error

qasm_code = '''
Rz q[0], 0.1
'''
mu = 0
sigma = 0.2

qasm_code = introduce_error(qasm_code, mu, sigma)
```
Expected outcome:
```python
qasm_code == '''
Rz q[0], 0.3
Rz q[0], 0.1
'''
```

#### cQASM to ProjectQ conversion

Example:
```python
from src.qasm_to_projectq.converter import qasm_to_projectq

qasm_code = '''
X q[0]
'''

projecq_code = qasm_to_projectq(qasm_code)
```
Expected outcome:
```python
projecq_code == '''
X | q0
'''
```

##  Sources
We were inspired by quantum inspire and used the provided sdk to apply our generated qasm code to a quantum backend:
* https://www.quantum-inspire.com/

We used the following repository to convert unitary matrices to qasm code:
* https://github.com/fedimser/quantum_decomp/
