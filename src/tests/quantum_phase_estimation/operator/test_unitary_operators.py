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


    def test_CR(self):
        result = get_unitary_operators_array('Y', 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)


    def test_CR(self):
        result = get_unitary_operators_array('Z', 5)

        for res in result:
            self.assertFalse('Invalid operator' in res)
