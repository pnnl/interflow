import unittest
from interflow.reader import *


class TestReader(unittest.TestCase):
    """Conduct tests for functions of reader.py."""

    def test_read_sample_data(self):
        """Test read_sample_data()."""

        # load the data
        df = read_sample_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

        # check for correct number of columns
        x = df.columns.to_list()
        self.assertTrue(len(x) == 16)

    def test_get_state_fips_crosswalk_data(self):
        """Test get_state_fips_crosswalk_data()."""

        # load the data
        df = get_state_fips_crosswalk_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_load_geojson_data(self):
        """Test load_geojson_data()."""

        # load the data
        geo = load_sample_geojson_data()

        # returns a geojson dictionary
        self.assertTrue(type(geo) == dict)


if __name__ == '__main__':
    unittest.main()
