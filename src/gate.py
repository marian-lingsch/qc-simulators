from enum import IntEnum
from typing import List


class GatesIdentfications(IntEnum):
    hadamard = 1
    cnot = 2
    ccnot = 3
    paulix = 4
    pauliy = 5
    pauliz = 5
    reset = 6
    invert_all_zero = 7
    invert_some_one = 8
    invert_all_one = 9
    diffusion = 10


class Gate:
    def __init__(self, gatter: GatesIdentfications, qubits: List[int]):
        self.qubits = qubits
        self.gatter = gatter

    def __repr__(self):
        return self.gatter.__repr__() + " " + self.qubits.__repr__()
