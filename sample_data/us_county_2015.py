import numpy as np
import pandas as pd


def prep_water_use_2015(variables=None, all_variables=False) -> pd.DataFrame:
    """prep 2015 water use data by replacing non-numeric values, reducing available variables in output dataframe,
     renaming variables appropriately, and returning a dataframe of specified variables.

    :param variables:                   None if no specific variables required in addition to FIPS code, state name,
                                        and county name. Default is None, otherwise a list of additional
                                        variables to include in returned dataframe.
    :type variables:                    list

    :param all_variables:               Include all available variables in returned dataframe. Default is False.
    :type all_variables:                bool


    :return:                           DataFrame of a water withdrawal and consumption values for 2015
                                        at the county level

    """

    # read in data
    df = pd.read_csv('input_data/usco2015v2.0.csv', skiprows=1, dtype={'FIPS': str})

    # replacing characters for missing USGS data with value of zero
    df.replace("--", 0, inplace=True)

    # creating a dictionary of required variables from full dataset with required naming
    variables_dict = {'FIPS': 'FIPS',
                      'STATE': 'State',
                      'COUNTY': 'County',
                      'TP-TotPop': 'population',

                      # direct use variables
                      'PS-WGWFr': 'WSW_fresh_groundwater_total_total_to_PWS_fresh_groundwater_total_total_mgd',
                      'PS-WSWFr': 'WSW_fresh_surfacewater_total_total_to_PWS_fresh_surfacewater_total_total_mgd',
                      'PS-WGWSa': 'WSW_saline_groundwater_total_total_to_PWS_saline_groundwater_total_total_mgd',
                      'PS-WSWSa': 'WSW_saline_surfacewater_total_total_to_PWS_saline_surfacewater_total_total_mgd',
                      'DO-PSDel': 'PWD_total_total_total_total_to_RES_public_total_total_total_mgd',
                      'DO-WGWFr': 'WSW_fresh_groundwater_total_total_to_RES_fresh_groundwater_total_total_mgd',
                      'DO-WSWFr': 'WSW_fresh_surfacewater_total_total_to_RES_fresh_surfacewater_total_total_mgd',
                      'IN-WGWFr': 'WSW_fresh_groundwater_total_total_to_IND_fresh_groundwater_total_total_mgd',
                      'IN-WSWFr': 'WSW_fresh_surfacewater_total_total_to_IND_fresh_surfacewater_total_total_mgd',
                      'IN-WGWSa': 'WSW_saline_groundwater_total_total_to_IND_saline_groundwater_total_total_mgd',
                      'IN-WSWSa': 'WSW_saline_surfacewater_total_total_to_IND_saline_surfacewater_total_total_mgd',
                      'MI-WGWFr': 'WSW_fresh_groundwater_total_total_to_MIN_fresh_groundwater_total_total_mgd',
                      'MI-WSWFr': 'WSW_fresh_surfacewater_total_total_to_MIN_fresh_surfacewater_total_total_mgd',
                      'MI-WGWSa': 'WSW_saline_groundwater_total_total_to_MIN_saline_groundwater_total_total_mgd',
                      'MI-WSWSa': 'WSW_saline_surfacewater_total_total_to_MIN_saline_surfacewater_total_total_mgd',
                      'IC-WGWFr': 'WSW_fresh_groundwater_total_total_to_ACI_fresh_groundwater_total_total_mgd',
                      'IC-WSWFr': 'WSW_fresh_surfacewater_total_total_to_ACI_fresh_groundwater_total_total_mgd',
                      'IC-RecWW': 'WSI_reclaimed_wastewater_total_total_to_ACI_reclaimed_wastewater_total_total_mgd',
                      'IG-WGWFr': 'WSW_fresh_groundwater_total_total_to_AGI_fresh_groundwater_total_total_mgd',
                      'IG-WSWFr': 'WSW_fresh_surfacewater_total_total_to_AGI_fresh_groundwater_total_total_mgd',
                      'IG-RecWW': 'WSI_reclaimed_wastewater_total_total_to_AGI_reclaimed_wastewater_total_total_mgd',
                      'LI-WGWFr': 'WSW_fresh_groundwater_total_total_to_ALV_fresh_groundwater_total_total_mgd',
                      'LI-WSWFr': 'WSW_fresh_surfacewater_total_total_to_ALV_fresh_surfacewater_total_total_mgd',
                      'AQ-WGWFr': 'WSW_fresh_groundwater_total_total_to_AAQ_fresh_groundwater_total_total_mgd',
                      'AQ-WGWSa': 'WSW_saline_groundwater_total_total_to_AAQ_saline_groundwater_total_total_mgd',
                      'AQ-WSWFr': 'WSW_fresh_surfacewater_total_total_to_AAQ_fresh_surfacewater_total_total_mgd',
                      'AQ-WSWSa': 'WSW_saline_surfacewater_total_total_to_AAQ_saline_surfacewater_total_total_mgd',

                      # secondary use variables
                      'IR-WGWFr': 'fresh_groundwater_total_irrigation_mgd',
                      'IR-WSWFr': 'fresh_surfacewater_total_irrigation_mgd',
                      'IR-RecWW': 'fresh_wastewater_total_irrigation_mgd',
                      'IG-CUsFr': 'golf_irrigation_fresh_consumption_mgd',
                      'IC-CUsFr': 'crop_irrigation_fresh_consumption_mgd',
                      'IR-CUsFr': 'total_irrigation_fresh_consumption',
                      'PS-Wtotl': 'total_pws_withdrawals_mgd',
                      'PT-WGWFr': 'fresh_groundwater_thermoelectric_mgd',
                      'PT-WGWSa': 'saline_groundwater_thermoelectric_mgd',
                      'PT-WSWFr': 'fresh_surfacewater_thermoelectric_mgd',
                      'PT-WSWSa': 'saline_surfacewater_thermoelectric_mgd',
                      'PT-RecWW': 'wastewater_thermoelectric_mgd',
                      'PT-PSDel': 'fresh_pws_thermoelectric_mgd',

                      # created variables
                      'IR-CU_frac': 'total_irrigation_consumption_fraction',
                      'IC-CU_FSW_frac': 'ACI_fresh_groundwater_total_total_to_CMP_total_total_total_total_fraction',
                      'IC-CU_FGW_frac': 'ACI_fresh_surfacewater_total_total_to_CMP_total_total_total_total_fraction',
                      'IC-CU_RWW_frac': 'ACI_reclaimed_wastewater_total_total_to_CMP_total_total_total_total_fraction',
                      'IG-CU_FSW_frac': 'AGI_fresh_groundwater_total_total_to_CMP_total_total_total_total_fraction',
                      'IG-CU_FGW_frac': 'AGI_fresh_surfacewater_total_total_to_CMP_total_total_total_total_fraction',
                      'IG-CU_RWW_frac': 'AGI_reclaimed_wastewater_total_total_to_CMP_total_total_total_total_fraction'
                      }

    # convert all columns that should be numerical to floats
    numerical_list = df.columns[6:]
    for col in numerical_list:
        df[col] = df[col].astype(float)

    # calculate consumption fractions for crop irrigation, golf irrigation, and total irrigation

    df['IR-CU_frac'] = np.where((df['IR-WGWFr'] + df['IR-WSWFr'] + df['IR-RecWW']) > 0,
                                df['IR-CUsFr'] / (df['IR-WGWFr'] + df['IR-WSWFr'] + df['IR-RecWW']),
                                0)

    df['IC-CU_FSW_frac'] = np.where((df['IR-WGWFr'] + df['IR-WSWFr'] + df['IR-RecWW']) > 0,
                                    df['IR-CUsFr'] / (df['IR-WGWFr'] + df['IR-WSWFr'] + df['IR-RecWW']),
                                    0)
    # fresh groundwater and reclaimed wastewater are assumed to have the same consumption fraction as fresh surface
    df['IC-CU_FGW_frac'] = df['IC-CU_FSW_frac']
    df['IC-CU_RWW_frac'] = df['IC-CU_FSW_frac']

    df['IG-CU_FSW_frac'] = np.where((df['IG-WGWFr'] + df['IG-WSWFr'] + df['IG-RecWW']) > 0,
                                    df['IG-CUsFr'] / (df['IG-WGWFr'] + df['IG-WSWFr'] + df['IG-RecWW']),
                                    0)

    # fresh groundwater and reclaimed wastewater are assumed to have the same consumption fraction as fresh surface
    df['IG-CU_FGW_frac'] = df['IG-CU_FSW_frac']
    df['IG-CU_RWW_frac'] = df['IG-CU_FSW_frac']

    # list of states that do not have specific crop and golf irrigation values, just total irrigation
    state_irrigation_adj_list = ['AR', 'HI', 'LA', 'MS', 'MO', 'MT', 'NE', 'NJ', 'ND',
                                 'OK', 'SD', 'TX', 'WI', 'WY', 'PR', 'VI']

    # fills crop irrigation values with total irrigation withdrawal and consumption values for states in list
    for state in state_irrigation_adj_list:
        df['IC-WGWFr'] = np.where(df['STATE'] == state, df['IR-WGWFr'], df['IC-WGWFr'])
        df['IC-WSWFr'] = np.where(df['STATE'] == state, df['IR-WSWFr'], df['IC-WSWFr'])
        df['IC-RecWW'] = np.where(df['STATE'] == state, df['IR-RecWW'], df['IC-RecWW'])
        df['IC-CU_FGW_frac'] = np.where(df['STATE'] == state, df['IR-CU_frac'], df['IC-CU_FGW_frac'])
        df['IC-CU_RWW_frac'] = np.where(df['STATE'] == state, df['IR-CU_frac'], df['IC-CU_FGW_frac'])
        df['IG-CU_FSW_frac'] = np.where(df['STATE'] == state, df['IR-CU_frac'], df['IC-CU_FGW_frac'])

    # reduce dataframe to variables in dictionary
    df = df[variables_dict]

    # rename columns to dictionary keys
    df.rename(columns=variables_dict, inplace=True)

    # add leading zeroes to FIPS Code
    df['FIPS'] = df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))

    # remove states not included in sample analysis
    state_remove_list = ['PR', 'VI']
    for state in state_remove_list:
        df = df[df.State != state]

    # return variables specified
    if variables is None and all_variables is False:
        variables = ['FIPS', "State", "County"]
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]

    return df


