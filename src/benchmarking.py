import os
from datetime import datetime
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from circuit import Circuit
from gate import GatesIdentfications, Gate
from simulators.db_simulator.db_simulator import DBSimulator
from simulators.db_simulator_state_drop.db_simulator_state_drop import DBSimulatorStateDrop
from simulators.simulator import Simulator


class Benchmark():
    def __init__(self, iterations: int, output_file: str, algorithms: List[Simulator]):
        self.iterations = iterations
        self.output_file = output_file
        self.algorithms = algorithms
        self.data = []

    def compare_addition(self, max_input_size=5, max_non_det_qubits=0):
        assert 2 * max_input_size >= max_non_det_qubits
        algorithm_times = {
            alg.name: {(3*input_size + 5, non_det_qubits): [-1.0 for _t in range(self.iterations)] for input_size in
                       range(1, max_input_size + 1) for
                       non_det_qubits in range(min(max_non_det_qubits + 1, 2 * input_size + 1))} for alg in
            self.algorithms}
        circuit = Circuit()
        for input_size in range(1, max_input_size + 1):
            for non_det in range(min(max_non_det_qubits + 1, 2 * input_size + 1)):
                circuit.set_addition_circuit(range(input_size), range(input_size, 2 * input_size),
                                             range(2 * input_size, 3 * input_size + 1),
                                             range(3 * input_size + 1, 3 * input_size + 5))
                for h in range(non_det):
                    circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [h]))
                for alg in self.algorithms:
                    for j in range(self.iterations):
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        print("Compare Addition", "Input Size:", input_size, "Nondet: ", non_det, "Algorithm: ",
                              alg.name, "Iteration: ", j, "Timestamp:", dt_string)
                        algorithm_times[alg.name][(3 * input_size + 5, non_det)][j] = alg.run(circuit,
                                                                                              3 * input_size + 5)
                self.data = algorithm_times
                self.write_data()

    def compare_grover_search_min_of_addition_two_numbers(self, max_qubits_per_input_number):
        algorithm_times = {
            alg.name: {(3*input_size + 5, 2*input_size) : [-1.0 for _t in range(self.iterations)] for input_size in
                       range(1, max_qubits_per_input_number + 1)} for alg in
            self.algorithms}
        circuit = Circuit()
        for input_size in range(1, max_qubits_per_input_number + 1):
            circuit.set_addition_circuit(range(input_size), range(input_size, 2 * input_size),
                                         range(2 * input_size, 3 * input_size + 1),
                                         range(3 * input_size + 1, 3 * input_size + 5))
            for h in range(2 * input_size):
                circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [h]))

            # Implement Grovers Algorithm on the result
            # For simplicity the sum is done previously
            for i in range(int(np.sqrt(2 * input_size)) + 1):
                # Make a single Grover iteration
                # Oracle
                circuit.append_gate(Gate(GatesIdentfications.invert_all_zero, range(2 * input_size)))
                # Diffusion Operator
                circuit.append_gate(Gate(GatesIdentfications.diffusion, range(2 * input_size)))

            for alg in self.algorithms:
                for j in range(self.iterations):
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("Compare Grover Min two Numbers", "Input Size:", input_size, "Algorithm: ", alg.name,
                          "Iteration: ", j, "Timestamp:", dt_string)
                    algorithm_times[alg.name][(3 * input_size + 5, 2 * input_size)][j] = alg.run(circuit,
                                                                                                 3 * input_size + 5)
                    self.data = algorithm_times
                    self.write_data()
        return

    def compare_superposition(self, max_size):
        algorithm_times = {
            alg.name: {(input_size, non_det_qubits): [-1.0 for _t in range(self.iterations)] for input_size in
                       range(1, max_size + 1) for
                       non_det_qubits in range(min(max_size + 1, input_size + 1))} for alg in
            self.algorithms}
        for input_size in range(1, max_size + 1):
            for non_det in range(min(max_size + 1, input_size + 1)):
                circuit = Circuit()
                for h in range(non_det):
                    circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [h]))
                for alg in self.algorithms:
                    for j in range(self.iterations):
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        print("Compare Superpostion", "Input Size:", input_size, "Nondet: ", non_det, "Algorithm: ",
                              alg.name, "Iteration: ", j, "Timestamp:", dt_string)
                        algorithm_times[alg.name][(input_size, non_det)][j] = alg.run(circuit, input_size)
                        self.data = algorithm_times
                        self.write_data()

    def write_data(self):
        string = "Algorithm Name, Total Qubits, Nondet Qubits, Times ->\n"
        for alg in self.algorithms:
            for k, v in self.data[alg.name].items():
                string += alg.name + " , " + str(k[0]) + " , " + str(k[1]) + " , " + " , ".join(
                    [str(t) for t in v]) + "\n"
        dir = "/".join(self.output_file.split("/")[:-1])
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(self.output_file, mode="w+") as f:
            f.write(string)
        return


