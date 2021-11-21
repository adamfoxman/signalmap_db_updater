import os
from dotenv import load_dotenv
from reader.csvreader import CSVReader
from reader.externalreader import ExternalReader
from dbupdater.dbupdater import DBUpdater


def main():
    # only load .env if it exists and outside of docker container!
    load_dotenv()

    reader = ExternalReader(endpoint="http://localhost/api/v1")
    database_updater = DBUpdater("http://localhost/api/v1")
    reader.download_data()

    # database_updater.set_transmitter_list(reader.get_transmitter_list())
    # database_updater.update_database()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
