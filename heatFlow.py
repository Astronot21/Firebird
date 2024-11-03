from threading import currentThread
import time
import ufl
import dolfinx.io
from petsc4py import PETSc
from mpi4py import MPI
import numpy as np
from dolfinx.fem.petsc import assemble_matrix, assemble_vector
from dolfinx.fem import (Function, FunctionSpace, dirichletbc, locate_dofs_geometrical, Constant, form)
from dolfinx import mesh, fem
from tqdm import tqdm
import generateOutputFiles


def apply_heat_flux_to_resistor_regions(V, domain, cell_tags, resistor_data):
    """
    Function to apply heat flux to resistors by averaging element-wise data to nodes.
    Each resistor is treated as a region identified in the mesh, and heat flux is applied uniformly.

    Args:
        V (FunctionSpace): The function space for temperature.
        domain (Mesh): The finite element mesh.
        cell_tags (MeshTags): MeshTags object containing the tagged cells.
        resistor_data (dict): Dictionary containing information about the resistors.

    Returns:
        Q (Function): A Function containing the nodal heat flux values.
    """
    # Number of nodes (DOFs)
    num_dofs = V.dofmap.index_map.size_local
    # print(f"\033[103mDOFS: {num_dofs}\033[0m")

    # Initialize arrays to accumulate heat flux contributions and counts at nodes
    heat_flux_accum = np.zeros(num_dofs, dtype=PETSc.ScalarType)
    node_count = np.zeros(num_dofs, dtype=int)

    # Loop through resistors to calculate element-wise heat flux
    for resistor in resistor_data.values():
        resistor_id = resistor['resistor_number']
        power = resistor['power_dissipation']
        
        # Get cells that belong to the current resistor
        resistor_cells = cell_tags.find(resistor_id + 1)
        # print(f"\033[103mCells in resistor: {resistor_cells.size}\033[0m")
        # print(resistor_cells.size) DEBUG
        
        # Calculate the heat flux for each resistor
        area = resistor['length'] * resistor['width']
        flux = power / area * 230 # units of uW/um2 = W/m2
        
        # Loop through cells in the resistor
        for cell_index in resistor_cells:
            # Get the nodes (DOFs) of the current cell
            cell = domain.topology.connectivity(domain.topology.dim, 0).links(cell_index)
            
            # Accumulate flux contribution to the nodes of the cell
            for node in cell:
                heat_flux_accum[node] += flux
                node_count[node] += 1

    # Calculate average heat flux at each node
    avg_heat_flux = np.zeros(num_dofs, dtype=PETSc.ScalarType)
    non_zero_nodes = node_count > 0
    avg_heat_flux[non_zero_nodes] = heat_flux_accum[non_zero_nodes] / node_count[non_zero_nodes]

    # Create a Function to store the nodal heat flux values
    Q = fem.Function(V)
    Q.vector.array[:] = avg_heat_flux

    return Q



def add_boundary_conditions(V, domain, facet_tags, T_ambient):
    """
    Adds boundary conditions using the facet tags.
    
    Args:
        V (FunctionSpace): The function space for temperature.
        domain (mesh): The FEniCS domain mesh.
        facet_tags (MeshTags): Boundary facet tags from the mesh.
        T_ambient (float): Ambient temperature value.
        
    Returns:
        list: Boundary conditions for the simulation.
    """
    boundary_conditions = []

    # Iterate over each boundary marker (assuming markers 1 to 4 for each boundary line)
    for boundary_marker in range(1, 5):
        boundary_facets = facet_tags.find(boundary_marker)
        # boundary_dofs = fem.locate_dofs_topological(V, domain.topology.dim - 1, boundary_facets)

        # # Apply Dirichlet boundary condition to the found DOFs
        # boundary_conditions.append(dirichletbc(PETSc.ScalarType(T_ambient), boundary_dofs, V))

    return boundary_conditions


