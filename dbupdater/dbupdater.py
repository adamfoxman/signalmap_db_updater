import os
import time
import logging
from functools import partial
from time import sleep
from multiprocessing import Pool, cpu_count

from pykml import parser
from google.cloud import storage
import pycountry

import requests as req
from json import dumps

from models.country import Country, CountryCompare
from .apicaller import InternalAPICaller
from .antennafilegenerator import get_antenna_file
from .locationfilegenerator import get_location_file
from models import Transmitter
from .splatrunner import run_simulation


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
        logging.error(e)
        print(e)
        return None


def convert_transmitter_obj_to_json(obj):
    """
    Converts Transmitter object to json.

    :param obj: Transmitter object.
    :return: Json object.
    """
    return dumps(obj.__dict__)


def convert_country_obj_to_json(c):
    """
    Converts Country object to json.

    :param c: Country object.
    :return: Json object.
    """
    return dumps(c.__dict__)


# Get boundaries from provided kml file from LatLonBox in GroundOverlay and return it as four floats.
def get_boundaries(kml_file_path: str):
    with open(kml_file_path, 'r') as f:
        try:
            root = parser.parse(f).getroot()
            north = float(root.Folder.GroundOverlay.LatLonBox.north)
            south = float(root.Folder.GroundOverlay.LatLonBox.south)
            east = float(root.Folder.GroundOverlay.LatLonBox.east)
            west = float(root.Folder.GroundOverlay.LatLonBox.west)
            return north, south, east, west
        except Exception as e:
            logging.error(e)
            print(e)
            return 0, 0, 0, 0


def delete_files(location_filename: str, station_name: str):
    if os.path.isfile(f"./{location_filename}.ppm"):
        delete_file(f"./{location_filename}.ppm")
    if os.path.isfile(f"./{location_filename}.png"):
        delete_file(f"./{location_filename}.png")
    if os.path.isfile(f"./{location_filename}-ck.ppm"):
        delete_file(f"./{location_filename}-ck.ppm")
    if os.path.isfile(f"./{location_filename}-ck.png"):
        delete_file(f"./{location_filename}-ck.png")
    if os.path.isfile(f"./{location_filename}.kml"):
        delete_file(f"./{location_filename}.kml")
    if os.path.isfile(f"./{location_filename}.az"):
        delete_file(f"./{location_filename}.az")
    if os.path.isfile(f"./{location_filename}.qth"):
        delete_file(f"./{location_filename}.qth")
    if os.path.isfile(f"./{location_filename}.scf"):
        delete_file(f"./{location_filename}.scf")
    if os.path.isfile(f"./{location_filename}.lrp"):
        delete_file(f"./{location_filename}.lrp")
    if os.path.isfile(f"./{station_name.replace(' ', '_')}-site_report.txt"):
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
        logging.error(f"File {file_name} not found.")
        print("File not found.")


def generate_transmitter(unit: Transmitter):
    logging.info(f"Generating map for {unit}")
    location_filename = f"{unit.country_id}_{unit.band}_{unit.external_id}"
    get_antenna_file("./", location_filename, unit.antenna_direction, unit.pattern_h, unit.pattern_v)
    get_location_file("./", location_filename, unit.station, unit.latitude, unit.longitude,
                      unit.antenna_height if unit.antenna_height != 0 else 100)
    try:
        while not os.path.exists(f"./{location_filename}.az"):
            time.sleep(1)
        while not os.path.exists(f"./{location_filename}.qth"):
            time.sleep(1)
        if os.path.isfile(f"./{location_filename}.az") and os.path.isfile(f"./{location_filename}.qth"):
            run_simulation("./", location_filename, unit.band, float(unit.erp), float(unit.frequency))
        else:
            raise Exception("Azimuth or QTH file not found.")
        north, south, east, west = get_boundaries(f"./{location_filename}.kml")
        coverage_url = upload_to_gcloud_storage(f"signalmap-{unit.band}", f"{location_filename}.png")
        if coverage_url is not None:
            unit.coverage_file = coverage_url
        else:
            raise Exception("Coverage file is not uploaded.")
        if north != 0 and south != 0 and east != 0 and west != 0:
            unit.north_bound = north
            unit.south_bound = south
            unit.east_bound = east
            unit.west_bound = west
        else:
            raise Exception("Bounds are not set.")
    except Exception as e:
        logging.error(e)
        raise e
    delete_files(location_filename, unit.station)


