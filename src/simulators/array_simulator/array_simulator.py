import numpy as np
import time

from gate import GatesIdentfications
from simulators.simulator import Simulator


class ArraySimulator(Simulator):

    def __init__(self):
        self.state = None
        self.amnt_qubits = None
        self.name = "ArraySimulator"

    def run(self, gates, amnt_qubits=None) -> float:
        start = time.process_time()
        if amnt_qubits is not None:
            self.amnt_qubits = amnt_qubits
            self.state = np.zeros((1, self.amnt_qubits + 2))
            self.state[0, -2] = 1.0
        for gate in gates:
            if gate.gatter == GatesIdentfications.cnot:
                self.execute_cnot(gate.qubits)
            elif gate.gatter == GatesIdentfications.ccnot:
                self.execute_ccnot(gate.qubits)
            elif gate.gatter == GatesIdentfications.paulix:
                self.execute_paulix(gate.qubits)
            elif gate.gatter == GatesIdentfications.pauliy:
                self.execute_pauliy(gate.qubits)
            elif gate.gatter == GatesIdentfications.pauliz:
                self.execute_pauliz(gate.qubits)
            elif gate.gatter == GatesIdentfications.hadamard:
                self.execute_hadamard(gate.qubits)
            elif gate.gatter == GatesIdentfications.reset:
                self.reset_qubits(gate.qubits)
            else:
                print("Unknown Gate Type")
                raise
        self.get_state()
        end = time.process_time()
        return end - start

    def init_state(self, amnt_qubits):
        self.amnt_qubits = amnt_qubits
        self.state = np.zeros((1, self.amnt_qubits + 2))
        self.state[0, -2] = 1.0

    def init_with_state(self, state):
        self.state = np.array(state)

    def aggregate_state(self):
        new_state = []
        i = 0
        while i < self.state.shape[0]:
            new_state.append(self.state[i, :])
            self.state = np.delete(self.state, (i), axis=0)
            j = i
            while j < self.state.shape[0]:
                if list(new_state[-1][:-2]) == list(self.state[j, :-2]):
                    new_state[-1][-2] += self.state[j, -2]
                    new_state[-1][-1] += self.state[j, -1]
                    self.state = np.delete(self.state, (j), axis=0)
                else:
                    j += 1
        self.state = np.array(new_state)
        return

    def get_state(self):
        self.aggregate_state()
        return self.state

    def execute_cnot(self, qubits):
        for i in range(self.state.shape[0]):
            if self.state[i, qubits[0]] == 1:
                self.state[i, qubits[1]] = 1 - self.state[i, qubits[1]]

    def execute_ccnot(self, qubits):
        for i in range(self.state.shape[0]):
            if self.state[i, qubits[0]] == 1 and self.state[i, qubits[1]] == 1:
                self.state[i, qubits[2]] = 1 - self.state[i, qubits[2]]

    def execute_paulix(self, qubits):
        for i in range(self.state.shape[0]):
            self.state[i, qubits[0]] = 1 - self.state[i, qubits[0]]

    def execute_pauliy(self, qubits):
        for i in range(self.state.shape[0]):
            if self.state[i, qubits[0]] == 0:
                tmp = self.state[i, -2]
                self.state[i, -2] = -self.state[i, -1]
                self.state[i, -1] = tmp
            else:
                tmp = self.state[i, -2]
                self.state[i, -2] = self.state[i, -1]
                self.state[i, -1] = -tmp
            self.state[i, qubits[0]] = 1 - self.state[i, qubits[0]]

    def execute_pauliz(self, qubits):
        for i in range(self.state.shape[0]):
            if self.state[i, qubits[0]] == 1:
                self.state[i, -2] *= -1
                self.state[i, -1] *= -1

    def execute_hadamard(self, qubits):
        for i in range(self.state.shape[0]):
            self.state = np.append(self.state, np.array([self.state[i]]), axis=0)
            self.state[-1][qubits[0]] = 1 - self.state[-1][qubits[0]]
            if self.state[i][qubits[0]] == 0:
                self.state[-1][-2] *= np.sqrt(0.5)
                self.state[-1][-1] *= np.sqrt(0.5)
                self.state[i][-2] *= np.sqrt(0.5)
                self.state[i][-1] *= np.sqrt(0.5)
            else:
                self.state[-1][-2] *= np.sqrt(0.5)
                self.state[-1][-1] *= np.sqrt(0.5)
                self.state[i][-2] *= -np.sqrt(0.5)
                self.state[i][-1] *= -np.sqrt(0.5)

    def reset_qubits(self, qubits):
        for q in qubits:
            for i in range(self.state.shape[0]):
                self.state[i, q] = 0


if __name__ == "__main__":
    array = ArraySimulator()
    array.run([], 2)
    print(array.get_state())
    # array.get_state()
