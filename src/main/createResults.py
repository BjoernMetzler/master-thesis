import itertools
import os
import subprocess

# Definieren Sie die möglichen Werte für jeden Parameter
gas_network_instances = ["GasLib-40"] #"testModel4","GasLib-11",
modes = {"SL": [], "Enum": ["Enum_Approach"]} #"Enum_CC", "SL_CC""SL_SOS1","SL_BigM""Enum_Primal",
scenarios = ["homogen-northEast-randomExits", "homogen-northEast", "homogen-randomExits", "south-randomExits", "homogen-south", "homogen", "northEast-randomExits", "northEast", "randomExits", "randomExits0-200", "scaled-randomExits", "scaled", "south-randomExits", "south",""]
results = {}
Budget = 3

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
            for scenario in scenarios:
                network_instance = gas_network_instance + "," + scenario
                for interdiction_budget in list(range(Budget + 1)):
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
            for scenario in scenarios:
                network_instance = gas_network_instance + "," + scenario
                for interdiction_budget in list(range(Budget + 1)):
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


