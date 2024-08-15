import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import logging
from network import GasLibNetwork
import lib.gaslibparse.helpers
from loggerFilter import DuplicateFilter

from pyomo.environ import SolverFactory, value

from lib.gaslibparse import GasLibParserUnits, Pipe,  \
    CompressorStation, ControlValve, Valve, Resistor, ShortPipe, \
    Entry, Exit, unit

# path to .scn file
scn_file = f"./instances/GasLib-11/GasLib-11.scn"
    

# path to .net file
net_file = f"./instances/GasLib-11/GasLib-11.net"



import networkx as nx
import numpy as np

network_data = {
        "interdictionBudget": {None: "0"},
        "nodes": {
            None: [
                "N01",
                "N02",
                "entry01",
                "exit01",
            ]
        },
        "sigma": {
            "entry01": 1,
            "exit01": -1,
        },
        "loadflow": {
            "entry01": 100.0,
            "exit01": 100.0,
        },
        "pressureLb": {
            "N01": 40.0,
            "N02": 40.0,
            "entry01": 40.0,
            "exit01": 40.0,
        },
        "pressureUb": {
            "N01": 70.0,
            "N02": 70.0,
            "entry01": 70.0,
            "exit01": 70.0,
        },
        "loadshedLB": {
            "entry01": -1,
            "exit01": 0.0,
        },
        "weaklyConnectedLoadflow": {
            "entry01": 3,
            "N01": -1.0,
            "N02": -1.0,
            "exit01": -1.0,
        },
        "arcs": {
            None: [
                ("N01", "N02"),
                ("N02", "exit01"),
                ("entry01", "N01"),
                ("entry01", "exit01"),
            ]
        },
        "pressureLossFactor": {
            ("N01", "N02"): 0.5660644491026487,
            ("N02", "exit01"): 0.5660644491026487,
            ("entry01", "N01"): 0.5660644491026487,
            ("entry01", "exit01"): 0.5660644491026487,
        },
        "activeElements": {None: []},
        "massflowLb": {
            ("N01", "N02"): -65.41666666666666,
            ("N02", "exit01"): -65.41666666666666,
            ("entry01", "N01"): -65.41666666666666,
            ("entry01", "exit01"): -65.41666666666666
        },
        "massflowUb": {
            ("N01", "N02"): 65.41666666666666,
            ("N02", "exit01"): 65.41666666666666,
            ("entry01", "N01"): 65.41666666666666,
            ("entry01", "exit01"): 65.41666666666666,
        }
    }

class Node:
    def __init__(self, node_id, pos):
        self.node_id = node_id
        self.pos = pos

class Arc:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class GasLibNetwork:
    def __init__(self):
        self.nodes = {
            'N01': Node('N01', [0, 0]),
            'N02': Node('N02', [1, 0]),
            'entry01': Node('entry01', [0, 1]),
            'exit01': Node('exit01', [1, 1])
        }
        self.passiveArcs = {
            'arc1': Arc('N01', 'N02'),
            'arc2': Arc('N02', 'exit01'),
            'arc3': Arc('entry01', 'N01'),
            'arc4': Arc('entry01', 'exit01')
        }

graph = GasLibNetwork()

import matplotlib.pyplot as plt

def read_solution_file(sol_path):
    solution = {"nodes": {}, "arcs": {}}
    
    with open(sol_path, 'r') as file:
        for line in file:
            if line.startswith("#") or line.strip() == "":
                continue
            
            parts = line.split()
            var_name = parts[0]
            value = float(parts[1])
            
            if '[' in var_name and ']' in var_name:
                var_type, indices = var_name.split('[')
                indices = indices.strip(']').split(',')
                
                if len(indices) == 1:
                    node = indices[0]
                    if node not in solution["nodes"]:
                        solution["nodes"][node] = {}
                    solution["nodes"][node][var_type] = value
                elif len(indices) == 2:
                    arc = tuple(indices)
                    if arc not in solution["arcs"]:
                        solution["arcs"][arc] = {}
                    solution["arcs"][arc][var_type] = value
    return solution