class BenchmarkStateDrop():
    def __init__(self, iterations: int, output_file: str):
        self.iterations = iterations
        self.output_file = output_file
        self.algorithms = [DBSimulatorStateDrop(), DBSimulator()]
        self.data = []

    def benchmark(self, circuit: Circuit):
        return

    def compare_addition(self, max_input_size=5, max_non_det_qubits=0):
        assert 2 * max_input_size >= max_non_det_qubits
        algorithm_times = {(input_size, non_det_qubits): [-1.0 for _t in range(self.iterations)] for input_size in
                           range(1, max_input_size + 1) for
                           non_det_qubits in range(min(max_non_det_qubits + 1, 2 * input_size + 1))}
        circuit = Circuit()
        for input_size in range(1, max_input_size + 1):
            for non_det in range(min(max_non_det_qubits + 1, 2 * input_size + 1)):
                circuit.set_addition_circuit(range(input_size), range(input_size, 2 * input_size),
                                             range(2 * input_size, 3 * input_size + 1),
                                             range(3 * input_size + 1, 3 * input_size + 5))
                for h in range(non_det):
                    circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [h]))
                for j in range(self.iterations):
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("Compare Addition", "Input Size:", input_size, "Nondet: ", non_det, "Iteration: ", j,
                          "Timestamp:", dt_string)
                    algorithm_times[(input_size, non_det)][j] = (self.algorithms[0].run(circuit, 3 * input_size + 5),
                                                                 self.algorithms[1].run(circuit, 3 * input_size + 5),
                                                                 self.calculate_error(self.algorithms[0].get_state(),
                                                                                      self.algorithms[1].get_state()))
                self.data = algorithm_times
                self.write_data_addition()

    def write_data_addition(self):
        string = "Input Size, Nondet Qubits, Total Qubits, (State Drop Time, Normal DB Time, Error between the two)\n"
        for k, v in self.data.items():
            string += str(k[0]) + " , " + str(k[1]) + " , " + str(3 * k[0] + 5) + " , " + " , ".join(
                [str(t) for t in v]) + "\n"
        dir = "/".join(self.output_file.split("/")[:-1])
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(self.output_file, mode="w+") as f:
            f.write(string)
        return

    def compare_grover_search_min_of_addition_two_numbers(self, max_qubits_per_input_number):
        """
        We suppose a full range of addition
        :return:
        """
        algorithm_times = {input_size: [-1.0 for _t in range(self.iterations)] for input_size in
                           range(1, max_qubits_per_input_number + 1)}
        circuit = Circuit()
        for input_size in range(1, max_qubits_per_input_number + 1):
            circuit.set_addition_circuit(range(input_size), range(input_size, 2 * input_size),
                                         range(2 * input_size, 3 * input_size + 1),
                                         range(3 * input_size + 1, 3 * input_size + 5))
            for h in range(2 * input_size):
                circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [h]))

            # Implement Grovers Algorithm on the result
            # For simplicity the sum is done previously
            for i in range(int(np.sqrt(2 * input_size)) + 1):
                # Make a single Grover iteration
                # Oracle
                circuit.append_gate(Gate(GatesIdentfications.invert_all_zero, range(2 * input_size)))
                # Diffusion Operator
                circuit.append_gate(Gate(GatesIdentfications.diffusion, range(2 * input_size)))

            for j in range(self.iterations):
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print("Compare Grover Min two Numbers", "Input Size:", input_size, "Iteration: ", j, "Timestamp:",
                      dt_string)
                algorithm_times[input_size][j] = (self.algorithms[0].run(circuit, 3 * input_size + 5),
                                                  self.algorithms[1].run(circuit, 3 * input_size + 5),
                                                  self.calculate_error(self.algorithms[0].get_state(),
                                                                       self.algorithms[1].get_state()))
                self.data = algorithm_times
                self.write_data_grover_addition()

        return

    def write_data_grover_addition(self):
        string = "Input Size, Nondet Qubits, Total Qubits, (State Drop Time, Normal DB Time, Error between the two) ->\n"
        for k, v in self.data.items():
            string += str(k) + " , " + str(2 * k) + " , " + str(3 * k + 5) + " , " + " , ".join(
                [str(t) for t in v]) + "\n"
        dir = "/".join(self.output_file.split("/")[:-1])
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(self.output_file, mode="w+") as f:
            f.write(string)
        return

    def compare_superposition(self, max_size):
        algorithm_times = {(input_size, non_det_qubits): [-1.0 for _t in range(self.iterations)] for input_size in
                           range(1, max_size + 1) for
                           non_det_qubits in range(min(max_size + 1, input_size + 1))}
        for input_size in range(1, max_size + 1):
            for non_det in range(min(max_size + 1, input_size + 1)):
                circuit = Circuit()
                for h in range(non_det):
                    circuit.prepend_gate(Gate(GatesIdentfications.hadamard, [h]))
                for j in range(self.iterations):
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("Compare Superpostion", "Input Size:", input_size, "Nondet: ", non_det, "Iteration: ", j,
                          "Timestamp:", dt_string)
                    algorithm_times[(input_size, non_det)][j] = (self.algorithms[0].run(circuit, input_size),
                                                                 self.algorithms[1].run(circuit, input_size),
                                                                 self.calculate_error(self.algorithms[0].get_state(),
                                                                                      self.algorithms[1].get_state()))
                    self.data = algorithm_times
                    self.write_data_superposition()

    def write_data_superposition(self):
        string = "Input Size, Nondet Qubits, Total Qubits, (State Drop Time, Normal DB Time, Error between the two)\n"
        for k, v in self.data.items():
            string += str(k[0]) + " , " + str(k[1]) + " , " + str(k[0]) + " , " + " , ".join([str(t) for t in v]) + "\n"
        dir = "/".join(self.output_file.split("/")[:-1])
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(self.output_file, mode="w+") as f:
            f.write(string)
        return

    def plot_data_addition(self, max_input_size, max_non_det_qubits):
        # TODO: 3D Plot generieren pro Simulator + Delta der zeit zwischen simulatoren und Farben pro Höhe machen
        fig, ax = plt.subplots()
        for alg in self.algorithms:
            for j in range(max_non_det_qubits + 1):
                x_axis = []
                y_axis = []
                for i in range(1, max_input_size + 1):
                    x_axis.append(i)
                    avg = sum(self.data[alg.name][(i, j)]) / len(self.data[alg.name][(i, j)])
                    y_axis.append(avg)
                ax.plot(x_axis, y_axis, label=alg.name + ": nondet qubits " + str(j))

        ax.set(xlabel='Amount Input Qubits', ylabel='Time',
               title='')
        ax.grid()
        dir = "/".join(self.output_file.split("/")[:-1])
        if not os.path.isdir(dir):
            os.makedirs(dir)
        fig.legend()
        fig.savefig(dir + "/graph.png")
        return

    def calculate_error(self, result_state_drop, result_db):
        """
        The error is calculated as the euclidian distance between the state drop result and the db result.
        To calculate this distance somewhat quicker a dictionary is used. This is possible since very state in the state dropped result is also a state in the Database result.
        """
        assert len(result_state_drop) <= len(result_db)

        hash_lookup_state_drop = {}
        for elem in result_state_drop:
            hash_lookup_state_drop[elem[0:-2]] = (elem[-2], elem[-1])

        error = 0.0
        for elem in result_db:
            re, im = 0.0, 0.0
            if elem[0:-2] in hash_lookup_state_drop:
                re, im = hash_lookup_state_drop[elem[0:-2]]
            error += (elem[-2] - re) ** 2 + (elem[-1] - im) ** 2

        error = np.sqrt(error)
        return error
