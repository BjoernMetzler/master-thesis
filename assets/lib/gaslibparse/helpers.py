def write_to_txt(data, instance_name):
    """
    Writes the given data to a text file with the specified instance name,
    formatting it with proper indentation to mimic JSON structure.

    Parameters:
    data (dict): The data to write to the file.
    instance_name (str): The name of the network instance for the filename.
    """
    file_name = f"{instance_name}.txt"

    def format_dict(d, indent=0):
        """Recursively formats a dictionary."""
        for key, value in d.items():
            if isinstance(key, tuple):
                key = ' - '.join(map(str, key))
            padding = ' ' * indent
            if isinstance(value, dict):
                file.write(f'{padding}"{key}": {{\n')
                format_dict(value, indent + 4)
                file.write(f'{padding}}},\n')
            elif isinstance(value, list):
                file.write(f'{padding}"{key}": [\n')
                format_list(value, indent + 4)
                file.write(f'{padding}],\n')
            else:
                file.write(f'{padding}"{key}": "{value}",\n')

    def format_list(l, indent=0):
        """Recursively formats a list."""
        for item in l:
            padding = ' ' * indent
            if isinstance(item, dict):
                file.write(f'{padding}{{\n')
                format_dict(item, indent + 4)
                file.write(f'{padding}}},\n')
            elif isinstance(item, list):
                file.write(f'{padding}[\n')
                format_list(item, indent + 4)
                file.write(f'{padding}],\n')
            else:
                file.write(f'{padding}"{item}",\n')

    with open(file_name, 'w') as file:
        file.write("{\n")
        format_dict(data, 4)
        file.write("}\n")

    print(f"Data has been written to {file_name}")
    
import json

def tuple_keys_to_strings(data):
    """
    Recursively converts all dictionary keys that are tuples into strings.

    Parameters:
    data (dict): The data with potential tuple keys.

    Returns:
    dict: The data with all tuple keys converted to strings.
    """
    if isinstance(data, dict):
        return {str(k) if isinstance(k, tuple) else k: tuple_keys_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [tuple_keys_to_strings(i) for i in data]
    else:
        return data

def convert_tuples_to_strings(data):
    # Convert tuples in arcs to strings
    for key, value in data["arcs"].items():
        data["arcs"][key] = [f"('{arc[0]}', '{arc[1]}')" for arc in value]
        
        
def write_to_json(data, instance_name):
    """
    Writes the given data to a JSON file with the specified instance name,
    ensuring all tuple keys are converted to strings.

    Parameters:
    data (dict): The data to write to the file.
    instance_name (str): The name of the network instance for the filename.
    """
    # Pre-process data to convert tuple keys to strings
    data = tuple_keys_to_strings(data)
    convert_tuples_to_strings(data)
    
    file_name = f"{instance_name}.json"
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data has been written to {file_name}")
    
def print_pyomoData(data: dict, mode: list, networkInstanceName: str):
    mode = [mode[i].lower() for i in range(len(mode))]
    ## as print in the CMI
    if "cmi" in mode:
        print(data)
    ## as txt in a separate file
    if "txt" in mode or "text" in mode:
        write_to_txt(data, networkInstanceName)
    if "json" in mode:
    ## as json in a separate file
        write_to_json(data, networkInstanceName)
