# qc-simulators

A comparison is made between different quantum computing simulators. The different simulators are:
* [Array Simulator](./src/simulators/array_simulator/array_simulator.py)
* [Database Simulator](./src/simulators/db_simulator/db_simulator.py)
* [Database State Drop Simulator](./src/simulators/db_simulator_state_drop/db_simulator_state_drop.py)
* [Mixed Simulator](./src/simulators/mixed_simulator/mixed_simulator.py)
* [Qiskit State Vector Simulator](./src/simulators/qiskit/qiskit_simulator.py)

## Usage

Update the variables which control what is being executed in [main](src/main.py). Once this is done execute the following in [src](src):

```shell
python3 main.py
```

This should run the experiments and produce the output as desired. To analyze the output produced, please use the functions found in [plot](src/plot.py). In that file you see some examples on how to call the functions. Once the file has been updated to match your requirements please execute the following in [src](src):

```shell
python3 plot.py
```

This should make the plots you requested.

## Tests

The simulators are [tested](./src/test) by using the python [unittest](https://docs.python.org/3/library/unittest.html) framework. These also exemplify some usages of the simulators. To run all tests, please execute the following in the [src](./src) directory:

```shell
python3 -m unittest discover test
```