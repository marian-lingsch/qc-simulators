from enum import Enum

from gate import GatesIdentfications


class HeuristicsEnumeration(Enum):
    basic_state_calculation_heuristic = 0


class Heuristics():
    def calculate_states(self, circuit, state_calculation_heuristic):
        if state_calculation_heuristic == HeuristicsEnumeration.basic_state_calculation_heuristic:
            return self.basic_state_calculation_heuristic(circuit)

    def basic_state_calculation_heuristic(self, circuit):
        states_approximation = 0
        for g in circuit:
            # This can be replaced with a more complex algorithm based on the amount of states a Gatter Produces
            # Which is the amount of columns it has, and mark every qubit which goes into a superposition
            # To calculate
            if g.gatter == GatesIdentfications.hadamard:
                states_approximation += 1
        return states_approximation
