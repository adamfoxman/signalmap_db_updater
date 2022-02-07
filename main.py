import os
import schedule
import time
import atexit
import logging
from dotenv import load_dotenv
from reader.externalreader import ExternalReader
from dbupdater import DBUpdater
from dbupdater import get_antenna_file, get_location_file, run_simulation
# from tests.dbupdater.test_antennafilegenerator import test_parse_antenna_direction
from tests.dbupdater.test_dbupdater import dbupdater_test
from dbupdater.apicaller import InternalAPICaller

logging.basicConfig(filename='logs/main.log',
                    level=logging.DEBUG,
                    format='%(asctime)s, %(levelname)s at [%(filename)s:%(lineno)d]: %(message)s')

load_dotenv()

def clean_up():
    logging.info("Cleaning up orphaned files")
    try:
        for file in os.listdir():
            if file.endswith(".lrp") and file != "splat.lrp":
                os.remove(file)
            if file.endswith(".scf") and file != "d.scf" and file != "f.scf" and file != "t.scf":
                os.remove(file)
            if file.endswith(".png") or file.endswith(".ppm") or file.endswith(".az") or file.endswith(
                    ".el") or file.endswith(".qth") or file.endswith(".kml") or file.endswith(".txt"):
                os.remove(file)
        logging.info("Cleanup done!")
    except Exception as e:
        logging.error(e)
    logging.info("Exiting...")


def run(is_running: list[bool]):
    if not is_running[0]:
        is_running[0] = True
        api_caller = InternalAPICaller()
        logging.info("Starting run")
        reader = ExternalReader(external_endpoint="http://localhost/api/v1", internal_api_caller=api_caller)
        database_updater = DBUpdater("http://localhost/api/v1")
        reader.download_data()
        database_updater.set_transmitter_list(reader.get_transmitter_list())
        database_updater.update_database()
        clean_up()
        is_running[0] = False
    else:
        logging.warning("Already running!")


def main():
    # only load .env if it exists and outside of docker container!
    logging.info("Loading .env file")
    if not os.path.isfile(".env"):
        logging.critical(".env file not found!")
        exit(1)
    is_running = [False]

    if os.getenv('RUN_EVERY_DAY') == 'True':
        logging.info("Running in cyclical mode")
        updater = schedule.every().day.at("01:00").do(run, is_running)
        while True:
            schedule.run_pending()
            # sleep for a minute
            time.sleep(60)
    else:
        logging.warning("Running in instant mode - will exit after runtime!")
        try:
            run(is_running)
        except Exception as e:
            print(e)
            logging.error(e)
            is_running[0] = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    atexit.register(clean_up)
    logging.info("Starting main.py")
    print("Starting!")
    main()
