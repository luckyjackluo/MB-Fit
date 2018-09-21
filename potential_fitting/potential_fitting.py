# external package imports
import os, subprocess, contextlib, random

# local module imports
from .utils import SettingsReader, files, system
from . import configurations, database, polynomials, fitting
from .database import Database

def optimize_geometry(settings_path, unopt_geo_path, opt_geo_path):
    """
    Optimizes the geometry of the given molecule.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        unopt_geo_path      - Local path to the file to read the unoptimized geoemtry from.
        opt_geo_path        - Local path to the file to write the optimized geometry to.

    Returns:
        None.
    """

    configurations.optimize_geometry(settings_path, unopt_geo, opt_geo)

def generate_normal_modes(settings_path, opt_geo_path, normal_modes_path):
    """
    Generates the normal modes for the given molecule.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        opt_geo_path        - Local path to the file to read the optimized geometry from.
        normal_modes_path   - Local path to the file to write the normal modes to.

    Returns:
        Null dimension of normal modes.
    """
    
    dim_null = configurations.generate_normal_modes(settings_path, opt_geo_path, normal_modes_path)

    return dim_null

def generate_1b_configurations(settings_path, opt_geo_path, normal_modes_path, dim_null, configurations_path):
    """
    Generates 1b configurations for a given monomer from a set of normal modes.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        opt_geo_path        - Local path to the file to read optimized geometry from.
        normal_modes_path   - Local path to the file to read normal modes from.
        dim_null            - The null dimension of this molecule, see generate_normal_modes().
        config_path         - Local path to the file to write configurations to.

    Returns:
        None.
    """

    configurations.generate_1b_configurations(settings_path, opt_gep_path, normal_modes_path, dim_null,
            configurations_path)

def generate_2b_configurations(settings_path, geo1_path, geo2_path, number_of_configs, configurations_path,
        min_distance = 1, max_distance = 5, min_inter_distance = 1.2, use_grid = False, step_size = 0.5,
        seed = random.randint(-1000000, 1000000)):
    """
    Generates 2b configurations for a given dimer.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        geo1_path           - Local path to read the first optimized geometry from.
        geo2_path           - Local path to read the second optimized geometry from.
        number_of_configs   - The target number of configurations to generate. If max_distance is set too low or 
                min_inter_distance is set too high, then less configurations may be generated.
        config_path         - Local path to the file in to write the configurations to.
        min_distance        - The minimum distance between the centers of mass of the two molecules in any
                configuration.
        max_distance        - The maximum distance between the centers of mass of the two molecules in any
                configuration.
        min_inter_distance  - The minimum intermolecular atomic distance in any configuration.
        use_grid            - If False, configurations are space roughly evenly between min_distance and max_distance.
                If True, then configurations are placed at intervals along this distance based on step_size.
        step_size           - If use_grid is True, then this dictates the distance of the spacing interval used to
                place the centers of masses of the molecules. Otherwise, this parameter has no effect.
        seed                - The same seed will generate the same configurations.

    Returns:
        None.
    """

    configurations.generate_2b_configurations(geo1_path, geo2_path, number_of_configs, configurations_path,
            min_distance, max_distance, min_inter_distance, use_grid, step_size, seed)

def init_database(settings_path, database_path, configurations_path):
    """
    Creates a database from the given configuration .xyz files. Can be called on a new database
    to create a new database, or an existing database to add more energies to be calculated

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        database_path       - Local path to the database file to add the configurations to. ".db" will automatically
                be added to the end if it does not already end in ".db".
        configurations_path - Local path to a single .xyz file or a directory containing ".xyz" files. If this argument
                is a directory, any non .xyz files will be ignored.

    Returns:
        None.
    """

    database.initialize_database(settings_path, database_path, configurations_files)

def fill_database(settings_path, database_path):
    """
    Goes through all the uncalculated energies in a database and calculates them. Will take a while. May be interrupted
    and restarted.
    
    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        database_path       - Local path to the database file containing uncaculated energies. ".db" will
                automatically be added to the end if it does not already end in ".db".

    Returns:
        None.
    """

    database.fill_database(settings_path, database_path)

def generate_1b_training_set(settings_path, database_path, training_set_path, molecule_name, method = "%", basis = "%",
            cp = "%", tag = "%"):
    """
    Generates a 1b training set from the energies inside a database.

    Specific method, bnasis, and cp may be specified to only use energies calculated
    with a specific model.

    '%' can be used to stand in as a wild card, meaning any method/basis/cp will be used in the training set.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        database_path       - Local path to the database file containing energies to put in the training set. ".db"
                will automatically be added to the end if it does not already end in ".db".
        training_set_path   - Local path to the file to write the training set to.
        molecule_name       - The name of the moelcule to generate a training set for.
        method              - Only use energies calcualted by this method.
        basis               - Only use energies calculated in this basis.
        cp                  - Only use energies calculated with this cp. Note that counterpoise correct has no
                effect on 1b energies.
        tag                 - Only use energies marked with this tag.

    Returns:
        None.
    """

    database.generate_1b_training_set(settings_path, database_path, training_set_path, molecule_name, method, basis,
            cp, tag)

