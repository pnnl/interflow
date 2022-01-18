import numpy as np
import pandas as pd

from .calculate import *
from .reader import *


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
    df = get_water_use_2015()  # USGS water use data for 2015 in million gallons per day (mgd) by county

    # replacing characters for missing USGS data with value of zero
    df.replace("--", 0, inplace=True)

    # creating a dictionary of required variables from full dataset with descriptive naming
    variables_dict = {'FIPS': 'FIPS',
                      'STATE': 'State',
                      'COUNTY': 'County',
                      'TP-TotPop': 'population',
                      'PS-WGWFr': 'fresh_groundwater_pws_mgd',
                      'PS-WSWFr': 'fresh_surfacewater_pws_mgd',
                      'PS-WGWSa': 'saline_groundwater_pws_mgd',
                      'PS-WSWSa': 'saline_surfacewater_pws_mgd',
                      'DO-PSDel': 'fresh_pws_residential_mgd',
                      'PS-Wtotl': 'total_pws_withdrawals_mgd',

                      'DO-WGWFr': 'fresh_groundwater_residential_mgd',
                      'DO-WSWFr': 'fresh_surfacewater_residential_mgd',

                      'PT-WGWFr': 'fresh_groundwater_thermoelectric_mgd',
                      'PT-WGWSa': 'saline_groundwater_thermoelectric_mgd',
                      'PT-WSWFr': 'fresh_surfacewater_thermoelectric_mgd',
                      'PT-WSWSa': 'saline_surfacewater_thermoelectric_mgd',
                      'PT-RecWW': 'wastewater_thermoelectric_mgd',
                      'PT-PSDel': 'fresh_pws_thermoelectric_mgd',
                      # TODO see if consumptive use for thermoelectric is split out by fresh/surface
                      'PT-CUTot': 'thermoelectric_fresh_consumption_mgd',

                      'IN-WGWFr': 'fresh_groundwater_industrial_mgd',
                      'IN-WSWFr': 'fresh_surfacewater_industrial_mgd',
                      'IN-WGWSa': 'saline_groundwater_industrial_mgd',
                      'IN-WSWSa': 'saline_surfacewater_industrial_mgd',

                      'MI-WGWFr': 'fresh_groundwater_mining_mgd',
                      'MI-WSWFr': 'fresh_surfacewater_mining_mgd',
                      'MI-WGWSa': 'saline_groundwater_mining_mgd',
                      'MI-WSWSa': 'saline_surfacewater_mining_mgd',

                      'IR-WGWFr': 'fresh_groundwater_total_irrigation_mgd',
                      'IR-WSWFr': 'fresh_surfacewater_total_irrigation_mgd',
                      'IR-RecWW': 'fresh_wastewater_total_irrigation_mgd',
                      'IR-CUsFr': 'total_irrigation_fresh_consumption',
                      'IC-WGWFr': 'fresh_groundwater_crop_irrigation_mgd',
                      'IC-WSWFr': 'fresh_surfacewater_crop_irrigation_mgd',
                      'IC-RecWW': 'fresh_wastewater_crop_irrigation_mgd',
                      'IC-CUsFr': 'crop_irrigation_fresh_consumption_mgd',

                      'IG-WGWFr': 'fresh_groundwater_golf_irrigation_mgd',
                      'IG-WSWFr': 'fresh_surfacewater_golf_irrigation_mgd',
                      'IG-RecWW': 'fresh_wastewater_golf_irrigation_mgd',
                      'IG-CUsFr': 'golf_irrigation_fresh_consumption_mgd',
                      'LI-WGWFr': 'fresh_groundwater_livestock_mgd',
                      'LI-WSWFr': 'fresh_surfacewater_livestock_mgd',
                      'AQ-WGWFr': 'fresh_groundwater_aquaculture_mgd',
                      'AQ-WGWSa': 'saline_groundwater_aquaculture_mgd',
                      'AQ-WSWFr': 'fresh_surfacewater_aquaculture_mgd',
                      'AQ-WSWSa': 'saline_surfacewater_aquaculture_mgd'
                      }
    df = df[variables_dict]

    state_irrigation_adj_list = ['AR', 'HI', 'LA', 'MS', 'MO', 'MT', 'NE', 'NJ', 'ND',
                                 'OK', 'SD', 'TX', 'WI', 'WY', 'PR', 'VI']
    for state in state_irrigation_adj_list:
        df['IC-WGWFr'] = np.where(df['STATE'] == state, df['IR-WGWFr'], df['IC-WGWFr'])
        df['IC-WSWFr'] = np.where(df['STATE'] == state, df['IR-WSWFr'], df['IC-WSWFr'])
        df['IC-RecWW'] = np.where(df['STATE'] == state, df['IR-RecWW'], df['IC-RecWW'])
        df['IC-CUsFr'] = np.where(df['STATE'] == state, df['IR-CUsFr'], df['IC-CUsFr'])

    # convert all columns that should be numerical to floats
    numerical_list = list(variables_dict.keys())[3:]  # create a list of columns beyond geographic identifier columns
    for col in numerical_list:  # convert columns to float
        df[col] = df[col].astype(float)

    # rename columns to add descriptive language
    df.rename(columns=variables_dict, inplace=True)

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
    """prepping 1995 water use data by replacing missing values, fixing FIPS codes,
     and reducing to needed variables

    :return:                DataFrame of a number of water values for 1995 at the county level

    """

    # read in data
    df = get_water_use_1995()  # 1995 USGS water use estimates

    # create a complete state + coutny FIPS code from the sum of the state and county level FIPS codes
    df["FIPS"] = df["StateCode"] + df["CountyCode"]

    # address FIPS code changes between 1995 and 2015
    df['FIPS'] = np.where(df['FIPS'] == "12025", "12086", df['FIPS'])  # Miami-Dade County, FL
    df['FIPS'] = np.where(df['FIPS'] == "46113", "46102", df['FIPS'])  # Oglala Lakota County, SD
    df['FIPS'] = np.where(df['FIPS'] == "02232", "02105", df['FIPS'])  # Hoonah-Angoon Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "02270", "02158", df['FIPS'])  # Kusilvak Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "02280", "02195", df['FIPS'])  # Petersburg Borough, AK
    df['FIPS'] = np.where(df['FIPS'] == "02201", "02198", df['FIPS'])  # Wales-Hyder Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "78001", "78010", df['FIPS'])  # St. Croix County, VI
    df['FIPS'] = np.where(df['FIPS'] == "78003", "78020", df['FIPS'])  # St. John County, VI
    df['FIPS'] = np.where(df['FIPS'] == "78004", "78030", df['FIPS'])  # St. Thomas County, VI

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


def prep_consumption_fraction() -> pd.DataFrame:
    """prepping water consumption fractions by sector to apply to 2015 water values.

    :return:                DataFrame of a number of consumption fractions by sector

    """

    # read in data
    df = prep_water_use_1995(variables=['FIPS', 'DO-CUTot', 'DO-WDelv', 'CO-CUTot', 'CO-WDelv', 'IN-CUsFr',
                                        'IN-WFrTo', 'IN-PSDel', 'IN-CUsSa', "IN-WSaTo", "MI-CUsFr",
                                        "MI-WFrTo", "MI-CUsSa", "MI-WSaTo", "LV-CUTot", "LV-WTotl",
                                        "LA-CUTot", "LA-WTotl"])
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # calculate water consumption fractions as consumptive use divided by delivered water
    df["DO_CF_Fr"] = df["DO-CUTot"] / df["DO-WDelv"]  # residential (domestic) sector freshwater consumption fraction
    df["CO_CF_Fr"] = df["CO-CUTot"] / df["CO-WDelv"]  # commercial sector freshwater consumption fraction
    df["IN_CF_Fr"] = df["IN-CUsFr"] / (df["IN-WFrTo"] + df["IN-PSDel"])  # ind sector freshwater consumption fraction
    df["IN_CF_Sa"] = df["IN-CUsSa"] / df["IN-WSaTo"]  # industrial sector saline water consumption fraction
    df["MI_CF_Fr"] = df["MI-CUsFr"] / df["MI-WFrTo"]  # mining sector freshwater consumption fraction
    df["MI_CF_Sa"] = df["MI-CUsSa"] / df["MI-WSaTo"]  # mining sector saline water consumption fraction
    df["LV_CF_Fr"] = df["LV-CUTot"] / df["LV-WTotl"]  # livestock freshwater water consumption fraction
    df["LA_CF_Fr"] = df["LA-CUTot"] / df["LA-WTotl"]  # aquaculture freshwater water consumption fraction

    # Replacing infinite (from divide by zero) with with 0
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    # creating a dictionary of required variables from full dataset with descriptive naming
    variables_list_1995 = {"FIPS": 'FIPS',
                           "DO_CF_Fr": "residential_fresh_surfacewater_consumption_fraction",
                           "CO_CF_Fr": "commercial_fresh_surfacewater_consumption_fraction",
                           "IN_CF_Fr": "industrial_fresh_surfacewater_consumption_fraction",
                           "IN_CF_Sa": "industrial_saline_surfacewater_consumption_fraction",
                           "MI_CF_Fr": "mining_fresh_surfacewater_consumption_fraction",
                           "MI_CF_Sa": "mining_saline_surfacewater_consumption_fraction",
                           "LV_CF_Fr": "livestock_fresh_surfacewater_consumption_fraction",
                           "LA_CF_Fr": "aquaculture_fresh_surfacewater_consumption_fraction"
                           }

    # reduce full dataframe to required variable list
    df = df[variables_list_1995]

    # rename columns to add descriptive language
    df.rename(columns=variables_list_1995, inplace=True)

    sector_list = ['residential', 'commercial', 'industrial', 'mining']
    water_type_list = ['fresh', 'saline']
    water_source_list = ['groundwater', 'pws']

    for sector in sector_list:
        for water_type in water_type_list:
            for water_source in water_source_list:
                water_consumption_name = f'{sector}_{water_type}_surfacewater_consumption_fraction'
                if water_consumption_name in df.columns:
                    df[f'{sector}_{water_type}_{water_source}_consumption_fraction'] = df[water_consumption_name]

    df = df.drop(['mining_fresh_pws_consumption_fraction', 'mining_saline_pws_consumption_fraction'], axis=1)

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on='FIPS')

    return df


