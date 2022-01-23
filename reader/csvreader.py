import csv
import urllib

from models.transmitter import Transmitter
from reader.reader import Reader


class CSVReader(Reader):
    def __init__(self, source: str = None):
        super().__init__(source)
        if source is not None:
            self.import_data(source)

    # Imports data from CSV
    def import_data(self, source: str):
        if source != '':
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
                            country_id="PL"
                        ))
            except IOError:
                raise Exception("Provided file does not exist or is not valid")

if __name__ == "__main__":
    pass
