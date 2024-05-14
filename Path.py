import random

IDLE = 1
ANTEGRADE = 2
RETROGRADE = 3
CONFLICT = 4
DOUBLE = 5


class Path:
    def __init__(self, path_name, path_integer_parameters, path_float_parameters):
        self._path_para = {
            "path_name": path_name,
            # (1) Idle, (2) Antegrade conduction, (3) Retrograde, (4) Conflict, and (5) Double
            "path_state_index": path_integer_parameters[0],
            # entry_node_index=0 (originally 1)
            "entry_node_index": path_integer_parameters[1] - 1,
            # exit_node_index=1 (originally 2)
            "exit_node_index": path_integer_parameters[2] - 1,
            "amplitude_factor": path_integer_parameters[3],
            "forward_speed": path_float_parameters[0],
            "backward_speed": path_float_parameters[1],
            "forward_timer_current": path_float_parameters[2],
            "forward_timer_default": path_float_parameters[3],
            "backward_timer_current": path_float_parameters[4],
            "backward_timer_default": path_float_parameters[5],
            "path_length": path_float_parameters[6],
            "path_slope": path_float_parameters[7]
        }

    def path_automaton(self, NT):
        temp_node1_activation = False
        temp_node2_activation = False

        entry_node_index = self._path_para["entry_node_index"]
        exit_node_index = self._path_para["exit_node_index"]
        entry_node = NT.node_table[entry_node_index]
        exit_node = NT.node_table[exit_node_index]

        if self._path_para["path_state_index"] == IDLE: 
            if entry_node._node_para["activation"]:
                # Antegrade conduction
                self._path_para["path_state_index"] = ANTEGRADE
            elif exit_node._node_para["activation"]:
                self._path_para["path_state_index"] = RETROGRADE 

        elif self._path_para["path_state_index"] == ANTEGRADE:  
            if exit_node._node_para["activation"]:
                self._path_para["path_state_index"] = DOUBLE  
            else:
                if self._path_para["forward_timer_current"] == 0:
                    self._path_para["forward_timer_current"] = self._path_para["forward_timer_default"]
                    temp_node2_activation = True
                    self._path_para["path_state_index"] = CONFLICT  
                else:
                    self._path_para["forward_timer_current"] -= 1

        elif self._path_para["path_state_index"] == RETROGRADE:  
            if entry_node._node_para["activation"]:
                self._path_para["path_state_index"] = DOUBLE  
            else:
                if self._path_para["backward_timer_current"] == 0:
                    self._path_para["backward_timer_current"] = self._path_para["backward_timer_default"]
                    temp_node1_activation = True
                    self._path_para["path_state_index"] = CONFLICT  # Conflict
                else:
                    self._path_para["backward_timer_current"] -= 1

        elif self._path_para["path_state_index"] == CONFLICT:  # Conflict
            self._path_para["path_state_index"] = IDLE  # Idle

        elif self._path_para["path_state_index"] == DOUBLE:  # Double
            if self._path_para["backward_timer_current"] == 0:
                self._path_para["backward_timer_current"] = self._path_para["backward_timer_default"]
                temp_node1_activation = True
                self._path_para["path_state_index"] = CONFLICT  # Conflict
                return temp_node1_activation, temp_node2_activation

            if self._path_para["forward_timer_current"] == 0:
                self._path_para["forward_timer_current"] = self._path_para["forward_timer_default"]
                temp_node2_activation = True
                self._path_para["path_state_index"] = CONFLICT  # Conflict
                return temp_node1_activation, temp_node2_activation

            forward_ratio = self._path_para["forward_timer_current"] / \
                self._path_para["forward_timer_default"]
            backward_ratio = self._path_para["backward_timer_current"] / \
                self._path_para["backward_timer_default"]

            if abs(1 - forward_ratio - backward_ratio) < (0.9 / min(self._path_para["forward_timer_default"], self._path_para["backward_timer_default"])):
                self._path_para["backward_timer_current"] = self._path_para["backward_timer_default"]
                self._path_para["forward_timer_current"] = self._path_para["forward_timer_default"]
                self._path_para["path_state_index"] = 4  # Conflict
            else:
                self._path_para["forward_timer_current"] -= 1
                self._path_para["backward_timer_current"] -= 1

        return temp_node1_activation, temp_node2_activation


class PathTable:
    def __init__(self, path_names, path_integer_parameters, path_float_parameters):
        self.path_table = []
        self.path_terminal_pairs_per_point_list = []
        node_idx_paths_terminals_umap = {}

        # Creating path objects and populating path_table
        for i in range(len(path_names)):
            path1 = Path(
                path_names[i], path_integer_parameters[i], path_float_parameters[i])
            self.path_table.append(path1)

            entry_idx = path1._path_para["entry_node_index"]
            exit_idx = path1._path_para["exit_node_index"]

            # Creating dictionary for node index to list of path_terminal_pairs mapping
            if entry_idx not in node_idx_paths_terminals_umap:
                node_idx_paths_terminals_umap[entry_idx] = []
            if exit_idx not in node_idx_paths_terminals_umap:
                node_idx_paths_terminals_umap[exit_idx] = []

            node_idx_paths_terminals_umap[entry_idx].append(
                {"path_idx": len(self.path_table) - 1, "terminal": "__entry"})
            node_idx_paths_terminals_umap[exit_idx].append(
                {"path_idx": len(self.path_table) - 1, "terminal": "__exit"})

        # Populating path_terminal_pairs_per_point_list
        for node_idx, path_terminal_pairs in node_idx_paths_terminals_umap.items():
            self.path_terminal_pairs_per_point_list.append(path_terminal_pairs)
