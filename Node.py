import random

REST = 1
ERP = 2
RRP = 3
class Node:
    def __init__(self, node_name, node_integer_parameters, path_terminal_pair, node_pos):
        self._node_para = {
            "node_name": node_name,
            "node_state_index": node_integer_parameters[0],  # 1 for rest, 2 for ERP, 3 for RRP
            "TERP_current": node_integer_parameters[1],
            "TERP_default": node_integer_parameters[2],
            "TRRP_current": node_integer_parameters[3],
            "TRRP_default": node_integer_parameters[4],
            "Trest_current": node_integer_parameters[5],
            "Trest_default": node_integer_parameters[6],
            "activation": bool(node_integer_parameters[7]),
            "Terp_min": node_integer_parameters[8],
            "Terp_max": node_integer_parameters[9],
            "index_of_path_activate_the_node": node_integer_parameters[10],
            "AVness": node_integer_parameters[11],
            "connected_paths": path_terminal_pair,
            "node_pos": node_pos
        }

    def node_automaton(self, PT):
        t_activation = False

        if self._node_para["activation"]:
            t_Terp_min = self._node_para["Terp_min"]
            t_Terp_max = self._node_para["Terp_max"]

            if self._node_para["node_state_index"] == REST:  # Rest
                self._node_para["TERP_default"] = t_Terp_max
                self._node_para["TERP_current"] = round(self._node_para["TERP_default"] + (random.random() - 0.5) * 0 * self._node_para["TERP_default"])

                for i in range(len(self._node_para["connected_paths"])):
                    path_idx = self._node_para["connected_paths"][i]["path_idx"]
                    if self._node_para["index_of_path_activate_the_node"] == path_idx:
                        continue

                    # TODO: change this to python
                    # const path_parameters &path_parameters =
                    #     PT.path_table[path_idx].getParameters();
                    # const float original_forward_speed = path_parameters.forward_speed;
                    # const float original_backward_speed = path_parameters.backward_speed;
                    # const float original_path_length = path_parameters.path_length;
        
                    if self._node_para["connected_paths"][i]["terminal"] == "entry":
                        tmp_forward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["forward_speed"])
                        PT.path_table[path_idx].setForwardTimerDefault(tmp_forward_timer_default)
                    else:
                        tmp_backward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["backward_speed"])
                        PT.path_table[path_idx].setBackwardTimerDefault(tmp_backward_timer_default)

                self._node_para["Trest_current"] = round(self._node_para["Trest_default"] * (1 + (random.random() - 0.5) * 0))
                self._node_para["node_state_index"] = ERP  # ERP

            elif self._node_para["node_state_index"] == ERP:  # ERP
                self._node_para["TERP_default"] = t_Terp_min

                for idx in range(len(self._node_para["connected_paths"])):
                    path_idx = self._node_para["connected_paths"][idx]["path_idx"]
                    if self._node_para["index_of_path_activate_the_node"] == path_idx:
                        continue

                    # TODO: change this to Python
                    # const path_parameters &path_parameters =
                    # PT.path_table[path_idx].getParameters();
                    # const float original_forward_speed =
                    # path_parameters.forward_speed;  // path_table{path_idx, 6}
                    # const float original_backward_speed =
                    # path_parameters.backward_speed;  // path_table{path_idx, 7}
                    # const float original_path_length =
                    # path_parameters.path_length;  // path_table{path_idx, 12}

                    if self._node_para["connected_paths"][idx]["terminal"] == "entry":
                        tmp_forward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["forward_speed"] * (self._node_para["AVness"] + 1))
                        PT.path_table[path_idx].setForwardTimerDefault(tmp_forward_timer_default)
                    else:
                        tmp_backward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["backward_speed"] * 3)
                        PT.path_table[path_idx].setBackwardTimerDefault(tmp_backward_timer_default)

                self._node_para["TERP_current"] = round((1 + (random.random() - 0.5) * 0) * self._node_para["TERP_default"])

            elif self._node_para["node_state_index"] == RRP:  # RRP
                ratio = self._node_para["TRRP_current"] / self._node_para["TRRP_default"]

                if self._node_para["AVness"] == 1:
                    self._node_para["TERP_default"] = t_Terp_max + round((1 + (random.random() - 0.5) * 0) * (1 - (1 - ratio) * (1 - ratio) * (1 - ratio)) * (t_Terp_min - t_Terp_max))
                else:
                    self._node_para["TERP_default"] = t_Terp_min + round((1 + (random.random() - 0.5) * 0) * (1 - (ratio * ratio * ratio)) * (t_Terp_max - t_Terp_min))

                self._node_para["TERP_current"] = round((1 + (random.random() - 0.5) * 0) * self._node_para["TERP_default"])

                for idx in range(len(self._node_para["connected_paths"])):
                    path_idx = self._node_para["connected_paths"][idx]["path_idx"]
                    if self._node_para["index_of_path_activate_the_node"] == path_idx:
                        continue

                    # TODO: change this to Python
                    # const path_parameters &path_parameters =
                    # PT.path_table[path_idx].getParameters();
                    # const float original_path_length = path_parameters.path_length;
                    # const float original_forward_speed = path_parameters.forward_speed;
                    # const float original_backward_speed = path_parameters.backward_speed;
          
                    if self._node_para["AVness"] == 1:
                        if self._node_para["connected_paths"][idx]["terminal"] == "entry":
                            tmp_forward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["forward_speed"] * (1 + ratio * 3))
                            PT.path_table[path_idx].setForwardTimerDefault(tmp_forward_timer_default)
                        else:
                            tmp_backward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["backward_speed"] * (1 + ratio * 3))
                            PT.path_table[path_idx].setBackwardTimerDefault(tmp_backward_timer_default)
                    else:
                        if self._node_para["connected_paths"][idx]["terminal"] == "entry":
                            tmp_forward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["forward_speed"] * (1 + ratio * ratio * 3))
                            PT.path_table[path_idx].setForwardTimerDefault(tmp_forward_timer_default)
                        else:
                            tmp_backward_timer_default = round((1 + (random.random() - 0.5) * 0) * PT.path_table[path_idx].getParameters()["path_length"] / PT.path_table[path_idx].getParameters()["backward_speed"] * (1 + ratio * ratio * 3))
                            PT.path_table[path_idx].setBackwardTimerDefault(tmp_backward_timer_default)

                self._node_para["TRRP_current"] = round((1 + (random.random() - 0.5) * 0) * self._node_para["TRRP_default"])
                self._node_para["node_state_index"] = ERP

        else:
            if self._node_para["node_state_index"] == REST:  # Rest
                if self._node_para["Trest_current"] == 0:
                    self._node_para["node_state_index"] = ERP  # ERP
                    self._node_para["Trest_current"] = round((1 + (random.random() - 0.5) * 0) * self._node_para["Trest_default"])
                    t_activation = True
                else:
                    self._node_para["Trest_current"] -= 1
            elif self._node_para["node_state_index"] == ERP:  # ERP
                if self._node_para["TERP_current"] == 0:
                    self._node_para["node_state_index"] = RRP  # RRP
                    self._node_para["TERP_current"] = round((1 + (random.random() - 0.5) * 0) * self._node_para["TERP_default"])
                else:
                    self._node_para["TERP_current"] -= 1
            elif self._node_para["node_state_index"] == RRP:  # RRP
                if self._node_para["TRRP_current"] == 0:
                    self._node_para["node_state_index"] = REST  # Rest
                    self._node_para["TRRP_current"] = round((1 + (random.random() - 0.5) * 0) * self._node_para["TRRP_default"])
                else:
                    self._node_para["TRRP_current"] -= 1

        self._node_para["activation"] = t_activation

class NodeTable:
    def __init__(self, node_names, node_int_parameters, node_positions, PathTable):
        self.node_table = []
        for i in range(len(node_names)):
            path_terminal_pair1 = PathTable.path_terminal_pairs_per_point_list[i]
            node1 = Node(node_names[i], node_int_parameters[i], path_terminal_pair1, node_positions[i])
            self.node_table.append(node1)
