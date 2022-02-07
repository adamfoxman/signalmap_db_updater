import requests as req
import logging
import os
import json


class APICallerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class InternalAPICaller(metaclass=APICallerMeta):
    url: str = ''
    token: str = ''
    headers: dict = {}

    def set_url(self, url):
        if self.url != url:
            self.url = url
        else:
            return

        if url.endswith('/'):
            self.url = url[:-1]
        try:
            token_url = self.url + "/api/v1/login/access-token"
            data = f"username={os.getenv('USERNAME')}&password={os.getenv('PASSWORD')}"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'accept': 'application/json'
            }
            r = req.post(token_url, data=data, headers=headers)
            if r.json()['access_token']:
                logging.info("Successfully logged in")
                self.token = r.json()['access_token']
                self.headers = {
                    'Authorization': f"Bearer {self.token}",
                    'Content-Type': 'application/json',
                    'accept': 'application/json'
                }
        except req.exceptions.RequestException as e:
            print(e)
            logging.error(e)

    def get_transmitter_by_external_id(self, band: str, external_id: int):
        url = f"{self.url}/api/v1/transmitters/get/external/?band={str(band)}&external_id={str(external_id)}"
        r = req.get(url, headers=self.headers)
        return r

    def create_transmitter(self, transmitter: str):
        try:
            json.loads(transmitter)
        except Exception as e:
            print(e)
            logging.error(e)

        return req.post(f"{self.url}/api/v1/transmitters/create/", data=transmitter, headers=self.headers)

    def update_transmitter(self, band: str, external_id: int, transmitter: str):
        try:
            json.loads(transmitter)
        except Exception as e:
            print(e)
            logging.error(e)

        return req.put(f"{self.url}/api/v1/transmitters/update/?band={str(band)}&external_id={str(external_id)}",
                       data=transmitter,
                       headers=self.headers)

    def get_countries(self):
        return req.get(f"{self.url}/api/v1/countries/",
                       headers=self.headers)

    def create_country(self, country: str):
        try:
            json.loads(country)
        except Exception as e:
            print(e)
            logging.error(e)

        return req.post(f"{self.url}/api/v1/countries/create/",
                        data=country,
                        headers=self.headers)

    def update_country(self, country: str):
        try:
            json.loads(country)
        except Exception as e:
            print(e)
            logging.error(e)

        return req.put(f"{self.url}/api/v1/countries/update/", data=country, headers=self.headers)

    def delete_country(self, country_code: str):
        return req.delete(f"{self.url}/api/v1/countries/delete/?country_code={country_code}", headers=self.headers)


api_caller = InternalAPICaller()

if __name__ == '__main__':
    api_caller.set_url(os.getenv('INTERNAL_API_ADDRESS'))
