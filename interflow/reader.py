import pkg_resources
import pandas as pd
import json


def read_sample_data() -> pd.DataFrame:
    """Read in complete sample input csv data as a Pandas DataFrame.

    :return:                        DataFrame of complete sample data values for US Counties
    """

    # collect file
    data = pkg_resources.resource_filename('interflow', 'input_data/us_county_sample_data.zip')

    # read in file
    df = pd.read_csv(data)

    # identify first column
    region_col = df.columns[0]

    # convert to string
    df[region_col] = df[region_col].astype(str)

    # add leading zeros to region
    df[region_col] = df[region_col].apply(lambda x: x.zfill(5))

    # return dataframe
    return df


def get_water_use_2015_data():
    """Read in 2015 USGS water use data

    :return:                        dataframe of 2015 water use values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/usco2015v2.0.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1, dtype={'FIPS': str})


def get_water_use_rename_data():
    """Read in variable renaming key for USGS 2015 water use data

    :return:                        dataframe of variable names to map to original names
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/variable_rename_key.csv')

    # return dataframe
    return pd.read_csv(data)


def get_water_use_1995_data():
    """Read in 1995 USGS water use data

    :return:                        dataframe of water use values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/usco1995.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'StateCode': str, 'CountyCode': str})


def get_water_consumption_rename_data():
    """Read in 1995 water use rename key data.

    :return:                        dataframe of variable names to map to original names
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/variable_rename_key_1995water.csv')

    # return dataframe
    return pd.read_csv(data)


def get_tx_ibt_data():
    """Read in data on Texas interbasin water transfers for 2015.

    :return:                        dataframe of interbasin transfer values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/HistoricalMunicipal_TX_IBT.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'County Used FIPS': str, 'County Source FIPS': str},
                       skiprows=1, usecols=['Year', 'County Used', 'County Source', 'Total Intake',
                                            'County Used Elevation (ft)', 'County Source Elevation (ft)',
                                            'County Used FIPS',
                                            'County Source FIPS'])


def get_west_ibt_data():
    """Read in data on western interbasin water transfers.

    :return:                        dataframe of interbasin transfer values for western states
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/West_IBT_county.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS': str})


def get_county_fips_data():
    """Read in data to map the 2015 county alphanumeric names to county FIPS codes.

    :return:                        dataframe of county names and FIPS codes
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/county_FIPS_list.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS': str, 'STATEFIPS': str})


def get_wastewater_flow_data():
    """Read in data of wastewater facility water flow data.

    :return:                        dataframe of wastewater flow values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/WW_Facility_Flow.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_type_data():
    """Read in data of wastewater facility treatment type data.

    :return:                        dataframe of wastewater treatment values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/WW_Facility_Type.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_location_data():
    """Read in data of wastewater facility location data.

    :return:                        dataframe of wastewater location values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/WW_Facility_Loc.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_discharge_data():
    """Read in data of wastewater facility discharge data.

    :return:                        dataframe of wastewater discharge values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/WW_Discharge.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_power_plant_location_data():
    """Read in data that includes information on the location (county, state) of individual power plants (by plant code)
     in the US for 2015

     :return:                        dataframe of power plants and their locations
     """

    data = pkg_resources.resource_filename('interflow', 'input_data/EIA860_Generator_Y2015.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1, usecols=['Plant Code', "State", 'County'])


def get_electricity_generation_data():
    """Read in electricity generation and fuel use by individual power plants in the US for 2015.

    :return:                        dataframe of electricity generation and fuel use values
    """

    data = pkg_resources.resource_filename('interflow', "input_data/EIA923_generation.csv")

    # return dataframe
    return pd.read_csv(data, skiprows=5)


def get_electricity_water_intensity_data():
    """Read in water intensity data for various types of power plant technologies.

    :return:                        dataframe of water intensity values
    """

    data = pkg_resources.resource_filename('interflow', "input_data/cooling_water_intensities.csv")

    # return dataframe
    return pd.read_csv(data)


def get_electricity_cooling_flow_data():
    """Read in USGS 2015 data on thermoelectric cooling withdrawals and water consumption for individual power plants.

    :return:                        dataframe of thermoelectric cooling values
    """

    data = pkg_resources.resource_filename('interflow', "input_data/2015_TE_Model_Estimates_USGS.csv")

    # return dataframe
    return pd.read_csv(data, usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE', 'GENERATION_TYPE',
                                      'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])


def get_irrigation_pumping_data():
    """Read in data from USDA Farm and Ranch Irrigation Survey 2013 with information on average_well_depth_ft,
    average operating pressure (psi),average pumping capacity (gpm), and the amount of irrigation pumping using
    electricity, natural gas, propane, and diesel at the state-level.

    :return:                        dataframe of irrigation pumping values
    """

    data = pkg_resources.resource_filename('interflow', 'input_data/FRIS2013tab8.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=3)


def get_pumping_intensity_rename_data():
    """Read in data to rename pumping intensity variables.

    :return:                        dataframe of rename values to map to old names

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/variable_rename_key_pump_intensity.csv')

    # return dataframe
    return pd.read_csv(data)


