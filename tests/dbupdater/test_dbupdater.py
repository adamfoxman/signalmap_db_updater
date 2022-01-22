from dbupdater import get_antenna_file, get_location_file, run_simulation, get_boundaries
from models import Transmitter


def dbupdater_test():
    t = Transmitter(
        external_id=6400936,
        band='f',
        frequency=91.7,
        mode='s',
        erp=2,
        antenna_height=97,
        antenna_pattern='D',
        antenna_direction='',
        pattern_h='',
        pattern_v='33   22 21.5   23   31   31   33   33   33   33 15.5   15   15   22   25   27   29   29   30   33  '
                  ' 33   33   27   27   33   33   33   33   33   33   33   33   33 25.5 25.5   33',
        polarisation='v',
        location='Wągrowiec/Chojna',
        region='WP',
        country_id='PL',
        latitude=53.013172,
        longitude=17.290322,
        precision=3,
        height=126,
        station='RMF FM'
    )
    manual_test_creating_transmitter(t)


def manual_test_creating_transmitter(unit: Transmitter):
    location_filename = f"{unit.country_id}_{unit.band}_{unit.external_id}"
    get_antenna_file('./', location_filename, unit.antenna_direction, unit.pattern_h, unit.pattern_v)
    get_location_file('./', location_filename, unit.station, unit.latitude, unit.longitude,
                      unit.antenna_height if unit.antenna_height != 0 else 100)
    run_simulation('./', location_filename, unit.band, float(unit.erp), float(unit.frequency))
    north, south, east, west = get_boundaries(f"./{location_filename}.kml")
    if north != 0 and south != 0 and east != 0 and west != 0:
        unit.north_bound = north
        unit.south_bound = south
        unit.east_bound = east
        unit.west_bound = west
