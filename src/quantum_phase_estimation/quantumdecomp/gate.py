import numpy as np

from src.quantum_phase_estimation.quantumdecomp.two_level_unitary import TwoLevelUnitary

""" NUMBER OF ANCILLA BITS"""

class Gate:
    """Represents gate acting on register of qubits."""
    pass


class GateSingle(Gate):
    """Represents gate acting on a single qubit in a register."""

    def __init__(self, gate2, qubit_id, qubit_count):
        self.gate2 = gate2
        self.qubit_id = qubit_id
        self.qubit_count = qubit_count

    def to_qsharp_command(self, nancillas):
        if self.gate2.name in ('Rx', 'Ry', 'Rz'):
            # QSharp uses different sign.
            return '%s(%.15f, q[%d]);' % (
                self.gate2.name, -round(self.gate2.arg, 10), self.qubit_id + nancillas)
        elif self.gate2.name == 'R1':
            return 'R1(%.15f, q[%d]);' % (round(self.gate2.arg, 10), self.qubit_id + nancillas)
        elif self.gate2.name == 'X':
            return 'X q[%d]' % (self.qubit_id + nancillas)

    def to_matrix(self):
        """Tensor product I x I x ... x `gate2.to_matrix()` x I x ... x I."""
        matrix = self.gate2.to_matrix()
        tile_size = 2**(self.qubit_id + 1)
        ts2 = tile_size // 2  # Half tile size.

        if (self.qubit_id == 0):
            tile = matrix
        else:
            tile = np.zeros((tile_size, tile_size), dtype=np.complex128)
            subtile = np.eye(tile_size // 2)
            for i in range(2):
                for j in range(2):
                    tile[i * ts2:(i + 1) * ts2, j *
                         ts2:(j + 1) * ts2] = subtile * matrix[i, j]

        matrix_size = 2 ** self.qubit_count
        ret = np.zeros((matrix_size, matrix_size), dtype=np.complex128)
        for i in range(2**(self.qubit_count - self.qubit_id - 1)):
            ret[i * tile_size:(i + 1) * tile_size,
                i * tile_size:(i + 1) * tile_size] = tile

        return ret

    def __repr__(self):
        return str(self.gate2) + " on bit " + str(self.qubit_id)

    def type(self):
        return self.gate2.name + "-single"


class GateFC(Gate):
    """ Represents fully contolled gate.

    `flip_mask` has ones at positions, for which qubit should be flipped before
    and after applying operation.
    """

    def __init__(self, gate2, qubit_id, qubit_count, flip_mask=0):
        self.gate2 = gate2
        self.qubit_id = qubit_id
        self.flip_mask = flip_mask
        self.qubit_count = qubit_count

    def without_flips(self):
        return GateFC(self.gate2, self.qubit_id, self.qubit_count, flip_mask=0)

    def to_qsharp_command(self, nancillas):
        # On one qubit controlled gate is just single-qubit gate.
        if self.qubit_count == 1:
            return GateSingle(self.gate2, self.qubit_id, 1).to_qsharp_command()

        if self.flip_mask != 0:
            raise ValueError("flip_mask must be zero.")

        control_ids = [
            i for i in range(
                self.qubit_count) if i != self.qubit_id]
        controls = '' + ', '.join(['q[%d]' % (i + nancillas) for i in control_ids]) + ''
        if self.gate2.name in ('Rx', 'Ry', 'Rz'):
            # QSharp uses different sign.
            return 'CNOT q[%d, q[%d] \n%s q[%d], %.15f \nCNOT q[%d, q[%d] \n%s q[%d], %.15f' % (
                control_ids[0], self.qubit_id + nancillas, self.gate2.name, self.qubit_id + nancillas, round(self.gate2.arg, 10), control_ids[0], self.qubit_id + nancillas, self.gate2.name, self.qubit_id + nancillas, -round(self.gate2.arg, 10))

        elif self.gate2.name == 'R1':
            return 'CR %s, q[%d], %.15f' % (
                controls, self.qubit_id + nancillas, round(self.gate2.arg, 10))
        elif self.gate2.name == 'X':
            if self.qubit_count == 2:
                return 'CNOT q[%d], q[%d]' % (
                    control_ids[0] + nancillas, self.qubit_id + nancillas)
            return 'CX %s, q[%d]' % (controls, self.qubit_id + nancillas)

    def to_matrix(self):
        matrix_size = 2**self.qubit_count
        index2 = (matrix_size - 1) - self.flip_mask
        index1 = index2 - 2**self.qubit_id
        matrix = TwoLevelUnitary(
            self.gate2.to_matrix(),
            matrix_size,
            index1,
            index2)
        return matrix.get_full_matrix()

    def __repr__(self):
        return "%s on bit %d, fully controlled" % (
            str(self.gate2), self.qubit_id)

    def type(self):
        return self.gate2.name + "-FC"


def gates_to_matrix(gates):
    """Converts gate sequence to matrix implemented by this sequence."""
    result = np.eye(2 ** gates[0].qubit_count)
    for gate in gates:
        assert isinstance(gate, Gate)
        result = quantum_decomp.gate.to_matrix() @ result
    return result


def apply_on_qubit(gates, qubit_id, qubit_count):
    """Converts Gate2 gates to GateSingle gates acting on the same qubit."""
    return [GateSingle(gate, qubit_id, qubit_count) for gate in gates]
