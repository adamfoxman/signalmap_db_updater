import os
from dotenv import load_dotenv
from reader.csvreader import CSVReader
from reader.externalreader import ExternalReader
from dbupdater import DBUpdater
from dbupdater import get_antenna_file, get_location_file, run_simulation
# from tests.dbupdater.test_antennafilegenerator import test_parse_antenna_direction


def main():
    # only load .env if it exists and outside of docker container!
    load_dotenv()
    test_parse_antenna_direction()

    reader = ExternalReader(endpoint="http://localhost/api/v1")
    database_updater = DBUpdater("http://localhost/api/v1")
    reader.download_data()
    database_updater.set_transmitter_list(reader.get_transmitter_list())
    database_updater.update_database()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
