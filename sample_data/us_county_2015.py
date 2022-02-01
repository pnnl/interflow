import numpy as np
import pandas as pd


def convert_kwh_bbtu(x: float) -> float:
    """converts kWh to billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.000003412140

    return bbtu


def convert_mwh_bbtu(x: float) -> float:
    """converts MWh to billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.003412

    return bbtu


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
                      'PS-WGWFr': 'PWS_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'PS-WSWFr': 'PWS_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'PS-WGWSa': 'PWS_saline_groundwater_withdrawal_total_mgd_from_WSW_saline_groundwater_total_total_mgd',
                      'PS-WSWSa': 'PWS_saline_surfacewater_withdrawal_total_mgd_from_WSW_saline_surfacewater_total_total_mgd',
                      'DO-PSDel': 'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd',
                      'DO-WGWFr': 'RES_fresh_groundwater_total_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'DO-WSWFr': 'RES_fresh_surfacewater_total_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'IN-WGWFr': 'IND_fresh_groundwater_total_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'IN-WSWFr': 'IND_fresh_surfacewater_total_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'IN-WGWSa': 'IND_saline_groundwater_total_total_mgd_from_WSW_saline_groundwater_total_total_mgd',
                      'IN-WSWSa': 'IND_saline_surfacewater_total_total_mgd_from_WSW_saline_surfacewater_total_total_mgd',
                      'MI-WGWFr': 'MIN_fresh_groundwater_total_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'MI-WSWFr': 'MIN_fresh_surfacewater_total_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'MI-WGWSa': 'MIN_saline_groundwater_total_total_mgd_from_WSW_saline_groundwater_total_total_mgd',
                      'MI-WSWSa': 'MIN_saline_surfacewater_total_total_mgd_from_WSW_saline_surfacewater_total_total_mgd',
                      'IC-WGWFr': 'ACI_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'IC-WSWFr': 'ACI_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'IC-RecWW': 'ACI_reclaimed_wastewater_import_total_mgd_from_WSI_reclaimed_wastewater_total_total_mgd',
                      'IG-WGWFr': 'AGI_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'IG-WSWFr': 'AGI_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'IG-RecWW': 'AGI_reclaimed_wastewater_import_total_mgd_from_WSI_reclaimed_wastewater_total_total_mgd',
                      'LI-WGWFr': 'ALV_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'LI-WSWFr': 'ALV_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'AQ-WGWFr': 'AAQ_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                      'AQ-WGWSa': 'AAQ_saline_groundwater_withdrawal_total_mgd_from_WSW_saline_groundwater_total_total_mgd',
                      'AQ-WSWFr': 'AAQ_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                      'AQ-WSWSa': 'AAQ_saline_surfacewater_withdrawal_total_mgd_from_WSW_saline_surfacewater_total_total_mgd',

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
                      'IC-CU_FSW_frac': 'ACI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                      'IC-CU_FGW_frac': 'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                      'IC-CU_RWW_frac': 'ACI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                      'IG-CU_FSW_frac': 'AGI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                      'IG-CU_FGW_frac': 'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                      'IG-CU_RWW_frac': 'AGI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
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

    state_remove_list = ['PR', 'VI']
    for state in state_remove_list:
        df = df[df.State != state]

    # return variables specified
    if variables is None and all_variables is False:
        variables = ['FIPS']
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]
    return df


def prep_consumption_fraction() -> pd.DataFrame:
    """prepping water consumption fractions by sector to apply to 2015 water values.

    :return:                DataFrame of consumption fractions for residential, commercial, industrial, mining,
                            livestock, and aquaculture sectors.

    """

    # read in data
    df = prep_water_use_1995(variables=['FIPS', 'State', 'DO-CUTot', 'DO-WDelv', 'CO-CUTot', 'CO-WDelv', 'IN-CUsFr',
                                        'IN-WFrTo', 'IN-PSDel', 'IN-CUsSa', "IN-WSaTo", "MI-CUsFr",
                                        "MI-WFrTo", "MI-CUsSa", "MI-WSaTo", "LV-CUsFr", "LV-WFrTo",
                                        "LA-CUsFr", "LA-WFrTo", "LA-CUsSa", "LA-WSaTo"])

    df_loc = prep_water_use_2015()  # prepared dataframe of 2015 FIPS codes, county names, and state names

    # calculate water consumption fractions as consumptive use divided by delivered water
    df["DO_sCF_Fr"] = df["DO-CUTot"] / df["DO-WDelv"]  # residential (domestic) sector freshwater consumption fraction
    df["CO_sCF_Fr"] = df["CO-CUTot"] / df["CO-WDelv"]  # commercial sector freshwater consumption fraction
    df["IN_sCF_Fr"] = df["IN-CUsFr"] / (df["IN-WFrTo"] + df["IN-PSDel"])  # ind sector freshwater consumption fraction
    df["IN_sCF_Sa"] = df["IN-CUsSa"] / df["IN-WSaTo"]  # industrial sector saline water consumption fraction
    df["MI_sCF_Fr"] = df["MI-CUsFr"] / df["MI-WFrTo"]  # mining sector freshwater consumption fraction
    df["MI_sCF_Sa"] = df["MI-CUsSa"] / df["MI-WSaTo"]  # mining sector saline water consumption fraction
    df["LV_sCF_Fr"] = df["LV-CUsFr"] / df["LV-WFrTo"]  # livestock fresh water consumption fraction
    df["LA_sCF_Fr"] = df["LA-CUsFr"] / df["LA-WFrTo"]  # aquaculture fresh water consumption fraction
    df['LA_sCF_Sa'] = df["LA-CUsSa"] / df["LA-WSaTo"]  # aquaculture saline water consumption fraction

    consumptive_use_list = ["DO-CUTot", "CO-CUTot", "IN-CUsFr", "IN-CUsSa",
                            "MI-CUsFr", "MI-CUsSa", "LV-CUsFr", "LA-CUsFr", "LA-CUsSa"]

    # Replacing infinite (from divide by zero) with with 0
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    # creating a dictionary of required variables from full dataset with descriptive naming
    variables_list = {
        # Retained and renamed 1995 variables
        "FIPS": 'FIPS',
        "State": 'State',
        "DO_sCF_Fr": "RES_fresh_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "CO_sCF_Fr": "COM_public_total_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "IN_sCF_Fr": "IND_fresh_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "IN_sCF_Sa": "IND_saline_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "MI_sCF_Fr": "MIN_fresh_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "MI_sCF_Sa": "MIN_saline_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "LV_sCF_Fr": "ALV_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "LA_sCF_Fr": "AAQ_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "LA_sCF_Sa": "AAQ_saline_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction",

        # created groundwater variables
        "DO_gCF_Fr": "RES_fresh_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "DO_pCF_Fr": "RES_public_total_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "IN_gCF_Fr": "IND_fresh_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "IN_gCF_Sa": "IND_saline_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "IN_pCF_Fr": "IND_public_total_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "MI_gCF_Fr": "MIN_fresh_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "MI_gCF_Sa": "MIN_saline_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "LV_gCF_Fr": "ALV_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "LA_gCF_Fr": "AAQ_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction",
        "LA_gCF_Sa": "AAQ_saline_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"
    }

    # Create groundwater consumption fractions for each sector from surface water consumption fractions
    df["DO_gCF_Fr"] = df["DO_sCF_Fr"]
    df["DO_pCF_Fr"] = df["DO_sCF_Fr"]
    df["IN_gCF_Fr"] = df["IN_sCF_Fr"]
    df["IN_pCF_Fr"] = df["IN_sCF_Fr"]
    df["IN_gCF_Sa"] = df["IN_sCF_Sa"]
    df["MI_gCF_Fr"] = df["MI_sCF_Fr"]
    df["MI_gCF_Sa"] = df["MI_sCF_Sa"]
    df["LV_gCF_Fr"] = df["LV_sCF_Fr"]
    df["LA_gCF_Fr"] = df["LA_sCF_Fr"]
    df["LA_gCF_Sa"] = df["LA_sCF_Sa"]

    # reduce full dataframe to required variable list
    df = df[variables_list]

    # calculate the mean consumption fraction in each state
    df_mean = df.groupby('State', as_index=False).mean()
    rename_list = df_mean.columns[1:].to_list()
    for col in rename_list:
        new_name = f"{col}_state"
        df_mean = df_mean.rename(columns={col: new_name})
    df_mean_all = pd.merge(df, df_mean, how='left', on=['State'])

    # replace counties with consumption fractions of zero with the state average to replace missing data
    rep_list = df.columns[2:].to_list()
    for col in rep_list:
        mean_name = f"{col}_state"
        df[col] = np.where(df[col] == 0, df_mean_all[mean_name], df[col])

    # rename columns to add descriptive language
    df.rename(columns=variables_list, inplace=True)

    # add leading zeroes to FIPS Code
    df['FIPS'] = df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))

    # merge with full list of counties from 2015 USGS water data
    # df = pd.merge(df_loc, df, how='left', on=['FIPS', 'State'])

    return df


def prep_public_water_supply_fraction() -> pd.DataFrame:
    """calculating public water supply deliveries for the commercial and industrial sectors individually
     as a percent of the sum of public water supply deliveries to residential end users and thermoelectric cooling.
     Used in calculation of public water supply demand to all sectors.

    :return:                DataFrame of public water supply ratios for commercial and industrial sector.

    """

    # read in data
    df = prep_water_use_1995(variables=['FIPS', 'State', 'PS-DelDO', 'PS-DelPT', 'PS-DelCO', 'PS-DelIN'])
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # calculate ratio of commercial pws to sum of domestic and thermoelectric cooling pws
    df['com_pws_fraction'] = np.where((df['PS-DelDO'] + df['PS-DelPT'] <= 0),
                                      0,
                                      (df['PS-DelCO'] / (df['PS-DelDO'] + df['PS-DelPT'])))

    # calculate ratio of industrial pws to sum of domestic and thermoelectric cooling pws
    df["ind_pws_fraction"] = np.where(((df['PS-DelDO'] + df['PS-DelPT']) <= 0),
                                      0,
                                      df['PS-DelIN'] / (df['PS-DelDO'] + df['PS-DelPT']))

    df = df[['FIPS', 'State', 'com_pws_fraction', 'ind_pws_fraction']]

    # fill counties with 0 commercial or industrial public water supply ratios with state averages
    df_mean = df.groupby('State', as_index=False).mean()
    rename_list = df_mean.columns[1:].to_list()
    for col in rename_list:
        new_name = f"{col}_state"
        df_mean = df_mean.rename(columns={col: new_name})
    df_mean_all = pd.merge(df, df_mean, how='left', on=['State'])

    # replace counties with consumption fractions of zero with the state average to replace missing data
    rep_list = df.columns[2:].to_list()
    for col in rep_list:
        mean_name = f"{col}_state"
        df[col] = np.where(df[col] == 0, df_mean_all[mean_name], df[col])

    # reduce dataframe to required output
    df = df[['FIPS', 'State', 'com_pws_fraction', 'ind_pws_fraction']]

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on=['FIPS', 'State'])
    df.fillna(0, inplace=True)

    return df