def findHeatSolution(msh_filename, layout_length:float, layout_width:float, rho_param:float, c_p_param:float, k_param:float, resistor_data:dict, iteration_num: int, delta: float, h_cooling: float, T_ambient: float):
    """
    Solves the transient heat flow equation over the layout.
    Includes in-plane heat conduction (x, y) and cooling in the z-direction (Neumann boundary condition).
    
    h_cooling: Heat transfer coefficient (to model cooling in negative z-direction).
    T_ambient: Ambient temperature (to model cooling effect).
    """

   

    start_time = time.time()

    # ------------------ Load the mesh and associated facet tags ----------------- #
    print("""\033[92m
    +-----------------------------+
    | Reading mesh data from file |
    +-----------------------------+
    \033[0m""")

    domain, cell_tags, facet_tags = generateOutputFiles.get_mesh(msh_filename)
    # domain: Core mesh object representing the entire computing domain
    # cell_tags: Stores information about the tags assigned to mesh elements (cells), which are the triangles in 2D: Used for subdomain identification
    # facet_tags: Stores information about the tags assigned to the boundaries (facets), which are edges in 2D: Used for boundary conditions


    # ----------------------- Defining the function space V ---------------------- #
    V = fem.FunctionSpace(domain, ("CG", 1))

    # ----------------- Defining relevant functions ---------------- #
    T_n = Function(V)  # Temperature at previous time step
    v = ufl.TestFunction(V) # test function
    u = ufl.TrialFunction(V)  # temperature at the current timestep (what we are trying to solve)

    delta_t = delta    # Time step size = delta parameter

    # --------- Define the heat source as a Function in the FunctionSpace -------- #
    Q = apply_heat_flux_to_resistor_regions(V, domain, cell_tags, resistor_data)
    with dolfinx.io.VTKFile(MPI.COMM_WORLD,"heat_flux_output_test.vtk", "w") as vtk_file:
        vtk_file.write_mesh(domain)  # Write the mesh first
        vtk_file.write_function(Q)   # Write the function Q containing heat flux values

    print("\n\033[92mPreparing simulation...\033[0m")

    # -------- Define the bilinear form (should contain unknowns u and v) -------- #
    a = (rho_param * c_p_param / delta_t) * u * v * ufl.dx + k_param * ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx


    # --- Define the linear form (including contributions from known T_n and Q) -- #
    L = (rho_param * c_p_param / delta_t) * T_n * v * ufl.dx + Q * v * ufl.dx
    # Add Neumann boundary condition for cooling (heat flux in negative z-direction)
    L += -h_cooling * (T_n - T_ambient) * v * ufl.ds


    # ---------- Boundary condition (Dirichlet for ambient temperature) ---------- #
    # This assumes that the edges of the layout are connected in such a way that it is maintained at a constant temperature, such as in a controlled cold bath environment
    boundary_conditions = add_boundary_conditions(V, domain, facet_tags, T_ambient)


    # ------------------------- Time-stepping parameters ------------------------- #
    num_steps = iteration_num  # Number of time steps
    current_time = 0.0


    # --------------------------- Assemble the matrix A -------------------------- #
    A = fem.petsc.create_matrix(form(a))
    A_mat = fem.petsc.assemble_matrix(A, form(a), bcs=boundary_conditions)
    A_mat.assemble()


    # ------------------------------ Create a solver ----------------------------- #
    solver = PETSc.KSP().create(domain.comm)
    solver.setOperators(A_mat)  # Use the PETSc matrix
    solver.setType(PETSc.KSP.Type.CG)
    solver.getPC().setType(PETSc.PC.Type.LU)
    solver.getPC().setFactorSolverType(PETSc.Mat.SolverType.MUMPS)
    solver.setFromOptions()  # This is necessary to finalize the setup of the solver


    # ---------------------------------------------------------------------------- #
    #              Run the simulation and save data at each time step              #
    # ---------------------------------------------------------------------------- #
    print("""\033[92m
        ===================
        Starting simulation
        ===================
          \033[0m""")


    with tqdm(total=num_steps, desc="Simulating Heat Flow", unit="step") as pbar:
        for step in range(num_steps):
            current_time += delta_t

            # ------------------ Assemble the right-hand side vector (b) ----------------- #
            b = fem.petsc.create_vector(form(L))
            b_vec = fem.petsc.assemble_vector(b, form(L))
            fem.apply_lifting(b_vec, [form(a)], bcs=[boundary_conditions])
            b_vec.ghostUpdate(addv=PETSc.InsertMode.ADD, mode=PETSc.ScatterMode.REVERSE)
            fem.set_bc(b_vec, boundary_conditions)

            # ----------------------------- Solve the system ----------------------------- #
            T_new = Function(V)
            solver.solve(b_vec, T_new.vector)
            T_new.x.scatter_forward()

            # ----------------------- Update for the next time step ---------------------- #
            T_n.x.array[:] = T_new.x.array[:]

            # ----------------------------- Save the solution ---------------------------- #
            if step % 10 == 0:
                vtk_filename = f"heat_solution_step_{step}.vtk"
                generateOutputFiles.write_legacy_vtk(vtk_filename, domain, T_new, step, current_time)


            pbar.update(1) # Update the progress bar

    # ------------------ Find simulation time form time elapsed ------------------ #
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000 # find time elapsed in milliseconds
    
    print("""\033[92m
        ===================
        Simulation complete
        ===================
         \033[0m""")
    print(f"Time elapsed since simulation start: {elapsed_time_ms:.2f} ms")
    print(f"Output file saved.\n")


