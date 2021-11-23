import os
from dotenv import load_dotenv
from reader.csvreader import CSVReader
from reader.externalreader import ExternalReader
from dbupdater.dbupdater import DBUpdater
from dbupdater import get_antenna_file


def main():
    # only load .env if it exists and outside of docker container!
    load_dotenv()

    # reader = ExternalReader(endpoint="http://localhost/api/v1")
    # database_updater = DBUpdater("http://localhost/api/v1")
    # reader.download_data()

    get_antenna_file("./", 6400001, "f", "PL", "", "38.2   38 38.3 38.3 37.5 36.9 37.7   39 39.9   40 39.6 38.9 37.8 "
                                                   "36.9 36.6 36.6   36 34.8 34.4 35.5 36.4 36.5   36 35.3   35 35.4 "
                                                   "36.2 36.4   36   36 37.3 38.9 39.7 39.9 39.6 38.9", "")

    # database_updater.set_transmitter_list(reader.get_transmitter_list())
    # database_updater.update_database()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
