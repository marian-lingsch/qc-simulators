import warnings

import time
from qiskit import QuantumCircuit, Aer

from gate import GatesIdentfications
from simulators.simulator import Simulator


class QiskitSimulator(Simulator):
    def __init__(self):
        self.qc = None
        self.amnt_qubits = None
        self.state = []
        self.name = "QiskitSimulator"
        # To ignore Pending Deprecation Warning for the simulator
        warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
        self.simulator = Aer.get_backend('statevector_simulator')

    def run(self, gates, amnt_qubits=None) -> float:
        start = time.process_time()
        if amnt_qubits is not None:
            self.init_network(amnt_qubits)
        for gate in gates:
            if gate.gatter == GatesIdentfications.cnot:
                self.qc.cx(*gate.qubits)
            elif gate.gatter == GatesIdentfications.ccnot:
                self.qc.ccx(*gate.qubits)
            elif gate.gatter == GatesIdentfications.paulix:
                self.qc.x(*gate.qubits)
            elif gate.gatter == GatesIdentfications.pauliy:
                self.qc.y(*gate.qubits)
            elif gate.gatter == GatesIdentfications.pauliz:
                self.qc.z(*gate.qubits)
            elif gate.gatter == GatesIdentfications.hadamard:
                self.qc.h(*gate.qubits)
            elif gate.gatter == GatesIdentfications.reset:
                self.qc.reset(*gate.qubits)
            elif gate.gatter == GatesIdentfications.invert_all_one:
                self.qc.h(gate.qubits[0])
                self.qc.mct(list(gate.qubits[1:]), gate.qubits[0])
                self.qc.h(gate.qubits[0])
            elif gate.gatter == GatesIdentfications.invert_all_zero:
                for q in gate.qubits:
                    self.qc.x(q)
                self.qc.h(gate.qubits[0])
                self.qc.mct(list(gate.qubits[1:]), gate.qubits[0])
                self.qc.h(gate.qubits[0])
                for q in gate.qubits:
                    self.qc.x(q)
            elif gate.gatter == GatesIdentfications.diffusion:
                for h in gate.qubits:
                    self.qc.h(h)

                # Invert all zero
                for q in gate.qubits:
                    self.qc.x(q)
                self.qc.h(gate.qubits[0])
                self.qc.mct(list(gate.qubits[1:]), gate.qubits[0])
                self.qc.h(gate.qubits[0])
                for q in gate.qubits:
                    self.qc.x(q)

                for h in gate.qubits:
                    self.qc.h(h)
            else:
                print("Unknown Gate Type")
                raise
        self.state = self.simulator.run(self.qc).result().get_statevector()
        end = time.process_time()
        return end - start

    def init_with_state(self, amnt_qubits, state):
        self.init_network(amnt_qubits)
        self.qc.initialize(state)

    def init_network(self, amnt_qubits):
        self.qc = QuantumCircuit(amnt_qubits)
        self.amnt_qubits = amnt_qubits

    def get_state(self):
        return self.state
