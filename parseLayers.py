import xml.etree.ElementTree as ET

def get_layer_properties(xml_file, layer_num : int):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for layer in root.findall('layer'):
            num = layer.find('LayerNumber')

            if num is not None and num.text == str(layer_num):
                material = layer.find('Material').text
                thickness = layer.find('Thickness').text
                thermal_conductivity = layer.find('ThermalConductivity').text
                specific_heat = layer.find('SpecificHeatCapacity').text
                density = layer.find('Density').text

                # Returns a dictionary containing all the relevant material properties
                return {
                    'LayerNumber': num,
                    'Material': material,
                    'Thickness': thickness,
                    'ThermalConductivity': thermal_conductivity,
                    'SpecificHeatCapacity': specific_heat,
                    'Density': density
                }
        return f"Layer number {layer_num} not found in the XML file."
    except ET.ParseError as e:
        return f"Error parsing XML: {e}"