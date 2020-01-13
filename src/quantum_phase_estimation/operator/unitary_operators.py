import numpy as np
import cmath
from src.quantum_phase_estimation.quantumdecomp.quantum_decomp import matrix_to_qsharp
from src.quantum_phase_estimation.quantumdecomp.quantum_decomp import U_to_CU


def get_unitary_operators_array(operator, nancillas, qubits):
    arg = None
    if isinstance(operator, list):
        arg = operator[1]
        operator = operator[0]

    if isinstance(operator, (np.ndarray, np.generic)):
        # It is a matrix
        matrix = operator
    elif 'QASM' in operator:
        array = []

        for i in range(1, nancillas + 1):
            power = 2 ** (nancillas - i)

            operation = '\n'.join(operator.split('\n')[1:])
            result_operation = operation
            for j in range(power - 1):
                result_operation += operation

            result_operation = 'QASM\n' + U_to_CU(qubits, i - 1, nancillas, result_operation)

            array.append(result_operation)

        return array
    else:
        # It is an operator key
        matrix = operator_to_matrix(operator, arg)

    # print(matrix)
    array = []
    for i in range(1, nancillas + 1):
        power = 2**(nancillas - i)

        result_matrix = matrix
        for j in range(power - 1):
            result_matrix = np.dot(matrix, result_matrix)
            # print(result_matrix)

        result_operator = matrix_to_operator(result_matrix)

        if 'Invalid' in result_operator:
            result_operator = matrix_to_qsharp(result_matrix) #, i, nancillas)

        array.append(result_operator)

    return array


def operator_to_matrix(operator, arg=None):
    if arg is not None:
        arg = float(arg)
        return {
            'Rx': np.array([[cmath.cos(arg / 2), -1j * cmath.sin(arg / 2)],
                            [1j * cmath.sin(arg / 2), cmath.cos(arg / 2)]]),
            'Ry': np.array([[cmath.cos(arg / 2), -cmath.sin(arg / 2)],
                            [cmath.sin(arg / 2), cmath.cos(arg / 2)]]),
            'Rz': np.array([[cmath.exp(-1j * arg / 2), 0],
                            [0, cmath.exp(1j * arg / 2)]]),
            'CR': np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, cmath.exp(arg * 1j)]]),
            'CRk': np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, cmath.exp((2 * cmath.pi * 1j) / 2 ** arg)]]),
        }.get(operator, 'Invalid operator: There should be no argument for operator: ' + operator)

    return {
        'X': np.array([[0, 1],
                       [1, 0]]),
        'Y': np.array([[0, -1j],
                       [1j, 0]]),
        'Z': np.array([[1, 0],
                       [0, -1]]),
        'H': (1/2**0.5) * np.array([[1, 1],
                                    [1, -1]]),
        'I': np.array([[1, 0],
                       [0, 1]]),
        'S': np.array([[1, 0],
                       [0, 1j]]),
        'Sdag': np.array([[1, 0],
                          [0, -1j]]),
        'T': np.array([[1, 0],
                       [0, cmath.exp((1j * cmath.pi) / 4)]]),
        'Tdag': np.array([[1, 0],
                          [0, cmath.exp((-1j * cmath.pi) / 4)]]),
        'CNOT': np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 1],
                          [0, 0, 1, 0]]),
        'CX': np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0]]),
        'CY': np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, -1j],
                        [0, 0, 1j, 0]]),
        'CZ': np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, -1]]),
        'SWAP': np.array([[1, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 1]]),
        'Toffoli': np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 1, 0]])
    }.get(operator, 'Invalid operator: The given operator does not exist: ' + operator)


def matrix_to_hash (matrix):
    # converts matrix to tuple to be able to hash it
    return hash(tuple(map(tuple, matrix.astype(complex))))


