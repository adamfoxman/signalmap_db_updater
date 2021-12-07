import os
from time import sleep
from google.cloud import storage

import requests as req
from json import dumps
from .antennafilegenerator import get_antenna_file
from .locationfilegenerator import get_location_file
from models import Transmitter
from .splatrunner import run_simulation


class DBUpdater:
    """
    Class for updating the database with new data.
    """
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.transmitter_list = []
        self.country_list = {}
        try:
            req.get(endpoint)
            self.endpoint = endpoint
        except req.ConnectionError:
            print(f"URL %s is not available on the internet.", endpoint)

    def set_transmitter_list(self, tlist: list[Transmitter]):
        """
        Set the list of transmitters to be updated.
        :param tlist: List of Transmitter objects.
        :return: None.
        """
        if isinstance(tlist, list):
            self.transmitter_list = tlist

    def update_database(self):
        """
        Update the database with new data.

        :return: None.
        """
        for unit in self.transmitter_list:
            sleep(0.2)
            response = req.get(f"{self.endpoint}/transmitters/get/external/?band={str(unit.band)}&external_id={str(unit.external_id)}")
            print("ZAPYTANIE:" + str(response) + " " + str(response.text))
            if response.text == "null":
                location_filename = f"{unit.country_id}_{unit.band}_{unit.external_id}"
                get_antenna_file("./", location_filename, unit.antenna_direction, unit.pattern_h, unit.pattern_v)
                get_location_file("./", location_filename, unit.station, unit.latitude, unit.longitude, unit.antenna_height)
                try:
                    run_simulation("./", location_filename, unit.band, float(unit.erp))
                    coverage_url = upload_to_gcloud_storage(f"signalmap-{unit.band}", f"{location_filename}.png")
                    kml_url = upload_to_gcloud_storage(f"signalmap-{unit.band}", f"{location_filename}.kml")
                    if coverage_url is not None and kml_url is not None:
                        unit.kml_file = kml_url
                        unit.coverage_file = coverage_url
                except Exception as e:
                    print(e)
                    continue
                json_transmitter = convert_transmitter_obj_to_json(unit)
                print("to co wysylamy:" + str(json_transmitter))
                res = req.post("http://localhost/api/v1/transmitters/create/", json_transmitter)
                print("ODPOWIEDŻ: " + str(res.text))
                delete_files(location_filename, unit.station)
            else:
                print("Już istnieje.")


# uploads the coverage file to google cloud storage and returns the url
def upload_to_gcloud_storage(bucket_name: str, file_name: str):
    """
    Uploads the coverage file to google cloud storage and returns the url.

    :param bucket_name: Name of the bucket.
    :param file_name: File name to be uploaded.
    :return: URL of the uploaded file.
    """
    try:
        storage_client = storage.Client.from_service_account_json(os.getenv("GCLOUD_JSON"))
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        return f"https://storage.googleapis.com/{bucket_name}/{file_name}"
    except Exception as e:
        print(e)
        return None


def convert_transmitter_obj_to_json(obj):
    """
    Converts Transmitter object to json.

    :param obj: Transmitter object.
    :return: Json object.
    """
    return dumps(obj.__dict__)


def delete_files(location_filename: str, station_name: str):
    delete_file(f"./{location_filename}.png")
    delete_file(f"./{location_filename}.ppm")
    delete_file(f"./{location_filename}-ck.ppm")
    delete_file(f"./{location_filename}.kml")
    delete_file(f"./{location_filename}.az")
    delete_file(f"./{location_filename}.qth")
    delete_file(f"./{location_filename}.scf")
    delete_file(f"./{station_name.replace(' ', '_')}-site_report.txt")


def delete_file(file_name: str):
    """
    Deletes the file.

    :param file_name: File name.
    :return: None.
    """
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print("File not found.")