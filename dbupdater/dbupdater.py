from time import sleep

import requests as req
from json import dumps


class DBUpdater:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.transmitter_list = []
        self.country_list = {}
        try:
            req.get(endpoint)
            self.endpoint = endpoint
        except req.ConnectionError:
            print(f"URL %s is not available on the internet.", endpoint)

    def set_transmitter_list(self, tlist):
        if isinstance(tlist, list):
            self.transmitter_list = tlist

    def update_database(self):
        for unit in self.transmitter_list:
            sleep(0.2)
            response = req.get(f"http://localhost/api/v1/transmitters/get/external/?external_id={str(unit.external_id)}")
            print("ZAPYTANIE:" + str(response) + " " + str(response.text))
            if response.text == "null":
                json_transmitter = self.__convert_transmitter_obj_to_json(unit)
                print("to co wysylamy:" + str(json_transmitter))
                res = req.post("http://localhost/api/v1/transmitters/create/", json_transmitter)
                print("ODPOWIEDŻ: " + str(res.text))
            else:
                print("Już istnieje.")

    def __convert_transmitter_obj_to_json(self, obj):
        return dumps(obj.__dict__)
