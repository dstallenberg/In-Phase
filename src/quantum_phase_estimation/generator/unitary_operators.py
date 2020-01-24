import numpy as np
import cmath
import string
from src.quantum_phase_estimation.quantumdecomp.quantum_decomp import matrix_to_qasm
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
        # It is an generator key
        matrix = operator_to_matrix(operator, arg)

    array = []
    for i in range(1, nancillas + 1):
        power = 2**(nancillas - i)

        result_matrix = matrix
        for j in range(power - 1):
            result_matrix = np.dot(matrix, result_matrix)

        result_matrix = result_matrix.round(decimals=5)

        result_operator = matrix_to_operator(result_matrix)

        if 'Invalid' in result_operator:
            result_operator = matrix_to_qasm(result_matrix, i-1, nancillas)
        else:
            # This means there is an argument
            if ' ' in result_operator:
                parts = result_operator.split(' ')
                result_operator = f'{parts[0]} q[0], {parts[1]}\n'
            result_operator = 'QASM\n' + U_to_CU(qubits, i - 1, nancillas, result_operator)

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
        }.get(operator, 'Invalid generator: There should be no argument for generator: ' + operator)

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
    }.get(operator, 'Invalid generator: The given generator does not exist: ' + operator)


def matrix_to_operator(matrix, arg=None):
    eye = np.identity(matrix.shape[0])

    if np.isclose(matrix, eye).all():
        return 'I'

    operator = {
        'X': np.array([[0, 1],
                       [1, 0]]),
        'Y': np.array([[0, -1j],
                       [1j, 0]]),
        'Z': np.array([[1, 0],
                       [0, -1]]),
        'H': (1/2**0.5) * np.array([[1, 1],
                                    [1, -1]]),
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
    }

    for key, value in operator.items():
        if matrix.shape == value.shape:
            if np.isclose(matrix, value).all():
                return key

    if arg is not None:
        arg = float(arg)
        operators = {
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
        }

        for key, value in operators.items():
            if np.isclose(matrix, value).all():
                return key + ' ' + str(arg)

        return 'Invalid generator: The given matrix does not require an argument or the matrix is invalid'
    else:
        # No argument is given so we try to find the R gate ourselves
        if matrix.shape == (2, 2):
            # R
            if matrix[0][1] == 0 and matrix[1][0] == 0:
                # Rz
                return 'Rz ' + str(2 * cmath.acos(matrix[0, 0].real).real)
            elif isinstance(matrix[1, 0], complex):
                # Rx
                return 'Rx ' + str(2 * cmath.acos(matrix[0, 0]).real)
            else:
                # Ry
                return 'Ry ' + str(2 * cmath.acos(matrix[0, 0]).real)
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

                        if np.isclose(phi, 0):
                            return 'CR ' + str(phi)

                        k = cmath.log(-(2 * cmath.pi) / phi, 2).real
                        if isinstance(k, int) or k.is_integer():
                            return 'CRk ' + str(int(k))

                        return 'CR ' + str(phi)

            return 'Invalid generator'
        else:
            return 'Invalid generator'
    return 'Something went wrong'


def find_controlled_equivalent(operator, control_bits, qubit, nancillas, qubits):
    controls_string = ', '.join(map(lambda c: f'q[{c}]', control_bits))
    if ' ' in operator:
        sep = operator.split(' ')
        sep.append(',')
    else:
        sep = [operator, '', '']

    result = {
        'X': f'''CNOT {controls_string}, q[{qubit}]\n''',
        'Y': f'''Sdag q[{qubit}]\nCNOT {controls_string}, q[{qubit}]\nS q[{qubit}]\n''',
        'Z': f'''CZ {controls_string}, q[{qubit}]\n''',
        'CX': f'''Toffoli {controls_string}, q[{qubit}]\n''',
        'CY': f'''Sdag q[{qubit}]\nToffoli {controls_string}, q[{qubit}]\nS q[{qubit}]\n''',
        'CZ': f'''H q[{qubit}]\nToffoli {controls_string}, q[{qubit}]\nH q[{qubit}]\n''',
        'CNOT': f'''Toffoli {controls_string}, q[{qubit}]\n'''
    }.get(operator, U_to_CU(qubits, control_bits[0], nancillas, sep[0] + f' q[{qubit}]' + sep[2] + sep[1] + f'\n'))

    if result == 'Invalid generator':
        raise Exception('Operator not supported yet! Operator: ' + operator)

    return result
