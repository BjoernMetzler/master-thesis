from gurobipy import *
import sys
import csv
import time 

class Single_Level_Formulation:
    def __init__(self, data: dict, networkInstanceName: str, with_loadflow_non_negative: bool, budget: int):
        self.m = Model(f"{networkInstanceName}")
        self.m.setParam('TimeLimit', 3600)
        self.m.setParam('OutputFlag', 0)
        self.with_loadflow_non_negative = with_loadflow_non_negative
        
        self.nodes_list = data["nodes"][None]
        self.arcs_list = data["arcs"][None]
        self.interdictionBudget_int = budget
        self.activeElements_list = data["activeElements"][None]
        self.entry_nodes_list = [node for node in data["sigma"].keys() if data["sigma"][node] > 0]
        self.exit_nodes_list = [node for node in data["sigma"].keys() if data["sigma"][node] < 0]
        self.inner_nodes_list = [node for node in self.nodes_list if node not in self.exit_nodes_list + self.entry_nodes_list]
        self.sigma_at_nodes_dict = {**data["sigma"], **{node: 0 for node in self.inner_nodes_list}}        
        self.loadflow_at_nodes_dict = {**data["loadflow"], **{node: 0.0 for node in self.inner_nodes_list}}
        
        #loadflow > 0
        if self.with_loadflow_non_negative:
            for node in self.nodes_list:
                if self.loadflow_at_nodes_dict[node] == 0.0:
                    self.loadflow_at_nodes_dict[node] = 10e-6
                
        self.WCloadflow_at_nodes_dict = data["weaklyConnectedLoadflow"]
        
        # TODO: Müssen für 0.0 Einträge ebenfalls Nebenbedingungen erfüllt werden? Da pressureLossFactor > 0 nach Paper
        self.pressureLossFactor_at_arcs_dict = data["pressureLossFactor"]
    
        self.pressureBounds_at_nodes_dict_dict = {"LB": data["pressureLb"],
                                                  "UB": data["pressureUb"]}
                
        self.loadshedBounds_at_nodes_dict_dict = {"LB": {**data["loadshedLB"], **{node: 0.0 for node in self.inner_nodes_list}},
                                                  "UB": {**{node: 1.0 for node in self.nodes_list if node not in self.inner_nodes_list}, 
                                                         **{node: 0.0 for node in self.inner_nodes_list}}}
        self.massflowBounds_at_arcs_dict_dict = {"LB": data["massflowLb"],
                                                 "UB": data["massflowUb"]}
        # PDAI: Potential Decoupling After Interdiction
        '''self.PDAIBounds_at_arcs_dict_dict = {"LB": {arc: interdictionDecision[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]) for arc in self.arcs_list},
                                             "UB": {arc: interdictionDecision[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]) for arc in self.arcs_list}}
        self.flowBounds_at_arcs_dict_dict = {"LB": {arc: (1.0 - self.interdiction[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc] for arc in self.arcs_list},
                                            "UB": {arc: (1.0 - self.interdiction[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] for arc in self.arcs_list}}
'''

    def adjacent_arcs_as_list(self, node: str, in_or_out: str):
        if "in" == in_or_out.lower():
            return [arc for arc in self.arcs_list if arc[1] == node]
        if "out" == in_or_out.lower():
            return [arc for arc in self.arcs_list if arc[0] == node]
        return []


    def add_WCcheck_constraints(self):
        self.WCcheck_flow_var_at_arcs = self.m.addVars(self.arcs_list, lb=-float("inf"), ub=float("inf"),name ="WCcheckFlow",vtype=GRB.CONTINUOUS)
        self.WCcheck_constraints = self.m.addConstrs(
            (
                quicksum(
                    self.WCcheck_flow_var_at_arcs[arc]
                    for arc in self.adjacent_arcs_as_list(node, "out")
                )
                - quicksum(
                    self.WCcheck_flow_var_at_arcs[arc]
                    for arc in self.adjacent_arcs_as_list(node, "in")
                )
                == self.WCloadflow_at_nodes_dict[node]
                for node in self.nodes_list
            ),
            name="WCcheck_constraints"
        )
        self.m.addConstrs(self.interdiction_var_at_arcs[arc] * self.WCcheck_flow_var_at_arcs[arc] == 0.0 for arc in self.arcs_list)
      
                
    def add_primal_feasibility_constraints(self):
        # Loadshed-Variable inklusive Beschränkungen für jeden Knoten
        self.loadshed_var_at_nodes = self.m.addVars(self.nodes_list, lb=self.loadshedBounds_at_nodes_dict_dict["LB"], ub=self.loadshedBounds_at_nodes_dict_dict["UB"], vtype=GRB.CONTINUOUS, name="loadshed")

        # Flow variables with bounds for each arc
        self.flow_var_at_arcs = self.m.addVars(self.arcs_list, lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="flow")

        # Pressure variables with bounds for each node
        self.pressure_var_at_nodes = self.m.addVars(self.nodes_list, lb=self.pressureBounds_at_nodes_dict_dict["LB"], ub=self.pressureBounds_at_nodes_dict_dict["UB"], vtype=GRB.CONTINUOUS, name="pressure")

        # Interdiction Variable
        self.interdiction_var_at_arcs = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="interdiction")

        # PDAI: Potential Decoupling After Interdiction Constraints
        PC_PDAI_lower_at_arcs = self.m.addConstrs((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc] >= self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]) for arc in self.arcs_list), name="PDAI_lower")
        PC_PDAI_upper_at_arcs = self.m.addConstrs((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc] <= self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]) for arc in self.arcs_list), name="PDAI_upper")
        
        # Flow conservation at nodes
        PC_flow_conservation_at_nodes = self.m.addConstrs((quicksum(self.flow_var_at_arcs[arc] for arc in self.adjacent_arcs_as_list(node,"out")) - quicksum(self.flow_var_at_arcs[arc] for arc in self.adjacent_arcs_as_list(node, "in")) == self.sigma_at_nodes_dict[node] * (1.0 - self.loadshed_var_at_nodes[node]) * self.loadflow_at_nodes_dict[node] for node in self.nodes_list), name="flow_conservation")

        PC_flow_lower_at_arcs = self.m.addConstrs(((1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc] <= self.flow_var_at_arcs[arc] for arc in self.arcs_list), name="flow_lower")
        PC_flow_upper_at_arcs = self.m.addConstrs(((1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] >= self.flow_var_at_arcs[arc] for arc in self.arcs_list), name="flow_upper")
  
    
    def add_dual_feasibility_constraints(self):
        # TODO: Testen der Dualen Variablen
        # beschränkte Dual-Variablen (zu primalen Ungleichungsnebenbedingungen)
        self.dual_flow_var_at_arcs_lower = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_flow_lower")
        self.dual_flow_var_at_arcs_upper = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_flow_upper")

        self.dual_PDAI_var_at_arcs_lower = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_PDAI_lower")
        self.dual_PDAI_var_at_arcs_upper = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_PDAI_upper")

        self.dual_pressure_var_at_nodes_lower = self.m.addVars(self.nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_pressure_lower")
        self.dual_pressure_var_at_nodes_upper = self.m.addVars(self.nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_pressure_upper")

        self.dual_loadshed_var_at_exit_nodes_lower = self.m.addVars(self.exit_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_exit_lower")
        self.dual_loadshed_var_at_exit_nodes_upper = self.m.addVars(self.exit_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_exit_upper")

        self.dual_loadshed_var_at_entry_nodes_lower = self.m.addVars(self.entry_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_entry_lower")
        self.dual_loadshed_var_at_entry_nodes_upper = self.m.addVars(self.entry_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_entry_upper")

        # unbeschränkte Dual-Variablen (zu primalen Gleichheitsnebenbedingungen)
        self.dual_flowConservation_var_at_nodes = self.m.addVars(self.nodes_list, lb=-float("inf"), ub=float("inf"), vtype=GRB.CONTINUOUS, name="dual_flowConservation")
        
        # EnNdfC: Entry node dual feasibility constraint
        DC_loadshed_at_entry_nodes = self.m.addConstrs((- self.dual_flowConservation_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] - self.dual_loadshed_var_at_entry_nodes_lower[node] + self.dual_loadshed_var_at_entry_nodes_upper[node] == 0.0 for node in self.entry_nodes_list), name="EnNdfC")

        # ExNdfC: Exit node dual feasibility constraint
        DC_loadshed_at_exit_nodes = self.m.addConstrs((self.loadflow_at_nodes_dict[node] + self.dual_flowConservation_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] - self.dual_loadshed_var_at_exit_nodes_lower[node] + self.dual_loadshed_var_at_exit_nodes_upper[node] == 0.0  for node in self.exit_nodes_list), name="ExNdfC")

        # Arc(without circle)dfC: Arc dual feasibility constraint
        DC_WOCircle_at_arcs = self.m.addConstrs((- self.dual_flowConservation_var_at_nodes[arc[0]] + self.dual_flowConservation_var_at_nodes[arc[1]] - self.dual_flow_var_at_arcs_lower[arc] + self.dual_flow_var_at_arcs_upper[arc] + self.dual_PDAI_var_at_arcs_lower[arc] * self.pressureLossFactor_at_arcs_dict[arc] - self.dual_PDAI_var_at_arcs_upper[arc] * self.pressureLossFactor_at_arcs_dict[arc] == 0.0 for arc in self.arcs_list if arc[0] != arc[1]), name="ArcdfC")

        # NodedfC: Node dual feasibility constraint
        DC_at_nodes = self.m.addConstrs((quicksum(self.dual_PDAI_var_at_arcs_upper[arc] - self.dual_PDAI_var_at_arcs_lower[arc] for arc in self.adjacent_arcs_as_list(node, "out")) - quicksum(self.dual_PDAI_var_at_arcs_upper[arc] - self.dual_PDAI_var_at_arcs_lower[arc] for arc in self.adjacent_arcs_as_list(node, "in")) + self.dual_pressure_var_at_nodes_upper[node] - self.dual_pressure_var_at_nodes_lower[node] == 0.0 for node in self.nodes_list), name="NodedfC")


    def add_SOS1(self):
        # Transforming the constraints into SOS1 constraints
        '''for arc in self.arcs_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_lower[arc], self.flow_var_at_arcs[arc] - (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_upper[arc], (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_lower[arc], (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]))])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_upper[arc], (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc])])
'''
        #replaced by 
        # Create auxiliary variables
        aux_vars_lower = {}
        aux_vars_upper = {}
        aux_vars_pdai_lower = {}
        aux_vars_pdai_upper = {}

        for arc in self.arcs_list:
            aux_vars_lower[arc] = self.m.addVar(name=f"aux_var_lower_{arc}")
            aux_vars_upper[arc] = self.m.addVar(name=f"aux_var_upper_{arc}")
            aux_vars_pdai_lower[arc] = self.m.addVar(name=f"aux_var_pdai_lower_{arc}")
            aux_vars_pdai_upper[arc] = self.m.addVar(name=f"aux_var_pdai_upper_{arc}")

        # Add constraints to define the auxiliary variables
        for arc in self.arcs_list:
            self.m.addConstr(aux_vars_lower[arc] == self.flow_var_at_arcs[arc] - (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc], name=f"aux_constr_lower_{arc}")
            self.m.addConstr(aux_vars_upper[arc] == (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc], name=f"aux_constr_upper_{arc}")
            self.m.addConstr(aux_vars_pdai_lower[arc] == (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]])), name=f"aux_constr_pdai_lower_{arc}")
            self.m.addConstr(aux_vars_pdai_upper[arc] == (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]), name=f"aux_constr_pdai_upper_{arc}")

        # Add SOS1 constraints using the auxiliary variables
        for arc in self.arcs_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_lower[arc], aux_vars_lower[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_upper[arc], aux_vars_upper[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_lower[arc], aux_vars_pdai_lower[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_upper[arc], aux_vars_pdai_upper[arc]])


        '''for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_lower[node], self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_upper[node], self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]])

        for node in self.exit_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_lower[node], self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_upper[node], self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]])

        for node in self.entry_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_lower[node], self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_upper[node], self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]])
'''
        ## Replaced by
        # Create auxiliary variables
        aux_vars_pressure_lower = {}
        aux_vars_pressure_upper = {}
        aux_vars_loadshed_exit_lower = {}
        aux_vars_loadshed_exit_upper = {}
        aux_vars_loadshed_entry_lower = {}
        aux_vars_loadshed_entry_upper = {}

        for node in self.nodes_list:
            aux_vars_pressure_lower[node] = self.m.addVar(name=f"aux_var_pressure_lower_{node}")
            aux_vars_pressure_upper[node] = self.m.addVar(name=f"aux_var_pressure_upper_{node}")

        for node in self.exit_nodes_list:
            aux_vars_loadshed_exit_lower[node] = self.m.addVar(name=f"aux_var_loadshed_exit_lower_{node}")
            aux_vars_loadshed_exit_upper[node] = self.m.addVar(name=f"aux_var_loadshed_exit_upper_{node}")

        for node in self.entry_nodes_list:
            aux_vars_loadshed_entry_lower[node] = self.m.addVar(name=f"aux_var_loadshed_entry_lower_{node}")
            aux_vars_loadshed_entry_upper[node] = self.m.addVar(name=f"aux_var_loadshed_entry_upper_{node}")

        # Add constraints to define the auxiliary variables
        for node in self.nodes_list:
            self.m.addConstr(aux_vars_pressure_lower[node] == self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node], name=f"aux_constr_pressure_lower_{node}")
            self.m.addConstr(aux_vars_pressure_upper[node] == self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node], name=f"aux_constr_pressure_upper_{node}")

        for node in self.exit_nodes_list:
            self.m.addConstr(aux_vars_loadshed_exit_lower[node] == self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node], name=f"aux_constr_loadshed_exit_lower_{node}")
            self.m.addConstr(aux_vars_loadshed_exit_upper[node] == self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node], name=f"aux_constr_loadshed_exit_upper_{node}")

        for node in self.entry_nodes_list:
            self.m.addConstr(aux_vars_loadshed_entry_lower[node] == self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node], name=f"aux_constr_loadshed_entry_lower_{node}")
            self.m.addConstr(aux_vars_loadshed_entry_upper[node] == self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node], name=f"aux_constr_loadshed_entry_upper_{node}")

        # Add SOS1 constraints using the auxiliary variables
        for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_lower[node], aux_vars_pressure_lower[node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_upper[node], aux_vars_pressure_upper[node]])

        for node in self.exit_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_lower[node], aux_vars_loadshed_exit_lower[node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_upper[node], aux_vars_loadshed_exit_upper[node]])

        for node in self.entry_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_lower[node], aux_vars_loadshed_entry_lower[node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_upper[node], aux_vars_loadshed_entry_upper[node]])

    def add__complementary_constraints(self):
        CC_dual_flow_var_at_arcs_lower = self.m.addConstrs((self.dual_flow_var_at_arcs_lower[arc] * (self.flow_var_at_arcs[arc] - (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc]) == 0.0 for arc in self.arcs_list), name="CC_dual_flow_var_at_arcs_lower")
        CC_dual_flow_var_at_arcs_upper = self.m.addConstrs((self.dual_flow_var_at_arcs_upper[arc] * ((1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc]) == 0.0 for arc in self.arcs_list), name="CC_dual_flow_var_at_arcs_upper")
        CC_dual_PDAI_var_at_arcs_lower = self.m.addConstrs((self.dual_PDAI_var_at_arcs_lower[arc] * ((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]))) == 0.0 for arc in self.arcs_list), name="CC_dual_PDAI_var_at_arcs_lower")
        CC_dual_PDAI_var_at_arcs_upper = self.m.addConstrs((self.dual_PDAI_var_at_arcs_upper[arc] * ((self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc])) == 0.0 for arc in self.arcs_list), name="CC_dual_PDAI_var_at_arcs_upper")
        CC_dual_pressure_var_at_nodes_lower = self.m.addConstrs((self.dual_pressure_var_at_nodes_lower[node] * (self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]) == 0.0 for node in self.nodes_list), name="CC_dual_pressure_var_at_nodes_lower")
        CC_dual_pressure_var_at_nodes_upper = self.m.addConstrs((self.dual_pressure_var_at_nodes_upper[node] * (self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]) == 0.0 for node in self.nodes_list), name="CC_dual_pressure_var_at_nodes_upper")
        CC_dual_loadshed_var_at_exit_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_lower[node] * (self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]) == 0.0 for node in self.exit_nodes_list), name="CC_dual_loadshed_var_at_exit_nodes_lower")
        CC_dual_loadshed_var_at_exit_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_upper[node] * (self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]) == 0.0 for node in self.exit_nodes_list), name="CC_dual_loadshed_var_at_exit_nodes_upper")
        CC_dual_loadshed_var_at_entry_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_lower[node] * (self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]) == 0.0 for node in self.entry_nodes_list), name="CC_dual_loadshed_var_at_entry_nodes_lower")
        CC_dual_loadshed_var_at_entry_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_upper[node] * (self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]) == 0.0 for node in self.entry_nodes_list), name="CC_dual_loadshed_var_at_entry_nodes_upper")

    def add_CC_bigM_reformulation(self):
        # binäre Hilfsvariablen für bigM-Reformulierung der Komplementaritätsbedingungen
        self.binary_var_for__dual_flow_var_at_arcs_lower = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_flow_var_at_arcs_lower")
        self.binary_var_for__dual_flow_var_at_arcs_upper = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_flow_var_at_arcs_upper")
        self.binary_var_for__dual_PDAI_var_at_arcs_lower = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_PDAI_var_at_arcs_lower")
        self.binary_var_for__dual_PDAI_var_at_arcs_upper = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_PDAI_var_at_arcs_upper")
        self.binary_var_for__dual_pressure_var_at_nodes_lower = self.m.addVars(self.nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_pressure_var_at_nodes_lower")
        self.binary_var_for__dual_pressure_var_at_nodes_upper = self.m.addVars(self.nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_pressure_var_at_nodes_upper")
        self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower = self.m.addVars(self.exit_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_exit_nodes_lower")
        self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper = self.m.addVars(self.exit_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_exit_nodes_upper")
        self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower = self.m.addVars(self.entry_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_entry_nodes_lower")
        self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper = self.m.addVars(self.entry_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_entry_nodes_upper")


        # bigM-Werte für primale Ungleichungsnebenbedingungen
        self.bigM_for__flow_var_at_arcs_lower = max([self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.massflowBounds_at_arcs_dict_dict["LB"][arc] for arc in self.arcs_list])
        self.bigM_for__flow_var_at_arcs_upper = self.bigM_for__flow_var_at_arcs_lower

        self.bigM_for__PDAI_var_at_arcs_lower = max([self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] + self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]] for arc in self.arcs_list if arc[0] != arc[1]])
        self.bigM_for__PDAI_var_at_arcs_upper = self.bigM_for__PDAI_var_at_arcs_lower


        self.bigM_for__pressure_var_at_nodes_lower = max([self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressureBounds_at_nodes_dict_dict["LB"][node] for node in self.nodes_list]) 
        self.bigM_for__pressure_var_at_nodes_upper = self.bigM_for__pressure_var_at_nodes_lower

        self.bigM_for__loadshed_var_at_exit_nodes_lower = 1.0
        self.bigM_for__loadshed_var_at_exit_nodes_upper = self.bigM_for__loadshed_var_at_exit_nodes_lower

        self.bigM_for__loadshed_var_at_entry_nodes_lower = max([1.0 - self.loadshedBounds_at_nodes_dict_dict["LB"][node] for node in self.entry_nodes_list])
        self.bigM_for__loadshed_var_at_entry_nodes_upper = self.bigM_for__loadshed_var_at_entry_nodes_lower

        #bigM values Dualvariablen     
        
        self.bigM_for__dual_flow_var_at_arcs_lower = 1.0
        self.bigM_for__dual_flow_var_at_arcs_upper = self.bigM_for__dual_flow_var_at_arcs_lower
        #print(self.bigM_for__dual_flow_var_at_arcs_lower)
        ## TODO: Try different modeling approach for the PDAI_var boundaries in combination with the pressure bounds. (see Paper)
        self.bigM_for__dual_PDAI_var_at_arcs_lower = max([GRB.INFINITY if self.pressureLossFactor_at_arcs_dict[arc] == 0.0 else 1.0 / self.pressureLossFactor_at_arcs_dict[arc] for arc in self.arcs_list])
        self.bigM_for__dual_PDAI_var_at_arcs_upper = self.bigM_for__dual_PDAI_var_at_arcs_lower
        #print(self.bigM_for__dual_PDAI_var_at_arcs_lower)
        self.bigM_for__dual_pressure_var_at_nodes_lower = max([((len(self.adjacent_arcs_as_list(node,"out") + self.adjacent_arcs_as_list(node, "in")) * self.bigM_for__dual_PDAI_var_at_arcs_upper)) for node in self.nodes_list])
        self.bigM_for__dual_pressure_var_at_nodes_upper = self.bigM_for__dual_pressure_var_at_nodes_lower 
        #print(self.bigM_for__dual_pressure_var_at_nodes_upper)
        self.bigM_for__dual_loadshed_var_at_entry_nodes_lower = max([self.loadflow_at_nodes_dict[node] for node in self.nodes_list])#1.0
        self.bigM_for__dual_loadshed_var_at_entry_nodes_upper = self.bigM_for__dual_loadshed_var_at_entry_nodes_lower
        #print(self.bigM_for__dual_loadshed_var_at_entry_nodes_lower)
        self.bigM_for__dual_loadshed_var_at_exit_nodes_lower = 2*self.bigM_for__dual_loadshed_var_at_entry_nodes_lower#max([self.loadflow_at_nodes_dict[node] * (1.0 + max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list]))) for node in self.exit_nodes_list])
        self.bigM_for__dual_loadshed_var_at_exit_nodes_upper = self.bigM_for__dual_loadshed_var_at_exit_nodes_lower 
        #print(self.bigM_for__dual_loadshed_var_at_exit_nodes_lower)
    
        self.m.addConstrs(self.dual_flowConservation_var_at_nodes[node] <= 1 for node in self.nodes_list) #max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list])) for node in self.nodes_list)
        self.m.addConstrs(self.dual_flowConservation_var_at_nodes[node] >= - 1 for node in self.nodes_list) #max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list])) for node in self.nodes_list)

        # obere Schranken für abwärts beschränkte Dual-Variablen
        UB_bigM_for__dual_flow_var_at_arcs_lower = self.m.addConstrs((self.dual_flow_var_at_arcs_lower[arc] <= self.bigM_for__dual_flow_var_at_arcs_lower * self.binary_var_for__dual_flow_var_at_arcs_lower[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_flow_var_at_arcs_lower")
        UB_bigM_for__dual_flow_var_at_arcs_upper = self.m.addConstrs((self.dual_flow_var_at_arcs_upper[arc] <= self.bigM_for__dual_flow_var_at_arcs_upper * self.binary_var_for__dual_flow_var_at_arcs_upper[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_flow_var_at_arcs_upper")

        UB_bigM_for__dual_PDAI_var_at_arcs_lower = self.m.addConstrs((self.dual_PDAI_var_at_arcs_lower[arc] <= self.bigM_for__dual_PDAI_var_at_arcs_lower * self.binary_var_for__dual_PDAI_var_at_arcs_lower[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_PDAI_var_at_arcs_lower")
        UB_bigM_for__dual_PDAI_var_at_arcs_upper = self.m.addConstrs((self.dual_PDAI_var_at_arcs_upper[arc] <= self.bigM_for__dual_PDAI_var_at_arcs_upper * self.binary_var_for__dual_PDAI_var_at_arcs_upper[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_PDAI_var_at_arcs_upper")

        ## WENN PRESSURE_LOSS = 0, kann man dann nicht einfach die angrenzenden Knoten als einen Knoten betrachten und zusammenlegen
        UB_bigM_for__dual_pressure_var_at_nodes_lower = self.m.addConstrs((self.dual_pressure_var_at_nodes_lower[node] <= self.bigM_for__dual_pressure_var_at_nodes_lower * self.binary_var_for__dual_pressure_var_at_nodes_lower[node] for node in self.nodes_list), name="UB_bigM_for__dual_pressure_var_at_nodes_lower")
        UB_bigM_for__dual_pressure_var_at_nodes_upper = self.m.addConstrs((self.dual_pressure_var_at_nodes_upper[node] <= self.bigM_for__dual_pressure_var_at_nodes_upper * self.binary_var_for__dual_pressure_var_at_nodes_upper[node] for node in self.nodes_list), name="UB_bigM_for__dual_pressure_var_at_nodes_upper")

        UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_lower[node] <= self.bigM_for__dual_loadshed_var_at_exit_nodes_lower * self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower[node] for node in self.exit_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower")
        UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_upper[node] <= self.bigM_for__dual_loadshed_var_at_exit_nodes_upper * self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper[node] for node in self.exit_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper")

        UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_lower[node] <= self.bigM_for__dual_loadshed_var_at_entry_nodes_lower * self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower[node] for node in self.entry_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower")
        UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_upper[node] <= self.bigM_for__dual_loadshed_var_at_entry_nodes_upper * self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper[node] for node in self.entry_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper")

        
        # obere Schranken für primale Ungleichungsnebenbedingungen zu den Dualvariablen
        UB_for__flow_var_at_arcs_lower = self.m.addConstrs((self.flow_var_at_arcs[arc] - (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc] <= (1.0 - self.binary_var_for__dual_flow_var_at_arcs_lower[arc]) * self.bigM_for__flow_var_at_arcs_lower for arc in self.arcs_list), name = "UB_for__flow_var_at_arcs_lower")
        UB_for__flow_var_at_arcs_upper = self.m.addConstrs(((1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc] <= (1.0 - self.binary_var_for__dual_flow_var_at_arcs_upper[arc]) * self.bigM_for__flow_var_at_arcs_upper for arc in self.arcs_list), name = "UB_for__flow_var_at_arcs_upper")

        UB_for__PDAI_var_at_arcs_lower = self.m.addConstrs(((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]])) <= (1.0 - self.binary_var_for__dual_PDAI_var_at_arcs_lower[arc]) * self.bigM_for__PDAI_var_at_arcs_lower for arc in self.arcs_list), name = "UB_for__PDAI_var_at_arcs_lower")
        UB_for__PDAI_var_at_arcs_upper = self.m.addConstrs(((self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) <= (1.0 - self.binary_var_for__dual_PDAI_var_at_arcs_upper[arc]) * self.bigM_for__PDAI_var_at_arcs_upper for arc in self.arcs_list), name = "UB_for__PDAI_var_at_arcs_upper")
        
        UB_for__pressure_var_at_nodes_lower = self.m.addConstrs((self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node] <= (1.0 - self.binary_var_for__dual_pressure_var_at_nodes_lower[node]) * self.bigM_for__pressure_var_at_nodes_lower for node in self.nodes_list), name = "UB_for__pressure_var_at_nodes_lower") 
        UB_for__pressure_var_at_nodes_upper = self.m.addConstrs((self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node] <= (1.0 - self.binary_var_for__dual_pressure_var_at_nodes_upper[node]) * self.bigM_for__pressure_var_at_nodes_upper for node in self.nodes_list), name = "UB_for__pressure_var_at_nodes_upper")
        
        UB_for__loadshed_var_at_exit_nodes_lower = self.m.addConstrs((self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower[node]) * self.bigM_for__loadshed_var_at_exit_nodes_lower for node in self.exit_nodes_list), name = "UB_for__loadshed_var_at_exit_nodes_lower")
        UB_for__loadshed_var_at_exit_nodes_upper = self.m.addConstrs((self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper[node]) * self.bigM_for__loadshed_var_at_exit_nodes_upper for node in self.exit_nodes_list), name = "UB_for__loadshed_var_at_exit_nodes_upper")

        UB_for__loadshed_var_at_entry_nodes_lower = self.m.addConstrs((self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower[node]) * self.bigM_for__loadshed_var_at_entry_nodes_lower for node in self.entry_nodes_list), name = "UB_for__loadshed_var_at_entry_nodes_lower")
        UB_for__loadshed_var_at_entry_nodes_upper = self.m.addConstrs((self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper[node]) * self.bigM_for__loadshed_var_at_entry_nodes_upper for node in self.entry_nodes_list), name = "UB_for__loadshed_var_at_entry_nodes_upper")
    
    
    def test_feasibility_for_given_solution(self, sol_file_path):
        def read_input_file(file_path):
            data = {}
            data["arcs"] = {}
            data["nodes"] = {}
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith('#') or line.strip() == '':
                        continue
                    parts = line.split()
                    key = parts[0]
                    value = float(parts[1])
                    if '[' in key and ']' in key:
                        var_name, nodes = key.split('[')
                        nodes = nodes.strip(']')
                        if ',' in nodes:
                            node_tuple = tuple(nodes.split(','))
                            data["arcs"][(node_tuple, var_name)] = value
                        else:
                            data["nodes"][(nodes, var_name)] = value
            return data
        
        sol_file_data = read_input_file(sol_file_path)
        
        ## assuming that we match the right models for feasibility
        ## further assuming that the important vars exist on both sides
        
        for key, value in sol_file_data["arcs"].items():
            arc, var_name = key
            #print(f"arc: {arc}\n var_name: {var_name} \n value: {value}")
            try:
                variable = self.m.getVarByName(f"{var_name}[{arc[0]},{arc[1]}]")
            except:
                print("failed")
                continue
            # Adding the constraint
            self.m.addConstr(variable == value, name=f"comp_constr_{var_name}_{arc}")
        
        for key, value in sol_file_data["nodes"].items():
            node, var_name = key
            #print(f"node: {node}\n var_name: {var_name} \n value: {value}")
            try:
                variable = self.m.getVarByName(f"{var_name}[{node}]")
            except:
                print("failed")
                continue
            # Adding the constraint
            self.m.addConstr(variable == value, name=f"comp_constr_{var_name}_{node}")
            
        
    def single_level_model_SOS1(self):
        self.add_primal_feasibility_constraints()
        self.add_dual_feasibility_constraints()
        self.add_SOS1()
        self.add_WCcheck_constraints()
        self.m.addConstr(quicksum(self.interdiction_var_at_arcs[arc] for arc in self.arcs_list) <= self.interdictionBudget_int)
        self.m.setObjective(quicksum(self.loadshed_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] for node in self.exit_nodes_list),GRB.MAXIMIZE)
        self.m.optimize()
        self.m.write("single_level_model_SOS1.sol")
        self.m.write("single_level_model_SOS1.lp")
        self.m.ObjVal
        objVal = 0
        interdiction = {}
        for v in self.m.getVars():
            for n in self.exit_nodes_list:
                if f"loadshed[{n}]" in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
            for a in self.arcs_list:
                if f"interdiction[{a[0]},{a[1]}]" in v.VarName:
                    interdiction[a] = int(v.X)
        print(interdiction)
        return {"interdiction": interdiction, "objVal": objVal, "Runtime": self.m.Runtime}
        
        
    def single_level_model_CC(self):
        self.add_primal_feasibility_constraints()
        self.add_dual_feasibility_constraints()
        self.add__complementary_constraints()
        self.add_WCcheck_constraints()
        self.m.addConstr(quicksum(self.interdiction_var_at_arcs[arc] for arc in self.arcs_list) <= self.interdictionBudget_int)
        self.m.setObjective(quicksum(self.loadshed_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] for node in self.exit_nodes_list),GRB.MAXIMIZE)
        self.m.optimize()
        self.m.write("single_level_model_CC.sol")
        self.m.ObjVal
        self.m.ObjVal
        objVal = 0
        interdiction = {}
        for v in self.m.getVars():
            for n in self.exit_nodes_list:
                if f"loadshed[{n}]" in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
            for a in self.arcs_list:
                if f"interdiction[{a[0]},{a[1]}]" in v.VarName:
                    interdiction[a] = int(v.X)
        return {"interdiction": interdiction, "objVal": objVal, "Runtime": self.m.Runtime}
   
        
    def single_level_model_BigM(self):
        self.add_primal_feasibility_constraints()
        self.add_dual_feasibility_constraints()
        self.add_CC_bigM_reformulation()
        self.add_WCcheck_constraints()
        self.m.addConstr(quicksum(self.interdiction_var_at_arcs[arc] for arc in self.arcs_list) <= self.interdictionBudget_int)
        self.m.setObjective(quicksum(self.loadshed_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] for node in self.exit_nodes_list),GRB.MAXIMIZE)
        self.m.optimize()
        #self.test_feasibility_for_given_solution("bigmmodel_mode_False.sol")
        self.m.optimize()
        self.m.write("single_level_model_BigM.lp")
        self.m.write("single_level_model_BigM.sol")
        self.m.ObjVal
        self.m.ObjVal
        objVal = 0
        interdiction = {}
        for v in self.m.getVars():
            for n in self.exit_nodes_list:
                if f"loadshed[{n}]" in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
            for a in self.arcs_list:
                if f"interdiction[{a[0]},{a[1]}]" in v.VarName:
                    interdiction[a] = int(v.X)
        return {"interdiction": interdiction, "objVal": objVal, "Runtime": self.m.Runtime}
    

class FollowerModel_WithInterdictionInput:
    def __init__(self, data: dict, interdictionDecision: dict, networkInstanceName: str, with_loadflow_non_negative: bool):
        self.m = Model(f"{networkInstanceName}" + f"{interdictionDecision}")
        self.m.setParam('TimeLimit', 3600)
        self.m.setParam('OutputFlag', 0)
        self.with_loadflow_non_negative = with_loadflow_non_negative
        
        self.nodes_list = data["nodes"][None]
        self.arcs_list = data["arcs"][None]
        # TODO: Ggf. Konvertierung von Gurobi-Interdiction-Vars aus Upper-Level in lesbare Zahlen für Lower-Level
        self.interdiction = interdictionDecision
        self.interdictionBudget_int = data["interdictionBudget"][None]
        self.activeElements_list = data["activeElements"][None]
        self.entry_nodes_list = [node for node in data["sigma"].keys() if data["sigma"][node] > 0]
        self.exit_nodes_list = [node for node in data["sigma"].keys() if data["sigma"][node] < 0]
        self.inner_nodes_list = [node for node in self.nodes_list if node not in self.exit_nodes_list + self.entry_nodes_list]
        self.sigma_at_nodes_dict = {**data["sigma"], **{node: 0 for node in self.inner_nodes_list}}        
        self.loadflow_at_nodes_dict = {**data["loadflow"], **{node: 0.0 for node in self.inner_nodes_list}}
        
        #loadflow > 0
        if self.with_loadflow_non_negative:
            for node in self.nodes_list:
                if self.loadflow_at_nodes_dict[node] == 0.0:
                    self.loadflow_at_nodes_dict[node] = 10e-6
                
        self.WCloadflow_at_nodes_dict = data["weaklyConnectedLoadflow"]
        
        # TODO: Müssen für 0.0 Einträge ebenfalls Nebenbedingungen erfüllt werden? Da pressureLossFactor > 0 nach Paper
        self.pressureLossFactor_at_arcs_dict = data["pressureLossFactor"]
    
        self.pressureBounds_at_nodes_dict_dict = {"LB": data["pressureLb"],
                                                  "UB": data["pressureUb"]}
                
        self.loadshedBounds_at_nodes_dict_dict = {"LB": {**data["loadshedLB"], **{node: 0.0 for node in self.inner_nodes_list}},
                                                  "UB": {**{node: 1.0 for node in self.nodes_list if node not in self.inner_nodes_list}, 
                                                         **{node: 0.0 for node in self.inner_nodes_list}}}
        self.massflowBounds_at_arcs_dict_dict = {"LB": data["massflowLb"],
                                                 "UB": data["massflowUb"]}
        # PDAI: Potential Decoupling After Interdiction
        self.PDAIBounds_at_arcs_dict_dict = {"LB": {arc: interdictionDecision[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]) for arc in self.arcs_list},
                                             "UB": {arc: interdictionDecision[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]) for arc in self.arcs_list}}
        self.flowBounds_at_arcs_dict_dict = {"LB": {arc: (1.0 - self.interdiction[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc] for arc in self.arcs_list},
                                            "UB": {arc: (1.0 - self.interdiction[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] for arc in self.arcs_list}}

    def adjacent_arcs_as_list(self, node: str, in_or_out: str):
        if "in" == in_or_out.lower():
            return [arc for arc in self.arcs_list if arc[1] == node]
        if "out" == in_or_out.lower():
            return [arc for arc in self.arcs_list if arc[0] == node]
        # TODO: Kann man das so machen? Oder muss hier None/Null hin?
        return []

    def add_WCcheck_constraints(self):
        self.WCcheck_flow_var_at_arcs = self.m.addVars(self.arcs_list, lb=-float("inf"), ub=float("inf"),name ="WCcheckFlow",vtype=GRB.CONTINUOUS)
        self.WCcheck_constraints = self.m.addConstrs(
            (
                quicksum(
                    self.WCcheck_flow_var_at_arcs[arc]
                    for arc in self.adjacent_arcs_as_list(node, "out")
                    if self.interdiction[arc] == 0.0
                )
                - quicksum(
                    self.WCcheck_flow_var_at_arcs[arc]
                    for arc in self.adjacent_arcs_as_list(node, "in")
                    if self.interdiction[arc] == 0.0
                )
                == self.WCloadflow_at_nodes_dict[node]
                for node in self.nodes_list
            ),
            name="WCcheck_constraints",
        )
                
    def add_primal_feasibility_constraints(self):
        # Loadshed-Variable inklusive Beschränkungen für jeden Knoten
        self.loadshed_var_at_nodes = self.m.addVars(self.nodes_list, lb=self.loadshedBounds_at_nodes_dict_dict["LB"], ub=self.loadshedBounds_at_nodes_dict_dict["UB"], vtype=GRB.CONTINUOUS, name="loadshed")

        # Flow variables with bounds for each arc
        self.flow_var_at_arcs = self.m.addVars(self.arcs_list, lb=self.flowBounds_at_arcs_dict_dict["LB"], ub=self.flowBounds_at_arcs_dict_dict["UB"], vtype=GRB.CONTINUOUS, name="flow")

        # Pressure variables with bounds for each node
        self.pressure_var_at_nodes = self.m.addVars(self.nodes_list, lb=self.pressureBounds_at_nodes_dict_dict["LB"], ub=self.pressureBounds_at_nodes_dict_dict["UB"], vtype=GRB.CONTINUOUS, name="pressure")

        # PDAI: Potential Decoupling After Interdiction Constraints
        PC_PDAI_lower_at_arcs = self.m.addConstrs((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc] >= self.PDAIBounds_at_arcs_dict_dict["LB"][arc] for arc in self.arcs_list), name="PDAI_lower")
        PC_PDAI_upper_at_arcs = self.m.addConstrs((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc] <= self.PDAIBounds_at_arcs_dict_dict["UB"][arc] for arc in self.arcs_list), name="PDAI_upper")
        
        # Flow conservation at nodes
        PC_flow_conservation_at_nodes = self.m.addConstrs((quicksum(self.flow_var_at_arcs[arc] for arc in self.adjacent_arcs_as_list(node,"out")) - quicksum(self.flow_var_at_arcs[arc] for arc in self.adjacent_arcs_as_list(node, "in")) == self.sigma_at_nodes_dict[node] * (1.0 - self.loadshed_var_at_nodes[node]) * self.loadflow_at_nodes_dict[node] for node in self.nodes_list), name="flow_conservation")
  
           
    def enum_approach_with_bilevel_formulation(self, withKKT):
        self.add_primal_feasibility_constraints()
        self.add_WCcheck_constraints()
        self.m.optimize()
        
        if withKKT:
            self.add_dual_feasibility_constraints()
            self.add_SOS1()
        if self.m.Status == GRB.INFEASIBLE:
            return [self.interdiction, "infeasible", self.m.Runtime]
        
        self.m.setObjective(quicksum(self.loadshed_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] for node in self.exit_nodes_list),GRB.MINIMIZE)
        self.m.optimize()
        self.m.write("FollowerModel_original.sol")
        if self.m.Status == GRB.INFEASIBLE:
            self.m.computeIIS()
            for c in self.m.getConstrs():
                if c.IISConstr and "WCcheck_constraints" in c.ConstrName:
                    return [self.interdiction, "not weakly connected",self.m.Runtime]
        else:  
            return [self.interdiction, self.m.ObjVal,self.m.Runtime]
        
        
    def add_dual_feasibility_constraints(self):
        # TODO: Testen der Dualen Variablen
        # beschränkte Dual-Variablen (zu primalen Ungleichungsnebenbedingungen)
        self.dual_flow_var_at_arcs_lower = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_flow_lower")
        self.dual_flow_var_at_arcs_upper = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_flow_upper")

        self.dual_PDAI_var_at_arcs_lower = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_PDAI_lower")
        self.dual_PDAI_var_at_arcs_upper = self.m.addVars(self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_PDAI_upper")

        self.dual_pressure_var_at_nodes_lower = self.m.addVars(self.nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_pressure_lower")
        self.dual_pressure_var_at_nodes_upper = self.m.addVars(self.nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_pressure_upper")

        self.dual_loadshed_var_at_exit_nodes_lower = self.m.addVars(self.exit_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_exit_lower")
        self.dual_loadshed_var_at_exit_nodes_upper = self.m.addVars(self.exit_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_exit_upper")

        self.dual_loadshed_var_at_entry_nodes_lower = self.m.addVars(self.entry_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_entry_lower")
        self.dual_loadshed_var_at_entry_nodes_upper = self.m.addVars(self.entry_nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, name="dual_loadshed_entry_upper")

        # unbeschränkte Dual-Variablen (zu primalen Gleichheitsnebenbedingungen)
        self.dual_flowConservation_var_at_nodes = self.m.addVars(self.nodes_list, lb=-float("inf"), ub=float("inf"), vtype=GRB.CONTINUOUS, name="dual_flowConservation")
        
        # EnNdfC: Entry node dual feasibility constraint
        DC_loadshed_at_entry_nodes = self.m.addConstrs((- self.dual_flowConservation_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] - self.dual_loadshed_var_at_entry_nodes_lower[node] + self.dual_loadshed_var_at_entry_nodes_upper[node] == 0.0 for node in self.entry_nodes_list), name="EnNdfC")

        # ExNdfC: Exit node dual feasibility constraint
        DC_loadshed_at_exit_nodes = self.m.addConstrs((self.loadflow_at_nodes_dict[node] + self.dual_flowConservation_var_at_nodes[node] * self.loadflow_at_nodes_dict[node] - self.dual_loadshed_var_at_exit_nodes_lower[node] + self.dual_loadshed_var_at_exit_nodes_upper[node] == 0.0  for node in self.exit_nodes_list), name="ExNdfC")

        # Arc(without circle)dfC: Arc dual feasibility constraint
        DC_WOCircle_at_arcs = self.m.addConstrs((- self.dual_flowConservation_var_at_nodes[arc[0]] + self.dual_flowConservation_var_at_nodes[arc[1]] - self.dual_flow_var_at_arcs_lower[arc] + self.dual_flow_var_at_arcs_upper[arc] + self.dual_PDAI_var_at_arcs_lower[arc] * self.pressureLossFactor_at_arcs_dict[arc] - self.dual_PDAI_var_at_arcs_upper[arc] * self.pressureLossFactor_at_arcs_dict[arc] == 0.0 for arc in self.arcs_list if arc[0] != arc[1]), name="ArcdfC")

        # NodedfC: Node dual feasibility constraint
        DC_at_nodes = self.m.addConstrs((quicksum(self.dual_PDAI_var_at_arcs_upper[arc] - self.dual_PDAI_var_at_arcs_lower[arc] for arc in self.adjacent_arcs_as_list(node, "out")) - quicksum(self.dual_PDAI_var_at_arcs_upper[arc] - self.dual_PDAI_var_at_arcs_lower[arc] for arc in self.adjacent_arcs_as_list(node, "in")) + self.dual_pressure_var_at_nodes_upper[node] - self.dual_pressure_var_at_nodes_lower[node] == 0.0 for node in self.nodes_list), name="NodedfC")

    
    def add_complementarity_constraints(self):
        # TODO: Testen der CC constraint Implementierung
        CC_dual_flow_var_at_arcs_lower = self.m.addConstrs((self.dual_flow_var_at_arcs_lower[arc] * (self.flow_var_at_arcs[arc] - self.flowBounds_at_arcs_dict_dict["LB"][arc]) == 0.0 for arc in self.arcs_list), name="CC_dual_flow_var_at_arcs_lower")
        CC_dual_flow_var_at_arcs_upper = self.m.addConstrs((self.dual_flow_var_at_arcs_upper[arc] * (self.flowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc]) == 0.0 for arc in self.arcs_list), name="CC_dual_flow_var_at_arcs_upper")
        CC_dual_PDAI_var_at_arcs_lower = self.m.addConstrs((self.dual_PDAI_var_at_arcs_lower[arc] * ((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - self.PDAIBounds_at_arcs_dict_dict["LB"][arc]) == 0.0 for arc in self.arcs_list), name="CC_dual_PDAI_var_at_arcs_lower")
        CC_dual_PDAI_var_at_arcs_upper = self.m.addConstrs((self.dual_PDAI_var_at_arcs_upper[arc] * (self.PDAIBounds_at_arcs_dict_dict["UB"][arc] - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc])) == 0.0 for arc in self.arcs_list), name="CC_dual_PDAI_var_at_arcs_upper")
        CC_dual_pressure_var_at_nodes_lower = self.m.addConstrs((self.dual_pressure_var_at_nodes_lower[node] * (self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]) == 0.0 for node in self.nodes_list), name="CC_dual_pressure_var_at_nodes_lower")
        CC_dual_pressure_var_at_nodes_upper = self.m.addConstrs((self.dual_pressure_var_at_nodes_upper[node] * (self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]) == 0.0 for node in self.nodes_list), name="CC_dual_pressure_var_at_nodes_upper")
        CC_dual_loadshed_var_at_exit_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_lower[node] * (self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]) == 0.0 for node in self.exit_nodes_list), name="CC_dual_loadshed_var_at_exit_nodes_lower")
        CC_dual_loadshed_var_at_exit_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_upper[node] * (self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]) == 0.0 for node in self.exit_nodes_list), name="CC_dual_loadshed_var_at_exit_nodes_upper")
        CC_dual_loadshed_var_at_entry_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_lower[node] * (self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]) == 0.0 for node in self.entry_nodes_list), name="CC_dual_loadshed_var_at_entry_nodes_lower")
        CC_dual_loadshed_var_at_entry_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_upper[node] * (self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]) == 0.0 for node in self.entry_nodes_list), name="CC_dual_loadshed_var_at_entry_nodes_upper")

    
    def add_SOS1(self):
        # Transforming the constraints into SOS1 constraints
        '''for arc in self.arcs_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_lower[arc], self.flow_var_at_arcs[arc] - (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_upper[arc], (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_lower[arc], (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]))])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_upper[arc], (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc])])
'''
        #replaced by 
        # Create auxiliary variables
        aux_vars_lower = {}
        aux_vars_upper = {}
        aux_vars_pdai_lower = {}
        aux_vars_pdai_upper = {}

        for arc in self.arcs_list:
            aux_vars_lower[arc] = self.m.addVar(name=f"aux_var_lower_{arc}")
            aux_vars_upper[arc] = self.m.addVar(name=f"aux_var_upper_{arc}")
            aux_vars_pdai_lower[arc] = self.m.addVar(name=f"aux_var_pdai_lower_{arc}")
            aux_vars_pdai_upper[arc] = self.m.addVar(name=f"aux_var_pdai_upper_{arc}")

        # Add constraints to define the auxiliary variables
        for arc in self.arcs_list:
            self.m.addConstr(aux_vars_lower[arc] == self.flow_var_at_arcs[arc] - (1.0 - self.interdiction[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc], name=f"aux_constr_lower_{arc}")
            self.m.addConstr(aux_vars_upper[arc] == (1.0 - self.interdiction[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc], name=f"aux_constr_upper_{arc}")
            self.m.addConstr(aux_vars_pdai_lower[arc] == (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]])), name=f"aux_constr_pdai_lower_{arc}")
            self.m.addConstr(aux_vars_pdai_upper[arc] == (self.interdiction[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]), name=f"aux_constr_pdai_upper_{arc}")

        # Add SOS1 constraints using the auxiliary variables
        for arc in self.arcs_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_lower[arc], aux_vars_lower[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_upper[arc], aux_vars_upper[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_lower[arc], aux_vars_pdai_lower[arc]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_upper[arc], aux_vars_pdai_upper[arc]])


        '''for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_lower[node], self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_upper[node], self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]])

        for node in self.exit_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_lower[node], self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_upper[node], self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]])

        for node in self.entry_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_lower[node], self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_upper[node], self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]])
'''
        ## Replaced by
        # Create auxiliary variables
        aux_vars_pressure_lower = {}
        aux_vars_pressure_upper = {}
        aux_vars_loadshed_exit_lower = {}
        aux_vars_loadshed_exit_upper = {}
        aux_vars_loadshed_entry_lower = {}
        aux_vars_loadshed_entry_upper = {}

        for node in self.nodes_list:
            aux_vars_pressure_lower[node] = self.m.addVar(name=f"aux_var_pressure_lower_{node}")
            aux_vars_pressure_upper[node] = self.m.addVar(name=f"aux_var_pressure_upper_{node}")

        for node in self.exit_nodes_list:
            aux_vars_loadshed_exit_lower[node] = self.m.addVar(name=f"aux_var_loadshed_exit_lower_{node}")
            aux_vars_loadshed_exit_upper[node] = self.m.addVar(name=f"aux_var_loadshed_exit_upper_{node}")

        for node in self.entry_nodes_list:
            aux_vars_loadshed_entry_lower[node] = self.m.addVar(name=f"aux_var_loadshed_entry_lower_{node}")
            aux_vars_loadshed_entry_upper[node] = self.m.addVar(name=f"aux_var_loadshed_entry_upper_{node}")

        # Add constraints to define the auxiliary variables
        for node in self.nodes_list:
            self.m.addConstr(aux_vars_pressure_lower[node] == self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node], name=f"aux_constr_pressure_lower_{node}")
            self.m.addConstr(aux_vars_pressure_upper[node] == self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node], name=f"aux_constr_pressure_upper_{node}")

        for node in self.exit_nodes_list:
            self.m.addConstr(aux_vars_loadshed_exit_lower[node] == self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node], name=f"aux_constr_loadshed_exit_lower_{node}")
            self.m.addConstr(aux_vars_loadshed_exit_upper[node] == self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node], name=f"aux_constr_loadshed_exit_upper_{node}")

        for node in self.entry_nodes_list:
            self.m.addConstr(aux_vars_loadshed_entry_lower[node] == self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node], name=f"aux_constr_loadshed_entry_lower_{node}")
            self.m.addConstr(aux_vars_loadshed_entry_upper[node] == self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node], name=f"aux_constr_loadshed_entry_upper_{node}")

        # Add SOS1 constraints using the auxiliary variables
        for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_lower[node], aux_vars_pressure_lower[node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_upper[node], aux_vars_pressure_upper[node]])

        for node in self.exit_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_lower[node], aux_vars_loadshed_exit_lower[node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_upper[node], aux_vars_loadshed_exit_upper[node]])

        for node in self.entry_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_lower[node], aux_vars_loadshed_entry_lower[node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_upper[node], aux_vars_loadshed_entry_upper[node]])

    
    def add_CC_bigM_reformulation(self):
        # binäre Hilfsvariablen für bigM-Reformulierung der Komplementaritätsbedingungen
        self.binary_var_for__dual_flow_var_at_arcs_lower = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_flow_var_at_arcs_lower")
        self.binary_var_for__dual_flow_var_at_arcs_upper = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_flow_var_at_arcs_upper")
        self.binary_var_for__dual_PDAI_var_at_arcs_lower = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_PDAI_var_at_arcs_lower")
        self.binary_var_for__dual_PDAI_var_at_arcs_upper = self.m.addVars(self.arcs_list, vtype=GRB.BINARY, name="binary_var_for__dual_PDAI_var_at_arcs_upper")
        self.binary_var_for__dual_pressure_var_at_nodes_lower = self.m.addVars(self.nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_pressure_var_at_nodes_lower")
        self.binary_var_for__dual_pressure_var_at_nodes_upper = self.m.addVars(self.nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_pressure_var_at_nodes_upper")
        self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower = self.m.addVars(self.exit_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_exit_nodes_lower")
        self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper = self.m.addVars(self.exit_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_exit_nodes_upper")
        self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower = self.m.addVars(self.entry_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_entry_nodes_lower")
        self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper = self.m.addVars(self.entry_nodes_list, vtype=GRB.BINARY, name="binary_var_for__dual_loadshed_var_at_entry_nodes_upper")


        # bigM-Werte für primale Ungleichungsnebenbedingungen
        self.bigM_for__flow_var_at_arcs_lower = max([self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.massflowBounds_at_arcs_dict_dict["LB"][arc] for arc in self.arcs_list])
        self.bigM_for__flow_var_at_arcs_upper = self.bigM_for__flow_var_at_arcs_lower

        self.bigM_for__PDAI_var_at_arcs_lower = max([self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] + self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]] for arc in self.arcs_list if arc[0] != arc[1]])
        self.bigM_for__PDAI_var_at_arcs_upper = self.bigM_for__PDAI_var_at_arcs_lower


        self.bigM_for__pressure_var_at_nodes_lower = max([self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressureBounds_at_nodes_dict_dict["LB"][node] for node in self.nodes_list]) 
        self.bigM_for__pressure_var_at_nodes_upper = self.bigM_for__pressure_var_at_nodes_lower

        self.bigM_for__loadshed_var_at_exit_nodes_lower = 1.0
        self.bigM_for__loadshed_var_at_exit_nodes_upper = self.bigM_for__loadshed_var_at_exit_nodes_lower

        self.bigM_for__loadshed_var_at_entry_nodes_lower = max([1.0 - self.loadshedBounds_at_nodes_dict_dict["LB"][node] for node in self.entry_nodes_list])
        self.bigM_for__loadshed_var_at_entry_nodes_upper = self.bigM_for__loadshed_var_at_entry_nodes_lower

        #bigM values Dualvariablen     
        
        self.bigM_for__dual_flow_var_at_arcs_lower = 1.0
        self.bigM_for__dual_flow_var_at_arcs_upper = self.bigM_for__dual_flow_var_at_arcs_lower
        #print(self.bigM_for__dual_flow_var_at_arcs_lower)
        ## TODO: Try different modeling approach for the PDAI_var boundaries in combination with the pressure bounds. (see Paper)
        self.bigM_for__dual_PDAI_var_at_arcs_lower = max([GRB.INFINITY if self.pressureLossFactor_at_arcs_dict[arc] == 0.0 else 1.0 / self.pressureLossFactor_at_arcs_dict[arc] for arc in self.arcs_list])
        self.bigM_for__dual_PDAI_var_at_arcs_upper = self.bigM_for__dual_PDAI_var_at_arcs_lower
        #print(self.bigM_for__dual_PDAI_var_at_arcs_lower)
        self.bigM_for__dual_pressure_var_at_nodes_lower = max([((len(self.adjacent_arcs_as_list(node,"out") + self.adjacent_arcs_as_list(node, "in")) * self.bigM_for__dual_PDAI_var_at_arcs_upper)) for node in self.nodes_list])
        self.bigM_for__dual_pressure_var_at_nodes_upper = self.bigM_for__dual_pressure_var_at_nodes_lower 
        #print(self.bigM_for__dual_pressure_var_at_nodes_upper)
        self.bigM_for__dual_loadshed_var_at_entry_nodes_lower = max([self.loadflow_at_nodes_dict[node] for node in self.nodes_list])#1.0
        self.bigM_for__dual_loadshed_var_at_entry_nodes_upper = self.bigM_for__dual_loadshed_var_at_entry_nodes_lower
        #print(self.bigM_for__dual_loadshed_var_at_entry_nodes_lower)
        self.bigM_for__dual_loadshed_var_at_exit_nodes_lower = 2*self.bigM_for__dual_loadshed_var_at_entry_nodes_lower#max([self.loadflow_at_nodes_dict[node] * (1.0 + max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list]))) for node in self.exit_nodes_list])
        self.bigM_for__dual_loadshed_var_at_exit_nodes_upper = self.bigM_for__dual_loadshed_var_at_exit_nodes_lower 
        #print(self.bigM_for__dual_loadshed_var_at_exit_nodes_lower)
    
        self.m.addConstrs(self.dual_flowConservation_var_at_nodes[node] <= 1 for node in self.nodes_list) #max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list])) for node in self.nodes_list)
        self.m.addConstrs(self.dual_flowConservation_var_at_nodes[node] >= - 1 for node in self.nodes_list) #max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list])) for node in self.nodes_list)

        ## TODO: Implementierung der Bedingung, damit \m_u^+ positiv ist. (Grenzen kleiner wählen)
        '''self.m.addConstrs(quicksum(self.dual_flow_var_at_arcs_lower) 
                         + quicksum(self.dual_flow_var_at_arcs_upper) 
                         + quicksum(self.dual_loadshed_var_at_entry_nodes_lower)
                         + quicksum(self.dual_loadshed_var_at_entry_nodes_upper) 
                         #+ quicksum(self.dual_PDAI_var_at_arcs_lower) 
                         + quicksum(self.dual_PDAI_var_at_arcs_upper) 
                         #+ quicksum(self.dual_pressure_var_at_nodes_lower)
                         #+ quicksum(self.dual_pressure_var_at_nodes_upper) 
                         -1.0 
                         <= self.dual_loadshed_var_at_exit_nodes_upper[node] * self.loadflow_at_nodes_dict[node] for node in self.exit_nodes_list if self.loadflow_at_nodes_dict[node] > 0)
        '''
        '''self.primal_PDAI_var_at_arcs_lower = self.m.addVars(self.arcs_list, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="primal_PDAI_var_at_arcs_lower")
        self.primal_PDAI_var_at_arcs_upper = self.m.addVars(self.arcs_list, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="primal_PDAI_var_at_arcs_upper")
        '''
        '''self.primal_pressure_var_at_nodes_lower = self.m.addVars(self.nodes_list, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="primal_pressure_var_at_nodes_lower")
        self.primal_pressure_var_at_nodes_upper = self.m.addVars(self.nodes_list, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="primal_pressure_var_at_nodes_upper")
'''
        
        
        #tolerance = 10e-12 # Define your tolerance

        '''for arc in self.arcs_list:
            self.m.addConstr((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - self.PDAIBounds_at_arcs_dict_dict["LB"][arc] - tolerance <= self.primal_PDAI_var_at_arcs_lower[arc], name=f"primal_PDAI_lower_{arc}")
            self.m.addConstr((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - self.PDAIBounds_at_arcs_dict_dict["LB"][arc] + tolerance >= self.primal_PDAI_var_at_arcs_lower[arc], name=f"primal_PDAI_lower_{arc}_reversed")
            self.m.addConstr(self.PDAIBounds_at_arcs_dict_dict["UB"][arc] - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) -tolerance  <= self.primal_PDAI_var_at_arcs_upper[arc], name=f"primal_PDAI_upper_{arc}")
            self.m.addConstr(self.PDAIBounds_at_arcs_dict_dict["UB"][arc] - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) +tolerance >= self.primal_PDAI_var_at_arcs_upper[arc], name=f"primal_PDAI_upper_{arc}_reversed")
        '''
        #For each node, add relaxed constraints for primal_pressure_var_at_nodes_lower and primal_pressure_var_at_nodes_upper
        '''for node in self.nodes_list:
            self.m.addConstr((self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]) - tolerance <= self.primal_pressure_var_at_nodes_lower[node], name=f"primal_pressure_lower_{node}")
            self.m.addConstr((self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]) + tolerance >= self.primal_pressure_var_at_nodes_lower[node], name=f"primal_pressure_lower_{node}_reversed")
            self.m.addConstr((self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]) - tolerance <= self.primal_pressure_var_at_nodes_upper[node], name=f"primal_pressure_upper_{node}")
            self.m.addConstr((self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]) + tolerance >= self.primal_pressure_var_at_nodes_upper[node], name=f"primal_pressure_upper_{node}_reversed")
'''
        
        '''for arc in self.arcs_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_lower[arc], self.primal_PDAI_var_at_arcs_lower[arc]])
                
        # For each arc, add SOS1 constraint for dual_PDAI_var_at_arcs_upper and primal_PDAI_var_at_arcs_upper
        for arc in self.arcs_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_upper[arc], self.primal_PDAI_var_at_arcs_upper[arc]])
'''
        '''# For each node, add SOS1 constraint for dual_pressure_var_at_nodes_lower and primal_pressure_var_at_nodes_lower
        for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_lower[node], self.primal_pressure_var_at_nodes_lower[node]])

        # For each node, add SOS1 constraint for dual_pressure_var_at_nodes_upper and primal_pressure_var_at_nodes_upper
        for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_upper[node], self.primal_pressure_var_at_nodes_upper[node]])
        '''


        
        # obere Schranken für abwärts beschränkte Dual-Variablen
        UB_bigM_for__dual_flow_var_at_arcs_lower = self.m.addConstrs((self.dual_flow_var_at_arcs_lower[arc] <= self.bigM_for__dual_flow_var_at_arcs_lower * self.binary_var_for__dual_flow_var_at_arcs_lower[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_flow_var_at_arcs_lower")
        UB_bigM_for__dual_flow_var_at_arcs_upper = self.m.addConstrs((self.dual_flow_var_at_arcs_upper[arc] <= self.bigM_for__dual_flow_var_at_arcs_upper * self.binary_var_for__dual_flow_var_at_arcs_upper[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_flow_var_at_arcs_upper")

        UB_bigM_for__dual_PDAI_var_at_arcs_lower = self.m.addConstrs((self.dual_PDAI_var_at_arcs_lower[arc] <= self.bigM_for__dual_PDAI_var_at_arcs_lower * self.binary_var_for__dual_PDAI_var_at_arcs_lower[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_PDAI_var_at_arcs_lower")
        UB_bigM_for__dual_PDAI_var_at_arcs_upper = self.m.addConstrs((self.dual_PDAI_var_at_arcs_upper[arc] <= self.bigM_for__dual_PDAI_var_at_arcs_upper * self.binary_var_for__dual_PDAI_var_at_arcs_upper[arc] for arc in self.arcs_list), name="UB_bigM_for__dual_PDAI_var_at_arcs_upper")

        ## WENN PRESSURE_LOSS = 0, kann man dann nicht einfach die angrenzenden Knoten als einen Knoten betrachten und zusammenlegen
        UB_bigM_for__dual_pressure_var_at_nodes_lower = self.m.addConstrs((self.dual_pressure_var_at_nodes_lower[node] <= self.bigM_for__dual_pressure_var_at_nodes_lower * self.binary_var_for__dual_pressure_var_at_nodes_lower[node] for node in self.nodes_list), name="UB_bigM_for__dual_pressure_var_at_nodes_lower")
        UB_bigM_for__dual_pressure_var_at_nodes_upper = self.m.addConstrs((self.dual_pressure_var_at_nodes_upper[node] <= self.bigM_for__dual_pressure_var_at_nodes_upper * self.binary_var_for__dual_pressure_var_at_nodes_upper[node] for node in self.nodes_list), name="UB_bigM_for__dual_pressure_var_at_nodes_upper")

        UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_lower[node] <= self.bigM_for__dual_loadshed_var_at_exit_nodes_lower * self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower[node] for node in self.exit_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower")
        UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_exit_nodes_upper[node] <= self.bigM_for__dual_loadshed_var_at_exit_nodes_upper * self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper[node] for node in self.exit_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper")

        UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_lower[node] <= self.bigM_for__dual_loadshed_var_at_entry_nodes_lower * self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower[node] for node in self.entry_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower")
        UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper = self.m.addConstrs((self.dual_loadshed_var_at_entry_nodes_upper[node] <= self.bigM_for__dual_loadshed_var_at_entry_nodes_upper * self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper[node] for node in self.entry_nodes_list), name="UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper")

        
        # obere Schranken für primale Ungleichungsnebenbedingungen zu den Dualvariablen
        UB_for__flow_var_at_arcs_lower = self.m.addConstrs((self.flow_var_at_arcs[arc] - self.flowBounds_at_arcs_dict_dict["LB"][arc] <= (1.0 - self.binary_var_for__dual_flow_var_at_arcs_lower[arc]) * self.bigM_for__flow_var_at_arcs_lower for arc in self.arcs_list), name = "UB_for__flow_var_at_arcs_lower")
        UB_for__flow_var_at_arcs_upper = self.m.addConstrs((self.flowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc] <= (1.0 - self.binary_var_for__dual_flow_var_at_arcs_upper[arc]) * self.bigM_for__flow_var_at_arcs_upper for arc in self.arcs_list), name = "UB_for__flow_var_at_arcs_upper")

        UB_for__PDAI_var_at_arcs_lower = self.m.addConstrs(((self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - self.PDAIBounds_at_arcs_dict_dict["LB"][arc] <= (1.0 - self.binary_var_for__dual_PDAI_var_at_arcs_lower[arc]) * self.bigM_for__PDAI_var_at_arcs_lower for arc in self.arcs_list), name = "UB_for__PDAI_var_at_arcs_lower")
        UB_for__PDAI_var_at_arcs_upper = self.m.addConstrs((self.PDAIBounds_at_arcs_dict_dict["UB"][arc] - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) <= (1.0 - self.binary_var_for__dual_PDAI_var_at_arcs_upper[arc]) * self.bigM_for__PDAI_var_at_arcs_upper for arc in self.arcs_list), name = "UB_for__PDAI_var_at_arcs_upper")
        
        UB_for__pressure_var_at_nodes_lower = self.m.addConstrs((self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node] <= (1.0 - self.binary_var_for__dual_pressure_var_at_nodes_lower[node]) * self.bigM_for__pressure_var_at_nodes_lower for node in self.nodes_list), name = "UB_for__pressure_var_at_nodes_lower") 
        UB_for__pressure_var_at_nodes_upper = self.m.addConstrs((self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node] <= (1.0 - self.binary_var_for__dual_pressure_var_at_nodes_upper[node]) * self.bigM_for__pressure_var_at_nodes_upper for node in self.nodes_list), name = "UB_for__pressure_var_at_nodes_upper")
        
        UB_for__loadshed_var_at_exit_nodes_lower = self.m.addConstrs((self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower[node]) * self.bigM_for__loadshed_var_at_exit_nodes_lower for node in self.exit_nodes_list), name = "UB_for__loadshed_var_at_exit_nodes_lower")
        UB_for__loadshed_var_at_exit_nodes_upper = self.m.addConstrs((self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper[node]) * self.bigM_for__loadshed_var_at_exit_nodes_upper for node in self.exit_nodes_list), name = "UB_for__loadshed_var_at_exit_nodes_upper")

        UB_for__loadshed_var_at_entry_nodes_lower = self.m.addConstrs((self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower[node]) * self.bigM_for__loadshed_var_at_entry_nodes_lower for node in self.entry_nodes_list), name = "UB_for__loadshed_var_at_entry_nodes_lower")
        UB_for__loadshed_var_at_entry_nodes_upper = self.m.addConstrs((self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node] <= (1.0 - self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper[node]) * self.bigM_for__loadshed_var_at_entry_nodes_upper for node in self.entry_nodes_list), name = "UB_for__loadshed_var_at_entry_nodes_upper")
        
        
    def test_for_zero_flow(self):
        n = self.m
        n.addConstrs(self.flow_var_at_arcs[arc] == 0.0 for arc in self.arcs_list)
        n.optimize()
        if n.Status == GRB.INFEASIBLE:
            print("!!!zero flow infeasible!!!")
            return False
        else:
            print("model valid")
            return True
        
    def test_for_complete_loadshed(self):
        n = self.m
        n.addConstrs(self.loadshed_var_at_nodes[node] == 1.0 for node in self.entry_nodes_list + self.exit_nodes_list)
        n.optimize()
        if n.Status == GRB.INFEASIBLE:
            print("!!!zero flow infeasible!!!")
            return False
        else:
            print("model valid")
            return True
        
    def test_all_possible_relaxations_of_the_IIS(self):
            tolerance = 1
            
            self.m.computeIIS()
            # Prepare a CSV file to save the results
            with open('results.csv', 'w', newline='') as file:
                writer = csv.writer(file,delimiter=";")
                writer.writerow(["Constraint", "Status"])
                dictionary = {c: c.IISConstr for c in self.m.getConstrs()}
                
                # Loop through each constraint
                for c in dictionary.keys() or True:
                    
                    #self.m.computeIIS()
                    if dictionary[c] == 1:
                        # Save the original RHS and sense
                        original_rhs = c.RHS
                        original_sense = c.Sense
                        original_expr = self.m.getRow(c)
                        original_name = c.ConstrName

                        # Adjust the constraint based on its sense
                        if c.Sense == GRB.EQUAL:  # If the sense is '=='
                            self.m.remove(c)
                            # Create a new constraint with '<=' sense
                            c_1_new = self.m.addConstr(original_expr <= original_rhs + tolerance, name=original_name+"_le")

                            # Create a new constraint with '>=' sense
                            c_2_new = self.m.addConstr(original_expr >= original_rhs - tolerance, name=original_name+"_ge")
                            
                            self.m.update()
                            
                        elif c.Sense == GRB.LESS_EQUAL:  # If the sense is '<='
                            c.RHS = original_rhs + tolerance  # Increase the RHS by the tolerance
                        elif c.Sense == GRB.GREATER_EQUAL:  # If the sense is '>='
                            c.RHS = original_rhs - tolerance  # Decrease the RHS by the tolerance

                        # Optimize the model with the adjusted constraint
                        self.m.optimize()

                        # Check the status of the model
                        status = self.m.Status
                        if status == GRB.OPTIMAL:
                            result = "Optimal"
                        elif status == GRB.INFEASIBLE:
                            result = "Infeasible"
                        else:
                            result = "Other"

                        #self.m.computeIIS()
                        self.m.write("tmp.lp")
                        
                        # Open the file and read its contents
                        with open("tmp.lp", "r") as tmp:
                            file_contents = tmp.read()

                        if self.m.Status != GRB.INFEASIBLE:
                            # Write the result to the CSV file
                            writer.writerow([original_name, file_contents, result])

                      # Restore the original RHS and sense before testing the next constraint
                        self.m.remove(c)

                        if original_sense == GRB.LESS_EQUAL:
                            self.m.addConstr(original_expr <= original_rhs, name = original_name)
                        elif original_sense == GRB.GREATER_EQUAL:
                            self.m.addConstr(original_expr >= original_rhs, name = original_name)
                        elif original_sense == GRB.EQUAL:
                            self.m.remove(c_1_new)
                            self.m.remove(c_2_new)
                            self.m.addConstr(original_expr == original_rhs, name = original_name)
                     
                        self.m.update()

    ## TODO: Try to change c.RHS instead of simply 
    def enum_approach_with_simulated_single_level_formulation(self, withKKT):
        self.add_primal_feasibility_constraints()
        self.add_WCcheck_constraints()
        self.m.optimize()
        if self.m.Status == GRB.INFEASIBLE:
            return [self.interdiction, "infeasible", self.m.Runtime]
            
        self.add_dual_feasibility_constraints()
        if withKKT:
            self.add_complementarity_constraints()
        else:
            self.add_CC_bigM_reformulation()
        
        #self.test_for_zero_flow()
        #self.test_for_complete_loadshed()
    
        
        self.m.update()
        self.m.optimize()
        
        objVal = 0
        for v in self.m.getVars():
            for n in self.exit_nodes_list:
                if f"loadshed[{n}]" in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
                    
        if self.m.Status != GRB.INFEASIBLE and objVal != 0:
            self.m.write(f"bigmmodel_mode_{withKKT}.sol")
            self.m.write(f"model_mode_{withKKT}.lp")
        '''#analyzing the increase of the bound 
        with open("GasLib-40-analysis.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            bigM_dual_pressure_bound_lower,bigM_dual_pressure_bound_upper = [self.bigM_for__dual_pressure_var_at_nodes_lower]*2
            while self.m.Status == GRB.INFEASIBLE:
                bigM_dual_pressure_bound_lower *= 2
                bigM_dual_pressure_bound_upper *= 2
                for node in self.nodes_list:
                    # Remove existing constraints
                    for c in self.m.getConstrs():
                        if f"UB_bigM_for__dual_pressure_var_at_nodes_lower[{node}]" == c.ConstrName:
                            self.m.remove(c)
                            # Add updated constraints
                            self.m.addConstr(
                                (self.dual_pressure_var_at_nodes_lower[node] <= bigM_dual_pressure_bound_lower * self.binary_var_for__dual_pressure_var_at_nodes_lower[node]),
                                name=f"UB_bigM_for__dual_pressure_var_at_nodes_lower[{node}]"
                            )
                        if f"UB_bigM_for__dual_pressure_var_at_nodes_upper[{node}]" == c.ConstrName:
                            self.m.remove(c)
                            self.m.addConstr(
                                (self.dual_pressure_var_at_nodes_upper[node] <= bigM_dual_pressure_bound_upper * self.binary_var_for__dual_pressure_var_at_nodes_upper[node]),
                                name=f"UB_bigM_for__dual_pressure_var_at_nodes_upper[{node}]"
                            )
                self.m.update()
                self.m.optimize()

                status = "infeasible" if self.m.Status == 3 else "feasible"
                self.m.write("model.sol") if self.m.Status != 3 else None
                writer.writerow([status, bigM_dual_pressure_bound_lower, bigM_dual_pressure_bound_upper])
                
            while self.m.Status != GRB.INFEASIBLE:
                bigM_dual_pressure_bound_upper /= 2
                for node in self.nodes_list:
                    # Remove existing constraints
                    for c in self.m.getConstrs():
                        if"UB_bigM_for__dual_pressure_var_at_nodes_upper[{node}]" == c.ConstrName:
                            self.m.remove(c)
                            self.m.addConstr(
                                (self.dual_pressure_var_at_nodes_upper[node] <= bigM_dual_pressure_bound_upper * self.binary_var_for__dual_pressure_var_at_nodes_upper[node]),
                                name=f"UB_bigM_for__dual_pressure_var_at_nodes_upper[{node}]"
                            )
                    
                self.m.update()
                self.m.optimize()
                status = "infeasible" if self.m.Status == 3 else "feasible"
                self.m.write("model.sol") if self.m.Status != 3 else None
                writer.writerow([status, bigM_dual_pressure_bound_lower, bigM_dual_pressure_bound_upper])
                '''
                           
        '''  # Assuming `model` is your Gurobi model
        self.m.setParam('NumericFocus', 1)
        self.m.setParam('TimeLimit', 600)  # Set a reasonable time limit
        self.m.setParam('NodefileStart', 0.5)  # Set node file start to use disk space

        try:
            self.m.computeIIS()
            self.m.write("model.ilp")
            print("IIS written to model.ilp")
        except Exception as e:
            print(f"Error computing IIS: {e}")      '''          
            
        '''if self.m.Status == GRB.INFEASIBLE:
            # Perform feasibility relaxation
            # Type 0: Minimize the weighted sum of relaxations
            self.m.feasRelaxS(0, True, False, True)

            # Optimize the relaxed model
            self.m.optimize()

            # Output the relaxed solution
            if self.m.Status == GRB.OPTIMAL:
                print("FeasRelax solution:")
                for v in self.m.getVars():
                    print(f"{v.VarName}: {v.X}")

                # Check which constraints were relaxed and by how much
                print("\nConstraint relaxations:")
                for constr in self.m.getConstrs():
                    relaxation_amount = constr.getAttr(GRB.Attr.Slack)
                    if relaxation_amount > 0:
                        print(f"{constr.ConstrName} was relaxed by {relaxation_amount}")
            else:
                print("No solution found for the relaxed model.")
        else:
            print("The original model is feasible.")
        sys.exit()'''
        if self.m.Status == GRB.INFEASIBLE:
            
            print(self.m.Status)
            print("iis0")
            self.m.computeIIS()
            print("iis1")
            #self.test_all_possible_relaxations_of_the_IIS()
            self.m.computeIIS()
            print("iis2")
            dictionary = {c: c.IISConstr for c in self.m.getConstrs()}
            self.m.write("model.ilp")
            for c in self.m.getConstrs():
                if dictionary[c] == 1 and "WCcheck_constraints" in c.ConstrName:
                    return [self.interdiction, "not weakly connected", self.m.Runtime]
                
        else:  
            objVal = 0
            for v in self.m.getVars():
                for n in self.exit_nodes_list:
                    if f"loadshed[{n}]" in v.VarName:
                        objVal += v.X * self.loadflow_at_nodes_dict[n]
            return [self.interdiction, objVal, self.m.Runtime]
        
    
class LeaderModel:
    def __init__(self, data: dict, networkInstanceName: str, interdictionBudget: int,reformulated: bool, withKKT: bool):
        self.data = data
        self.withKKT = withKKT
        self.reformulated = reformulated
        self.interdictionBudget = interdictionBudget
        self.networkInstanceName = networkInstanceName
        self.numberOfInterdictionVars = len(data["arcs"][None])
        
    
    def bruteForce(self):
        
        def generate_combinations(length, max_sum):
            if length == 0:
                yield []
            elif length == 1:
                for i in range(min(2, max_sum + 1)):
                    yield [i]
            else:
                for i in range(min(2, max_sum + 1)):
                    for rest in generate_combinations(length - 1, max_sum - i):
                        yield [i] + rest

        start_time_generate_combinations = time.time()
        interdictionDecisions_list = generate_combinations(self.numberOfInterdictionVars, self.interdictionBudget)
        end_time_generate_combinations = time.time()
        elapsed_time_generate_combinations = end_time_generate_combinations - start_time_generate_combinations
        
        

        all_feasible_interdiction_decisions_with_ObjVal = []
        for decision in interdictionDecisions_list:
            list_of_notWeakly_connected_interdictions = []
            interdiction_decision = dict(zip(self.data["arcs"][None], decision))
            
            tempModel = FollowerModel_WithInterdictionInput(data=self.data, interdictionDecision=interdiction_decision, networkInstanceName=self.networkInstanceName,with_loadflow_non_negative=True)
            
            isAlreadyNotFeasible=False
            for notWeakly_connected_interdiction in list_of_notWeakly_connected_interdictions:
                for key in interdiction_decision.keys():
                    if interdiction_decision[key] >= notWeakly_connected_interdiction[key]:
                        isAlreadyNotFeasible = True
            if not isAlreadyNotFeasible: 
                if not self.reformulated:
                    solution = tempModel.enum_approach_with_bilevel_formulation(self.withKKT)
                else:
                    solution = tempModel.enum_approach_with_simulated_single_level_formulation(self.withKKT)
                all_feasible_interdiction_decisions_with_ObjVal.append(solution)
                if solution[1] in ["infeasible","not weakly connected"]:
                    list_of_notWeakly_connected_interdictions.append(solution[0])
                
                
            
        #print(all_feasible_interdiction_decisions_with_ObjVal)
        sorted_list_of_dicts = sorted(filter(lambda x: not (x == None or isinstance(x[1], str)), all_feasible_interdiction_decisions_with_ObjVal), key=lambda x: x[1], reverse=True)

        if sorted_list_of_dicts != None and sorted_list_of_dicts != []:
            print("Feasible")
            return [sorted_list_of_dicts[0], elapsed_time_generate_combinations]
        else:
            return [[None, GRB.INFEASIBLE], elapsed_time_generate_combinations]
                
        