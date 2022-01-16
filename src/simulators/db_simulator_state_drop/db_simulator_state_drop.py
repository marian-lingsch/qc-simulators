import sqlite3
import time
from typing import List, Tuple

import numpy as np

from gate import GatesIdentfications
from simulators.simulator import Simulator


class DBSimulatorStateDrop(Simulator):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cur = self.conn.cursor()
        self.maximum_rows = 1000
        self.amnt_qubits = None
        self.name = "DBSimulatorStateDrop"
        # See: https://blog.devart.com/increasing-sqlite-performance.html
        self.cur.execute('''PRAGMA threads = 8''')  # Maximum of the compiled version of sql
        self.cur.execute('''PRAGMA journal_mode = OFF''')
        self.cur.execute('''PRAGMA synchronous  = OFF''')
        self.cur.execute('''PRAGMA LOCKING_MODE  = EXCLUSIVE''')

    def run(self, gates, amnt_qubits=None) -> float:
        start = time.process_time()
        if amnt_qubits is not None:
            if self.amnt_qubits is not None:
                self.destroy_db()
            self.init_db(amnt_qubits)
        for gate in gates:
            if gate.gatter == GatesIdentfications.cnot:
                self.execute_cnot(gate.qubits)
            elif gate.gatter == GatesIdentfications.ccnot:
                self.execute_ccnot(gate.qubits)
            elif gate.gatter == GatesIdentfications.paulix:
                self.execute_paulix(gate.qubits)
            elif gate.gatter == GatesIdentfications.pauliy:
                self.execute_pauliy(gate.qubits)
            elif gate.gatter == GatesIdentfications.pauliz:
                self.execute_pauliz(gate.qubits)
            elif gate.gatter == GatesIdentfications.hadamard:
                self.execute_hadamard(gate.qubits)
            elif gate.gatter == GatesIdentfications.reset:
                self.reset_qubits(gate.qubits)
            elif gate.gatter == GatesIdentfications.invert_all_zero:
                self.invert_all_zero(gate.qubits)
            elif gate.gatter == GatesIdentfications.invert_some_one:
                self.invert_some_one(gate.qubits)
            elif gate.gatter == GatesIdentfications.invert_all_one:
                self.invert_all_one(gate.qubits)
            elif gate.gatter == GatesIdentfications.diffusion:
                self.diffusion(gate.qubits)
            else:
                print("Unknown Gate Type")
                raise
        self.get_state()
        end = time.process_time()
        return end - start

    def init_db(self, amnt_qubits: int):
        assert amnt_qubits > 0
        self.amnt_qubits = amnt_qubits
        query_create = "CREATE TABLE quantumstate_drop ("
        primary_key = ""
        for _t in range(amnt_qubits):
            query_create += "q" + str(_t) + " Integer , "
            if _t == 0:
                primary_key += "q" + str(_t)
            else:
                primary_key += ", " + "q" + str(_t)
        query_create += " revalue REAL, imvalue REAL, PRIMARY KEY (" + primary_key + ") )"
        self.cur.execute(query_create)
        self.cur.execute("insert into quantumstate_drop values (?" + ", ?" * (amnt_qubits + 1) + ")",
                         [0 for _t in range(amnt_qubits)] + [1.0, 0.0])
        return

    def init_with_state(self, state: List[Tuple[List[int], float, float]]):
        assert abs(sum([r ** 2 + i ** 2 for (_s, r, i) in state]) - 1.0) < 1e-6
        self.cur.execute("DELETE FROM quantumstate_drop")
        for (s, r, i) in state:
            assert len(s) == self.amnt_qubits
            self.cur.execute("insert into quantumstate_drop values (?" + ", ?" * (self.amnt_qubits + 1) + ")",
                             s + [r, i])
        return

    def destroy_db(self):
        self.cur.execute("DROP TABLE quantumstate_drop")

    def get_state(self):
        """
        Only this function commits the transaction. This is done for performance reasons. Only use this function
        to access the state or commit before accessing the state.
        :return:
        """
        self.conn.commit()
        return self.cur.execute('SELECT * FROM quantumstate_drop').fetchall()

    def execute_cnot(self, qubits):
        assert len(qubits) == 2
        query = "update quantumstate_drop set q{1} = (1 - q{1})*q{0} + q{1}*(1 - q{0}) where 1".format(qubits[0],
                                                                                                       qubits[1])
        self.cur.execute(query)
        return

    def execute_paulix(self, qubits):
        assert len(qubits) == 1
        query = "update quantumstate_drop set q{0} = (1 - q{0}) where 1".format(qubits[0])
        self.cur.execute(query)
        return

    def execute_pauliy(self, qubits):
        assert len(qubits) == 1
        query = "update quantumstate_drop set q{0} = (1 - q{0})," \
                " imvalue = case when q{0} = 1 then -revalue else revalue end, " \
                "revalue = case when q{0} = 1 then imvalue else -imvalue END where 1".format(
            qubits[0])
        self.cur.execute(query)
        return

    def execute_pauliz(self, qubits):
        assert len(qubits) == 1
        query = "update quantumstate_drop set imvalue = case when q{0} = 1 then -imvalue else imvalue end," \
                " revalue = case when q{0} = 1 then -revalue else revalue END where 1".format(
            qubits[0])
        self.cur.execute(query)
        return

    def execute_ccnot(self, qubits):
        assert len(qubits) == 3
        query = "update quantumstate_drop set q{2} = case when q{0} = 1 AND q{1} = 1 then 1 - q{2} ELSE q{2} END where 1".format(
            qubits[0],
            qubits[1], qubits[2])
        self.cur.execute(query)
        return

    def execute_hadamard(self, qubits):
        """
        This gate is more complicated than the other, since multiple states can be fused into one, so a simple update is
        not possible. Thats why we sepparate the update into four queries and aggregate over them.
        """
        # queryj means query qubit output value j

        query0 = "Select " + ", ".join(
            ["q" + str(_t) if _t != qubits[0] else "0 as q" + str(_t) for _t in
             range(self.amnt_qubits)]) + ", revalue*{0} as revalue, imvalue*{0}  as imvalue".format(
            np.sqrt(0.5)) + " FROM quantumstate_drop"

        query1 = "Select " + ", ".join(
            ["q" + str(_t) if _t != qubits[0] else "1 as q" + str(_t) for _t in
             range(
                 self.amnt_qubits)]) + ", revalue*{0}*(1 - {1}) - revalue*{0}*{1} as revalue, imvalue*{0}*(1 - {1}) - imvalue*{0}*{1}  as imvalue".format(
            np.sqrt(0.5), "q" + str(qubits[0])) + " FROM quantumstate_drop"

        new_values = "Select " + ", ".join(["q" + str(t) for t in range(self.amnt_qubits)]) + \
                     ", sum(revalue) as revalue, sum(imvalue) as imvalue FROM (" + query0 + " union all " + query1 + ") GROUP BY " + ", ".join(
            ["q" + str(_t) for _t in range(self.amnt_qubits)])

        update_query = "replace into quantumstate_drop (" + ", ".join(
            ["q" + str(_t) for _t in range(
                self.amnt_qubits)]) + ", revalue, imvalue) " + new_values
        self.cur.execute(update_query)

        delete_query = "delete from quantumstate_drop order by imvalue*imvalue + revalue*revalue ASC, random() LIMIT (SELECT case when count(*) - " + str(
            self.maximum_rows) + " < 0 then 0 else count(*) - " + str(
            self.maximum_rows) + " end FROM quantumstate_drop)"
        self.cur.execute(delete_query)
        return

    def reset_qubits(self, qubits: List[int]):
        """
        This will produce irregularities, meaning the quantum state does not have amplitude 1,
         if the superposition is dependent on the resetted qubits
        """
        query = "update quantumstate_drop set " + ",".join(["q{0} = 0".format(q) for q in qubits]) + " where 1"
        self.cur.execute(query)
        return

    def invert_all_zero(self, qubits: List[int]):
        query = "update quantumstate_drop set revalue = -revalue, imvalue = -imvalue where " + " and ".join(
            ["q{0} = 0".format(q) for q in qubits])
        self.cur.execute(query)
        return

    def invert_some_one(self, qubits: List[int]):
        query = "update quantumstate_drop set revalue = -revalue, imvalue = -imvalue where " + " or ".join(
            ["q{0} = 1".format(q) for q in qubits])
        self.cur.execute(query)
        return

    def invert_all_one(self, qubits: List[int]):
        query = "update quantumstate_drop set revalue = -revalue, imvalue = -imvalue where " + " and ".join(
            ["q{0} = 1".format(q) for q in qubits])
        self.cur.execute(query)
        return

    def diffusion(self, qubits):
        query = "update quantumstate_drop set revalue = -revalue + (Select sum(revalue)*" + str(
            2.0 / (2 ** len(qubits))) + " FROM quantumstate_drop)" \
                                        ", imvalue = -imvalue + (Select sum(imvalue)*" + str(
            2.0 / (2 ** len(qubits))) + " FROM quantumstate_drop) where 1"
        self.cur.execute(query)
        return
