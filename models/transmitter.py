class Transmitter:
    """
    Class representing a transmitter, which will be added to a database.

    :param band: The band of the transmitter (FM/DAB/TV).
    :param external_id: The external id of the transmitter.
    :param frequency: The frequency of the transmitter.
    :param mode: The mode of the transmitter.
    :param erp: The Effective Radiated Power of the transmitter.
    :param antenna_height: The height of the antenna above the ground.
    :param antenna_pattern: The antenna pattern of the transmitter (directional or not).
    :param antenna_direction: The direction of the antenna.
    :param polarisation: The antenna polarisation of the transmitter.
    :param location: The location of the transmitter.
    :param region: The region of the transmitter.
    :param country_id: The country ISO code of the transmitter.
    :param latitude: The latitude of the transmitter.
    :param longitude: The longitude of the transmitter.
    :param precision: The precision of the transmitter as given by external database.
    :param height: The height of the transmitter above sea level.
    :param station: The transmitted program.
    :param pattern_h: The horizontal antenna pattern of the transmitter.
    :param pattern_v: The vertical antenna pattern of the transmitter.

    :returns: Nothing.
    """
    band: str = None
    external_id: int = None
    frequency: float = None
    mode: str = None
    erp: float = 1.0
    antenna_height: int = 100
    antenna_pattern: str = None
    antenna_direction: str = None
    pattern_h: str = None
    pattern_v: str = None
    polarisation: str = None
    location: str = None
    region: str = None
    country_id: str = None
    latitude: float = None
    longitude: float = None
    precision: int = 3
    height: int = None
    station: str = None
    station_id: int = None
    logo_id: int = None
    coverage_file: str = None
    north_bound: float = None
    south_bound: float = None
    east_bound: float = None
    west_bound: float = None

    def __init__(self,
                 band: str,
                 external_id: int,
                 frequency: float,
                 mode: str,
                 antenna_pattern: str,
                 antenna_direction: str,
                 polarisation: str,
                 location: str,
                 region: str,
                 country_id: str,
                 latitude: float,
                 longitude: float,
                 station: str,
                 station_id: int,
                 logo_id: int,
                 height: int,
                 precision: int = 3,
                 antenna_height: int = 100,
                 erp: float = 1.0,
                 pattern_h: str = None,
                 pattern_v: str = None):
        self.band = band
        self.external_id = external_id
        self.frequency = frequency
        self.erp = erp if erp is not None or erp != "" else 0.0
        self.antenna_height = antenna_height if antenna_height != "" else 0
        self.location = location
        self.region = region if region is not None else ""
        self.country_id = country_id
        self.latitude = latitude
        self.longitude = longitude
        self.station = station
        self.station_id = station_id
        self.logo_id = logo_id
        self.antenna_direction = antenna_direction
        self.height = height if height != "" else 0
        self.pattern_h = pattern_h if pattern_h is not None else ""
        self.pattern_v = pattern_v if pattern_v is not None else ""
        self.mode = mode
        self.antenna_pattern = antenna_pattern if antenna_pattern is not None else ""
        self.polarisation = polarisation
        self.precision = precision if precision != "" else 0

    def __str__(self):
        if self.band == 'f':
            type_of_transmitter = 'FM radio'
        elif self.band == 'd':
            type_of_transmitter = 'DAB radio'
        elif self.band == 't':
            type_of_transmitter = 'TV'
        else:
            type_of_transmitter = 'Unknown'
        return f"{type_of_transmitter} {self.erp} kW transmitter with external id = {self.external_id} working on {self.frequency} MHz from {self.location} in {self.country_id}"

    def __eq__(self, other):
        if not isinstance(other, Transmitter):
            return False
        if int(self.height) != int(other.height):
            return False
        if int(self.external_id) != int(other.external_id):
            return False
        if float(self.frequency) != float(other.frequency):
            return False
        if int(self.antenna_height) != int(other.antenna_height):
            return False
        if str(self.antenna_pattern) != str(other.antenna_pattern):
            return False
        if str(self.band) != str(other.band):
            return False
        if float(self.erp) != float(other.erp):
            return False
        if float(self.latitude) != float(other.latitude):
            return False
        if float(self.longitude) != float(other.longitude):
            return False
        if str(self.location) != str(other.location):
            return False
        if str(self.polarisation) != str(other.polarisation):
            return False
        if str(self.region) != str(other.region):
            return False
        if str(self.station) != str(other.station):
            return False
        if int(self.station_id) != int(other.station_id):
            return False
        if str(self.country_id) != str(other.country_id):
            return False
        if str(self.pattern_h) != str(other.pattern_h):
            return False
        if str(self.pattern_v) != str(other.pattern_v):
            return False
        return True


if __name__ == "__main__":
    pass