def create_transmitter(api_caller: InternalAPICaller, unit: Transmitter):
    generate_transmitter(unit)
    json_transmitter = convert_transmitter_obj_to_json(unit)
    # res = req.post("http://localhost/api/v1/transmitters/create/", json_transmitter)
    res = api_caller.create_transmitter(json_transmitter)
    if res.status_code == 200:
        logging.info(f"Transmitter {unit.external_id} created.")
        print("Transmitter created successfully")
    else:
        logging.error(f"Transmitter {unit.external_id} not created.")
        print("Transmitter not created")


def update_transmitter(api_caller: InternalAPICaller, unit: Transmitter):
    generate_transmitter(unit)
    json_transmitter = convert_transmitter_obj_to_json(unit)
    # res = req.post(f"http://localhost/api/v1/transmitters/update/?band={unit.band}&external_id={unit.external_id}",
                   # json_transmitter)
    res = api_caller.update_transmitter(unit.band, unit.external_id, json_transmitter)
    if res.status_code == 200:
        logging.info(f"Transmitter {unit.external_id} updated.")
        print("Transmitter updated successfully")
    else:
        logging.error(f"Transmitter {unit.external_id} not updated.")
        print("Transmitter not updated")


# multiprocessing friendly version of update_transmitters
def update_transmitters_multi(api_caller: InternalAPICaller, unit: Transmitter):
    # response = req.get(
    #     f"{endpoint}/transmitters/get/external/?band={str(unit.band)}&external_id={str(unit.external_id)}")
    response = api_caller.get_transmitter_by_external_id(unit.band, unit.external_id)
    print("ZAPYTANIE:" + str(response) + " " + str(response.text))
    if response.text == "null":
        try:
            create_transmitter(api_caller, unit)
        except Exception as e:
            logging.error(e)
            print(e)
    else:
        if os.getenv('REGENERATE_MAPS') == 'True':
            try:
                update_transmitter(api_caller, unit)
            except Exception as e:
                logging.error(e)
                print(e)
        else:
            # compare unit from external source with unit from internal database
            transmitter_from_internal_source = Transmitter(
                external_id=int(response.json()["external_id"]),
                band=response.json()["band"],
                frequency=float(response.json()["frequency"]),
                mode=response.json()["mode"],
                erp=float(response.json()["erp"]),
                antenna_height=int(response.json()["antenna_height"]),
                antenna_pattern=response.json()["antenna_pattern"],
                antenna_direction=response.json()["antenna_direction"],
                pattern_h=response.json()["pattern_h"],
                pattern_v=response.json()["pattern_v"],
                polarisation=response.json()["polarisation"],
                location=response.json()["location"],
                region=response.json()["region"],
                country_id=response.json()["country_id"],
                latitude=float(response.json()["latitude"]),
                longitude=float(response.json()["longitude"]),
                precision=int(response.json()["precision"]),
                height=int(response.json()["height"]),
                station=response.json()["station"]
            )
            if unit != transmitter_from_internal_source:
                print(unit.__dict__.items() ^ transmitter_from_internal_source.__dict__.items())
                try:
                    update_transmitter(api_caller, unit)
                except Exception as e:
                    print(e)
                    logging.error(e)
            else:
                print("Transmitter is up to date.")


