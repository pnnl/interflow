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
x = prep_water_use_2015(all_variables=True)
x.to_csv('test_output.csv')
