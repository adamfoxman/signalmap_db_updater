from reader import Reader

import csv

from models.transmitter import Transmitter


class ExternalReader(Reader):
    def __init__(self, source=None, country: str = None):
        super().__init__()
        self.source = source
        self.country = country
        if self.source is not None and self.country is not None:
            self.import_data(self.source, self.country)

    def import_data(self, source=None, country: str = None):
        if source is not None and country is not None:
            try:
                with open(source, 'r') as file:
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
                            country_id=country
                        ))
            except IOError:
                raise Exception("Provided file does not exist or is not valid")