class DBUpdater:
    """
    Class for updating the database with new data.
    """

    def __init__(self, endpoint: str):
        self.transmitter_list = []
        self.country_list = {}
        self.pool = Pool()
        try:
            req.get(endpoint)
            self.endpoint = endpoint
            self.api_caller = InternalAPICaller()
            self.api_caller.set_url(os.getenv('INTERNAL_API_ADDRESS'))
        except Exception as e:
            logging.error("Connection error")
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
        self.update_countries()
        if os.getenv('MULTIPROCESSING') == 'True':
            func = partial(update_transmitters_multi, self.api_caller)
            self.pool.map(func, self.transmitter_list)
            self.pool.close()
            self.pool.join()
        else:
            self.update_transmitters()
        # self.update_transmitters()

    def update_countries(self):
        """
        Update the list of countries.

        :return: None.
        """
        temp_internal_country_list: dict[str, CountryCompare] = {}
        # signalmap_country_response = req.get(f"{self.endpoint}/countries/").json()
        signalmap_country_response = self.api_caller.get_countries().json()
        for country in signalmap_country_response:
            c: CountryCompare = CountryCompare(
                country_code=country["country_code"],
                country_name=country["country_name"])
            temp_internal_country_list[c.country_code] = c

        temp_external_country_list: dict[str, CountryCompare] = {}
        for country in pycountry.countries:
            c: CountryCompare = CountryCompare(
                country_code=country.alpha_2,
                country_name=country.name)
            temp_external_country_list[c.country_code] = c

        # country_list_intersection = set(temp_internal_country_list).intersection(temp_external_country_list)
        if len(temp_external_country_list) != len(temp_internal_country_list):
            for country in temp_internal_country_list.values():
                if country not in temp_external_country_list.values():
                    # req.delete(f"{self.endpoint}/countries/delete/{country.country_code}")
                    self.api_caller.delete_country(country.country_code)
            for country in temp_external_country_list.values():
                if country not in temp_internal_country_list.values():
                    c: Country = Country(country_code=country.country_code,
                                         country_name=country.country_name,
                                         is_enabled="True" == os.getenv("UPDATE_COUNTRIES"))
                    # req.post(f"{self.endpoint}/countries/create/", data=convert_country_obj_to_json(c))
                    c_json = convert_country_obj_to_json(c)
                    self.api_caller.create_country(c_json)
                # if country not in temp_internal_country_list:
                #     c: Country = Country(country_code=country_code, country_name=country.country_name)
                #     data = convert_country_obj_to_json(c)
                #     req.post(f"{self.endpoint}/countries/create/", data)
        else:
            print("Countries are up to date.")

    def update_transmitters(self):
        for unit in self.transmitter_list:
            sleep(0.1)
            # response = req.get(
            #     f"{self.endpoint}/transmitters/get/external/?band={str(unit.band)}&external_id={str(unit.external_id)}")
            response = self.api_caller.get_transmitter_by_external_id(unit.band, unit.external_id)
            print("ZAPYTANIE:" + str(response) + " " + str(response.text))
            if response.text == "null":
                try:
                    create_transmitter(unit)
                except Exception as e:
                    logging.error(e)
                    print(e)
            else:
                if os.getenv('REGENERATE_MAPS') == 'True':
                    try:
                        update_transmitter(unit)
                    except Exception as e:
                        logging.error(e)
                        print(e)
                else:
                    # compare unit from external source with unit from internal database
                    transmitter_from_internal_source = Transmitter(
                        external_id=int(response.json()["external_id"]),
                        band=response.json()["band"],
                        frequency=float(response.json()["frequency"]),
                        mode=response.json()["mode"],
                        erp=float(response.json()["erp"]),
                        antenna_height=int(response.json()["antenna_height"]),
                        antenna_pattern=response.json()["antenna_pattern"],
                        antenna_direction=response.json()["antenna_direction"],
                        pattern_h=response.json()["pattern_h"],
                        pattern_v=response.json()["pattern_v"],
                        polarisation=response.json()["polarisation"],
                        location=response.json()["location"],
                        region=response.json()["region"],
                        country_id=response.json()["country_id"],
                        latitude=float(response.json()["latitude"]),
                        longitude=float(response.json()["longitude"]),
                        precision=int(response.json()["precision"]),
                        height=int(response.json()["height"]),
                        station=response.json()["station"]
                    )
                    if unit != transmitter_from_internal_source:
                        print(unit.__dict__.items() ^ transmitter_from_internal_source.__dict__.items())
                        try:
                            update_transmitter(unit)
                        except Exception as e:
                            logging.error(e)
                            print(e)
                    else:
                        print("Transmitter is up to date.")

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)


if __name__ == '__main__':
    pass
