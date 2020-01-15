import numpy as np

from unittest import TestCase

from src.quantum_phase_estimation.operator.unitary_operators import get_unitary_operators_array


class TestUnitaryOperator(TestCase):

    def test_CRk(self):
        result = get_unitary_operators_array(['CRk', '3'], 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)

    def test_CR(self):
        result = get_unitary_operators_array(['CR', '1.5'], 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)


    def test_X(self):
        result = get_unitary_operators_array('X', 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)


    def test_Y(self):
        result = get_unitary_operators_array('Y', 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)


    def test_Z(self):
        result = get_unitary_operators_array('Z', 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)

    def test_Z_matrix(self):
        result = get_unitary_operators_array(np.array([[1, 0],
                                                       [0, -1]]), 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)

    def test_Z_operator_vs_matrix(self):
        result1 = get_unitary_operators_array(np.array([[1, 0],
                                                       [0, -1]]), 5)

        result2 = get_unitary_operators_array('Z', 5)

        self.assertListEqual(result1, result2)
