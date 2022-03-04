import pkg_resources
import pandas as pd


def read_input_data(path: str, leading_zeros=None) -> pd.DataFrame:
    """Read in input csv data as a Pandas DataFrame.
        :param path:                    path to a csv file with flow values
        :type path:                     str

        :param leading_zeros:           Optional parameter to add leading zeros to the region column to ensure the
                                        regional identifier has the correct number of data positions.
        :type leading_zeros:            int

        :return:                        Pandas Dataframe of input flow values and parameters

        """

    # collect file
    df = pd.read_csv(path)

    # read the region column as a string
    region_col = df.columns[0]
    df[region_col] = df[region_col].astype(str)

    # add leading zeros to region if necessary
    if leading_zeros is None:
        df = df
    else:
        df[region_col] = df[region_col].apply(lambda x: x.zfill(leading_zeros))

    # return dataframe
    return df


def read_sample_data() -> pd.DataFrame:
    """Read in input csv data as a Pandas DataFrame.

        """

    # collect file
    data = pkg_resources.resource_filename('flow', 'input_data/test_output.csv')

    # read in file
    df = pd.read_csv(data, dtype={'FIPS': str})

    # read the region column as a string
    region_col = df.columns[0]

    # add leading zeros to region if necessary
    df[region_col] = df[region_col].apply(lambda x: x.zfill(5))

    # return dataframe
    return df


def get_water_use_2015_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/usco2015v2.0.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1, dtype={'FIPS': str})


def get_water_use_rename_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/variable_rename_key.csv')

    # return dataframe
    return pd.read_csv(data)


def get_water_use_1995_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/usco1995.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'StateCode': str, 'CountyCode': str})


def get_water_consumption_rename_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/variable_rename_key_1995water.csv')

    # return dataframe
    return pd.read_csv(data)


def get_tx_ibt_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/HistoricalMunicipal_TX_IBT.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'County Used FIPS': str, 'County Source FIPS': str},
                       skiprows=1, usecols=['Year', 'County Used', 'County Source', 'Total Intake',
                                            'County Used Elevation (ft)', 'County Source Elevation (ft)',
                                            'County Used FIPS',
                                            'County Source FIPS'])


def get_west_ibt_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/West_IBT_county.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS': str})


def get_county_fips_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/county_FIPS_list.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS': str, 'STATEFIPS': str})


def get_power_plant_location_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/EIA860_Generator_Y2015.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1, usecols=['Plant Code', "State", 'County'])


def get_electricity_generation_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data\EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=5)


def get_electricity_water_intensity_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data\cooling_water_intensities.csv')

    # return dataframe
    return pd.read_csv(data)


def get_electricity_cooling_flow_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', r'input_data\2015_TE_Model_Estimates_USGS.csv')

    # return dataframe
    return pd.read_csv(data, usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE', 'GENERATION_TYPE',
                                      'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])


def get_irrigation_pumping_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/FRIS2013tab8.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=3)


def get_pumping_intensity_rename_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/variable_rename_key_pump_intensity.csv')

    # return dataframe
    return pd.read_csv(data)


def get_electricity_demand_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/eia_sales_annual.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1,
                       dtype={'Residential': float, 'Commercial': float,
                              'Industrial': float, 'Transportation': float})


def get_fuel_demand_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/use_all_btu.csv')

    # return dataframe
    return pd.read_csv(data)


def get_fuel_renaming_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/variable_rename_key_fuel_demand.csv')

    # return dataframe
    return pd.read_csv(data)


def get_state_fuel_production_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/eia_SEDS_Prod_dataset.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=1)


def get_county_petroleum_natgas_production_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/oilgascounty.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'geoid': str})


def get_state_water_to_conventional_oil_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/PADD_intensity.csv')

    # return dataframe
    return pd.read_csv(data)


def get_state_water_to_unconventional_production_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/Unconventional_Oil_NG_State.csv')

    # return dataframe
    return pd.read_csv(data)


def get_state_petroleum_natgas_water_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/Oil_NG_WOR_WGR.csv')

    # return dataframe
    return pd.read_csv(data)


def get_petroleum_natgas_rename_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/variable_rename_key_ng_petroleum.csv')

    # return dataframe
    return pd.read_csv(data)


def get_coal_production_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/coalpublic2015.csv')

    # return dataframe
    return pd.read_csv(data, skiprows=3)


def get_coal_mine_location_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/Coal_Mine_Loc.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])


def get_state_fips_crosswalk_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/State_FIPS_Code.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'State_FIPS': str})


def get_ethanol_plant_location_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/eia819_ethanolcapacity_2015.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'FIPS': str}, skiprows=1)


def get_corn_irrigation_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/USDA_FRIS.csv')

    # return dataframe
    return pd.read_csv(data)


def get_corn_production_data():
    """Read in data
        :return:                        dataframe of values
        """

    data = pkg_resources.resource_filename('flow', 'input_data/USDA_NASS_CornProd_2015.csv')

    # return dataframe
    return pd.read_csv(data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})

