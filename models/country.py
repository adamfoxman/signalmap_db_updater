class Country:
    country_code: str
    country_name: str
    is_enabled: bool

    def __init__(self, country_code: str, country_name: str, is_enabled: bool):
        self.country_code = country_code
        self.country_name = country_name
        self.is_enabled = is_enabled


class CountryCompare:
    country_code: str
    country_name: str

    def __init__(self, country_code: str, country_name: str):
        self.country_code = country_code
        self.country_name = country_name
