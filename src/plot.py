import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter


def plot_3D(file_name):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Load data
    algorithms = {}
    with open(file_name, mode="r") as f:
        data_string = f.read()
        data_string = data_string.split("\n")
        for s in data_string[1:]:
            splitted_line = s.split(",")
            total_times = [float(splitted_line[i].replace(" ", "")) for i in range(3, len(splitted_line)) if
                           abs(float(splitted_line[i].replace(" ", "")) + 1.0) > 1e-4]
            if len(total_times) != 0:
                algorithm_name = splitted_line[0].replace(" ", "")
                if algorithm_name not in algorithms:
                    algorithms[algorithm_name] = ([], [], [])
                x = int(splitted_line[1].replace(" ", ""))
                y = int(splitted_line[2].replace(" ", ""))
                z = np.log(sum(total_times) / len(total_times))
                algorithms[algorithm_name][0].append(x)
                algorithms[algorithm_name][1].append(y)
                algorithms[algorithm_name][2].append(z)

    for k, v in algorithms.items():
        # Plot the surface.
        surf = ax.plot_trisurf(v[0], v[1], v[2], linewidth=0.2, antialiased=True, label=k)
        # See: https://stackoverflow.com/questions/54994600/pyplot-legend-poly3dcollection-object-has-no-attribute-edgecolors2d
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        ax.legend()

    # Customize the z axis.
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    ax.set_xlabel('Total Qubits')
    ax.set_ylabel('Nondet Qubits')
    ax.set_zlabel('Logarithm of Time taken')

    plt.show()


def plot_line(file_name):
    fig = plt.figure()
    ax = fig.gca()
    # Load data
    algorithms = {}
    with open(file_name, mode="r") as f:
        data_string = f.read()
        data_string = data_string.split("\n")
        for s in data_string[1:]:
            splitted_line = s.split(",")
            total_times = [float(splitted_line[i].replace(" ", "")) for i in range(3, len(splitted_line)) if
                           abs(float(splitted_line[i].replace(" ", "")) + 1.0) > 1e-4]
            if len(total_times) != 0:
                algorithm_name = splitted_line[0].replace(" ", "")
                if algorithm_name not in algorithms:
                    algorithms[algorithm_name] = ([], [])
                x = int(splitted_line[2].replace(" ", ""))
                y = np.log(sum(total_times) / len(total_times))
                algorithms[algorithm_name][0].append(x)
                algorithms[algorithm_name][1].append(y)
    for k, v in algorithms.items():
        ax.plot(v[0], v[1], label=k)

    ax.legend()
    ax.set_xlabel('Total Qubits')
    ax.set_ylabel('Logarithm of Time taken')

    plt.show()


def states_drop_parsing(input_file):
    data = None
    with open(input_file, mode="r") as f:
        data = f.read()

    # (nondet_qubits, total_qubits) = (avg_runtime_state_drop, avg_runtime_db, avg_error)
    processed_data = {}

    for line in data.split("\n"):
        if line == "" or "-1.0" in line or "Nondet Qubits" in line:
            continue
        else:
            runtimes_state_drop_simulator = []
            runtimes_db_simulator = []
            errors = []
            line = line.replace(" ", "")
            nondet_qubits = int(line.split(",")[1])
            total_qubits = int(line.split(",")[2])
            tuples_as_string = map(lambda x: x.split("(")[-1], line.split(")"))
            for tuple_string in tuples_as_string:
                if tuple_string == "":
                    continue
                runtime_state_drop, runtime_db, error = map(lambda y: float(y.replace(" ", "")),
                                                            tuple_string.split(","))
                runtimes_state_drop_simulator.append(runtime_state_drop)
                runtimes_db_simulator.append(runtime_db)
                errors.append(error)
            processed_data[(nondet_qubits, total_qubits)] = (
                np.average(runtimes_state_drop_simulator), np.average(runtimes_db_simulator), np.average(errors))

    return processed_data


def plot_states_drop(input_file):
    processed_data = states_drop_parsing(input_file)

    # Define Data
    nondet_qubits = []
    runtime_db = []
    runtime_state_drop = []
    errors = []

    max_qubits = max([k[1] for k in processed_data.keys()])
    duplicates = len([k[0] for k in processed_data.keys()]) != len(set([k[0] for k in processed_data.keys()]))

    for k, v in processed_data.items():
        if max_qubits == k[1] or not duplicates:
            nondet_qubits.append(k[0])
            runtime_db.append(np.log(v[1]))
            runtime_state_drop.append(np.log(v[0]))
            errors.append(v[2])

    print(nondet_qubits)
    print(runtime_db)

    # Plot Graph

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Nondet qubits')
    ax1.set_ylabel('Logarithmic runtime (s)')
    lns1 = ax1.plot(nondet_qubits, runtime_db, label='DB simulator')
    lns2 = ax1.plot(nondet_qubits, runtime_state_drop, label='State drop DB simulator')
    # ax1.legend()
    # ax1.tick_params(axis='y')

    # Twin Axes

    ax2 = ax1.twinx()

    ax2.set_ylabel('Average error')
    lns3 = ax2.plot(nondet_qubits, errors, label='Error between results-for-3d-plots', color="red")
    # ax2.tick_params(axis='y', labelcolor='blue')
    # Display
    # ax2.legend()

    # added these three lines
    lns = lns1 + lns2 + lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)

    plt.show()


if __name__ == "__main__":
    # plot_3D("./output-almost-all/addition.csv")
    # plot_line("./output-almost-all/grover.csv")
    plot_states_drop("./output-state-drop/superposition.csv")
