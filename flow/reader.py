import pkg_resources
import pandas as pd
from .read_config import *


def read_baseline_data():
    """Read in baseline data as DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('baseline', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cesw_energy_flow_targets():
    """Read in energy flow target data for calculating water in energy sector and output as DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_energy_sector_water', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cesw_energy_sector_water_split_fractions():
    """Read in water split data for calculating water sources to and discharges from the energy sector and output as a
    DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_energy_sector_water', 'file2')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cw_water_flow_targets():
    """Read in water flow target data for collecting water flows to non-energy sectors. Provides output as a DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('collect_water', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_ce_energy_flow_targets():
    """Read in energy flow target data for collecting energy flows to non-water sectors. Provides output as a DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('collect_energy', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwwwd_water_flow_targets():
    """Read in water flow to wastewater target data.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_ww_water_demand', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwswd_water_flow_targets():
    """Read in water flows to water-sector data, not including wastewater sector.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_water_sector_water_demand', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwse_water_flow_targets():
    """Read in water_sector water target data and energy intensities.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_water_sector_energy', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwse_water_sector_energy_split_fractions():
    """Read in water sector energy split data to determine energy sources and energy discharge locations.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_water_sector_energy', 'file2')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_update_data():
    """Read in flow value update sets to update flow output and remove double counting.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('update_flow_data', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)



# TODO ###### BELOW TO BE DELETED #######
# TODO ######


def test_EP_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/EP_test_param.csv')

    return pd.read_csv(data)

def test_EP_flows():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_nested.csv')

    return pd.read_csv(data)

def test_collect_water_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_collect_water.csv')

    return pd.read_csv(data)

def test_collect_energy_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_collect_energy.csv')

    return pd.read_csv(data)

def test_ww_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/water_sector_params.csv')

    return pd.read_csv(data)

def test_water_sector_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_water_sector_water_param.csv')

    return pd.read_csv(data)

def test_water_sector_energy():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_water_sector_energy_param.csv')

    return pd.read_csv(data)

def test_water_sector_energy_discharge():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_water_sector_energy_discharge.csv')

    return pd.read_csv(data)


def test_update_data():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_updater.csv')

    return pd.read_csv(data)









def get_fuel_demand_target_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/EC_to_EG_Energy_Target_Parameters.csv')

    return pd.read_csv(data)

def get_water_demand_source_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/WS_to_PWS_and_NonWater_Source_Parameters.csv')

    return pd.read_csv(data)

def get_water_demand_target_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/WS_to_PWS_and_NonWater_Target_Parameters.csv')

    return pd.read_csv(data)

def get_electricity_dict():
    """Read in a dataframe of 2015 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/electricity_generation_dict.csv')

    return pd.read_csv(data)

def load_baseline_data():
    """Read in a dataframe of 2015 USGS Water Use Data.

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/baseline_data.csv')

    return pd.read_csv(data)

def get_electricity_generation_efficiency_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/electricitygeneration_efficiency_parameters.csv')

    return pd.read_csv(data)

def get_sectoral_efficiency_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/sectoral_efficiency_parameters.csv')

    return pd.read_csv(data)

def get_sectoral_water_consumption_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/sector_water_consumption_fractions.csv')

    return pd.read_csv(data)



def get_sectoral_water_discharge_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/sector_water_discharge_fractions.csv')

    return pd.read_csv(data)






# Items below are for US sample data

def get_water_use_2015():
    """Read in a dataframe of 2015 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/usco2015v2.0.csv')

    return pd.read_csv(data, skiprows=1, dtype={'FIPS': str})


def get_water_use_1995():
    """Read in a dataframe of 1995 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/usco1995.csv')

    return pd.read_csv(data,  dtype={'StateCode': str, 'CountyCode': str})


def get_county_identifier_data():
    """Read in a dataframe of FIPS code - Interconnect crosswalk.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/county_interconnect_list.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data, dtype={'FIPS': str,'STATEFIPS': str })


def get_wastewater_flow_data():
    """Read in a dataframe of wastewater treatment facility water flows (MGD) by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Flow.csv')

    # read in wastewater treatment facility water flow data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_type_data():
    """Read in a dataframe of wastewater treatment facility type by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Type.csv')

    # read in wastewater treatment facility type data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_loc_data():
    """Read in a dataframe of wastewater treatment facility location by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Loc.csv')

    # read in wastewater treatment facility location data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_discharge_data():
    """Read in a dataframe of wastewater treatment facility discharge by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Discharge.csv')

    # read in wastewater treatment facility discharge data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_electricity_generation_data():
    """Read in a dataframe of electricity generation by power plant

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow',
                                           'data/EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.csv')

    # read in wastewater treatment facility discharge data
    return pd.read_csv(data, skiprows=5)

def get_power_plant_county_data():
    """Read in a dataframe of power plant locations

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow',
                                           'data/EIA860_Generator_Y2015.csv')

    # read in data
    return pd.read_csv(data, skiprows=1, usecols= ['Plant Code', "State", 'County'])

def get_powerplant_primary_data():
    """Read in a dataframe of power plant primary generation type by power plant ID

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow',
                                           'data/eia_powerplant_primary_2020.csv')

    # read in data
    return pd.read_csv(data, usecols=['Plant_Code', "StateName", 'County', 'PrimSource'])