def prep_water_use_1995(variables=None, all_variables=False) -> pd.DataFrame:
    """prepping 1995 water use data from USGS by replacing missing values, fixing FIPS codes,
     and reducing to needed variables

    :return:                DataFrame of a number of water values for 1995 at the county level

    """
    # read in data
    data = 'input_data/usco1995.csv'
    df = pd.read_csv(data, dtype={'StateCode': str, 'CountyCode': str})

    # create a complete state + county FIPS code from the sum of the state and county level FIPS code strings
    df["FIPS"] = df["StateCode"] + df["CountyCode"]

    # address FIPS code changes between 1995 and 2015
    df['FIPS'] = np.where(df['FIPS'] == "12025", "12086", df['FIPS'])  # Miami-Dade County, FL
    df['FIPS'] = np.where(df['FIPS'] == "46113", "46102", df['FIPS'])  # Oglala Lakota County, SD
    df['FIPS'] = np.where(df['FIPS'] == "02232", "02105", df['FIPS'])  # Hoonah-Angoon Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "02270", "02158", df['FIPS'])  # Kusilvak Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "02280", "02195", df['FIPS'])  # Petersburg Borough, AK
    df['FIPS'] = np.where(df['FIPS'] == "02201", "02198", df['FIPS'])  # Wales-Hyder Census Area, AK

    # Copy data from counties that split into multiple FIPS codes between 1995 and 2015 into new rows and assigns FIPS
    wrangell_petersburg_index = df.index[df['FIPS'] == "02195"].tolist()  # Wrangell, AK from Wrangell-Petersburg, AK
    df = df.append(df.loc[wrangell_petersburg_index * 1].assign(FIPS="02275"), ignore_index=True)
    skagway_index = df.index[df['FIPS'] == "02105"].tolist()  # Hoonah-Angoon, AK from Skagway-Hoonah-Angoon, AK
    df = df.append(df.loc[skagway_index * 1].assign(FIPS="02230"), ignore_index=True)
    boulder_index = df.index[df['FIPS'] == "08013"].tolist()  # Broomfield County, CO from Boulder County, CO
    df = df.append(df.loc[boulder_index * 1].assign(FIPS="08014"), ignore_index=True)

    # return variables specified
    if variables is None and all_variables is False:
        variables = ['FIPS']
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]
    return df


