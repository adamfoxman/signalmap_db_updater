import csv
import urllib.request
import os
import sys
from io import IOBase
from io import BytesIO

import requests
import requests as req

from reader import Reader
from models.transmitter import Transmitter


def get_api_address(country_code: str):
    """
    Get the API address for the given country code.
    :param country_code: 2-letter ISO country code.
    :return: API address.
    """
    address = str(os.getenv("API_ADDRESS")) + "?iso=" + country_code + "&token=" + str(os.getenv("API_TOKEN"))
    print(address)
    return address


class ExternalReader(Reader):
    """
    Reader class for external data sources.
    """
    def __init__(self, endpoint: str = None):
        super().__init__()
        self.endpoint = endpoint
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
        response = req.get(self.endpoint + "/countries/")
        for country in response.json():
            if country["country_code"] is not None and country["country_code"] not in self.country_list:
                self.country_list[country["country_code"]] = country["is_enabled"]

    def download_data(self):
        """
        Download data from external sources.

        :return: None.
        """
        if self.endpoint is None:
            raise Exception("Endpoint is not set")
        if len(self.transmitter_list) > 0:
            self.transmitter_list.clear()
        self._download_countries()
        if len(self.country_list) is 0:
            raise Exception("No countries found")
        for country in self.country_list:
            if self.country_list[country]:
                headers = {'user-agent': 'SignalMap Updater 1.0'}
                request = requests.get(get_api_address(country), headers=headers)
                data = request.content.decode('utf-8').split('\r\n')
                self._import_country_data(data, country)
