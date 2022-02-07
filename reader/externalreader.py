import csv
import os
import sys
import logging

import requests as req

from reader import Reader
from models.transmitter import Transmitter
from dbupdater.apicaller import InternalAPICaller


def get_api_address(country_code: str):
    """
    Get the API address for the given country code.
    :param country_code: 2-letter ISO country code.
    :return: API address.
    """
    address = str(os.getenv("EXTERNAL_API_ADDRESS")) + "?iso=" + country_code + "&token=" + str(os.getenv("API_TOKEN"))
    return address


class ExternalReader(Reader):
    """
    Reader class for external data sources.
    """
    def __init__(self, external_endpoint: str = None, internal_api_caller: InternalAPICaller = None):
        super().__init__()
        logging.info("Initializing external reader")
        try:
            logging.info("Testing connection to API")
            req.get(external_endpoint)
            self.endpoint = external_endpoint
            self.api_caller = internal_api_caller
            self.api_caller.set_url(os.getenv('INTERNAL_API_ADDRESS'))
        except req.ConnectionError:
            print(f"URL %s is not available on the internet.", external_endpoint)
            logging.critical("URL %s is not available on the internet.", external_endpoint)
            raise Exception("URL is not available on the internet.")

        self.country_list = {}

    def _import_country_data(self, source=None, country: str = None):
        """
        Import data from a CSV file.

        :param source: Source data.
        :param country: 2-letter ISO country code.
        :return: None.
        """
        if source is not None and country is not None:
            csv.field_size_limit(sys.maxsize)
            try:
                reader = csv.DictReader(source, delimiter=';')
                for line in reader:
                    transmitter = Transmitter(
                        band=line["band"],
                        external_id=int(line['id']),
                        frequency=float(line['frequency']),
                        mode=line['mode'],
                        erp=line['erp'],
                        antenna_height=line['ant'],
                        antenna_direction=line['dirdeg'],
                        antenna_pattern=line['dir'],
                        pattern_h=line['pattern_h'],
                        pattern_v=line['pattern_v'],
                        polarisation=line['pol'],
                        location=line['location'],
                        region=line['reg'],
                        latitude=float(line['latitude']),
                        longitude=float(line['longitude']),
                        precision=line['precision'],
                        height=line['height'],
                        station=line['station'],
                        station_id=line['stationid'],
                        logo_id=line['logoid'],
                        country_id=country
                    )
                    self.transmitter_list.append(transmitter)
            except Exception:
                raise Exception("Provided source is not valid")

    def _download_countries(self):
        """
        Download the list of countries.

        :return: None.
        """
        response = self.api_caller.get_countries()
        for country in response.json():
            if country["country_code"] is not None and country["country_code"] not in self.country_list:
                self.country_list[country["country_code"]] = country["is_enabled"]

    def download_data(self):
        """
        Download data from external sources.

        :return: None.
        """
        if self.endpoint is None:
            logging.critical("No endpoint provided")
            raise Exception("Endpoint is not set")
        if len(self.transmitter_list) > 0:
            self.transmitter_list.clear()
        self._download_countries()
        if len(self.country_list) == 0:
            logging.critical("No countries available")
            raise Exception("No countries found")
        for country in self.country_list:
            if self.country_list[country]:
                try:
                    logging.info("Downloading data for country %s", country)
                    headers = {'user-agent': 'SignalMap Updater 1.0'}
                    request = req.get(get_api_address(country), headers=headers)
                    # data = request.content.decode('utf-8').split('\r\n')
                    data = request.content.decode('utf-8', errors='ignore').strip().split('\r\n')
                    self._import_country_data(data, country)
                except Exception as e:
                    logging.error("Error while downloading data for country %s: %s", country, e)
                    raise Exception("Error while downloading data for country " + country)


if __name__ == "__main__":
    pass
