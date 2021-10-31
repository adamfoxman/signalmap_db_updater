from enum import Enum as EnumType

class TransmitterType(EnumType):
    NONE = 0
    m = 1
    s = 2
    D = 3
    X = 4
    a = 5


class RadiationPattern(EnumType):
    NONE = 0
    D = 1
    N = 2


class Polarisation(EnumType):
    NONE = 0
    h = 1
    v = 2
    m = 3
    s = 4
    c = 5


class Precision(EnumType):
    NONE = 0
    ONE_KM = 1
    HUNDRED_METRES = 2
    TEN_METRES = 3


class Transmitter:
    external_id: int = None
    frequency: float = None
    mode: TransmitterType = TransmitterType.NONE
    erp: float = 1
    antenna_height: int = 100
    antenna_pattern: RadiationPattern = RadiationPattern.NONE
    antenna_direction: int = None
    pattern_h: str = None
    pattern_v: str = None
    polarisation: Polarisation = Polarisation.NONE
    location: str = None
    region: str = None
    country_id: str = None
    latitude: float = None
    longitude: float = None
    precision: Precision = Precision.NONE
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

        self.mode = self.__set_mode(mode)
        self.antenna_pattern = self.__set_pattern(antenna_pattern)
        self.polarisation = self.__set_polarization(polarisation)
        self.precision = self.__set_precision(precision)

    def __set_mode(self, mode: str = None):
        if mode is not None and mode != '':
            return TransmitterType[mode]
        else:
            return TransmitterType.NONE

    def __set_pattern(self, pattern: str = None):
        if pattern is not None and pattern != '':
            return RadiationPattern[pattern]
        else:
            return RadiationPattern.NONE

    def __set_polarization(self, polarisation: str = None):
        if polarisation is not None and polarisation != '':
            return Polarisation[polarisation]
        else:
            return Polarisation.NONE

    def __set_precision(self, precision: int = None):
        if precision is not None:
            return Precision(precision)
        else:
            return Precision.NONE
