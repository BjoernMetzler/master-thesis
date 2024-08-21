from gurobipy import *
import sys
import csv
import time


class Single_Level_Formulation_Model:
    def __init__(
        self,
        data: dict,
        networkInstanceName: str,
        budget: int,
        with_loadflow_non_negative_at_entry_and_exit=True,
        with_pressureLossFactor_non_negative_at_arcs=False,
        with_mathematical_varnames_instead_of_GRB_model_names=False,
    ):
        self.m = Model(f"{networkInstanceName}")

        # General Model Parameters
        self.m.setParam("TimeLimit", 3600)  # Set a time limit for the optimization
        self.m.setParam("OutputFlag", 0)  # Suppress Gurobi output

        # Data conversion into Model
        self.nodes_list = data["nodes"][None]  # List of nodes
        self.arcs_list = data["arcs"][None]  # List of arcs
        self.interdictionBudget_int = budget  # Budget for interdiction
        self.activeElements_list = data["activeElements"][
            None
        ]  # List of active elements
        self.entry_nodes_list = [
            node for node in data["sigma"].keys() if data["sigma"][node] > 0
        ]  # Nodes with positive sigma (entry nodes)
        self.exit_nodes_list = [
            node for node in data["sigma"].keys() if data["sigma"][node] < 0
        ]  # Nodes with negative sigma (exit nodes)
        self.inner_nodes_list = [
            node
            for node in self.nodes_list
            if node not in self.exit_nodes_list + self.entry_nodes_list
        ]  # Nodes that are neither entry nor exit nodes
        self.sigma_at_nodes_dict = {
            **data["sigma"],
            **{node: 0 for node in self.inner_nodes_list},
        }  # Sigma values at nodes, with inner nodes set to 0
        self.pressureBounds_at_nodes_dict_dict = {
            "LB": data["pressureLb"],  # Lower bounds of pressure at nodes
            "UB": data["pressureUb"],  # Upper bounds of pressure at nodes
        }
        self.loadshedBounds_at_nodes_dict_dict = {
            "LB": {
                **data["loadshedLB"],
                **{node: 0.0 for node in self.inner_nodes_list},
            },  # Lower bounds of load shedding at nodes
            "UB": {
                **{
                    node: 1.0
                    for node in self.nodes_list
                    if node not in self.inner_nodes_list
                },
                **{node: 0.0 for node in self.inner_nodes_list},
            },  # Upper bounds of load shedding at nodes
        }
        self.massflowBounds_at_arcs_dict_dict = {
            "LB": data["massflowLb"],  # Lower bounds of mass flow at arcs
            "UB": data["massflowUb"],  # Upper bounds of mass flow at arcs
        }
        self.loadflow_at_nodes_dict = {
            **data["loadflow"],
            **{node: 0.0 for node in self.inner_nodes_list},
        }  # Load flow at nodes, with inner nodes set to 0
        self.pressureLossFactor_at_arcs_dict = data[
            "pressureLossFactor"
        ]  # Pressure loss factor at arcs
        self.WCloadflow_at_nodes_dict = data[
            "weaklyConnectedLoadflow"
        ]  # Weakly connected load flow at nodes

        # Data Manipulation Parameters
        self.with_loadflow_non_negative_at_entry_and_exit = with_loadflow_non_negative_at_entry_and_exit  # Flag to ensure load flow is non-negative at entry and exit nodes
        self.with_pressureLossFactor_non_negative_at_arcs = with_pressureLossFactor_non_negative_at_arcs  # Flag to ensure pressure loss factor is non-negative at arcs
        self.with_mathematical_varnames_instead_of_GRB_model_names = with_mathematical_varnames_instead_of_GRB_model_names #Flag to switch between variable names based on application

        # Ensure load flow is greater than 0 at entry and exit nodes
        if self.with_loadflow_non_negative_at_entry_and_exit:
            for node in self.entry_nodes_list + self.exit_nodes_list:
                if self.loadflow_at_nodes_dict[node] == 0.0:
                    self.loadflow_at_nodes_dict[
                        node
                    ] = 10e-6  # Adjust load flow to a small positive value
                    print(f"Info: Loadflow got adjusted to be != 0 at node {node}!")

        # Ensure pressure loss factor is greater than 0 at arcs
        if self.with_pressureLossFactor_non_negative_at_arcs:
            for arc in self.arcs_list:
                if self.pressureLossFactor_at_arcs_dict[arc] == 0.0:
                    self.pressureLossFactor_at_arcs_dict[
                        arc
                    ] = 10e-6  # Adjust pressure loss factor to a small positive value
                    print(
                        f"Info: Pressure Loss Factor got adjusted to be != 0 at arc {arc}!"
                    )
                    

    def adjacent_arcs_as_list(self, node: str, in_or_out: str):
        if "in" == in_or_out.lower():
            return [arc for arc in self.arcs_list if arc[1] == node]
        if "out" == in_or_out.lower():
            return [arc for arc in self.arcs_list if arc[0] == node]
        return []


    def add_WCcheck_constraints(self):
        self.WCcheck_flow_var_at_arcs = self.m.addVars(
            self.arcs_list,
            lb=-float("inf"),
            ub=float("inf"),
            name=f'{"WCcheckFlow" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "f"}',
            vtype=GRB.CONTINUOUS,
        )
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
            name="WCcheck_constraints",
        )
        self.m.addConstrs(
            self.interdiction_var_at_arcs[arc] * self.WCcheck_flow_var_at_arcs[arc] == 0.0
            for arc in self.arcs_list
        )


    def add_primal_feasibility_constraints(self):
        # Loadshed-Variable inklusive Beschränkungen für jeden Knoten
        self.loadshed_var_at_nodes = self.m.addVars(
            self.nodes_list,
            lb=self.loadshedBounds_at_nodes_dict_dict["LB"],
            ub=self.loadshedBounds_at_nodes_dict_dict["UB"],
            vtype=GRB.CONTINUOUS,
            name=f'{"loadshed" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "lambda"}',
        )

        # Flow variables with bounds for each arc
        self.flow_var_at_arcs = self.m.addVars(
            self.arcs_list,
            lb=-GRB.INFINITY,
            ub=GRB.INFINITY,
            vtype=GRB.CONTINUOUS,
            name=f'{"flow" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "q"}',
        )

        # Pressure variables with bounds for each node
        self.pressure_var_at_nodes = self.m.addVars(
            self.nodes_list,
            lb=self.pressureBounds_at_nodes_dict_dict["LB"],
            ub=self.pressureBounds_at_nodes_dict_dict["UB"],
            vtype=GRB.CONTINUOUS,
            name=f'{"pressure" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "pi"}',
        )

        # Interdiction Variable
        self.interdiction_var_at_arcs = self.m.addVars(
            self.arcs_list, vtype=GRB.BINARY,             
            name=f'{"interdiction" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "x"}',
        )

        # PDAI: Potential Decoupling After Interdiction Constraints
        PC_PDAI_lower_at_arcs = self.m.addConstrs(
            (
                self.pressure_var_at_nodes[arc[0]]
                - self.pressure_var_at_nodes[arc[1]]
                - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]
                >= self.interdiction_var_at_arcs[arc]
                * (
                    self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]]
                    - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]
                )
                for arc in self.arcs_list
            ),
            name="PDAI_lower",
        )
        PC_PDAI_upper_at_arcs = self.m.addConstrs(
            (
                self.pressure_var_at_nodes[arc[0]]
                - self.pressure_var_at_nodes[arc[1]]
                - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]
                <= self.interdiction_var_at_arcs[arc]
                * (
                    self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]]
                    - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]
                )
                for arc in self.arcs_list
            ),
            name="PDAI_upper",
        )

        # Flow conservation at nodes
        PC_flow_conservation_at_nodes = self.m.addConstrs(
            (
                quicksum(
                    self.flow_var_at_arcs[arc]
                    for arc in self.adjacent_arcs_as_list(node, "out")
                )
                - quicksum(
                    self.flow_var_at_arcs[arc]
                    for arc in self.adjacent_arcs_as_list(node, "in")
                )
                == self.sigma_at_nodes_dict[node]
                * (1.0 - self.loadshed_var_at_nodes[node])
                * self.loadflow_at_nodes_dict[node]
                for node in self.nodes_list
            ),
            name="flow_conservation",
        )

        PC_flow_lower_at_arcs = self.m.addConstrs(
            (
                (1.0 - self.interdiction_var_at_arcs[arc])
                * self.massflowBounds_at_arcs_dict_dict["LB"][arc]
                <= self.flow_var_at_arcs[arc]
                for arc in self.arcs_list
            ),
            name="flow_lower",
        )
        PC_flow_upper_at_arcs = self.m.addConstrs(
            (
                (1.0 - self.interdiction_var_at_arcs[arc])
                * self.massflowBounds_at_arcs_dict_dict["UB"][arc]
                >= self.flow_var_at_arcs[arc]
                for arc in self.arcs_list
            ),
            name="flow_upper",
        )


    def add_dual_feasibility_constraints(self):

        # beschränkte Dual-Variablen (zu primalen Ungleichungsnebenbedingungen)
        self.dual_flow_var_at_arcs_lower = self.m.addVars(
            self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS,             
            name=f'{"dual_flow_lower" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "delta_minus"}',
        )
        self.dual_flow_var_at_arcs_upper = self.m.addVars(
            self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS,             
            name=f'{"dual_flow_upper" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "delta_plus"}',
        )


        self.dual_PDAI_var_at_arcs_lower = self.m.addVars(
            self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, 
            name=f'{"dual_PDAI_lower" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "epsilon_minus"}',
        )
        self.dual_PDAI_var_at_arcs_upper = self.m.addVars(
            self.arcs_list, lb=0.0, vtype=GRB.CONTINUOUS, 
            name=f'{"dual_PDAI_upper" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "epsilon_plus"}',
        )

        self.dual_pressure_var_at_nodes_lower = self.m.addVars(
            self.nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, 
            name=f'{"dual_pressure_lower" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "zeta_minus"}',
        )
        self.dual_pressure_var_at_nodes_upper = self.m.addVars(
            self.nodes_list, lb=0.0, vtype=GRB.CONTINUOUS, 
            name=f'{"dual_pressure_upper" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "zeta_plus"}',
        )

        self.dual_loadshed_var_at_exit_nodes_lower = self.m.addVars(
            self.exit_nodes_list,
            lb=0.0,
            vtype=GRB.CONTINUOUS,
            name=f'{"dual_loadshed_exit_lower" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "mu_minus"}',
        )
        self.dual_loadshed_var_at_exit_nodes_upper = self.m.addVars(
            self.exit_nodes_list,
            lb=0.0,
            vtype=GRB.CONTINUOUS,
            name=f'{"dual_loadshed_exit_upper" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "minus_plus"}',
        )

        self.dual_loadshed_var_at_entry_nodes_lower = self.m.addVars(
            self.entry_nodes_list,
            lb=0.0,
            vtype=GRB.CONTINUOUS,
            name=f'{"dual_loadshed_entry_lower" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "eta_minus"}',
        )
        self.dual_loadshed_var_at_entry_nodes_upper = self.m.addVars(
            self.entry_nodes_list,
            lb=0.0,
            vtype=GRB.CONTINUOUS,
            name=f'{"dual_loadshed_entry_upper" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "eta_plus"}',
        )

        # unbeschränkte Dual-Variablen (zu primalen Gleichheitsnebenbedingungen)
        self.dual_flowConservation_var_at_nodes = self.m.addVars(
            self.nodes_list,
            lb=-float("inf"),
            ub=float("inf"),
            vtype=GRB.CONTINUOUS,
            name=f'{"dual_flowConservation" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "alpha"}',
        )

        # EnNdfC: Entry node dual feasibility constraint
        DC_loadshed_at_entry_nodes = self.m.addConstrs(
            (
                -self.dual_flowConservation_var_at_nodes[node]
                * self.loadflow_at_nodes_dict[node]
                - self.dual_loadshed_var_at_entry_nodes_lower[node]
                + self.dual_loadshed_var_at_entry_nodes_upper[node]
                == 0.0
                for node in self.entry_nodes_list
            ),
            name="EnNdfC",
        )

        # ExNdfC: Exit node dual feasibility constraint
        DC_loadshed_at_exit_nodes = self.m.addConstrs(
            (
                self.loadflow_at_nodes_dict[node]
                + self.dual_flowConservation_var_at_nodes[node]
                * self.loadflow_at_nodes_dict[node]
                - self.dual_loadshed_var_at_exit_nodes_lower[node]
                + self.dual_loadshed_var_at_exit_nodes_upper[node]
                == 0.0
                for node in self.exit_nodes_list
            ),
            name="ExNdfC",
        )

        # Arc(without circle)dfC: Arc dual feasibility constraint
        DC_WOCircle_at_arcs = self.m.addConstrs(
            (
                -self.dual_flowConservation_var_at_nodes[arc[0]]
                + self.dual_flowConservation_var_at_nodes[arc[1]]
                - self.dual_flow_var_at_arcs_lower[arc]
                + self.dual_flow_var_at_arcs_upper[arc]
                + self.dual_PDAI_var_at_arcs_lower[arc]
                * self.pressureLossFactor_at_arcs_dict[arc]
                - self.dual_PDAI_var_at_arcs_upper[arc]
                * self.pressureLossFactor_at_arcs_dict[arc]
                == 0.0
                for arc in self.arcs_list
                if arc[0] != arc[1]
            ),
            name="ArcdfC",
        )

        # NodedfC: Node dual feasibility constraint
        DC_at_nodes = self.m.addConstrs(
            (
                quicksum(
                    self.dual_PDAI_var_at_arcs_upper[arc]
                    - self.dual_PDAI_var_at_arcs_lower[arc]
                    for arc in self.adjacent_arcs_as_list(node, "out")
                )
                - quicksum(
                    self.dual_PDAI_var_at_arcs_upper[arc]
                    - self.dual_PDAI_var_at_arcs_lower[arc]
                    for arc in self.adjacent_arcs_as_list(node, "in")
                )
                + self.dual_pressure_var_at_nodes_upper[node]
                - self.dual_pressure_var_at_nodes_lower[node]
                == 0.0
                for node in self.nodes_list
            ),
            name="NodedfC",
        )


    def add_SOS1(self):
        # Transforming the constraints into SOS1 constraints
        """for arc in self.arcs_list:
        self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_lower[arc], self.flow_var_at_arcs[arc] - (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["LB"][arc]])
        self.m.addSOS(GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_upper[arc], (1.0 - self.interdiction_var_at_arcs[arc]) * self.massflowBounds_at_arcs_dict_dict["UB"][arc] - self.flow_var_at_arcs[arc]])
        self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_lower[arc], (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]) - (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]))])
        self.m.addSOS(GRB.SOS_TYPE1, [self.dual_PDAI_var_at_arcs_upper[arc], (self.interdiction_var_at_arcs[arc] * (self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]] - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]])) - (self.pressure_var_at_nodes[arc[0]] - self.pressure_var_at_nodes[arc[1]] - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc])])"""
        # replaced by
        # Create auxiliary variables
        aux_vars_lower = self.m.addVars(self.arcs_list,name=f"aux_var_lower")
        aux_vars_upper = self.m.addVars(self.arcs_list,name=f"aux_var_upper")
        aux_vars_pdai_lower = self.m.addVars(self.arcs_list,name=f"aux_var_pdai_lower")
        aux_vars_pdai_upper = self.m.addVars(self.arcs_list,name=f"aux_var_pdai_upper")

        # Add constraints to define the auxiliary variables
        for arc in self.arcs_list:
            self.m.addConstr(
                aux_vars_lower[arc]
                == self.flow_var_at_arcs[arc]
                - (1.0 - self.interdiction_var_at_arcs[arc])
                * self.massflowBounds_at_arcs_dict_dict["LB"][arc],
                name=f"aux_constr_lower_{arc}",
            )
            self.m.addConstr(
                aux_vars_upper[arc]
                == (1.0 - self.interdiction_var_at_arcs[arc])
                * self.massflowBounds_at_arcs_dict_dict["UB"][arc]
                - self.flow_var_at_arcs[arc],
                name=f"aux_constr_upper_{arc}",
            )
            self.m.addConstr(
                aux_vars_pdai_lower[arc]
                == (
                    self.pressure_var_at_nodes[arc[0]]
                    - self.pressure_var_at_nodes[arc[1]]
                    - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]
                )
                - (
                    self.interdiction_var_at_arcs[arc]
                    * (
                        self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]]
                        - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]
                    )
                ),
                name=f"aux_constr_pdai_lower_{arc}",
            )
            self.m.addConstr(
                aux_vars_pdai_upper[arc]
                == (
                    self.interdiction_var_at_arcs[arc]
                    * (
                        self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]]
                        - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]
                    )
                )
                - (
                    self.pressure_var_at_nodes[arc[0]]
                    - self.pressure_var_at_nodes[arc[1]]
                    - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]
                ),
                name=f"aux_constr_pdai_upper_{arc}",
            )

        # Add SOS1 constraints using the auxiliary variables
        for arc in self.arcs_list:
            self.m.addSOS(
                GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_lower[arc], aux_vars_lower[arc]]
            )
            self.m.addSOS(
                GRB.SOS_TYPE1, [self.dual_flow_var_at_arcs_upper[arc], aux_vars_upper[arc]]
            )
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [self.dual_PDAI_var_at_arcs_lower[arc], aux_vars_pdai_lower[arc]],
            )
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [self.dual_PDAI_var_at_arcs_upper[arc], aux_vars_pdai_upper[arc]],
            )

        """for node in self.nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_lower[node], self.pressure_var_at_nodes[node] - self.pressureBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_pressure_var_at_nodes_upper[node], self.pressureBounds_at_nodes_dict_dict["UB"][node] - self.pressure_var_at_nodes[node]])

        for node in self.exit_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_lower[node], self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_exit_nodes_upper[node], self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]])

        for node in self.entry_nodes_list:
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_lower[node], self.loadshed_var_at_nodes[node] - self.loadshedBounds_at_nodes_dict_dict["LB"][node]])
            self.m.addSOS(GRB.SOS_TYPE1, [self.dual_loadshed_var_at_entry_nodes_upper[node], self.loadshedBounds_at_nodes_dict_dict["UB"][node] - self.loadshed_var_at_nodes[node]])
    """
        ## Replaced by
        # Create auxiliary variables
        aux_vars_pressure_lower = self.m.addVars(
            self.nodes_list,
            name=f"aux_var_pressure_lower",
        )
        aux_vars_pressure_upper = self.m.addVars(
            self.nodes_list,
            name=f"aux_var_pressure_upper",
        )
        print(aux_vars_pressure_lower)
        
        aux_vars_loadshed_exit_lower = self.m.addVars(
            self.exit_nodes_list,
            name=f"aux_var_loadshed_exit_lower",
        )
        aux_vars_loadshed_exit_upper = self.m.addVars(
            self.exit_nodes_list,
            name=f"aux_var_loadshed_exit_upper",
        )

        aux_vars_loadshed_entry_lower = self.m.addVars(
            self.entry_nodes_list,
            name=f"aux_var_loadshed_entry_lower",
        )
        aux_vars_loadshed_entry_upper = self.m.addVars(
            self.entry_nodes_list,
            name=f"aux_var_loadshed_entry_upper",
        )

        # Add constraints to define the auxiliary variables
        for node in self.nodes_list:
            self.m.addConstr(
                aux_vars_pressure_lower[node]
                == self.pressure_var_at_nodes[node]
                - self.pressureBounds_at_nodes_dict_dict["LB"][node],
                name=f"aux_constr_pressure_lower_{node}",
            )
            self.m.addConstr(
                aux_vars_pressure_upper[node]
                == self.pressureBounds_at_nodes_dict_dict["UB"][node]
                - self.pressure_var_at_nodes[node],
                name=f"aux_constr_pressure_upper_{node}",
            )

        for node in self.exit_nodes_list:
            self.m.addConstr(
                aux_vars_loadshed_exit_lower[node]
                == self.loadshed_var_at_nodes[node]
                - self.loadshedBounds_at_nodes_dict_dict["LB"][node],
                name=f"aux_constr_loadshed_exit_lower_{node}",
            )
            self.m.addConstr(
                aux_vars_loadshed_exit_upper[node]
                == self.loadshedBounds_at_nodes_dict_dict["UB"][node]
                - self.loadshed_var_at_nodes[node],
                name=f"aux_constr_loadshed_exit_upper_{node}",
            )

        for node in self.entry_nodes_list:
            self.m.addConstr(
                aux_vars_loadshed_entry_lower[node]
                == self.loadshed_var_at_nodes[node]
                - self.loadshedBounds_at_nodes_dict_dict["LB"][node],
                name=f"aux_constr_loadshed_entry_lower_{node}",
            )
            self.m.addConstr(
                aux_vars_loadshed_entry_upper[node]
                == self.loadshedBounds_at_nodes_dict_dict["UB"][node]
                - self.loadshed_var_at_nodes[node],
                name=f"aux_constr_loadshed_entry_upper_{node}",
            )

        # Add SOS1 constraints using the auxiliary variables
        for node in self.nodes_list:
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [
                    self.dual_pressure_var_at_nodes_lower[node],
                    aux_vars_pressure_lower[node],
                ],
            )
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [
                    self.dual_pressure_var_at_nodes_upper[node],
                    aux_vars_pressure_upper[node],
                ],
            )

        for node in self.exit_nodes_list:
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [
                    self.dual_loadshed_var_at_exit_nodes_lower[node],
                    aux_vars_loadshed_exit_lower[node],
                ],
            )
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [
                    self.dual_loadshed_var_at_exit_nodes_upper[node],
                    aux_vars_loadshed_exit_upper[node],
                ],
            )

        for node in self.entry_nodes_list:
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [
                    self.dual_loadshed_var_at_entry_nodes_lower[node],
                    aux_vars_loadshed_entry_lower[node],
                ],
            )
            self.m.addSOS(
                GRB.SOS_TYPE1,
                [
                    self.dual_loadshed_var_at_entry_nodes_upper[node],
                    aux_vars_loadshed_entry_upper[node],
                ],
            )


    def add__complementary_constraints(self):
        CC_dual_flow_var_at_arcs_lower = self.m.addConstrs(
            (
                self.dual_flow_var_at_arcs_lower[arc]
                * (
                    self.flow_var_at_arcs[arc]
                    - (1.0 - self.interdiction_var_at_arcs[arc])
                    * self.massflowBounds_at_arcs_dict_dict["LB"][arc]
                )
                == 0.0
                for arc in self.arcs_list
            ),
            name="CC_dual_flow_var_at_arcs_lower",
        )
        CC_dual_flow_var_at_arcs_upper = self.m.addConstrs(
            (
                self.dual_flow_var_at_arcs_upper[arc]
                * (
                    (1.0 - self.interdiction_var_at_arcs[arc])
                    * self.massflowBounds_at_arcs_dict_dict["UB"][arc]
                    - self.flow_var_at_arcs[arc]
                )
                == 0.0
                for arc in self.arcs_list
            ),
            name="CC_dual_flow_var_at_arcs_upper",
        )
        CC_dual_PDAI_var_at_arcs_lower = self.m.addConstrs(
            (
                self.dual_PDAI_var_at_arcs_lower[arc]
                * (
                    (
                        self.pressure_var_at_nodes[arc[0]]
                        - self.pressure_var_at_nodes[arc[1]]
                        - self.pressureLossFactor_at_arcs_dict[arc]
                        * self.flow_var_at_arcs[arc]
                    )
                    - (
                        self.interdiction_var_at_arcs[arc]
                        * (
                            self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]]
                            - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]
                        )
                    )
                )
                == 0.0
                for arc in self.arcs_list
            ),
            name="CC_dual_PDAI_var_at_arcs_lower",
        )
        CC_dual_PDAI_var_at_arcs_upper = self.m.addConstrs(
            (
                self.dual_PDAI_var_at_arcs_upper[arc]
                * (
                    (
                        self.interdiction_var_at_arcs[arc]
                        * (
                            self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]]
                            - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]
                        )
                    )
                    - (
                        self.pressure_var_at_nodes[arc[0]]
                        - self.pressure_var_at_nodes[arc[1]]
                        - self.pressureLossFactor_at_arcs_dict[arc]
                        * self.flow_var_at_arcs[arc]
                    )
                )
                == 0.0
                for arc in self.arcs_list
            ),
            name="CC_dual_PDAI_var_at_arcs_upper",
        )
        CC_dual_pressure_var_at_nodes_lower = self.m.addConstrs(
            (
                self.dual_pressure_var_at_nodes_lower[node]
                * (
                    self.pressure_var_at_nodes[node]
                    - self.pressureBounds_at_nodes_dict_dict["LB"][node]
                )
                == 0.0
                for node in self.nodes_list
            ),
            name="CC_dual_pressure_var_at_nodes_lower",
        )
        CC_dual_pressure_var_at_nodes_upper = self.m.addConstrs(
            (
                self.dual_pressure_var_at_nodes_upper[node]
                * (
                    self.pressureBounds_at_nodes_dict_dict["UB"][node]
                    - self.pressure_var_at_nodes[node]
                )
                == 0.0
                for node in self.nodes_list
            ),
            name="CC_dual_pressure_var_at_nodes_upper",
        )
        CC_dual_loadshed_var_at_exit_nodes_lower = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_exit_nodes_lower[node]
                * (
                    self.loadshed_var_at_nodes[node]
                    - self.loadshedBounds_at_nodes_dict_dict["LB"][node]
                )
                == 0.0
                for node in self.exit_nodes_list
            ),
            name="CC_dual_loadshed_var_at_exit_nodes_lower",
        )
        CC_dual_loadshed_var_at_exit_nodes_upper = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_exit_nodes_upper[node]
                * (
                    self.loadshedBounds_at_nodes_dict_dict["UB"][node]
                    - self.loadshed_var_at_nodes[node]
                )
                == 0.0
                for node in self.exit_nodes_list
            ),
            name="CC_dual_loadshed_var_at_exit_nodes_upper",
        )
        CC_dual_loadshed_var_at_entry_nodes_lower = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_entry_nodes_lower[node]
                * (
                    self.loadshed_var_at_nodes[node]
                    - self.loadshedBounds_at_nodes_dict_dict["LB"][node]
                )
                == 0.0
                for node in self.entry_nodes_list
            ),
            name="CC_dual_loadshed_var_at_entry_nodes_lower",
        )
        CC_dual_loadshed_var_at_entry_nodes_upper = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_entry_nodes_upper[node]
                * (
                    self.loadshedBounds_at_nodes_dict_dict["UB"][node]
                    - self.loadshed_var_at_nodes[node]
                )
                == 0.0
                for node in self.entry_nodes_list
            ),
            name="CC_dual_loadshed_var_at_entry_nodes_upper",
        )


    def add_CC_bigM_reformulation(self):
        # binäre Hilfsvariablen für bigM-Reformulierung der Komplementaritätsbedingungen
        self.binary_var_for__dual_flow_var_at_arcs_lower = self.m.addVars(
            self.arcs_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_flow_var_at_arcs_lower",
        )
        self.binary_var_for__dual_flow_var_at_arcs_upper = self.m.addVars(
            self.arcs_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_flow_var_at_arcs_upper",
        )
        self.binary_var_for__dual_PDAI_var_at_arcs_lower = self.m.addVars(
            self.arcs_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_PDAI_var_at_arcs_lower",
        )
        self.binary_var_for__dual_PDAI_var_at_arcs_upper = self.m.addVars(
            self.arcs_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_PDAI_var_at_arcs_upper",
        )
        self.binary_var_for__dual_pressure_var_at_nodes_lower = self.m.addVars(
            self.nodes_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_pressure_var_at_nodes_lower",
        )
        self.binary_var_for__dual_pressure_var_at_nodes_upper = self.m.addVars(
            self.nodes_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_pressure_var_at_nodes_upper",
        )
        self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower = self.m.addVars(
            self.exit_nodes_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_loadshed_var_at_exit_nodes_lower",
        )
        self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper = self.m.addVars(
            self.exit_nodes_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_loadshed_var_at_exit_nodes_upper",
        )
        self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower = self.m.addVars(
            self.entry_nodes_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_loadshed_var_at_entry_nodes_lower",
        )
        self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper = self.m.addVars(
            self.entry_nodes_list,
            vtype=GRB.BINARY,
            name="binary_var_for__dual_loadshed_var_at_entry_nodes_upper",
        )

        # bigM-Werte für primale Ungleichungsnebenbedingungen
        self.bigM_for__flow_var_at_arcs_lower = max(
            [
                self.massflowBounds_at_arcs_dict_dict["UB"][arc]
                - self.massflowBounds_at_arcs_dict_dict["LB"][arc]
                for arc in self.arcs_list
            ]
        )
        self.bigM_for__flow_var_at_arcs_upper = self.bigM_for__flow_var_at_arcs_lower

        self.bigM_for__PDAI_var_at_arcs_lower = max(
            [
                self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]]
                - self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]]
                + self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]
                - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]
                for arc in self.arcs_list
                if arc[0] != arc[1]
            ]
        )
        self.bigM_for__PDAI_var_at_arcs_upper = self.bigM_for__PDAI_var_at_arcs_lower

        self.bigM_for__pressure_var_at_nodes_lower = max(
            [
                self.pressureBounds_at_nodes_dict_dict["UB"][node]
                - self.pressureBounds_at_nodes_dict_dict["LB"][node]
                for node in self.nodes_list
            ]
        )
        self.bigM_for__pressure_var_at_nodes_upper = (
            self.bigM_for__pressure_var_at_nodes_lower
        )

        self.bigM_for__loadshed_var_at_exit_nodes_lower = 1.0
        self.bigM_for__loadshed_var_at_exit_nodes_upper = (
            self.bigM_for__loadshed_var_at_exit_nodes_lower
        )

        self.bigM_for__loadshed_var_at_entry_nodes_lower = max(
            [
                1.0 - self.loadshedBounds_at_nodes_dict_dict["LB"][node]
                for node in self.entry_nodes_list
            ]
        )
        self.bigM_for__loadshed_var_at_entry_nodes_upper = (
            self.bigM_for__loadshed_var_at_entry_nodes_lower
        )

        # bigM values Dualvariablen

        self.bigM_for__dual_flow_var_at_arcs_lower = 1.0
        self.bigM_for__dual_flow_var_at_arcs_upper = (
            self.bigM_for__dual_flow_var_at_arcs_lower
        )


        self.bigM_for__dual_PDAI_var_at_arcs_lower = max(
            [
                GRB.INFINITY
                if self.pressureLossFactor_at_arcs_dict[arc] == 0.0
                else 1.0 / self.pressureLossFactor_at_arcs_dict[arc]
                for arc in self.arcs_list
            ]
        )
        self.bigM_for__dual_PDAI_var_at_arcs_upper = (
            self.bigM_for__dual_PDAI_var_at_arcs_lower
        )

        self.bigM_for__dual_pressure_var_at_nodes_lower = max(
            [
                (
                    (
                        len(
                            self.adjacent_arcs_as_list(node, "out")
                            + self.adjacent_arcs_as_list(node, "in")
                        )
                        * self.bigM_for__dual_PDAI_var_at_arcs_upper
                    )
                )
                for node in self.nodes_list
            ]
        )
        self.bigM_for__dual_pressure_var_at_nodes_upper = (
            self.bigM_for__dual_pressure_var_at_nodes_lower
        )

        self.bigM_for__dual_loadshed_var_at_entry_nodes_lower = max(
            [self.loadflow_at_nodes_dict[node] for node in self.nodes_list]
        )  # 1.0
        self.bigM_for__dual_loadshed_var_at_entry_nodes_upper = (
            self.bigM_for__dual_loadshed_var_at_entry_nodes_lower
        )

        self.bigM_for__dual_loadshed_var_at_exit_nodes_lower = (
            2 * self.bigM_for__dual_loadshed_var_at_entry_nodes_lower
        )  # max([self.loadflow_at_nodes_dict[node] * (1.0 + max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list]))) for node in self.exit_nodes_list])
        self.bigM_for__dual_loadshed_var_at_exit_nodes_upper = (
            self.bigM_for__dual_loadshed_var_at_exit_nodes_lower
        )


        self.m.addConstrs(
            self.dual_flowConservation_var_at_nodes[node] <= 1 for node in self.nodes_list
        )  # max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list])) for node in self.nodes_list)
        self.m.addConstrs(
            self.dual_flowConservation_var_at_nodes[node] >= -1 for node in self.nodes_list
        )  # max(1.0, max([GRB.INFINITY if self.loadflow_at_nodes_dict[node] == 0.0 else 1.0 / self.loadflow_at_nodes_dict[node] for node in self.entry_nodes_list])) for node in self.nodes_list)

        # obere Schranken für abwärts beschränkte Dual-Variablen
        UB_bigM_for__dual_flow_var_at_arcs_lower = self.m.addConstrs(
            (
                self.dual_flow_var_at_arcs_lower[arc]
                <= self.bigM_for__dual_flow_var_at_arcs_lower
                * self.binary_var_for__dual_flow_var_at_arcs_lower[arc]
                for arc in self.arcs_list
            ),
            name="UB_bigM_for__dual_flow_var_at_arcs_lower",
        )
        UB_bigM_for__dual_flow_var_at_arcs_upper = self.m.addConstrs(
            (
                self.dual_flow_var_at_arcs_upper[arc]
                <= self.bigM_for__dual_flow_var_at_arcs_upper
                * self.binary_var_for__dual_flow_var_at_arcs_upper[arc]
                for arc in self.arcs_list
            ),
            name="UB_bigM_for__dual_flow_var_at_arcs_upper",
        )

        UB_bigM_for__dual_PDAI_var_at_arcs_lower = self.m.addConstrs(
            (
                self.dual_PDAI_var_at_arcs_lower[arc]
                <= self.bigM_for__dual_PDAI_var_at_arcs_lower
                * self.binary_var_for__dual_PDAI_var_at_arcs_lower[arc]
                for arc in self.arcs_list
            ),
            name="UB_bigM_for__dual_PDAI_var_at_arcs_lower",
        )
        UB_bigM_for__dual_PDAI_var_at_arcs_upper = self.m.addConstrs(
            (
                self.dual_PDAI_var_at_arcs_upper[arc]
                <= self.bigM_for__dual_PDAI_var_at_arcs_upper
                * self.binary_var_for__dual_PDAI_var_at_arcs_upper[arc]
                for arc in self.arcs_list
            ),
            name="UB_bigM_for__dual_PDAI_var_at_arcs_upper",
        )

        UB_bigM_for__dual_pressure_var_at_nodes_lower = self.m.addConstrs(
            (
                self.dual_pressure_var_at_nodes_lower[node]
                <= self.bigM_for__dual_pressure_var_at_nodes_lower
                * self.binary_var_for__dual_pressure_var_at_nodes_lower[node]
                for node in self.nodes_list
            ),
            name="UB_bigM_for__dual_pressure_var_at_nodes_lower",
        )
        UB_bigM_for__dual_pressure_var_at_nodes_upper = self.m.addConstrs(
            (
                self.dual_pressure_var_at_nodes_upper[node]
                <= self.bigM_for__dual_pressure_var_at_nodes_upper
                * self.binary_var_for__dual_pressure_var_at_nodes_upper[node]
                for node in self.nodes_list
            ),
            name="UB_bigM_for__dual_pressure_var_at_nodes_upper",
        )

        UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_exit_nodes_lower[node]
                <= self.bigM_for__dual_loadshed_var_at_exit_nodes_lower
                * self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower[node]
                for node in self.exit_nodes_list
            ),
            name="UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower",
        )
        UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_exit_nodes_upper[node]
                <= self.bigM_for__dual_loadshed_var_at_exit_nodes_upper
                * self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper[node]
                for node in self.exit_nodes_list
            ),
            name="UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper",
        )

        UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_entry_nodes_lower[node]
                <= self.bigM_for__dual_loadshed_var_at_entry_nodes_lower
                * self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower[node]
                for node in self.entry_nodes_list
            ),
            name="UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower",
        )
        UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper = self.m.addConstrs(
            (
                self.dual_loadshed_var_at_entry_nodes_upper[node]
                <= self.bigM_for__dual_loadshed_var_at_entry_nodes_upper
                * self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper[node]
                for node in self.entry_nodes_list
            ),
            name="UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper",
        )

        # obere Schranken für primale Ungleichungsnebenbedingungen zu den Dualvariablen
        UB_for__flow_var_at_arcs_lower = self.m.addConstrs(
            (
                self.flow_var_at_arcs[arc]
                - (1.0 - self.interdiction_var_at_arcs[arc])
                * self.massflowBounds_at_arcs_dict_dict["LB"][arc]
                <= (1.0 - self.binary_var_for__dual_flow_var_at_arcs_lower[arc])
                * self.bigM_for__flow_var_at_arcs_lower
                for arc in self.arcs_list
            ),
            name="UB_for__flow_var_at_arcs_lower",
        )
        UB_for__flow_var_at_arcs_upper = self.m.addConstrs(
            (
                (1.0 - self.interdiction_var_at_arcs[arc])
                * self.massflowBounds_at_arcs_dict_dict["UB"][arc]
                - self.flow_var_at_arcs[arc]
                <= (1.0 - self.binary_var_for__dual_flow_var_at_arcs_upper[arc])
                * self.bigM_for__flow_var_at_arcs_upper
                for arc in self.arcs_list
            ),
            name="UB_for__flow_var_at_arcs_upper",
        )

        UB_for__PDAI_var_at_arcs_lower = self.m.addConstrs(
            (
                (
                    self.pressure_var_at_nodes[arc[0]]
                    - self.pressure_var_at_nodes[arc[1]]
                    - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]
                )
                - (
                    self.interdiction_var_at_arcs[arc]
                    * (
                        self.pressureBounds_at_nodes_dict_dict["LB"][arc[0]]
                        - self.pressureBounds_at_nodes_dict_dict["UB"][arc[1]]
                    )
                )
                <= (1.0 - self.binary_var_for__dual_PDAI_var_at_arcs_lower[arc])
                * self.bigM_for__PDAI_var_at_arcs_lower
                for arc in self.arcs_list
            ),
            name="UB_for__PDAI_var_at_arcs_lower",
        )
        UB_for__PDAI_var_at_arcs_upper = self.m.addConstrs(
            (
                (
                    self.interdiction_var_at_arcs[arc]
                    * (
                        self.pressureBounds_at_nodes_dict_dict["UB"][arc[0]]
                        - self.pressureBounds_at_nodes_dict_dict["LB"][arc[1]]
                    )
                )
                - (
                    self.pressure_var_at_nodes[arc[0]]
                    - self.pressure_var_at_nodes[arc[1]]
                    - self.pressureLossFactor_at_arcs_dict[arc] * self.flow_var_at_arcs[arc]
                )
                <= (1.0 - self.binary_var_for__dual_PDAI_var_at_arcs_upper[arc])
                * self.bigM_for__PDAI_var_at_arcs_upper
                for arc in self.arcs_list
            ),
            name="UB_for__PDAI_var_at_arcs_upper",
        )

        UB_for__pressure_var_at_nodes_lower = self.m.addConstrs(
            (
                self.pressure_var_at_nodes[node]
                - self.pressureBounds_at_nodes_dict_dict["LB"][node]
                <= (1.0 - self.binary_var_for__dual_pressure_var_at_nodes_lower[node])
                * self.bigM_for__pressure_var_at_nodes_lower
                for node in self.nodes_list
            ),
            name="UB_for__pressure_var_at_nodes_lower",
        )
        UB_for__pressure_var_at_nodes_upper = self.m.addConstrs(
            (
                self.pressureBounds_at_nodes_dict_dict["UB"][node]
                - self.pressure_var_at_nodes[node]
                <= (1.0 - self.binary_var_for__dual_pressure_var_at_nodes_upper[node])
                * self.bigM_for__pressure_var_at_nodes_upper
                for node in self.nodes_list
            ),
            name="UB_for__pressure_var_at_nodes_upper",
        )

        UB_for__loadshed_var_at_exit_nodes_lower = self.m.addConstrs(
            (
                self.loadshed_var_at_nodes[node]
                - self.loadshedBounds_at_nodes_dict_dict["LB"][node]
                <= (1.0 - self.binary_var_for__dual_loadshed_var_at_exit_nodes_lower[node])
                * self.bigM_for__loadshed_var_at_exit_nodes_lower
                for node in self.exit_nodes_list
            ),
            name="UB_for__loadshed_var_at_exit_nodes_lower",
        )
        UB_for__loadshed_var_at_exit_nodes_upper = self.m.addConstrs(
            (
                self.loadshedBounds_at_nodes_dict_dict["UB"][node]
                - self.loadshed_var_at_nodes[node]
                <= (1.0 - self.binary_var_for__dual_loadshed_var_at_exit_nodes_upper[node])
                * self.bigM_for__loadshed_var_at_exit_nodes_upper
                for node in self.exit_nodes_list
            ),
            name="UB_for__loadshed_var_at_exit_nodes_upper",
        )

        UB_for__loadshed_var_at_entry_nodes_lower = self.m.addConstrs(
            (
                self.loadshed_var_at_nodes[node]
                - self.loadshedBounds_at_nodes_dict_dict["LB"][node]
                <= (1.0 - self.binary_var_for__dual_loadshed_var_at_entry_nodes_lower[node])
                * self.bigM_for__loadshed_var_at_entry_nodes_lower
                for node in self.entry_nodes_list
            ),
            name="UB_for__loadshed_var_at_entry_nodes_lower",
        )
        UB_for__loadshed_var_at_entry_nodes_upper = self.m.addConstrs(
            (
                self.loadshedBounds_at_nodes_dict_dict["UB"][node]
                - self.loadshed_var_at_nodes[node]
                <= (1.0 - self.binary_var_for__dual_loadshed_var_at_entry_nodes_upper[node])
                * self.bigM_for__loadshed_var_at_entry_nodes_upper
                for node in self.entry_nodes_list
            ),
            name="UB_for__loadshed_var_at_entry_nodes_upper",
        )


    def test_feasibility_for_given_solution(self, sol_file_path):
        def read_input_file(file_path):
            data = {}
            data["arcs"] = {}
            data["nodes"] = {}
            with open(file_path, "r") as file:
                for line in file:
                    if line.startswith("#") or line.strip() == "":
                        continue
                    parts = line.split()
                    key = parts[0]
                    value = float(parts[1])
                    if "[" in key and "]" in key:
                        var_name, nodes = key.split("[")
                        nodes = nodes.strip("]")
                        if "," in nodes:
                            node_tuple = tuple(nodes.split(","))
                            data["arcs"][(node_tuple, var_name)] = value
                        else:
                            data["nodes"][(nodes, var_name)] = value
            return data

        sol_file_data = read_input_file(sol_file_path)

        ## assuming that we match the right models for feasibility
        ## further assuming that the important vars exist on both sides

        for key, value in sol_file_data["arcs"].items():
            arc, var_name = key
            # print(f"arc: {arc}\n var_name: {var_name} \n value: {value}")
            try:
                variable = self.m.getVarByName(f"{var_name}[{arc[0]},{arc[1]}]")
            except:
                print("failed")
                continue
            # Adding the constraint
            self.m.addConstr(variable == value, name=f"comp_constr_{var_name}_{arc}")

        for key, value in sol_file_data["nodes"].items():
            node, var_name = key
            # print(f"node: {node}\n var_name: {var_name} \n value: {value}")
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
                if f'{"loadshed" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "lambda"}[{n}]' in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
            for a in self.arcs_list:
                if f'{"interdiction" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "x"}[{a[0]},{a[1]}]' in v.VarName:
                    interdiction[a] = int(v.X)
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
        objVal = 0
        interdiction = {}
        for v in self.m.getVars():
            for n in self.exit_nodes_list:
                if f'{"loadshed" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "lambda"}[{n}]' in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
            for a in self.arcs_list:
                if f'{"interdiction" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "x"}[{a[0]},{a[1]}]' in v.VarName:
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
        objVal = 0
        interdiction = {}
        for v in self.m.getVars():
            for n in self.exit_nodes_list:
                if f'{"loadshed" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "lambda"}[{n}]' in v.VarName:
                    objVal += v.X * self.loadflow_at_nodes_dict[n]
            for a in self.arcs_list:
                if f'{"interdiction" if not self.with_mathematical_varnames_instead_of_GRB_model_names else "x"}[{a[0]},{a[1]}]' in v.VarName:
                    interdiction[a] = int(v.X)
        return {"interdiction": interdiction, "objVal": objVal, "Runtime": self.m.Runtime}
     