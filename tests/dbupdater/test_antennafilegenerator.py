import unittest
import pathlib as pl
from models.transmitter import Transmitter
from dbupdater.antennafilegenerator import get_antenna_file, split_string_to_list
from dbupdater.dbupdater import delete_file


class MyTestCase(unittest.TestCase):
    def test_antennafilegenerator(self):
        first = Transmitter(
            band='f',
            external_id=6400001,
            frequency=87.500000,
            mode='s',
            antenna_pattern='D',
            antenna_direction='',
            polarisation='h',
            location='Częstochowa/Wręczyca',
            region='SL',
            country_id='PL',
            latitude=50.846978,
            longitude=18.863581,
            station='Polskie Radio Jedynka',
            height=272,
            precision=3,
            antenna_height=250,
            erp=10.0,
            pattern_h='38.2   38 38.3 38.3 37.5 36.9 37.7   39 39.9   40 39.6 38.9 37.8 36.9 36.6 36.6   36 34.8 34.4 35.5 36.4 36.5   36 35.3   35 35.4 36.2 36.4   36   36 37.3 38.9 39.7 39.9 39.6 38.9',
            pattern_v=''
        )
        split_pattern = split_string_to_list(first.pattern_h)
        self.assertEqual(len(split_pattern), 36)
        self.assertEqual(split_pattern[0], '38.2')
        self.assertEqual(split_pattern[35], '38.9')
        location_filename = f"{first.country_id}_{first.band}_{first.external_id}"
        self.assertEqual(get_antenna_file('./',
                                          location_filename,
                                          first.antenna_direction,
                                          first.pattern_h,
                                          first.pattern_v),
                         f"{location_filename}.az")
        self.assertIsFile(f"./{location_filename}.az")
    #     open the file, read line by line and check if it contains the right data
        with open(f"./{location_filename}.az", 'r') as f:
            lines = f.readlines()
            self.assertEqual(lines[0], '0.0\n')
            self.assertEqual(lines[1], '0   38.2\n')
            self.assertEqual(lines[10], '10   38.0\n')

    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"{path} is not a file")


if __name__ == '__main__':
    unittest.main()
