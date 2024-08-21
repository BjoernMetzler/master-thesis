# Global imports
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import logging

from helpers.loggerFilter import DuplicateFilter

from pyomo.environ import SolverFactory, value

from assets.lib.gaslibparse import GasLibParserUnits, Pipe,  \
    CompressorStation, ControlValve, Valve, Resistor, ShortPipe, \
    Entry, Exit, unit

logger = logging.getLogger(__name__)
logger.addFilter(DuplicateFilter())





class GasLibNetwork(object):
    """
    Constructs a GasLib Network with corresponding scenario
    while considering Methane transport and an average temperature
    of 283 K.
    Methane constant are chosen according to thermopedia.com
    """

    def __init__(self, net_file, scn_file, interdictionBudget=0):
        # Methane R_s in J/(kg K)
        self.specificGasConstant = np.float64(
            581.28) * unit.J / (unit.kg * unit.K)
        # Methane pseudo-critical pressure p_c in bar
        self.pseudocriticalPressure = np.float64(45.95) * unit.bar
        # Methan pseudo-critical temperature T_c in K
        self.pseudocriticalTemperature = np.float64(190.55) * unit.K
        # average temperature of 283.15 K
        self.meanTemperature = np.float64(283.15) * unit.K
        # methane density
        self.normDensity = np.float64(0.785) * unit.kg / (unit.m ** 3)

        # maximum number of arcs that can be interdicted
        self.interdictionBudget = interdictionBudget

        parser = GasLibParserUnits(net_file, scn_file)
        parser.parse()

        # nodes of the networks
        self.nodes = {
            **parser.innode_data,
            **parser.entry_data,
            **parser.exit_data
        }
            
        self.innodes = parser.innode_data
        self.entries = parser.entry_data
        self.exits = parser.exit_data

        # all arcs of the network
        self.arcs = {
            **parser.pipe_data,
            **parser.compressor_station_data,
            **parser.control_valve_data,
            **parser.valve_data,
            **parser.short_pipe_data,
            **parser.resistor_data
        }

        # passive arcs
        self.passiveArcs = {
            **parser.pipe_data,
            **parser.short_pipe_data,
            **parser.resistor_data,
            **parser.valve_data  # here valve is passive because not modelled
        }
        
        
        # active arcs
        self.activeArcs = {
            **parser.compressor_station_data,
            **parser.control_valve_data,
        }
        self.pipes = parser.pipe_data
        self.compressors = parser.compressor_station_data
        self.controlValves = parser.control_valve_data,
        self.valves = parser.valve_data,
        self.shortPipe = parser.short_pipe_data,
        self.resistors = parser.resistor_data

        self.network = nx.MultiDiGraph(name=parser.net_name)

        # given load flow, nomination
        self.loadflow = {}

        # contains all data necessary for pyomo model
        self.pyomoData = {}

        # Fill in information: nodes, arcs + attributes to graph for natural gas network
        self._populate()

        # # # plot graph
        self.plot()
        

    def _populate(self) -> None:
        # add all nodes
        for nodeId, nodeData in self.nodes.items():
            self.network.add_node(nodeId, data=nodeData)
        # add passive arcs
        for arcData in self.passiveArcs.values():
            self.network.add_edge(
                arcData.from_node, arcData.to_node, data=arcData)

        # add active elements to network (later replaced by shortpipes)
        for arcData in self.activeArcs.values():
            self.network.add_edge(
                arcData.from_node, arcData.to_node, data=arcData)


        # check that graph is weakly connected
        logger.debug("Number of weakly connected components: {}".format(
            nx.number_weakly_connected_components(self.network)))
        assert(nx.is_weakly_connected(self.network))


    def plot(self) -> None:
        # set position of nodes
        pos = {}
        for node in self.nodes.values():
            pos[node.node_id] = np.array(node.pos)
#        nx.draw(self.network, pos, node_size=30, labels=self.loadflow)
        nx.draw(self.network, pos, node_size=5, with_labels=True, font_size=5, edge_color="b")
