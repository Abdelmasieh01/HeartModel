from Node import NodeTable, Node
from Path import PathTable
from AFlutterData import AFlutterData as Data

IDLE = 1
ERP = 2


class Heart:
    instance = None

    def __init__(self, h_node_names, h_node_int_parameters, h_node_positions, h_path_names, h_path_integer_parameters, h_path_float_parameters):
        self.m_path_table = PathTable(
            h_path_names, h_path_integer_parameters, h_path_float_parameters)
        self.m_node_table = NodeTable(
            h_node_names, h_node_int_parameters, h_node_positions, self.m_path_table)

    @staticmethod
    def getInstance():
        if Heart.instance is None:
            Heart.instance = Heart(Data.node_names, Data.node_int_parameters, Data.node_positions,
                                   Data.path_names, Data.path_int_parameters, Data.path_float_parameters)
        return Heart.instance

    # getter methods
    def getNodeTable(self):
        return self.m_node_table

    def getPathTable(self):
        return self.m_path_table

    # setter methods
    def setNodeTable(self, m_node_table):
        self.m_node_table = m_node_table

    def setPathTable(self, m_path_table):
        self.m_path_table = m_path_table

    def heart_automaton(self):
        temp_node = self.m_node_table
        temp_path = self.m_path_table
        path_table = self.m_path_table
        node_table = self.m_node_table
        temp_path_node = self.m_path_table
        temp_act = [False] * len(self.m_node_table.node_table)

        for i in range(len(self.m_node_table.node_table)):
            temp_node_elem = temp_node.node_table[i]
            temp_node_elem.setIndex_of_path_activate_the_node(-1)
            temp_node_elem.node_automaton(temp_path_node)
            temp_act[i] = temp_node_elem._node_para["activation"]

        for i in range(len(self.m_path_table.path_table)):
            node_act_1, node_act_2 = temp_path.path_table[i].path_automaton(
                node_table)
            path = path_table.path_table[i]
            entry_index = path._path_para["entry_node_index"]

            if node_table.node_table[entry_index]._node_para["node_state_index"] != ERP:
                temp_act[entry_index] = temp_act[entry_index] or node_act_1
                if node_act_1:
                    temp_node.node_table[entry_index].setIndex_of_path_activate_the_node(
                        i)
            else:
                temp_act[entry_index] = False
                node_table.node_table[entry_index].setTERP_current(
                    node_table.node_table[entry_index]._node_para["TERP_default"])

            exit_index = path._path_para["exit_node_index"]

            if node_table.node_table[exit_index]._node_para["node_state_index"] != ERP:
                temp_act[exit_index] = temp_act[exit_index] or node_act_2
                if node_act_2:
                    temp_node.node_table[exit_index].setIndex_of_path_activate_the_node(
                        i)
            else:
                temp_act[exit_index] = False
                node_table.node_table[exit_index].setTERP_current(
                    node_table.node_table[exit_index]._node_para["TERP_default"])

        for i in range(len(self.m_node_table.node_table)):
            temp_node.node_table[i].setActivation(temp_act[i])

        self.m_node_table = temp_node

        for i in range(len(temp_path.path_table)):
            if temp_path_node.path_table[i]._path_para["forward_timer_default"] != temp_path.path_table[i]._path_para["forward_timer_default"]:
                temp_path.path_table[i].setForwardTimerDefault(
                    temp_path_node.path_table[i]._path_para["forward_timer_default"])

                if temp_path_node.path_table[i]._path_para["path_state_index"] == IDLE:
                    temp_path.path_table[i].setForwardTimerCurrent(
                        temp_path.path_table[i]._path_para["forward_timer_default"])

            if temp_path.path_table[i]._path_para["backward_timer_default"] != self.m_path_table.path_table[i]._path_para["backward_timer_default"]:
                self.m_path_table.path_table[i].setBackwardTimerDefault(
                    temp_path.path_table[i]._path_para["backward_timer_default"])
                if temp_path.path_table[i]._path_para["path_state_index"] == IDLE:
                    self.m_path_table.path_table[i].setBackwardTimerCurrent(
                        self.m_path_table.path_table[i]._path_para["backward_timer_default"])

        self.m_path_table = temp_path
