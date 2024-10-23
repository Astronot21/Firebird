import re

def parse_file(file_name):
    '''
    Takes in a path to a text file containing the parameter values to be used in simulation. The file has to be in the specified format.
    '''
    print(f"\nParameter File to extract: \033[95m{file_name}\033[0m")
    with open(file_name, 'r') as file:
        text = file.read()

    # Use regular expressions to extract the values of parameters
    delta_match = re.search(r'delta=([0-9\.]+)', text)
    substrate_match = re.search(r'substrate=([0-9\.]+)',text)
    resist_match = re.search(r'resist=([0-9\.]+)',text)
    iterations_match = re.search(r'iterations=([0-9\.]+)',text)
    ambient_temp_match = re.search(r'ambient=([0-9\.]+)',text)
    substrate_sensitivity_match = re.search(r's_sense=([0-9\.]+)',text)

    # ---------------- Check if all parameters have been obtained ---------------- #
    if delta_match and substrate_match and resist_match and iterations_match and ambient_temp_match and substrate_sensitivity_match:
        delta = float(delta_match.group(1)) # time step value
        substrate = int(substrate_match.group(1)) # substrate layer
        resist = int(resist_match.group(1)) # resistor layer
        iterations = int(iterations_match.group(1)) # number of iterations
        ambient_temp = float(ambient_temp_match.group(1)) # in Kelvin
        substrate_sensitivity =  float(substrate_sensitivity_match.group(1)) # ex. 20e-1

        # ------------------------------ Error checking ------------------------------ #
        if substrate_sensitivity <= 0:
            print(f"\nError: Substrate mesh sensitivity value must contain positive integer value. Check parameter file.\n")
            raise ValueError()

        if substrate != resist:
            if delta <=0 or iterations <= 0:
                print(f"\nError: Number of iterations and delta value must contain positive integer values. Check parameter file.\n")
                raise ValueError()
            else:
                return substrate, resist, iterations, delta, ambient_temp, substrate_sensitivity
        else:
            print(f"\nError: Substrate and resistive layer cannot be on the same layer. Check parameter file.\n")
            raise ValueError()
    
    
    else:
        raise ValueError("Could not parse parameters from file")
