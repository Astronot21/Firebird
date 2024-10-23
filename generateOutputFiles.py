from urllib import response
from dolfinx.io import gmshio
from mpi4py import MPI


def write_legacy_vtk(filename, msh, temperature_data, step, current_time):
    with open(filename, "w") as f:
        # Header
        f.write("# vtk DataFile Version 3.0\n")
        f.write(f"Transient thermal analysis data for step {step} and time {current_time}s\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n")

        # Write points (mesh nodes)
        num_points = msh.geometry.x.shape[0]
        f.write(f"POINTS {num_points} float\n")
        for point in msh.geometry.x:
            f.write(f"{point[0]} {point[1]} 0.0\n")  # z = 0.0 for 2D mesh

        # Write cells (triangles)
        num_cells = msh.topology.index_map(msh.topology.dim).size_local
        cell_connectivity = msh.topology.connectivity(2, 0).array
        f.write(f"CELLS {num_cells} {num_cells * 4}\n")  # "4" includes 3 vertices + count of vertices
        for i in range(0, len(cell_connectivity), 3):
            f.write(f"3 {cell_connectivity[i]} {cell_connectivity[i+1]} {cell_connectivity[i+2]}\n")

        f.write(f"CELL_TYPES {num_cells}\n")
        for _ in range(num_cells):
            f.write("5\n")  # "5" is the VTK type for triangle

        # Write temperature data as point data
        f.write(f"POINT_DATA {num_points}\n")
        f.write("SCALARS temperature float 1\n")
        f.write("LOOKUP_TABLE default\n")
        for temp in temperature_data.x.array:
            f.write(f"{temp}\n")


