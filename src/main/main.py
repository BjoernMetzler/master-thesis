"""
This is only a simple main to give an example
how to parse the instance files
"""
import helpers.network
import sys
import multiprocessing
import ast
import networkx as nx
import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly.io as pio
import numpy as np
from model import *


if (len(sys.argv) >= 4):
    Budget = int(sys.argv[3])


if (len(sys.argv) >= 3):
    mode = sys.argv[2]
    
networkInstanceName = sys.argv[1]

if "testModel4" not in networkInstanceName:
    # path to .scn file
    scn_file = f"./assets/instances/{networkInstanceName}/{networkInstanceName}.scn"
    
    # path to .net file
    net_file = f"./assets/instances/{networkInstanceName}/{networkInstanceName}.net"

    # now build the network object
    network = helpers.network.GasLibNetwork(net_file, scn_file)
    # create model for data (not complete)
    withoutFlowBounds = False
    network._toPyomo(False)

    pyomoData = network.pyomoData[None] 
    
else:
    # Read the data from the file
    with open(f'./assets/instances/pyomoData/{networkInstanceName}.txt', 'r') as file:
        file_contents = file.read()

    # Convert the string representation of the dictionary to an actual dictionary
    pyomoData = ast.literal_eval(file_contents)

    import networkx as nx

    import numpy as np
    import matplotlib.pyplot as plt
    
    #TODO: Work on visualization for this case 
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
            self.arcs = {
                'arc1': Arc('N01', 'N02'),
                'arc2': Arc('N02', 'exit01'),
                'arc3': Arc('entry01', 'N01'),
                'arc4': Arc('entry01', 'exit01')
            }
    '''class GasLibNetwork:
        def __init__(self, network_data):
            self.network = nx.MultiDiGraph(name=network_data.get('networkInstanceName', 'GasLibNetwork'))
            self.network_data = network_data
            self.create_nodes()
            self.create_arcs()
            #self.add_attributes()
            self.set_positions()

        def create_nodes(self):
            for node_id in self.network_data['nodes'][None]:
                self.network.add_node(node_id)

        def create_arcs(self):
            for from_node, to_node in self.network_data['arcs'][None]:
                self.network.add_edge(from_node, to_node)

        def add_attributes(self):
            nx.set_node_attributes(self.network, self.network_data['pressureLb'], 'pressureLb')
            nx.set_node_attributes(self.network, self.network_data['pressureUb'], 'pressureUb')
            nx.set_node_attributes(self.network, self.network_data['loadflow'], 'loadflow')
            nx.set_node_attributes(self.network, self.network_data['sigma'], 'sigma')
            nx.set_node_attributes(self.network, self.network_data['loadshedLB'], 'loadshedLB')
            nx.set_node_attributes(self.network, self.network_data['weaklyConnectedLoadflow'], 'weaklyConnectedLoadflow')
            nx.set_edge_attributes(self.network, self.network_data['pressureLossFactor'], 'pressureLossFactor')
            nx.set_edge_attributes(self.network, self.network_data['massflowLb'], 'massflowLb')
            nx.set_edge_attributes(self.network, self.network_data['massflowUb'], 'massflowUb')

        def set_positions(self):
            # Use a layout algorithm for better visualization
            pos = nx.spring_layout(self.network, seed=42)
            for node_id, position in pos.items():
                self.network.nodes[node_id]['pos'] = position

        @property
        def nodes(self):
            return self.network.nodes

        @property
        def arcs(self):
            return {(u, v): self.network[u][v] for u, v in self.network.edges}
        '''
        
    network=GasLibNetwork()
    '''
    print(network.arcs)
    print(network.nodes)
    # Now pyomoData contains the data from the file
    print(pyomoData)'''
    
# display data for the model
'''displayModes = ["cmi","teXt","json"]
lib.gaslibparse.helpers.print_pyomoData(network.pyomoData[None], displayModes, networkInstanceName)'''



