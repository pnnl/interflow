import unittest

from flow.prep import *
from flow.reader import get_interconnect_data


class TestReader(unittest.TestCase):
    """Conduct test for functions of reader.py."""

    def test_prep_water_2015(self):
        """Ensure we get what is expected from  prep_water_2025()."""

        # load input data
        df_interconnect = get_interconnect_data()

        # load data
        df = prep_water_2015(df_interconnect)

        # expected number of columns
        self.assertEqual(df.columns.shape[0], 142)

        # ensure interconnect field has expected values
        expected_columns = set(['East', 'None', 'West', 'ERCOT'])
        not_in_expected = set(df['Interconnect'].unique()) - expected_columns
        not_in_produced = expected_columns - set(df['Interconnect'].unique())

        self.assertEqual(len(not_in_expected), 0)
        self.assertEqual(len(not_in_produced), 0)


if __name__ == '__main__':
    unittest.main()
