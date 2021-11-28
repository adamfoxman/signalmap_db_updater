import os
from dotenv import load_dotenv
from reader.csvreader import CSVReader
from reader.externalreader import ExternalReader
from dbupdater import DBUpdater
from dbupdater import get_antenna_file, get_location_file, run_simulation


def main():
    # only load .env if it exists and outside of docker container!
    load_dotenv()

    # reader = ExternalReader(endpoint="http://localhost/api/v1")
    # database_updater = DBUpdater("http://localhost/api/v1")
    # reader.download_data()
    # database_updater.set_transmitter_list(reader.get_transmitter_list())
    # database_updater.update_database()

    get_antenna_file("./", 6401179, "f", "PL", "", "",
                     "23   23   23   23   23   23   23   20   20   23   23   23   23   23   23   23   17   17   20   23   23   23   23   23   23   23   10   23   17   17   23   23   23   23   23   23")
    get_location_file("./", 6401179, "f", "PL", "Radio Plus Olsztyn", 54.075269, 21.353856,
                      55)
    run_simulation("./", 6401179, "f", "PL", float("0.2"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