def run_method(mode, pyomoData, networkInstanceName, Budget):
    model = Single_Level_Formulation_Model(pyomoData,networkInstanceName,Budget,False)
    
    if mode == "SL_SOS1":
        result= model.single_level_model_SOS1()
    elif mode == "SL_CC":
        result= model.single_level_model_CC()
    elif mode == "SL_BigM":
        result= model.single_level_model_BigM()
    elif mode == "Enum_Approach":
        result = model.enum_approach()
        
    # Old model (CURRENT_MODELS.py)
    '''elif mode == "Enum_Primal":
        model = LeaderModel(data, networkInstanceName, Budget, False, False)
        result= {"interdiction": model.bruteForce()[0][0], "objVal": model.bruteForce()[0][1], "Runtime": model.bruteForce()[0][2]}
    elif mode == "Enum_CC":
        model = LeaderModel(data, networkInstanceName, Budget, True, True)
        result= {"interdiction": model.bruteForce()[0][0], "objVal": model.bruteForce()[0][1], "Runtime": model.bruteForce()[0][2]}
    elif mode == "Enum_SOS1":
        model = LeaderModel(data, networkInstanceName, Budget, False, True)
        result= {"interdiction": model.bruteForce()[0][0], "objVal": model.bruteForce()[0][1], "Runtime": model.bruteForce()[0][2]}
    elif mode == "Enum_BigM":
        model = LeaderModel(data, networkInstanceName, Budget, True, False)
        result= {"interdiction": model.bruteForce()[0][0], "objVal": model.bruteForce()[0][1], "Runtime": model.bruteForce()[0][2]}
    '''  
    
    optimal_interdiction_decision = result["interdiction"]
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

    def plot_solution(graph, sol_path, optimal_interdiction_decision, show_all_attributes: bool, mathematical_var_names: bool):
        solution_data = read_solution_file(sol_path)
        solution_data = add_problem_boundaries_to_solution_data(solution_data, pyomoData)
        interdicted_network = nx.MultiDiGraph()
        interdiction = optimal_interdiction_decision
        
        #plt.switch_backend('Qt5Agg')
        # Add nodes with attributes
        for nodeId, nodeData in graph.nodes.items():
            if show_all_attributes:
                node_attrs = solution_data["nodes"].get(nodeId, {})
            else:
                nodeId_data = solution_data["nodes"][nodeId]
                node_attrs = {
                    'π' if mathematical_var_names else 'pressure': f'{nodeId_data["pressureLb"]:.2f} <= {nodeId_data["pressure"]:.2f} <= {nodeId_data["pressureUb"]:.2f}',
                    'λ' if mathematical_var_names else 'loadshed': f'{nodeId_data.get("loadshedLB", 0.0):.2f} <= {nodeId_data["loadshed"]:.2f} <= 1.0'
                }
            interdicted_network.add_node(nodeId, **nodeData.__dict__, **node_attrs)

        # Add passive arcs with attributes
        for arcData in graph.arcs.values():
            tmp_arc = (arcData.from_node, arcData.to_node)
            if show_all_attributes:
                arc_attrs = solution_data["arcs"].get(tmp_arc, {})
            else:
                tmp_arc_data = solution_data["arcs"][tmp_arc]
                arc_attrs = {
                    'q' if mathematical_var_names else 'flow': f'{   tmp_arc_data["massflowLb"]:.2f}\n<= {tmp_arc_data["flow"]:.2f}\n<= {tmp_arc_data["massflowUb"]:.2f}'
                }
            color = "red" if interdiction.get(tmp_arc, 0.0) == 1.0 else "black"
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
        nx.draw_networkx_labels(interdicted_network, pos, labels=node_labels, font_size=8)

        # Draw edge labels with attributes
        edge_labels = {
            (u, v): "\n".join([f"{k}: {v}" for k, v in attrs.items() if k not in ['color']])
            for u, v, attrs in interdicted_network.edges(data=True)
        }
        nx.draw_networkx_edge_labels(interdicted_network, pos, edge_labels=edge_labels, font_size=8)

        #TODO: Insert different folders to insert the plots into
        plt.savefig("./myfile.pdf", format='pdf')
        
        plt.show()


    plot_solution(network, f'./logs/{mode}/SOL/intBudget_{Budget}_instance_{networkInstanceName}.sol', optimal_interdiction_decision, False, True)
    
    #print(result)


p = multiprocessing.Process(target=run_method, args=(mode, pyomoData, networkInstanceName, Budget))
p.start()

# Wait for 3600 seconds (1 hour)
p.join(timeout=3600)

# Terminate the process if it's still running
if p.is_alive():
    p.terminate()
    print("Method execution timed out after 3600 seconds.")
else:
    print("Method executed successfully within 3600 seconds.")
