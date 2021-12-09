import unittest

import numpy as np

from circuit import Circuit
from gate import Gate, GatesIdentfications
from simulators.qiskit.qiskit_simulator import QiskitSimulator


class QiskitSimulatorTest(unittest.TestCase):

    def test_db_simulator_addition_zero(self):
        """
        Test that the DB simulator is initialized correctly
        """

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1], [2, 3], [4, 5, 6], [7, 8, 9, 10])
        simulator_simulator.run(circuit, 11)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 0:
                self.assertAlmostEqual(x, 1.0, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_one_left(self):
        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1], [2, 3], [4, 5, 6], [7, 8, 9, 10])
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [0]))
        simulator_simulator.run(circuit, 11)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 17:  # 17 = 2**4 + 2**0
                self.assertAlmostEqual(x, 1.0, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_one_right(self):

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1], [2, 3], [4, 5, 6], [7, 8, 9, 10])
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [2]))
        simulator_simulator.run(circuit, 11)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 20:  # 24 = 2**4 + 2**2
                self.assertAlmostEqual(x, 1.0, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_one_both(self):

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1], [2, 3], [4, 5, 6], [7, 8, 9, 10])
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [2]))
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [0]))
        simulator_simulator.run(circuit, 11)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 37:  # 37 = 2**5 + 2**2 + 2**0
                self.assertAlmostEqual(x, 1.0, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_two_both(self):

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2], [3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13])
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [1]))
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [4]))
        simulator_simulator.run(circuit, 14)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 274:  # = 2**8 + 2**4 + 2**1
                self.assertAlmostEqual(x, 1.0, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_three_both(self):

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2], [3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13])
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [0]))
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [1]))
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [3]))
        circuit.prepend_gate(Gate(GatesIdentfications.paulix, [4]))
        simulator_simulator.run(circuit, 14)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 411:  # = 2**8 + 2**7 + 2**4 + 2**3 + 2**1 + 2**0
                self.assertAlmostEqual(x, 1.0, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_hadamard_first(self):

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1], [2, 3], [4, 5, 6], [7, 8, 9, 10])
        circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [0]))
        simulator_simulator.run(circuit, 11)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i == 17:  # 17 = 2**4 + 2**0
                self.assertAlmostEqual(x, np.sqrt(0.5), delta=10e-7)
            elif i == 0:  # = 0
                self.assertAlmostEqual(x, np.sqrt(0.5), delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_simulator_addition_hadamard_first_two(self):

        simulator_simulator = QiskitSimulator()

        circuit = Circuit()
        circuit.set_addition_circuit([0, 1], [2, 3], [4, 5, 6], [7, 8, 9, 10])
        circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [0]))
        circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [1]))
        simulator_simulator.run(circuit, 11)

        for i, x in enumerate(simulator_simulator.get_state()):
            if i in [0, 17, 34, 51]:
                self.assertAlmostEqual(x, 0.5, delta=10e-7)
            else:
                self.assertAlmostEqual(x, 0.0, delta=10e-7)
