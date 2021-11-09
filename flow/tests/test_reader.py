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


if __name__ == '__main__':
    unittest.main()
