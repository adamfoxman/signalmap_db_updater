import unittest
from models.transmitter import Transmitter


class MyTestCase(unittest.TestCase):
    def test_transmitter(self):
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
        self.assertEqual(first.__str__(), 'FM Radio 10.0 kW transmitter with external id = 6400001 working on 87.5 MHz from Częstochowa/Wręczyca in PL')
        self.assertEqual(first.coverage_file, None)
        self.assertEqual(first.north_bound, None)
        self.assertEqual(first.south_bound, None)
        self.assertEqual(first.east_bound, None)
        self.assertEqual(first.west_bound, None)
        first.north_bound = 51.0
        first.south_bound = 50.0
        first.east_bound = 19.0
        first.west_bound = 18.0
        self.assertEqual(first.north_bound, 51.0)
        self.assertEqual(first.south_bound, 50.0)
        self.assertEqual(first.east_bound, 19.0)
        self.assertEqual(first.west_bound, 18.0)
        second = Transmitter(
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
        self.assertEqual(first == second, True)
        self.assertEqual(first != second, False)
        third = Transmitter(
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
            erp=30.0,
            pattern_h='38.2   38 38.3 38.3 37.5 36.9 37.7   39 39.9   40 39.6 38.9 37.8 36.9 36.6 36.6   36 34.8 34.4 35.5 36.4 36.5   36 35.3   35 35.4 36.2 36.4   36   36 37.3 38.9 39.7 39.9 39.6 38.9',
            pattern_v=''
        )
        self.assertEqual(first == third, False)


if __name__ == '__main__':
    unittest.main()
