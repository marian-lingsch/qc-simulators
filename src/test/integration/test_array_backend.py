import unittest

import numpy as np

from circuit import Circuit
from simulators.array_simulator.array_simulator import ArraySimulator


class ArraySimulatorTest(unittest.TestCase):

    def test_array_simulator_addition_zero(self):

        array_simulator = ArraySimulator()

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_one_left(self):
        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[1] + [0] * (amnt_qubits - 1) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)
        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [0, 10, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_one_right(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[0] * 5 + [1] + [0] * (amnt_qubits - 6) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)
        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [5, 10, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_one_both(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[1] + [0] * 4 + [1] + [0] * (amnt_qubits - 6) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)
        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [0, 5, 11, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_two_both(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[0, 1] + [0] * 3 + [0, 1] + [0] * (amnt_qubits - 7) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [1, 6, 12, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_three_both(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[1, 1] + [0] * 3 + [1, 1] + [0] * (amnt_qubits - 7) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [0, 1, 5, 6, 11, 12, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_five_both(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[1, 0, 1] + [0] * 2 + [1, 0, 1] + [0] * (amnt_qubits - 8) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [0, 2, 5, 7, 11, 13, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_seven_both(self):
        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        initial_state = [[1, 1, 1] + [0] * 2 + [1, 1, 1] + [0] * (amnt_qubits - 8) + [1.0, 0.0]]
        array_simulator.init_with_state(initial_state)
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if i in [0, 1, 2, 5, 6, 7, 11, 12, 13, amnt_qubits]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_hadamard_first(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        array_simulator.execute_hadamard([0])
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if state[0] == 0:
                    if i in [amnt_qubits]:
                        self.assertAlmostEqual(x, np.sqrt(0.5), delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif state[0] == 1:
                    if i in [0, 10]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, np.sqrt(0.5), delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_array_simulator_addition_hadamard_first_two(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        array_simulator.execute_hadamard([0])
        array_simulator.execute_hadamard([1])
        array_simulator.run(circuit)

        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if list(state[0:2]) == [0, 0]:
                    if i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif list(state[0:2]) == [1, 0]:
                    if i in [0, 10]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif list(state[0:2]) == [0, 1]:
                    if i in [1, 11]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif list(state[0:2]) == [1, 1]:
                    if i in [0, 1, 10, 11]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                else:
                    self.assertEqual(0, 1)

    def test_array_simulator_addition_hadamard_first_left_and_right(self):

        array_simulator = ArraySimulator()
        amnt_qubits = 100

        array_simulator.init_state(100)
        circuit = Circuit()
        circuit.set_addition_circuit([0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18, 19])

        array_simulator.execute_hadamard([0])
        array_simulator.execute_hadamard([5])
        array_simulator.run(circuit)
        for state in array_simulator.get_state():
            for i, x in enumerate(state):
                if [state[0], state[5]] == [0, 0]:
                    if i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif [state[0], state[5]] == [1, 0]:
                    if i in [0, 10]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif [state[0], state[5]] == [0, 1]:
                    if i in [5, 10]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                elif [state[0], state[5]] == [1, 1]:
                    if i in [0, 5, 11]:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    elif i in [amnt_qubits]:
                        self.assertAlmostEqual(x, 0.5, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
                else:
                    self.assertEqual(0, 1)
