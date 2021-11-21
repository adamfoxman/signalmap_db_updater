import os
from csv import DictWriter

class BatchFileGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.batchfile = open(filename, 'w')
        self.fieldnames = [
            'Picture file',
            'System gain',
            'Antenna file',
            'Antenna azimuth',
            'Antenna tilt',
            'Antenna height',
            'Elevation ASL',
            'Mobile antenna height',
            'Frequency',
            'Latitude',
            'Longitude',
            'Map resolution',
            'Maximum range',
            'Color',
            'SRTM path',
            'Landcover path'
        ]
        self.writer = DictWriter(self.batchfile, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def add_entry(self, id: int,
                  ):
