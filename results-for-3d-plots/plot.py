import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter


def plot(file_names):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Load data
    # x = Total Qubits
    # y = Nondet qubits
    # z = average time
    for file_name in file_names:
        x, y, z = [], [], []
        with open(file_name, mode="r") as f:
            data_string = f.read()
            data_string = data_string.split("\n")
            for s in data_string[1:]:
                splitted_line = s.split(",")
                total_times = [float(splitted_line[i].replace(" ", "")) for i in range(4, len(splitted_line)) if
                               abs(float(splitted_line[i].replace(" ", "")) + 1.0) > 1e-4]
                if len(total_times) != 0:
                    if "addition" in file_name:
                        x.append(3 * int(splitted_line[1].replace(" ", "")) + 5)
                    else:
                        x.append(int(splitted_line[1].replace(" ", "")))
                    y.append(int(splitted_line[2].replace(" ", "")))
                    z.append(np.log(sum(total_times) / len(total_times)))
        # Plot the surface.
        surf = ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True, label=file_name.split("/")[-1].split("-")[0])
        # See: https://stackoverflow.com/questions/54994600/pyplot-legend-poly3dcollection-object-has-no-attribute-edgecolors2d
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        ax.legend()

    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    ax.set_xlabel('Total Qubits')
    ax.set_ylabel('Nondet Qubits')
    ax.set_zlabel('Logarithm of Time taken')

    plt.show()


def plot_line(file_names):
    fig = plt.figure()
    ax = fig.gca()
    # Load data
    # x = Total Qubits
    # y = average time
    for file_name in file_names:
        x, y = [], []
        with open(file_name, mode="r") as f:
            data_string = f.read()
            data_string = data_string.split("\n")
            for s in data_string[1:]:
                splitted_line = s.split(",")
                total_times = [float(splitted_line[i].replace(" ", "")) for i in range(4, len(splitted_line)) if
                               abs(float(splitted_line[i].replace(" ", "")) + 1.0) > 1e-4]
                if len(total_times) != 0:
                    if "addition" in file_name:
                        x.append(3 * int(splitted_line[1].replace(" ", "")) + 5)
                    else:
                        x.append(int(splitted_line[1].replace(" ", "")))
                    y.append(np.log(sum(total_times) / len(total_times)))
        # Plot the surface.
        ax.plot(x, y, label=file_name.split("/")[-1].split("-")[0])
        ax.legend()

    ax.set_xlabel('Total Qubits')
    ax.set_ylabel('Logarithm of Time taken')

    plt.show()


if __name__ == "__main__":
    plot(["output-benchmark/db-addition-test-2.csv", "output-benchmark/qiskit-addition-test-2.csv",
          "output-benchmark/mixed-addition-test-2.csv"])
