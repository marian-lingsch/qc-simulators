from benchmarking import Benchmark, BenchmarkStateDrop
from circuit import Circuit
from simulators.array_simulator.array_simulator import ArraySimulator
from simulators.db_simulator.db_simulator import DBSimulator
from simulators.db_simulator_state_drop.db_simulator_state_drop import DBSimulatorStateDrop
from simulators.mixed_simulator.mixed_simulator import MixedSimulator
from simulators.qiskit.qiskit_simulator import QiskitSimulator

if __name__ == "__main__":
    # Constants for benchmarking
    benchmarking = True
    benchmark_type = "StateDrop"
    output_dir_state_drop = "output-state-drop/"
    output_dir_almost_all = "output-almost-all/"
    iterations = 10
    algorithms = [DBSimulator(), QiskitSimulator(), ArraySimulator(), MixedSimulator()]
    max_qubits_superposition = 20
    max_variable_size_addition = 10
    max_nondet_qubits_addition = 2 * max_variable_size_addition
    max_variable_size_grover = 10

    # Constant for executing a single Simulator for the circuit
    circuit = Circuit()
    chosen_simulator = "Qiskit"

    if benchmarking:
        print("Benchmarking algorithms")
        if benchmark_type == "StateDrop":
            print("Benchmarking the database simulator and the state drop database simulator")

            print("Benchmarking Superposition")
            BenchmarkStateDrop(iterations, output_dir_state_drop + "superposition.csv").compare_superposition(
                max_qubits_superposition)

            print("Benchmarking Addition")
            BenchmarkStateDrop(iterations, output_dir_state_drop + "addition.csv").compare_addition(
                max_variable_size_addition,
                max_nondet_qubits_addition)
            print("Benchmarking Grover")
            BenchmarkStateDrop(iterations,
                               output_dir_state_drop + "grover.csv").compare_grover_search_min_of_addition_two_numbers(
                max_variable_size_grover)

        elif benchmark_type == "AlmostAll":
            print("Benchmarking all simulators except the state drop simulator")

            print("Benchmarking Superposition")
            Benchmark(iterations, output_dir_almost_all + "superposition.csv", algorithms).compare_superposition(
                max_qubits_superposition)

            print("Benchmarking Addition")
            algorithms = [DBSimulator(), QiskitSimulator(), MixedSimulator()]
            Benchmark(iterations, output_dir_almost_all + "addition.csv", algorithms).compare_addition(
                max_variable_size_addition,
                max_nondet_qubits_addition)

            print("Benchmarking Grover")
            algorithms = [DBSimulator(), QiskitSimulator(), MixedSimulator()]
            Benchmark(iterations, output_dir_almost_all + "grover.csv",
                      algorithms).compare_grover_search_min_of_addition_two_numbers(max_variable_size_grover)
        else:
            print("There is no known benchmark for: " + benchmark_type)
    else:
        if chosen_simulator == "Qiskit":
            print("Using the qiskit simulator")
            print("Time taken for this circuit: " + str(QiskitSimulator().run(circuit, circuit.get_required_qubits())))
        elif chosen_simulator == "Database":
            print("Using the database simulator")
            print("Time taken for this circuit: " + str(DBSimulator().run(circuit, circuit.get_required_qubits())))
        elif chosen_simulator == "DatabaseStateDrop":
            print("Using the database simulator")
            print("Time taken for this circuit: " +
                  str(DBSimulatorStateDrop().run(circuit, circuit.get_required_qubits())))
        elif chosen_simulator == "Array":
            print("Using the array simulator")
            print("Time taken for this circuit: " + str(ArraySimulator().run(circuit, circuit.get_required_qubits())))
        elif chosen_simulator == "Mixed":
            print("Using the mixed simulator")
            print("Time taken for this circuit: " + str(MixedSimulator().run(circuit, circuit.get_required_qubits())))
        else:
            print("No valid simulator found for: " + chosen_simulator)
