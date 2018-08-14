import sys, os
import sqlite3
import calculator
from database import Database

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../")
from exceptions import LibraryCallError
import settings_reader

def fill_database(settings_file, database_name):
    """
    Calculates all the pending energies in a database

    Args:
        settings_file   - the file with all relevant settings information
        database_name   - the database file

    Returns:
        None
    """
    # add .db to the database name if it doesn't already end in .db
    if database_name[-3:] != ".db":
        print("Database name \"{}\" does not end in database suffix \".db\". Automatically adding \".db\" to end of database name.".format(database_name))
        database_name += ".db"

    # open the database
    with Database(database_name) as database:

        print("Filling database {}".format(database_name))

        # parse settings file
        settings = settings_reader.SettingsReader(settings_file)
        
        for calculation in database.missing_energies():

            try:
                # calculate the missing energy
                energy = calculator.calculate_energy(calculation.molecule, calculation.fragments, calculation.method + "/" + calculation.basis, calculation.cp, settings)
                # update the energy in the database
                database.set_energy(calculation.job_id, energy, "some/log/path")
            except LibraryCallError:
                database.set_failed(calculation.job_id, "failed", "some/log/path")
            
            # save changes to the database
            database.save()

        print("Filling of database {} successful".format(database_name))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect number of arguments");
        print("Usage: python database_filler.py <settings_file> <database_name>")
        exit(1)
    fill_database(sys.argv[1], sys.argv[2])