def get_electricity_demand_data():
    """Read in data from US EIA for 2015 on the total electricity demand in each state by the residential, commercial,
    industrial, and transportation sector.

    :return:                        dataframe of electricity demand values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/eia_sales_annual.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1,
                       dtype={'Residential': float, 'Commercial': float,
                              'Industrial': float, 'Transportation': float})


def get_fuel_demand_data():
    """Read in data from US EIA for 2015 on the total fuel demand in each state by the residential, commercial,
    industrial, and transportation sector.

    :return:                        dataframe of fuel demand values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/use_all_btu.csv')

    # return dataframe
    return pd.read_csv(data)


def get_fuel_renaming_data():
    """Read in data to rename fuel demand variables.

    :return:                        dataframe of new variable names to map to old variable names

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/variable_rename_key_fuel_demand.csv')

    # return dataframe
    return pd.read_csv(data)


def get_state_fuel_production_data():
    """Read in data from US EIA for 2015 with state-level fuel production data including biomass, natural gas, and
    petroleum.

    :return:                        dataframe of fuel production values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/eia_SEDS_Prod_dataset.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1)


def get_county_petroleum_natgas_production_data():
    """Read in data on county level petroleum and natural gas production data.

    :return:                        dataframe of natural gas and petroleum production values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/oilgascounty.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'geoid': str})


def get_state_water_to_conventional_oil_data():
    """Read in data on the water to oil ratio by PADD region for conventional oil production.

    :return:                        dataframe of water intensity values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/PADD_intensity.csv')

    # return dataframe
    return pd.read_csv(data)


def get_state_water_to_unconventional_production_data():
    """Read in state-level data on water use in the production of unconventional natural gas and petroleum.

    :return:                        dataframe of water use values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/Unconventional_Oil_NG_State.csv')

    # return dataframe
    return pd.read_csv(data)


def get_state_petroleum_natgas_water_data():
    """Read in state-level data on the water to oil and water to natural gas ratios as well as the percent of water
    from each that is injected, consumed, or discharged to the surface.

    :return:                        dataframe of natural gas and petroleum values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/Oil_NG_WOR_WGR.csv')

    # return dataframe
    return pd.read_csv(data)


def get_petroleum_natgas_rename_data():
    """Read in data to rename original petroleum and natural gas values to their long-form descriptive name.

    :return:                        dataframe of new variable names to map to old variable names

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/variable_rename_key_ng_petroleum.csv')

    # return dataframe
    return pd.read_csv(data)


def get_coal_production_data():
    """Read in 2015 data from US EIA on coal production and mine type at the coal-mine level.

    :return:                        dataframe of coal mine production values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/coalpublic2015.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=3)


def get_coal_mine_location_data():
    """Read in data with information on the county location of individual coal mines.

    :return:                        dataframe of coal mine location values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/Coal_Mine_Loc.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])


def get_state_fips_crosswalk_data():
    """Read in data with state names, state abbreviations, and state-level FIPS codes.

    :return:                        dataframe of state identification values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/State_FIPS_Code.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'State_FIPS': str})


def get_ethanol_plant_location_data():
    """Read in data on ethanol plant locations for 2015.

    :return:                        dataframe of ethanol plant location values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/eia819_ethanolcapacity_2015.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS': str}, skiprows=1)


def get_corn_irrigation_data():
    """Read in data from USDA Farm and Ranch Irrigation Survey on total irrigation to all crops and corn production.

    :return:                        dataframe of irrigation values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/USDA_FRIS.csv')

    # return dataframe
    return pd.read_csv(data)


def get_corn_production_data():
    """Read in data from USDA on the total corn production for 2015 at the county level.

    :return:                        dataframe of county-level corn production values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/USDA_NASS_CornProd_2015.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})


def load_sample_geojson_data():
    """Read in GeoJSON file with county-level information for mapping all US counties.

    :return:                        dataframe of county-level corn production values

    """

    data = pkg_resources.resource_filename('interflow', 'input_data/geojson-counties-fips.json')

    f = open(data)

    # return dataframe
    return json.load(f)


def load_sample_data_output() -> pd.DataFrame:
    """Read in a copy of the run output for all US counties.

    :return:                        dataframe of county output values

    """

    # collect file
    data = pkg_resources.resource_filename('interflow', 'input_data/us_county_sample_output.csv')

    # read in file
    df = pd.read_csv(data)

    # identify first column
    region_col = df.columns[0]

    # convert to string
    df[region_col] = df[region_col].astype(str)

    # add leading zeros to region
    df[region_col] = df[region_col].apply(lambda x: x.zfill(5))

    # return dataframe
    return df