def prep_hydroelectric_water_intensity(intensity_cap=False, intensity_cap_amt=48000) -> pd.DataFrame:
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
    df["hydro_intensity_mg_per_bbtu"] = np.where(df["HY-InPow"] > 0, (df["HY-InUse"] / df["HY-InPow"]), 0)

    # removing outlier intensities
    if intensity_cap:
        df['hydro_intensity_mg_per_bbtu'] = np.where(df['hydro_intensity_mg_per_bbtu'] >= intensity_cap_amt,
                                                     intensity_cap_amt,
                                                     df['hydro_intensity_mg_per_bbtu'])
    else:
        df = df

    # calculate state average
    state_avg = df.groupby("State", as_index=False).mean().drop(['HY-InUse', 'HY-InPow'], axis=1)
    state_avg = state_avg.rename(columns={'hydro_intensity_mg_per_bbtu': 'state_avg'})

    # calculate country average for states with no hydro in 1995
    country_avg = df['hydro_intensity_mg_per_bbtu'].mean()
    state_avg['state_avg'] = np.where(state_avg['state_avg'] == 0, country_avg, state_avg['state_avg'])

    # merge with main dataframe and replace 0 values
    df = pd.merge(df, state_avg, how='left', on='State')
    df['hydro_intensity_mg_per_bbtu'] = np.where(df['hydro_intensity_mg_per_bbtu'] == 0, df['state_avg'],
                                                 df['hydro_intensity_mg_per_bbtu'])

    # simplify dataframe
    df = df[['FIPS', 'hydro_intensity_mg_per_bbtu']]

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on='FIPS')

    return df


def prep_public_water_supply_fraction() -> pd.DataFrame:
    """calculating public water supply deliveries for the commercial and industrial sectors individually
     as a percent of the sum of public water supply deliveries to residential end users and thermoelectric cooling.
     Used in calculation of public water supply demand to all sectors.

    :return:                DataFrame of public water supply ratios for commercial and industrial sector.

    """

    # read in data
    df = prep_water_use_1995(all_variables=True)
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # calculate ratio of commercial pws to sum of domestic and thermoelectric cooling pws
    df['commercial_pws_fraction'] = np.where((df['PS-DelDO'] + df['PS-DelPT'] <= 0),
                                             0,
                                             (df['PS-DelCO'] / (df['PS-DelDO'] + df['PS-DelPT'])))

    # calculate ratio of industrial pws to sum of domestic and thermoelectric cooling pws
    df["industrial_pws_fraction"] = np.where(((df['PS-DelDO'] + df['PS-DelPT']) <= 0),
                                             0,
                                             df['PS-DelIN'] / (df['PS-DelDO'] + df['PS-DelPT']))

    # reduce dataframe to required output
    df = df[["FIPS", "commercial_pws_fraction", "industrial_pws_fraction"]]

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on='FIPS')
    df.fillna(0, inplace=True)

    return df


def prep_conveyance_loss_fraction(loss_cap=True, loss_cap_amt=.90) -> pd.DataFrame:
    """
    This function calculates the fraction of water lost during conveyance for irrigation for each row in the provided
    dataframe. The fraction is calculated as water lost in conveyance of irrigation water divided by total water
    withdrawn for irrigation.

    :param loss_cap:                       If True, a cap is placed on the conveyance loss fraction
    :type loss_cap:                        bool

    :param loss_cap_amt:                   The amount at which irrigation losses are capped and values beyond are
                                            replaced by the specified cap amount. The default value is .90.
    :type loss_cap_amt:                    float

    :return:                               DataFrame of conveyance loss fractions by row

    """
    # read in data
    df = prep_water_use_1995(all_variables=True)  # read in 1995 water values
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # calculate conveyance loss fraction of total water withdrawn for irrigation if irrigation water > 0
    df["crop_irrigation_conveyance_loss_fraction"] = df['IR-CLoss'] / df['IR-WTotl']
    df["golf_irrigation_conveyance_loss_fraction"] = df['IR-CLoss'] / df['IR-WTotl']

    # if a cap is placed on irrigation loss fraction, apply the supplied cap
    if loss_cap_amt < 0 or loss_cap_amt > 1:
        raise ValueError(f"loss_cap_amt must be a float between 0 and 1")

    if loss_cap:
        df["crop_irrigation_conveyance_loss_fraction"] = np.where(
            df['crop_irrigation_conveyance_loss_fraction'] > loss_cap_amt,
            loss_cap_amt,
            df["crop_irrigation_conveyance_loss_fraction"])
        df["golf_irrigation_conveyance_loss_fraction"] = np.where(
            df['golf_irrigation_conveyance_loss_fraction'] > loss_cap_amt,
            loss_cap_amt,
            df["golf_irrigation_conveyance_loss_fraction"])

    else:
        df["crop_irrigation_conveyance_loss_fraction"] = df["crop_irrigation_conveyance_loss_fraction"]
        df["golf_irrigation_conveyance_loss_fraction"] = df["golf_irrigation_conveyance_loss_fraction"]

    # Replacing infinite (from divide by zero) with nan and filling with 0
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    # reduce dataframe
    df = df[["FIPS", "crop_irrigation_conveyance_loss_fraction", "golf_irrigation_conveyance_loss_fraction"]]

    # merge with full list of counties from 2015 water data
    df = pd.merge(df_loc, df, how='left', on='FIPS')

    return df


def prep_county_identifier() -> pd.DataFrame:
    """preps a dataset of FIPS codes and associated county names so that datasets with just county names can be
    mapped to appropriate FIPS codes.

            :return:                DataFrame of FIPS code and county name identifier crosswalk

            """
    # read data
    df = get_county_identifier_data()  # dataset of full county names, state name, and FIPS codes

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

    # read in data
    df_county = prep_county_identifier()  # county identifier to FIPS crosswalk
    df_ww_flow = get_wastewater_flow_data()  # wastewater facility water flow data
    df_ww_type = get_wastewater_facility_type_data()  # wastewater facility treatment type data
    df_ww_loc = get_wastewater_facility_loc_data()  # wastewater facility location data
    df_ww_dis = get_wastewater_facility_discharge_data()  # wastewater facility discharge data
    df_county_list = prep_water_use_2015()  # full county list from 2015 water data
    df_2015_pws = prep_water_use_2015(
        variables=['FIPS', 'State', 'total_pws_withdrawals_mgd'])  # public water supply data

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
    df_ww_loc["PRIMARY_COUNTY"] = np.where(df_ww_loc["PRIMARY_COUNTY"] == "Mayaguez",
                                           "mayaquez",
                                           df_ww_loc["PRIMARY_COUNTY"])
    df_ww_loc["PRIMARY_COUNTY"] = np.where(df_ww_loc["PRIMARY_COUNTY"] == "Bedford City",
                                           "Bedford",
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

    # combine wastewater treatment facility flow data and wastewater treatment facility discharge data
    df_ww_flow = pd.merge(df_ww_flow, df_ww_loc, how="left", on='CWNS_NUMBER')  # merge dataframes

    # remove wastewater treatment facility flow data rows for geographic areas outside of scope
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "AS"]  # remove flow values for American Samoa
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "GU"]  # remove flow values for Guam

    # prep wastewater treatment facility discharge type data to remove naming and capitalization inconsistencies
    df_ww_dis['DISCHARGE_METHOD'] = df_ww_dis['DISCHARGE_METHOD'].str.replace(',', '')  # remove commas
    df_ww_dis['DISCHARGE_METHOD'] = df_ww_dis['DISCHARGE_METHOD'].str.lower()  # change to lowercase
    df_ww_dis['DISCHARGE_METHOD'] = np.where(df_ww_dis['DISCHARGE_METHOD'] == "reuse: ground water recharge",  # rename
                                             "reuse: groundwater recharge",
                                             df_ww_dis['DISCHARGE_METHOD'])
    df_ww_dis['DISCHARGE_METHOD'] = np.where(df_ww_dis['DISCHARGE_METHOD'] == "cso discharge",  # rename
                                             "combined sewer overflow (cso) discharge",
                                             df_ww_dis['DISCHARGE_METHOD'])

    # rename wastewater treatment discharge types to add clarity
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

    # for treatment plants with no discharge data, assume 100% of discharge is to surface discharge
    df_ww_dis['wastewater_surface_discharge'] = np.where(df_ww_dis['sum_pct'] == 0,  # fill blanks values
                                                         1,
                                                         df_ww_dis['wastewater_surface_discharge'])
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
    df_ww_type['TREATMENT_LEVEL_BIN'] = df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'].map(treat_dict)  # bin treat. types

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

    # fix missing treatment levels for a small number of wastewater treatment plants
    for col in df_ww_type.columns:  # fill nan rows with 0
        df_ww_flow[col] = df_ww_flow[col].fillna(0)

    # for treatment plants with no treatment type data, assume 100% of treatment type is secondary
    df_ww_flow['wastewater_secondary_treatment'] = np.where(df_ww_flow['sum_type'] < 1,
                                                            1,
                                                            df_ww_flow['wastewater_secondary_treatment'])
    df_ww_flow['sum_type'] = df_ww_flow.iloc[:, 15:-1].sum(axis=1)  # recalculate sum

    # reducing list of variables
    df_ww = df_ww_flow.drop(['sum_type', 'sum_pct'], axis=1)

    # multiply total water flows in each wastewater treatment plant by discharge and treatment type percentages
    column_list = df_ww.columns[df_ww.columns.get_loc("wastewater_consumption"):]
    for column in column_list:
        df_ww[column] = df_ww[column] * df_ww['total_wastewater_mgd']

    # add mgd units to discharge and treatment type variable names
    retain = {'FIPS', 'total_wastewater_mgd', 'infiltration_wastewater_mgd', 'municipal_wastewater_mgd'}
    df_ww.columns = ['{}{}'.format(c, '' if c in retain else '_mgd') for c in df_ww.columns]

    # group by FIPS code to get wastewater treatment flows, treatment type flows, and discharge flows by county
    df_ww = df_ww.groupby("FIPS", as_index=False).sum()

    # combine with full county list to get values for each county and fill counties with no plants with 0
    df_ww = pd.merge(df_county_list, df_ww, how='left', on='FIPS')
    df_ww.fillna(0, inplace=True)

    # create a dictionary of public water supply flows for south carolina by FIPS code
    df_2015_pws = df_2015_pws[df_2015_pws.State == "SC"]
    df_2015_pws = df_2015_pws.drop("State", axis=1)
    # sc_pws_dict = df_2015_pws.set_index('FIPS').to_dict()

    # filling in estimates for south carolina from total public water supply flows given missing data
    df_ww = pd.merge(df_ww, df_2015_pws, how='left', on='FIPS')
    for row in df_ww.iterrows():
        df_ww['total_wastewater_mgd'] = np.where(df_ww['State'] == "SC",  # fill total wastewater from public supply
                                                 df_ww['total_pws_withdrawals_mgd'],
                                                 df_ww['total_wastewater_mgd'])
        df_ww['municipal_wastewater_mgd'] = np.where(df_ww['State'] == "SC",  # fill total wastewater from public supply
                                                     df_ww['total_wastewater_mgd'],
                                                     df_ww['municipal_wastewater_mgd'])
        df_ww['wastewater_surface_discharge_mgd'] = np.where(df_ww['State'] == "SC",  # fill discharge with surface
                                                             df_ww['total_wastewater_mgd'],
                                                             df_ww['wastewater_surface_discharge_mgd'])
        df_ww['wastewater_advanced_treatment_mgd'] = np.where(df_ww['State'] == "SC",  # fill treatment with advanced
                                                              .8 * df_ww['total_wastewater_mgd'],
                                                              df_ww['wastewater_advanced_treatment_mgd'])
        df_ww['wastewater_secondary_treatment_mgd'] = np.where(df_ww['State'] == "SC",  # fill treatment with secondary
                                                               .2 * df_ww['total_wastewater_mgd'],
                                                               df_ww['wastewater_secondary_treatment_mgd'])

    # add column indicating percentage of energy from electricity, assumed 100%
    df_ww['wastewater_electricity_fuel_pct'] = 1

    # drop public water supply variable
    df_ww = df_ww.drop('total_pws_withdrawals_mgd', axis=1)

    return df_ww


