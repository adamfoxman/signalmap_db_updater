import csv

import row as row

from models.transmitter import Transmitter


class CSVReader:
    transmitter_list = []

    def __init__(self, filename=None):
        if filename is not None:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file, delimiter=';')
                for line in reader:
                    self.transmitter_list.append(Transmitter(
                        external_id=int(line['id']),
                        frequency=float(line['frequency']),
                        mode=line['mode'],
                        erp=float(line['erp']),
                        antenna_height=int(line['ant']),
                        antenna_direction=line['dirdeg'],
                        antenna_pattern=line['dir'],
                        pattern_h=line['pattern_h'],
                        pattern_v=line['pattern_v'],
                        polarisation=line['pol'],
                        location=line['location'],
                        region=line['reg'],
                        latitude=float(line['latitude']),
                        longitude=float(line['longitude']),
                        precision=int(line['precision']),
                        height=int(line['height']),
                        station=line['station'],
                        country_id="pl"
                    ))
        print(self.transmitter_list)
