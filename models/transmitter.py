from enum import Enum as EnumType


class Transmitter:
    external_id: int = None
    frequency: float = None
    # mode: TransmitterType = TransmitterType.NONE
    mode: str = None
    erp: float = 1
    antenna_height: int = 100
    # antenna_pattern: RadiationPattern = RadiationPattern.NONE
    antenna_pattern: str = None
    antenna_direction: int = None
    pattern_h: str = None
    pattern_v: str = None
    # polarisation: Polarisation = Polarisation.NONE
    polarisation: str = None
    location: str = None
    region: str = None
    country_id: str = None
    latitude: float = None
    longitude: float = None
    # precision: Precision = Precision.NONE
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
        # self.antenna_direction = antenna_direction
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
