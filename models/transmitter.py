class Transmitter:
    band: str = None
    external_id: int = None
    frequency: float = None
    mode: str = None
    erp: float = 1
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
    kml_file: str = None
    coverage: str = None

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
                 precision: int = 3,
                 antenna_height: int = 100,
                 erp: float = 1,
                 height: int = 100,
                 pattern_h: str = None,
                 pattern_v: str = None):
        """
        Class representing a transmitter, which will be added to a database.

        Parameters
        ----------
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
        self.band = band
        self.external_id = external_id
        self.frequency = frequency
        self.erp = erp
        self.antenna_height = antenna_height
        self.location = location
        self.region = region
        self.country_id = country_id
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.station = station

        self.antenna_direction = antenna_direction

        if pattern_h is not None:
            self.pattern_h = pattern_h
        if pattern_v is not None:
            self.pattern_v = pattern_v

        self.mode = mode
        self.antenna_pattern = antenna_pattern
        self.polarisation = polarisation
        self.precision = precision

    def __str__(self):
        if self.band == 'f':
            type_of_transmitter = 'FM radio'
        elif self.band == 'd':
            type_of_transmitter = 'DAB radio'
        elif self.band == 't':
            type_of_transmitter = 'TV'
        else:
            type_of_transmitter = 'Unknown'
        return f"{type_of_transmitter} Transmitter(band={self.band}, external_id={self.external_id}, frequency={self.frequency}, mode={self.mode}, erp={self.erp}, antenna_height={self.antenna_height}, antenna_pattern={self.antenna_pattern}, antenna_direction={self.antenna_direction}, polarisation={self.polarisation}, location={self.location}, region={self.region}, country_id={self.country_id}, latitude={self.latitude}, longitude={self.longitude}, precision={self.precision}, height={self.height}, station={self.station}, pattern_h={self.pattern_h}, pattern_v={self.pattern_v}) "
