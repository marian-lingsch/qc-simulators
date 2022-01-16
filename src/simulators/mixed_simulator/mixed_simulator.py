from simulators.db_simulator.db_simulator import DBSimulator
from simulators.mixed_simulator.heuristics import Heuristics, HeuristicsEnumeration
from simulators.qiskit.qiskit_simulator import QiskitSimulator
from simulators.simulator import Simulator


class MixedSimulator(Simulator):
    def __init__(self):
        self.db_simulator = DBSimulator()
        self.qiskit_simulator = QiskitSimulator()
        self.heuristics = Heuristics()
        self.state = None
        self.name = "MixedSimulator"

    def run(self, gates, amnt_qubits,
            state_calculation_heuristic=HeuristicsEnumeration.basic_state_calculation_heuristic) -> float:
        states_approximation = self.heuristics.calculate_states(gates, state_calculation_heuristic)

        time = 0.0
        if 0.7 * amnt_qubits > states_approximation:
            time += self.db_simulator.run(gates, amnt_qubits)
            self.state = self.db_simulator.get_state()
        else:
            time += self.qiskit_simulator.run(gates, amnt_qubits)
            self.state = self.qiskit_simulator.get_state()
        return time

    def get_state(self):
        return self.state