def prep_power_plant_location() -> pd.DataFrame:
    """prepping power plant location information to provide a dataframe of power plant codes and their associated
    FIPS code.

    :return:                DataFrame of power plant codes and associated FIPS codes

    """
    # read in data
    df_county = prep_county_identifier()  # county identifier data
    df_plant = get_power_plant_county_data()  # power plant location data

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
    df = get_electricity_generation_data()

    # read in power plant location data by power plant id
    df_gen_loc = prep_power_plant_location()
    df_loc = prep_water_use_2015()

    # remove unnecessary variables
    df_gen_loc = df_gen_loc[['FIPS', 'plant_code']]
    df = df[['Plant Id', "AER\nFuel Type Code", "Total Fuel Consumption\nMMBtu", "Net Generation\n(Megawatthours)"]]

    # create a dictionary to bin power plant fuel types
    fuel_dict = {'SUN': 'solar',  # solar
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

    # rename columns in power plant generation data file
    df = df.rename(columns={"Plant Id": "plant_code"})
    df = df.rename(columns={"AER\nFuel Type Code": "fuel_type"})
    df = df.rename(columns={"Total Fuel Consumption\nMMBtu": "fuel_amt"})
    df = df.rename(columns={"Net Generation\n(Megawatthours)": "generation_mwh"})

    # changing string columns to numeric
    string_col = df.columns[2:]  # create list of string columns
    for col in string_col:
        df[col] = df[col].str.replace(r"[^\w ]", '', regex=True)  # replace any non alphanumeric values
        df[col] = df[col].astype(float)  # convert to float

    # removing power plant generation rows that should not be included
    df = df[df.plant_code != 99999]  # removing state level estimated differences rows

    # dropping power plants with zero fuel use and zero output
    index_list = df[(df['fuel_amt'] <= 0) & (df['generation_mwh'] <= 0)].index  # list of indices with both zero values
    df.drop(index_list, inplace=True)  # dropping rows with zero fuel and zero generation amount

    # using fuel type dictionary to bin fuel types
    df['fuel_type'] = df['fuel_type'].map(fuel_dict)  # bin fuel types

    # converting units to billion btu from million btu
    df["fuel_amt"] = df["fuel_amt"] / 1000

    # grouping rows by both plant code and fuel type
    df = df.groupby(['plant_code', 'fuel_type'], as_index=False).sum()

    # merging power plant location data with power plant generation data
    df = pd.merge(df, df_gen_loc, how='left', on='plant_code')

    # splitting out fuel data into a separate dataframe and pivoting to get fuel (bbtu) as columns by type
    df_fuel = df[["FIPS", "fuel_amt", "fuel_type"]].copy()  # create a copy of fuel type data
    df_fuel["fuel_type"] = df_fuel["fuel_type"] + "_fuel_bbtu"  # add units to fuel type column name
    df_fuel = pd.pivot_table(df_fuel, values='fuel_amt', index=['FIPS'], columns=['fuel_type'], aggfunc=np.sum)  # pivot
    df_fuel = df_fuel.reset_index()  # reset index to remove multi-index from pivot table
    df_fuel = df_fuel.rename_axis(None, axis=1)  # drop index name
    df_fuel.fillna(0, inplace=True)  # fill nan with zero

    # splitting out generation data into a separate dataframe and pivoting to get generation (mwh) as columns by type
    df_gen = df[["FIPS", "generation_mwh", "fuel_type"]].copy()  # create a copy of generation data
    df_gen['generation_mwh'] = df_gen['generation_mwh'].apply(convert_mwh_bbtu)  # convert to bbtu from mwh
    df_gen["fuel_type"] = df_gen["fuel_type"] + "_gen_bbtu"  # add units to generation type column name
    df_gen = pd.pivot_table(df_gen, values='generation_mwh', index=['FIPS'], columns=['fuel_type'], aggfunc=np.sum)
    df_gen = df_gen.reset_index()  # reset index to remove multi-index from pivot table
    df_gen = df_gen.rename_axis(None, axis=1)  # drop index name
    df_gen.fillna(0, inplace=True)  # fill nan with zero

    # merge fuel and generation dataframes into single dataframe
    df = pd.merge(df_fuel, df_gen, how='left', on='FIPS')
    df = pd.merge(df_loc, df, how='left')

    # merge dataframe with county data to distribute value to each county in a state
    df.fillna(0, inplace=True)  # fill nan with zero

    return df


def prep_thermo_cooling_data() -> pd.DataFrame:
    """prepping irrigation data so that

    :return:                DataFrame of percent of total irrigation using specified fuel type for pumping by county

    """

    df = get_powerplant_cooling_data()
    df_primary = get_powerplant_primary_data()

    fuel_dict = {'BIOMASS': 'biomass',
                 'COAL': 'coal',
                 'NUCLEAR': 'nuclear',
                 'GAS STEAM': 'natgas',  # gas steam
                 'NGCC': 'natgas',  # gas combined cycle
                 'OIL CC': 'petroleum',  # petroleum
                 'OIL': 'petroleum',
                 'COMPLEX': 'complex'}

    eia_fuel_dict = {'natural gas': 'natgas',
                     }

    cooling_dict = {'COMPLEX': 'complex',
                    'ONCE-THROUGH FRESH': 'oncethrough',
                    'RECIRCULATING TOWER': 'tower',
                    'RECIRCULATING POND': 'pond',
                    'ONCE-THROUGH SALINE': 'oncethrough'}

    water_source_dict = {'SW': 'surfacewater',
                         'GW': 'groundwater',
                         'PD': 'pws',
                         "-nr-": "surfacewater",  # all blanks assumed to be surface water
                         "GW & PD": "groundwater",  # all GW+PD are assumed to be groundwater only
                         "GW & SW": 'surfacewater',  # all GW+SW combinations are assumed to be SW
                        "OT": "surfacewater"
                         }

    water_type_dict = {'FR': 'fresh',
                       'SA': 'saline',
                       'OT': 'fresh', # all other source is assumed to be surface water
                       "FR & BE": 'fresh', # all combinations with fresh and BE are assumed to be fresh
                       "BE": "fresh",  # all BE should be changed to fresh (pws)
                        "BR": "saline"      # all brackish should be changed to saline
                        }


    # all surface water without a type is assumed to be fresh
    df['WATER_TYPE_CODE'] = np.where((df["WATER_SOURCE_CODE"] == "SW") & (df["WATER_TYPE_CODE"] == "-nr-"),
                                     "FR", df['WATER_TYPE_CODE'])

    # all groundwater without a type is assumed to be fresh
    df['WATER_TYPE_CODE'] = np.where((df["WATER_SOURCE_CODE"] == "GW") & (df["WATER_TYPE_CODE"] == "-nr-"),
                                     "FR", df['WATER_TYPE_CODE'])

    # apply dictionaries
    df['GENERATION_TYPE'] = df['GENERATION_TYPE'].map(fuel_dict)  # bin generation types
    df['COOLING_TYPE'] = df['COOLING_TYPE'].map(cooling_dict)  # rename cooling types
    df['WATER_SOURCE_CODE'] = df['WATER_SOURCE_CODE'].map(water_source_dict)  # rename water sources
    df['WATER_TYPE_CODE'] = df['WATER_TYPE_CODE'].map(water_type_dict)  # rename water types

    #
    df_primary = df_primary.rename(columns={'Plant_Code': 'EIA_PLANT_ID'})

    df = pd.merge(df, df_primary, how='left', on='EIA_PLANT_ID')
    df['PrimSource'].replace('natural gas', 'natgas', inplace=True)

    # fill complex generation types with primary source from EIA data set
    df['GENERATION_TYPE'] = np.where(df["GENERATION_TYPE"] == "complex", df['PrimSource'], df['GENERATION_TYPE'])

    # TODO fill NAN power plant types

    # TODO map values to power plant location FIPS codes

    # TODO combine columns to get single name fresh_surfacewater_biomass_tower_mgd

    # TODO pivot to get each one as a column

    return df


def prep_irrigation_fuel_data() -> pd.DataFrame:
    """prepping irrigation data so that the outcome is a dataframe showing the percent of total acres of irrigation
    that use each type of fuel for pumping (electricity, natural gas, propane, diesel, and other gas). This dataframe
    is used to calculate the total electricity and fuels to irrigation based on total water flows in irrigation.

    :return:                DataFrame of percent of total irrigation using specified fuel type for pumping by county

    """

    # read in irrigation pumping dataset
    df = get_irrigation_data()

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
    df = df.drop(["gas_pumping", "propane_pumping", "diesel_pumping", 'ng_pumping'], axis=1)

    # add units to columns
    column_list = df.columns[3:]
    for column in column_list:
        df = df.rename(columns={column: f"{column}_pct"})

    return df


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

    # read in irrigation data
    df = get_irrigation_data()
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

    return df


def prep_interbasin_transfer_data() -> pd.DataFrame:
    """Prepares interbasin water transfer data so that output is a dataframe of energy use (BBTU) and total
        water transferred for irrigation and public water supply in total.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in
    df_tx = get_tx_inter_basin_transfer_data()  # interbasin transfer data for texas
    df_west = get_west_inter_basin_transfer_data()  # interbasin transfer data for western states
    df_loc = prep_water_use_2015()  # full county list

    feet_meter_conversion = 1 / 3.281  # feet to meter conversion
    af_mps_conversion = 1 / 25567  # acre-ft-year to meters per second^3 conversion
    mwh_bbtu = 3412000 / (10 ** 9)  # megawatthour to billion btu conversion
    ag_pump_eff = .466  # assumed pump efficiency rate
    acc_gravity = 9.81  # Acceleration of gravity  (m/s^2)
    water_density = 997  # Water density (kg/m^3)

    # calculate texas interbasin transfer energy
    elevation_meters = df_tx["Elevation Difference (Feet)"] * feet_meter_conversion  # elevation in meters
    mps_cubed = df_tx["Total_Intake__Gallons (Acre-Feet/Year)"] * af_mps_conversion  # meters per second cubed
    interbasin_mwh = ((elevation_meters * mps_cubed * acc_gravity * water_density) / ag_pump_eff) / (10 ** 6)
    interbasin_bbtu = interbasin_mwh * mwh_bbtu  # convert mwh to bbtu
    df_tx[
        "electricity_interbasin_bbtu"] = interbasin_bbtu / 2  # dividing in half to split across source and target counties

    # split out target county data
    df_tx_target = df_tx[["State", "Used_FIPS", "electricity_interbasin_bbtu"]].copy()
    df_tx_target = df_tx_target.rename(columns={"Used_FIPS": "FIPS"})

    # split out source county data
    df_tx_source = df_tx[["State", "Source_FIPS", "electricity_interbasin_bbtu"]].copy()
    df_tx_source = df_tx_source.rename(columns={"Source_FIPS": "FIPS"})

    # stack source and target county interbasin transfer data
    dataframe_list = [df_tx_target, df_tx_source]
    df_tx = pd.concat(dataframe_list)

    # group by state and county fips code
    df_tx = df_tx.groupby(["State", "FIPS"], as_index=False).sum()

    # prep western state interbasin transfer energy
    df_west = df_west[['FIPS', 'Mwh/yr (Low)', 'Mwh/yr (High)']]
    df_west['FIPS'] = df_west['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero to fips

    df_west["electricity_interbasin_bbtu"] = (df_west["Mwh/yr (Low)"] + df_west[
        "Mwh/yr (High)"]) / 2  # average energy use by row
    df_west = df_west.groupby(["FIPS"], as_index=False).sum()  # group by county fips code
    df_west["electricity_interbasin_bbtu"] = df_west[
                                                 "electricity_interbasin_bbtu"] * mwh_bbtu  # convert mwh values to bbtu

    ibt_dataframe_list = [df_tx, df_west]  # bring west IBT data together with TX data
    df = pd.concat(ibt_dataframe_list)
    df = df[["FIPS", "electricity_interbasin_bbtu"]]

    # merge with county data to distribute value to each county in a state
    df = pd.merge(df_loc, df, how='left', on='FIPS')

    # filling counties that were not in the interbasin transfer datasets with 0
    df['electricity_interbasin_bbtu'].fillna(0, inplace=True)

    return df


def prep_irrigation_pws_ratio() -> pd.DataFrame:
    """prepping the ratio of water flows to irrigation vs. water flows to public water supply by county. Used to
    determine the split of electricity in interbasin transfers between the two sectors.

    :return:                DataFrame of percentages by county

    """
    # read data
    df_irr_pws = prep_water_use_2015(variables=['FIPS', 'State', 'County', 'fresh_groundwater_crop_irrigation_mgd',
                                                'fresh_surfacewater_crop_irrigation_mgd', 'total_pws_withdrawals_mgd'])

    # calculate public water supply percent of combined flows
    df_irr_pws['pws_ibt_pct'] = df_irr_pws['total_pws_withdrawals_mgd'] \
                                / (df_irr_pws['fresh_groundwater_crop_irrigation_mgd']
                                   + df_irr_pws['fresh_surfacewater_crop_irrigation_mgd']
                                   + df_irr_pws['total_pws_withdrawals_mgd'])

    # add in column for agriculture fraction (1-pws)
    df_irr_pws['irrigation_ibt_pct'] = 1 - df_irr_pws['pws_ibt_pct']

    # fill counties that have no public water supply or irrigation flows with zero
    df_irr_pws.fillna(0, inplace=True)

    # reduce dataframe variables
    df_irr_pws = df_irr_pws[['FIPS', 'State', 'County', 'pws_ibt_pct', 'irrigation_ibt_pct']]

    return df_irr_pws


def prep_electricity_demand_data() -> pd.DataFrame:
    """prepping electricity demand data by sector. Produces a dataframe of demand data by county.

    :return:                DataFrame of electricity demand data

    """

    # read in state and territory electricity demand data
    df_states = get_state_electricity_demand_data()
    df_terr = get_territory_electricity_demand_data()

    # build renaming dictionary
    rename_dict = {"RESIDENTIAL": "electricity_residential_bbtu",
                   "COMMERCIAL": "electricity_commercial_bbtu",
                   "INDUSTRIAL": "electricity_industrial_bbtu",
                   "TRANSPORTATION": "electricity_transportation_bbtu"}

    # concatenate state and territory demand data
    df_list = [df_states, df_terr]
    df = pd.concat(df_list)

    # prep dataframe
    df = df.dropna(subset=["Month"])  # drop rows where month is blank
    df = df.dropna(subset=["Ownership"])  # Drop state totals and state adjustments
    df = df[df.Ownership != "Behind the Meter"]  # removing behind the meter generation
    df = df.groupby("State", as_index=False).sum()  # get total by state
    df = df[["State", "RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL", "TRANSPORTATION"]]

    # convert electricity demand values from mwh to bbtu
    column_list = df.columns[1:]
    for col in column_list:
        df[col] = df[col].apply(convert_mwh_bbtu)

    # rename columns to add descriptive language
    df.rename(columns=rename_dict, inplace=True)

    # add a row for the US Virgin Islands
    virgin_islands_percent = 0.0298  # percent of puerto rico total population
    puertorico_index = df.index[df['State'] == "PR"].tolist()  # copy puerto rico values to list
    df = df.append(df.loc[puertorico_index * 1].assign(State="VI"), ignore_index=True)
    multiply_columns = df.columns[1:]
    for m in multiply_columns:
        df[m] = np.where(df['State'] == "VI", df[m] * virgin_islands_percent, df[m])

    # split out into county values based on percent of state population
    df = calc_population_county_weight(df)
    demand_columns = df.columns[3:7]
    for d in demand_columns:
        df[d] = df[d] * df['pop_weight']
        df[d] = df[d].round(4)
    df = df.drop(['pop_weight'], axis=1)

    return df


def prep_fuel_demand_data() -> pd.DataFrame:
    """prepping fuel demand data. Returns a dataframe of fuel demand by fuel type and sector in bbtu for each county.

    :return:                DataFrame of a fuel demand values by sector

    """

    # read in energy consumption data
    df = get_fuel_demand_data()

    # dictionary of fuel demand codes that are relevant and descriptive names
    msn_dict = {"CLCCB": "coal_commercial_bbtu",  # Coal, commercial sector (bbtu)
                "CLICB": "coal_industrial_bbtu",  # Coal, industrial sector (bbtu)
                "EMACB": "biomass_transportation_bbtu",  # Fuel ethanol, transportation sector (bbtu)
                "GECCB": "geothermal_commercial_bbtu",  # Geothermal, commercial sector (bbtu)
                "GERCB": "geothermal_residential_bbtu",  # Geothermal, residential sector (bbtu)
                "NGACB": "natural_gas_transportation_bbtu",  # Natural gas, transportation sector  (bbtu)
                "NGCCB": "natural_gas_commercial_bbtu",  # Natural gas, commercial sector (bbtu)
                "NGICB": "natural_gas_industrial_bbtu",  # Natural gas, industrial sector (bbtu)
                "NGRCB": "natural_gas_residential_bbtu",  # Natural gas, residential sector (bbtu
                "PAACB": "petroleum_transportation_bbtu",  # petroleum products, transportation sector (bbtu)
                "PACCB": "petroleum_commercial_bbtu",  # petroleum products, commercial sector (bbtu)
                "PAICB": "petroleum_industrial_bbtu",  # petroleum products, industrial sector (bbtu)
                "PARCB": "petroleum_residential_bbtu",  # petroleum products, residential sector (bbtu)
                "SOCCB": "solar_commercial_bbtu",  # Solar, commercial sector (bbtu)
                "SORCB": "solar_residential_bbtu",  # Solar, residential sector (bbtu)
                "WDRCB": "biomass_residential_bbtu",  # Wood energy, residential sector (bbtu)
                "WWCCB": "biomass_commercial_bbtu",  # Wood and waste energy, commercial sector (bbtu)
                "WWICB": "biomass_industrial_bbtu",  # Wood and waste energy, industrial sector (bbtu)
                "WYCCB": "wind_commercial_bbtu"  # Wind energy, commercial sector (bbtu)
                }

    # reduce dataframe
    df = df[df['MSN'].isin(msn_dict)]  # using MSN codes that are relevant

    # pivoting dataframe to get fuel codes as columns
    df = pd.pivot_table(df, values='2015', index=['State'],  # pivot
                        columns=['MSN'], aggfunc=np.sum)
    df = df.reset_index()  # reset index to remove multi-index
    df = df.rename_axis(None, axis=1)  # drop index name
    df.fillna(0, inplace=True)  # filling blanks with zero

    # split out data into county values and multiply by population weighting
    df = calc_population_county_weight(df)
    energy_columns = df.columns[3:]
    for d in energy_columns:
        df[d] = df[d] * df['pop_weight']

    # rename columns to add descriptive language
    df.rename(columns=msn_dict, inplace=True)

    # remove unneeded columns
    df = df.drop(['pop_weight'], axis=1)

    df.fillna(0, inplace=True)

    return df


def prep_state_fuel_production_data() -> pd.DataFrame:
    """prepping state-level fuel production data for petroleum, biomass, natural gas, and coal. Outputs can be used
    to determine county-level fuel production for each fuel type.

    :return:                DataFrame of fuel production data by fuel type and state

    """

    # read in energy production data
    df = get_energy_production_data()

    # list of fuel demand codes that are relevant from dataset
    msn_prod_dict = {"PAPRB": "petroleum_production_bbtu",  # crude oil production (including lease condensate) (BBTU)
                     "EMFDB": "biomass_production_bbtu",  # biomass inputs to the production of fuel ethanol (BBTU)
                     "NGMPB": "natgas_production_bbtu",  # natural gas marketed production (BBTU)
                     "CLPRB": "coal_production_bbtu",  # coal production (BBTU)
                     }
    df = df[df['MSN'].isin(msn_prod_dict)]  # grabbing MSN codes that are relevant

    # prepping data
    df = pd.pivot_table(df, values='2015', index=['StateCode'],  # pivoting to get fuel codes as columns
                        columns=['MSN'], aggfunc=np.sum)
    df = df.reset_index()  # reset index to remove multi-index
    df = df.rename_axis(None, axis=1)  # drop index name
    df = df.rename(columns={"StateCode": "State"})  # rename state column
    df = df[df.State != "X3"]  # drop offshore (gulf of mexico) values
    df = df[df.State != "X5"]  # drop offshore (pacific) values
    df = df[df.State != "US"]  # drop total US values
    df.fillna(0, inplace=True)  # filling blanks with zero

    df.rename(columns=msn_prod_dict, inplace=True)  # rename columns to add descriptive language

    # add rows for puerto rico and virgin islands
    pr_df = {'State': 'PR', 'petroleum_production_bbtu': 0, 'biomass_production_bbtu': 0,
             'natgas_production_bbtu': 0, 'coal_production_bbtu': 0}
    vi_df = {'State': 'VI', 'petroleum_production_bbtu': 0, 'biomass_production_bbtu': 0,
             'natgas_production_bbtu': 0, 'coal_production_bbtu': 0}
    df = df.append(pr_df, ignore_index=True)
    df = df.append(vi_df, ignore_index=True)

    return df


def prep_county_petroleum_production_data() -> pd.DataFrame:
    """prepares a dataframe of oil production by county for the year 2015. The dataframe uses 2011 crude oil production
    (barrels per year) by county in the US to determine which counties in a given state contribute the most to the
    state total. These percent of state total values from 2011 are mapped to 2015 state total oil production to get
    2015 values on a county level.

    :return:                DataFrame of a oil production (bbtu) by county

    """
    UNCONVENTIONAL_PETROLEUM_FRACTION = .63  # fraction of all petroleum production that is unconventional
    GALLON_OIL_TO_BBTU_CONVERSION = 0.0001355  # gallon of oil to billion btu conversion
    MILLION_MULTIPLIER = 1000000  # a million
    SURFACEWATER_PCT = .8  # assumed percent of withdrawals for unconventional petroleum from surface water

    # read in data
    df = prep_state_fuel_production_data()  # read in 2015 state level petroleum production data
    df_petroleum_loc = get_county_oil_gas_production_data()  # read in 2011 county level oil data
    df_loc = prep_water_use_2015()  # read in FIPS codes and states from 2015 water dataset
    df_conventional_water = get_conventional_oil_water_intensity_data()  # read water withdrawal intensity values
    df_unconventional_water = get_unconventional_oil_gas_production_data()

    # reduce dataframes to required variables
    df = df[["State", "petroleum_production_bbtu"]]
    df_petroleum_loc = df_petroleum_loc[['FIPS', 'Stabr', 'oil2011']]

    # calculate percent of total 2011 state oil production by county
    df_petroleum_loc_sum = df_petroleum_loc[['Stabr', 'oil2011']].groupby("Stabr", as_index=False).sum()
    df_petroleum_loc_sum = df_petroleum_loc_sum.rename(columns={"oil2011": "state_total"})  # rename column
    df_petroleum_loc = pd.merge(df_petroleum_loc, df_petroleum_loc_sum, how='left', on='Stabr')  # merge dataframes
    df_petroleum_loc['oil_pct'] = df_petroleum_loc['oil2011'] / df_petroleum_loc['state_total']  # calculate percent

    # reformat data
    df_petroleum_loc = df_petroleum_loc.rename(columns={"Stabr": "State"})
    df_petroleum_loc['FIPS'] = df_petroleum_loc['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero

    # add missing states (Idaho, and Alaska) that have 2015 oil production data
    idaho_df = {'State': 'ID', 'FIPS': '16075', 'oil_pct': 1}  # Idaho
    ak_arctic_df = {'State': 'AK', 'FIPS': '02185', 'oil_pct': .9738}  # Alaska, arctic slope region
    ak_cook_df = {'State': 'AK', 'FIPS': '02122', 'oil_pct': .0262}  # Alaska, cook inlet basin (kenai peninsula)
    oil_list = [idaho_df, ak_arctic_df, ak_cook_df]
    for oil_county in oil_list:
        df_petroleum_loc = df_petroleum_loc.append(oil_county, ignore_index=True)

    # merge 2015 state-level production data with 2011 county level percent data
    df = pd.merge(df_petroleum_loc, df, how='left', on="State")

    # calculate 2015 percent by county
    df['petroleum_production_bbtu'] = df['petroleum_production_bbtu'] * df['oil_pct']

    # split into unconventional and conventional
    df['petroleum_unconventional_production_bbtu'] = UNCONVENTIONAL_PETROLEUM_FRACTION \
                                                     * df['petroleum_production_bbtu']
    df['petroleum_conventional_production_bbtu'] = (1 - UNCONVENTIONAL_PETROLEUM_FRACTION) \
                                                   * df['petroleum_production_bbtu']

    # unconventional water use
    df_unconventional_water = df_unconventional_water[
        ['State', 'FSW_Unconventional_Oil (MGD)', 'FGW_Unconventional_Oil (MGD)']]
    df = pd.merge(df, df_unconventional_water, how='left', on='State')
    df['fresh_surfacewater_petroleum_unconventional_mgd'] = df['FSW_Unconventional_Oil (MGD)'] * df['oil_pct']
    df['fresh_groundwater_petroleum_unconventional_mgd'] = df['FGW_Unconventional_Oil (MGD)'] * df['oil_pct']

    # fill water values with average water intensity for locations where petroleum is produced, but no water estimates
    df['total_water'] = df['fresh_surfacewater_petroleum_unconventional_mgd'] + df[
        'fresh_groundwater_petroleum_unconventional_mgd']
    df['intensity_mg_per_bbtu'] = np.where(df['petroleum_unconventional_production_bbtu'] > 0,
                                           df['total_water'] / (df['petroleum_unconventional_production_bbtu'] / 365),
                                           np.nan)
    avg_intensity = df['intensity_mg_per_bbtu'].mean()

    # rows where there is natural gas production
    prod_rows = df['petroleum_unconventional_production_bbtu'].notnull()

    # rows where there is no surface water withdrawal
    sw_rows = df['fresh_surfacewater_petroleum_unconventional_mgd'].isna()
    # rows where there is no groundwater withdrawal
    gw_rows = df['fresh_groundwater_petroleum_unconventional_mgd'].isna()

    df['fresh_surfacewater_petroleum_unconventional_mgd'] = np.where(prod_rows & sw_rows,
                                                                     df['petroleum_unconventional_production_bbtu']
                                                                     * avg_intensity * SURFACEWATER_PCT,
                                                                     df[
                                                                         'fresh_surfacewater_petroleum_unconventional_mgd'])
    df['fresh_groundwater_petroleum_unconventional_mgd'] = np.where(prod_rows & gw_rows,
                                                                    df['petroleum_unconventional_production_bbtu']
                                                                    * avg_intensity * (1 - SURFACEWATER_PCT),
                                                                    df[
                                                                        'fresh_groundwater_petroleum_unconventional_mgd'])

    df = df.drop(['total_water', 'intensity_mg_per_bbtu'], axis=1)

    # calculate mg/bbtu water intensity for conventional petroleum by county
    intensity_name = 'petroleum_conventional_water_use_intensity_mg_per_bbtu'
    df_conventional_water[intensity_name] = (df_conventional_water['GalWater_GalOil'] / MILLION_MULTIPLIER) \
                                            / GALLON_OIL_TO_BBTU_CONVERSION

    df_conventional_water = df_conventional_water[["State", intensity_name]]
    df_conventional_water = pd.merge(df_loc, df_conventional_water, how='left', on='State')
    df = pd.merge(df, df_conventional_water, how='right', on='FIPS')

    # reduce dataframe
    df = df[['FIPS', 'petroleum_production_bbtu',
             'petroleum_unconventional_production_bbtu',
             'petroleum_conventional_production_bbtu', 'petroleum_conventional_water_use_intensity_mg_per_bbtu',
             'fresh_surfacewater_petroleum_unconventional_mgd', 'fresh_groundwater_petroleum_unconventional_mgd']]

    # merge with county data to distribute value to each county in a state and include all FIPS
    df = pd.merge(df_loc, df, how='left', on='FIPS')
    df.fillna(0, inplace=True)

    return df


def prep_county_natgas_production_data() -> pd.DataFrame:
    """prepares a dataframe of natural gas production by county for the year 2015. The dataframe uses 2011 natural gas
     production (million cubic ft) by county in the US to determine which counties in a given state contribute the
     most to the state total. These percent of state total values from 2011 are mapped to 2015 state total natural gas
      production to get 2015 values on a county level. Water withdrawal data is supplied for a select number of states
      these state totals are split out to counties using the same county percent of total natural gas production as
      the production calculation. For states with 2015 production but no water withdrawal estimates, the national
      average water intensity (mg/bbtu) is applied to their natural gas production quantity. It is assumed that 80% of
      these calculated total water use values come from fresh surface water and 20% from fresh groundwater.

    :return:                DataFrame of a natural gas production (bbtu) and water use (mgd) by county

    """
    # establish percent of water withdrawals for unconventional natural gas from surface water
    SURFACEWATER_PCT = .80

    # read in data
    df = prep_state_fuel_production_data()  # read in 2015 state level petroleum production data
    df_ng_loc = get_county_oil_gas_production_data()  # read in 2011 county level oil data
    df_loc = prep_water_use_2015()  # read in FIPS codes and states from 2015 water dataset
    df_unconventional_water = get_unconventional_oil_gas_production_data()

    # reduce dataframes to required variables
    df = df[["State", "natgas_production_bbtu"]]
    df_ng_loc = df_ng_loc[['FIPS', 'Stabr', 'gas2011']]

    # calculate percent of total 2011 state oil production by county
    df_ng_loc_sum = df_ng_loc[['Stabr', 'gas2011']].groupby("Stabr", as_index=False).sum()
    df_ng_loc_sum = df_ng_loc_sum.rename(columns={"gas2011": "state_total"})
    df_ng_loc = pd.merge(df_ng_loc, df_ng_loc_sum, how='left', on='Stabr')
    df_ng_loc['gas_pct'] = df_ng_loc['gas2011'] / df_ng_loc['state_total']

    # rename columns
    df_ng_loc = df_ng_loc.rename(columns={"Stabr": "State"})
    df_ng_loc['FIPS'] = df_ng_loc['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero

    # add rows with missing county percentages to cover all states in 2015 production
    idaho_df = {'State': 'ID', 'FIPS': '16075', 'gas_pct': 1}  # Idaho
    ak_arctic_df = {'State': 'AK', 'FIPS': '02185', 'gas_pct': .9608}  # Alaska, arctic slope region
    ak_cook_df = {'State': 'AK', 'FIPS': '02122', 'gas_pct': .0392}  # Alaska, cook inlet basin (kenai peninsula)
    md_garret_df = {'State': 'MD', 'FIPS': '24023', 'gas_pct': .5}  # Maryland, Garret County
    md_allegany_df = {'State': 'MD', 'FIPS': '24001', 'gas_pct': .5}  # Maryland, Allegany County
    nv_nye_df = {'State': 'NV', 'FIPS': '32023', 'gas_pct': 1}  # Nevada, Nye County
    or_columbia_df = {'State': 'OR', 'FIPS': '41009', 'gas_pct': 1}  # Oregon, Columbia County
    ng_list = [idaho_df, ak_arctic_df, ak_cook_df, md_garret_df, md_allegany_df, nv_nye_df, or_columbia_df]

    for county in ng_list:
        df_ng_loc = df_ng_loc.append(county, ignore_index=True)

    # merge 2015 state-level production data with 2011 county level percent data
    df = pd.merge(df_ng_loc, df, how='left', on="State")

    # calculate 2015 percent by county
    df['natgas_production_bbtu'] = df['natgas_production_bbtu'] * df['gas_pct']
    df['natgas_unconventional_production_bbtu'] = df['natgas_production_bbtu']

    df_unconventional_water = df_unconventional_water[['State', 'FSW_Unconventional_NG (MGD)',
                                                       'FGW_Unconventional_NG (MGD)']]

    df_unconventional_water = pd.merge(df_loc, df_unconventional_water, how='left', on='State')

    df = pd.merge(df, df_unconventional_water, how='right', on="FIPS")
    df['fresh_surfacewater_natgas_unconventional_mgd'] = df['FSW_Unconventional_NG (MGD)'] * df['gas_pct']
    df['fresh_groundwater_natgas_unconventional_mgd'] = df['FGW_Unconventional_NG (MGD)'] * df['gas_pct']

    # reduce dataframe
    df = df[['FIPS', 'natgas_production_bbtu', 'natgas_unconventional_production_bbtu',
             'fresh_surfacewater_natgas_unconventional_mgd', 'fresh_groundwater_natgas_unconventional_mgd']]

    # fill water values with average water intensity for locations where natural gas is produced, but no water estimates
    df['total_water'] = df['fresh_surfacewater_natgas_unconventional_mgd'] + df[
        'fresh_groundwater_natgas_unconventional_mgd']
    df['intensity_mg_per_bbtu'] = np.where(df['natgas_unconventional_production_bbtu'] > 0,
                                           df['total_water'] / (df['natgas_unconventional_production_bbtu'] / 365),
                                           np.nan)

    avg_intensity = df['intensity_mg_per_bbtu'].mean()

    # rows where there is natural gas production
    prod_rows = df['natgas_production_bbtu'].notnull()

    # rows where there is no water withdrawal
    sw_rows = df['fresh_surfacewater_natgas_unconventional_mgd'].isna()
    # rows where there is no water withdrawal
    gw_rows = df['fresh_groundwater_natgas_unconventional_mgd'].isna()

    df['fresh_surfacewater_natgas_unconventional_mgd'] = np.where(prod_rows & sw_rows,
                                                                  df[
                                                                      'natgas_production_bbtu'] * avg_intensity * SURFACEWATER_PCT,
                                                                  df['fresh_surfacewater_natgas_unconventional_mgd'])
    df['fresh_groundwater_natgas_unconventional_mgd'] = np.where(prod_rows & gw_rows,
                                                                 df['natgas_production_bbtu'] * avg_intensity * (
                                                                             1 - SURFACEWATER_PCT),
                                                                 df['fresh_groundwater_natgas_unconventional_mgd'])

    df = df.drop(['total_water', 'intensity_mg_per_bbtu'], axis=1)

    # merge with county data to distribute value to each county in a state and include all FIPS
    df = pd.merge(df_loc, df, how='left', on='FIPS')
    df.fillna(0, inplace=True)

    return df


def prep_petroleum_gas_discharge_data() -> pd.DataFrame:
    """prepares a dataframe of produced water intensities, consumption fractions, and discharge fractions for
    unconventional petroleum and unconventional natural gas drilling.

    :return:                DataFrame of produced water intensities, consumption fractions, and discharge fractions
                            for unconventional natural gas and petroleum production

    """
    # read in data
    df = get_oil_gas_discharge_data()
    df_loc = prep_water_use_2015()

    # rename dictionary
    rename_dict = {'Total injected (%)': "petroleum_unconventional_ground_discharge_fraction",
                   'Surface Discharge (%)': 'petroleum_unconventional_surface_discharge_fraction',
                   'Evaporation/ Consumption (%)': 'petroleum_unconventional_consumption_fraction'}

    generation_list = ['natgas_unconventional', 'natgas_conventional']

    # establish conversion factors
    WATER_BARREL_TO_MG_CONVERSION = 0.000042
    OIL_BARREL_TO_BBTU_CONVERSION = 0.005691
    GAS_MMCF_TO_BBTU_CONVERSION = 1

    # convert barrels of water per barrel of oil to million gallons per bbtu of oil
    df['petroleum_unconventional_produced_water_intensity_mg_per_bbtu'] = df['WOR (bbl/bbl)'] \
                                                                          * (WATER_BARREL_TO_MG_CONVERSION
                                                                             / OIL_BARREL_TO_BBTU_CONVERSION)

    # convert barrels of water per mmcf of natural gas to million gallons per bbtu of natural gas
    df['natgas_unconventional_produced_water_intensity_mg_per_bbtu'] = df['WGR (bbl/Mmcf)'] \
                                                                       * (WATER_BARREL_TO_MG_CONVERSION
                                                                          / GAS_MMCF_TO_BBTU_CONVERSION)

    # recalculate discharge fractions as a percent of remaining water, not inclusive of consumption fraction
    df['discharge_total_pct'] = df['Surface Discharge (%)'] + df['Total injected (%)']
    df['Surface Discharge (%)'] = df['Surface Discharge (%)'] / df['discharge_total_pct']
    df['Total injected (%)'] = df['Total injected (%)'] / df['discharge_total_pct']

    # rename columns
    df.rename(columns=rename_dict, inplace=True)

    # copy discharge and consumption fractions to each generation type
    for gen_type in generation_list:
        ground_name = gen_type + "_ground_discharge_fraction"
        surface_name = gen_type + "_surface_discharge_fraction"
        consumption_name = gen_type + "_consumption_fraction"

        df[ground_name] = df["petroleum_unconventional_ground_discharge_fraction"]
        df[surface_name] = df["petroleum_unconventional_surface_discharge_fraction"]
        df[consumption_name] = df["petroleum_unconventional_consumption_fraction"]

    # drop unneeded variables
    df = df.drop(['WOR (bbl/bbl)', 'WGR (bbl/Mmcf)', 'discharge_total_pct'], axis=1)

    # calculate the mean of each column
    df_mean_dict = df[df.columns[1:].to_list()].mean().to_dict()

    # replace blank values with zero at state level
    df.fillna(0, inplace=True)

    # merge to get values at county level
    df = pd.merge(df_loc, df, how='left', on='State')

    # create a list of columns to fill blank values
    fill_list = df.columns[3:].to_list()

    for column in fill_list:
        df[column].fillna(df_mean_dict[column], inplace=True)

    return df


def prep_county_coal_production_data() -> pd.DataFrame:
    """prepares a dataframe of coal production by county from surface and underground mines in bbtu. Dataframe can be
    used to determine water in coal mining.

    :return:                DataFrame of coal production values in bbtu by county

    """
    # read in data
    df_coal_loc = get_coal_mine_location_data()  # coal mine location data
    df_fips = get_state_fips_data()  # State-level FIPS codes
    df_coal = get_coal_production_data()  # coal mine production data
    df_loc = prep_water_use_2015()  # read in FIPS codes and states from 2015 water dataset

    # establish unit conversions
    shortton_bbtu_conversion = 0.02009  # one short ton is equal to 0.02009 bbtu

    # process coal mine location data to get coal mine ID and associated FIPS code
    df_coal_loc = df_coal_loc.rename(columns={"STATE": "State"})  # rename column
    df_coal_loc = pd.merge(df_coal_loc, df_fips, how="left", on="State")  # merge coal mine location and state FIPS
    df_coal_loc['FIPS_CNTY_CD'] = df_coal_loc['FIPS_CNTY_CD'].apply(lambda x: '{0:0>3}'.format(x))  # leading zeroes
    df_coal_loc["FIPS"] = df_coal_loc['State_FIPS'] + df_coal_loc['FIPS_CNTY_CD']  # create single FIPS code
    df_coal_loc['FIPS'] = df_coal_loc['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero
    df_coal_loc = df_coal_loc[["MINE_ID", "FIPS"]]  # reduce to needed variables

    # process coal mine production data
    df_coal = df_coal.rename(columns={"MSHA ID": "MINE_ID"})  # renaming Mine ID column
    df_coal = df_coal[['MINE_ID', 'Mine Type', 'Production (short tons)']]  # reduce to variables of interest

    # combine coal mine production and location data
    df_coal = pd.merge(df_coal, df_coal_loc, how="left", on="MINE_ID")  # merge dataframes

    # fill in missing FIPS codes for two mines
    df_coal['FIPS'] = np.where(df_coal['MINE_ID'] == 3609086, "42051", df_coal['FIPS'])
    df_coal['FIPS'] = np.where(df_coal['MINE_ID'] == 3607079, "42079", df_coal['FIPS'])

    # reorganize dataframe to get mine type as a column and individual row for each FIPS code
    df_coal = pd.pivot_table(df_coal, values='Production (short tons)',  # pivot dataframe
                             index=['FIPS'], columns=['Mine Type'], aggfunc=np.sum)
    df_coal = df_coal.reset_index()  # reset index to remove multi-index from pivot table
    df_coal = df_coal.rename_axis(None, axis=1)  # drop index name
    df_coal.fillna(0, inplace=True)

    # calculate coal production per county in billion btus
    df_coal['Refuse'] = df_coal['Refuse'] * shortton_bbtu_conversion
    df_coal['Surface'] = df_coal['Surface'] * shortton_bbtu_conversion
    df_coal['Underground'] = df_coal['Underground'] * shortton_bbtu_conversion
    df_coal['coal_production_bbtu'] = (df_coal['Refuse'] + df_coal['Surface']
                                       + df_coal['Underground'])

    # rename short ton production columns to add units
    coal_prod_dict = {"Refuse": "coal_refuse_production_bbtu",  # refuse coal production
                      "Surface": "coal_surface_production_bbtu",  # coal production from surface mines
                      "Underground": "coal_underground_production_bbtu",  # coal production from underground mines
                      }
    df_coal.rename(columns=coal_prod_dict, inplace=True)  # rename columns to add descriptive language

    # merge with full county data to distribute value to each county in a state and include all FIPS
    df_coal = pd.merge(df_loc, df_coal, how='left', on='FIPS')
    df_coal.fillna(0, inplace=True)

    return df_coal


def prep_county_coal_water_source_fractions() -> pd.DataFrame:
    """prepares a dataframe of water type and water source fractions to coal mining by county

    :return:                DataFrame of water types and water source fractions to coal production

    """

    # read in water use data for 2015 in million gallons per day by county
    df = prep_water_use_2015(variables=['FIPS', 'fresh_groundwater_mining_mgd',
                                        'fresh_surfacewater_mining_mgd', 'saline_groundwater_mining_mgd',
                                        'saline_surfacewater_mining_mgd'])

    # read in region identifier
    df_loc = prep_water_use_2015()

    # create a list of mining water source names
    source_list = ['fresh_groundwater', 'fresh_surfacewater',
                   'saline_groundwater', 'saline_surfacewater']

    # calculate total water flows to mining
    df['total_mining_water'] = df[df.columns[3:].to_list()].sum(axis=1)

    # start a list of data to retain
    retain_list = ['FIPS']

    # calculate water fractions
    for source in source_list:
        fraction_name = source + "_coal_production_fraction"
        water_name = source + "_mining_mgd"
        df[fraction_name] = np.where(df['total_mining_water'] > 0,
                                     df[water_name] / df['total_mining_water'],
                                     np.nan)

        # fill blank water fractions
        df[fraction_name].fillna(df[fraction_name].mean(), inplace=True)

        retain_list.append(fraction_name)

    # merge with county location data
    df = pd.merge(df_loc, df[retain_list], how='left', on='FIPS')

    return df


def prep_county_ethanol_production_data() -> pd.DataFrame:
    """ Takes 2015 eia data on ethanol plant capacity with locational data and combines with state level biomass
     (ethanol) production from prep_state_fuel_production_data() to split out state total by county. Returns a
     dataframe of ethanol production (bbtu) by county FIPS for each county in the US for 2015.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in data
    df_ethanol_loc = get_ethanol_location_data()  # coal mine location data
    df_ethanol_production = prep_state_fuel_production_data()  # coal mine production data
    df_loc = prep_water_use_2015()  # read in FIPS codes and states from 2015 water dataset

    # calculate percentage of state total ethanol production for each county in ethanol plant location data
    df_ethanol_loc = df_ethanol_loc[["State", "FIPS", "Mmgal/yr"]]
    df_ethanol_loc = df_ethanol_loc.groupby(["State", "FIPS"], as_index=False).sum()
    df_ethanol_loc_sum = df_ethanol_loc.groupby("State", as_index=False).sum()
    df_ethanol_loc_sum = df_ethanol_loc_sum.rename(columns={"Mmgal/yr": "State Total"})
    df_ethanol_loc = pd.merge(df_ethanol_loc, df_ethanol_loc_sum, how='left', on='State')

    df_ethanol_loc['ethanol_pct'] = df_ethanol_loc['Mmgal/yr'] / df_ethanol_loc['State Total']
    df_ethanol_loc = df_ethanol_loc[['State', 'FIPS', 'ethanol_pct']]

    # add missing row for wyoming county ethanol production
    wy_df = {'State': 'WY', 'FIPS': '56015', 'ethanol_pct': 1}  # Goshen County, Wyoming
    df_ethanol_loc = df_ethanol_loc.append(wy_df, ignore_index=True)

    df_ethanol_loc['FIPS'] = df_ethanol_loc['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero

    # merge ethanol location data with ethanol production data
    df_ethanol_production = df_ethanol_production[['State', 'biomass_production_bbtu']]
    df_biomass = pd.merge(df_ethanol_loc, df_ethanol_production, how='left', on='State')

    # split out state level 2015 ethanol production to individual counties by state
    df_biomass['biomass_production_bbtu'] = df_biomass['biomass_production_bbtu'] * df_biomass['ethanol_pct']
    df_biomass = df_biomass[['FIPS', 'biomass_production_bbtu']]
    df_biomass['biomass_ethanol_production_bbtu'] = df_biomass['biomass_production_bbtu']

    # merge with full county data to distribute value to each county in a state and include all FIPS
    df_biomass = pd.merge(df_loc, df_biomass, how='left', on='FIPS')
    df_biomass.fillna(0, inplace=True)

    return df_biomass


def prep_county_water_corn_biomass_data() -> pd.DataFrame:
    """ Produces a dataframe of water (MGD) for corn irrigation for ethanol by county. Water intensity applied to all
    crop irrigation is applied to the irrigation used in the production of corn for ethanol.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in data
    df_corn = get_corn_irrigation_data()  # coal mine location data
    df_irr_water = prep_water_use_2015(variables=['State', 'fresh_groundwater_crop_irrigation_mgd',
                                                  'fresh_surfacewater_crop_irrigation_mgd'])
    df_loc = prep_water_use_2015()
    df_corn_prod = get_corn_production_data()
    df_state_abb = get_state_fips_data()

    # set up variables
    ethanol_fraction = 0.38406  # corn grown for ethanol fraction
    af_gal_conversion = 325851  # acre ft to gallon conversion

    # clean data
    df_corn.fillna(0, inplace=True)  # replaces blank values with 0

    # calculate the irrigation intensity for all crops by state (total gallons per year)
    df_corn["gallons_applied"] = af_gal_conversion * df_corn["Acre-feet-Applied_All"]  # gallons applied to all crops
    df_corn["irr_intensity"] = df_corn["gallons_applied"] / df_corn["Total_Acres_Irrigated_All"]  # gal/acre all crops
    df_corn["irr_intensity"] = df_corn["irr_intensity"] / 10 ** 6  # convert to million gallons/acre

    # calculate the amount of corn grown for ethanol production in each state
    df_corn["corn_prod"] = ethanol_fraction * df_corn["Acres_Corn_Harvested"]  # acres of corn for ethanol by state

    # calculate the total amount of water applied to corn grown for ethanol
    df_corn["ethanol_corn_mgal"] = df_corn["irr_intensity"] * df_corn["corn_prod"]
    df_corn["ethanol_corn_mgal"] = (df_corn["ethanol_corn_mgal"] / 365).round(4)  # convert to million gallons per day

    # calculate surface water vs. groundwater fraction in corn irrigation
    df_corn["surface_total"] = df_corn["Off"] + df_corn["Surface"]  # adds off-farm and surface together for surface
    df_corn["water_total"] = df_corn["surface_total"] + df_corn["Ground"]  # sum surface water and groundwater
    df_corn['surface_frac'] = df_corn["surface_total"] / df_corn["water_total"]  # surface water fraction

    # calculate irrigation surface water to groundwater ratio for each state from 2015 USGS water dataset
    df_irr_water = df_irr_water.groupby("State", as_index=False).sum()
    df_irr_water['surface_frac_fill'] = df_irr_water['fresh_surfacewater_crop_irrigation_mgd'] \
                                        / (df_irr_water['fresh_surfacewater_crop_irrigation_mgd']
                                           + df_irr_water['fresh_groundwater_crop_irrigation_mgd'])
    df_irr_water = df_irr_water[['State', 'surface_frac_fill']]
    df_irr_water.fillna(0, inplace=True)  # replaces blank values with 0

    # fill states with corn growth but no surface vs. groundwater fraction available with estimate from 2015 water data
    df_corn = pd.merge(df_corn, df_irr_water, how='left', on="State")
    df_corn['surface_frac'].fillna(df_corn['surface_frac_fill'], inplace=True)

    # split up ethanol corn irrigation water by surface and groundwater source percentages
    df_corn['sw_ethanol_corn'] = (df_corn['surface_frac'] * df_corn["ethanol_corn_mgal"]).round(4)  # surface water
    df_corn['gw_ethanol_corn'] = ((1 - df_corn['surface_frac']) * df_corn["ethanol_corn_mgal"]).round(4)  # groundwater
    df_corn.fillna(0, inplace=True)  # replaces blank values with 0

    # reduce variables
    df_corn = df_corn[['State', 'sw_ethanol_corn', 'gw_ethanol_corn']]

    # prep corn production data
    df_corn_prod = df_corn_prod.dropna(subset=["County ANSI"])  # drop unnamed counties
    df_corn_prod['County ANSI'] = df_corn_prod['County ANSI'].apply(lambda x: '{0:0>3}'.format(x))
    df_corn_prod['State ANSI'] = df_corn_prod['State ANSI'].apply(lambda x: '{0:0>2}'.format(x))
    df_corn_prod["FIPS"] = df_corn_prod["State ANSI"] + df_corn_prod["County ANSI"]  # creat FIPS code from ANSI
    df_corn_prod = df_corn_prod[["State", "FIPS", "Value"]]  # reduce to required variables

    # determine corn growth by percent of state total corn production
    df_corn_prod_sum = df_corn_prod.groupby("State", as_index=False).sum()  # sum by state
    df_corn_prod_sum = df_corn_prod_sum[["State", "Value"]]  # reduce to required variables
    df_corn_prod_sum = df_corn_prod_sum.rename(columns={"Value": "state_total"})  # rename value column
    df_corn_prod = pd.merge(df_corn_prod, df_corn_prod_sum, how="left", on="State")  # merge state and total
    df_corn_prod["corn_frac"] = df_corn_prod["Value"] / df_corn_prod['state_total']  # county fraction of state total
    df_corn_prod = df_corn_prod[["State", "FIPS", "corn_frac"]]  # reduce to required variables
    df_corn_prod = df_corn_prod.rename(columns={"State": "State_name"})  # rename
    df_corn_prod['State_name'] = df_corn_prod['State_name'].str.lower()

    # change state full name to state abbreviation
    df_state_abb = df_state_abb[['State_name', 'State']]
    df_state_abb['State_name'] = df_state_abb['State_name'].str.lower()
    df_corn_prod = pd.merge(df_corn_prod, df_state_abb, how='left', on='State_name')

    # calculate corn for ethanol by county based on percent of state total corn growth
    df_corn_prod = pd.merge(df_corn_prod, df_corn, how='left', on='State')  # merge dataframes
    df_corn_prod['sw_ethanol_corn'] = df_corn_prod['sw_ethanol_corn'] * df_corn_prod['corn_frac']  # calc surface water
    df_corn_prod['gw_ethanol_corn'] = df_corn_prod['gw_ethanol_corn'] * df_corn_prod['corn_frac']  # calc groundwater

    # combine with full county list to get complete US water for corn irrigation for ethanol by county
    df_corn_prod = df_corn_prod[['FIPS', 'sw_ethanol_corn', 'gw_ethanol_corn']]  # reduce dataframe
    df_corn_prod = pd.merge(df_loc, df_corn_prod, how='left', on='FIPS')  # merge dataframes
    df_corn_prod.fillna(0, inplace=True)  # replace blank values with zero

    # rename columns for descriptive language
    df_corn_prod = df_corn_prod.rename(columns={'sw_ethanol_corn': 'fresh_surfacewater_biomass_ethanol_mgd'})
    df_corn_prod = df_corn_prod.rename(columns={'gw_ethanol_corn': 'fresh_groundwater_biomass_ethanol_mgd'})

    return df_corn_prod


def calc_pws_discharge() -> pd.DataFrame:
    """calculating public water supply demand for the commercial and industrial sectors along with total
        public water supply exports or imports for each row of dataset.

    :return:                DataFrame of public water supply demand by sector, pws imports, and pws exports

    """

    # read in cleaned water use data variables for 2015
    df = prep_water_use_2015(
        variables=["FIPS", 'State', 'County', 'total_pws_withdrawals_mgd', 'fresh_pws_residential_mgd',
                   'fresh_pws_thermoelectric_mgd'])

    # read in dataframe of commercial and industrial pws ratios
    df_pws = prep_public_water_supply_fraction()

    # merge dataframes
    df = pd.merge(df, df_pws, how="left", on=["FIPS", "State", "County"])

    # calculate public water supply deliveries to commercial and industrial sectors
    df['fresh_pws_commercial_mgd'] = df["commercial_pws_fraction"] \
                                     * (df['fresh_pws_residential_mgd'] + df['fresh_pws_thermoelectric_mgd'])
    df['fresh_pws_industrial_mgd'] = df["industrial_pws_fraction"] \
                                     * (df['fresh_pws_residential_mgd'] + df['fresh_pws_thermoelectric_mgd'])

    # calculate new total deliveries from public water supply to all sectors
    df['pws_deliveries_total_mgd'] = df['fresh_pws_residential_mgd'] + df['fresh_pws_thermoelectric_mgd'] \
                                     + df['fresh_pws_commercial_mgd'] + df['fresh_pws_industrial_mgd']

    # calculate public water supply imports and exports
    df['pws_imports_mgd'] = np.where(df['pws_deliveries_total_mgd'] - df['total_pws_withdrawals_mgd'] < 0,
                                     # if withdrawals < deliveries
                                     df['total_pws_withdrawals_mgd'] - df['pws_deliveries_total_mgd'],
                                     # import quantity
                                     0)

    df['pws_exports_mgd'] = np.where(df['pws_deliveries_total_mgd'] - df['total_pws_withdrawals_mgd'] > 0,
                                     # if withdrawals > deliveries
                                     df['total_pws_withdrawals_mgd'] - df['pws_deliveries_total_mgd'],
                                     # export quantity
                                     0)

    # calculate net exports
    df['pws_net_exports_mgd'] = df['pws_exports_mgd'] - df['pws_imports_mgd']

    df = df[["FIPS", 'State', 'County', 'total_pws_withdrawals_mgd', 'pws_deliveries_total_mgd',
             "fresh_pws_commercial_mgd", "fresh_pws_industrial_mgd", "pws_imports_mgd",
             'pws_exports_mgd', 'pws_net_exports_mgd']]

    return df
