import unittest

from flow.reader import *


class TestReader(unittest.TestCase):
    """Conduct test for functions of reader.py."""

    def test_get_water_use_2015(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_water_use_2015()

        # expected number of columns
        self.assertEqual(df.columns.shape[0], 141)

        # expect FIPS as a column name
        self.assertTrue('FIPS' in df.columns)

    def test_get_water_use_1995(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_water_use_1995()

        # expect StateCode as a column name
        self.assertTrue('StateCode' in df.columns)

        # expect CountyCode as a column name
        self.assertTrue('CountyCode' in df.columns)

    def test_get_interconnect_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_interconnect_data()

        # expect FIPS as a column name
        self.assertTrue('FIPS' in df.columns)

        # expect Interconnect as a column name
        self.assertTrue('Interconnect' in df.columns)

if __name__ == '__main__':
    unittest.main()
