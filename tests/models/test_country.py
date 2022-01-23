import unittest
from models.country import Country, CountryCompare


class MyTestCase(unittest.TestCase):
    def test_country(self):
        poland = Country(name="Poland", code="PL")
        self.assertEqual(poland.name, "Poland")
        self.assertEqual(poland.code, "PL")
        self.assertEqual(poland.is_enabled, False)
        czech = Country(name="Czech Republic", code="CZ", is_enabled=True)
        self.assertEqual(czech.name, "Czech Republic")
        self.assertEqual(czech.code, "CZ")
        self.assertEqual(czech.is_enabled, True)


if __name__ == '__main__':
    unittest.main()
