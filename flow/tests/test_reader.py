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

    def test_get_population_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_population_data()

        # expect STATE FIPS as a column name
        self.assertTrue('STATE FIPS' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('COUNTY FIPS' in df.columns)

    def test_get_wastewater_flow_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_wastewater_flow_data()

        # expect STATE FIPS as a column name
        self.assertTrue('CWNS_NUMBER' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('EXIST_TOTAL' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('EXIST_MUNICIPAL' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('EXIST_INDUSTRIAL' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('EXIST_INFILTRATION' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('EXIST_WET_WEATHER_PEAK' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('PRES_WET_WEATHER_PEAK' in df.columns)

    def test_get_wastewater_facility_type_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_wastewater_facility_type_data()

        # expect STATE FIPS as a column name
        self.assertTrue('CWNS_NUMBER' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('PRES_EFFLUENT_TREATMENT_LEVEL' in df.columns)

    def test_get_wastewater_facility_loc_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_wastewater_facility_loc_data()

        # expect STATE FIPS as a column name
        self.assertTrue('CWNS_NUMBER' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('STATE' in df.columns)

        # expect COUNTY FIPS as a column name
        self.assertTrue('PRIMARY_COUNTY' in df.columns)

        # expect PRES_FACILITY_OVERALL_TYPE as a column name
        self.assertTrue('PRES_FACILITY_OVERALL_TYPE' in df.columns)

    def test_get_wastewater_facility_discharge_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_wastewater_facility_discharge_data()

        # expect STATE FIPS as a column name
        self.assertTrue('CWNS_NUMBER' in df.columns)

        # expect DISCHARGE_METHOD as a column name
        self.assertTrue('DISCHARGE_METHOD' in df.columns)

        # expect PRES_FLOW_PERCENTAGE as a column name
        self.assertTrue('PRES_FLOW_PERCENTAGE' in df.columns)

    def test_get_electricity_generation_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_electricity_generation_data()

        # expect Plant Id as a column name
        self.assertTrue('Plant Id' in df.columns)

        # expect AER\nFuel Type Code as a column name
        self.assertTrue('AER\nFuel Type Code' in df.columns)

        # expect Plant State as a column name
        self.assertTrue('Plant State' in df.columns)

        # expect Total Fuel Consumption\nMMBtu as a column name
        self.assertTrue('Total Fuel Consumption\nMMBtu' in df.columns)

        # expect Net Generation\n(Megawatthours) as a column name
        self.assertTrue('Net Generation\n(Megawatthours)' in df.columns)

    def test_get_irrigation_depth_pressure_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_irrigation_depth_pressure_data()

        # expect STATE as a column name
        self.assertTrue('STATE' in df.columns)

        # expect Average Well Depth (ft) as a column name
        self.assertTrue('Average Well Depth (ft)' in df.columns)

        # expect Average operating pressure (psi) as a column name
        self.assertTrue('Average operating pressure (psi)' in df.columns)

        # expect Elec_Total_Acres as a column name
        self.assertTrue('Elec_Total_Acres' in df.columns)

        # expect NG_Total_Acres as a column name
        self.assertTrue('NG_Total_Acres' in df.columns)

        # expect Propane_Total_Acres as a column name
        self.assertTrue('Propane_Total_Acres' in df.columns)

        # expect Diesel_Total_Acres as a column name
        self.assertTrue('Diesel_Total_Acres' in df.columns)

        # expect Gas_Total_Acres as a column name
        self.assertTrue('Gas_Total_Acres' in df.columns)

    def test_tx_inter_basin_transfer_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_tx_inter_basin_transfer_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect County_Used as a column name
        self.assertTrue('County_Used' in df.columns)

        # expect Used_FIPS as a column name
        self.assertTrue('Used_FIPS' in df.columns)

        # expect Source_FIPS as a column name
        self.assertTrue('Source_FIPS' in df.columns)

        # expect Elevation Difference (Feet) as a column name
        self.assertTrue('Elevation Difference (Feet)' in df.columns)

        # expect Total_Intake__Gallons (Acre-Feet/Year) as a column name
        self.assertTrue('Total_Intake__Gallons (Acre-Feet/Year)' in df.columns)

    def test_get_west_inter_basin_transfer_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_west_inter_basin_transfer_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect FIPS as a column name
        self.assertTrue('FIPS' in df.columns)

        # expect Mwh/yr (Low) as a column name
        self.assertTrue('Mwh/yr (Low)' in df.columns)

        # expect Mwh/yr (High) as a column name
        self.assertTrue('Mwh/yr (High)' in df.columns)

    def test_get_residential_electricity_demand_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_residential_electricity_demand_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect Sales (Megawatthours) as a column name
        self.assertTrue('Sales (Megawatthours)' in df.columns)

    def test_get_commercial_electricity_demand_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_commercial_electricity_demand_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect Sales (Megawatthours) as a column name
        self.assertTrue('Sales (Megawatthours)' in df.columns)

    def test_get_industrial_electricity_demand_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_industrial_electricity_demand_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect Sales (Megawatthours) as a column name
        self.assertTrue('Sales (Megawatthours)' in df.columns)

    def test_get_transportation_electricity_demand_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_transportation_electricity_demand_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect Sales (Megawatthours) as a column name
        self.assertTrue('Sales (Megawatthours)' in df.columns)

    def test_get_energy_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_energy_production_data()

        # expect StateCode as a column name
        self.assertTrue('StateCode' in df.columns)

        # expect MSN as a column name
        self.assertTrue('MSN' in df.columns)

    def test_get_corn_irrigation_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_corn_irrigation_data()

        # expect StateAbb as a column name
        self.assertTrue('StateAbb' in df.columns)

        # expect Acre-feet-Applied_All as a column name
        self.assertTrue('Acre-feet-Applied_All' in df.columns)

        # expect Acres_Corn_Harvested as a column name
        self.assertTrue('Acres_Corn_Harvested' in df.columns)

        # expect Total_Acres_Irrigated_All as a column name
        self.assertTrue('Total_Acres_Irrigated_All' in df.columns)

        # expect Ground as a column name
        self.assertTrue('Ground' in df.columns)

        # expect Surface as a column name
        self.assertTrue('Surface' in df.columns)

        # expect Off as a column name
        self.assertTrue('Off' in df.columns)


if __name__ == '__main__':
    unittest.main()