def get_powerplant_cooling_data():
    """Read in a dataframe water withdrawals and consumption for thermoelectric cooling by power plant ID

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow',
                                           'data/2015_TE_Model_Estimates_USGS.csv')

    # read in data
    return pd.read_csv(data, usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE','GENERATION_TYPE',
                                      'COOLING_TYPE','WATER_SOURCE_CODE','WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])

def get_irrigation_data():
    """Read in a dataframe of irrigation well depth, pressure, and pump fuel type by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/FRIS2013tab8.csv')

    # read in irrigation well depth, pressure, and pump fuel type data
    return pd.read_csv(data, skiprows=3)


def get_tx_inter_basin_transfer_data():
    """Read in a dataframe of Texas inter-basin transfer data by FIPS

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/TX_IBT_2015.csv')

    # read in Texas inter-basin transfer data by FIPS
    return pd.read_csv(data, dtype={'Used_FIPS': str, 'Source_FIPS': str})


def get_west_inter_basin_transfer_data():
    """Read in a dataframe of western inter-basin transfer data by FIPS

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/West_IBT_county.csv')

    # read in Texas inter-basin transfer data by FIPS
    return pd.read_csv(data, dtype={'FIPS': str})


def get_residential_electricity_demand_data():
    """Read in a dataframe of residential electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table6_Res.csv')

    # read in residential electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_commercial_electricity_demand_data():
    """Read in a dataframe of commercial electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table7_Com.csv')

    # read in commercial electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_industrial_electricity_demand_data():
    """Read in a dataframe of industrial electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table8_Ind.csv')

    # read in industrial electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_transportation_electricity_demand_data():
    """Read in a dataframe of transportation electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table9_Trans.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skiprows=2)

def get_state_electricity_demand_data():
    """Read in a dataframe of transportation electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia_861m_states.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skipfooter=2, engine='python',
                       dtype={'RESIDENTIAL': float, 'COMMERCIAL': float,
                              'INDUSTRIAL': float, 'TRANSPORTATION': float})

def get_territory_electricity_demand_data():
    """Read in a dataframe of transportation electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia_861m_terr.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skipfooter=1, engine='python',
                       dtype={'RESIDENTIAL': float, 'COMMERCIAL': float,
                              'INDUSTRIAL': float, 'TRANSPORTATION': float}
                       )

def get_fuel_demand_data():
    """Read in a dataframe of energy production (fuel) data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/use_all_btu.csv')

    # read in energy production (fuel) data
    return pd.read_csv(data)

def get_energy_production_data():
    """Read in a dataframe of energy production (fuel) data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia_SEDS_Prod_dataset.csv')

    # read in energy production (fuel) data
    return pd.read_csv(data, skiprows=1)


def get_corn_irrigation_data():
    """Read in a dataframe of corn irrigation for biomass data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/USDA_FRIS.csv')

    # read in corn irrigation data
    return pd.read_csv(data)


def get_corn_production_data():
    """Read in a dataframe of corn production for biomass data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/USDA_NASS_CornProd_2015.csv')

    # read in corn irrigation data
    return pd.read_csv(data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})


def get_county_oil_gas_production_data():
    """Read in a dataframe of oil and natural gas production by county

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/oilgascounty.csv')

    # read in county level oil and gas production data
    return pd.read_csv(data, dtype={'geoid': str})


def get_state_petroleum_production_data():
    """Read in a dataframe of oil production by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/petroleum_eia.csv')

    # read in state level petroleum production data
    return pd.read_csv(data, skiprows=4)


def get_state_gas_production_data():
    """Read in a dataframe of natural gas production by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/natgas_eia.csv')

    # read in read in state level natural gas production data
    return pd.read_csv(data, skiprows=4)


def get_unconventional_oil_gas_production_data():
    """Read in a dataframe of unconventional oil and natural gas production water use by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/Unconventional_Oil_NG_State.csv')

    # read in read in state level unconventional natural gas and oil production data
    return pd.read_csv(data)


def get_conventional_oil_water_intensity_data():
    """Read in a dataframe of conventional oil water intensity by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/PADD_intensity.csv')

    # read in read in state level water to oil intensity data
    return pd.read_csv(data)


def get_oil_gas_discharge_data():
    """Read in a dataframe of water discharge data from oil and natural gas production

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/Oil_NG_WOR_WGR.csv')

    # read in read in state level water discharge data from oil and natural gas
    return pd.read_csv(data)


def get_coal_production_data():
    """Read in a dataframe of coal production data

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/coalpublic2015.csv')

    # read in read in coal production data
    return pd.read_csv(data, skiprows=3)


def get_coal_mine_location_data():
    """Read in a dataframe of coal mine locations

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/Coal_Mine_Loc.csv')

    # read in read in coal mine data
    return pd.read_csv(data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])


def get_state_fips_data():
    """Read in a dataframe of state FIPS code by state abbreviation

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/State_FIPS_Code.csv')

    # read in read in state fips code to state abbrev. data
    return pd.read_csv(data, dtype={'State_FIPS': str})

def get_ethanol_location_data():
    """Read in a dataframe of state FIPS code by state abbreviation

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia819_ethanolcapacity_2015.csv')

    # read in read in state fips code to state abbrev. data
    return pd.read_csv(data, dtype={'FIPS': str}, skiprows=1)