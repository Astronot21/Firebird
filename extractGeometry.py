from curses import reset_shell_mode
import gdspy
import numpy as np

def read_gdsii(file_path, main_layer, resistive_layer):
    '''
    Reads the layout of a given GDSII file and returns the dimensions of the substrate layer
    and the resistor polygons on the resistive layer. Resistor data includes power dissipation,
    position, polygon dimensions, and bounds (specific to each resistor).
    '''
    split_item = "#"
    gdsii_lib = gdspy.GdsLibrary(infile=file_path)
    top_level_cells = gdsii_lib.top_level()

    # Create empty dictionary to store resistor data
    resistor_data = {}

    # Initialize substrate dimensions
    substrate_length = 0
    substrate_width = 0

    for cell in top_level_cells:
        # Extract polygons and labels
        polygons = cell.get_polygons(by_spec=True)
        texts = cell.get_labels()

        # Loop through polygons on the resistive layer and substrate layer
        for (layer, datatype), polygon_list in polygons.items():
            # Process the resistive layer for resistor data
            if layer == resistive_layer:
                for polygon in polygon_list:
                    # Calculate the center of the polygon
                    polygon_center = np.mean(polygon, axis=0)

                    # Calculate the dimensions (length, width)
                    min_x, max_x = np.min(polygon[:, 0]), np.max(polygon[:, 0])
                    min_y, max_y = np.min(polygon[:, 1]), np.max(polygon[:, 1])
                    length = max_x - min_x
                    width = max_y - min_y

                    # Define bounds (corners) of the polygon
                    bounds = {
                        'x_min': min_x,
                        'x_max': max_x,
                        'y_min': min_y,
                        'y_max': max_y
                    }

                    # Create an entry in the resistor_data dictionary for this resistor
                    resistor_entry = {
                        'position': polygon_center,
                        'length': length,
                        'width': width,
                        'bounds': bounds
                    }

                    # Find the corresponding label for this resistor
                    for text in texts:
                        label_text = text.text
                        label_position = text.position

                        # Check if the label position falls within the bounds of this polygon
                        if (bounds['x_min'] <= label_position[0] <= bounds['x_max'] and
                                bounds['y_min'] <= label_position[1] <= bounds['y_max']):
                            if split_item in label_text:
                                try:
                                    resistor_number, power_dissipation = label_text.split(split_item)
                                    resistor_entry['resistor_number'] = int(resistor_number)
                                    resistor_entry['power_dissipation'] = float(power_dissipation)
                                    break # avoid unnecessary iterations
                                except ValueError:
                                    print(f"Error processing label: {label_text}")
                        

                    # Add the resistor entry to the dictionary
                    resistor_data[tuple(polygon_center)] = resistor_entry

            # Process the main layer for substrate dimensions
            if layer == main_layer:
                for polygon in polygon_list:
                    # Calculate substrate dimensions based on the polygon bounds
                    min_x, max_x = np.min(polygon[:, 0]), np.max(polygon[:, 0])
                    min_y, max_y = np.min(polygon[:, 1]), np.max(polygon[:, 1])

                    # Update the substrate length and width
                    substrate_length = max(substrate_length, max_x - min_x)
                    substrate_width = max(substrate_width, max_y - min_y)

    # -------------- Order the data in terms of the resistor numbers ------------- #
    sorted_resistor_data = dict(sorted(resistor_data.items(), key=lambda item: item[1]['resistor_number'], reverse=False))
    # -------- Print the resulting resistor data and substrate dimensions -------- #
    print_resistor_data(sorted_resistor_data)

    return substrate_length, substrate_width, sorted_resistor_data


def print_resistor_data(resistor_data):
    '''Prints the resistor data including the number, power dissipation, position, and dimensions.'''
    print("""\033[92m
    +----------------------------------------------+
    | Resistor Data: Number, Power, Position, Flux |
    +----------------------------------------------+
    \033[0m""")
    for key, resistor in resistor_data.items():
        flux = resistor.get('power_dissipation','N/A') / (resistor['length'] * resistor['width'])
        print(f"Resistor {resistor.get('resistor_number', 'N/A')}: "
              f"Power = {resistor.get('power_dissipation', 'N/A')} μW, "
              f"Position = {resistor['position']}, "
              f"Length = {resistor['length']} μm, Width = {resistor['width']} μm, "
              f"Flux = {flux:.4f} W/m^2")
