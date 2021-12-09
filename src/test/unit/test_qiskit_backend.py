import unittest

import numpy as np

from circuit import Circuit
from gate import Gate, GatesIdentfications
from simulators.qiskit.qiskit_simulator import QiskitSimulator


class QiskitSimulatorTest(unittest.TestCase):

    def test_qiskit_simulator_paulix(self):
        qiskit_simulator = QiskitSimulator()
        circuit = Circuit()
        circuit.set_paulix(0)

        qiskit_simulator.run(circuit, 2)

        state = qiskit_simulator.get_state()
        for i, x in enumerate(state):
            if i == 1:
                self.assertAlmostEqual(x, 1.0, 1e-7)
            else:
                self.assertAlmostEqual(x, 0.0, 1e-7)

    def test_qiskit_simulator_hadamard(self):
        qiskit_simulator = QiskitSimulator()
        circuit = Circuit()
        circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [0]))

        qiskit_simulator.run(circuit, 2)

        state = qiskit_simulator.get_state()
        for i, x in enumerate(state):
            if i in [0, 1]:
                self.assertAlmostEqual(x, np.sqrt(0.5))
            else:
                self.assertAlmostEqual(x, 0.0)
