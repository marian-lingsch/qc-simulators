import unittest

import numpy as np

from simulators.db_simulator_state_drop.db_simulator_state_drop import DBSimulatorStateDrop


class DBSimulatorStateDropTest(unittest.TestCase):

    def test_db_simulator_init(self):
        """
        Test that the DB simulator is initialized correctly
        """

        db_simulator = DBSimulatorStateDrop()

        db_simulator.init_db(100)

        for state in db_simulator.get_state():
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)

    def test_db_init_with_state(self):
        db_simulator = DBSimulatorStateDrop()

        amnt_qubits = 100

        db_simulator.init_db(amnt_qubits)
        state = [([1 for _t in range(amnt_qubits)], 0.5, 0.0), ([0 for _t in range(amnt_qubits)], 0.0, 0.5),
                 ([0] + [1 for _t in range(amnt_qubits - 1)], 0.5, 0.0),
                 ([0, 0] + [1 for _t in range(amnt_qubits - 2)], 0.0, 0.5)]

        db_simulator.init_with_state(state)

        for s in db_simulator.get_state():
            selected_state = -1
            if s[0:3] == (0, 0, 0):
                selected_state = 1
            elif s[0:3] == (1, 1, 1):
                selected_state = 0
            elif s[0:3] == (0, 1, 1):
                selected_state = 2
            elif s[0:3] == (0, 0, 1):
                selected_state = 3
            for i, x in enumerate(s):
                if i < amnt_qubits:
                    self.assertAlmostEqual(x, state[selected_state][0][i], delta=10e-7)
                elif i == amnt_qubits:
                    self.assertAlmostEqual(x, state[selected_state][1], delta=10e-7)
                elif i == amnt_qubits + 1:
                    self.assertAlmostEqual(x, state[selected_state][2], delta=10e-7)

    def test_db_simulator_init_and_destruction(self):
        """
        Test that the DB simulator is initialized and destroyed correctly
        """
        db_simulator = DBSimulatorStateDrop()

        for qubit_amnt in [1, 10, 100, 1000]:
            db_simulator.init_db(qubit_amnt)

            for state in db_simulator.get_state():
                for i, x in enumerate(state):
                    if i == len(state) - 2:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)

            db_simulator.destroy_db()

    def test_db_simulator_cnot_zero(self):
        db_simulator = DBSimulatorStateDrop()

        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_cnot((0, 1))
        for state in db_simulator.get_state():
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_cnot_one(self):
        db_simulator = DBSimulatorStateDrop()

        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_paulix([0])
        db_simulator.execute_cnot((0, 1))
        for state in db_simulator.get_state():
            for i, x in enumerate(state):
                if i in [len(state) - 2, 0, 1]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_cnot_identity(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_cnot((0, 1))
        db_simulator.execute_cnot((0, 1))
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_paulix(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        current_state = [0 for i in range(qubit_amnt + 2)]
        current_state[-2] = 1.0
        for q in [0, 1, 10, 20, 50, 99]:
            db_simulator.execute_paulix([q])
            current_state[q] = 1 - current_state[q]
            for state in db_simulator.get_state():
                for i, x in enumerate(state):
                    self.assertAlmostEqual(x, current_state[i], delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_paulix_identity(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_paulix([0])
        db_simulator.execute_paulix([0])
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_pauliy(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        current_state = [0 for i in range(qubit_amnt + 2)]
        current_state[-2] = 1.0
        for q in [0, 1, 10, 20, 50, 99]:
            db_simulator.execute_pauliy([q])
            temp = current_state[-2]
            current_state[-2] = -current_state[-1]
            current_state[-1] = temp
            current_state[q] = 1 - current_state[q]
            for state in db_simulator.get_state():
                for i, x in enumerate(state):
                    self.assertAlmostEqual(x, current_state[i], delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_pauliy_identity(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_pauliy([0])
        db_simulator.execute_pauliy([0])
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_pauliz(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        current_state = [0 for i in range(qubit_amnt + 2)]
        current_state[-2] = 1.0
        for q in [0, 1, 10, 20, 50, 99]:
            db_simulator.execute_pauliz([q])
            for state in db_simulator.get_state():
                for i, x in enumerate(state):
                    self.assertAlmostEqual(x, current_state[i], delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_pauliz_identity(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_pauliz([0])
        db_simulator.execute_pauliz([0])
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_ccnot(self):
        db_simulator = DBSimulatorStateDrop()

        qubit_amnt = 100
        for t in [[], [0], [1], [0, 1]]:
            db_simulator.init_db(qubit_amnt)
            for q in t:
                db_simulator.execute_paulix([q])
            db_simulator.execute_ccnot((0, 1, 2))
            for state in db_simulator.get_state():
                for i, x in enumerate(state):
                    if i in [len(state) - 2] + t or (t == [0, 1] and i == 2):
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
            db_simulator.destroy_db()

    def test_db_simulator_ccnot_identity(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_ccnot((0, 1, 2))
        db_simulator.execute_ccnot((0, 1, 2))
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_hadamard(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_hadamard([0])
        first_qubits = []
        for j, state in enumerate(db_simulator.get_state()):
            first_qubits.append(state[0])
            for i, x in enumerate(state):
                if i == len(state) - 2:
                    self.assertAlmostEqual(x, np.sqrt(0.5), delta=10e-7)
                elif i != 0:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        self.assertEqual(len(first_qubits), 2)
        first_qubits.sort()
        self.assertEqual(first_qubits[0], 0)
        self.assertEqual(first_qubits[1], 1)
        db_simulator.destroy_db()

    def test_db_simulator_hadamard_identity(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 3
        db_simulator.init_db(qubit_amnt)
        db_simulator.execute_hadamard([0])
        db_simulator.execute_hadamard([0])
        for j, state in enumerate(db_simulator.get_state()):
            if abs(state[-2] - 1.0) < 1e-8:
                for i, x in enumerate(state):
                    if i == len(state) - 2:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
            else:
                for i, x in enumerate(state):
                    if i == 0:
                        self.assertAlmostEqual(x, 1.0, delta=10e-7)
                    else:
                        self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_reset(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.init_with_state([([1 for _t in range(qubit_amnt)], 1.0, 0.0)])
        db_simulator.reset_qubits([0, 1, 2])
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i not in [0, 1, 2, qubit_amnt + 1]:
                    self.assertAlmostEqual(x, 1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()

    def test_db_simulator_invert_zero(self):
        db_simulator = DBSimulatorStateDrop()
        qubit_amnt = 100
        db_simulator.init_db(qubit_amnt)
        db_simulator.invert_all_zero(list(range(qubit_amnt)))
        for j, state in enumerate(db_simulator.get_state()):
            for i, x in enumerate(state):
                if i in [qubit_amnt]:
                    self.assertAlmostEqual(x, -1.0, delta=10e-7)
                else:
                    self.assertAlmostEqual(x, 0.0, delta=10e-7)
        db_simulator.destroy_db()
