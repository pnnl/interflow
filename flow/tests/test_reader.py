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

    def test_get_county_identifier_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_county_identifier_data()

        # expect FIPS as a column name
        self.assertTrue('FIPS' in df.columns)

        # expect Interconnect as a column name
        self.assertTrue('Interconnect' in df.columns)

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

    def test_get_irrigation_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_irrigation_data()

        # expect STATE as a column name
        self.assertTrue('State' in df.columns)

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

    def test_get_corn_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_corn_production_data()

        # expect State ANSI as a column name
        self.assertTrue('State ANSI' in df.columns)

        # expect County ANSI as a column name
        self.assertTrue('County ANSI' in df.columns)

        # expect Value as a column name
        self.assertTrue('Value' in df.columns)

    def test_get_county_oil_gas_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_county_oil_gas_production_data()

        # expect geoid as a column name
        self.assertTrue('geoid' in df.columns)

        # expect gas2011 as a column name
        self.assertTrue('gas2011' in df.columns)

        # expect oil2011 as a column name
        self.assertTrue('oil2011' in df.columns)

    def test_get_state_petroleum_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_state_petroleum_production_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect 2010_Pet as a column name
        self.assertTrue('2010_Pet' in df.columns)

        # expect 2015_Pet as a column name
        self.assertTrue('2015_Pet' in df.columns)

    def test_get_state_gas_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_state_gas_production_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect 2010_Pet as a column name
        self.assertTrue('2010_NG' in df.columns)

        # expect 2015_Pet as a column name
        self.assertTrue('2015_NG' in df.columns)

    def test_get_unconventional_oil_gas_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_unconventional_oil_gas_production_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect FSW_Unconventional_Oil (MGD) as a column name
        self.assertTrue('FSW_Unconventional_Oil (MGD)' in df.columns)

        # expect FGW_Unconventional_Oil (MGD)	 as a column name
        self.assertTrue('FGW_Unconventional_Oil (MGD)' in df.columns)

        # expect FSW_Unconventional_NG (MGD) as a column name
        self.assertTrue('FSW_Unconventional_NG (MGD)' in df.columns)

        # expect FGW_Unconventional_NG (MGD) as a column name
        self.assertTrue('FGW_Unconventional_NG (MGD)' in df.columns)

    def test_get_conventional_oil_water_intensity_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_conventional_oil_water_intensity_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect GalWater_GalOil as a column name
        self.assertTrue('GalWater_GalOil' in df.columns)

    def test_get_oil_gas_discharge_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_oil_gas_discharge_data()

        # expect State as a column name
        self.assertTrue('State' in df.columns)

        # expect WOR (bbl/bbl)	 as a column name
        self.assertTrue('WOR (bbl/bbl)' in df.columns)

        # expect WGR (bbl/Mmcf)	 as a column name
        self.assertTrue('WGR (bbl/Mmcf)' in df.columns)

        # expect Total injected (%)	 as a column name
        self.assertTrue('Total injected (%)' in df.columns)

        # expect Surface Discharge (%)	as a column name
        self.assertTrue('Surface Discharge (%)' in df.columns)

        # expect Evaporation/ Consumption (%) as a column name
        self.assertTrue('Evaporation/ Consumption (%)' in df.columns)

    def test_get_coal_production_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_coal_production_data()

        # expect MSHA ID as a column name
        self.assertTrue('MSHA ID' in df.columns)

        # expect Mine State as a column name
        self.assertTrue('Mine State' in df.columns)

        # expect Mine County as a column name
        self.assertTrue('Mine County' in df.columns)

        # expect Mine Type as a column name
        self.assertTrue('Mine Type' in df.columns)

        # expect Production (short tons) as a column name
        self.assertTrue('Production (short tons)' in df.columns)

    def test_get_coal_mine_location_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_coal_mine_location_data()

        # expect MINE_ID as a column name
        self.assertTrue('MINE_ID' in df.columns)

        # expect STATE as a column name
        self.assertTrue('STATE' in df.columns)

        # expect FIPS_CNTY_CD as a column name
        self.assertTrue('FIPS_CNTY_CD' in df.columns)

    def test_get_state_fips_data(self):
        """Ensure we get what is expected from the input file."""

        # load the data
        df = get_state_fips_data()

        # expect STATE as a column name
        self.assertTrue('State' in df.columns)

        # expect STATEFIPS as a column name
        self.assertTrue('STATEFIPS' in df.columns)


if __name__ == '__main__':
    unittest.main()