def prep_pws_to_pwd():
    '''preparing variables for connection'''

    df = prep_water_use_2015()

    df['PWD_total_total_total_total_mgd_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_fresh_surfacewater_withdrawal_total_mgd_fraction'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_fresh_groundwater_withdrawal_total_mgd_fraction'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_saline_groundwater_withdrawal_total_mgd_fraction'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity'] = 1
    df['PWD_total_total_total_total_mgd_from_PWS_saline_surfacewater_withdrawal_total_mgd_fraction'] = 1

    return df


def calc_pws_deliveries() -> pd.DataFrame:
    """calculating public water deliveries to the commercial and industrial sectors.

    :return:                DataFrame of public water supply demand by sector, pws imports, and pws exports

    """

    # read in cleaned water use data variables for 2015
    df = prep_water_use_2015(
        variables=["FIPS", 'State', 'County', 'total_pws_withdrawals_mgd',
                   'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd',
                   'fresh_pws_thermoelectric_mgd'])

    # read in dataframe of commercial and industrial pws ratios
    df_pws = prep_public_water_supply_fraction()

    # merge dataframes
    df = pd.merge(df, df_pws, how="left", on=["FIPS", "State", "County"])

    # calculate public water supply deliveries to commercial and industrial sectors
    res_pwd_name = 'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'
    df['total_delivery'] = df[res_pwd_name] + df['fresh_pws_thermoelectric_mgd']

    # create variables names as flows
    com_pwd_name = 'COM_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'
    ind_pwd_name = 'COM_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'

    # calculate public water deliveries to the commercial and industrial sector
    df[com_pwd_name] = df["com_pws_fraction"] * df['total_delivery']
    df[ind_pwd_name] = df["ind_pws_fraction"] * df['total_delivery']

    # reduce dataframe to required variables
    df = df[["FIPS", 'State', 'County', com_pwd_name, ind_pwd_name]]

    return df


def calc_conveyance_loss_fraction(loss_cap=True, loss_cap_amt=.90) -> pd.DataFrame:
    """
    This function calculates the fraction of water lost during conveyance for irrigation (Crop and golf).
     The fraction is calculated as water lost in conveyance of irrigation water divided by total water
    withdrawn for irrigation.

    :param loss_cap:                       If True, a cap is placed on the conveyance loss fraction
    :type loss_cap:                        bool

    :param loss_cap_amt:                   The amount at which irrigation losses are capped and values beyond are
                                            replaced by the specified cap amount. The default value is .90.
    :type loss_cap_amt:                    float

    :return:                               DataFrame of conveyance loss fractions by row

    """
    # read in data
    df = prep_water_use_1995(variables=['FIPS', 'State', 'IR-WTotl', 'IR-CLoss'])  # read in 1995 water values
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # create extended variable names
    crop_irr_sw_name = 'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    crop_irr_gw_name = 'ACI_fresh_groundwater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    crop_irr_rw_name = 'ACI_reclaimed_wastewater_import_total_mgd_to_CVL_total_total_total_total_mgd_fraction'

    golf_irr_sw_name = 'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    golf_irr_gw_name = 'AGI_fresh_groundwater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    golf_irr_rw_name = 'AGI_reclaimed_wastewater_import_total_mgd_to_CVL_total_total_total_total_mgd_fraction'

    # calculate conveyance loss fraction of total water withdrawn for irrigation if irrigation water > 0
    df["loss_fraction"] = np.where(df['IR-WTotl'] > 0, df['IR-CLoss'] / df['IR-WTotl'], 0)

    if loss_cap:
        df["loss_fraction"] = np.where(df['loss_fraction'] > loss_cap_amt, loss_cap_amt, df["loss_fraction"])
        df["loss_fraction"] = np.where(df['loss_fraction'] > loss_cap_amt, loss_cap_amt, df["loss_fraction"])

    else:
        df["loss_fraction"] = df["loss_fraction"]

    # fill counties with 0 conveyance loss with state averages
    df_mean = df.groupby('State', as_index=False).mean()
    rename_list = df_mean.columns[1:].to_list()
    for col in rename_list:
        new_name = f"{col}_state"
        df_mean = df_mean.rename(columns={col: new_name})
    df_mean_all = pd.merge(df, df_mean, how='left', on=['State'])

    df_mean_us_all = df_mean_all[df_mean_all.loss_fraction > 0]
    us_average = df_mean_us_all['loss_fraction'].mean()

    # replace counties with consumption fractions of zero with the state average to replace missing data
    rep_list = df.columns[2:].to_list()
    for col in rep_list:
        mean_name = f"{col}_state"
        df[col] = np.where(df[col] == 0, df_mean_all[mean_name], df[col])
        df[col] = np.where(df[col] == 0, us_average, df[col])

    # assign conveyance loss value to crop and golf irrigation loss names
    df[crop_irr_sw_name] = df["loss_fraction"]
    df[crop_irr_gw_name] = df["loss_fraction"]
    df[golf_irr_sw_name] = df["loss_fraction"]
    df[golf_irr_gw_name] = df["loss_fraction"]
    df[crop_irr_rw_name] = df["loss_fraction"]
    df[golf_irr_rw_name] = df["loss_fraction"]
    # reduce dataframe
    df = df[["FIPS", crop_irr_sw_name, crop_irr_gw_name, golf_irr_sw_name, golf_irr_gw_name,
             crop_irr_rw_name, golf_irr_rw_name]]

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on='FIPS')

    return df


