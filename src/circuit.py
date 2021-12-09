from typing import List

from gate import Gate, GatesIdentfications


class Circuit:
    def __init__(self):
        self.gates: List[Gate] = []

    def __iter__(self):
        return self.gates.__iter__()

    def set_addition_circuit(self, input_qubits1: List[int], input_qubits2: List[int], output_qubits: List[int],
                             ancilliary_qubits: List[int]):
        assert max(len(input_qubits1), len(input_qubits2)) < len(output_qubits)
        assert len(input_qubits1) == len(input_qubits2)
        assert len(ancilliary_qubits) == 4  # Can be compressed because of the reset Gate

        gates = []

        for i in range(len(input_qubits1)):
            if i == 0:
                gates.append(Gate(GatesIdentfications.cnot, [input_qubits1[i], output_qubits[i]]))
                gates.append(Gate(GatesIdentfications.cnot, [input_qubits2[i], output_qubits[i]]))
                gates.append(
                    Gate(GatesIdentfications.ccnot, [input_qubits1[i], input_qubits2[i], ancilliary_qubits[0]]))
            else:
                gates.append(Gate(GatesIdentfications.cnot, [input_qubits1[i], output_qubits[i]]))
                gates.append(Gate(GatesIdentfications.cnot, [input_qubits2[i], output_qubits[i]]))
                gates.append(
                    Gate(GatesIdentfications.ccnot, [output_qubits[i], ancilliary_qubits[0], ancilliary_qubits[1]]))
                gates.append(
                    Gate(GatesIdentfications.ccnot, [input_qubits1[i], input_qubits2[i], ancilliary_qubits[2]]))
                # Or Gate
                gates.append(Gate(GatesIdentfications.cnot, [ancilliary_qubits[1], ancilliary_qubits[3]]))
                gates.append(Gate(GatesIdentfications.cnot, [ancilliary_qubits[2], ancilliary_qubits[3]]))
                gates.append(
                    Gate(GatesIdentfications.ccnot, [ancilliary_qubits[1], ancilliary_qubits[2], ancilliary_qubits[3]]))
                # Reset ancilliary qubits
                gates.append(
                    Gate(GatesIdentfications.ccnot, [output_qubits[i], ancilliary_qubits[0], ancilliary_qubits[1]]))
                gates.append(
                    Gate(GatesIdentfications.ccnot, [input_qubits1[i], input_qubits2[i], ancilliary_qubits[2]]))
                # Finish calculating value
                gates.append(Gate(GatesIdentfications.cnot, [ancilliary_qubits[0], output_qubits[i]]))
                # Swap
                gates.append(Gate(GatesIdentfications.cnot, [ancilliary_qubits[0], ancilliary_qubits[3]]))
                gates.append(Gate(GatesIdentfications.cnot, [ancilliary_qubits[3], ancilliary_qubits[0]]))
                gates.append(Gate(GatesIdentfications.cnot, [ancilliary_qubits[0], ancilliary_qubits[3]]))
                # Reset previous Overflow using a reset gate to not use a lot of ancilliary qubits
                gates.append(Gate(GatesIdentfications.reset, [ancilliary_qubits[3]]))
        gates.append(Gate(GatesIdentfications.reset, [ancilliary_qubits[0]]))

        self.gates = gates

    def set_paulix(self, qubit):
        self.gates = [Gate(GatesIdentfications.paulix, [qubit])]

    def prepend_gate(self, gate):
        self.gates = [gate] + self.gates

    def append_gate(self, gate):
        self.gates.append(gate)

    def get_required_qubits(self):
        qubits = set([])
        for g in self.gates:
            qubits = qubits.union(set(g.qubits))
        if qubits == set([]):
            return 1
        return max(qubits)