def matrix_to_operator(matrix, arg=None):
    hash_of_matrix = matrix_to_hash(matrix)

    operator = {
        matrix_to_hash(np.array([[0, 1],
                                 [1, 0]])): 'X',
        matrix_to_hash(np.array([[0, -1j],
                                 [1j, 0]])): 'Y',
        matrix_to_hash(np.array([[1, 0],
                                 [0, -1]])): 'Z',
        matrix_to_hash((1/2**0.5) * np.array([[1, 1],
                                              [1, -1]])): 'H',
        matrix_to_hash(np.array([[1, 0],
                                 [0, 1]])): 'I',
        matrix_to_hash(np.array([[1, 0],
                                 [0, 1j]])): 'S',
        matrix_to_hash(np.array([[1, 0],
                                 [0, -1j]])): 'Sdag',
        matrix_to_hash(np.array([[1, 0],
                                 [0, cmath.exp((1j * cmath.pi) / 4)]])): 'T',
        matrix_to_hash(np.array([[1, 0],
                                 [0, cmath.exp((-1j * cmath.pi) / 4)]])): 'Tdag',
        matrix_to_hash(np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1],
                                 [0, 0, 1, 0]])): 'CNOT',
        matrix_to_hash(np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1],
                                 [0, 0, 1, 0]])): 'CX',
        matrix_to_hash(np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, -1j],
                                 [0, 0, 1j, 0]])): 'CY',
        matrix_to_hash(np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, -1]])): 'CZ',
        matrix_to_hash(np.array([[1, 0, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1]])): 'SWAP',
        matrix_to_hash(np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 1, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 1, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 1, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 1, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 1],
                                 [0, 0, 0, 0, 0, 0, 1, 0]])): 'Toffoli'
    }.get(hash_of_matrix, 'No matches')

    if operator != 'No matches':
        return operator

    if arg is not None:
        arg = float(arg)
        return {
            matrix_to_hash(np.array([[cmath.cos(arg / 2), -1j * cmath.sin(arg / 2)],
                                     [1j * cmath.sin(arg / 2), cmath.cos(arg / 2)]])): 'Rx ' + str(arg),
            matrix_to_hash(np.array([[cmath.cos(arg / 2), -cmath.sin(arg / 2)],
                                     [cmath.sin(arg / 2), cmath.cos(arg / 2)]])): 'Ry ' + str(arg),
            matrix_to_hash(np.array([[cmath.exp(-1j * arg / 2), 0],
                                     [0, cmath.exp(1j * arg / 2)]])): 'Rz ' + str(arg),
            matrix_to_hash(np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, cmath.exp(arg * 1j)]])): 'CR ' + str(arg),
            matrix_to_hash(np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, cmath.exp((2 * cmath.pi * 1j) / 2**arg)]])): 'CRk ' + str(arg),

        }.get(hash_of_matrix, 'Invalid operator: The given matrix does not require an argument or the matrix is invalid')
    else:
        # No argument is given so we try to find the R gate ourselves
        # TODO check which R gate
        if matrix.shape == (2, 2):
            # R
            if matrix[0][1] == 0 and matrix[1][0] == 0:
                # Rz
                return 'TODO'
            elif isinstance(matrix[1, 0], complex):
                # Rx
                return 'TODO'
            else:
                # Ry
                return 'TODO'
        elif matrix.shape == (4, 4):
            # Controlled R
            if np.count_nonzero(matrix - np.diag(np.diagonal(matrix))) == 0:
                # This checks if the matrix is diagonalized
                if matrix[0][0] == matrix[1][1] == matrix[2][2] == 1:
                    # This checks whether the first 3 diagonal entries are 1
                    polar_coords = cmath.polar(matrix[3][3])
                    if np.isclose(polar_coords[0], 1):
                        # Check whether r_coord equals 1
                        phi = polar_coords[1]

                        k = cmath.log(-(2 * cmath.pi) / phi, 2).real
                        if isinstance(k, int) or k.is_integer():
                            return 'CRk ' + str(int(k))

                        return 'CR ' + str(phi)

            return 'Invalid operator'
        else:
            return 'Invalid operator'
    return 'Something went wrong'


def find_controlled_equivalent(operator, control_bits, qubit):
    controls_string = ', '.join(map(lambda c: f'q[{c}]', control_bits))
    result = {
        'X': f'''CNOT {controls_string}, q[{qubit}]\n''',
        'Y': f'''Sdag q[{qubit}]\nCNOT {controls_string}, q[{qubit}]\nS q[{qubit}]\n''',
        'Z': f'''CZ {controls_string}, q[{qubit}]\n''',
        'CX': f'''Toffoli {controls_string}, q[{qubit}]\n''',
        'CY': f'''Sdag q[{qubit}]\nToffoli {controls_string}, q[{qubit}]\nS q[{qubit}]\n''',
        'CZ': f'''H q[{qubit}]\nToffoli {controls_string}, q[{qubit}]\nH q[{qubit}]\n''',
        'CNOT': f'''Toffoli {controls_string}, q[{qubit}]\n'''
    }.get(operator, 'Invalid operator')

    if result == 'Invalid operator':
        raise Exception('Operator not supported yet!')

    return result
