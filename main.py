from reader.csvreader import CSVReader
from dbupdater.dbupdater import DBUpdater


def main():

    reader = CSVReader("example_data.csv")
    database_updater = DBUpdater("http://localhost/api/v1")
    database_updater.download_countries()
    # database_updater.set_transmitter_list(reader.get_transmitter_list())
    # database_updater.update_database()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
