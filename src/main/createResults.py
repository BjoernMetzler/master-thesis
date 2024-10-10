import itertools
import os
import subprocess

# Definieren Sie die möglichen Werte für jeden Parameter
gas_network_instances = ["GasLib-40","GasLib-135-v1-20211130"] #"testModel4","GasLib-11","GasLib-135-v1-20211130"
modes = {"SL": [], "Enum": ["Hybrid_Approach"]} #"Enum_CC", "SL_CC""SL_SOS1","SL_BigM""Enum_Primal",
scenarios = {"GasLib-11": [f'lfset{i+1}' for i in range(20)] + ['standard'],
    "GasLib-40": ["homogen-randomExits", "scaled", "scaled-randomExits"],#"scaled-randomExits",  "standard","scaled" #"homogen-northEast-randomExits", "homogen-northEast","south-randomExits", "homogen-south", "homogen", "northEast-randomExits", "northEast", "randomExits", "randomExits0-200", "scaled-randomExits", "scaled", "south-randomExits", "south"
    "GasLib-134-v2-20211129":["2011-11-01"],
    "GasLib-135-v1-20211130":["standard"]}
results = {}

import csv
import subprocess
import locale
import re

def extract_desired_output(output):
    match = re.search(r"\{'interdiction':.*?('objVal':\s*[\d.]+,\s*'Runtime':\s*[\d.]+)\}", output, re.DOTALL)
    if match:
        return match.group(0)
    return "None"

with open("analysis.csv", 'a', newline='') as file:
    writer = csv.writer(file, delimiter=";")
    
    
    for mode in modes["SL"]:
        for gas_network_instance in gas_network_instances:
            for scenario in scenarios[gas_network_instance]:
                network_instance = gas_network_instance + "," + scenario
                if gas_network_instance == "GasLib-40": 
                    budget_list = list(range(1,2,1))
                elif gas_network_instance == "GasLib-135-v1-20211130":
                    budget_list = list(range(4))
                    
                for interdiction_budget in budget_list:
                    try:
                        result = subprocess.run(
                            f'python ./main.py {network_instance} {mode} {interdiction_budget}', 
                            shell=True, 
                            check=True, 
                            capture_output=True, 
                            text=True
                        )
                        print(result)
                        output = extract_desired_output(result.stdout.strip())
                    except subprocess.CalledProcessError:
                        output = "None"

                    writer.writerow([network_instance, mode, interdiction_budget, output])
                    file.flush()  # Ensure data is written to the file immediately
                    results[f'({network_instance},{mode},{interdiction_budget}'] = output
                    
                    
    for mode in modes["Enum"]:
        for gas_network_instance in gas_network_instances:
            for scenario in scenarios[gas_network_instance]:
                network_instance = gas_network_instance + "," + scenario
                if gas_network_instance == "GasLib-40": 
                    budget_list = list(range(0,5,1))
                elif gas_network_instance == "GasLib-135-v1-20211130":
                    budget_list = list(range(3))
                    
                for interdiction_budget in budget_list:
                    import time

                    # Start the timer
                    start_time = time.time()
                    try:
                        result = subprocess.run(
                            f'python ./main.py {network_instance} {mode} {interdiction_budget}', 
                            shell=True, 
                            check=True, 
                            capture_output=True, 
                            text=True
                        )
                        output = extract_desired_output(result.stdout.strip())
                    except subprocess.CalledProcessError:
                        output = "None"

                    # End the timer
                    end_time = time.time()

                    # Calculate the elapsed time
                    runtime = end_time - start_time
                    
                    output = f'{output}//{locale.format_string("%.16f", runtime, grouping=True)}'
                    
                    writer.writerow([network_instance, mode, interdiction_budget, output])
                    file.flush()  # Ensure data is written to the file immediately
                    results[f'({network_instance},{mode},{interdiction_budget}'] = output
    
    
                
    