def add_problem_boundaries_to_solution_data(solution_data, network_data):
    for element in solution_data.keys():
        for nodeId in solution_data[element].keys():
            for bound_name in network_data.keys():
                if nodeId in network_data[bound_name].keys():
                    solution_data[element][nodeId][bound_name] = network_data[bound_name][nodeId]
    return solution_data
    
def plot_solution(graph, sol_path, optimal_interdiction_decision,show_all_attributes: bool, mathematical_var_names: bool):
    solution_data = read_solution_file(sol_path)
    solution_data = add_problem_boundaries_to_solution_data(solution_data, network_data)
    interdicted_network = nx.MultiDiGraph()
    interdiction = optimal_interdiction_decision
    
    # Add nodes with attributes
    for nodeId, nodeData in graph.nodes.items():
        if show_all_attributes:
            node_attrs = solution_data["nodes"].get(nodeId, {})
        else:
            nodeId_data = solution_data["nodes"][nodeId]
            node_attrs = {'π' if mathematical_var_names else 'pressure': f'{nodeId_data["pressureLb"]} <= {nodeId_data["pressure"]} <= {nodeId_data["pressureUb"]}',
                          'λ' if mathematical_var_names else 'loadshed': f'{nodeId_data["loadshedLB"] if "loadshedLB" in nodeId_data.keys() else 0.0} <= {nodeId_data["loadshed"]} <= 1.0'}
        interdicted_network.add_node(nodeId, **nodeData.__dict__, **node_attrs)

    # Add passive arcs with attributes
    for arcData in graph.passiveArcs.values():
        tmp_arc = (arcData.from_node, arcData.to_node)
        if show_all_attributes:
            arc_attrs = solution_data["arcs"].get(tmp_arc, {})
        else:
            tmp_arc_data = solution_data["arcs"][tmp_arc]
            arc_attrs = {'q' if mathematical_var_names else 'flow': f'{tmp_arc_data["massflowLb"]} <= {tmp_arc_data["flow"]} <= {tmp_arc_data["massflowUb"]}'}
        color = "red" if interdiction.get(str(tmp_arc), 0.0) == 1.0 else "black"
        interdicted_network.add_edge(arcData.from_node, arcData.to_node, color=color, **arc_attrs)

    pos = {node.node_id: np.array(node.pos) for node in graph.nodes.values()}

    edge_color_list = [color for _, _, _, color in interdicted_network.edges(data="color", keys=True)]

    # Draw the graph
    nx.draw(interdicted_network, pos, node_size=500, with_labels=False, font_size=10, edge_color=edge_color_list)

    # Draw node labels with attributes, excluding 'node_id' and 'position'
    node_labels = {
        node: f"{node}\n" + "\n".join([f"{k}: {v}" for k, v in attrs.items() if k not in ['node_id', 'pos']])
        for node, attrs in interdicted_network.nodes(data=True)
    }
    nx.draw_networkx_labels(interdicted_network, pos, labels=node_labels, font_size=10)

    # Draw edge labels with attributes
    edge_labels = {
        (u, v): "\n".join([f"{k}: {v}" for k, v in attrs.items() if k not in ['color']])
        for u, v, attrs in interdicted_network.edges(data=True)
    }
    nx.draw_networkx_edge_labels(interdicted_network, pos, edge_labels=edge_labels, font_size=8)

    plt.show()

# Beispielverwendung
optimal_interdiction_decision = {
    "('N01', 'N02')": 1.0,
    "('N02', 'exit01')": 0.0,
    "('entry01', 'N01')": 0.0,
    "('entry01', 'exit01')": 0.0
}

plot_solution(graph, 'test.sol', optimal_interdiction_decision, False, True)