#        plt.show()
        # path to store file
        plt.savefig("gasNetwork.png", format="PNG", dpi=1200)


    def plot_interdiction(self, interdiction):
        """
        here we plot the network in which we mark the interdicted arcs by
        interdiction is dictionary key arc, value 0/1; 0 non-interdicted, 1 interdicted
        """
        # we build the network from scratch so that we can separately color the interdicted arcs
        # add all nodes
        interdicted_network = nx.MultiDiGraph()

        for nodeId, nodeData in self.nodes.items():
            interdicted_network.add_node(nodeId, data=nodeData)

        # add passive arcs
        for arcData in self.passiveArcs.values():
            tmp_arc = (arcData.from_node, arcData.to_node)
            if interdiction[tmp_arc] == 1.0:
                # mark arc with color red
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "red")
            else:interdicted_network = nx.MultiDiGraph()

        for nodeId, nodeData in self.nodes.items():
            interdicted_network.add_node(nodeId, data=nodeData)

        # add passive arcs
        for arcData in self.passiveArcs.values():
            tmp_arc = (arcData.from_node, arcData.to_node)
            if interdiction[tmp_arc] == 1.0:
                # mark arc with color red
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "red")
            else:
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "black")



        # add active elements to network (later replaced by shortpipes)
        for arcData in self.activeArcs.values():
            tmp_arc = (arcData.from_node, arcData.to_node)
            if interdiction[tmp_arc] == 1.0:
                # mark arc with color red
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "red")
            else:
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "black")

        # # check that graph is weakly connected
        # logger.debug("Number of weakly connected components: {}".format(
        #     nx.number_weakly_connected_components(interdicted_network)))
        # assert(nx.is_weakly_connected(interdicted_network))

        pos = {}
        for node in self.nodes.values():
            pos[node.node_id] = np.array(node.pos)

        edge_color_list = []
        # keys is counter for parallel arcs, as far as I understand
        for u, v, keys, color in interdicted_network.edges(data="color", keys=True):
            edge_color_list.append(color)

        nx.draw(interdicted_network, pos, node_size=5, with_labels=True, font_size=5, \
                edge_color = edge_color_list)
        plt.show()



        # add active elements to network (later replaced by shortpipes)
        for arcData in self.activeArcs.values():
            tmp_arc = (arcData.from_node, arcData.to_node)
            if interdiction[tmp_arc] == 1.0:
                # mark arc with color red
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "red")
            else:
                interdicted_network.add_edge(
                    arcData.from_node, arcData.to_node, color = "black")

        # # check that graph is weakly connected
        # logger.debug("Number of weakly connected components: {}".format(
        #     nx.number_weakly_connected_components(interdicted_network)))
        # assert(nx.is_weakly_connected(interdicted_network))

        pos = {}
        for node in self.nodes.values():
            pos[node.node_id] = np.array(node.pos)

        edge_color_list = []
        # keys is counter for parallel arcs, as far as I understand
        for u, v, keys, color in interdicted_network.edges(data="color", keys=True):
            edge_color_list.append(color)

        nx.draw(interdicted_network, pos, node_size=5, with_labels=True, font_size=5, \
                edge_color = edge_color_list)
        plt.show()
        
        



    def frictionFactor(self, pipe):
        """
        Determines the frictionFactor of a pipe using Nikuradse's
        approximation,
        lambda(q) = (2log_10(D/k) + 1.138)^{-2}
        see (2.19) Chapter 2 book Koch et al. 2015
        """
        if not isinstance(pipe, Pipe):
            pipe = self.pipes[pipe]
        return (2 * np.log10(pipe.diameter / pipe.roughness) + 1.138)**(-2)


    def meanPressure(self, pipe):
        """
        Determines an approximate of the meanPressure; unit tracked by pint.
        We use state independent formula,
        see (10.23a) Chapter 7 book Koch et al.
        """
        if not isinstance(pipe, Pipe):
            pipe = self.pipes[pipe]
        u = self.nodes[pipe.from_node]
        v = self.nodes[pipe.to_node]
        return (max(u.pressure_min, v.pressure_min) +
                min(u.pressure_max, v.pressure_max)) / 2


    def reducedMeanPressure(self, pipe):
        """
        reduced mean pressure necessary for computation of
        mean compressibilityFactor by Papay.
        """
        return self.meanPressure(pipe) / self.pseudocriticalPressure


    def reducedMeanTemperature(self):
        """
        reduced mean temperature for computation of
        mean compressibilityFactor by Papay
        """
        return self.meanTemperature / self.pseudocriticalTemperature


    def meanCompressibilityFactorPapay(self, pipe):
        """
        Determines the mean compressibilityFactor with
        the Papay formula,
        z(p_m,T_m)=1 - 3.52 p_m/p_c exp(-2.26 T_m/T_c)
                 + 0.274 (p_m/p_c)^2 exp(-1.878 T_m/T_c)
        see (2.4) Chapter 2 book Koch et al.
        """
        return 1 - 3.52 * self.reducedMeanPressure(pipe) * \
            np.exp(-2.26 * self.reducedMeanTemperature()) + \
            0.274 * self.reducedMeanPressure(pipe)**2 * \
            np.exp(-1.878 * self.reducedMeanTemperature())

    def crosssectionalArea(self, pipe):
        """
        Determines the area of a cross-section of a pipe.
        """
        if not isinstance(pipe, Pipe):
            pipe = self.pipes[pipe]
        return (np.pi / 4) * pipe.diameter**2


    def meanCompressibilityFactorAGA(self, pipe):
        """
        Determines the mean compressibilityFactor with
        the AGA formula,
        z(p_m,T_m)=1 + 0.257 p_m/p_c - 0.533 (p_m/p_c)/(T_m/T_c)
        see (2.5) Chapter 2 book Koch et al.
        """
        return 1 + 0.257 * self.reducedMeanPressure(pipe) \
            - 0.533 * self.reducedMeanPressure(pipe) \
            / self.reducedMeanTemperature()


    def pressureLossFactor(self, pipe):
        """
        Determines the pipe specific pressure loss factor.
        according to (2.25) and Lemma 2.2 of Chapter 2 in book Koch et. al. 2015
        units are tracked by pint
        """
        if not isinstance(pipe, Pipe):
            pipe = self.pipes[pipe]
        return self.frictionFactor(pipe) * self.specificGasConstant * \
            self.meanCompressibilityFactorAGA(pipe) * self.meanTemperature * \
            pipe.length / (pipe.diameter * self.crosssectionalArea(pipe)**2)



    def flowBoundsTotalLoad(self, boolFlowboundsInstance, arc, tupleArc):
        """
        if boolFlowboundsInstance is true, then we consider flow bounds of gaslib.
        Then, we try to tighten the flow bounds by
        we set massflowLB = max(-0.5 sum(loadflow), flowboundLB_gaslib)
        and massflowUB = min(0.5 sum(loadflow), flowboundUB_gaslib)
        if boolFlowboundsInstance is false, then we set
        massflowLB = -0.5 sum(loadflow) and massflowUB = 0.5 sum(loadflow)
        """
        maxFlowLoadflow = 0.5 *sum(self.pyomoData[None]['loadflow'].values())
        if boolFlowboundsInstance:
            logger.info("We consider flow bounds of network and possibly tighten them")
            # we first get flowbounds of gaslib
            self.pyomoData[None]['massflowUb'][tupleArc] = \
                (arc.flow_max * self.normDensity).to(unit.kg/ unit.second)\
                                                 .magnitude
            self.pyomoData[None]['massflowLb'][tupleArc] = \
                (arc.flow_min * self.normDensity).to(unit.kg/ unit.second)\
                                                 .magnitude
            # we check that lower and upper arc flow bounds satisfy assumption:
            # massflowLb < 0 < massflowUb
            assert(self.pyomoData[None]['massflowUb'][tupleArc] > 0)
            assert(self.pyomoData[None]['massflowLb'][tupleArc] < 0)

            logger.info("We tighten flow bounds by maximal flow within load flow")
            if self.pyomoData[None]['massflowUb'][tupleArc] > maxFlowLoadflow:
                logger.debug("We tighten upper arc flow bound from {} to {}".format(
                    self.pyomoData[None]['massflowUb'][tupleArc], maxFlowLoadflow))
                self.pyomoData[None]['massflowUb'][tupleArc] = maxFlowLoadflow
            if self.pyomoData[None]['massflowLb'][tupleArc] < -maxFlowLoadflow:
                logger.debug("We tighten lower arc flow bound from {} to {}".format(
                    self.pyomoData[None]['massflowLb'][tupleArc], -maxFlowLoadflow))
                self.pyomoData[None]['massflowLb'][tupleArc] = -maxFlowLoadflow
            assert(self.pyomoData[None]['massflowUb'][tupleArc] > 0)
            assert(self.pyomoData[None]['massflowLb'][tupleArc] < 0)

        else:
            # we do not consider flow bounds of the Gaslib
            # set lower and upper flow bounds
            logger.info("We do not consider flow bounds of network")
            self.pyomoData[None]['massflowUb'][tupleArc] = maxFlowLoadflow
            self.pyomoData[None]['massflowLb'][tupleArc] = -maxFlowLoadflow
            assert(self.pyomoData[None]['massflowUb'][tupleArc] > 0)
            assert(self.pyomoData[None]['massflowLb'][tupleArc] < 0)

        return



    def _toPyomo(self, boolFlowBounds, interdictionSol = None, loadflowNotScn = None):
        """
        Extract necessary information for pyomo models according to the
        raw_dicts entry in the pyomo documentation.

        Flows are transformed to mass flow by multiplication with
        normDensity.
        Units:
          [massflow] kg/second
          [pressureLossFactor] bar**2/(kg**2/second**2)
          [pressure] bar

        interdictionSol, if given, is a dict key: arc;
        value: 0 (not interdicted) or 1 (interdicted)
        loadflowNotScn if given means we consider different loadflow than in .scn file
        boolFlowBounds is true if the consider flow bounds of .net otherwise false
        """
        self.pyomoData[None] = {}

        # interdictionBudget is maximal number of arcs that can be interdicted
        self.pyomoData[None]['interdictionBudget'] = {None:self.interdictionBudget}

        self.pyomoData[None]['nodes'] = {None: list(self.nodes.keys())}

        # sigma equals 1 for entries, -1 for exits, and 0 for inner nodes
        self.pyomoData[None]['sigma'] = {}
        self.pyomoData[None]['loadflow'] = {}
        self.pyomoData[None]['pressureLb'] = {}
        self.pyomoData[None]['pressureUb'] = {}

        # original follower problem: lower bound loadshed can be negativ
        # set lbLoadShed entries to (entry.flow_max -loadflow[entry])/loadflow[entry]
        self.pyomoData[None]['loadshedLB'] = {}


        # store loadflow that checks if graph is weakly connected after interdiction
        # first choose an entry that sends to each other node of the one unit flow
        superSource = None
        for nodeId, node in self.nodes.items():
            if isinstance(node, Entry):
                superSource = nodeId
                break
        self.pyomoData[None]['weaklyConnectedLoadflow'] = {}
        # we directly set value of superSource: number of nodes -1
        self.pyomoData[None]['weaklyConnectedLoadflow'][superSource] = \
            len(self.pyomoData[None]['nodes'][None]) -1
        logger.debug("Super source for connected graph {} with load {}".format(\
                    superSource, self.pyomoData[None]['weaklyConnectedLoadflow'][superSource]))



        for nodeId, node in self.nodes.items():
            # save lower and upper pressure bounds in bar
            self.pyomoData[None]['pressureLb'][nodeId] = node.pressure_min.to(
                unit.bar).magnitude
            self.pyomoData[None]['pressureUb'][nodeId] = node.pressure_max.to(
                unit.bar).magnitude

            if isinstance(node, Entry):
                self.pyomoData[None]['sigma'][nodeId] = 1
                # check that lower and upper load flow bound are the same
                # logger.debug("Check that lower and upper nomination" \
                #             + " bounds are the same")
                assert((node.nomination_min * self.normDensity).to(
                         unit.kg / unit.second).magnitude
                       ==
                       (node.nomination_max * self.normDensity).to(
                         unit.kg / unit.second).magnitude)
                # set loadflow to upper nomination bound
                # note that previsous assert guarantees lower=upper bound
                # if no nomination is given in function to pyomo, we use the one of the .scn file
                if loadflowNotScn == None:
                    self.pyomoData[None]['loadflow'][nodeId] = \
                        (node.nomination_max *
                         self.normDensity).to(
                             unit.kg / unit.second
                         ).magnitude
                else:
                    # we set loadflow to given nomination
                    self.pyomoData[None]['loadflow'][nodeId] = loadflowNotScn[str(nodeId)]

                # original follower problem: lb loadshed can be negativ for entries
                # because entries can sent more flow than in original nomination
                # set lbLoadShed = -(entry.flow_max -loadflow[entry])/loadflow[entry]
                # except loadflow is zero then loadflowlb is zero as well
                if self.pyomoData[None]['loadflow'][nodeId] == 0.0:
                    self.pyomoData[None]['loadshedLB'][nodeId] = 0.0
                else:
                    self.pyomoData[None]['loadshedLB'][nodeId] = \
                    -((node.flow_max *self.normDensity).to(unit.kg / unit.second).magnitude \
                     - self.pyomoData[None]['loadflow'][nodeId])\
                     /(self.pyomoData[None]['loadflow'][nodeId])

            if isinstance(node, Exit):
                self.pyomoData[None]['sigma'][nodeId] = -1
                # set loadflow to upper nomination bound
                # note that previsous assert guarantees lower=upper bound
                # if no nomination is given in function to pyomo, we use the one of the .scn file
                if loadflowNotScn == None:
                    self.pyomoData[None]['loadflow'][nodeId] = \
                        (node.nomination_max *
                         self.normDensity).to(
                             unit.kg / unit.second
                         ).magnitude
                else:
                    # we set loadflow to given nomination
                    self.pyomoData[None]['loadflow'][nodeId] = loadflowNotScn[str(nodeId)]

                # original follower problem: lb loadshed is zero for exits
                # exits cannot increase their demand
                self.pyomoData[None]['loadshedLB'][nodeId] = 0.0


            # we set load flow to check that graph is weakly connected after interdiction
            # if node is not superSource then demand is -1
            if nodeId != superSource:
                self.pyomoData[None]['weaklyConnectedLoadflow'][nodeId] = -1.0

        # we check that loadflow is balanced
        # sum of entry loads
        loadEntries = sum(self.pyomoData[None]['loadflow'][nodeId] \
                          for nodeId, node in self.nodes.items() \
                          if nodeId in self.pyomoData[None]['sigma'].keys() and \
                          self.pyomoData[None]['sigma'][nodeId] == 1)
        # sum of exit loads
        loadExits = sum(self.pyomoData[None]['loadflow'][nodeId] \
                          for nodeId, node in self.nodes.items() \
                          if nodeId in self.pyomoData[None]['sigma'].keys() and \
                          self.pyomoData[None]['sigma'][nodeId] == -1)
        logger.debug("Total load of injection is {}".format(loadEntries))
        logger.debug("Total load of withdrawl is {}".format(loadExits))
        logger.info("Absolute difference between total injections" \
                    + " and withdrawals is {}".format(abs(loadEntries-loadExits)))

        # here arcs are pipes + active elements that we replace by shortPipes
        self.pyomoData[None]['arcs'] = {None: []}
        self.pyomoData[None]['pressureLossFactor'] = {}
        # active elements will be replaced by shortpipes in the model
        self.pyomoData[None]['activeElements'] = {None: []}
        self.pyomoData[None]['massflowLb'] = {}
        self.pyomoData[None]['massflowUb'] = {}



        for arcId, arc in self.arcs.items():
            tupleArc = (arc.from_node, arc.to_node)

            # for each pipe we compute pressureLossFactor
            if isinstance(arc, Pipe):
                self.pyomoData[None]['arcs'][None].append(tupleArc)
                self.pyomoData[None]['pressureLossFactor'][tupleArc] = \
                    self.pressureLossFactor(arc).to(
                        unit.bar**2 / (unit.kg**2 / unit.second**2)
                    ).magnitude
                # we get lower and upper flow bounds
                # if boolFlowBounds is true, we consider flow bounds of gaslib and tighten
                # them with maxFlow in given loadflow
                # if bool is false, we do not consider flow bounds of gaslib and
                # only use maxFlow within given load flow
                # maxflow is given by total amount of injections, respectively withdrawls
                self.flowBoundsTotalLoad(boolFlowBounds, arc, tupleArc)


            # if arc is compressor, control valve, valve, or resistor, we
            # consider it as shortPipe -> pressureLossFactor = 0.0
            # we set massflowLb:= -0.5 sum(load flow) < 0.5 sum(load flow) =:massflowUb
            # since loadflow >=0 for each node and 0.5 sum(load flow) = sum_exits(load flow)
            # we note that the flow does not exceed these flow bounds since
            # passive potential based flows do not contain cycles
            elif isinstance(arc, CompressorStation) or isinstance(arc, ControlValve) \
                 or isinstance(arc, Valve) or \
                 isinstance(arc, Resistor):
                # logger.debug("We have active elements of type: {}".format(type(arc)) \
                #             + " for arc {}".format(arc.arc_id))
                logger.debug("We have active elements of type: {}".format(type(arc)))

                self.pyomoData[None]['arcs'][None].append(tupleArc)
                self.pyomoData[None]['pressureLossFactor'][tupleArc] = 0.0

                # now we set valid lower and upper flow bounds
                self.pyomoData[None]['massflowUb'][tupleArc] = \
                    0.5 *sum(self.pyomoData[None]['loadflow'].values())

                self.pyomoData[None]['massflowLb'][tupleArc] = -1.0*\
                    0.5 *sum(self.pyomoData[None]['loadflow'].values())


            elif isinstance(arc, ShortPipe):
                # handle this case analogously to compressors
                logger.debug("We have shortPipes: {}".format(arc.arc_id) \
                            + " for arc {}".format(arc.arc_id))
                self.pyomoData[None]['arcs'][None].append(tupleArc)
                self.pyomoData[None]['pressureLossFactor'][tupleArc] = 0.0

                # now we set valid lower and upper flow bounds
                self.pyomoData[None]['massflowUb'][tupleArc] = \
                    0.5 *sum(self.pyomoData[None]['loadflow'].values())

                self.pyomoData[None]['massflowLb'][tupleArc] = \
                    -0.5 *sum(self.pyomoData[None]['loadflow'].values())

            # actually we have considered all pipeline elements
            else:
                raise TypeError("We do not support type " + str(type(arc) + \
                                "of arc " + str(arc)))

        # if interdictionSol is given, we set parameter for interdictionSol that will fix the
        # interdiction decision later in the follower problem
        if interdictionSol != None:
            self.pyomoData[None]['interdictionSol'] = {}
            # if given we set solution for interdiction variables
            self.pyomoData[None]['interdictionSol'] = {}
            for arc in self.pyomoData[None]['arcs'][None]:
                # we round so that we have really zero - one values
                self.pyomoData[None]['interdictionSol'][arc] = int(round(interdictionSol[str(arc)],0))
