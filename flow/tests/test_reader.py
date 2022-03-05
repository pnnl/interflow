import unittest
from flow.reader import *


class TestReader(unittest.TestCase):
    """Conduct test for functions of reader.py."""

    def test_read_sample_data(self):
        """Test read_sample_data()."""

        # load the data
        df = read_sample_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

        # check for correct number of columns
        x = df.columns.to_list()
        self.assertTrue(len(x) == 16)

    def test_get_water_use_2015_data(self):
        """Test get_water_use_2015_data()."""

        # load the data
        df = get_water_use_2015_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_water_use_rename_data(self):
        """Test get_water_use_rename_data()."""

        # load the data
        df = get_water_use_rename_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_water_use_1995_data(self):
        """Test get_water_use_1995_data()."""

        # load the data
        df = get_water_use_1995_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_water_consumption_rename_data(self):
        """Test get_water_consumption_rename_data()."""

        # load the data
        df = get_water_consumption_rename_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_tx_ibt_data(self):
        """Test get_tx_ibt_data()."""

        # load the data
        df = get_tx_ibt_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_west_ibt_data(self):
        """Test get_west_ibt_data()."""

        # load the data
        df = get_west_ibt_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_county_fips_data(self):
        """Test get_county_fips_data()."""

        # load the data
        df = get_county_fips_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_wastewater_flow_data(self):
        """Test get_wastewater_flow_data()."""

        # load the data
        df = get_wastewater_flow_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_wastewater_type_data(self):
        """Test get_wastewater_type_data()."""

        # load the data
        df = get_wastewater_type_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_wastewater_location_data(self):
        """Test get_wastewater_location_data()."""

        # load the data
        df = get_wastewater_location_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_wastewater_discharge_data(self):
        """Test get_wastewater_discharge_data()."""

        # load the data
        df = get_wastewater_discharge_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_power_plant_location_data(self):
        """Test get_power_plant_location_data()."""

        # load the data
        df = get_power_plant_location_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_electricity_generation_data(self):
        """Test get_electricity_generation_data()."""

        # load the data
        df = get_electricity_generation_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_electricity_water_intensity_data(self):
        """Test get_electricity_water_intensity_data()."""

        # load the data
        df = get_electricity_water_intensity_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_electricity_cooling_flow_data(self):
        """Test get_electricity_cooling_flow_data()."""

        # load the data
        df = get_electricity_cooling_flow_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_irrigation_pumping_data(self):
        """Test get_irrigation_pumping_data()."""

        # load the data
        df = get_irrigation_pumping_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_pumping_intensity_rename_data(self):
        """Test get_pumping_intensity_rename_data()."""

        # load the data
        df = get_pumping_intensity_rename_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_electricity_demand_data(self):
        """Test get_electricity_demand_data()."""

        # load the data
        df = get_electricity_demand_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_fuel_demand_data(self):
        """Test get_fuel_demand_data()."""

        # load the data
        df = get_fuel_demand_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_state_fuel_production_data(self):
        """Test get_state_fuel_production_data()."""

        # load the data
        df = get_state_fuel_production_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_state_water_to_conventional_oil_data(self):
        """Test get_state_water_to_conventional_oil_data()."""

        # load the data
        df = get_state_water_to_conventional_oil_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_state_petroleum_natgas_water_data(self):
        """Test get_state_petroleum_natgas_water_data()."""

        # load the data
        df = get_state_petroleum_natgas_water_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_petroleum_natgas_rename_data(self):
        """Test get_petroleum_natgas_rename_data()."""

        # load the data
        df = get_petroleum_natgas_rename_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def get_coal_production_data(self):
        """Test get_coal_production_data()."""

        # load the data
        df = get_coal_production_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_coal_mine_location_data(self):
        """Test get_coal_mine_location_data()."""

        # load the data
        df = get_coal_mine_location_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_state_fips_crosswalk_data(self):
        """Test get_state_fips_crosswalk_data()."""

        # load the data
        df = get_state_fips_crosswalk_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_corn_irrigation_data(self):
        """Test get_corn_irrigation_data()."""

        # load the data
        df = get_corn_irrigation_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_get_corn_production_data(self):
        """Test get_corn_production_data()."""

        # load the data
        df = get_corn_production_data()

        # returns a dataframe
        self.assertTrue(type(df) == pd.DataFrame)

    def test_load_geojson_data(self):
        """Test load_geojson_data()."""

        # load the data
        geo = load_geojson_data()

        # returns a geojson dictionary
        self.assertTrue(type(geo) == dict)


if __name__ == '__main__':
    unittest.main()