def generate_2b_training_set(settings_path, database_path, training_set_path, monomer1_name, monomer2_name,
        method = "%", basis = "%", cp = "%", tag = "%"):
    """
    Generates a 2b training set from the energies inside a database.

    Specific method, basis, and cp may be specified to only use energies calculated
    with a specific model.

    '%' can be used to stand in as a wild card, meaning any method/basis/cp will be used in the training set.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        database_path       - Local path to the database file containing energies to put in the training set. ".db"
                will automatically be added to the end if it does not already end in ".db".
        training_set_path   - Local path to the file to write the training set to.
        monomer1_name       - The Name of first monomer in the dimer.
        monomer2_name       - The Name of the second monomer in the dimer.
        method              - Only use energies calcualted by this method.
        basis               - Only use energies calculated in this basis.
        cp                  - Only use energies calculated with this cp.
        tag                 - Only use energies marked with this tag.

    Returns:
        None.
    """

    database.generate_2b_training_set(settings_path, database_path, training_set_path, monomer1_name, monomer2_name,
            method, basis, cp, tag)

def generate_poly_input(settings_path, poly_in_path):
    """
    Generates an input file for polynomial generation.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        poly_in_path        - Local path to the file to write the polynomial input to. Name of file should be in
                the format A1B2.in, it is ok to have extra directories prior to file name (thisplace/thatplace/A3.in).

    Returns:
        None.
    """

    polynomials.generate_input_poly(settings_path, poly_in_path)

def generate_poly_input_from_database(settings_path, database_path, molecule_name, input_dir_path):
    """
    Generates an input file for polynomial generation.
    Looks in a database to find the symmetry and creates a file in the given directory.

    If the symmetry is A1B2, then the file A1B2.in containing polynomial generation input will be created inside
    the poly_directory_path directory.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        database_path       - Local path to the database file containing the molecular symmetry. ".db" will
                automatically be added to the end if it does not already end in ".db".
        molecule_name       - The name of the molecule to generate a polynomial generation input file for. At least one
                instance of this molecule must be in the database.
        input_dir_path      - Local path to the directory to write the polynomial generation input file in.

    Returns:
        None.
    """

    with Database(database_path) as database:
        symmetry = database.get_symmetry(molecule_name)

        generate_poly_input(settings_path, poly_dir_path + "/" + symmetry + ".in")

def generate_polynomials(settings_path, poly_in_path, order, poly_dir_path):
    """
    Generates polynomial input for maple and some ".cpp" and ".h" polynomial files.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        poly_in_path        - Local path to the file to read the polynomial input from. Name of file should be in
                the format "A1B2.in". It is ok to have extra directories prior to file name. For example:
                "thisplace/thatplace/A3.in".
        order               - The order of the polynomial to generate.
        poly_dir_path       - Local path to the directory to write the polynomial files in.

    Returns:
        None.
    """

    this_file_path = os.path.dirname(os.path.abspath(__file__))

    original_dir = os.getcwd()

    files.init_directory(poly_dir_path)

    os.chdir(poly_dir_path)

    system.call("poly-gen_mb-nrg.pl", str(order), "{}/{}".format(original_dir, poly_in_path), ">", "poly.log")

    os.chdir(original_dir)

def execute_maple(settings_path, poly_dir_path):
    """
    Runs maple on the polynomial files in the specified directory to turn them into actual cpp files.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        poly_directory      - Local path to the directory to read the ".maple" files from and write the ".cpp" files
                to.

    Returns:
        None.
    """

    this_file_path = os.path.dirname(os.path.abspath(__file__))

    original_dir = os.getcwd()

    os.chdir(poly_dir_path)

    # clear any old files, because for some reason maple appends to existing files instead of clobbering
    with contextlib.suppress(FileNotFoundError):
        os.remove("poly-grd.c")
        os.remove("poly-nogrd.c")
        os.remove("poly-grd.cpp")
        os.remove("poly-nogrd.cpp")
    
    system.call("maple", "poly-grd.maple")
    system.call("maple", "poly-nogrd.maple")

    system.call("clean-maple-c.pl", "<", "poly-grd.c", ">", "poly-grd.cpp")
    system.call("clean-maple-c.pl", "<", "poly-nogrd.c", ">", "poly-nogrd.cpp")

    os.chdir(original_dir)

def generate_fit_config(settings_path, molecule_in, config_path, *opt_geometry_paths, distance_between = 20):
    """
    Generates the config file needed to perform a fit from the optimized geometries of up to 3 monomers.

    Qchem is required for this step to work.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        molecule_in         - A String of fromat "A1B2". Same as poly_in_path but without ".in".
        config_path         - Local path to file to write the config file to.
        opt_geometry_paths  - Local paths to the optimized geometries to include in this fit config, should be 1 to 3
                (inclusive) of them.
        distance_between    - The Distance between each geometry in the qchem calculation. If the qchem calculation
                does not converge, try different values of this.

    Returns:
        None.
    """

    fitting.make_config(settings_path, molecule_in, config_path, *opt_geometry_paths,
            distance_between = distance_between)
    
