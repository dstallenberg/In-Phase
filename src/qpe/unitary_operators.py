import numpy as np

def get_unitary_operators_array(operator, nancillas):
    # TODO remove hard coded operator Z
    operator = 'Z'

    matrix = operator_to_matrix(operator)

    array = []
    for i in range(1, nancillas + 1):
        power = 2**(nancillas - i)

        result_matrix = matrix
        for j in range(power - 1):
            result_matrix = np.dot(matrix, result_matrix)

        array.append(matrix_to_operator(result_matrix))


    return array

def operator_to_matrix(operator):
    return {
        'Z': [[1, 0], [0, -1]],
        'I': [[1, 0], [0, 1]]
    }.get(operator, 'Invalid operator')


def matrix_to_operator(matrix):
    # convert matrix to tuple to be able to hash it
    tuple_matrix = tuple(map(tuple, matrix))
    hash_of_matrix = hash(tuple_matrix)

    return {
        hash(((1, 0), (0, -1))): 'Z',
        hash(((1, 0), (0, 1))): 'I'
    }.get(hash_of_matrix, 'Invalid operator')

def transform_controlled_unitary_to_toffoli(operator, controls, qubit):
    result = ''
    if operator == 'Z':
        result += f'H q[{qubit}]\n'
        controls_string = ', '.join(map(lambda c: f'q[{c}]', controls))
        result += f'Toffoli {controls_string}, q[{qubit}]\n'
        result += f'H q[{qubit}]\n'
    else:
        raise Exception('Operator not supported yet!')

    return result

