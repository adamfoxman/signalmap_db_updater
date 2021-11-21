from enum import Enum as EnumType


class Transmitter:
    external_id: int = None
    frequency: float = None
    mode: str = None
    erp: float = 1
    antenna_height: int = 100
    antenna_pattern: str = None
    antenna_direction: int = None
    pattern_h: str = None
    pattern_v: str = None
    polarisation: str = None
    location: str = None
    region: str = None
    country_id: str = None
    latitude: float = None
    longitude: float = None
    precision: int = None
    height: int = None
    station: str = None

    def __init__(self,
                 external_id: int,
                 frequency: float,
                 mode: str,
                 erp: float,
                 antenna_height: int,
                 antenna_pattern: str,
                 antenna_direction: int,
                 polarisation: str,
                 location: str,
                 region: str,
                 country_id: str,
                 latitude: float,
                 longitude: float,
                 precision: int,
                 height: int,
                 station: str,
                 pattern_h: str = None,
                 pattern_v: str = None):
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

        if antenna_direction == '':
            self.antenna_direction = None
        else:
            self.antenna_direction = int(antenna_direction)

        if pattern_h is not None:
            self.pattern_h = pattern_h
        if pattern_v is not None:
            self.pattern_v = pattern_v

        self.mode = mode
        self.antenna_pattern = antenna_pattern
        self.polarisation = polarisation
        self.precision = precision

    def __str__(self):
        return "Transmitter(external_id={}, frequency={}, mode={}, erp={}, antenna_height={}, antenna_pattern={}, antenna_direction={}, polarisation={}, location={}, region={}, country_id={}, latitude={}, longitude={}, precision={}, height={}, station={}, pattern_h={}, pattern_v={})".format(
            self.external_id,
            self.frequency,
            self.mode,
            self.erp,
            self.antenna_height,
            self.antenna_pattern,
            self.antenna_direction,
            self.polarisation,
            self.location,
            self.region,
            self.country_id,
            self.latitude,
            self.longitude,
            self.precision,
            self.height,
            self.station,
            self.pattern_h,
            self.pattern_v
        )
