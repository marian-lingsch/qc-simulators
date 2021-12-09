import abc


class Simulator(metaclass=abc.ABCMeta):

    def __init__(self):
        self.name = None

    @abc.abstractmethod
    def run(self, gates, amnt_qubits=None) -> float:
        pass

    @abc.abstractmethod
    def get_state(self):
        pass
