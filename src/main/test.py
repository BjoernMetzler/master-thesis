import os



# Example usage
folder_path = './logs/Enum_Approach/SOL/intBudget_1_instance_GasLib-40/'
interdiction_decision = {('source_1', 'sink_3'): 0, ('innode_1', 'sink_16'): 0, ('innode_6', 'sink_13'): 0, ('sink_13', 'sink_14'): 0, ('sink_14', 'sink_10'): 0, ('sink_25', 'sink_26'): 0, ('sink_26', 'sink_9'): 1, ('sink_9', 'sink_18'): 0, ('sink_26', 'sink_4'): 0, ('sink_4', 'sink_20'): 0, ('sink_18', 'sink_6'): 0, ('sink_25', 'innode_8'): 0, ('sink_6', 'sink_7'): 0, ('sink_6', 'sink_22'): 0, ('sink_7', 'sink_24'): 0, ('sink_22', 'sink_1'): 0, ('sink_24', 'sink_21'): 0, ('sink_21', 'sink_12'): 0, ('sink_7', 'sink_5'): 0, ('sink_5', 'sink_17'): 0, ('sink_17', 'sink_4'): 0, ('sink_17', 'sink_8'): 0, ('sink_3', 'sink_23'): 0, ('sink_8', 'sink_20'): 0, ('sink_25', 'sink_20'): 0, ('sink_25', 'sink_15'): 0, ('sink_15', 'sink_29'): 0, ('sink_29', 'sink_28'): 0, ('sink_29', 'sink_2'): 0, ('sink_2', 'sink_15'): 0, ('sink_29', 'innode_7'): 0, ('innode_4', 'sink_19'): 0, ('sink_19', 'innode_3'): 0, ('innode_4', 'innode_5'): 0, ('sink_27', 'innode_5'): 0, ('sink_27', 'sink_19'): 0, ('sink_10', 'sink_11'): 0, ('sink_10', 'innode_2'): 0, ('sink_10', 'innode_3'): 0, ('innode_6', 'sink_25'): 0, ('sink_11', 'innode_1'): 0, ('sink_19', 'innode_2'): 0, ('source_3', 'innode_4'): 0, ('source_2', 'innode_7'): 0, ('sink_3', 'innode_8'): 0}  # Replace with the specific interdiction decision you are looking for

destination = './logs/Enum_Approach/SOL/intBudget_1_instance_GasLib-40.sol'

result=os.path.join(os.path.dirname(folder_path.rstrip('/')), os.path.basename(folder_path.rstrip('/')) + '.sol')

print(result)


