# In-Phase tool
> A quantum phase estimation tool
Group 7

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

#TODO 


This function has several possible arguments. The most important argument is the unitary which is also the only required argument. This unitary can be one of the following:
* A string containing a singular gate and one argument if the gate requires it.
```python
unitary = 'Rz 0.5'
```
> Note: Do not add anything to the format: "[gate] [argument]".
> If there is no argument the format is "[gate]".
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

##  Sources
We were inspired by quantum inspire and used the provided sdk to apply our generated qasm code to a quantum backend:
* https://www.quantum-inspire.com/

We used the following repository to convert unitary matrices to qasm code:
* https://github.com/fedimser/quantum_decomp/