# READER


def get_water_use_1995():
    data = pkg_resources.resource_filename('flow', 'data/usco1995.csv')

    return pd.read_csv(data,  dtype={'StateCode': str, 'CountyCode': str})


def get_county_identifier_data():
    data = pkg_resources.resource_filename('flow', 'data/county_interconnect_list.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data, dtype={'FIPS': str,'STATEFIPS': str })


def get_wastewater_flow_data():
    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Flow.csv')

    # read in wastewater treatment facility water flow data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_type_data():
    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Type.csv')

    # read in wastewater treatment facility type data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_loc_data():
    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Loc.csv')

    # read in wastewater treatment facility location data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_discharge_data():
    data = pkg_resources.resource_filename('flow', 'data/WW_Discharge.csv')

    # read in wastewater treatment facility discharge data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_electricity_generation_data():
    data = pkg_resources.resource_filename('flow',
                                           'data/EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.csv')

    # read in wastewater treatment facility discharge data
    return pd.read_csv(data, skiprows=5)

def get_power_plant_county_data():
    data = pkg_resources.resource_filename('flow',
                                           'data/EIA860_Generator_Y2015.csv')

    # read in data
    return pd.read_csv(data, skiprows=1, usecols= ['Plant Code', "State", 'County'])

def get_powerplant_primary_data():
    data = pkg_resources.resource_filename('flow',
                                           'data/eia_powerplant_primary_2020.csv')

    # read in data
    return pd.read_csv(data, usecols=['Plant_Code', "StateName", 'County', 'PrimSource'])


def get_powerplant_cooling_data():
    data = pkg_resources.resource_filename('flow',
                                           'data/2015_TE_Model_Estimates_USGS.csv')

    # read in data
    return pd.read_csv(data, usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE','GENERATION_TYPE',
                                      'COOLING_TYPE','WATER_SOURCE_CODE','WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])

def get_irrigation_data():
    data = pkg_resources.resource_filename('flow', 'data/FRIS2013tab8.csv')

    # read in irrigation well depth, pressure, and pump fuel type data
    return pd.read_csv(data, skiprows=3)


def get_tx_inter_basin_transfer_data():
    data = pkg_resources.resource_filename('flow', 'data/TX_IBT_2015.csv')

    # read in Texas inter-basin transfer data by FIPS
    return pd.read_csv(data, dtype={'Used_FIPS': str, 'Source_FIPS': str})


def get_west_inter_basin_transfer_data():
    data = pkg_resources.resource_filename('flow', 'data/West_IBT_county.csv')

    # read in Texas inter-basin transfer data by FIPS
    return pd.read_csv(data, dtype={'FIPS': str})


def get_residential_electricity_demand_data():
    data = pkg_resources.resource_filename('flow', 'data/EIA_table6_Res.csv')

    # read in residential electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_commercial_electricity_demand_data():
    data = pkg_resources.resource_filename('flow', 'data/EIA_table7_Com.csv')

    # read in commercial electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_industrial_electricity_demand_data():
    data = pkg_resources.resource_filename('flow', 'data/EIA_table8_Ind.csv')

    # read in industrial electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_transportation_electricity_demand_data():
    data = pkg_resources.resource_filename('flow', 'data/EIA_table9_Trans.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skiprows=2)

def get_state_electricity_demand_data():
    data = pkg_resources.resource_filename('flow', 'data/eia_861m_states.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skipfooter=2, engine='python',
                       dtype={'RESIDENTIAL': float, 'COMMERCIAL': float,
                              'INDUSTRIAL': float, 'TRANSPORTATION': float})


def get_fuel_demand_data():

    data = pkg_resources.resource_filename('flow', 'data/use_all_btu.csv')

    # read in energy production (fuel) data
    return pd.read_csv(data)

def get_energy_production_data():
    data = pkg_resources.resource_filename('flow', 'data/eia_SEDS_Prod_dataset.csv')

    # read in energy production (fuel) data
    return pd.read_csv(data, skiprows=1)


def get_corn_irrigation_data():

    data = pkg_resources.resource_filename('flow', 'data/USDA_FRIS.csv')

    # read in corn irrigation data
    return pd.read_csv(data)


def get_corn_production_data():

    data = pkg_resources.resource_filename('flow', 'data/USDA_NASS_CornProd_2015.csv')

    # read in corn irrigation data
    return pd.read_csv(data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})


def get_county_oil_gas_production_data():

    data = pkg_resources.resource_filename('flow', 'data/oilgascounty.csv')

    # read in county level oil and gas production data
    return pd.read_csv(data, dtype={'geoid': str})


def get_state_petroleum_production_data():

    data = pkg_resources.resource_filename('flow', 'data/petroleum_eia.csv')

    # read in state level petroleum production data
    return pd.read_csv(data, skiprows=4)


def get_state_gas_production_data():

    data = pkg_resources.resource_filename('flow', 'data/natgas_eia.csv')

    # read in read in state level natural gas production data
    return pd.read_csv(data, skiprows=4)


def get_unconventional_oil_gas_production_data():

    data = pkg_resources.resource_filename('flow', 'data/Unconventional_Oil_NG_State.csv')

    # read in read in state level unconventional natural gas and oil production data
    return pd.read_csv(data)


def get_conventional_oil_water_intensity_data():

    data = pkg_resources.resource_filename('flow', 'data/PADD_intensity.csv')

    # read in read in state level water to oil intensity data
    return pd.read_csv(data)


def get_oil_gas_discharge_data():


    data = pkg_resources.resource_filename('flow', 'data/Oil_NG_WOR_WGR.csv')

    # read in read in state level water discharge data from oil and natural gas
    return pd.read_csv(data)


def get_coal_production_data():


    data = pkg_resources.resource_filename('flow', 'data/coalpublic2015.csv')

    # read in read in coal production data
    return pd.read_csv(data, skiprows=3)


def get_coal_mine_location_data():

    data = pkg_resources.resource_filename('flow', 'data/Coal_Mine_Loc.csv')

    # read in read in coal mine data
    return pd.read_csv(data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])


def get_state_fips_data():
    data = pkg_resources.resource_filename('flow', 'data/State_FIPS_Code.csv')

    # read in read in state fips code to state abbrev. data
    return pd.read_csv(data, dtype={'State_FIPS': str})

def get_ethanol_location_data():
    data = pkg_resources.resource_filename('flow', 'data/eia819_ethanolcapacity_2015.csv')

    # read in read in state fips code to state abbrev. data
    return pd.read_csv(data, dtype={'FIPS': str}, skiprows=1)





x = prep_water_use_2015(all_variables=True)
x.to_csv('test_output.csv')
