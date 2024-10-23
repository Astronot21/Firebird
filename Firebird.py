# ==============================================================================================
# Firebird: FEniCS based thermal analyser tool for cryogenic Integrated Circuits - Skripsie 2024
# Copyright (C) Intellectual Property 2024 - Richard Neill Finn (24756369@sun.ac.za)
# v2.2
# ==============================================================================================


from pathlib import WindowsPath
import click
import parseParams
import parseLayers
import extractGeometry
import heatFlow
import generateOutputFiles
import subprocess


def initialise_logic(gds_file, xml_file, params_file):
    # ---------------------------------------------------------------------------- #
    #         Restart function in case of unsuccessful simulation or setup         #
    # ---------------------------------------------------------------------------- #
    def restart_program():
        response = click.prompt("Do you want to restart the program? [y for yes]", type=str)
        if response.lower() == "y":
            command = f"python Firebird.py {gds_file} {xml_file} {params_file}"
        else:
            print(f"\n\u001b[41;1m=== Exiting program ===\u001b[0m\n")
            command = "exit"
        subprocess.run(command, shell=True, capture_output=False, text=True)

    # --------------------------- Function entry point --------------------------- #
    if params_file is not None:
        try:
            substrate_layer, resist_layer, iterations, delta, ambient_temp, s_sense = parseParams.parse_file(params_file)
        except ValueError: 
            print("\033[91mAn error occured during setup: Values could not be read from paramter file.\033[0m\n")
            restart_program()
        else:
            print("""\033[92m
            +---------------------------------+
            | Extracted simulation parameters |
            +---------------------------------+
            \033[0m""")
            print(f"\nSubstrate layer: {substrate_layer}\nResistor layer: {resist_layer}\nIterations: {iterations}\nDelta: {delta}\nAmbient temperature: {ambient_temp} K")


            # ----------------- Find layout dimensions and resistor data ----------------- #
            layoutLength, layoutWidth, resistor_data = extractGeometry.read_gdsii(gds_file, substrate_layer, resist_layer)

             # ----------------------- Extract substrate properties ----------------------- #
            substrate_layer_properties = parseLayers.get_layer_properties(xml_file, substrate_layer)
            if not type(substrate_layer_properties) == dict:
                print(substrate_layer_properties)

            rho_param = substrate_layer_properties['Density']
            cp_param = substrate_layer_properties['SpecificHeatCapacity']
            k_param = substrate_layer_properties['ThermalConductivity']

            # ---------- Prepare to run simulation if all parameters are correct --------- #
            if int(layoutLength) == 0 or int(layoutWidth) == 0:
                print(f"\n\033[103mDimensions are not workable, please enter a layer with non-zero dimensions.\033[0m\n")
                restart_program()
            else:
                print("""\033[92m
                +-----------------------+
                | Substrate information |
                +-----------------------+
                \033[0m""")
                print(f"Substrate length is {layoutLength} μm and width is {layoutWidth} μm\n")

                # -------------------------------- File names -------------------------------- #
                mesh_file = "layoutMesh.msh"
                geo_file = "layoutMesh.geo"

                # ------ Create geo file, which also creates the mesh file upon opening ------ #
                generateOutputFiles.generate_geo_file(geo_file, layoutLength, layoutWidth, resistor_data, s_sense)
                windows_path = geo_file.replace('/','\\')
                subprocess.run(['explorer.exe', windows_path])

                # --------------------- Function call to start simulation -------------------- #
                try:
                    heatFlow.findHeatSolution(mesh_file, layoutLength, layoutWidth, int(rho_param), int(cp_param), int(k_param), resistor_data, iterations, delta, 1000, ambient_temp)
                except Exception as e:
                    print(f"\033[91mError: There was an error when attempting to simulate: {e}\033[0m")
                    restart_program()

    else:
        # -------------------- If parameter file is NOT specified -------------------- #
        print("\n\033[91mError in simulaiton setup: No parameter file specified.\033[0m\n")
        restart_program()

        

# ---------------------------------------------------------------------------- #
#                                 ROOT FUNCTION                                #
# ---------------------------------------------------------------------------- #
@click.command()
@click.argument('gds_file', type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True))
@click.argument('xml_file', type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True))
@click.argument('params', type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True))
def initialise(gds_file, xml_file, params):
    """Initialise the tool with a required GDSII file, XML LDF file and parameter file."""

    # --------------------------- Print welcome message -------------------------- #
    print(
        """\033[96m 
    ================================================================================================
    Firebird: FEniCS based thermal analyser tool for cryogenic Integrated Circuits - Skripsie 2024
    Copyright (C) Intellectual Property 2024 - Richard Neill Finn (24756369@sun.ac.za)
    v2.2
    ================================================================================================ 
        \033[0m"""
    ) 
    initialise_logic(gds_file, xml_file, params)


if __name__ == '__main__':
    initialise()