def generate_geo_file(filename: str, substrate_length: float, substrate_width: float, resistor_data: dict, s_sense: float):
    """
    Generates a GMSH .geo file that represents the substrate with resistors.
    The substrate is created as a surface, and resistors are placed into cut-out holes within the substrate.
    
    Args:
    filename (str): The name of the .geo file to be created.
    substrate_length (float): The length of the substrate layer.
    substrate_width (float): The width of the substrate layer.
    resistor_data (dict): The resistor data, where each entry contains:
                          - 'position': (x, y) center of the resistor
                          - 'length': Length of the resistor
                          - 'width': Width of the resistor
    s_sense (float): The sensitivity value of the mesh generation for the substrate layer.
    """
    geo_filename = filename
    mesh_filename = filename.replace(".geo", ".msh")


    with open(geo_filename, 'w') as f:
        # Write the substrate layer as a rectangle
        f.write("// GMSH geometry file for substrate and resistors\n")
        f.write("// Variables: \n")
        f.write(f"lcs = {s_sense};\n")
        
        # Define substrate points (assuming the substrate is centered at origin)
        x_min_sub, x_max_sub = -substrate_length / 2, substrate_length / 2
        y_min_sub, y_max_sub = -substrate_width / 2, substrate_width / 2

        # Substrate points
        f.write("// SUBSTRATE POINTS:\n")
        f.write(f"Point(1) = {{{x_min_sub}, {y_min_sub}, 0, lcs}};\n")
        f.write(f"Point(2) = {{{x_max_sub}, {y_min_sub}, 0, lcs}};\n")
        f.write(f"Point(3) = {{{x_max_sub}, {y_max_sub}, 0, lcs}};\n")
        f.write(f"Point(4) = {{{x_min_sub}, {y_max_sub}, 0, lcs}};\n")

        # Lines forming the substrate
        f.write("// SUBSTRATE LINES:\n")
        f.write(f"Line(1) = {{1, 2}};\n")
        f.write(f"Line(2) = {{2, 3}};\n")
        f.write(f"Line(3) = {{3, 4}};\n")
        f.write(f"Line(4) = {{4, 1}};\n")

        # Define physical group for boundary lines
        f.write("Physical Line(\"Boundary_1\") = {1};\n")
        f.write("Physical Line(\"Boundary_2\") = {2};\n")
        f.write("Physical Line(\"Boundary_3\") = {3};\n")
        f.write("Physical Line(\"Boundary_4\") = {4};\n")

        # Create the substrate surface
        f.write("// SUBSTRATE SURFACE\n")
        f.write("Curve Loop(1) = {1, 2, 3, 4};\n")
        # NOT adding PlaneSurface(1) as this interferes with the holes

        # Define physical group for substrate
        f.write("Physical Surface(\"Substrate\", 1) = {1};  // Substrate\n")

        # Now add resistors as holes and surfaces inside them
        hole_loops = []
        resistor_surfaces = []
        hole_loop_id = 1 

        for resistor in resistor_data.values():
            x_pos, y_pos = resistor['position']
            length = resistor['length']
            width = resistor['width']

            resistor_surface_id = resistor['resistor_number']

            # ------------------- Test cases for finding optimal choice ------------------ #
            # r_sense = 200
            # r_sense = 100
            # r_sense = 50
            # r_sense = 25
            # r_sense = 15
            # r_sense = 12.5
            # r_sense = 10
            # r_sense = 8.5
            # r_sense = 6
            # r_sense = 3
            r_sense = min(length, width)
            # r_sense = 50

            # Calculate the corners of the resistor (centered at x_pos, y_pos)
            x_min = x_pos - length / 2
            x_max = x_pos + length / 2
            y_min = y_pos - width / 2
            y_max = y_pos + width / 2
            
            # Define points for the resistor hole
            f.write("\n// RESISTOR POINTS:\n")
            f.write(f"lcr = {r_sense};\n")
            f.write(f"Point({hole_loop_id * 4 + 1}) = {{{x_min}, {y_min}, 0, lcr}};\n")
            f.write(f"Point({hole_loop_id * 4 + 2}) = {{{x_max}, {y_min}, 0, lcr}};\n")
            f.write(f"Point({hole_loop_id * 4 + 3}) = {{{x_max}, {y_max}, 0, lcr}};\n")
            f.write(f"Point({hole_loop_id * 4 + 4}) = {{{x_min}, {y_max}, 0, lcr}};\n")

            # Define lines for the resistor hole
            f.write("// RESISTOR LINES:\n")
            f.write(f"Line({hole_loop_id * 4 + 1}) = {{{hole_loop_id * 4 + 1}, {hole_loop_id * 4 + 2}}};\n")
            f.write(f"Line({hole_loop_id * 4 + 2}) = {{{hole_loop_id * 4 + 2}, {hole_loop_id * 4 + 3}}};\n")
            f.write(f"Line({hole_loop_id * 4 + 3}) = {{{hole_loop_id * 4 + 3}, {hole_loop_id * 4 + 4}}};\n")
            f.write(f"Line({hole_loop_id * 4 + 4}) = {{{hole_loop_id * 4 + 4}, {hole_loop_id * 4 + 1}}};\n")

            # Create a curve loop for the resistor hole
            f.write("// RESISTOR CURVE\n")
            f.write(f"Curve Loop({hole_loop_id + 1}) = {{{hole_loop_id * 4 + 1}, {hole_loop_id * 4 + 2}, {hole_loop_id * 4 + 3}, {hole_loop_id * 4 + 4}}};\n")   
            hole_loops.append(hole_loop_id+1)

            # Create a surface for the resistor inside the hole
            f.write("// RESISTOR PLANE SURFACE:\n")
            f.write(f"Plane Surface({hole_loop_id + 1}) = {{{hole_loop_id + 1}}};\n")
            resistor_surfaces.append(resistor_surface_id)

            # Define physical group for the resistor
            f.write(f"Physical Surface(\"Resistor_{resistor_surface_id}\", {resistor_surface_id + 1}) = {{{hole_loop_id + 1}}};  // Resistor {resistor_surface_id}\n")

            hole_loop_id += 1

        # Define the substrate surface with holes
        f.write("\n// SUBSTRATE SURFACE WITH HOLES:\n")
        f.write(f"Plane Surface(1) = {{1, {', '.join(map(str, hole_loops))}}};\n")

        # Refine mesh around resistor edges
        f.write("Field[1] = Distance;\n")
        f.write("Field[1].CurvesList = {" + ", ".join([str(i * 4 + j) for i in range(2, hole_loop_id) for j in range(1, 5)]) + "};\n")
        f.write("Field[1].NumPointsPerCurve = 100;\n")
        f.write("Field[2] = Threshold;\n")
        f.write("Field[2].InField = 1;\n")
        f.write(f"Field[2].LcMin = {r_sense};\n")
        f.write(f"Field[2].LcMax = {s_sense};\n")
        f.write("Field[2].DistMin = 0.1;\n")
        f.write("Field[2].DistMax = 1.0;\n")
        f.write("Background Field = 2;\n")

        # Generate the mesh
        f.write("\nMesh 2;\n")
        f.write(f'Save "{mesh_filename}";\n')

    print(f"\033[93mOutput: .geo file written to \033[0m\033[95m{geo_filename}\033[0m\n\033[93mOutput: .msh file written to\033[0m \033[95m{mesh_filename}\033[0m\n")


        

def get_mesh(msh_filename: str):
    """
    Loads the .msh file created by GMSH and returns the FEniCS mesh objects.

    Args:
        msh_filename (str): The input GMSH .msh file.

    Returns:
        domain (dolfinx.mesh.Mesh): The FEniCS mesh object representing the domain.
        facet_tags (dolfinx.mesh.MeshTags): The facet tags for the boundary conditions.
        volume_tags (dolfinx.mesh.MeshTags): The volume tags for subdomains (e.g., resistors).
    """

    # Convert the Gmsh model to Dolfinx mesh, facet tags, and volume tags
    domain, facet_tags, volume_tags = gmshio.read_from_msh(msh_filename, MPI.COMM_WORLD, gdim=2)

    return domain, facet_tags, volume_tags