def generate_1b_fit_code(settings_path, config_path, poly_in_path, poly_dir_path, order, fit_dir_path):
    """
    Generates the fit code based on the polynomials and config file for a monomer.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        config_path         - Local path to the monomer config file to read config info from.
        poly_in_path        - Local path to the file to read the polynomial input from. Name of file should be in
                the format A1B2.in, it is ok to have extra directories prior to file name (thisplace/thatplace/A3.in).
        poly_dir_path       - Local path to the directory where the polynomial ".h" and ".cpp" files are files are.
        order               - The order of the polynomial to in poly_dir_path.
        fit_dir_path        - Local path to the directory to write the fit code in.

    Returns:
        None.
    """

    fitting.prepare_1b_fitting_code(config_path, poly_in_path, poly_dir_path, order, fit_dir_path)

def generate_2b_ttm_fit_code(settings_path, config_path, molecule_in, fit_dir_path):
    """
    Generates the fit TTM fit code for a dimer.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        config_path         - Local path to the dimer config file to read config info from.
        molecule_in         - A String of fromat "A1B2". Same as poly_in_path but without ".in".
        fit_dir_path        - Local path to the directory to write the ttm fit code in.

    Returns:
        None.
    """

    this_file_path = os.path.dirname(os.path.abspath(__file__))

    original_dir = os.getcwd()

    files.init_directory(fit_dir_path)

    os.chdir(fit_dir_path) 
    
    system.call("cp", this_file_path + "/../codes/2b-codes/template/*", ".")

    ttm_script_path = "{}/../codes/2b-codes/get_2b_TTM_codes.py".format(this_file_path))

    system.call("python", ttm_script_path, "{}/{}".format(original_dir, settings_path), "{}/{}".format(original_dir, config_path), molecule_in)

    os.chdir(original_dir)   


def compile_fit_code(settings_path, fit_dir_path):
    """
    Compiles the fit code in the given directory.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        fit_dir_path        - Local path to the directory to read uncompiled fit code from and write compiled fit code
                to.

    Returns:
        None.
    """

    original_dir = os.getcwd()

    files.init_directory(fit_dir_path)

    os.chdir(fit_dir_path)

    system.call("make", "clean")
    system.call("make")

    os.chdir(original_dir)

def fit_1b_training_set(settings_path, fit_code_path, training_set_path, fit_dir_path, fitted_nc_path):
    """
    Fits a given 1b training set using a given 1b fit code.

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        fit_code_path       - Local path to the fit code with which to fit the training set. Generated in fit_dir_path
                by compile_fit_code.
        training_set_path   - Local path to the file to read the training set from.
        fit_dir_path        - Local path to the directory to write the ".cdl" and ".dat" files created by this fit.
        fitted_code         - Local path to the file to write the final fitted ".nc" to.

    Returns:
        None
    """

    files.init_directory(fit_dir_path)
    files.init_file(fitted_nc_path)

    system.call(fit_code_path, training_set_path)

    system.call("ncgen", "-o", "fit-1b.nc", "fit-1b.cdl")

    os.rename("fit-1b.cdl", os.path.join(fit_dir_path, "fit-1b.cdl"))
    os.rename("fit-1b-initial.cdl", os.path.join(fit_dir_path, "fit-1b-initial.cdl"))
    os.rename("correlation.dat", os.path.join(fit_dir_path, "correlation.dat"))
    os.rename("fit-1b.nc", fitted_nc_path)

def fit_2b_ttm_training_set(settings_path, fit_code_path, training_set_path, fit_dir_path):
    """
    Fits a given 2b training set using a given 2b ttm fit code

    Args:
        settings_path       - Local path to the file containing all relevent settings information.
        fit_code_path       - Local path to the fit code with which to fit the training set. Generated in fit_dir_path
                by compile_fit_code.
        training_set_path   - Local path to the file to read the training set from.
        fit_dir_path - the directory where the fit log and other files created by the fit go

    Returns:
        None
    """

    files.init_directory(fit_dir_path)

    attempts = 1;
    system.call(fit_code_path, training_set_path, ">", fit_dir_path + "/best_fit.log")
    while(attempts < 10):
        system.call(fit_code_path, training_set_path, ">", fit_dir_path + "/fit.log")
        
        with open(fit_dir_path + "/fit.log", "r") as fit_log, open(fit_dir_path + "/best_fit.log", "r") as best_fit_log:
            log_lines = fit_log.readlines()
            best_log_lines = best_fit_log.readlines()

        rmsd = float(log_lines[-4].split()[2])
        best_rmsd = float(best_log_lines[-4].split()[2])

        if rmsd < best_rmsd:
            os.rename(os.path.join(fit_dir_path, "fit.log"), os.path.join(fit_dir_path, "best_fit.log"))
            

        attempts += 1

    os.remove(os.path.join(fit_dir_path, "fit.log"))
    os.rename("individual_terms.dat", os.path.join(fit_dir_path, "individual_terms.dat"))
    os.rename("ttm-params.txt", os.path.join(fit_dir_path, "ttm-params.txt"))
    os.rename("correlation.dat", os.path.join(fit_dir_path, "correlation.dat"))
