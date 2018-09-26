from potential_fitting.molecule import xyz_to_molecules
from potential_fitting.utils import SettingsReader, utils
from potential_fitting.exceptions import ParsingError, LineFormatError
def generate_1b_configurations(settings_path, geo_path, normal_modes_path, config_path):
    """
    Generates a set of 1b configurations for a molecule given its optimized geometry and normal modes.

    Args:
        settings_path - path to the .ini file with relevant settings
        geo_path - path to the optimized geometry .xyz file
        normal_modes_path - path to normal modes file as generated by generate_normal_modes
        config_path - path to the file to write the configurations, existing content will be clobbered.
    """

    print("Parsing normal mode input file.")

    # read the optimized geometry    
    molecule = xyz_to_molecules(geo_path, settings)[0]

    frequencies = []
    reduced_masses = []
    normal_modes = []

    # read frequencies, reduced masses, and normal modes from the input file.
    with open(normal_modes_path, "r") as normal_modes_file:

        # we loop until we run out of normal modes to parse
        while(True):
            first_line = normal_modes_file.readline()

            # if first line is empty string, we have reached EOF
            if first_line == "":
                break

            # if first line is not of valid format, raise error
            if not first_line.startswith("normal mode:") or not len(first_line.split()) == 3:
                raise LineFormatError(normal_modes_path, first_line, "EOF or normal mode: x")

            frequency_line = normal_modes_file.readline()

            # if the frequency line is not of valid format, raise error
            if frequency_line == "":
                raise ParsingError(normal_modes_path, "Unexpected EOF, expected line of format 'frequency = x'")

            if not frequency_line.startswith("frequency = ") or not len(frequency_line.split()) == 3:
                raise LineFormatError(normal_modes_path, frequency_line, "frequency = x")

            # parse the frequency from the frequency line
            try:
                frequency = float(frequency_line.split()[2])

            except ValueError:
                raise ParsingError(normal_modes_path, 
                        "cannot parse {} into a frequency float".format(frequecy_line.split()[2])) from None
            frequencies.append(frequency)

            reduced_mass_line = normal_modes_file.readline()

            # if the reduced mass line is not of valid format, raise error
            if reduced_mass_line == "":
                raise ParsingError(normal_modes_path, "Unexpected EOF, expected line of format 'recued mass = x'")

            if not reduced_mass_line.startswith("reduced mass = ") or not len(reduced_mass_line.split()) == 4:
                raise LineFormatError(normal_modes_path, reduced_mass_line, "reduced mass = x")

            # parse the reduced mass from the frequency line
            try:
                reduced_mass = float(reduced_mass_line.split()[3])

            except ValueError:
                raise ParsingError(normal_modes_path,
                        "cannot parse {} into a reduced mass float".format(reduced_mass_line.split()[3])) from None

            reduced_masses.append(reduced_mass)

            # parse the normal mode
            normal_mode = [[None, None, None] for i in range(molecule.get_num_atoms())]

            for atom_index in range(molecule.get_num_atoms()):
                normal_mode_line = normal_modes_file.readline()

                if normal_mode_line == "":
                    raise ParsingError(normal_modes_path, 
                            "Unexpected EOF, expected line of format 'x y z'")

                if len(normal_mode_line.split()) != 3:
                    raise LineFormatError(normal_modes_path, normal_mode_line,
                            "x y z")

                for ordinate_index, token in enumerate(normal_mode_line.split()):
                    try:
                        offset = float(token)

                    except ValueErrorL:
                        raise ParsingError(normal_modes_path,
                                "cannot parse {} into a offset float".format(token)) from None

                    normal_mode[atom_index][ordinate_index] = offset
                
            normal_modes.append(normal_mode)

            # skip the blank line
            blank_line = normal_modes_file.readline()
            if blank_line != "\n":
                raise ParsingError(normal_modes_path, "expected blank line")

    print("Frequencies:", frequencies)
    print("Reduced Masses:", reduced_masses)
    print("Normal Modes:", normal_modes)

    print("Completed parsing normal modes input file.")

    generate_1b_normal_mode_configs(settings_path, geo_path, frequencies, reduced_masses, normal_modes)


def generate_1b_normal_mode_configs(settings_path, geo_path, frequencies, reduced_masses, normal_modes, config_path, seed = random.randint(-100000, 100000), geometric = True):
    """
    NOTES/TODOS:
        * currently, highest frequency must be last, lowest frequency must be first

    """    

    print("Running normal distribution configuration generator...")

    settings = SettingsReader(settings_path)

    molecule = xyz_to_molecules(geo_path, settings)[0]

    num_configs = settings.getint("config_generator", "num_configs")

    dim = 3 * molecule.get_num_atoms()
    dim_null = dim - len(normal_modes)

    # first generate the T distribution configs
    if geometric:
        min_temp = ? # Kelvin
        max_temp = 2 * frequencies[len(frequencies) - 1] / autocm # Kelvin
        min_A = 1
        max_A = 2
    else:
        min_temp = 0 # Kelvin
        max_temp = frequencies[len(frequencies) - 1] / autocm # Kelvin
        min_A = 0
        max_A = 2
    # now generate the A distribution configs

    print("Normal Distribution Configuration generation complete.")
