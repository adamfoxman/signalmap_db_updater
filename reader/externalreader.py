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


class ExternalReader(Reader):
    def __init__(self, source=None, endpoint: str = None):
        super().__init__()
        self.source = source
        self.endpoint = endpoint
        self.country_list = {}

    def _import_country_data(self, source=None, country: str = None):
        if source is not None and country is not None:
            csv.field_size_limit(sys.maxsize)
            try:
                reader = csv.DictReader(source, delimiter=';')
                for line in reader:
                    print(line)
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
                    print(transmitter)
                    self.transmitter_list.append(transmitter)
            except Exception:
                raise Exception("Provided source is not valid")

    def _download_countries(self):
        response = req.get(self.endpoint + "/countries/")
        for country in response.json():
            self.country_list.update({country["country_code"]: country["is_enabled"]})

    def download_data(self):
        self._download_countries()
        for country in self.country_list:
            if self.country_list[country]:
                headers = {'user-agent': 'SignalMap Updater 1.0'}
                request = requests.get(self._get_api_address(country), headers=headers)
                data = request.content.decode('utf-8').split('\r\n')
                self._import_country_data(data, country)
                # request = urllib.request.Request(
                #     url=self._get_api_address(country),
                #     data=None,
                #     headers=headers
                # )
                #
                # with urllib.request.urlopen(request) as url:
                #     data = url.read()
                #     self._import_country_data(source=data, country=country)

    def _get_api_address(self, country_code: str):
        address = str(os.getenv("API_ADDRESS")) + "?iso=" + country_code + "&token=" + str(os.getenv("API_TOKEN"))
        print(address)
        return address
