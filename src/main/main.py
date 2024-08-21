"""
This is only a simple main to give an example
how to parse the instance files
"""

from helpers.network import GasLibNetwork
import assets.lib.gaslibparse.helpers
import sys
import multiprocessing
import time

networkInstanceName = sys.argv[1]

if networkInstanceName != "testModel4":
    
    # path to .scn file
    if networkInstanceName != "GasLib-11":
        if len(sys.argv) == 3:
            scenario = sys.argv[2]
            scn_file = f"./assets/instances/{networkInstanceName}/{networkInstanceName}-{scenario}.scn"
        else:
            scn_file = f"./assets/instances/{networkInstanceName}/{networkInstanceName}.scn"
        
    else:
        scn_file = f"./assets/instances/{networkInstanceName}/{networkInstanceName}.scn"
    

    # path to .net file
    net_file = f"./assets/instances/{networkInstanceName}/{networkInstanceName}.net"

    # now build the network object
    network = GasLibNetwork(net_file, scn_file)
    # create model for data (not complete)
    withoutFlowBounds = False
    network._toPyomo(False)

# display data for the model
'''displayModes = ["cmi","teXt","json"]
lib.gaslibparse.helpers.print_pyomoData(network.pyomoData[None], displayModes, networkInstanceName)'''

if networkInstanceName != "testModel4":
    data = network.pyomoData[None] 
else:
    data = {
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


from CURRENT_MODELS import *

if (len(sys.argv) >= 4):
    Budget = int(sys.argv[3])


if (len(sys.argv) >= 3):
    mode = sys.argv[2]


def run_method(mode, data, networkInstanceName, Budget):
    if mode == "SL_SOS1":
        model = Single_Level_Formulation(data, networkInstanceName, False, Budget)
        result= model.single_level_model_SOS1()
    elif mode == "SL_CC":
        model = Single_Level_Formulation_Model(data, networkInstanceName, False, Budget)
        result= model.single_level_model_CC()
    elif mode == "SL_BigM":
        #run_method("Enum_BigM", data, networkInstanceName, Budget)
        model = Single_Level_Formulation_Model(data, networkInstanceName, False, Budget)
        result= model.single_level_model_BigM()
    """elif mode == "Enum_Primal":
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
    """
    print(result["interdiction"])
    network.plot_interdiction(result['interdiction'])

p = multiprocessing.Process(target=run_method, args=(mode, data, networkInstanceName, Budget))
p.start()

# Wait for 3600 seconds (1 hour)
p.join(timeout=3600)

# Terminate the process if it's still running
if p.is_alive():
    p.terminate()
    print("Method execution timed out after 3600 seconds.")
else:
    print("Method executed successfully within 3600 seconds.")