def recalc_irrigation_consumption():
    cons_df = prep_water_use_2015(
        variables=['FIPS', 'State',
                   'ACI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                   'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                   'ACI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                   'AGI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                   'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                   'AGI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'])

    loss_df = calc_conveyance_loss_fraction()

    df = pd.merge(cons_df, loss_df, how='left', on=['FIPS', 'State'])

    aci_gw_loss = 'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    aci_sw_loss = 'ACI_fresh_groundwater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    aci_rw_loss = 'AGI_reclaimed_wastewater_import_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    agi_rw_loss = 'AGI_reclaimed_wastewater_import_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    agi_gw_loss = 'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'
    agi_sw_loss = 'AGI_fresh_groundwater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction'

    aci_gw_con = 'ACI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    aci_sw_con = 'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    aci_rw_con = 'ACI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    agi_gw_con = 'AGI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    agi_sw_con = 'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    agi_rw_con = 'AGI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'

    df[aci_gw_con] = (1 - df[aci_gw_loss]) * df[aci_gw_con]
    df[aci_sw_con] = (1 - df[aci_sw_loss]) * df[aci_sw_con]
    df[aci_rw_con] = (1 - df[aci_rw_loss]) * df[aci_rw_con]
    df[agi_gw_con] = (1 - df[agi_gw_loss]) * df[agi_gw_con]
    df[agi_sw_con] = (1 - df[agi_sw_loss]) * df[agi_sw_con]
    df[agi_rw_con] = (1 - df[agi_rw_loss]) * df[agi_rw_con]

    return df


def calc_discharge_fractions():
    """"""

    cons_df = prep_consumption_fraction()
    rem = recalc_irrigation_consumption()
    df_loc = prep_water_use_2015()
    df = pd.merge(cons_df, rem, how='left', on=['FIPS', 'State'])

    res_fsw_total = df["RES_fresh_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    res_fgw_total = df["RES_fresh_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    res_pub_total = df["RES_public_total_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    com_pub_total = df["COM_public_total_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    ind_fsw_total = df["IND_fresh_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    ind_fgw_total = df["IND_fresh_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    ind_ssw_total = df["IND_saline_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    ind_sgw_total = df["IND_saline_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    ind_pub_total = df["IND_public_total_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    min_fsw_total = df["MIN_fresh_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    min_fgw_total = df["MIN_fresh_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    min_ssw_total = df["MIN_saline_surfacewater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    min_sgw_total = df["MIN_saline_groundwater_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    alv_fsw_total = df["ALV_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    alv_fgw_total = df["ALV_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    aaq_fsw_total = df["AAQ_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    aaq_fgw_total = df["AAQ_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    aaq_ssw_total = df["AAQ_saline_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    aaq_sgw_total = df["AAQ_saline_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction"]
    ci_fgw_total = df['ACI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'] \
                   + df['ACI_fresh_groundwater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction']
    ci_fsw_total = df['ACI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'] \
                   + df['ACI_fresh_surfacewater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction']
    ci_rww_total = df['ACI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'] \
                   + df['ACI_reclaimed_wastewater_import_total_mgd_to_CVL_total_total_total_total_mgd_fraction']

    gi_fgw_total = df['AGI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'] \
                   + df['AGI_fresh_groundwater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction']
    gi_fsw_total = df['AGI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction'] \
                   + df['AGI_fresh_surfacewater_withdrawal_total_mgd_to_CVL_total_total_total_total_mgd_fraction']
    gi_rww_total = df['AGI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'] \
                   + df['AGI_reclaimed_wastewater_import_total_mgd_to_CVL_total_total_total_total_mgd_fraction']

    res_fsw_sd = 1 - res_fsw_total
    res_fgw_sd = 1 - res_fgw_total
    res_ww_dis = 1 - res_pub_total
    com_ww_dis = 1 - com_pub_total
    ind_fsw_sd = 1 - ind_fsw_total
    ind_fgw_sd = 1 - ind_fgw_total
    ind_ssw_sd = 1 - ind_ssw_total
    ind_sgw_sd = 1 - ind_sgw_total
    ind_ww_dis = 1 - ind_pub_total
    min_fsw_sd = 1 - min_fsw_total
    min_fgw_sd = 1 - min_fgw_total
    min_ssw_sd = 1 - min_ssw_total
    min_sgw_sd = 1 - min_sgw_total
    alv_fsw_sd = 1 - alv_fsw_total
    alv_fgw_sd = 1 - alv_fgw_total
    aaq_fsw_sd = 1 - aaq_fsw_total
    aaq_fgw_sd = 1 - aaq_fgw_total
    aaq_ssw_od = 1 - aaq_ssw_total
    aaq_sgw_od = 1 - aaq_sgw_total
    ci_fgw_sd = 1 - ci_fgw_total
    ci_fsw_sd = 1 - ci_fsw_total
    ci_rww_sd = 1 - ci_rww_total
    gi_fgw_sd = 1 - gi_fgw_total
    gi_fsw_sd = 1 - gi_fsw_total
    gi_rww_sd = 1 - gi_rww_total

    df_out = df[['FIPS', 'State']].copy()

    df_out["RES_fresh_surfacewater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = res_fsw_sd
    df_out["RES_fresh_groundwater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = res_fgw_sd
    df_out["RES_public_total_total_total_mgd_to_WWS_total_total_total_total_mgd_fraction"] = res_ww_dis
    df_out["COM_public_total_total_total_mgd_to_WWS_total_total_total_total_mgd_fraction"] = com_ww_dis
    df_out["IND_fresh_surfacewater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = ind_fsw_sd
    df_out["IND_fresh_groundwater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = ind_fgw_sd
    df_out["IND_saline_surfacewater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = ind_ssw_sd
    df_out["IND_saline_groundwater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = ind_sgw_sd
    df_out["IND_public_total_total_total_mgd_to_WWS_total_total_total_total_mgd_fraction"] = ind_ww_dis
    df_out["MIN_fresh_surfacewater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = min_fsw_sd
    df_out["MIN_fresh_groundwater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = min_fgw_sd
    df_out["MIN_saline_surfacewater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = min_ssw_sd
    df_out["MIN_saline_groundwater_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = min_sgw_sd
    df_out["ALV_fresh_surfacewater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = alv_fsw_sd
    df_out["ALV_fresh_groundwater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = alv_fgw_sd
    df_out["AAQ_fresh_surfacewater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = aaq_fsw_sd
    df_out["AAQ_fresh_groundwater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction"] = aaq_fgw_sd
    df_out["AAQ_saline_surfacewater_withdrawal_total_mgd_to_OCD_total_total_total_total_mgd_fraction"] = aaq_ssw_od
    df_out["AAQ_saline_groundwater_withdrawal_total_mgd_to_OCD_total_total_total_total_mgd_fraction"] = aaq_sgw_od
    df_out['ACI_fresh_groundwater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = ci_fgw_sd
    df_out['ACI_fresh_surfacewater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = ci_fsw_sd
    df_out['ACI_reclaimed_wastewater_import_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = ci_rww_sd
    df_out['AGI_fresh_groundwater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = gi_fgw_sd
    df_out['AGI_fresh_surfacewater_withdrawal_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = gi_fsw_sd
    df_out['AGI_reclaimed_wastewater_import_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = gi_rww_sd

    df_out = pd.merge(df_loc, df_out, how='left', on=['FIPS', 'State'])

    return df_out


def calc_hydro_water_intensity(intensity_cap=True, intensity_cap_amt=6000000) -> pd.DataFrame:
    """calculating the water use required for a megawatt-hour of hydroelectric generation. Daily water use (mgd) is
    combined with annual generation from hydropower for each region.

    :return:                DataFrame of water intensity of hydroelectric generation by county

    """

    # read in data
    df = prep_water_use_1995(variables=['FIPS', 'State', "HY-InUse", "HY-InPow"])  # 1995 hydropower data
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # convert from mwh of generation to bbtu
    df["HY-InPow"] = df["HY-InPow"].apply(convert_mwh_bbtu)

    # get daily power generation from annual generation (annual bbtu generated)
    df["HY-InPow"] = df["HY-InPow"] / 365

    # calculate water intensity fraction million gallons per bbtu
    water_intensity_name = 'WSW_fresh_surfacewater_total_total_mgd_to_EGS_hydro_instream_nocooling_total_bbtu_intensity'
    df[water_intensity_name] = np.where(df["HY-InPow"] > 0, (df["HY-InUse"] / df["HY-InPow"]), 0)

    # cap outlier intensities
    if intensity_cap:
        df[water_intensity_name] = np.where(df[water_intensity_name] >= intensity_cap_amt,
                                            intensity_cap_amt,
                                            df[water_intensity_name])
    else:
        df[water_intensity_name] = df[water_intensity_name]

    # calculate state average
    state_avg = df[df.WSW_fresh_surfacewater_total_total_mgd_to_EGS_hydro_instream_nocooling_total_bbtu_intensity > 0]
    state_avg = df.groupby("State", as_index=False).mean().drop(['HY-InUse', 'HY-InPow'], axis=1)
    state_avg = state_avg.rename(columns={water_intensity_name: 'state_avg'})
    us_avg = state_avg['state_avg'].mean()

    ## calculate country average for states with no hydro in 1995
    country_avg = df[water_intensity_name].mean()

    df_mean_all = pd.merge(df, state_avg, how='left', on=['State'])

    # replace counties with consumption fractions of zero with the state average to replace missing data
    rep_list = df.columns[2:].to_list()
    for col in rep_list:
        df[col] = np.where(df[col] == 0, df_mean_all['state_avg'], df[col])
        df[col] = np.where(df[col] == 0, us_avg, df[col])

    # create discharge fraction
    hydro_discharge_name = 'EGS_hydro_total_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'
    df[hydro_discharge_name] = 1
    # create source fraction
    hydro_source_name = 'EGS_hydro_total_total_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd_fraction'
    df[hydro_source_name] = 1

    # merge with main dataframe and replace 0 values
    df = pd.merge(df, state_avg, how='left', on='State')
    df[water_intensity_name] = np.where(df[water_intensity_name] == 0, df['state_avg'],
                                        df[water_intensity_name])

    # simplify dataframe
    df = df[['FIPS', water_intensity_name, hydro_source_name, hydro_discharge_name]]

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on='FIPS')

    return df


def prep_county_identifier() -> pd.DataFrame:
    """preps a dataset of FIPS codes and associated county name crosswalk so that datasets with just county names can be
    mapped to appropriate FIPS codes.

            :return:                DataFrame of FIPS code and county name identifier crosswalk

            """
    # read in data
    data = 'input_data/county_FIPS_list.csv'
    df = pd.read_csv(data, dtype={'FIPS': str, 'STATEFIPS': str})

    # clean data
    df["COUNTY_SHORT"] = df["COUNTY_SHORT"].str.replace(' ', '')  # remove spaces between words in county name
    df['COUNTY_SHORT'] = df['COUNTY_SHORT'].str.lower()  # change county name to lowercase
    df['FIPS'] = df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero to FIPS code

    # create identifier column with state abbreviation and county name
    df["county_identifier"] = df["STATE"] + df["COUNTY_SHORT"]  # create identifier

    # reduce dataframe
    df = df[["FIPS", 'county_identifier']]

    return df


def prep_wastewater_data() -> pd.DataFrame:
    """preps each wastewater treatment facility data file (water flows, facility locations, facility types, and
    facility discharge data), cleans input, and brings them together to produce a single wastewater treatment
    datafile by FIPS county code.

    :return:                DataFrame of wastewater treatment water flows for each county

    """
    # read in county identifier to FIPS crosswalk data
    df_county = prep_county_identifier()

    # read in list of full county list from 2015 USGS water data
    df_county_list = prep_water_use_2015()

    # read in public water supply withdrawal data from 2015 USGS water data
    df_2015_pws = prep_water_use_2015(variables=['FIPS', 'State', 'total_pws_withdrawals_mgd'])  # pws data

    # read in wastewater facility water flow data
    ww_flow_data = 'input_data/WW_Facility_Flow.csv'
    df_ww_flow = pd.read_csv(ww_flow_data, dtype={'CWNS_NUMBER': str})

    # read in wastewater facility treatment type data
    ww_type_data = 'input_data/WW_Facility_Type.csv'
    df_ww_type = pd.read_csv(ww_type_data, dtype={'CWNS_NUMBER': str})

    # read in wastewater facility location data
    ww_loc_data = 'input_data/WW_Facility_Loc.csv'
    df_ww_loc = pd.read_csv(ww_loc_data, dtype={'CWNS_NUMBER': str})

    # read in wastewater facility discharge data
    ww_dis_data = 'input_data/WW_Discharge.csv'
    df_ww_dis = pd.read_csv(ww_dis_data, dtype={'CWNS_NUMBER': str})

    # wastewater flow type dictionary
    flow_dict = {'EXIST_INFILTRATION': 'infiltration_wastewater_mgd',
                 'EXIST_TOTAL': 'total_wastewater_mgd',
                 'EXIST_MUNI': 'municipal_wastewater_mgd'}

    # wastewater discharge type dictionary
    dis_dict = {'outfall to surface waters': 'wastewater_surface_discharge',
                'ocean discharge': 'wastewater_ocean_discharge',
                'deep well': 'wastewater_groundwater_discharge',
                "reuse: industrial": 'wastewater_industrial_discharge',
                'evaporation': 'wastewater_consumption',
                'spray irrigation': 'wastewater_irrigation_discharge',
                'overland flow no discharge': 'wastewater_wastewater_discharge',
                'overland flow with discharge': 'wastewater_surface_discharge',
                'discharge to another facility': 'wastewater_wastewater_discharge',
                'combined sewer overflow (cso) discharge': 'wastewater_surface_discharge',
                'other': 'wastewater_surface_discharge',
                'discharge to groundwater': 'wastewater_groundwater_discharge',
                'no discharge, unknown': 'wastewater_wastewater_discharge',
                'reuse: irrigation': 'wastewater_irrigation_discharge',
                'reuse: other non-potable': 'wastewater_surface_discharge',
                'reuse: indirect potable': 'wastewater_surface_discharge',
                'reuse: potable': 'wastewater_pws_discharge',
                'reuse: groundwater recharge': 'wastewater_groundwater_discharge'}

    # wastewater facility treatment type dictionary
    treat_dict = {'raw discharge': 'wastewater_no_treatment',
                  'primary (45mg/l< bod)': 'wastewater_primary_treatment',
                  'advanced primary': 'wastewater_advanced_treatment',
                  'secondary wastewater treatment': 'wastewater_secondary_treatment',
                  'secondary': 'wastewater_secondary_treatment',
                  'advanced treatment': 'wastewater_advanced_treatment'}

    # correct naming in wastewater facility location data
    df_ww_loc["PRIMARY_COUNTY"] = np.where(df_ww_loc["PRIMARY_COUNTY"] == "Bedford City", "Bedford",
                                           df_ww_loc["PRIMARY_COUNTY"])

    # reformat county identifier columns in wastewater facility location data
    df_ww_loc['PRIMARY_COUNTY'] = df_ww_loc['PRIMARY_COUNTY'].str.lower()  # change to lowercase
    df_ww_loc["PRIMARY_COUNTY"] = df_ww_loc["PRIMARY_COUNTY"].str.replace(' ', '')  # remove spaces between words

    # create a state+county identifier column in wastewater facility location data
    df_ww_loc['CWNS_NUMBER'] = df_ww_loc['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero
    df_ww_loc["county_identifier"] = df_ww_loc["STATE"] + df_ww_loc["PRIMARY_COUNTY"]  # add identifier

    # combine wastewater facility location data and county to FIPS crosswalk data to get a FIPS code for each plant
    df_ww_loc = pd.merge(df_ww_loc, df_county, how="left", on="county_identifier")  # merge dataframes
    df_ww_loc = df_ww_loc[["CWNS_NUMBER", "FIPS", "STATE"]]  # reducing to required variables

    # prepare wastewater treatment flow data
    df_ww_flow = df_ww_flow[["CWNS_NUMBER", "EXIST_INFILTRATION", "EXIST_TOTAL"]]  # reducing to required variables
    df_ww_flow = df_ww_flow.dropna(subset=["EXIST_TOTAL"])  # drop treatment plants with zero flows
    df_ww_flow["EXIST_INFILTRATION"] = df_ww_flow["EXIST_INFILTRATION"].fillna(0)  # fill blank infiltration with zero

    # calculate municipal water flows for each facility in wastewater treatment flow data
    df_ww_flow['EXIST_MUNI'] = df_ww_flow["EXIST_TOTAL"] - df_ww_flow["EXIST_INFILTRATION"]  # subtract infiltration

    # reformat and rename wastewater treatment facility flow data
    df_ww_flow['CWNS_NUMBER'] = df_ww_flow['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero
    df_ww_flow.rename(columns=flow_dict, inplace=True)  # rename columns to add descriptive language

    # combine wastewater treatment facility flow data and wastewater treatment facility location data
    df_ww_flow = pd.merge(df_ww_flow, df_ww_loc, how="left", on='CWNS_NUMBER')  # merge dataframes

    # remove wastewater treatment facility flow data rows for geographic areas not included in other datasets
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "AS"]  # remove flow values for American Samoa
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "GU"]  # remove flow values for Guam
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "PR"]  # remove flow values for Guam
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "VI"]  # remove flow values for Guam

    # prep wastewater treatment facility discharge type data to remove naming and capitalization inconsistencies
    df_ww_dis['DISCHARGE_METHOD'] = df_ww_dis['DISCHARGE_METHOD'].str.replace(',', '')  # remove commas
    df_ww_dis['DISCHARGE_METHOD'] = df_ww_dis['DISCHARGE_METHOD'].str.lower()  # change to lowercase
    df_ww_dis['DISCHARGE_METHOD'] = np.where(df_ww_dis['DISCHARGE_METHOD'] == "reuse: ground water recharge",  # rename
                                             "reuse: groundwater recharge",
                                             df_ww_dis['DISCHARGE_METHOD'])
    df_ww_dis['DISCHARGE_METHOD'] = np.where(df_ww_dis['DISCHARGE_METHOD'] == "cso discharge",  # rename
                                             "combined sewer overflow (cso) discharge",
                                             df_ww_dis['DISCHARGE_METHOD'])

    # rename wastewater treatment discharge types
    df_ww_dis['DISCHARGE_METHOD_BIN'] = df_ww_dis['DISCHARGE_METHOD'].map(dis_dict)  # map to discharge dictionary

    # reduce and reformat variables in wastewater treatment facility discharge data
    df_ww_dis = df_ww_dis[["CWNS_NUMBER", 'DISCHARGE_METHOD_BIN', 'PRES_FLOW_PERCENTAGE']]  # keep required columns
    df_ww_dis['CWNS_NUMBER'] = df_ww_dis['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero
    df_ww_dis['PRES_FLOW_PERCENTAGE'] = df_ww_dis['PRES_FLOW_PERCENTAGE'] / 100  # convert to fraction

    # pivot wastewater treatment facility discharge dataframe to get discharge type as columns
    df_ww_dis = pd.pivot_table(df_ww_dis, values='PRES_FLOW_PERCENTAGE', index=['CWNS_NUMBER'],
                               columns=['DISCHARGE_METHOD_BIN'],
                               aggfunc=np.sum)  # pivot to get discharge types as columns
    df_ww_dis = df_ww_dis.reset_index()  # reset index to remove multi-index from pivot table
    df_ww_dis = df_ww_dis.rename_axis(None, axis=1)  # drop index name

    # fill nan discharge percentage values in wastewater facility discharge data with 0 percent
    for col in df_ww_dis.columns[1:]:
        df_ww_dis[col] = df_ww_dis[col].fillna(0)  # fill nan rows with 0

    # calculate the sum of all discharge type percentages by plant in wastewater treatment facility discharge data
    df_ww_dis['sum_pct'] = df_ww_dis.iloc[:, 1:].sum(axis=1)  # calculate sum of all flow percentages

    # for treatment plants with no discharge data, assume 70% of discharge is to surface discharge
    df_ww_dis['wastewater_surface_discharge'] = np.where(df_ww_dis['sum_pct'] == 0,  # fill blanks values
                                                         .68,
                                                         df_ww_dis['wastewater_surface_discharge'])
    # for treatment plants with no discharge data, assume 18% of discharge is to groundwater
    df_ww_dis['wastewater_groundwater_discharge'] = np.where(df_ww_dis['sum_pct'] == 0,  # fill blanks values
                                                             .19,
                                                             df_ww_dis['wastewater_groundwater_discharge'])

    # for treatment plants with no discharge data, assume 8% of discharge is to irrigation
    df_ww_dis['wastewater_irrigation_discharge'] = np.where(df_ww_dis['sum_pct'] == 0,  # fill blanks values
                                                            .08,
                                                            df_ww_dis['wastewater_irrigation_discharge'])

    # for treatment plants with no discharge data, assume 5% of discharge is to consumption
    df_ww_dis['wastewater_consumption'] = np.where(df_ww_dis['sum_pct'] == 0,  # fill blanks values
                                                   .05,
                                                   df_ww_dis['wastewater_consumption'])

    # for treatment plants that discharge to another treatment plant, the values are redistributed
    # for treatment plants with no discharge data, assume 70% of discharge is to surface discharge
    df_ww_dis['wastewater_surface_discharge'] = np.where(df_ww_dis['wastewater_wastewater_discharge'] > 0,
                                                         df_ww_dis['wastewater_surface_discharge']
                                                         + (.68 * df_ww_dis['wastewater_wastewater_discharge']),
                                                         df_ww_dis['wastewater_surface_discharge'])
    # for treatment plants with no discharge data, assume 18% of discharge is to groundwater
    df_ww_dis['wastewater_groundwater_discharge'] = np.where(df_ww_dis['wastewater_wastewater_discharge'] > 0,
                                                             # fill blanks values
                                                             df_ww_dis['wastewater_groundwater_discharge']
                                                             + (.19 * df_ww_dis['wastewater_wastewater_discharge']),
                                                             df_ww_dis['wastewater_groundwater_discharge'])

    # for treatment plants with no discharge data, assume 8% of discharge is to irrigation
    df_ww_dis['wastewater_irrigation_discharge'] = np.where(df_ww_dis['wastewater_wastewater_discharge'] > 0,
                                                            # fill blanks values
                                                            df_ww_dis['wastewater_irrigation_discharge']
                                                            + (.08 * df_ww_dis['wastewater_wastewater_discharge']),
                                                            df_ww_dis['wastewater_irrigation_discharge'])

    # for treatment plants with no discharge data, assume 5% of discharge is to consumption
    df_ww_dis['wastewater_consumption'] = np.where(df_ww_dis['wastewater_wastewater_discharge'] > 0,
                                                   # fill blanks values
                                                   df_ww_dis['wastewater_consumption']
                                                   + (.05 * df_ww_dis['wastewater_wastewater_discharge']),
                                                   df_ww_dis['wastewater_consumption'])

    # drop discharges to wastewater
    df_ww_dis = df_ww_dis.drop(['wastewater_wastewater_discharge'], axis=1)

    df_ww_dis['sum_pct'] = df_ww_dis.iloc[:, 1:-1].sum(axis=1)  # recalculate sum

    # combine wastewater treatment facility flow data and wastewater treatment facility discharge data
    df_ww_flow = pd.merge(df_ww_flow, df_ww_dis, how='left', on='CWNS_NUMBER')

    # prep wastewater treatment facility treatment type data
    df_ww_type = df_ww_type[['CWNS_NUMBER', 'PRES_EFFLUENT_TREATMENT_LEVEL']]  # reducing to required variables
    df_ww_type['pct'] = 1  # add a percent column

    # reduce and reformat variables in wastewater treatment facility treatment type data
    df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'] = df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'].str.lower()  # lowercase
    df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'] = np.where(df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'] ==  # rename
                                                           "primary (45mg/l is less than bod)",
                                                           "primary (45mg/l< bod)",
                                                           df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'])

    # bin wastewater treatment facility treatment types
    df_ww_type['TREATMENT_LEVEL_BIN'] = df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'].map(treat_dict)

    # pivot wastewater treatment facility treatment type dataframe to get treatment type as columns
    df_ww_type = pd.pivot_table(df_ww_type, values='pct', index=['CWNS_NUMBER'],
                                columns=['TREATMENT_LEVEL_BIN'],
                                aggfunc=np.sum)  # pivot to get treatment types as columns
    df_ww_type = df_ww_type.reset_index()  # reset index to remove multi-index from pivot table
    df_ww_type = df_ww_type.rename_axis(None, axis=1)  # drop index name

    # fill nan treatment type values with 0 percent
    for col in df_ww_type.columns[1:]:  # fill nan rows with 0
        df_ww_type[col] = df_ww_type[col].fillna(0)

    df_ww_type['sum_type'] = df_ww_type.iloc[:, 1:].sum(axis=1)  # calculate sum
    df_ww_type['CWNS_NUMBER'] = df_ww_type['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero

    # combine wastewater treatment facility flow data and wastewater treatment facility type data
    df_ww_flow = pd.merge(df_ww_flow, df_ww_type, how='left', on='CWNS_NUMBER')

    # fill nan with 0
    for col in df_ww_type.columns:  # fill nan rows with 0
        df_ww_flow[col] = df_ww_flow[col].fillna(0)

    # for treatment plants with flow data but no treatment type data, assume 60% of treatment type is secondary
    df_ww_flow['wastewater_secondary_treatment'] = np.where(df_ww_flow['sum_type'] < 1,
                                                            .6,
                                                            df_ww_flow['wastewater_secondary_treatment'])
    # for treatment plants with flow data but no treatment type data, assume 40% of treatment type is secondary
    df_ww_flow['wastewater_advanced_treatment'] = np.where(df_ww_flow['sum_type'] < 1,
                                                           .4,
                                                           df_ww_flow['wastewater_advanced_treatment'])
    df_ww_flow['sum_type'] = df_ww_flow.iloc[:, 15:-1].sum(axis=1)  # recalculate sum

    # creating new df and  reducing list of variables
    df_ww_fractions = df_ww_flow.drop(['sum_type', 'sum_pct', 'infiltration_wastewater_mgd', 'total_wastewater_mgd',
                                       'municipal_wastewater_mgd'], axis=1)
    df_ww_flow = df_ww_flow[['FIPS', 'CWNS_NUMBER', 'infiltration_wastewater_mgd', 'total_wastewater_mgd',
                             'municipal_wastewater_mgd']]

    # group by FIPS code to get average wastewater discharge and treatment types by county
    df_ww_fractions = df_ww_fractions.groupby("FIPS", as_index=False).mean()

    # combine with full county list to get values for each county and fill counties with no plants with 0
    df_ww_fractions = pd.merge(df_county_list, df_ww_fractions, how='left', on='FIPS')
    df_ww_fractions.fillna(0, inplace=True)

    # group by FIPS code to get average wastewater discharge and treatment types by county
    df_ww_flow = df_ww_flow.groupby("FIPS", as_index=False).mean()

    # combine with full county list to get values for each county and fill counties with no plants with 0
    df_ww_flow = pd.merge(df_county_list, df_ww_flow, how='left', on='FIPS')
    df_ww_flow.fillna(0, inplace=True)

    # recombine flow and fraction dataframes
    df_ww = pd.merge(df_ww_flow, df_ww_fractions, how='left', on=['FIPS', 'State', 'County'])

    # create output df
    df_out = df_ww.copy()

    # add column indicating percentage of energy from electricity, assumed 100%
    df_out['WWD_treatment_advanced_total_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['WWD_treatment_primary_total_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['WWD_treatment_secondary_total_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1

    df_ww['advanced_infiltration_flows_mgd'] = df_ww['wastewater_advanced_treatment'] \
                                               * df_ww['infiltration_wastewater_mgd']
    df_ww['primary_infiltration_flows_mgd'] = df_ww['wastewater_secondary_treatment'] \
                                              * df_ww['infiltration_wastewater_mgd']
    df_ww['secondary_infiltration_flows_mgd'] = df_ww['wastewater_secondary_treatment'] \
                                                * df_ww['infiltration_wastewater_mgd']

    df_ww['advanced_municipal_flows_mgd'] = df_ww['wastewater_advanced_treatment'] \
                                            * df_ww['municipal_wastewater_mgd']
    df_ww['primary_municipal_flows_mgd'] = df_ww['wastewater_secondary_treatment'] \
                                           * df_ww['municipal_wastewater_mgd']
    df_ww['secondary_municipal_flows_mgd'] = df_ww['wastewater_secondary_treatment'] \
                                             * df_ww['municipal_wastewater_mgd']

    # name water flows for output dictionary
    advanced_infiltration_flows_mgd = 'WWD_advanced_infiltration_total_total_mgd_from_WWD_advanced_infiltration_total_total_mgd'
    primary_infiltration_flows_mgd = 'WWD_primary_infiltration_total_total_mgd_from_WWD_primary_infiltration_total_total_mgd'
    secondary_infiltration_flows_mgd = 'WWD_secondary_infiltration_total_total_mgd_from_WWD_secondary_infiltration_total_total_mgd'
    advanced_municipal_flows_mgd = 'WWD_advanced_municipal_total_total_mgd_from_WWD_advanced_municipal_total_total_mgd'
    primary_municipal_flows_mgd = 'WWD_primary_municipal_total_total_mgd_from_WWD_primary_municipal_total_total_mgd'
    secondary_municipal_flows_mgd = 'WWD_secondary_municipal_total_total_mgd_from_WWD_secondary_municipal_total_total_mgd'

    # save flows to output dictionary
    df_out[advanced_infiltration_flows_mgd] = df_ww['advanced_infiltration_flows_mgd']
    df_out[primary_infiltration_flows_mgd] = df_ww['primary_infiltration_flows_mgd']
    df_out[secondary_infiltration_flows_mgd] = df_ww['secondary_infiltration_flows_mgd']
    df_out[advanced_municipal_flows_mgd] = df_ww['advanced_municipal_flows_mgd']
    df_out[primary_municipal_flows_mgd] = df_ww['primary_municipal_flows_mgd']
    df_out[secondary_municipal_flows_mgd] = df_ww['secondary_municipal_flows_mgd']

    # name discharges for output
    # consumption
    advanced_infiltration_cons_mgd = 'WWD_advanced_infiltration_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    primary_infiltration_cons_mgd = 'WWD_primary_infiltration_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    secondary_infiltration_cons_mgd = 'WWD_secondary_infiltration_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    advanced_municipal_cons_mgd = 'WWD_advanced_municipal_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    primary_municipal_cons_mgd = 'WWD_primary_municipal_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
    secondary_municipal_cons_mgd = 'WWD_secondary_municipal_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction'

    # groundwater discharge
    advanced_infiltration_gwd_mgd = 'WWD_advanced_infiltration_total_total_mgd_to_GWD_total_total_total_total_mgd_fraction'
    primary_infiltration_gwd_mgd = 'WWD_primary_infiltration_total_total_mgd_to_GWD_total_total_total_total_mgd_fraction'
    secondary_infiltration_gwd_mgd = 'WWD_secondary_infiltration_total_total_mgd_to_GWD_total_total_total_total_mgd_fraction'
    advanced_municipal_gwd_mgd = 'WWD_advanced_municipal_total_total_mgd_to_GWD_total_total_total_total_mgd_fraction'
    primary_municipal_gwd_mgd = 'WWD_primary_municipal_total_total_mgd_to_GWD_total_total_total_total_mgd_fraction'
    secondary_municipal_gwd_mgd = 'WWD_secondary_municipal_total_total_mgd_to_GWD_total_total_total_total_mgd_fraction'

    # industrial discharge
    advanced_infiltration_inx_mgd = 'WWD_advanced_infiltration_total_total_mgd_to_INX_total_total_total_total_mgd_fraction'
    primary_infiltration_inx_mgd = 'WWD_primary_infiltration_total_total_mgd_to_INX_total_total_total_total_mgd_fraction'
    secondary_infiltration_inx_mgd = 'WWD_secondary_infiltration_total_total_mgd_to_INX_total_total_total_total_mgd_fraction'
    advanced_municipal_inx_mgd = 'WWD_advanced_municipal_total_total_mgd_to_INX_total_total_total_total_mgd_fraction'
    primary_municipal_inx_mgd = 'WWD_primary_municipal_total_total_mgd_to_INX_total_total_total_total_mgd_fraction'
    secondary_municipal_inx_mgd = 'WWD_secondary_municipal_total_total_mgd_to_INX_total_total_total_total_mgd_fraction'

    # irrigation discharge
    advanced_infiltration_irx_mgd = 'WWD_advanced_infiltration_total_total_mgd_to_IRX_total_total_total_total_mgd_fraction'
    primary_infiltration_irx_mgd = 'WWD_primary_infiltration_total_total_mgd_to_IRX_total_total_total_total_mgd_fraction'
    secondary_infiltration_irx_mgd = 'WWD_secondary_infiltration_total_total_mgd_to_IRX_total_total_total_total_mgd_fraction'
    advanced_municipal_irx_mgd = 'WWD_advanced_municipal_total_total_mgd_to_IRX_total_total_total_total_mgd_fraction'
    primary_municipal_irx_mgd = 'WWD_primary_municipal_total_total_mgd_to_IRX_total_total_total_total_mgd_fraction'
    secondary_municipal_irx_mgd = 'WWD_secondary_municipal_total_total_mgd_to_IRX_total_total_total_total_mgd_fraction'

    # ocean discharge
    advanced_infiltration_ocd_mgd = 'WWD_advanced_infiltration_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction'
    primary_infiltration_ocd_mgd = 'WWD_primary_infiltration_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction'
    secondary_infiltration_ocd_mgd = 'WWD_secondary_infiltration_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction'
    advanced_municipal_ocd_mgd = 'WWD_advanced_municipal_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction'
    primary_municipal_ocd_mgd = 'WWD_primary_municipal_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction'
    secondary_municipal_ocd_mgd = 'WWD_secondary_municipal_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction'

    # surface discharge
    advanced_infiltration_srd_mgd = 'WWD_advanced_infiltration_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'
    primary_infiltration_srd_mgd = 'WWD_primary_infiltration_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'
    secondary_infiltration_srd_mgd = 'WWD_secondary_infiltration_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'
    advanced_municipal_srd_mgd = 'WWD_advanced_municipal_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'
    primary_municipal_srd_mgd = 'WWD_primary_municipal_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'
    secondary_municipal_srd_mgd = 'WWD_secondary_municipal_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'

    # save discharges to output
    df_out[advanced_infiltration_cons_mgd] = df_ww['wastewater_consumption']
    df_out[primary_infiltration_cons_mgd] = df_ww['wastewater_consumption']
    df_out[secondary_infiltration_cons_mgd] = df_ww['wastewater_consumption']
    df_out[advanced_municipal_cons_mgd] = df_ww['wastewater_consumption']
    df_out[primary_municipal_cons_mgd] = df_ww['wastewater_consumption']
    df_out[secondary_municipal_cons_mgd] = df_ww['wastewater_consumption']

    # groundwater discharge
    df_out[advanced_infiltration_gwd_mgd] = df_ww['wastewater_groundwater_discharge']
    df_out[primary_infiltration_gwd_mgd] = df_ww['wastewater_groundwater_discharge']
    df_out[secondary_infiltration_gwd_mgd] = df_ww['wastewater_groundwater_discharge']
    df_out[advanced_municipal_gwd_mgd] = df_ww['wastewater_groundwater_discharge']
    df_out[primary_municipal_gwd_mgd] = df_ww['wastewater_groundwater_discharge']
    df_out[secondary_municipal_gwd_mgd] = df_ww['wastewater_groundwater_discharge']

    # industrial discharge
    df_out[advanced_infiltration_inx_mgd] = df_ww['wastewater_industrial_discharge']
    df_out[primary_infiltration_inx_mgd] = df_ww['wastewater_industrial_discharge']
    df_out[secondary_infiltration_inx_mgd] = df_ww['wastewater_industrial_discharge']
    df_out[advanced_municipal_inx_mgd] = df_ww['wastewater_industrial_discharge']
    df_out[primary_municipal_inx_mgd] = df_ww['wastewater_industrial_discharge']
    df_out[secondary_municipal_inx_mgd] = df_ww['wastewater_industrial_discharge']

    # irrigation discharge
    df_out[advanced_infiltration_irx_mgd] = df_ww['wastewater_irrigation_discharge']
    df_out[primary_infiltration_irx_mgd] = df_ww['wastewater_irrigation_discharge']
    df_out[secondary_infiltration_irx_mgd] = df_ww['wastewater_irrigation_discharge']
    df_out[advanced_municipal_irx_mgd] = df_ww['wastewater_irrigation_discharge']
    df_out[primary_municipal_irx_mgd] = df_ww['wastewater_irrigation_discharge']
    df_out[secondary_municipal_irx_mgd] = df_ww['wastewater_irrigation_discharge']

    # ocean discharge
    df_out[advanced_infiltration_ocd_mgd] = df_ww['wastewater_ocean_discharge']
    df_out[primary_infiltration_ocd_mgd] = df_ww['wastewater_ocean_discharge']
    df_out[secondary_infiltration_ocd_mgd] = df_ww['wastewater_ocean_discharge']
    df_out[advanced_municipal_ocd_mgd] = df_ww['wastewater_ocean_discharge']
    df_out[primary_municipal_ocd_mgd] = df_ww['wastewater_ocean_discharge']
    df_out[secondary_municipal_ocd_mgd] = df_ww['wastewater_ocean_discharge']

    # surface discharge
    df_out[advanced_infiltration_srd_mgd] = df_ww['wastewater_surface_discharge']
    df_out[primary_infiltration_srd_mgd] = df_ww['wastewater_surface_discharge']
    df_out[secondary_infiltration_srd_mgd] = df_ww['wastewater_surface_discharge']
    df_out[advanced_municipal_srd_mgd] = df_ww['wastewater_surface_discharge']
    df_out[primary_municipal_srd_mgd] = df_ww['wastewater_surface_discharge']
    df_out[secondary_municipal_srd_mgd] = df_ww['wastewater_surface_discharge']

    # name energy intensity for output
    inf_adv_in = 'WWD_treatment_advanced_total_total_bbtu_from_WWD_advanced_infiltration_total_total_mgd_intensity'
    mun_adv_in = 'WWD_treatment_advanced_total_total_bbtu_from_WWD_advanced_municipal_total_total_mgd_intensity'
    inf_prim_in = 'WWD_treatment_primary_total_total_bbtu_from_WWD_primary_infiltration_total_total_mgd_intensity'
    mun_prim_in = 'WWD_treatment_primary_total_total_bbtu_from_WWD_primary_municipal_total_total_mgd_intensity'
    inf_sec_in = 'WWD_treatment_secondary_total_total_bbtu_from_WWD_secondary_infiltration_total_total_mgd_intensity'
    mun_sec_in = 'WWD_treatment_secondary_total_total_bbtu_from_WWD_secondary_municipal_total_total_mgd_intensity'

    adv_intensity_value = convert_kwh_bbtu(2690)
    primary_intensity_value = convert_kwh_bbtu(2080)
    secondary_intensity_value = convert_kwh_bbtu(750)

    # save intensity to output
    df_out[inf_adv_in] = adv_intensity_value
    df_out[mun_adv_in] = adv_intensity_value
    df_out[inf_prim_in] = primary_intensity_value
    df_out[mun_prim_in] = primary_intensity_value
    df_out[inf_sec_in] = secondary_intensity_value
    df_out[mun_sec_in] = secondary_intensity_value

    df_out['WWD_treatment_advanced_total_total_bbtu_to_REJ_total_total_total_total_bbtu_fraction'] = .35
    df_out['WWD_treatment_primary_total_total_bbtu_to_REJ_total_total_total_total_bbtu_fraction'] = .35
    df_out['WWD_treatment_secondary_total_total_bbtu_to_REJ_total_total_total_total_bbtu_fraction'] = .35

    df_out['WWD_treatment_advanced_total_total_bbtu_to_ESV_total_total_total_total_bbtu_fraction'] = .65
    df_out['WWD_treatment_primary_total_total_bbtu_to_ESV_total_total_total_total_bbtu_fraction'] = .65
    df_out['WWD_treatment_secondary_total_total_bbtu_to_ESV_total_total_total_total_bbtu_fraction'] = .65

    df_out = df_out.drop(
        ['wastewater_surface_discharge', 'wastewater_ocean_discharge', 'wastewater_irrigation_discharge',
         'wastewater_consumption', 'wastewater_groundwater_discharge', 'infiltration_wastewater_mgd',
         'total_wastewater_mgd', 'municipal_wastewater_mgd', 'wastewater_no_treatment', 'wastewater_primary_treatment',
         'wastewater_advanced_treatment', 'wastewater_secondary_treatment', ], axis=1)

    return df_out


# def calc_sc_ww_values():

# TODO fix south carolina estimates by brining in residential pws deliveries, commercial pws deliveres, ind
# pws deliveries, and their fresh consumption fractions.

## create a dictionary of public water supply flows for south carolina by FIPS code
# df_2015_pws = df_2015_pws[df_2015_pws.State == "SC"]
# df_2015_pws = df_2015_pws.drop("State", axis=1)
# sc_pws_dict = df_2015_pws.set_index('FIPS').to_dict()
#
## filling in estimates for south carolina from total public water supply flows given missing data
# df_ww = pd.merge(df_ww, df_2015_pws, how='left', on='FIPS')

# for row in df_ww.iterrows():
#    df_ww['total_wastewater_mgd'] = np.where(df_ww['State'] == "SC",  # fill total wastewater from public supply
#                                             df_ww['total_pws_withdrawals_mgd'],
#                                             df_ww['total_wastewater_mgd'])
#    df_ww['municipal_wastewater_mgd'] = np.where(df_ww['State'] == "SC",  # fill total wastewater from public supply
#                                                 df_ww['total_wastewater_mgd'],
#                                                 df_ww['municipal_wastewater_mgd'])
#
#    # replace discharge values
#    df_ww['wastewater_surface_discharge'] = np.where(df_ww['State'] == "SC",  # fill discharge with surface
#                                                         .68,
#                                                         df_ww['wastewater_surface_discharge_mgd'])
#    df_ww['wastewater_groundwater_discharge'] = np.where(df_ww['State'] == "SC",  # fill discharge with surface
#                                                         .19,
#                                                         df_ww['wastewater_groundwater_discharge_mgd'])
#    df_ww['wastewater_irrigation_discharge'] = np.where(df_ww['State'] == "SC",  # fill discharge with surface
#                                                         .08,
#                                                         df_ww['wastewater_irrigation_discharge'])
#    df_ww['wastewater_consumption'] = np.where(df_ww['State'] == "SC",  # fill discharge with surface
#                                                         .05,
#                                                         df_ww['wastewater_consumption'])
#
#    # replace treatment values
#    df_ww['wastewater_advanced_treatment_mgd'] = np.where(df_ww['State'] == "SC",  # fill treatment with advanced
#                                                          .4 ,
#                                                          df_ww['wastewater_advanced_treatment_mgd'])
#    df_ww['wastewater_secondary_treatment_mgd'] = np.where(df_ww['State'] == "SC",  # fill treatment with secondary
#                                                           .6,
#                                                           df_ww['wastewater_secondary_treatment_mgd'])
#

def prep_power_plant_location() -> pd.DataFrame:
    """prepping power plant location information to provide a dataframe of power plant codes and their associated
    FIPS code.

    :return:                DataFrame of power plant codes and associated FIPS codes

    """
    # read in wastewater facility water flow data
    df_plant_data = 'input_data/EIA860_Generator_Y2015.csv'
    df_plant = pd.read_csv(df_plant_data, skiprows=1, usecols=['Plant Code', "State", 'County'])

    # read in data
    df_county = prep_county_identifier()  # county identifier data

    # prepare county identifier data
    df_county["county_identifier"] = df_county['county_identifier'].str.replace("'", '', regex=True)  # apostrophes
    df_county["county_identifier"] = df_county["county_identifier"].str.replace('.', '', regex=True)  # periods
    df_county["county_identifier"] = df_county["county_identifier"].str.replace('-', '', regex=True)  # dashes
    df_county["county_identifier"] = df_county["county_identifier"].str.replace(r"[^\w ]", '', regex=True)  # non alpha

    # prepare power plant location data
    df_plant = df_plant.drop_duplicates()  # drop duplicate generators to get individual power plants
    df_plant = df_plant.dropna(subset=["Plant Code"])  # drop rows with missing plant codes
    df_plant['County'] = df_plant['County'].str.lower()  # change to lowercase
    df_plant["County"] = df_plant["County"].str.replace(' ', '')  # remove spaces between words
    df_plant["county_identifier"] = df_plant["State"] + df_plant["County"]  # add county_identifier column
    df_plant["county_identifier"] = df_plant["county_identifier"].str.replace(r"[^\w ]", '', regex=True)  # non alpha

    # create a list of counties that need name corrections
    city_list = ['VAchesapeakecity', 'VAportsmouthcity', 'VAhopewellcity', 'VAalexandriacity',
                 'VAcovingtoncity', 'VAsuffolkcity', 'VAharrisonburgcity', 'VAsalemcity',
                 'VAlynchburgcity', 'VAdanvillecity', 'VAmanassascity', 'VAhamptoncity',
                 'VAvirginiabeachcity', 'VAbristolcity', 'MOstlouiscity']

    # remove 'city' from identifiers in city_list
    for i in city_list:
        df_plant["county_identifier"] = np.where(df_plant["county_identifier"] == i,
                                                 df_plant["county_identifier"].str.replace('city', '', regex=True),
                                                 df_plant["county_identifier"])

    # rename specific county identifiers
    df_plant["county_identifier"] = np.where(df_plant["county_identifier"] == "MEchainofponds",  # rename
                                             "MEfranklin",
                                             df_plant["county_identifier"])
    df_plant["county_identifier"] = np.where(df_plant["county_identifier"] == "AKwadehampton",  # rename
                                             "AKkusilvak",
                                             df_plant["county_identifier"])
    df_plant["county_identifier"] = np.where(df_plant["county_identifier"] == "AKprinceofwalesketchikan",  # rename
                                             "AKprinceofwaleshyder",
                                             df_plant["county_identifier"])
    df_plant["county_identifier"] = np.where(df_plant["county_identifier"] == "AKwrangellpetersburg",  # rename
                                             "AKpetersburg",
                                             df_plant["county_identifier"])
    df_plant["county_identifier"] = np.where(df_plant["county_identifier"] == "AKwrangellpetersburg",  # rename
                                             "AKpetersburg",
                                             df_plant["county_identifier"])

    # replace county identifiers for specific power plants
    skagway_list = [66, 7751, 56542]
    for s in skagway_list:
        df_plant["county_identifier"] = np.where(df_plant["Plant Code"] == s,
                                                 "AKskagway",
                                                 df_plant["county_identifier"])
    hoonah_list = [6702, 7462, 7463]
    for h in hoonah_list:
        df_plant["county_identifier"] = np.where(df_plant["Plant Code"] == h,
                                                 "AKhoonahangoon",
                                                 df_plant["county_identifier"])

    # merge power plant location data with county identifier-FIPS crosswalk
    df_plant = pd.merge(df_plant, df_county, how="left", on="county_identifier")  # merge dataframes
    df_plant = df_plant.rename(columns={"Plant Code": "plant_code"})  # rename column

    return df_plant


def prep_electricity_generation() -> pd.DataFrame:
    """ Provides a dataframe of electricity generation (MWh) and fuel use (BBTU) per year by generating technology type
    and by FIPS code. Can be used to estimate fuel use for electricity generation by type for each county
    and total electricity generation by county.

    :return:                DataFrame of fuel use in electricity generation and total generation by generation type
                            within each FIPS code
    """

    # read in electricity generation data by power plant id
    data = 'input_data\EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.csv'
    df = pd.read_csv(data, skiprows=5)

    # read in power plant location data by power plant id
    df_gen_loc = prep_power_plant_location()
    df_loc = prep_water_use_2015()

    # read in power plant cooling type data
    cooling_data = r'input_data\2015_TE_Model_Estimates_USGS.csv'
    df_cooling = pd.read_csv(cooling_data,
                             usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE', 'GENERATION_TYPE',
                                      'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])

    # remove unnecessary variables
    df_gen_loc = df_gen_loc[['FIPS', 'plant_code']]
    df = df[['Plant Id', "AER\nFuel Type Code", "Reported\nPrime Mover", "Total Fuel Consumption\nMMBtu",
             "Net Generation\n(Megawatthours)"]]

    # create a dictionary to bin power plant fuel types
    fuel_consumption_dict = {'SUN': 'solar',  # solar
                             'COL': 'coal',  # coal
                             'DFO': 'petroleum',  # distillate petroleum
                             "GEO": 'geothermal',  # geothermal
                             'HPS': 'hydro',  # hydro pumped storage
                             'HYC': 'hydro',  # hydro conventional
                             'MLG': 'biomass',  # biogenic municipal solid waste and landfill gas
                             'NG': 'natgas',  # natural gas
                             'NUC': 'nuclear',  # nuclear
                             'OOG': 'other',  # other gases
                             'ORW': 'other',  # other renewables
                             'OTH': 'other',  # other
                             'PC': 'petroleum',  # petroleum coke
                             'RFO': 'petroleum',  # residual petroleum
                             'WND': 'wind',  # wind
                             'WOC': 'coal',  # waste coal
                             'WOO': 'petroleum',  # waste oil
                             'WWW': 'biomass'}  # wood and wood waste

    prime_mover_dict = {'HY': 'instream',
                        'CA': 'combinedcycle',
                        'CT': 'combinedcycle',
                        'ST': 'steam',
                        'GT': 'combustionturbine',
                        'IC': 'internalcombustion',
                        'WT': 'onshore',
                        'PS': 'pumpedstorage',
                        'PV': 'photovoltaic',
                        'CS': 'combinedcycle',
                        'CE': 'compressedair',
                        'BT': 'binarycycle',
                        'OT': 'other',
                        'FC': 'fuelcell',
                        'CP': 'csp',
                        'BA': 'battery',
                        'FW': 'flywheel'
                        }

    water_source_dict = {'SW': 'surfacewater',  # river, canal, bay
                         'GW': 'groundwater',  # well, aquifer
                         'PD': 'wastewater',  # PD = plant discharge
                         "-nr-": "surfacewater",  # all blanks assumed to be surface water
                         "GW & PD": "groundwater",  # all GW+PD are assumed to be groundwater only
                         "GW & SW": 'surfacewater',  # all GW+SW combinations are assumed to be SW
                         "OT": "surfacewater"
                         }

    water_type_dict = {'FR': 'fresh',
                       'SA': 'saline',
                       'OT': 'fresh',  # all other source is assumed to be surface water
                       "FR & BE": 'fresh',  # all combinations with fresh and BE are assumed to be fresh
                       "BE": "fresh",  # reclaimed wastewater
                       "BR": "saline",  # all brackish should be changed to saline
                       "": "fresh"}

    cooling_dict = {'COMPLEX': 'complex',
                    'ONCE-THROUGH FRESH': 'oncethrough',
                    'RECIRCULATING TOWER': 'tower',
                    'RECIRCULATING POND': 'pond',
                    'ONCE-THROUGH SALINE': 'oncethrough'}

    # rename columns in power plant generation data file
    df = df.rename(columns={"Plant Id": "plant_code"})
    df = df.rename(columns={"AER\nFuel Type Code": "fuel_type"})
    df = df.rename(columns={"Reported\nPrime Mover": "prime_mover"})
    df = df.rename(columns={"Total Fuel Consumption\nMMBtu": "fuel_amt"})
    df = df.rename(columns={"Net Generation\n(Megawatthours)": "generation_mwh"})

    # changing string columns to numeric
    string_col = df.columns[3:]  # create list of string columns
    for col in string_col:
        df[col] = df[col].str.replace(r"[^\w ]", '', regex=True)  # replace any non alphanumeric values
        df[col] = df[col].astype(float)  # convert to float

    # removing power plant generation rows that should not be included
    df = df[df.plant_code != 99999]  # removing state level estimated differences rows

    # dropping power plants with zero fuel use and zero output
    index_list = df[(df['fuel_amt'] <= 0) & (df['generation_mwh'] <= 0)].index  # list of indices with both zero values
    df.drop(index_list, inplace=True)  # dropping rows with zero fuel and zero generation amount

    # using fuel type dictionary to bin fuel types
    df['fuel_type'] = df['fuel_type'].map(fuel_consumption_dict)  # bin fuel types

    # using prime_mover_dict to bin prime mover types
    df['prime_mover'] = df['prime_mover'].map(prime_mover_dict)  # bin fuel types

    # converting units to billion btu from million btu
    df["fuel_amt"] = df["fuel_amt"] / 1000

    # grouping rows by both plant code and fuel type
    df = df.groupby(['plant_code', 'fuel_type', 'prime_mover'], as_index=False).sum()

    # merging power plant location data with power plant generation data
    df = pd.merge(df, df_gen_loc, how='left', on='plant_code')

    # COOLING WATER DATA

    # estimate discharge location from source information
    df_cooling['OCEAN_DISCHARGE_MGD'] = np.where(df_cooling['NAME_OF_WATER_SOURCE'].str.contains('Ocean', regex=False),
                                                 df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
                                                 0)
    # gulf of mexico
    df_cooling['OCEAN_DISCHARGE_MGD'] = np.where(df_cooling['NAME_OF_WATER_SOURCE'].str.contains('Gulf', regex=False),
                                                 df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
                                                 df_cooling['OCEAN_DISCHARGE_MGD'])

    # only bays with saline water are ocean discharge (some bays are on lakes (e.g. Green Bay))
    df_cooling['OCEAN_DISCHARGE_MGD'] = np.where(df_cooling['NAME_OF_WATER_SOURCE'].str.contains('Gulf', regex=False) &
                                                 df_cooling['WATER_TYPE_CODE'] == "SA",
                                                 df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
                                                 df_cooling['OCEAN_DISCHARGE_MGD'])
    # harbors
    df_cooling['OCEAN_DISCHARGE_MGD'] = np.where(
        df_cooling['NAME_OF_WATER_SOURCE'].str.contains('Harbor', regex=False) &
        df_cooling['WATER_TYPE_CODE'] == "SA",
        df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
        df_cooling['OCEAN_DISCHARGE_MGD'])
    # channels
    df_cooling['OCEAN_DISCHARGE_MGD'] = np.where(
        df_cooling['NAME_OF_WATER_SOURCE'].str.contains('Channel', regex=False) &
        df_cooling['WATER_TYPE_CODE'] == "SA",
        df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
        df_cooling['OCEAN_DISCHARGE_MGD'])
    # sounds
    df_cooling['OCEAN_DISCHARGE_MGD'] = np.where(df_cooling['NAME_OF_WATER_SOURCE'].str.contains('Sound', regex=False) &
                                                 df_cooling['WATER_TYPE_CODE'] == "SA",
                                                 df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
                                                 df_cooling['OCEAN_DISCHARGE_MGD'])

    # all remaining discharge is to surface water
    df_cooling['SURFACE_DISCHARGE_MGD'] = np.where(df_cooling['OCEAN_DISCHARGE_MGD'] == 0,
                                                   df_cooling['WITHDRAWAL'] - df_cooling['CONSUMPTION'],
                                                   0)
    # Fix water source and type data
    # all surface water without a type is assumed to be fresh
    df_cooling['WATER_TYPE_CODE'] = np.where((df_cooling["WATER_SOURCE_CODE"] == "SW")
                                             & (df_cooling["WATER_TYPE_CODE"] == "-nr-"),
                                             "FR", df_cooling['WATER_TYPE_CODE'])

    # all groundwater without a type is assumed to be fresh
    df_cooling['WATER_TYPE_CODE'] = np.where((df_cooling["WATER_SOURCE_CODE"] == "GW")
                                             & (df_cooling["WATER_TYPE_CODE"] == "-nr-"),
                                             "FR", df_cooling['WATER_TYPE_CODE'])

    # apply dictionaries
    df_cooling['COOLING_TYPE'] = df_cooling['COOLING_TYPE'].map(cooling_dict)  # rename cooling types
    df_cooling['WATER_SOURCE_CODE'] = df_cooling['WATER_SOURCE_CODE'].map(water_source_dict)  # rename water sources
    df_cooling['WATER_TYPE_CODE'] = df_cooling['WATER_TYPE_CODE'].map(water_type_dict)  # rename water types
    df_cooling['WATER_TYPE_CODE'].fillna('fresh', inplace=True)
    df_cooling['WATER_SOURCE_CODE'].fillna('surfacewater', inplace=True)

    df_cooling = df_cooling[['EIA_PLANT_ID', 'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL',
                             'CONSUMPTION', 'SURFACE_DISCHARGE_MGD', 'OCEAN_DISCHARGE_MGD']]
    df_cooling = df_cooling.rename(columns={'EIA_PLANT_ID': 'plant_code'})
    #
    df = pd.merge(df, df_cooling, how='left', on='plant_code')

    no_cool_list = ['hydro', 'wind', 'solar']

    for item in no_cool_list:
        df["COOLING_TYPE"] = np.where(df['fuel_type'] == item, np.nan, df["COOLING_TYPE"])
    #
    ## splitting out fuel data into a separate dataframe and pivoting to get fuel (bbtu) as columns by type
    df_fuel = df[
        ["FIPS", "fuel_amt", "fuel_type", 'prime_mover', "COOLING_TYPE"]].copy()  # create a copy of fuel type data
    df_fuel['COOLING_TYPE'].fillna('nocooling', inplace=True)

    df_fuel["fuel_name"] = 'EGS_' + + df_fuel["fuel_type"] + '_' + df_fuel["prime_mover"] + '_' \
                           + df_fuel['COOLING_TYPE'] + '_total_bbtu_from_EPD_' + df_fuel["fuel_type"] \
                           + '_total_total_total_bbtu'

    # example: EGS_coal_stream_oncethrough_total_bbtu_from_EPD_coal_total_total_total_bbtu

    df_fuel = pd.pivot_table(df_fuel, values='fuel_amt', index=['FIPS'], columns=['fuel_name'], aggfunc=np.sum)  # pivot
    df_fuel = df_fuel.reset_index()  # reset index to remove multi-index from pivot table
    df_fuel = df_fuel.rename_axis(None, axis=1)  # drop index name
    df_fuel.fillna(0, inplace=True)  # fill nan with zero
    #
    ## splitting out generation data into a separate dataframe and pivoting to get generation (mwh) as columns by type
    df_gen = df[["FIPS", "generation_mwh", 'fuel_amt', 'prime_mover', "fuel_type",
                 'COOLING_TYPE']].copy()  # create a copy of generation data
    df_gen['COOLING_TYPE'].fillna('nocooling', inplace=True)
    df_gen['generation_mwh'] = df_gen['generation_mwh'].apply(convert_mwh_bbtu)  # convert to bbtu from mwh

    # calculate rejected energy fractions
    df_gen['rej_fraction'] = np.where(df_gen['fuel_amt'] > 0, df_gen['generation_mwh'] / df_gen['fuel_amt'], 0)

    df_gen["fuel_type_name"] = 'EGS_' + df_gen["fuel_type"] + '_' + df_gen["prime_mover"] + '_' \
                               + df_gen[
                                   'COOLING_TYPE'] + "_total_bbtu_to_REJ_total_total_total_total_bbtu_fraction"  # add naming
    #
    df_gen = pd.pivot_table(df_gen, values='rej_fraction', index=['FIPS'], columns=['fuel_type_name'], aggfunc=np.sum)
    df_gen = df_gen.reset_index()  # reset index to remove multi-index from pivot table
    df_gen = df_gen.rename_axis(None, axis=1)  # drop index name
    df_gen.fillna(0, inplace=True)  # fill nan with zero

    # create water intensity values

    # create water withdrawal source fractions
    df_cooling_int = df[["FIPS", 'plant_code', 'prime_mover', "generation_mwh", "fuel_type", 'COOLING_TYPE',
                         'WATER_TYPE_CODE', 'WATER_SOURCE_CODE', 'WITHDRAWAL']].copy()

    df_cooling_int["water_intensity_name"] = 'EGS_' + df['fuel_type'] + '_' + df['prime_mover'] + '_' \
                                             + df['COOLING_TYPE'] + '_total_mgd_from_EGS_' \
                                             + df['fuel_type'] + '_' + df['prime_mover'] + '_' \
                                             + df['COOLING_TYPE'] + '_total_bbtu_intensity'

    cooling_only = df_cooling_int[df_cooling_int.COOLING_TYPE != 'nocooling'].groupby('plant_code',
                                                                                      as_index=False).count()
    cooling_only = cooling_only.rename(columns={'FIPS': 'count'})
    cooling_only = cooling_only[['plant_code', 'count']]
    df_cooling_int = pd.merge(df_cooling_int, cooling_only, how='left', on='plant_code')
    df_cooling_int['count'].fillna(1, inplace=True)
    df_cooling_int = df_cooling_int.dropna(subset=["WITHDRAWAL"])
    df_cooling_int['WITHDRAWAL'] = df_cooling_int['WITHDRAWAL'] / df_cooling_int['count']

    df_cooling_int['generation_mwh'] = df_cooling_int['generation_mwh'].apply(
        convert_mwh_bbtu)  # convert to bbtu from mwh
    df_cooling_int['intensity'] = np.where(df_cooling_int['generation_mwh'] > 0,
                                           df_cooling_int['WITHDRAWAL'] / df_cooling_int['generation_mwh'],
                                           0)

    df_cooling_int = pd.pivot_table(df_cooling_int, values='intensity', index=['FIPS'],
                                    columns=['water_intensity_name'], aggfunc=np.mean)
    df_cooling_int = df_cooling_int.reset_index()  # reset index to remove multi-index from pivot table
    df_cooling_int = df_cooling_int.rename_axis(None, axis=1)  # drop index name
    df_cooling_int.fillna(0, inplace=True)  # fill nan with zero

    # create water withdrawal source fractions
    df_cooling_w = df[["FIPS", 'plant_code', 'prime_mover', "fuel_type", 'COOLING_TYPE',
                       'WATER_TYPE_CODE', 'WATER_SOURCE_CODE', 'WITHDRAWAL']].copy()

    df_cooling_w["water_withdrawal_name"] = 'EGS_' + df['fuel_type'] + '_' + df['prime_mover'] + '_' \
                                            + df['COOLING_TYPE'] + '_total_mgd_from_WSW_' \
                                            + df_cooling_w["WATER_TYPE_CODE"] + '_' + df_cooling_w["WATER_SOURCE_CODE"] \
                                            + '_total_total_mgd_fraction'

    cooling_only = df_cooling_w[df_cooling_w.COOLING_TYPE != 'nocooling'].groupby('plant_code', as_index=False).count()
    cooling_only = cooling_only.rename(columns={'FIPS': 'count'})
    cooling_only = cooling_only[['plant_code', 'count']]
    df_cooling_w = pd.merge(df_cooling_w, cooling_only, how='left', on='plant_code')
    df_cooling_w['count'].fillna(1, inplace=True)
    df_cooling_w = df_cooling_w.dropna(subset=["WITHDRAWAL"])
    df_cooling_w['WITHDRAWAL'] = df_cooling_w['WITHDRAWAL'] / df_cooling_w['count']

    # convert withdrawal to value of 1 to be 100% fraction of source
    df_cooling_w['WITHDRAWAL'] = np.where(df_cooling_w['WITHDRAWAL'] > 0, 1, 0)

    df_cooling_w = pd.pivot_table(df_cooling_w, values='WITHDRAWAL', index=['FIPS'],
                                  columns=['water_withdrawal_name'], aggfunc=np.mean)
    df_cooling_w = df_cooling_w.reset_index()  # reset index to remove multi-index from pivot table
    df_cooling_w = df_cooling_w.rename_axis(None, axis=1)  # drop index name
    df_cooling_w.fillna(0, inplace=True)  # fill nan with zero

    # create consumption fractions
    df_cooling_c = df[
        ["FIPS", 'plant_code', 'prime_mover', "fuel_type", 'COOLING_TYPE', 'WATER_TYPE_CODE', 'WATER_SOURCE_CODE',
         'CONSUMPTION', 'WITHDRAWAL']].copy()
    df_cooling_c["water_consumption_name"] = 'EGS_' + df['fuel_type'] + '_' + df['prime_mover'] + '_' \
                                             + df[
                                                 'COOLING_TYPE'] + '_total_mgd_to_CMP_total_total_total_total_mgd_fraction'

    df_cooling_c = pd.merge(df_cooling_c, cooling_only, how='left', on='plant_code')
    df_cooling_c['count'].fillna(1, inplace=True)
    df_cooling_c = df_cooling_c.dropna(subset=["CONSUMPTION"])
    df_cooling_c['CONSUMPTION'] = df_cooling_c['CONSUMPTION'] / df_cooling_c['count']

    df_cooling_c['cons_fraction'] = df_cooling_c['CONSUMPTION'] / df_cooling_c['WITHDRAWAL']

    df_cooling_c = pd.pivot_table(df_cooling_c, values='cons_fraction', index=['FIPS'],
                                  columns=['water_consumption_name'],
                                  aggfunc=np.mean)
    df_cooling_c = df_cooling_c.reset_index()  # reset index to remove multi-index from pivot table
    df_cooling_c = df_cooling_c.rename_axis(None, axis=1)  # drop index name
    df_cooling_c.fillna(0, inplace=True)  # fill nan with zero

    # surface discharge fraction
    df_cooling_sd = df[
        ["FIPS", 'plant_code', 'prime_mover', "fuel_type", 'COOLING_TYPE', 'WATER_TYPE_CODE', 'WATER_SOURCE_CODE',
         'SURFACE_DISCHARGE_MGD', 'WITHDRAWAL']].copy()
    df_cooling_sd["sd_name"] = 'EGS_' + df['fuel_type'] + '_' + df['prime_mover'] + '_' \
                               + df['COOLING_TYPE'] + '_total_mgd_to_SRD_total_total_total_total_mgd_fraction'

    df_cooling_sd = pd.merge(df_cooling_sd, cooling_only, how='left', on='plant_code')
    df_cooling_sd['count'].fillna(1, inplace=True)
    df_cooling_sd = df_cooling_sd.dropna(subset=["SURFACE_DISCHARGE_MGD"])
    df_cooling_sd['SURFACE_DISCHARGE_MGD'] = df_cooling_sd['SURFACE_DISCHARGE_MGD'] / df_cooling_sd['count']

    df_cooling_sd['sd_fraction'] = df_cooling_sd['SURFACE_DISCHARGE_MGD'] / df_cooling_sd['WITHDRAWAL']

    df_cooling_sd = pd.pivot_table(df_cooling_sd, values='sd_fraction', index=['FIPS'], columns=['sd_name'],
                                   aggfunc=np.sum)
    df_cooling_sd = df_cooling_sd.reset_index()  # reset index to remove multi-index from pivot table
    df_cooling_sd = df_cooling_sd.rename_axis(None, axis=1)  # drop index name
    df_cooling_sd.fillna(0, inplace=True)  # fill nan with zero

    # ocean discharge fractions
    df_cooling_od = df[
        ["FIPS", 'plant_code', 'prime_mover', "fuel_type", 'COOLING_TYPE', 'WATER_TYPE_CODE', 'WATER_SOURCE_CODE',
         'OCEAN_DISCHARGE_MGD', 'WITHDRAWAL']].copy()
    df_cooling_od["od_name"] = 'EGS_' + df['fuel_type'] + '_' + df['prime_mover'] + '_' \
                               + df['COOLING_TYPE'] + '_total_mgd_to_OCD_total_total_total_total_mgd_fraction'

    df_cooling_od = pd.merge(df_cooling_od, cooling_only, how='left', on='plant_code')
    df_cooling_od['count'].fillna(1, inplace=True)
    df_cooling_od = df_cooling_od.dropna(subset=["OCEAN_DISCHARGE_MGD"])
    df_cooling_od['OCEAN_DISCHARGE_MGD'] = df_cooling_od['OCEAN_DISCHARGE_MGD'] / df_cooling_od['count']

    df_cooling_od['od_fraction'] = df_cooling_od['OCEAN_DISCHARGE_MGD'] / df_cooling_od['WITHDRAWAL']

    df_cooling_od = pd.pivot_table(df_cooling_od, values='OCEAN_DISCHARGE_MGD', index=['FIPS'], columns=['od_name'],
                                   aggfunc=np.sum)
    df_cooling_od = df_cooling_od.reset_index()  # reset index to remove multi-index from pivot table
    df_cooling_od = df_cooling_od.rename_axis(None, axis=1)  # drop index name
    df_cooling_od.fillna(0, inplace=True)  # fill nan with zero

    # merge dataframes
    df_fuel = pd.merge(df_loc, df_fuel, how='left', on='FIPS').fillna(0)
    df_gen = pd.merge(df_loc, df_gen, how='left', on='FIPS').fillna(0)
    df_cooling_int = pd.merge(df_loc, df_cooling_int, how='left', on='FIPS').fillna(0)
    df_cooling_w = pd.merge(df_loc, df_cooling_w, how='left', on='FIPS').fillna(0)
    df_cooling_c = pd.merge(df_loc, df_cooling_c, how='left', on='FIPS').fillna(0)
    df_cooling_sd = pd.merge(df_loc, df_cooling_sd, how='left', on='FIPS').fillna(0)
    df_cooling_od = pd.merge(df_loc, df_cooling_od, how='left', on='FIPS').fillna(0)

    # rem_list = [df_cooling_w, df_cooling_c, df_cooling_sd, df_cooling_od]
    out_df = pd.merge(df_fuel, df_gen, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, df_cooling_int, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, df_cooling_w, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, df_cooling_c, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, df_cooling_sd, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, df_cooling_od, how='left', on=['FIPS', 'State', 'County'])

    return out_df


def prep_irrigation_fuel_data() -> pd.DataFrame:
    """prepping irrigation data so that the outcome is a dataframe showing the percent of total acres of irrigation
    that use each type of fuel for pumping (electricity, natural gas, propane, diesel, and other gas). This dataframe
    is used to calculate the total electricity and fuels to irrigation based on total water flows in irrigation.

    :return:                DataFrame of percent of total irrigation using specified fuel type for pumping by county

    """

    # read in irrigation pumping dataset
    data = 'input_data/FRIS2013tab8.csv'
    df = pd.read_csv(data, skiprows=3)

    # read in FIPS codes and states from 2015 water dataset
    df_loc = prep_water_use_2015()

    # determine percent of irrigated acres that use each pump type (electricity, diesel, natural gas, or propane)
    col_list = df.columns[4:]  # list of pump fuel type columns
    df['total_Irr'] = df[col_list].sum(axis=1)  # calculate sum of fuel type columns
    for col in col_list:
        df[col] = (df[col] / df['total_Irr'])  # determine percent of total acres irrigated for each fuel type

    # calculate the mean percent across all states in dataset
    elec_avg = df['electricity_pumping'].mean(axis=0)  # electricity
    ng_avg = df['ng_pumping'].mean(axis=0)  # natural gas
    prop_avg = df['propane_pumping'].mean(axis=0)  # propane
    diesel_avg = df['diesel_pumping'].mean(axis=0)  # diesel
    other_avg = df['gas_pumping'].mean(axis=0)  # other gas

    # reducing dataframe to required variables
    df = df[['State', 'electricity_pumping', 'ng_pumping', 'propane_pumping',
             'diesel_pumping', 'gas_pumping']]

    # merge with county data to distribute value to each county in a state
    df = pd.merge(df_loc, df, how='left', on='State')

    # filling states that were not in the irrigation dataset with the average for each fuel type
    df['electricity_pumping'].fillna(elec_avg, inplace=True)
    df['ng_pumping'].fillna(ng_avg, inplace=True)
    df['propane_pumping'].fillna(prop_avg, inplace=True)
    df['diesel_pumping'].fillna(diesel_avg, inplace=True)
    df['gas_pumping'].fillna(other_avg, inplace=True)

    # bin similar fuel types
    df['petroleum_pumping'] = df['propane_pumping'] + df['diesel_pumping']
    df['natural_gas_pumping'] = df['ng_pumping'] + df['gas_pumping']

    # keep only required columns
    df_out = df.drop(["gas_pumping", "propane_pumping", "diesel_pumping", 'ng_pumping'], axis=1)

    df_out['ACI_pumping_fresh_surfacewater_total_bbtu_from_EPD_natgas_total_total_total_bbtu_fraction'] = df[
        'natural_gas_pumping']
    df_out['ACI_pumping_fresh_groundwater_total_bbtu_from_EPD_natgas_total_total_total_bbtu_fraction'] = df[
        'natural_gas_pumping']
    df_out['ACI_pumping_fresh_surfacewater_total_bbtu_from_EPD_petroleum_total_total_total_bbtu_fraction'] = df[
        'petroleum_pumping']
    df_out['ACI_pumping_fresh_groundwater_total_bbtu_from_EPD_petroleum_total_total_total_bbtu_fraction'] = df[
        'petroleum_pumping']
    df_out['ACI_pumping_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = df[
        'electricity_pumping']
    df_out['ACI_pumping_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = df[
        'electricity_pumping']

    df_out['AGI_pumping_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['AGI_pumping_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['AAQ_pumping_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['AAQ_pumping_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['AAQ_pumping_saline_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['AAQ_pumping_saline_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['ALV_pumping_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['ALV_pumping_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1

    # public water supply
    df_out['PWS_pumping_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['PWS_pumping_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['PWS_treatment_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['PWS_treatment_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['PWS_distribution_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['PWS_distribution_fresh_groundwater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1
    df_out['PWS_ibt_fresh_surfacewater_total_bbtu_from_EGD_total_total_total_total_bbtu_fraction'] = 1

    df_out = df_out.drop(["natural_gas_pumping", "petroleum_pumping", "electricity_pumping"], axis=1)

    return df_out


def prep_pumping_intensity_data() -> pd.DataFrame:
    """Prepares irrigation data so that the outcome is a dataframe of groundwater and surface water pumping energy
    intensities (billion BTU per million gallons) by county. For groundwater pumping intensity, The total differential
    height is calculated as the sum of the average well depth and the pressurization head. The pressure data is provided
    in pounds per square inch (psi). This is converted to feet using a coefficient of 2.31. This analysis also follows
    the assumption that average well depth is used instead of depth to water to counteract some of the
    undocumented friction that would occur in the pumping process. Surface water pumping intensity follows the same
    methodology as groundwater pumping intensity except the total differential height has a value of zero for well
    depth.

    :return:                DataFrame of irrigation surface and groundwater pumping intensity per county

    """

    # read in irrigation well depth, pressure, and pump fuel type data
    data = 'input_data/FRIS2013tab8.csv'
    df = pd.read_csv(data, skiprows=3)
    df = df[['State', 'average_well_depth_ft', 'average_operating_pressure_psi']]

    # read in FIPS codes and states from 2015 water dataset
    df_loc = prep_water_use_2015()

    # establish variables
    acc_gravity = 9.81  # Acceleration of gravity  (m/s^2)
    water_density = 997  # Water density (kg/m^3)
    ag_pump_eff = .65  # assumed pump efficiency rate
    psi_psf_conversion = 2.31  # conversion of pounds per square inch (psi) to pounds per square foot (psf)
    m3_mg_conversion = 3785.41178  # conversion factor for m^3 to million gallons
    joules_kwh_conversion = 1 / 3600000  # conversion factor from joules to kWh
    kwh_bbtu_conversion = 3412.1416416 / 1000000000  # 1 kWh is equal to 3412.1416416 btu
    meter_ft_conversion = 0.3048  # meters in a foot

    # determine groundwater pumping intensity by state
    head_ft = psi_psf_conversion * df["average_operating_pressure_psi"]  # conversion of psi to head (pounds per sqft)
    diff_height_gw = meter_ft_conversion * (df["average_well_depth_ft"] + head_ft)  # calc. differential height (m)
    pump_power_gw = (water_density * diff_height_gw * acc_gravity * m3_mg_conversion) / ag_pump_eff  # joules/MG
    df[
        'groundwater_pumping_bbtu_per_mg'] = pump_power_gw * joules_kwh_conversion * kwh_bbtu_conversion  # power intensity (bbtu/mg)

    # calculating average groundwater pumping to apply to regions without values
    groundwater_pumping_bbtu_per_mg_avg = df['groundwater_pumping_bbtu_per_mg'].mean()

    # determine surface water pumping intensity by state
    diff_height_sw = meter_ft_conversion * head_ft  # calc. differential height (m)
    pump_power_sw = (water_density * diff_height_sw * acc_gravity * m3_mg_conversion) / ag_pump_eff  # joules/MG
    df[
        'surface_water_pumping_bbtu_per_mg'] = pump_power_sw * joules_kwh_conversion * kwh_bbtu_conversion  # power intensity (bbtu/mg)

    # calculating average surface water pumping to apply to regions without values
    surface_water_pumping_bbtu_per_mg_avg = df['surface_water_pumping_bbtu_per_mg'].mean()

    # reducing dataframe to required variables
    df = df[['State', 'groundwater_pumping_bbtu_per_mg', 'surface_water_pumping_bbtu_per_mg']]

    # merge with county data to distribute value to each county in a state
    df = pd.merge(df_loc, df, how='left', on='State')

    # filling states that were not in the irrigation dataset with the average for each fuel type
    df['groundwater_pumping_bbtu_per_mg'].fillna(groundwater_pumping_bbtu_per_mg_avg,
                                                 inplace=True)  # groundwater intensity
    df['surface_water_pumping_bbtu_per_mg'].fillna(surface_water_pumping_bbtu_per_mg_avg, inplace=True)

    # add column for wastewater pumping
    df['wastewater_pumping_bbtu_per_mg'] = df['surface_water_pumping_bbtu_per_mg']

    out_df = df_loc

    sw_var_list = [
        'ACI_pumping_fresh_surfacewater_total_bbtu_from_ACI_fresh_surfacewater_withdrawal_total_mgd_intensity',
        'AGI_pumping_fresh_surfacewater_total_bbtu_from_AGI_fresh_surfacewater_withdrawal_total_mgd_intensity',
        'AAQ_pumping_fresh_surfacewater_total_bbtu_from_AAQ_fresh_surfacewater_withdrawal_total_mgd_intensity',
        'AAQ_pumping_saline_surfacewater_total_bbtu_from_AAQ_saline_surfacewater_withdrawal_total_mgd_intensity',
        'ALV_pumping_fresh_surfacewater_total_bbtu_from_ALV_fresh_surfacewater_withdrawal_total_mgd_intensity',
        'PWS_pumping_fresh_surfacewater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity',
        'PWS_pumping_saline_surfacewater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity',
    ]

    gw_var_list = [
        'ACI_pumping_fresh_groundwater_total_bbtu_from_ACI_fresh_groundwater_withdrawal_total_mgd_intensity',
        'AGI_pumping_fresh_groundwater_total_bbtu_from_AGI_fresh_groundwater_withdrawal_total_mgd_intensity',
        'AAQ_pumping_fresh_groundwater_total_bbtu_from_AAQ_fresh_groundwater_withdrawal_total_mgd_intensity',
        'AAQ_pumping_saline_groundwater_total_bbtu_from_AAQ_saline_groundwater_withdrawal_total_mgd_intensity',
        'ALV_pumping_fresh_groundwater_total_bbtu_from_ALV_fresh_groundwater_withdrawal_total_mgd_intensity',
        'PWS_pumping_fresh_groundwater_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity',
        'PWS_pumping_saline_groundwater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity',
    ]

    for sw in sw_var_list:
        out_df[sw] = df['surface_water_pumping_bbtu_per_mg']

    for gw in gw_var_list:
        out_df[gw] = df['groundwater_pumping_bbtu_per_mg']

    # create variables for pws treatment and distribution intensity variables

    fgw_treat = convert_kwh_bbtu(205)
    fsw_treat = convert_kwh_bbtu(405)
    sgw_treat = convert_kwh_bbtu(13805)
    ssw_treat = convert_kwh_bbtu(14005)
    dist = convert_kwh_bbtu(1040)

    out_df[
        'PWS_treatment_fresh_groundwater_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity'] = fgw_treat
    out_df[
        'PWS_treatment_fresh_surfacewater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity'] = fsw_treat
    out_df[
        'PWS_treatment_saline_groundwater_total_bbtu_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'] = sgw_treat
    out_df[
        'PWS_treatment_saline_surfacewater_total_bbtu_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity'] = ssw_treat

    out_df['PWS_distribution_total_total_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity'] = dist
    out_df['PWS_distribution_total_total_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity'] = dist
    out_df['PWS_distribution_total_total_total_bbtu_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity'] = dist
    out_df['PWS_distribution_total_total_total_bbtu_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'] = dist

    return out_df


def combine_data():
    x1 = prep_water_use_2015(all_variables=True)
    x2 = calc_pws_deliveries()
    x3 = prep_pws_to_pwd()
    x4 = calc_discharge_fractions()
    x5 = calc_hydro_water_intensity()
    x6 = prep_wastewater_data()
    x7 = prep_electricity_generation()
    x8 = prep_irrigation_fuel_data()
    x9 = prep_pumping_intensity_data()
    x10 =recalc_irrigation_consumption()

    x1 = x1.drop(['population', 'fresh_groundwater_total_irrigation_mgd', 'fresh_surfacewater_total_irrigation_mgd',
                  'fresh_wastewater_total_irrigation_mgd', 'golf_irrigation_fresh_consumption_mgd',
                  'crop_irrigation_fresh_consumption_mgd', 'total_irrigation_fresh_consumption',
                  'total_pws_withdrawals_mgd', 'fresh_groundwater_thermoelectric_mgd',
                  'saline_groundwater_thermoelectric_mgd', 'fresh_surfacewater_thermoelectric_mgd',
                  'saline_surfacewater_thermoelectric_mgd', 'wastewater_thermoelectric_mgd',
                  'fresh_pws_thermoelectric_mgd', 'total_irrigation_consumption_fraction',
                  'ACI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                  'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                  'ACI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                  'AGI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                  'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
                  'AGI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction'
                  ], axis=1)

    out_df = pd.merge(x1, x2, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x3, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x4, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x5, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x6, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x7, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x8, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x9, how='left', on=['FIPS', 'State', 'County'])
    out_df = pd.merge(out_df, x10, how='left', on=['FIPS', 'State', 'County'])

    out_df = out_df[out_df.State == 'CA']


    value_columns = out_df.columns[3:].to_list()
    out_df = pd.melt(out_df, value_vars=value_columns, var_name='flow_name', value_name='value', id_vars=['FIPS'])
    out_df = out_df[out_df.value > 0]

    i = out_df.columns.get_loc('flow_name')
    df2 = out_df['flow_name'].str.split("_", expand=True)
    out_df = pd.concat([out_df.iloc[:, :i], df2, out_df.iloc[:, i + 1:]], axis=1)

    col = ['FIPS', 't1', 't2', 't3', 't4', 't5', 'T_unit', 'to', 's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value']
    out_df.columns = col

    out_df['parameter'].fillna('flow_value', inplace=True)
    out_df['type'] = np.where(out_df['parameter'] == 'flow_value', 'A_collect', np.nan)
    out_df['type'] = np.where(out_df['parameter'] == 'intensity', 'B_calculate', out_df['type'])
    out_df['type'] = np.where((out_df['to'] == 'from')& (out_df['parameter'] == 'fraction'), 'C_source', out_df['type'])
    out_df['type'] = np.where((out_df['to'] == 'to') & (out_df['parameter'] == 'fraction'), 'D_discharge', out_df['type'])

    out_df = out_df.sort_values(by=['FIPS', 'type', 't1', 't2', 't3', 't4', 't5'])

    out_df = out_df[['FIPS','type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
               's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value']]
    return out_df


x = combine_data()
# for col in x.columns:
#    print(col)
x.to_csv(r"C:\Users\mong275\Local Files\Repos\flow\sample_data\test_output.csv", index=False)
import os

os.startfile(r"C:\Users\mong275\Local Files\Repos\flow\sample_data\test_output.csv")

# TODO START HERE


# READER

# def get_irrigation_data():
#
#
#
# def get_tx_inter_basin_transfer_data():
#    data = pkg_resources.resource_filename('flow', 'data/TX_IBT_2015.csv')
#
#    # read in Texas inter-basin transfer data by FIPS
#    return pd.read_csv(data, dtype={'Used_FIPS': str, 'Source_FIPS': str})
#
#
# def get_west_inter_basin_transfer_data():
#    data = pkg_resources.resource_filename('flow', 'data/West_IBT_county.csv')
#
#    # read in Texas inter-basin transfer data by FIPS
#    return pd.read_csv(data, dtype={'FIPS': str})
#
#
# def get_residential_electricity_demand_data():
#    data = pkg_resources.resource_filename('flow', 'data/EIA_table6_Res.csv')
#
#    # read in residential electricity sales data
#    return pd.read_csv(data, skiprows=2)
#
#
# def get_commercial_electricity_demand_data():
#    data = pkg_resources.resource_filename('flow', 'data/EIA_table7_Com.csv')
#
#    # read in commercial electricity sales data
#    return pd.read_csv(data, skiprows=2)
#
#
# def get_industrial_electricity_demand_data():
#    data = pkg_resources.resource_filename('flow', 'data/EIA_table8_Ind.csv')
#
#    # read in industrial electricity sales data
#    return pd.read_csv(data, skiprows=2)
#
#
# def get_transportation_electricity_demand_data():
#    data = pkg_resources.resource_filename('flow', 'data/EIA_table9_Trans.csv')
#
#    # read in transportation electricity sales data
#    return pd.read_csv(data, skiprows=2)
#
#
# def get_state_electricity_demand_data():
#    data = pkg_resources.resource_filename('flow', 'data/eia_861m_states.csv')
#
#    # read in transportation electricity sales data
#    return pd.read_csv(data, skipfooter=2, engine='python',
#                       dtype={'RESIDENTIAL': float, 'COMMERCIAL': float,
#                              'INDUSTRIAL': float, 'TRANSPORTATION': float})
#
#
# def get_fuel_demand_data():
#    data = pkg_resources.resource_filename('flow', 'data/use_all_btu.csv')
#
#    # read in energy production (fuel) data
#    return pd.read_csv(data)
#
#
# def get_energy_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/eia_SEDS_Prod_dataset.csv')
#
#    # read in energy production (fuel) data
#    return pd.read_csv(data, skiprows=1)
#
#
# def get_corn_irrigation_data():
#    data = pkg_resources.resource_filename('flow', 'data/USDA_FRIS.csv')
#
#    # read in corn irrigation data
#    return pd.read_csv(data)
#
#
# def get_corn_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/USDA_NASS_CornProd_2015.csv')
#
#    # read in corn irrigation data
#    return pd.read_csv(data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})
#
#
# def get_county_oil_gas_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/oilgascounty.csv')
#
#    # read in county level oil and gas production data
#    return pd.read_csv(data, dtype={'geoid': str})
#
#
# def get_state_petroleum_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/petroleum_eia.csv')
#
#    # read in state level petroleum production data
#    return pd.read_csv(data, skiprows=4)
#
#
# def get_state_gas_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/natgas_eia.csv')
#
#    # read in read in state level natural gas production data
#    return pd.read_csv(data, skiprows=4)
#
#
# def get_unconventional_oil_gas_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/Unconventional_Oil_NG_State.csv')
#
#    # read in read in state level unconventional natural gas and oil production data
#    return pd.read_csv(data)
#
#
# def get_conventional_oil_water_intensity_data():
#    data = pkg_resources.resource_filename('flow', 'data/PADD_intensity.csv')
#
#    # read in read in state level water to oil intensity data
#    return pd.read_csv(data)
#
#
# def get_oil_gas_discharge_data():
#    data = pkg_resources.resource_filename('flow', 'data/Oil_NG_WOR_WGR.csv')
#
#    # read in read in state level water discharge data from oil and natural gas
#    return pd.read_csv(data)
#
#
# def get_coal_production_data():
#    data = pkg_resources.resource_filename('flow', 'data/coalpublic2015.csv')
#
#    # read in read in coal production data
#    return pd.read_csv(data, skiprows=3)
#
#
# def get_coal_mine_location_data():
#    data = pkg_resources.resource_filename('flow', 'data/Coal_Mine_Loc.csv')
#
#    # read in read in coal mine data
#    return pd.read_csv(data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])
#
#
# def get_state_fips_data():
#    data = pkg_resources.resource_filename('flow', 'data/State_FIPS_Code.csv')
#
#    # read in read in state fips code to state abbrev. data
#    return pd.read_csv(data, dtype={'State_FIPS': str})
#
#
# def get_ethanol_location_data():
#    data = pkg_resources.resource_filename('flow', 'data/eia819_ethanolcapacity_2015.csv')
#
#    # read in read in state fips code to state abbrev. data
#    return pd.read_csv(data, dtype={'FIPS': str}, skiprows=1)
