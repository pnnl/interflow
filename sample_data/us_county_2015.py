import numpy as np
import pandas as pd


def convert_kwh_bbtu(x: float) -> float:
    """converts energy in kWh to energy in billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.000003412140

    return bbtu


def convert_mwh_bbtu(x: float) -> float:
    """converts energy in MWh to energy in billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.003412

    return bbtu


def prep_water_use_2015(variables=None, all_variables=False) -> pd.DataFrame:
    """prepares 2015 water use data from USGS. Includes modifications such as replacing non-numeric values,
    reducing available variables in output dataframe, renaming variables appropriately,
    and returning a dataframe of specified variables.

    :param variables:                   None if no specific variables required in addition to FIPS code, state name,
                                        and county name. Default is None, otherwise a list of additional
                                        variables to include in returned dataframe.
    :type variables:                    list

    :param all_variables:               Include all available variables in returned dataframe. Default is False.
    :type all_variables:                bool

    :return:                            DataFrame of a water withdrawal and consumption values for 2015
                                        at the county level
    """

    # read in 2015 USGS data
    df = pd.read_csv('input_data/usco2015v2.0.csv', skiprows=1, dtype={'FIPS': str})

    # replacing characters for missing data with value of zero
    df.replace("--", 0, inplace=True)

    # creating a dictionary of required variables from full dataset with required naming
    variables_list = ['FIPS', 'STATE', 'COUNTY', 'TP-TotPop',
                      'PS-WGWFr', 'PS-WSWFr', 'PS-WGWSa', 'PS-WSWSa',
                      'DO-PSDel', 'DO-WGWFr', 'DO-WSWFr',
                      'IN-WGWFr', 'IN-WSWFr', 'IN-WGWSa', 'IN-WSWSa',
                      'MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa', 'MI-WSWSa',
                      'IC-WGWFr', 'IC-WSWFr', 'IC-RecWW',
                      'IG-WGWFr', 'IG-WSWFr', 'IG-RecWW',
                      'LI-WGWFr', 'LI-WSWFr',
                      'AQ-WGWFr', 'AQ-WGWSa', 'AQ-WSWFr', 'AQ-WSWSa',
                      'IR-WGWFr', 'IR-WSWFr', 'IR-RecWW', 'IG-CUsFr', 'IC-CUsFr',
                      'IR-CUsFr', 'PS-Wtotl', 'PT-WGWFr', 'PT-WGWSa', 'PT-WSWFr',
                      'PT-WSWSa', 'PT-RecWW', 'PT-PSDel']

    # convert all columns that should be numerical to floats
    numerical_list = df.columns[6:]
    for col in numerical_list:
        df[col] = df[col].astype(float)

    # reduce dataframe to variables in dictionary
    df = df[variables_list]

    # add leading zeroes to FIPS Code
    df['FIPS'] = df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))

    # remove states not included in sample analysis
    state_remove_list = ['PR', 'VI']
    for state in state_remove_list:
        df = df[df.STATE != state]

    # rename identification variables
    df = df.rename(columns={'STATE': 'State', 'COUNTY': 'County'})

    # set crop irrigation values equal to total irrigation values if there are no separate crop values
    df['IC-WGWFr'] = np.where(((df['IC-WGWFr'] == 0) & (df['IR-WGWFr'] > 0) & (df['IG-WGWFr'] == 0)),
                              df['IR-WGWFr'],
                              df['IC-WGWFr'])

    df['IC-WSWFr'] = np.where(((df['IC-WSWFr'] == 0) & (df['IR-WSWFr'] > 0) & (df['IG-WSWFr'] == 0)),
                              df['IR-WSWFr'],
                              df['IC-WSWFr'])

    df['IC-RecWW'] = np.where(((df['IC-RecWW'] == 0) & (df['IR-RecWW'] > 0) & (df['IG-RecWW'] == 0)),
                              df['IR-WGWFr'],
                              df['IC-RecWW'])

    # return variables specified
    if variables is None and all_variables is False:
        variables = ['FIPS', "State", "County"]
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]

    return df


def calc_irrigation_consumption() -> pd.DataFrame:
    '''
    Takes 2015 USGS water flow data and calculates consumption fractions for crop irrigation and golf irrigation based
    on consumptive use in those subsectors. Additionally, water withdrawal values for crop irrigation are filled in
    with general irrigation values for counties with missing crop irrigation data.

    :return:                               Dataframe of 2015 water flow values and irrigation subsector consumption
                                            fractions
    '''

    # read in prepared 2015 USGS water data
    df = prep_water_use_2015(variables=['FIPS', 'State', 'County', 'IR-WGWFr', 'IR-WSWFr', 'IR-RecWW', 'IR-CUsFr',
                                        'IC-WGWFr', 'IC-WSWFr', 'IC-RecWW', 'IC-CUsFr',
                                        'IG-WGWFr', 'IG-WSWFr', 'IG-RecWW', 'IG-CUsFr'])

    # calculate fresh surface water consumption fractions for all irrigation to fill missing crop irrigation cells
    df['IR_CU_FSW_frac'] = np.where((df['IR-WGWFr'] + df['IR-WSWFr'] + df['IR-RecWW']) > 0,
                                    df['IR-CUsFr'] / (df['IR-WGWFr'] + df['IR-WSWFr'] + df['IR-RecWW']),
                                    0)

    # calculate fresh surface water consumption fractions for crop irrigation where data is available
    df['IC_CU_FSW_frac'] = np.where((df['IC-WGWFr'] + df['IC-WSWFr'] + df['IC-RecWW']) > 0,
                                    df['IC-CUsFr'] / (df['IC-WGWFr'] + df['IC-WSWFr'] + df['IC-RecWW']),
                                    0)

    # calculate fresh surface water consumption fractions for crop irrigation where data is available
    df['IG_CU_FSW_frac'] = np.where((df['IG-WGWFr'] + df['IG-WSWFr'] + df['IG-RecWW']) > 0,
                                    df['IG-CUsFr'] / (df['IG-WGWFr'] + df['IG-WSWFr'] + df['IG-RecWW']),
                                    0)

    # replacing consumption fractions for counties with >100% consumption with 100%
    df['IR_CU_FSW_frac'] = np.where(df['IR_CU_FSW_frac'] > 1, 1, df['IR_CU_FSW_frac'])  # general irrigation
    df['IC_CU_FSW_frac'] = np.where(df['IC_CU_FSW_frac'] > 1, 1, df['IC_CU_FSW_frac'])  # crop irrigation
    df['IG_CU_FSW_frac'] = np.where(df['IG_CU_FSW_frac'] > 1, 1, df['IG_CU_FSW_frac'])  # golf irrigation

    # set groundwater and reclaimed wastewater consumption fractions equal to fresh surface water
    df['IR_CU_FGW_frac'] = df['IR_CU_FSW_frac']  # general irrigation, groundwater
    df['IR_CU_RWW_frac'] = df['IR_CU_FSW_frac']  # general irrigation, reclaimed wastewater

    df['IC_CU_FGW_frac'] = df['IC_CU_FSW_frac']  # crop irrigation, groundwater
    df['IC_CU_RWW_frac'] = df['IC_CU_FSW_frac']  # crop irrigation, reclaimed wastewater

    df['IG_CU_FGW_frac'] = df['IG_CU_FSW_frac']  # golf irrigation, groundwater
    df['IG_CU_RWW_frac'] = df['IG_CU_FSW_frac']  # golf irrigation, reclaimed wastewater

    # list of states that do not have specific crop and golf irrigation values, just total irrigation
    state_irrigation_adj_list = ['AR', 'HI', 'LA', 'MS', 'MO', 'MT', 'NE', 'NJ', 'ND',
                                 'OK', 'SD', 'TX', 'WI', 'WY', 'PR', 'VI']

    # fills crop irrigation values with total irrigation withdrawal and consumption values for states in list
    for state in state_irrigation_adj_list:
        # withdrawals
        df['IC-WSWFr'] = np.where(df['State'] == state, df['IR-WSWFr'], df['IC-WSWFr'])  # fresh surface water
        df['IC-WGWFr'] = np.where(df['State'] == state, df['IR-WGWFr'], df['IC-WGWFr'])  # fresh groundwater
        df['IC-RecWW'] = np.where(df['State'] == state, df['IR-RecWW'], df['IC-RecWW'])  # reclaimed wastewater

        # consumption fractions
        df['IC_CU_FSW_frac'] = np.where(df['State'] == state, df['IR_CU_FSW_frac'],
                                        df['IC_CU_FSW_frac'])  # fresh surface
        df['IC_CU_FGW_frac'] = np.where(df['State'] == state, df['IR_CU_FGW_frac'],
                                        df['IC_CU_FGW_frac'])  # fresh ground
        df['IC_CU_RWW_frac'] = np.where(df['State'] == state, df['IR_CU_RWW_frac'],
                                        df['IC_CU_RWW_frac'])  # reclaimed

    # set interbasin transfer to crop irrigation consumption equal to fresh surface water consumption
    df['IC_CU_ibt_frac'] = df['IC_CU_FSW_frac']

    # rename variables
    variable_dict = {'FIPS': 'FIPS',
                     'State': 'State',
                     'County': 'County',
                     'IC_CU_FSW_frac': 'AGR_crop_fresh_surfacewater_withdrawal_mgd',
                     'IC_CU_FGW_frac': 'AGR_crop_fresh_groundwater_withdrawal_mgd',
                     'IC_CU_RWW_frac': 'AGR_crop_reclaimed_wastewater_import_mgd',
                     'IG_CU_FSW_frac': 'AGR_golf_fresh_surfacewater_withdrawal_mgd',
                     'IG_CU_FGW_frac': 'AGR_golf_fresh_groundwater_withdrawal_mgd',
                     'IG_CU_RWW_frac': 'AGR_golf_reclaimed_wastewater_import_mgd',
                     'IC_CU_ibt_frac': 'AGR_crop_ibt_total_import_mgd'}
    df = df[variable_dict]
    df = df.rename(columns=variable_dict)

    flow_list = ['AGR_crop_fresh_surfacewater_withdrawal_mgd', 'AGR_crop_fresh_groundwater_withdrawal_mgd',
                 'AGR_crop_reclaimed_wastewater_import_mgd', 'AGR_golf_fresh_surfacewater_withdrawal_mgd',
                 'AGR_golf_fresh_groundwater_withdrawal_mgd', 'AGR_golf_reclaimed_wastewater_import_mgd',
                 'AGR_crop_ibt_total_import_mgd' ]

    ## consumption name adder
    adder = '_to_CMP_total_total_total_total_mgd_fraction'

    for var in flow_list:
        df = df.rename(columns={var: var + adder})

    return df


# below is correct and ready
def rename_water_data_2015(variables=None, all_variables=False) -> pd.DataFrame:
    '''
    Takes USGS 2015 flow values and calculated consumption fractions and renames them for higher description.

    :return:                 returns a DataFrame of 2015 water flows and consumption fractions for agriculture
    '''

    # read in USGS 2015 flows and irrigation consumption calculations
    df = prep_water_use_2015(all_variables=True)

    # read in renaming data
    df_names = pd.read_csv('input_data/variable_rename_key.csv')

    # convert to dictionary
    df_names = dict(zip(df_names.original_name, df_names.new_name))

    # rename columns based on dictionary
    df.rename(columns=df_names, inplace=True)

    # return variables specified
    if variables is None and all_variables is False:
        variables = ['FIPS', "State", "County"]
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]

    return df


def calc_population_county_weight(df: pd.DataFrame) -> pd.DataFrame:
    """calculates the percentage of state total population by county and merges to provided dataframe
    by 'State'. Used in splitting up state-level estimates to the county level.

    :return:                DataFrame of water consumption fractions for various sectors by county

    """

    # read in USGS 2015 dataset
    df_state = rename_water_data_2015(all_variables=True)

    # collect required columns
    df_state = df_state[['FIPS', 'State', 'County', 'population']]

    # sum population data by state to get total state population
    df_state_sum = df_state.groupby("State", as_index=False).sum()
    df_state_sum = df_state_sum.rename(columns={"population": "state_pop_sum"})  # rename state total pop. column

    # merge state total back to county-level population dataframe
    df_state = pd.merge(df_state, df_state_sum, how='left', on='State')

    # calculate population weight as county population divided by state total population
    df_state['pop_weight'] = df_state['population'] / df_state['state_pop_sum']

    # reduce to required output columns
    df_state = df_state[['FIPS', 'State', 'County', 'pop_weight']]

    # merge back with county level dataframe
    df_state = pd.merge(df, df_state, how="left", on="State")

    return df_state


# BELOW IS COMPLETE AND WORKING
def prep_water_use_1995(variables=None, all_variables=False) -> pd.DataFrame:
    """prepping 1995 water use data from USGS by replacing missing values, fixing FIPS codes,
     and reducing to needed variables

    :return:                DataFrame of water values for 1995 at the county level

    """
    # read in 1995 water data
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

    # remove puerto rico and virgin islands values
    state_remove_list = ['PR', 'VI']
    for state in state_remove_list:
        df = df[df.State != state]

    # return variables specified in parameters
    if variables is None and all_variables is False:
        variables = ['FIPS']
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]

    return df


# BELOW IS COMPLETE AND WORKING
def calc_irrigation_conveyance_loss_fraction(loss_cap=True, loss_cap_amt=.90) -> pd.DataFrame:
    """
    This function calculates the fraction of water lost during conveyance for irrigation (Crop and golf) for surface
    water, groundwater, and reused wastewater. The fraction is calculated as water lost in conveyance of irrigation
    water divided by total water withdrawn for irrigation. States with no conveyance losses were replaced with the
    country average. Counties with missing values were replaced with the state average.

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

    # calculate conveyance loss fraction of total water withdrawn for irrigation if irrigation water > 0
    df["loss_fraction"] = np.where(df['IR-WTotl'] > 0, df['IR-CLoss'] / df['IR-WTotl'], np.nan)

    # places a cap on the conveyance loss fraction
    if loss_cap:
        df["loss_fraction"] = np.where(df['loss_fraction'] > loss_cap_amt, loss_cap_amt, df["loss_fraction"])
    else:
        df["loss_fraction"] = df["loss_fraction"]

    # calculate state averages
    df_mean = df.groupby('State', as_index=False).mean()
    rename_list = df_mean.columns[1:].to_list()
    for col in rename_list:
        new_name = f"{col}_state"
        df_mean = df_mean.rename(columns={col: new_name})

    # fill states with 0 values with US average
    fill_list = df_mean.columns[1:].to_list()
    for col in fill_list:
        df_mean[col].replace(0, np.nan, inplace=True)  # replace 0 values with blanks so they are not included in avg
        df_mean[col].fillna(df_mean[col].mean(), inplace=True)  # fill blank values with average

    # fill counties with missing conveyance loss with state averages
    df_mean_all = pd.merge(df, df_mean, how='left', on=['State'])

    # replace counties with fractions of zero with the state average to replace missing data
    rep_list = df.columns[2:].to_list()  # county values to replace
    for col in rep_list:
        mean_name = f"{col}_state"
        df_mean_all[col].fillna(df_mean_all[mean_name], inplace=True)

    # reduce to required variables
    df_output = df_mean_all[['FIPS', 'State', 'loss_fraction']].copy()

    # assign conveyance loss value to crop and golf irrigation from surface, ground, and reuse
    created_variable_list = ['AGR_crop_fresh_surfacewater_withdrawal_mgd',
                             'AGR_crop_fresh_groundwater_withdrawal_mgd',
                             'AGR_crop_reclaimed_wastewater_import_mgd',
                             'AGR_crop_ibt_total_import_mgd',
                             'AGR_golf_fresh_surfacewater_withdrawal_mgd',
                             'AGR_golf_fresh_groundwater_withdrawal_mgd',
                             'AGR_golf_reclaimed_wastewater_import_mgd']

    # assign loss fraction to each variable name and add flow name information to discharge
    for var in created_variable_list:
        df_output[var] = df_output["loss_fraction"]
        df_output = df_output.rename(columns={var: var + "_to_CVL_total_total_total_total_mgd_fraction"})

    df_output = df_output.drop(['loss_fraction'], axis=1)

    # merge with full list of counties from 2015 water data
    df_output = pd.merge(df_loc, df_output, how='left', on=['FIPS', 'State'])

    return df_output


# Below is correct and should be included in output (Includes all discharges from crop and golf irrigation
def calc_irrigation_discharge_flows():
    """ Recalculates the consumption fractions for crop and golf irrigation given the calculated conveyance loss
        fractions. Returns irrigation discharges to consumption, conveyance losses, and surface discharge. The fraction
        sent to consumption is assumed to be the prior consumption fraction multiplied by any remaining water after
        conveyance losses. Surface discharge fraction is calculated as any remaining percentage after consumption.

    :return:                                        Dataframe of recalculated irrgiation consumption fractions,
                                                    conveyance losses, and surface discharge
    """

    # create subsector flow variable list
    variable_list = ['AGR_crop_fresh_surfacewater_withdrawal_mgd',
                     'AGR_crop_fresh_groundwater_withdrawal_mgd',
                     'AGR_crop_reclaimed_wastewater_import_mgd',
                     'AGR_crop_ibt_total_import_mgd',
                     'AGR_golf_fresh_surfacewater_withdrawal_mgd',
                     'AGR_golf_fresh_groundwater_withdrawal_mgd',
                     'AGR_golf_reclaimed_wastewater_import_mgd']

    # build full flow names for both consumption and conveyance losses
    consumption_flow_variables = [var + '_to_CMP_total_total_total_total_mgd_fraction' for var in variable_list]

    # read in consumption flow variables from renamed 2015 USGS water data
    consumption_flow_variables.extend(['FIPS', 'State', 'County'])
    cons_df = calc_irrigation_consumption()
    cons_df = cons_df[consumption_flow_variables]

    # read in calculated irrigation conveyance losses
    loss_df = calc_irrigation_conveyance_loss_fraction()

    # merge data frames
    df = pd.merge(cons_df, loss_df, how='left', on=['FIPS', 'State', 'County'])

    # calculate percent of water remaining after conveyance losses
    for var in variable_list:
        conveyance_loss_var = var + '_to_CVL_total_total_total_total_mgd_fraction'
        remaining_loss_flow_variable = var + '_to_CVL_total_total_total_total_mgd_fraction' + "_rem"
        df[remaining_loss_flow_variable] = 1 - df[conveyance_loss_var]

        # set consumption fraction equal to the previous consumption fraction * the percent of water remaining
        consumption_var = var + '_to_CMP_total_total_total_total_mgd_fraction'
        df[consumption_var] = df[consumption_var] * df[remaining_loss_flow_variable]

        # calculate any remaining percentage as discharge to surface water
        surface_discharge_var = var + '_to_SRD_total_total_total_total_mgd_fraction'
        df[surface_discharge_var] = 1 - (df[consumption_var] + df[conveyance_loss_var])

    return df


# BELOW IS COMPLETE AND WORKING
def prep_consumption_fraction() -> pd.DataFrame:
    """prepping water consumption fractions for sectors not included in the 2015 USGS water datset by using the
    consumptive use estimates in the 1995 USGS dataset. For Residential and Commercial sectors it is assumed that
    all water consumed is fresh water. For the Industrial and Mining sectors, separate fresh and saline consumption
    fractions are  calculated.

    :return:                DataFrame of consumption fractions for residential, commercial, industrial, mining,
                            livestock, and aquaculture sectors.

    """

    # read in 1995 water use data variables
    df = prep_water_use_1995(variables=['FIPS', 'State', 'DO-CUTot', 'DO-WDelv', 'CO-CUTot', 'CO-WDelv', 'IN-CUsFr',
                                        'IN-WFrTo', 'IN-PSDel', 'IN-CUsSa', "IN-WSaTo", "MI-CUsFr",
                                        "MI-WFrTo", "MI-CUsSa", "MI-WSaTo", "LV-CUsFr", "LV-WFrTo",
                                        "LA-CUsFr", "LA-WFrTo", "LA-CUsSa", "LA-WSaTo"])

    # read in full 2015 county list
    df_loc = prep_water_use_2015()  # prepared dataframe of 2015 FIPS codes, county names, and state names

    # read in variable naming key data
    df_rename = pd.read_csv('input_data/variable_rename_key_1995water.csv')
    # convert to dictionary
    rename_dict = dict(zip(df_rename.original_name, df_rename.new_name))

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

    # Replacing infinite (from divide by zero) with with null
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

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

    # creating a list of required variables
    variables_list = ['FIPS', 'State', 'DO_sCF_Fr', 'CO_sCF_Fr', 'IN_sCF_Fr', 'IN_sCF_Sa', 'MI_sCF_Fr', 'MI_sCF_Sa',
                      'LV_sCF_Fr', 'LA_sCF_Fr', 'LA_sCF_Sa', 'DO_gCF_Fr', 'DO_pCF_Fr', 'IN_gCF_Fr', 'IN_gCF_Sa',
                      'IN_pCF_Fr', 'MI_gCF_Fr', 'MI_gCF_Sa', 'LV_gCF_Fr', 'LA_gCF_Fr', 'LA_gCF_Sa']

    # reduce full dataframe to required variable list
    df = df[variables_list]

    # replace consumption fractions greater than 1 with 1
    column_list = variables_list[2:]
    for col in column_list:
        df[col] = np.where(df[col] > 1, 1, df[col])

    # calculate the mean consumption fraction in each state for each sector
    df_mean = df.groupby('State', as_index=False).mean()
    rename_list = df_mean.columns[1:].to_list()
    for col in rename_list:
        new_name = f"{col}_state"
        df_mean = df_mean.rename(columns={col: new_name})

    # fill blank values in state averages with total US averages
    fill_list = df_mean.columns[1:].to_list()
    for col in fill_list:
        df_mean.fillna(df_mean[col].mean(), inplace=True)

    # merge state averages back to main county level dataframe
    df_all = pd.merge(df, df_mean, how='left', on=['State'])

    # replace counties with missing consumption fractions with the state average
    rep_list = df.columns[2:].to_list()
    for col in rep_list:
        mean_name = f"{col}_state"
        df_all[col].fillna(df_all[mean_name], inplace=True)

    # reduce output to required variables
    df_all = df_all[rename_dict]

    # rename columns to add descriptive language from key
    df_all.rename(columns=rename_dict, inplace=True)

    # merge with full list of counties from 2015 USGS water data
    df_all = pd.merge(df_loc, df_all, how='left', on=['FIPS', 'State'])

    # add leading zeroes to FIPS Code
    df_all['FIPS'] = df_all['FIPS'].apply(lambda x: '{0:0>5}'.format(x))

    return df_all


# below is complete, do not include in output
def prep_public_water_supply_fraction() -> pd.DataFrame:
    """calculates public water supply deliveries for the commercial and industrial sectors individually
     as a ratio to the sum of public water supply deliveries to residential end users and thermoelectric cooling.
     Used in calculation of public water supply demand to commercial and industrial sectors.

    :return:                DataFrame of public water supply ratios for commercial and industrial sector.

    """

    # read in data
    df = prep_water_use_1995(variables=['FIPS', 'State', 'PS-DelDO', 'PS-DelPT', 'PS-DelCO', 'PS-DelIN'])
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # calculate ratio of commercial pws to sum of domestic and thermoelectric cooling pws
    df['com_pws_fraction'] = np.where((df['PS-DelDO'] + df['PS-DelPT'] <= 0),
                                      np.nan, (df['PS-DelCO'] / (df['PS-DelDO'] + df['PS-DelPT'])))

    # calculate ratio of industrial pws to sum of domestic and thermoelectric cooling pws
    df["ind_pws_fraction"] = np.where(((df['PS-DelDO'] + df['PS-DelPT']) <= 0),
                                      np.nan, df['PS-DelIN'] / (df['PS-DelDO'] + df['PS-DelPT']))

    # reduce dataframe
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
        df_mean_all[col].fillna(df_mean_all[mean_name], inplace=True)

    # reduce dataframe to required output
    df_output = df_mean_all[['FIPS', 'State', 'com_pws_fraction', 'ind_pws_fraction']]

    # merge with full list of counties from 2015 water data
    df_output = pd.merge(df_loc, df_output, how='left', on=['FIPS', 'State'])

    return df_output


# BELOW IS COMPLETE AND READY
def calc_pws_commercial_industrial_flows() -> pd.DataFrame:
    """calculates public water deliveries to the commercial and industrial sectors based on ratios determined
    from 1995 USGS water dataset

    :return:                DataFrame of public water supply demand by commercial and industrial sector

    """

    # read in cleaned water use data variables for 2015
    df = rename_water_data_2015(
        variables=["FIPS", 'State', 'County', 'total_pws_withdrawals_mgd',
                   'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd',
                   'fresh_pws_thermoelectric_mgd'])

    # read in dataframe of commercial and industrial pws ratios
    df_pws = prep_public_water_supply_fraction()

    # merge dataframes
    df = pd.merge(df, df_pws, how="left", on=["FIPS", "State", "County"])

    # calculate public water supply deliveries to residential and thermoelectric cooling in total
    res_pwd_name = 'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'
    df['total_delivery'] = df[res_pwd_name] + df['fresh_pws_thermoelectric_mgd']

    # create variables names as flows
    com_pwd_name = 'COM_public_total_total_total_mgd'
    ind_pwd_name = 'IND_public_total_total_total_mgd'

    pwd_flow_name = '_from_PWD_total_total_total_total_mgd'

    com_pwd_name = com_pwd_name + pwd_flow_name
    ind_pwd_name = ind_pwd_name + pwd_flow_name

    # calculate public water deliveries to the commercial and industrial sector
    df[com_pwd_name] = df["com_pws_fraction"] * df['total_delivery']
    df[ind_pwd_name] = df["ind_pws_fraction"] * df['total_delivery']

    # reduce dataframe to required variables
    df = df[["FIPS", 'State', 'County', com_pwd_name, ind_pwd_name]]

    return df


# BELOW IS COMPLETE AND READy
def calc_discharge_fractions():
    """ Takes water flows to residential, commercial, industrial, mining, and nonirrigation agriculture sectors
        and calculates their discharge fractions to the surface and ocean.
        All water that is not consumed by these sectors is assumed to be discharged to either the surface or ocean.

    :return:
    """

    # load prepared consumption fraction data for sectors
    cons_df = prep_consumption_fraction()

    # residential, commercial, and industrial sectors
    cons_fraction_flow_adder = "_total_total_mgd_to_CMP_total_total_total_total_mgd_fraction"
    srd_fraction_flow_adder = "_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction"
    ocd_fraction_flow_adder = "_total_total_mgd_to_OCD_total_total_total_total_mgd_fraction"
    wws_fraction_flow_adder = "_total_total_mgd_to_WWS_total_total_total_total_mgd_fraction"

    public_water_list = ['RES_public_total', "COM_public_total", "IND_public_total"]

    fresh_water_list = ['RES_fresh_surfacewater', 'RES_fresh_groundwater', "IND_fresh_surfacewater",
                        "IND_fresh_groundwater"]

    saline_water_list = ["IND_saline_surfacewater", "IND_saline_groundwater"]

    # set output dataframe equal to consumption dataframe
    output_df = cons_df.copy()
    output_variable_list = []

    for item in public_water_list:
        consumption_name = item + cons_fraction_flow_adder
        wws_flow_name = item + wws_fraction_flow_adder
        output_df[wws_flow_name] = 1 - output_df[consumption_name]  # all public water not consumed is sent to WWS
        output_variable_list.append(wws_flow_name)
    for item in fresh_water_list:
        consumption_name = item + cons_fraction_flow_adder
        srd_flow_name = item + srd_fraction_flow_adder
        output_df[srd_flow_name] = 1 - output_df[consumption_name]  # all fresh water not consumed sent to surface
        output_variable_list.append(srd_flow_name)
    for item in saline_water_list:
        consumption_name = item + cons_fraction_flow_adder
        ocd_flow_name = item + ocd_fraction_flow_adder
        output_df[ocd_flow_name] = 1 - output_df[consumption_name]  # all saline water not consumed sent to ocean
        output_variable_list.append(ocd_flow_name)

    # mining sector
    mining_freshwater_list = ["MIN_other_total_fresh_surfacewater", "MIN_other_total_fresh_groundwater"]
    mining_salinewater_list = ["MIN_other_total_saline_surfacewater", "MIN_other_total_saline_groundwater"]

    min_cons_fraction_flow_adder = "_mgd_to_CMP_total_total_total_total_mgd_fraction"
    min_srd_fraction_flow_adder = "_mgd_to_SRD_total_total_total_total_mgd_fraction"
    min_ocd_fraction_flow_adder = "_mgd_to_OCD_total_total_total_total_mgd_fraction"

    for item in mining_freshwater_list:
        consumption_name = item + min_cons_fraction_flow_adder
        srd_flow_name = item + min_srd_fraction_flow_adder
        output_df[srd_flow_name] = 1 - output_df[consumption_name]  # all fresh water not consumed sent to surface
        output_variable_list.append(srd_flow_name)

    for item in mining_salinewater_list:
        consumption_name = item + min_cons_fraction_flow_adder
        ocd_flow_name = item + min_ocd_fraction_flow_adder
        output_df[ocd_flow_name] = 1 - output_df[consumption_name]  # all saline water not consumed sent to ocean
        output_variable_list.append(ocd_flow_name)

    # non-irrigation agriculture sectors
    agr_freshwater_list = ['AGR_livestock_fresh_groundwater_withdrawal', 'AGR_livestock_fresh_surfacewater_withdrawal',
                           'AGR_aquaculture_fresh_surfacewater_withdrawal',
                           'AGR_aquaculture_fresh_groundwater_withdrawal']

    agr_salinewater_list = ["AGR_aquaculture_saline_surfacewater_withdrawal",
                            "AGR_aquaculture_saline_groundwater_withdrawal"]

    agr_cons_fraction_flow_adder = "_mgd_to_CMP_total_total_total_total_mgd_fraction"
    agr_srd_fraction_flow_adder = "_mgd_to_SRD_total_total_total_total_mgd_fraction"
    agr_ocd_fraction_flow_adder = "_mgd_to_OCD_total_total_total_total_mgd_fraction"

    for item in agr_freshwater_list:
        consumption_name = item + agr_cons_fraction_flow_adder
        srd_flow_name = item + agr_srd_fraction_flow_adder
        output_df[srd_flow_name] = 1 - output_df[consumption_name]  # all fresh water not consumed sent to surface
        output_variable_list.append(srd_flow_name)

    for item in agr_salinewater_list:
        consumption_name = item + agr_cons_fraction_flow_adder
        ocd_flow_name = item + agr_ocd_fraction_flow_adder
        output_df[ocd_flow_name] = 1 - output_df[consumption_name]  # all saline water not consumed sent to ocean
        output_variable_list.append(ocd_flow_name)

    return output_df

# BELOW IS GOOD TO GO
def prep_irrigation_pws_ratio() -> pd.DataFrame:
    """prepping the ratio of water flows to irrigation vs. water flows to public water supply by county. Used to
    determine the split of electricity in interbasin transfers between the two sectors.

    :return:                DataFrame of percentages by county

    """
    # read data
    df_irr_pws = prep_water_use_2015(variables=['FIPS', 'State', 'County', 'IC-WGWFr', 'IC-WSWFr', 'PS-Wtotl'])

    # calculate public water supply percent of combined flows
    total_crop_irr = df_irr_pws['IC-WGWFr'] + df_irr_pws['IC-WSWFr']

    df_irr_pws['pws_ibt_pct'] = df_irr_pws['PS-Wtotl'] / (total_crop_irr + df_irr_pws['PS-Wtotl'])

    # add in column for irrigation fraction (1-pws)
    df_irr_pws['irrigation_ibt_pct'] = 1 - df_irr_pws['pws_ibt_pct']

    # fill counties that have zero values with average
    df_irr_pws['irrigation_ibt_pct'].fillna(df_irr_pws['irrigation_ibt_pct'].mean(), inplace=True)
    df_irr_pws['pws_ibt_pct'].fillna(df_irr_pws['pws_ibt_pct'].mean(), inplace=True)

    # reduce dataframe variables
    df_irr_pws = df_irr_pws[['FIPS', 'State', 'County', 'pws_ibt_pct', 'irrigation_ibt_pct']]

    return df_irr_pws

# BELOW IS GOOD TO GO
def prep_interbasin_transfer_data() -> pd.DataFrame:
    """Prepares interbasin water transfer data so that output is a dataframe of energy use (BBTU) and total
        water transferred for irrigation and public water supply in total.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in TX interbasin transfer
    data_tx = 'input_data/TX_IBT_2015.csv'
    df_tx = pd.read_csv(data_tx, dtype={'Used_FIPS': str, 'Source_FIPS': str})

    # get_west_inter_basin_transfer_data
    data_west = 'input_data/West_IBT_county.csv'
    df_west = pd.read_csv(data_west, dtype={'FIPS': str})

    # read in pws to irr water ratio
    df_ratio = prep_irrigation_pws_ratio()
    df_loc = prep_water_use_2015()  # full county list

    feet_meter_conversion = 1 / 3.281  # feet to meter conversion
    af_mps_conversion = 1 / 25567  # acre-ft-year to meters per second^3 conversion
    mps_mgd = 22.82  # cubic meters per second to million gallons per day
    cfs_mgd = 0.646317  # cubic feet per second to million gallons per day
    afy_mgd = 0.000892742  # acre foot per year to million gallons per day

    pump_eff = .65  # assumed pump efficiency rate
    acc_gravity = 9.81  # Acceleration of gravity  (m/s^2)
    water_density = 997  # Water density (kg/m^3)

    # calculate texas interbasin transfer energy
    elevation_meters = df_tx["Elevation Difference (Feet)"] * feet_meter_conversion  # elevation in meters
    mps_cubed = df_tx["Total_Intake__Gallons (Acre-Feet/Year)"] * af_mps_conversion  # meters per second cubed
    mgd_tx = mps_cubed * mps_mgd
    df_tx["water_interbasin_mgd"] = mgd_tx / 2  # dividing in half to split across source and target counties

    interbasin_mwh = ((elevation_meters * mps_cubed * acc_gravity * water_density) / pump_eff) / (10 ** 6)
    interbasin_bbtu = convert_mwh_bbtu(interbasin_mwh)  # convert mwh to bbtu
    df_tx["electricity_interbasin_bbtu"] = interbasin_bbtu / 2  # dividing in half to split across both counties

    # split out target county data
    df_tx_target = df_tx[["State", "Used_FIPS", "electricity_interbasin_bbtu", "water_interbasin_mgd"]].copy()
    df_tx_target = df_tx_target.rename(columns={"Used_FIPS": "FIPS"})

    # split out source county data
    df_tx_source = df_tx[["State", "Source_FIPS", "electricity_interbasin_bbtu", "water_interbasin_mgd"]].copy()
    df_tx_source = df_tx_source.rename(columns={"Source_FIPS": "FIPS"})

    # stack source and target county interbasin transfer data
    dataframe_list = [df_tx_target, df_tx_source]
    df_tx = pd.concat(dataframe_list)

    # group by state and county fips code
    df_tx = df_tx.groupby(["State", "FIPS"], as_index=False).sum()

    # calculate energy intensity per mgd
    df_tx['ibt_energy_intensity_bbtu'] = df_tx["electricity_interbasin_bbtu"] / df_tx["water_interbasin_mgd"]

    df_tx = df_tx[["State", "FIPS", 'ibt_energy_intensity_bbtu', "water_interbasin_mgd"]]

    # prep western state interbasin transfer energy
    df_west = df_west[['FIPS', 'Mwh/yr (Low)', 'Mwh/yr (High)', 'Water Delivery (AF/yr)', 'cfs']]
    df_west['FIPS'] = df_west['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero to fips

    df_west["electricity_interbasin_bbtu"] = (df_west["Mwh/yr (Low)"] + df_west[
        "Mwh/yr (High)"]) / 2  # average energy use by row
    df_west = df_west.groupby(["FIPS"], as_index=False).sum()  # group by county fips code
    df_west["electricity_interbasin_bbtu"] = convert_mwh_bbtu(
        df_west["electricity_interbasin_bbtu"])  # convert mwh values to bbtu

    # convert to bbtu per day rather than bbtu per year
    df_west["electricity_interbasin_bbtu"] = df_west["electricity_interbasin_bbtu"] / 365

    # calculate a single water flow value in mgd
    df_west['water_interbasin_mgd'] = np.where(df_west['cfs'] > 0, cfs_mgd * df_west['cfs'], 0)
    df_west['water_interbasin_mgd'] = np.where((df_west['cfs'] == 0) & (df_west['Water Delivery (AF/yr)'] > 0),
                                               afy_mgd * df_west['Water Delivery (AF/yr)'],
                                               df_west['water_interbasin_mgd'])

    # calculate the energy intensity
    df_west['ibt_energy_intensity_bbtu'] = df_west["electricity_interbasin_bbtu"] / df_west['water_interbasin_mgd']

    # bring west IBT data together with TX data
    ibt_dataframe_list = [df_tx, df_west]
    df = pd.concat(ibt_dataframe_list)
    df = df[["FIPS", 'ibt_energy_intensity_bbtu', 'water_interbasin_mgd']]

    # merge data with pws and irrigation ratio data
    df = pd.merge(df, df_ratio, how='left', on='FIPS')

    crop_with_name = 'AGR_crop_ibt_total_import_mgd'
    pws_with_name = 'PWS_fresh_surfacewater_import_total_mgd'
    ibt_flow_name = '_from_WSI_ibt_fresh_surfacewater_total_mgd'

    # creates water flows to each sector from ibt imports
    df[crop_with_name + ibt_flow_name] = df['water_interbasin_mgd'] * df['irrigation_ibt_pct']
    df[pws_with_name + ibt_flow_name] = df['water_interbasin_mgd'] * df['pws_ibt_pct']

    # create prefix for energy flow name
    crop_energy_name = 'AGR_crop_ibt_total_import_bbtu'
    pws_energy_name = 'PWS_ibt_total_total_total_bbtu'

    # create energy intensity names and assign values
    df[crop_energy_name + '_from_' + crop_with_name + '_intensity'] = df['ibt_energy_intensity_bbtu']
    df[pws_energy_name + '_from_' + pws_with_name + '_intensity'] = df['ibt_energy_intensity_bbtu']

    # create prefix for energy flow name
    rejected_energy_suffix = '_to_REJ_total_total_total_total_bbtu_fraction'
    energy_services_suffix = '_to_ESV_total_total_total_total_bbtu_fraction'

    # create rejected energy flows
    df[crop_energy_name + rejected_energy_suffix] = 1 - pump_eff
    df[pws_energy_name + rejected_energy_suffix] = 1 - pump_eff

    # create energy service flows
    df[crop_energy_name + energy_services_suffix] = pump_eff
    df[pws_energy_name + energy_services_suffix] = pump_eff

    # create energy source names
    electricity_name = '_from_EGD_total_total_total_total_bbtu_fraction'

    # create energy source flow values, set 100% to electricity
    df[crop_energy_name + electricity_name] = 1
    df[pws_energy_name + electricity_name] = 1

    # merge with county data to distribute value to each county in a state
    df = pd.merge(df_loc, df, how='left', on=['FIPS', 'State', 'County'])
    df.fillna(0, inplace=True)

    df = df.drop(['ibt_energy_intensity_bbtu', 'water_interbasin_mgd','pws_ibt_pct','irrigation_ibt_pct'], axis=1)

    return df


# TODO, need to add pws interbasin transfers to this total
def prep_pws_to_pwd():
    '''preparing variables for connection'''

    df = prep_water_use_2015(variables=['FIPS', 'State', 'County',
                                        'PWS_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                                        'PWS_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                                        'PWS_saline_groundwater_withdrawal_total_mgd_from_WSW_saline_groundwater_total_total_mgd',
                                        'PWS_saline_surfacewater_withdrawal_total_mgd_from_WSW_saline_surfacewater_total_total_mgd',
                                        'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'])

    df2 = calc_pws_deliveries()

    df = pd.merge(df, df2, how='left', on=['FIPS', 'State', 'County'])

    out_df = prep_water_use_2015()

    # res, com, ind
    res_flow = 'RES_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'
    com_flow = 'COM_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'
    ind_flow = 'IND_public_total_total_total_mgd_from_PWD_total_total_total_total_mgd'
    df['total_pwd'] = df[res_flow] + df[com_flow] + df[ind_flow]

    # 2015 water flows
    fgw_flow = 'PWS_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd'
    fsw_flow = 'PWS_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd'
    sgw_flow = 'PWS_saline_groundwater_withdrawal_total_mgd_from_WSW_saline_groundwater_total_total_mgd'
    ssw_flow = 'PWS_saline_surfacewater_withdrawal_total_mgd_from_WSW_saline_surfacewater_total_total_mgd'

    df['total_pws'] = df[fgw_flow] + df[fsw_flow] + df[sgw_flow] + df[ssw_flow]

    fsw_frac = df[fsw_flow] / df['total_pws']
    fgw_frac = df[fgw_flow] / df['total_pws']
    sgw_frac = df[sgw_flow] / df['total_pws']
    ssw_frac = df[ssw_flow] / df['total_pws']

    # determine the total amount of public water demand that can be supplied by public water supply
    df['net_supply'] = df['total_pws'] - df['total_pwd']

    # if net supply is > 0, then calculate exports and demand

    pws_fsw_exports = 'PWX_total_total_total_total_mgd_from_PWS_fresh_surfacewater_withdrawal_total_mgd'
    pws_fgw_exports = 'PWX_total_total_total_total_mgd_from_PWS_fresh_groundwater_withdrawal_total_mgd'
    pws_sgw_exports = 'PWX_total_total_total_total_mgd_from_PWS_saline_groundwater_withdrawal_total_mgd'
    pws_ssw_exports = 'PWX_total_total_total_total_mgd_from_PWS_saline_surfacewater_withdrawal_total_mgd'

    out_df[pws_fsw_exports] = np.where(df['net_supply'] > 0, df['net_supply'] * fsw_frac, 0)
    out_df[pws_fgw_exports] = np.where(df['net_supply'] > 0, df['net_supply'] * fgw_frac, 0)
    out_df[pws_sgw_exports] = np.where(df['net_supply'] > 0, df['net_supply'] * sgw_frac, 0)
    out_df[pws_ssw_exports] = np.where(df['net_supply'] > 0, df['net_supply'] * ssw_frac, 0)

    # if net supply is <0, then calculate imports to demand

    pws_imports = 'PWD_total_total_total_total_mgd_from_PWI_total_total_total_total_mgd'

    out_df[pws_imports] = np.where(df['net_supply'] < 0, abs(df['net_supply']), 0)

    # determine what goes to PWS from PWD

    fsw_PWD = 'PWD_total_total_total_total_mgd_from_PWS_fresh_surfacewater_withdrawal_total_mgd'
    fgw_PWD = 'PWD_total_total_total_total_mgd_from_PWS_fresh_groundwater_withdrawal_total_mgd'
    sgw_PWD = 'PWD_total_total_total_total_mgd_from_PWS_saline_groundwater_withdrawal_total_mgd'
    ssw_PWD = 'PWD_total_total_total_total_mgd_from_PWS_saline_surfacewater_withdrawal_total_mgd'

    out_df[fsw_PWD] = np.where(out_df[pws_imports] > 0, df[fsw_flow], fsw_frac * df['total_pwd'])
    out_df[fgw_PWD] = np.where(out_df[pws_imports] > 0, df[fgw_flow], fgw_frac * df['total_pwd'])
    out_df[sgw_PWD] = np.where(out_df[pws_imports] > 0, df[sgw_flow], sgw_frac * df['total_pwd'])
    out_df[ssw_PWD] = np.where(out_df[pws_imports] > 0, df[ssw_flow], ssw_frac * df['total_pwd'])

    return out_df


# BELOW IS READY TO GO
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
    advanced_infiltration_flows_mgd = 'WWD_advanced_infiltration_total_total_mgd_from_WWS_total_total_total_total_mgd'
    primary_infiltration_flows_mgd = 'WWD_primary_infiltration_total_total_mgd_from_WWS_total_total_total_total_mgd'
    secondary_infiltration_flows_mgd = 'WWD_secondary_infiltration_total_total_mgd_from_WWS_total_total_total_total_mgd'
    advanced_municipal_flows_mgd = 'WWD_advanced_municipal_total_total_mgd_from_WWS_total_total_total_total_mgd'
    primary_municipal_flows_mgd = 'WWD_primary_municipal_total_total_mgd_from_WWS_total_total_total_total_mgd'
    secondary_municipal_flows_mgd = 'WWD_secondary_municipal_total_total_mgd_from_WWS_total_total_total_total_mgd'

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
# FUNCTION BELOW IS GOOD TO GO
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


# FUNCTION BELOW IS CORRECT
def prep_electricity_fuel() -> pd.DataFrame:
    """
    Prepares fuel and generation data by power plant ID from EIA 923 data. Bins generation type, prime mover, and
    maps power plants to location information.

    :return:                            Dataframe of power plant fuel and generation data by plant ID.
    """

    # assumed efficiency level to fill missing values
    EFFICIENCY = .3

    # read in electricity generation data by power plant id
    data = 'input_data\EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.csv'
    df = pd.read_csv(data, skiprows=5)

    # read in power plant location data by power plant id
    df_gen_loc = prep_power_plant_location()
    df_loc = prep_water_use_2015()

    # read in cooling water withdrawal intensities
    water_data = 'input_data\cooling_water_intensities.csv'
    df_water = pd.read_csv(water_data)

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

    # changing from annual values to daily
    df['fuel_amt'] = df['fuel_amt'] / 365
    df['generation_mwh'] = df['generation_mwh'] / 365

    # dropping power plants with zero fuel use and zero output
    index_list = df[(df['fuel_amt'] <= 0) & (df['generation_mwh'] <= 0)].index  # list of indices with both zero values
    df.drop(index_list, inplace=True)  # dropping rows with zero fuel and zero generation amount

    # using fuel type dictionary to bin fuel types
    df['fuel_type'] = df['fuel_type'].map(fuel_consumption_dict)  # bin fuel types

    # using prime_mover_dict to bin prime mover types
    df['prime_mover'] = df['prime_mover'].map(prime_mover_dict)  # bin fuel types

    # remove pumped storage hydro from dataset
    df = df[df.prime_mover != 'pumpedstorage']

    # converting units to billion btu from million btu for fuel
    df["fuel_amt"] = df["fuel_amt"] / 1000

    # merge cooling water intensities with power plant data
    df = pd.merge(df, df_water, how='left', on='fuel_type')

    # calculate water withdrawals and consumption based on intensities
    df['water_withdrawal_mgd'] = (df['withdrawal (gal/mwh)'] * df['generation_mwh']) / 1000000

    # calculate water withdrawals and consumption based on intensities
    df['water_consumption_mgd'] = (df['consumption (gal/mwh)'] * df['generation_mwh']) / 1000000

    # converting generation to bbtu from mwh
    df['generation_bbtu'] = df['generation_mwh'].apply(convert_mwh_bbtu)

    # fill missing fuel amounts with 1/efficiency * generation
    df['fuel_amt'] = np.where(df['fuel_amt'] == 0, ((1 / EFFICIENCY) * df['generation_bbtu']), df['fuel_amt'])

    # grouping rows by both plant code and fuel type
    df = df.groupby(['plant_code', 'fuel_type', 'prime_mover'], as_index=False).sum()

    # merging power plant location data with power plant generation data
    df = pd.merge(df, df_gen_loc, how='left', on='plant_code')

    # reduce dataframe
    df = df[['plant_code', 'fuel_type', 'prime_mover', 'fuel_amt', 'water_withdrawal_mgd', 'water_consumption_mgd',
             'generation_bbtu', 'FIPS']]

    return df


# FUNCTION BELOW IS CORRECT
def prep_electricity_cooling() -> pd.DataFrame:
    """ Function maps cooling water data to power plant generation data and fills blank values.

    :return:
    """

    # read in electricity generation data
    df_gen = prep_electricity_fuel()

    # read in power plant cooling type data
    cooling_data = r'input_data\2015_TE_Model_Estimates_USGS.csv'
    df_cooling = pd.read_csv(cooling_data,
                             usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE', 'GENERATION_TYPE',
                                      'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])

    water_source_dict = {'SW': 'surfacewater',  # river, canal, bay
                         'GW': 'groundwater',  # well, aquifer
                         'PD': 'wastewater',  # PD = plant discharge
                         "-nr-": "surfacewater",  # all blanks assumed to be surface water
                         "GW & PD": "groundwater",  # all GW+PD are assumed to be groundwater only
                         "GW & SW": 'surfacewater',  # all GW+SW combinations are assumed to be SW
                         "OT": "surfacewater"  # all other assumed to be surface water
                         }

    water_type_dict = {'FR': 'fresh',
                       'SA': 'saline',
                       'OT': 'fresh',  # all other source is assumed to be fresh water
                       "FR & BE": 'fresh',  # all combinations with fresh and BE are assumed to be fresh
                       "BE": "fresh",  # reclaimed wastewater
                       "BR": "saline",  # all brackish should be changed to saline
                       "": "fresh"}  # fill blanks with fresh water

    cooling_dict = {'COMPLEX': 'complex',
                    'ONCE-THROUGH FRESH': 'oncethrough',
                    'RECIRCULATING TOWER': 'tower',
                    'RECIRCULATING POND': 'pond',
                    'ONCE-THROUGH SALINE': 'oncethrough'}

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

    # reduce dataset
    df_cooling = df_cooling[['EIA_PLANT_ID', 'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL',
                             'CONSUMPTION', 'SURFACE_DISCHARGE_MGD', 'OCEAN_DISCHARGE_MGD']]

    # rename plant ID column
    df_cooling = df_cooling.rename(columns={'EIA_PLANT_ID': 'plant_code'})

    # merge cooling information by plant ID with generation data by plant ID
    df_cooling = pd.merge(df_gen, df_cooling, how='left', on='plant_code')

    # create a list of generation that does not require cooling
    no_cool_list = ['hydro', 'wind', 'solar', 'geothermal']

    # fill values for power plants with no cooling (renewables)
    for item in no_cool_list:
        df_cooling["COOLING_TYPE"] = np.where(df_cooling['fuel_type'] == item, "nocooling", df_cooling["COOLING_TYPE"])
        df_cooling["WATER_SOURCE_CODE"] = np.where(df_cooling['fuel_type'] == item, "nocooling",
                                                   df_cooling["WATER_SOURCE_CODE"])
        df_cooling["WATER_TYPE_CODE"] = np.where(df_cooling['fuel_type'] == item, "nocooling",
                                                 df_cooling["WATER_TYPE_CODE"])
        df_cooling["WITHDRAWAL"] = np.where(df_cooling['fuel_type'] == item, 0, df_cooling["WITHDRAWAL"])
        df_cooling["CONSUMPTION"] = np.where(df_cooling['fuel_type'] == item, 0, df_cooling["CONSUMPTION"])
        df_cooling["SURFACE_DISCHARGE_MGD"] = np.where(df_cooling['fuel_type'] == item, 0,
                                                       df_cooling["SURFACE_DISCHARGE_MGD"])
        df_cooling["OCEAN_DISCHARGE_MGD"] = np.where(df_cooling['fuel_type'] == item, 0,
                                                     df_cooling["OCEAN_DISCHARGE_MGD"])

    # fill cooling type column blanks with 'complex'
    df_cooling["COOLING_TYPE"].fillna('complex', inplace=True)
    df_cooling["WATER_SOURCE_CODE"].fillna('surfacewater', inplace=True)
    df_cooling["WATER_TYPE_CODE"].fillna('fresh', inplace=True)

    # fill missing water values with Macknick et al. (2012) averages
    df_cooling["WITHDRAWAL"].fillna(df_cooling["water_withdrawal_mgd"], inplace=True)
    df_cooling["CONSUMPTION"].fillna(df_cooling["water_consumption_mgd"], inplace=True)

    # all filled values are assumed to be discharged to the surface
    df_cooling["SURFACE_DISCHARGE_MGD"].fillna(df_cooling["water_withdrawal_mgd"] - df_cooling["water_consumption_mgd"],
                                               inplace=True)
    df_cooling['OCEAN_DISCHARGE_MGD'].fillna(0, inplace=True)

    # reduce output dataset
    df_cooling = df_cooling[['plant_code', 'fuel_type', 'prime_mover', 'fuel_amt', 'generation_bbtu', 'FIPS',
                             'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL', 'CONSUMPTION',
                             'SURFACE_DISCHARGE_MGD', 'OCEAN_DISCHARGE_MGD']]

    return df_cooling


# FUNCTION BELOW IS CORRECT
def prep_generation_fuel_flows() -> pd.DataFrame:
    """ Function prepares data flows from fuel supply to electricity generation, electricity generation supply to
    electricity generation demand, and electricity generation to rejected energy.

    :return:
    """

    EFFICIENCY_ASSUMPTION = .30

    # load electricity generation and cooling data
    df = prep_electricity_cooling()

    # load data of all county FIPS codes from USGS 2015 dataset
    df_loc = prep_water_use_2015()

    # reduce dataframe to only include generation information, including cooling type
    df = df[['plant_code', 'fuel_type', 'prime_mover', 'fuel_amt', 'generation_bbtu', 'FIPS', 'COOLING_TYPE']]

    # create a combined name for fuel type, prime mover, and cooling type
    df['combo_name'] = 'EGS_' + df['fuel_type'] + "_" + df['prime_mover'] + "_" + df[
        'COOLING_TYPE'] + "_" + "total_bbtu"

    # combine power plants by FIPS code
    df = df.groupby(['FIPS', 'combo_name', 'fuel_type'], as_index=False).sum()

    # create a combine fuel name for fuel flows
    df['fuel_supply_name'] = df['combo_name'] + '_from_EPD_' + df['fuel_type'] + '_total_total_total_bbtu'

    # create a rejected energy flow fraction name
    df['rej_energy_name'] = df['combo_name'] + '_to_REJ_total_total_total_total_bbtu_fraction'

    # create an electricity demand flow fraction name
    df['elec_demand_name'] = df['combo_name'] + '_to_EGD_total_total_total_total_bbtu_fraction'

    # split out a separate fuel amount dataframe
    df_fuel = df[['FIPS', 'fuel_amt', 'fuel_supply_name']]

    # pivot to get fuel flows to electricity generation as columns
    df_fuel = pd.pivot_table(df_fuel, values='fuel_amt', index=['FIPS'], columns=['fuel_supply_name'],
                             aggfunc=np.sum)  # pivot
    df_fuel = df_fuel.reset_index()  # reset index to remove multi-index from pivot table
    df_fuel = df_fuel.rename_axis(None, axis=1)  # drop index name
    df_fuel.fillna(0, inplace=True)  # fill nan with zero

    # split out a separate rejected energy amount dataframe
    df_rej = df[['FIPS', 'fuel_amt', 'generation_bbtu', 'rej_energy_name', 'elec_demand_name']].copy()

    # calculated rejected energy flows
    df_rej['rejected_energy_bbtu'] = np.where(df_rej['fuel_amt'] > 0,
                                              df_rej['fuel_amt'] - df_rej['generation_bbtu'],
                                              (1 - EFFICIENCY_ASSUMPTION) * df_rej['fuel_amt'])

    # replace >100% efficiency flows with 30% efficiency assumption
    df_rej['rejected_energy_bbtu'] = np.where(df_rej['generation_bbtu'] > df_rej['fuel_amt'],
                                              (1 - EFFICIENCY_ASSUMPTION) * df_rej['fuel_amt'],
                                              df_rej['rejected_energy_bbtu'])

    # recalculated rejected energy as a fraction of fuel
    df_rej['rejected_energy_frac'] = np.where(df_rej['fuel_amt'] > 0,
                                              df_rej['rejected_energy_bbtu'] / df_rej['fuel_amt'],
                                              0)

    # calculate the amount of discharge to electricity generation demand as 1 - loss fraction
    df_rej['energy_service_frac'] = 1 - df_rej['rejected_energy_frac']

    # create a copy of the rejected energy dataframe to use later for energy service discharge
    df_esv = df_rej.copy()

    # pivot rejected energy dataframe to get a single row for each FIPS and rejected energy fractions as columns
    df_rej = pd.pivot_table(df_rej, values='rejected_energy_frac', index=['FIPS'], columns=['rej_energy_name'],
                            aggfunc=np.mean)  # pivot
    df_rej = df_rej.reset_index()  # reset index to remove multi-index from pivot table
    df_rej = df_rej.rename_axis(None, axis=1)  # drop index name
    df_rej.fillna(0, inplace=True)  # fill nan with zero

    # pivot energy service (discharge to demand) to get a single row for each FIPS
    df_esv = pd.pivot_table(df_esv, values='energy_service_frac', index=['FIPS'], columns=['elec_demand_name'],
                            aggfunc=np.mean)  # pivot
    df_esv = df_esv.reset_index()  # reset index to remove multi-index from pivot table
    df_esv = df_esv.rename_axis(None, axis=1)  # drop index name
    df_esv.fillna(0, inplace=True)  # fill nan with zero

    # merge each of the separate dataframes with the full list of FIPS counties
    df_fuel = pd.merge(df_loc, df_fuel, how='left', on='FIPS')
    df_fuel.fillna(0, inplace=True)

    df_rej = pd.merge(df_loc, df_rej, how='left', on='FIPS')
    df_rej.fillna(0, inplace=True)

    df_esv = pd.merge(df_loc, df_esv, how='left', on='FIPS')
    df_esv.fillna(0, inplace=True)

    # merge each of the separate dataframes into a single output dataframe
    output_df = pd.merge(df_fuel, df_rej, how='left', on=['FIPS', 'State', 'County'])
    output_df = pd.merge(output_df, df_esv, how='left', on=['FIPS', 'State', 'County'])

    return output_df


# FUNCTION BELOW IS CORRECT
def prep_electricity_cooling_flows() -> pd.DataFrame:
    """
    Prepares flows from water supply to thermoelectric cooling and water flows from thermoelectric cooling to
    consumption, surface discharge, and ocean discharge.

    :return:
    """
    # read in full list of FIPS counties from USGS 2015 dataset
    df_loc = prep_water_use_2015()

    # read in prepared cooling water data
    df = prep_electricity_cooling()

    # remove rows with no cooling water withdrawals
    df = df[df.WITHDRAWAL > 0]

    # create a cooling water withdrawal name
    df['withdrawal_name'] = 'WSW_' + df['WATER_TYPE_CODE'] + "_" + df['WATER_SOURCE_CODE'] + "_total_total_mgd"

    # create a reclaimed wastewater source name
    df['wastewater_name'] = 'WSI_reclaimed_wastewater_total_total_mgd'

    # create a generation target name
    df['generation_target_name'] = "EGS_" + df['fuel_type'] + "_" \
                                   + df['prime_mover'] + "_" + df['COOLING_TYPE'] + "_total_mgd"

    # create a consumption fraction discharge name
    df['consumption_name'] = "CMP_total_total_total_total_mgd_fraction"

    # create a surface discharge name
    df['sd_name'] = "SRD_total_total_total_total_mgd_fraction"

    # create an ocean discharge name
    df['od_name'] = "OCD_total_total_total_total_mgd_fraction"

    # create a copy of the dataframe to split out withdrawal flows
    df_withdrawal = df.copy()

    # create a full withdrawal flow name from either water supply or reclaimed wastewater
    df_withdrawal['withdrawal_name_full'] = np.where(df['WATER_SOURCE_CODE'] != "wastewater",
                                                     df_withdrawal['generation_target_name'] \
                                                     + "_from_" + df_withdrawal['withdrawal_name'],
                                                     df_withdrawal['generation_target_name'] \
                                                     + "_from_" + df_withdrawal['wastewater_name'])

    # pivot the withdrawal flows to get flows as columns and a single row per FIPS
    df_withdrawal = pd.pivot_table(df_withdrawal, values='WITHDRAWAL', index=['FIPS'], columns=['withdrawal_name_full'],
                                   aggfunc=np.sum)  # pivot
    df_withdrawal = df_withdrawal.reset_index()  # reset index to remove multi-index from pivot table
    df_withdrawal = df_withdrawal.rename_axis(None, axis=1)  # drop index name
    df_withdrawal.fillna(0, inplace=True)  # fill nan with zero

    # create a copy of the main dataframe for consumption fraction
    df_consumption = df.copy()

    # create a full consumption flow variable name
    df_consumption['consumption_name_full'] = df_consumption['generation_target_name'] \
                                              + "_to_" + df_consumption['consumption_name']

    # divide the total consumption by the total withdrawal to get consumption as a fraction
    df_consumption['CONSUMPTION_FRAC'] = df_consumption['CONSUMPTION'] / df_consumption['WITHDRAWAL']

    # pivot the consumption values to get a single row for each FIPS
    df_consumption = pd.pivot_table(df_consumption, values='CONSUMPTION_FRAC', index=['FIPS'],
                                    columns=['consumption_name_full'],
                                    aggfunc=np.mean)  # pivot
    df_consumption = df_consumption.reset_index()  # reset index to remove multi-index from pivot table
    df_consumption = df_consumption.rename_axis(None, axis=1)  # drop index name
    df_consumption.fillna(0, inplace=True)  # fill nan with zero

    # create a copy of the main dataframe for surface discharge fraction
    df_sd = df.copy()

    # create a full surface discharge fraction variable name
    df_sd['surface_name_full'] = df_sd['generation_target_name'] \
                                 + "_to_" + df_sd['sd_name']

    # divide the total surface discharge by the total withdrawal to get surface discharge as a fraction
    df_sd['SURFACE_DISCHARGE_MGD_FRAC'] = df_sd['SURFACE_DISCHARGE_MGD'] / df_sd['WITHDRAWAL']

    # pivot the consumption values to get a single row for each FIPS
    df_sd = pd.pivot_table(df_sd, values='SURFACE_DISCHARGE_MGD_FRAC', index=['FIPS'],
                           columns=['surface_name_full'],
                           aggfunc=np.mean)  # pivot
    df_sd = df_sd.reset_index()  # reset index to remove multi-index from pivot table
    df_sd = df_sd.rename_axis(None, axis=1)  # drop index name
    df_sd.fillna(0, inplace=True)  # fill nan with zero

    # create a copy of the main dataframe for ocean discharge fraction
    df_od = df.copy()

    # create a full surface discharge fraction variable name
    df_od['ocean_name_full'] = df_od['generation_target_name'] \
                               + "_to_" + df_od['od_name']

    # divide the total surface discharge by the total withdrawal to get surface discharge as a fraction
    df_od['OCEAN_DISCHARGE_MGD_FRAC'] = df_od['OCEAN_DISCHARGE_MGD'] / df_od['WITHDRAWAL']

    # pivot the consumption values to get a single row for each FIPS
    df_od = pd.pivot_table(df_od, values='OCEAN_DISCHARGE_MGD_FRAC', index=['FIPS'],
                           columns=['ocean_name_full'],
                           aggfunc=np.mean)  # pivot
    df_od = df_od.reset_index()  # reset index to remove multi-index from pivot table
    df_od = df_od.rename_axis(None, axis=1)  # drop index name
    df_od.fillna(0, inplace=True)  # fill nan with zero

    # combine each dataframe with the full list of FIPS counties
    df_withdrawal = pd.merge(df_loc, df_withdrawal, how='left', on='FIPS')
    df_withdrawal.fillna(0, inplace=True)

    df_consumption = pd.merge(df_loc, df_consumption, how='left', on='FIPS')
    df_consumption.fillna(0, inplace=True)

    df_sd = pd.merge(df_loc, df_sd, how='left', on='FIPS')
    df_sd.fillna(0, inplace=True)

    df_od = pd.merge(df_loc, df_od, how='left', on='FIPS')
    df_od.fillna(0, inplace=True)

    # combine all dataframes together into single output dataframes
    output_df = pd.merge(df_withdrawal, df_consumption, how='left', on=['FIPS', 'State', 'County'])
    output_df = pd.merge(output_df, df_sd, how='left', on=['FIPS', 'State', 'County'])
    output_df = pd.merge(output_df, df_od, how='left', on=['FIPS', 'State', 'County'])

    return output_df


# FUNCTION BELOW IS COMPLETE AND READY
def calc_hydro_water_intensity(intensity_cap=True, intensity_cap_amt=6000000) -> pd.DataFrame:
    """calculating the water use required for a bbtu of hydroelectric generation. Daily water use (mgd) is
    combined with daily generation from hydropower for each region from 1995 USGS data. Discharge and source
    fraction variables are also created.

    :return:                DataFrame of water intensity of hydroelectric generation by county

    """

    # read in data from 1995 water use
    df = prep_water_use_1995(variables=['FIPS', 'State', "HY-InUse", "HY-InPow"])  # 1995 hydropower data
    df_loc = prep_water_use_2015()  # prepared list of 2015 counties with FIPS codes

    # read in generation data for hydro to only include intensities for counties with hydro
    df_hydro = prep_generation_fuel_flows()

    df_hydro = df_hydro[['FIPS', 'State',
                         'EGS_hydro_instream_nocooling_total_bbtu_to_EGD_total_total_total_total_bbtu_fraction',
                         'EGS_hydro_instream_nocooling_total_bbtu_from_EPD_hydro_total_total_total_bbtu']]

    # convert from mwh of generation to bbtu
    df["HY-InPow"] = df["HY-InPow"].apply(convert_mwh_bbtu)

    # get daily power generation from annual generation
    df["HY-InPow"] = df["HY-InPow"] / 365

    # calculate water intensity fraction million gallons per bbtu
    hydro_name = 'EGS_hydro_instream_nocooling_total_mgd'
    water_intensity_name = hydro_name + '_from_EGS_hydro_instream_nocooling_total_bbtu_intensity'
    df[water_intensity_name] = np.where(df["HY-InPow"] > 0, (df["HY-InUse"] / df["HY-InPow"]), np.nan)

    # cap outlier intensities
    if intensity_cap:
        df[water_intensity_name] = np.where(df[water_intensity_name] >= intensity_cap_amt,
                                            intensity_cap_amt,
                                            df[water_intensity_name])
    else:
        df[water_intensity_name] = df[water_intensity_name]

    # calculate state average
    state_avg = df.groupby("State", as_index=False).mean().drop(['HY-InUse', 'HY-InPow'], axis=1)
    state_avg = state_avg.rename(columns={water_intensity_name: 'state_avg'})

    # fill missing states with country average
    state_avg.fillna(state_avg['state_avg'].mean(), inplace=True)

    # merge back with original county-level dataframe
    df_mean_all = pd.merge(df, state_avg, how='left', on=['State'])

    # replace counties with consumption fractions of zero with the state average to replace missing data
    df_mean_all[water_intensity_name].fillna(df_mean_all['state_avg'], inplace=True)

    # create discharge fraction variable
    hydro_discharge_name = hydro_name + '_to_SRD_total_total_total_total_mgd_fraction'
    df_mean_all[hydro_discharge_name] = 1

    # create source fraction
    hydro_source_name = hydro_name + 'from_WSW_fresh_surfacewater_total_total_mgd_fraction'
    df_mean_all[hydro_source_name] = 1

    # simplify dataframe
    output_df = df_mean_all[['FIPS', 'State', water_intensity_name, hydro_source_name, hydro_discharge_name]]

    # merge with hydro generation data
    output_df = pd.merge(output_df, df_hydro, how='right', on=['FIPS', 'State'])

    # only keep counties with hydro generation
    output_df = output_df[output_df.EGS_hydro_instream_nocooling_total_bbtu_from_EPD_hydro_total_total_total_bbtu > 0]

    # merge with full list of counties from 2015 water data
    output_df = pd.merge(df_loc, output_df, how='left', on=['FIPS', 'State'])
    output_df.fillna(0, inplace=True)

    return output_df


# BELOW IS READY TO GO
def prep_pumping_energy_fuel_data() -> pd.DataFrame:
    """prepping pumping fuel source data so that the outcome is a dataframe showing the percent of energy for
    crop irrigation, golf irrigation, aquaculture, livestock, and public water supply, that comes from each fuel
    source type (e.g., electricity, natural gas). Also includes discharge fractions for rejected energy and energy
    services.

    :return:                DataFrame fuel source fractions, rejected energy fractions, and energy services fractions

    """
    # pumping efficiency assumption
    EFFICIENCY = .65

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

    # reducing dataframe to required variables
    df = df[['State', 'electricity_pumping', 'ng_pumping', 'propane_pumping',
             'diesel_pumping', 'gas_pumping']]

    # filling states that were not in the irrigation dataset with the average for each fuel type
    df['electricity_pumping'].fillna(df['electricity_pumping'].mean(axis=0), inplace=True)
    df['ng_pumping'].fillna(df['ng_pumping'].mean(axis=0), inplace=True)
    df['propane_pumping'].fillna(df['propane_pumping'].mean(axis=0), inplace=True)
    df['diesel_pumping'].fillna(df['diesel_pumping'].mean(axis=0), inplace=True)
    df['gas_pumping'].fillna(df['gas_pumping'].mean(axis=0), inplace=True)

    # bin similar fuel types
    df['EPD_petroleum'] = df['propane_pumping'] + df['diesel_pumping']
    df['EPD_natgas'] = df['ng_pumping'] + df['gas_pumping']

    # rename electricity fuel type
    df['EGD_total'] = df['electricity_pumping']

    # keep only required columns
    df_out = df.drop(["gas_pumping", "propane_pumping", "diesel_pumping", 'ng_pumping'], axis=1)

    # merge with county data to distribute value to each county in a state
    df_out = pd.merge(df_loc, df_out, how='left', on='State')

    fuel_source_list = ['EPD_natgas',
                        'EPD_petroleum',
                        'EGD_total']

    fuel_flow_name = '_total_total_total_bbtu_fraction'

    irr_sector_list = ['AGR_crop_pumping_fresh_surfacewater_bbtu',
                       'AGR_golf_pumping_fresh_surfacewater_bbtu',
                       'AGR_crop_pumping_fresh_groundwater_bbtu',
                       'AGR_golf_pumping_fresh_groundwater_bbtu']

    rejected_energy_flow = '_to_REJ_total_total_total_total_bbtu_fraction'
    energy_services_flow = '_to_ESV_total_total_total_total_bbtu_fraction'

    output_df = df_out[['FIPS', 'State', 'County']].copy()
    for sector in irr_sector_list:
        for fuel in fuel_source_list:
            fuel_flow = fuel + fuel_flow_name
            full_flow_name = sector + "_from_" + fuel_flow
            output_df[full_flow_name] = df_out[fuel]

            # rejected energy name
            rej_flow = sector + rejected_energy_flow
            output_df[rej_flow] = 1 - EFFICIENCY

            esv_flow = sector + energy_services_flow
            output_df[esv_flow] = EFFICIENCY

    # electricity source name
    egd_name = '_from_EGD_total_total_total_total_bbtu_fraction'

    non_irr_sector_list = ['AGR_aquaculture_pumping_fresh_surfacewater_bbtu',
                           'AGR_aquaculture_pumping_fresh_surfacewater_bbtu',
                           'AGR_aquaculture_pumping_saline_surfacewater_bbtu',
                           'AGR_aquaculture_pumping_saline_surfacewater_bbtu',
                           'AGR_livestock_pumping_fresh_groundwater_bbtu',
                           'AGR_livestock_pumping_fresh_groundwater_bbtu']

    for sector in non_irr_sector_list:
        sector_source_name = sector + egd_name
        output_df[sector_source_name] = 1  # set all energy flow to 100% from electricity

        rej_flow_name = sector + rejected_energy_flow
        output_df[rej_flow_name] = 1 - EFFICIENCY

        esv_flow_name = sector + energy_services_flow
        output_df[energy_services_flow] = EFFICIENCY

    pws_sector_list = ['PWS_pumping_fresh_surfacewater_total_bbtu',
                       'PWS_pumping_fresh_groundwater_total_bbtu',
                       'PWS_pumping_saline_surfacewater_total_bbtu',
                       'PWS_pumping_saline_groundwater_total_bbtu',
                       'PWS_treatment_fresh_surfacewater_total_bbtu',
                       'PWS_treatment_fresh_groundwater_total_bbtu',
                       'PWS_treatment_saline_surfacewater_total_bbtu',
                       'PWS_treatment_saline_groundwater_total_bbtu',
                       'PWS_distribution_fresh_surfacewater_total_bbtu',
                       'PWS_distribution_fresh_groundwater_total_bbtu',
                       'PWS_distribution_saline_surfacewater_total_bbtu',
                       'PWS_distribution_saline_groundwater_total_bbtu']

    for sector in pws_sector_list:
        sector_source_name = sector + egd_name
        output_df[sector_source_name] = 1  # set all energy flow to 100% from electricity

        rej_flow_name = sector + rejected_energy_flow
        output_df[rej_flow_name] = 1 - EFFICIENCY

        esv_flow_name = sector + energy_services_flow
        output_df[energy_services_flow] = EFFICIENCY

    # df_out = df_out.drop(["natural_gas_pumping", "petroleum_pumping", "electricity_pumping"], axis=1)

    return output_df


# BELOW IS READY TO GO
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

    # read in renaming data
    df_names = pd.read_csv('input_data/variable_rename_key_pump_intensity.csv')

    # convert to dictionary
    name_dict = dict(zip(df_names.original_name, df_names.new_name))

    # establish variables
    acc_gravity = 9.81  # Acceleration of gravity  (m/s^2)
    water_density = 997  # Water density (kg/m^3)
    ag_pump_eff = .465  # assumed pump efficiency rate
    psi_psf_conversion = 2.31  # conversion of pounds per square inch (psi) to pounds per square foot (psf)
    m3_mg_conversion = 3785.41178  # conversion factor for m^3 to million gallons
    joules_kwh_conversion = 1 / 3600000  # conversion factor from joules to kWh
    kwh_bbtu_conversion = 3412.1416416 / 1000000000  # 1 kWh is equal to 3412.1416416 btu
    meter_ft_conversion = 0.3048  # meters in a foot

    # determine groundwater pumping intensity by state
    head_ft = psi_psf_conversion * df["average_operating_pressure_psi"]  # conversion of psi to head (pounds per sqft)
    diff_height_gw = meter_ft_conversion * (df["average_well_depth_ft"] + head_ft)  # calc. differential height (m)
    pump_power_gw = (water_density * diff_height_gw * acc_gravity * m3_mg_conversion) / ag_pump_eff  # joules/MG
    df['groundwater_pumping_bbtu_per_mg'] = pump_power_gw * joules_kwh_conversion * kwh_bbtu_conversion  # (bbtu/mg)

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
    df['groundwater_pumping_bbtu_per_mg'].fillna(groundwater_pumping_bbtu_per_mg_avg, inplace=True)
    df['surface_water_pumping_bbtu_per_mg'].fillna(surface_water_pumping_bbtu_per_mg_avg, inplace=True)

    sw_list = ['AGR_crop_pumping_fresh_surfacewater_bbtu',
               'AGR_golf_pumping_fresh_surfacewater_bbtu',
               'AGR_aquaculture_pumping_fresh_surfacewater_bbtu',
               'AGR_aquaculture_pumping_saline_surfacewater_bbtu',
               'AGR_livestock_pumping_fresh_surfacewater_bbtu',
               'PWS_pumping_fresh_surfacewater_total_bbtu',
               'PWS_pumping_saline_surfacewater_total_bbtu']

    for sw in sw_list:
        df[sw] = df['surface_water_pumping_bbtu_per_mg']

    gw_list = ['AGR_crop_pumping_fresh_groundwater_bbtu',
               'AGR_golf_pumping_fresh_groundwater_bbtu',
               'AGR_aquaculture_pumping_fresh_groundwater_bbtu',
               'AGR_aquaculture_pumping_saline_groundwater_bbtu',
               'AGR_livestock_pumping_fresh_groundwater_bbtu',
               'PWS_pumping_fresh_groundwater_total_bbtu',
               'PWS_pumping_saline_groundwater_total_bbtu']

    for gw in gw_list:
        df[gw] = df['groundwater_pumping_bbtu_per_mg']

    # reduce dataframe to variables in renaming dictionary
    df = df[name_dict]

    # rename columns based on dictionary
    df.rename(columns=name_dict, inplace=True)

    return df


# BELOW IS GOOD TO GO
def prep_pws_treatment_dist_intensity_values():
    """ Prepares energy intensity values for public water supply treatment and distribution

    :return:                                            Dataframe of publicw water supply intensities
    """
    # create a dataframe of counties
    out_df = prep_water_use_2015()

    # establish intensity values
    FGW_TREATMENT = 205  # fresh groundwater treatment (kwh/mg)
    FSW_TREATMENT = 405  # fresh surface water treatment (kWh/mg)
    SGW_TREATMENT = 12000  # saline groundwater treatment (kWh/mg)
    SSW_TREATMENT = 12000  # saline surface water treatment (kWh/mg)
    DISTRIBUTION = 1040  # distrubution (kWh)

    # convert intensities to bbtu/million gallon
    fgw_treat = convert_kwh_bbtu(FGW_TREATMENT)
    fsw_treat = convert_kwh_bbtu(FSW_TREATMENT)
    sgw_treat = convert_kwh_bbtu(SGW_TREATMENT)
    ssw_treat = convert_kwh_bbtu(SSW_TREATMENT)
    dist = convert_kwh_bbtu(DISTRIBUTION)

    fgw_t_flow = 'PWS_treatment_fresh_groundwater_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity'
    out_df[fgw_t_flow] = fgw_treat

    fsw_t_flow = 'PWS_treatment_fresh_surfacewater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity'
    out_df[fsw_t_flow] = fsw_treat

    sgw_t_flow = 'PWS_treatment_saline_groundwater_total_bbtu_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'
    out_df[sgw_t_flow] = sgw_treat

    ssw_t_flow = 'PWS_treatment_saline_surfacewater_total_bbtu_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity'
    out_df[ssw_t_flow] = ssw_treat

    dist_flow_list = [
        'PWS_distribution_total_total_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity',
        'PWS_distribution_total_total_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity',
        'PWS_distribution_total_total_total_bbtu_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity',
        'PWS_distribution_total_total_total_bbtu_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'
    ]

    for item in dist_flow_list:
        out_df[item] = dist

    return out_df





# BELOW IS WORKING
def prep_electricity_demand_data() -> pd.DataFrame:
    """prepping electricity demand data by sector from EIA electricity sales data.
    Produces a dataframe of demand data by county.

    :return:                DataFrame of electricity demand data

    """
    # Create efficiency assumptions (amount sent to energy services)
    res_eff = .65
    com_eff = .65
    ind_eff = .49
    tra_eff = .21

    # Read in state-level electricity generation demand by sector
    data = 'input_data/eia_sales_annual.csv'

    # read in transportation electricity sales data
    df = pd.read_csv(data, skiprows=1,
                     dtype={'Residential': float, 'Commercial': float,
                            'Industrial': float, 'Transportation': float})

    # build renaming dictionary
    rename_dict = {"Residential": 'RES',
                   "Commercial": 'COM',
                   "Industrial": 'IND',
                   "Transportation": 'TRA'}

    # reduce dataframe to only include 2015
    df = df[df.Year == 2015]

    # remove US total
    df = df[df.State != 'US']

    # remove all rows except total electricity sales
    df = df.loc[df['Industry Sector Category'] == 'Total Electric Industry']

    # prep dataframe
    sector_list = ["State", "Residential", "Commercial", "Industrial", "Transportation"]
    df = df[sector_list]

    # convert to daily values from annual
    column_list = df.columns[1:]
    for col in column_list:
        df[col] = df[col] / 365

    # convert electricity demand values from mwh/day to bbtu/day
    for col in column_list:
        df[col] = df[col].apply(convert_mwh_bbtu)

    # rename columns to add descriptive language
    df.rename(columns=rename_dict, inplace=True)

    # split out into county values based on percent of state population
    df = calc_population_county_weight(df)
    demand_columns = df.columns[1:5].to_list()
    for d in demand_columns:
        df[d] = df[d] * df['pop_weight']
    df = df.drop(['pop_weight'], axis=1)

    # create full variable names for demand flows
    flow_name = '_total_total_total_total_bbtu_from_EGD_total_total_total_total_bbtu'
    rej_name = '_total_total_total_total_bbtu_to_REJ_total_total_total_total_bbtu_fraction'
    esv_name = '_total_total_total_total_bbtu_to_ESV_total_total_total_total_bbtu_fraction'

    sector_list = ['RES', 'COM', 'IND', 'TRA']

    # create energy demand flows to sectors
    for sector in sector_list:
        demand_name = sector + flow_name
        df[demand_name] = df[sector]

    # create rejected energy flows to sectors
    for sector in sector_list:
        rej_flow_name = sector + rej_name
        esv_flow_name = sector + esv_name

        if sector == "RES":
            df[rej_flow_name] = 1 - res_eff
            df[esv_flow_name] = res_eff

        elif sector == "COM":
            df[rej_flow_name] = 1 - com_eff
            df[esv_flow_name] = com_eff

        elif sector == "IND":
            df[rej_flow_name] = 1 - ind_eff
            df[esv_flow_name] = ind_eff

        else:
            df[rej_flow_name] = 1 - tra_eff
            df[esv_flow_name] = tra_eff

    # drop unneeded variables
    df = df.drop(sector_list, axis=1)

    return df


# BELOW IS GOOD TO GO
def prep_fuel_demand_data() -> pd.DataFrame:
    """prepares fuel demand data to the residential, commercial, industrial, and transportation sectors. Returns a
    dataframe of fuel demand by fuel type and sector in bbtu per day for each county.

    :return:                DataFrame of a fuel demand values by sector

    """

    # read in fuel data
    data = 'input_data/use_all_btu.csv'
    df = pd.read_csv(data)

    # read in variable renaming key
    # read in renaming data
    df_names = pd.read_csv('input_data/variable_rename_key_fuel_demand.csv')

    # convert to dictionary
    df_names = dict(zip(df_names.original_name, df_names.new_name))

    msn_list = ["CLCCB",  # Coal, commercial sector (bbtu)
                "CLICB",  # Coal, industrial sector (bbtu)
                "EMACB",  # Fuel ethanol, transportation sector (bbtu)
                "GECCB",  # Geothermal, commercial sector (bbtu)
                "GERCB",  # Geothermal, residential sector (bbtu)
                "NGACB",  # Natural gas, transportation sector  (bbtu)
                "NGCCB",  # Natural gas, commercial sector (bbtu)
                "NGICB",  # Natural gas, industrial sector (bbtu)
                "NGRCB",  # Natural gas, residential sector (bbtu
                "PAACB",  # petroleum products, transportation sector (bbtu)
                "PACCB",  # petroleum products, commercial sector (bbtu)
                "PAICB",  # petroleum products, industrial sector (bbtu)
                "PARCB",  # petroleum products, residential sector (bbtu)
                "SOCCB",  # Solar, commercial sector (bbtu)
                "SORCB",  # Solar, residential sector (bbtu)
                "WDRCB",  # Wood energy, residential sector (bbtu)
                "WWCCB",  # Wood and waste energy, commercial sector (bbtu)
                "WWICB"]  # Wind energy, commercial sector (bbtu)

    # reduce dataframe
    df = df[df['MSN'].isin(msn_list)]  # using MSN codes that are relevant

    # pivoting dataframe to get fuel codes as columns
    df = pd.pivot_table(df, values='2015', index=['State'],  # pivot
                        columns=['MSN'], aggfunc=np.sum)
    df = df.reset_index()  # reset index to remove multi-index
    df = df.rename_axis(None, axis=1)  # drop index name
    df.fillna(0, inplace=True)  # filling blanks with zero

    # split out data into county values by using state population percent
    df = calc_population_county_weight(df)

    # multiply out by county weight and convert to daily bbtu from annual
    energy_columns = df.columns[1:-3].to_list()
    for d in energy_columns:
        df[d] = (df[d] * df['pop_weight'])  # multiply out each county by population percentage of state
        df[d] = df[d] / 365  # change from annual values to daily values

    # rename columns to add descriptive language
    df.rename(columns=df_names, inplace=True)

    # drop county population variable
    df = df.drop(['pop_weight'], axis=1)

    return df


# BELOW IS GOOD TO GO
def prep_state_fuel_production_data() -> pd.DataFrame:
    """preps state-level fuel production data for petroleum, biomass, natural gas, and coal. Outputs are used
    to determine county-level fuel production for each fuel type. Values are annual production.

    :return:                DataFrame of fuel production data by fuel type and state

    """

    # read in energy production data
    data = 'input_data/eia_SEDS_Prod_dataset.csv'
    df = pd.read_csv(data, skiprows=1)

    # list of fuel demand codes that are relevant from dataset
    msn_prod_dict = {"PAPRB": "petroleum_production_bbtu",  # crude oil production (including lease condensate) (BBTU)
                     "EMFDB": "biomass_production_bbtu",  # biomass inputs to the production of fuel ethanol (BBTU)
                     "NGMPB": "natgas_production_bbtu",  # natural gas marketed production (BBTU)
                     }

    # reduce dataset to relevant variables
    df = df[df['MSN'].isin(msn_prod_dict)]

    # prepping data
    df = pd.pivot_table(df, values='2015', index=['StateCode'],  # pivoting to get fuel codes as columns for 2015
                        columns=['MSN'], aggfunc=np.sum)
    df = df.reset_index()  # reset index to remove multi-index
    df = df.rename_axis(None, axis=1)  # drop index name
    df = df.rename(columns={"StateCode": "State"})  # rename state column

    # remove unneeded values
    df = df[df.State != "X3"]  # drop offshore (gulf of mexico) values
    df = df[df.State != "X5"]  # drop offshore (pacific) values
    df = df[df.State != "US"]  # drop total US values
    df.fillna(0, inplace=True)  # filling blanks with zero

    # rename columns to dictionary values
    df.rename(columns=msn_prod_dict, inplace=True)  # rename columns to add descriptive language

    return df


# BELOW IS GOOD TO GO
def prep_county_petroleum_production_data() -> pd.DataFrame:
    """prepares a dataframe of oil production by county. The dataframe uses 2011 crude oil production
    (barrels per year) by county in the US to determine which counties in a given state contribute the most to the
    state total. These percent of state total values from 2011 are mapped to 2015 state total oil production to get
    2015 values on a county level.

    :return:                DataFrame of a oil production (bbtu) by county

    """

    # establish unconventional to conventional petroleum ratio
    UNCONVENTIONAL_PETROLEUM_FRACTION = .63  # fraction of all petroleum production that is unconventional

    # read in state level fuel production data
    df = prep_state_fuel_production_data()  # read in 2015 state level petroleum production data
    df = df[["State", "petroleum_production_bbtu"]]  # reduce dataframe to required variables

    # read in county level oil and gas production data for 2011
    data_prod = 'input_data/oilgascounty.csv'
    df_petroleum_loc = pd.read_csv(data_prod, dtype={'geoid': str})
    df_petroleum_loc = df_petroleum_loc[['FIPS', 'Stabr', 'oil2011']]  # reduce dataframe to required variables

    # read in FIPS codes and states from 2015 water dataset
    df_loc = prep_water_use_2015()

    # calculate percent of state total petroleum production for each county in 2011
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
    ak_cook_df = {'State': 'AK', 'FIPS': '02122', 'oil_pct': .0262}  # Alaska, cook inlet basin (Kenai peninsula)
    oil_list = [idaho_df, ak_arctic_df, ak_cook_df]
    for oil_county in oil_list:
        df_petroleum_loc = df_petroleum_loc.append(oil_county, ignore_index=True)

    # merge county level percent data with 2015 state-level production data
    df = pd.merge(df_petroleum_loc, df, how='left', on="State")

    # calculate 2015 percent by county
    df['petroleum_production_bbtu'] = (df['petroleum_production_bbtu'] * df['oil_pct'])

    # convert to daily production from annual
    df['petroleum_production_bbtu'] = df['petroleum_production_bbtu'] / 365

    # split into unconventional and conventional
    df['petroleum_unconventional_production_bbtu'] = UNCONVENTIONAL_PETROLEUM_FRACTION * df['petroleum_production_bbtu']
    df['petroleum_conventional_production_bbtu'] = (1 - UNCONVENTIONAL_PETROLEUM_FRACTION) \
                                                   * df['petroleum_production_bbtu']

    # reduce dataframe
    df = df[['FIPS', 'State', 'oil_pct',
             'petroleum_unconventional_production_bbtu', 'petroleum_conventional_production_bbtu']]

    return df


# BELOW IS READY
def prep_petroleum_water_intensity():
    """ Takes county level petroleum-production values and determines the water intensity for the given county for
    both unconventional and conventional petroleum production.

    :return:                                        Dataframe of county-level petroleum water intensity values
    """

    # create variables
    GALLON_OIL_TO_BBTU_CONVERSION = 0.0001355  # gallon of oil to billion btu conversion
    MILLION_MULTIPLIER = 1000000
    CONVENTIONAL_SURFACE_WATER = .80  # percent of water in conventional oil that comes from surface

    # read in county list
    df_loc = prep_water_use_2015()

    # read in county-level petroleum production
    df = prep_county_petroleum_production_data()
    df_unconventional = df[['FIPS', 'State', 'oil_pct', 'petroleum_unconventional_production_bbtu']].copy()
    df_conventional = df[['FIPS', 'State', 'oil_pct', 'petroleum_conventional_production_bbtu']].copy()

    # read in state-level water to oil intensity data for conventional oil production
    data_water_intensity = 'input_data/PADD_intensity.csv'
    df_conventional_water = pd.read_csv(data_water_intensity)

    # read in state level unconventional oil water use data
    un_data = 'input_data/Unconventional_Oil_NG_State.csv'
    df_unconventional_water = pd.read_csv(un_data)
    df_unconventional_water = df_unconventional_water[['State', 'FSW_Unconventional_Oil (MGD)',
                                                       'FGW_Unconventional_Oil (MGD)']]

    # merge unconventional water use with county-level petroleum production percents
    df_unconventional = pd.merge(df_unconventional, df_unconventional_water, how='left', on='State')

    # split state surface and groundwater use in unconventional oil using county-level oil production percent
    df_unconventional['fsw_unconventional_mgd'] = df_unconventional['FSW_Unconventional_Oil (MGD)'] \
                                                  * df_unconventional['oil_pct']
    df_unconventional['fgw_unconventional_mgd'] = df_unconventional['FGW_Unconventional_Oil (MGD)'] \
                                                  * df_unconventional['oil_pct']

    # calculate county level water intensity based on county level petroleum production
    df_unconventional['total_water'] = df_unconventional['fsw_unconventional_mgd'] \
                                       + df_unconventional['fgw_unconventional_mgd']
    df_unconventional['un_water_intensity'] = df_unconventional['total_water'] \
                                              / df_unconventional['petroleum_unconventional_production_bbtu']

    # calculate the surface water fraction of total water use
    df_unconventional['un_fsw_frac'] = df_unconventional['fsw_unconventional_mgd'] / df_unconventional['total_water']

    # calculate the groundwater fraction of total water use
    df_unconventional['un_fgw_frac'] = 1 - df_unconventional['un_fsw_frac']

    # fill missing water intensity, surface water fractions and groundwater fractions with averages
    df_unconventional['un_water_intensity'].fillna(df_unconventional['un_water_intensity'].mean(), inplace=True)
    df_unconventional['un_fsw_frac'].fillna(df_unconventional['un_fsw_frac'].mean(), inplace=True)
    df_unconventional['un_fsw_frac'].fillna(df_unconventional['un_fsw_frac'].mean(), inplace=True)

    # conventional oil production
    df_conventional = pd.merge(df_conventional, df_conventional_water, how='left', on='State')

    # convert gallon of water per gallon of oil to million gallon of water per gallon of oil
    df_conventional['con_water_int'] = df_conventional['GalWater_GalOil'] / MILLION_MULTIPLIER

    # convert million gallon of water per gallon of oil to million gallon of water per bbtu of oil
    df_conventional['con_water_int'] = df_conventional['con_water_int'] \
                                       / GALLON_OIL_TO_BBTU_CONVERSION

    # create fresh surface water source fraction
    df_conventional['con_fsw_frac'] = CONVENTIONAL_SURFACE_WATER

    # create fresh groundwater source fraction
    df_conventional['con_fgw_frac'] = 1 - CONVENTIONAL_SURFACE_WATER

    # merge unconventional and conventional dataframes with full county list
    df_unconventional = pd.merge(df_loc, df_unconventional, how='left', on=['FIPS', 'State'])
    df_unconventional.fillna(0, inplace=True)
    df_conventional = pd.merge(df_loc, df_conventional, how='left', on=['FIPS', 'State'])
    df_conventional.fillna(0, inplace=True)

    df_conventional = df_conventional.drop(['oil_pct'], axis=1)

    # merge unconventional and conventional together
    output_df = pd.merge(df_unconventional, df_conventional, how='left', on=['FIPS', 'State', 'County'])

    output_df = output_df[['FIPS', 'State', 'County', 'un_water_intensity', 'un_fsw_frac', 'un_fgw_frac',
                           'con_water_int', 'con_fsw_frac', 'con_fgw_frac']]

    return output_df


# BELOW IS READY TO GO
def prep_county_natgas_production_data() -> pd.DataFrame:
    """prepares a dataframe of natural gas production by county for the year 2015. The dataframe uses 2011 natural gas
     production (million cubic ft) by county in the US to determine which counties in a given state contribute the
     most to the state total. These percent of state total values from 2011 are mapped to 2015 state total natural gas
      production to get 2015 values on a county level.

    :return:                DataFrame of a natural gas production (bbtu) and water use (mgd) by county

    """
    # read in data
    df = prep_state_fuel_production_data()  # read in 2015 state level petroleum production data
    df = df[["State", "natgas_production_bbtu"]]  # collect required variables

    # read in county level gas production data from 2011 dataset
    data_prod = 'input_data/oilgascounty.csv'
    df_ng_loc = pd.read_csv(data_prod, dtype={'geoid': str})
    df_ng_loc = df_ng_loc[['FIPS', 'Stabr', 'gas2011']]  # collect required variables

    # read in FIPS codes and states from 2015 water dataset
    df_loc = prep_water_use_2015()

    # calculate percent of total 2011 state oil production by county
    df_ng_loc_sum = df_ng_loc[['Stabr', 'gas2011']].groupby("Stabr", as_index=False).sum()
    df_ng_loc_sum = df_ng_loc_sum.rename(columns={"gas2011": "state_total"})
    df_ng_loc = pd.merge(df_ng_loc, df_ng_loc_sum, how='left', on='Stabr')
    df_ng_loc['gas_pct'] = df_ng_loc['gas2011'] / df_ng_loc['state_total']

    # rename columns
    df_ng_loc = df_ng_loc.rename(columns={"Stabr": "State"})

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
    ng_df = pd.merge(df_ng_loc, df, how='left', on="State")

    # calculate 2015 percent by county
    ng_df['natgas_county_bbtu'] = ng_df['natgas_production_bbtu'] * ng_df['gas_pct']

    # change to daily values from annual
    ng_df['natgas_county_bbtu'] = ng_df['natgas_county_bbtu'] / 365

    # remove rows with 0 production
    ng_df = ng_df[ng_df.natgas_county_bbtu > 0]

    # keep only required columns

    ng_df = ng_df[['FIPS', 'State', 'gas_pct', 'natgas_county_bbtu']]

    return ng_df


# BELOW IS GOOD TO GO
def prep_natgas_water_intensity():
    """Water withdrawal data is supplied for a select number of states. State totals are split out to counties using
    the same county percent of total natural gas production as the production calculation. For states with 2015
    production but no water withdrawal estimates, the national average water intensity (mg/bbtu) is applied to their
    natural gas production quantity. It is assumed that 80% of these calculated total water use values come from fresh
    surface water and 20% from fresh groundwater.

    :return:
    """

    # read in full county list data
    df_loc = prep_water_use_2015()

    # read in read in state level natural gas water data
    un_data = 'input_data/Unconventional_Oil_NG_State.csv'
    df_ng_water = pd.read_csv(un_data)
    df_ng_water = df_ng_water[['State', 'FSW_Unconventional_NG (MGD)', 'FGW_Unconventional_NG (MGD)']]

    # read in county-level natural gas production data
    ng_prod_df = prep_county_natgas_production_data()

    # combine natural gas production data and natural gas water data
    df = pd.merge(ng_prod_df, df_ng_water, how='left', on='State')

    # split state surface and groundwater use in natural gas using county-level oil production percent
    df['fsw_natgas_mgd'] = df['FSW_Unconventional_NG (MGD)'] * df['gas_pct']
    df['fgw_natgas_mgd'] = df['FGW_Unconventional_NG (MGD)'] * df['gas_pct']

    # calculate county level water intensity based on county level natural gas production
    df['total_water'] = df['fsw_natgas_mgd'] + df['fgw_natgas_mgd']
    df['natgas_water_intensity'] = df['total_water'] / df['natgas_county_bbtu']

    # calculate the surface water fraction of total water use
    df['natgas_fsw_frac'] = df['fsw_natgas_mgd'] / df['total_water']

    # calculate the groundwater fraction of total water use
    df['natgas_fgw_frac'] = 1 - df['natgas_fsw_frac']

    # fill missing water intensity, surface water fractions and groundwater fractions with averages
    df['natgas_water_intensity'].fillna(df['natgas_water_intensity'].mean(), inplace=True)
    df['natgas_fsw_frac'].fillna(df['natgas_fsw_frac'].mean(), inplace=True)
    df['natgas_fgw_frac'].fillna(df['natgas_fgw_frac'].mean(), inplace=True)

    # reduce dataframe to required variables
    df = df[['FIPS', 'State', 'natgas_water_intensity', 'natgas_fsw_frac', 'natgas_fgw_frac']]

    # merge with county data to distribute value to each county in a state and include all FIPS
    df = pd.merge(df_loc, df, how='left', on=['FIPS', 'State'])
    df.fillna(0, inplace=True)

    return df

# BELOW IS GOOD TO GO
def prep_petroleum_gas_discharge_data() -> pd.DataFrame:
    """prepares a dataframe of produced water intensities, consumption fractions, and discharge fractions for
    petroleum and natural gas production. Note that only unconventional petroleum production results in produced water.
    Consumption and discharge fractions are assumed for all types of petroleum production.

    :return:                DataFrame of produced water intensities, consumption fractions, and discharge fractions
                            for unconventional natural gas and petroleum production

    """

    # read in state level water discharge data from oil and natural gas
    data = 'input_data/Oil_NG_WOR_WGR.csv'
    df = pd.read_csv(data)

    # read in full county list data
    df_loc = prep_water_use_2015()

    # read in petroleum production data by county
    df_pet = prep_county_petroleum_production_data()

    # read in natural gas production data by county
    df_ng = prep_county_natgas_production_data()

    # establish conversion factors
    WATER_BARREL_TO_MG_CONVERSION = 0.000042
    OIL_BARREL_TO_BBTU_CONVERSION = 0.005691
    GAS_MMCF_TO_BBTU_CONVERSION = 1

    # convert barrels of water per barrel of oil to million gallons per bbtu of oil
    df['un_petrol_produced_int'] = df['WOR (bbl/bbl)'] * (WATER_BARREL_TO_MG_CONVERSION / OIL_BARREL_TO_BBTU_CONVERSION)

    # convert barrels of water per mmcf of natural gas to million gallons per bbtu of natural gas
    df['natgas_produced_int'] = df['WGR (bbl/Mmcf)'] * (WATER_BARREL_TO_MG_CONVERSION / GAS_MMCF_TO_BBTU_CONVERSION)

    # drop unneeded variables
    df = df.drop(['WOR (bbl/bbl)', 'WGR (bbl/Mmcf)'], axis=1)

    # combine with natural gas production data
    df_ng = pd.merge(df_ng, df, how='left', on='State')
    df_ng = df_ng[['FIPS', 'State', 'natgas_county_bbtu', 'Total injected (%)', 'Surface Discharge (%)',
                   'Evaporation/ Consumption (%)', 'natgas_produced_int']]

    # fill rows with missing discharge and produced water intensities with averages
    df_ng['Total injected (%)'].fillna(df_ng['Total injected (%)'].mean(), inplace=True)
    df_ng['Surface Discharge (%)'].fillna(df_ng['Surface Discharge (%)'].mean(), inplace=True)
    df_ng['Evaporation/ Consumption (%)'].fillna(df_ng['Evaporation/ Consumption (%)'].mean(), inplace=True)
    df_ng['natgas_produced_int'].fillna(df_ng['natgas_produced_int'].mean(), inplace=True)

    # rename key columns
    df_ng = df_ng.rename(columns={'Total injected (%)': 'NG_uncon_withdrawal_GD',
                                  'Surface Discharge (%)': 'NG_uncon_withdrawal_SD',
                                  'Evaporation/ Consumption (%)': 'NG_uncon_withdrawal_CMP'})

    # set produced water from natural gas fractions equal to natural gas unconventional withdrawal discharge fractions
    df_ng['NG_uncon_prod_GD'] = df_ng['NG_uncon_withdrawal_GD']
    df_ng['NG_uncon_prod_SD'] = df_ng['NG_uncon_withdrawal_SD']
    df_ng['NG_uncon_prod_CMP'] = df_ng['NG_uncon_withdrawal_CMP']

    # create variable for source fraction for produced water (set equal to 100%)
    df_ng['NG_uncon_prod_source'] = 1

    # merge natural gas data frame with full county list
    df_ng = pd.merge(df_loc, df_ng, how='left', on=['FIPS', 'State'])
    df_ng.fillna(0, inplace=True)

     # combine with petroleum production data
    df_pet = pd.merge(df_pet, df, how='left', on='State')
    df_pet = df_pet[['FIPS', 'State', 'petroleum_unconventional_production_bbtu',
                      'petroleum_conventional_production_bbtu', 'Total injected (%)', 'Surface Discharge (%)',
                      'Evaporation/ Consumption (%)', 'un_petrol_produced_int']]

     # rename key columns for unconventional petroleum
    df_pet = df_pet.rename(columns={'Total injected (%)': 'PET_uncon_withdrawal_GD',
                                     'Surface Discharge (%)': 'PET_uncon_withdrawal_SD',
                                     'Evaporation/ Consumption (%)': 'PET_uncon_withdrawal_CMP'})

    # set conventional petroleum fractions equal to unconventional discharge fractions
    df_pet['PET_con_withdrawal_GD'] = df_pet['PET_uncon_withdrawal_GD']
    df_pet['PET_con_withdrawal_SD'] = df_pet['PET_uncon_withdrawal_SD']
    df_pet['PET_con_withdrawal_CMP'] = df_pet['PET_uncon_withdrawal_CMP']

    # set produced water from petroleum fractions equal to unconventional discharge fractions
    df_pet['PET_uncon_prod_GD'] = df_pet['PET_uncon_withdrawal_GD']
    df_pet['PET_uncon_prod_SD'] = df_pet['PET_uncon_withdrawal_SD']
    df_pet['PET_uncon_prod_CMP'] = df_pet['PET_uncon_withdrawal_CMP']

    # create variable for source fraction for produced water (set equal to 100%)
    df_pet['PET_uncon_prod_source'] = 1

    # merge natural gas data frame with full county list
    df_pet = pd.merge(df_loc, df_pet, how='left', on=['FIPS', 'State'])
    df_pet.fillna(0, inplace=True)

    # merge natural gas and petroleum dataframes together
    output_df = pd.merge(df_ng, df_pet, how='left', on=['FIPS', 'State', 'County'])

    return output_df

# BELOW IS READY TO GO
def rename_natgas_petroleum_data():
    """ Takes county level natural gas and petroleum production, water intensity, water source, and water discharge
    data and renames into required variable name structure.

    :return:
    """

    # load petroleum water data
    df_pet_water = prep_petroleum_water_intensity()

    # load natural gas water data
    df_ng_water = prep_natgas_water_intensity()

    # load produced water and discharge data (also includes production data)
    df_prod = prep_petroleum_gas_discharge_data()

    # load variable renaming key
    # read in renaming data
    df_names = pd.read_csv('input_data/variable_rename_key_ng_petroleum.csv')

    # convert to dictionary
    name_dict = dict(zip(df_names.original_name, df_names.new_name))

    # merge natural gas and petroleum dataframes
    df = pd.merge(df_pet_water, df_ng_water, how='left', on = ['FIPS', 'State', 'County'])
    df = pd.merge(df, df_prod, how='left', on = ['FIPS', 'State', 'County'])

    # rename columns based on dictionary
    df.rename(columns=name_dict, inplace=True)

    return df

# BELOW IS GOOD TO GO
def prep_county_coal_production_data() -> pd.DataFrame:
    """prepares a dataframe of coal production by county from surface and underground mines in bbtu. Also creates a
    surface and underground water intensity per bbtu variable.

    :return:                DataFrame of coal production values in bbtu by county

    """
    # TODO make sure below intensities are correct
    # create water intensity variables by mine type (million gallon per bbtu)
    UNDERGROUND_INTENSITY = 0.00144
    SURFACE_INTENSITY = 0.00034

    # read in coal production data
    data_prod = 'input_data/coalpublic2015.csv'
    df_coal = pd.read_csv(data_prod, skiprows=3)

    # read in coal mine location data
    loc_data = 'input_data/Coal_Mine_Loc.csv'
    df_coal_loc = pd.read_csv(loc_data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])

    # read in state fips code to state abbrev. data
    fipsdata = 'input_data/State_FIPS_Code.csv'
    df_fips = pd.read_csv(fipsdata, dtype={'State_FIPS': str})

    # read in full list of FIPS codes and states from 2015 water dataset
    df_loc = prep_water_use_2015()

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

    # remove rows with Refuse Coal
    df_coal = df_coal.loc[df_coal['Mine Type'] != 'Refuse']

    # reorganize dataframe to get mine type as a column and individual row for each FIPS code
    df_coal = pd.pivot_table(df_coal, values='Production (short tons)',  # pivot dataframe
                             index=['FIPS'], columns=['Mine Type'], aggfunc=np.sum)
    df_coal = df_coal.reset_index()  # reset index to remove multi-index from pivot table
    df_coal = df_coal.rename_axis(None, axis=1)  # drop index name
    df_coal.fillna(0, inplace=True)

    # calculate coal production per county in billion btus per day
    df_coal['Surface'] = df_coal['Surface'] * shortton_bbtu_conversion / 365
    df_coal['Underground'] = df_coal['Underground'] * shortton_bbtu_conversion / 365

    # rename surface and underground columns to lowercase
    df_coal = df_coal.rename(columns = {'Surface': 'surface', 'Underground': 'underground'})

    # calculate total coal production per county
    df_coal['coal_production_bbtu'] = (df_coal['surface'] + df_coal['underground'])

    # create water intensity variables by mine type
    df_coal['underground_water_int'] = UNDERGROUND_INTENSITY
    df_coal['surface_water_int'] = SURFACE_INTENSITY

    return df_coal

# BELOW IS GOOD TO GO
def prep_county_coal_data() -> pd.DataFrame:
    """prepares a dataframe of water type and water source fractions to coal mining by county. These are assumed to
    be equal to total mining water withdrawal sources and discharge fractions in the 2015 USGS water data. Also
    develops full variable names for coal production and coal water intensity variables.

    :return:                DataFrame of water types and water source fractions to coal production

    """

    # read in county coal production data
    coal_prod_df = prep_county_coal_production_data()

    # read in water use data for 2015 in million gallons per day by county
    df = prep_water_use_2015(variables=['FIPS', 'MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa', 'MI-WSWSa'])

    # consumption fraction data
    cons_df = prep_consumption_fraction()

    # read in full list of counties for 2015
    df_loc = prep_water_use_2015()

    # create mining consumption fraction names
    water_types = ['fresh_surfacewater', 'saline_surfacewater', 'fresh_groundwater', 'saline_groundwater']
    cons_variable_list = []
    for type in water_types:
        prefix = 'MIN_other_total_'
        suffix = '_mgd_to_CMP_total_total_total_total_mgd_fraction'
        full_name = prefix + type + suffix
        cons_variable_list.append(full_name)

    cons_variable_list.append('FIPS')

    # reduce consumption dataframe to required variables
    cons_df = cons_df[cons_variable_list]

    # create a list of mining water source names
    source_list = ['MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa', 'MI-WSWSa']
    # calculate total water flows to mining
    df['total_mining_water'] = df[df.columns[1:].to_list()].sum(axis=1)

    # calculate water fractions
    for source in source_list:
        fraction_name = source + '_fraction'
        df[fraction_name] = np.where(df['total_mining_water'] > 0,
                                     df[source] / df['total_mining_water'],
                                     np.nan)

    # merge water source fraction data with coal production data
    df = pd.merge(coal_prod_df, df, how='left', on='FIPS')

    # fill missing water source fractions with the average for each type
    for source in source_list:
        fraction_name = source + '_fraction'
        df[fraction_name].fillna(df[fraction_name].mean(), inplace=True)

    # rename water fraction names
    df = df.rename(columns={'MI-WGWFr': 'WSW_fresh_groundwater',
                            'MI-WSWFr': 'WSW_fresh_surfacewater',
                            'MI-WGWSa': 'WSW_saline_groundwater',
                            'MI-WSWSa': 'WSW_saline_surfacewater'})

    # merge with consumption fraction dataset
    df = pd.merge(df, cons_df, how='left', on='FIPS')

    mine_type_list = ['surface', 'underground']
    output_variable_list = []

    # create surface discharge variables and consumption variables for each water type for coal
    for type in water_types:
        for mine_type in mine_type_list:
            other_prefix = 'MIN_other_total_'
            coal_prefix = 'MIN_coal_' + mine_type + "_"
            other_cmp_suffix = '_mgd_to_CMP_total_total_total_total_mgd_fraction'
            coal_full_name = coal_prefix  + 'withdrawal_total' + other_cmp_suffix
            other_full_name = other_prefix + type + other_cmp_suffix
            df[coal_full_name] = df[other_full_name]
            output_variable_list.append(coal_full_name)

            # surface discharge
            sd_suffix = 'mgd_to_SRD_total_total_total_total_mgd_fraction'
            coal_sd_name = coal_prefix + 'withdrawal_total_' + sd_suffix
            df[coal_sd_name] = 1 - df[coal_full_name]
            output_variable_list.append(coal_sd_name)

            # create source fraction names
            coal_prefix = 'MIN_coal_' + mine_type + "_" + 'withdrawal_total_'
            source_name = 'mgd_from_WSW_' + type + '_total_total_mgd_fraction'
            full_source_name = coal_prefix + source_name
            if type == 'fresh_surfacewater':
                df[full_source_name] = df['MI-WSWFr_fraction']
            elif type == 'fresh_groundwater':
                df[full_source_name] = df['MI-WGWFr_fraction']
            elif type == 'saline_surfacewater':
                df[full_source_name] = df['MI-WSWSa_fraction']
            else:
                df[full_source_name] = df['MI-WGWSa_fraction']
            output_variable_list.append(full_source_name)

            # create production naming and set equal to daily mine production by type
            mine_type_prefix = 'MIN_coal_'+ mine_type + '_total_total_bbtu'
            mine_type_suffix = '_from_MIN_coal_'+ mine_type + '_total_total_bbtu'
            mine_prod_name = mine_type_prefix + mine_type_suffix
            df[mine_prod_name] = df[mine_type]
            output_variable_list.append(mine_prod_name)

            # create water intensity naming for each mine type
            mine_int_prefix = 'MIN_coal_' + mine_type + '_withdrawal_total_mgd'
            mine_int_suffix = mine_type_suffix + '_intensity'
            mine_int_full = mine_int_prefix + mine_int_suffix
            intensity_name = mine_type + '_water_int'
            df[mine_int_full] = df[intensity_name]
            output_variable_list.append(mine_int_full)

            # calculate total water from each source for coal mining to substract out from USGS total
            water_with_type = 'coal_' + mine_type + "_" + type + "_withdrawal"
            df[water_with_type] = df[mine_prod_name] * df[mine_int_full] * df[full_source_name]

    # calculate total fresh surface water withdrawals by coal
    df['total_fsw_with'] = df['coal_surface_fresh_surfacewater_withdrawal'] \
                           + df['coal_underground_fresh_surfacewater_withdrawal']

    # calculate total fresh groundwater withdrawals by coal
    df['total_fgw_with'] = df['coal_surface_fresh_groundwater_withdrawal'] + df[
        'coal_underground_fresh_groundwater_withdrawal']

    # calculate total saline surface water withdrawals by coal
    df['total_ssw_with'] = df['coal_surface_saline_surfacewater_withdrawal'] + df[
        'coal_underground_saline_surfacewater_withdrawal']

    # calculate total saline groundwater withdrawals by coal
    df['total_sgw_with'] = df['coal_surface_saline_groundwater_withdrawal'] + df[
        'coal_underground_saline_groundwater_withdrawal']

    for type in water_types:
        # subtract coal calculated values from water to other mining
        other_mining_prefix = 'MIN_other_total_total_total_mgd_from_'
        other_mining_suffix = 'WSW_' + type + '_total_total_total_mgd'
        other_mining_total = other_mining_prefix + other_mining_suffix
        if type == 'fresh_surfacewater':
            df[other_mining_total] = np.where((df['WSW_fresh_surfacewater']- df['total_fsw_with'])<0,
                                              0,
                                              df['WSW_fresh_surfacewater'] - df['total_fsw_with'])
        elif type == 'fresh_groundwater':
            df[other_mining_total] = np.where((df['WSW_fresh_groundwater']- df['total_fgw_with'])<0,
                                              0,
                                              df['WSW_fresh_groundwater'] - df['total_fgw_with'])
        elif type == 'saline_surfacewater':
            df[other_mining_total] = np.where((df['WSW_saline_surfacewater']- df['total_ssw_with'])<0,
                                              0,
                                              df['WSW_saline_surfacewater'] - df['total_ssw_with'])
        else:
            df[other_mining_total] = np.where((df['WSW_saline_groundwater'] - df['total_sgw_with'])<0,
                                              0,
                                              df['WSW_saline_groundwater'] - df['total_sgw_with'])
        output_variable_list.append(other_mining_total)

    # append FIPS codes to keep variable list and reduce dataframe to needed variables
    output_variable_list.append('FIPS')
    df = df[output_variable_list]

    # merge with county location data
    df = pd.merge(df_loc, df, how='left', on='FIPS')
    df.fillna(0, inplace=True)

    return df


def remove_double_counting_from_mining():
    """ Calculates total water withdrawals in natural gas and petroleum to split them out from all mining water
    provided in USGS 2015 data. Takes leftover mining water after already subtracting out coal water use.

    :return:                                        DataFrame of recalculated water use in non-energy mining
    """

    # bring in full list of counties and state names
    df_loc = prep_water_use_2015()

    # bring in updated other mining values
    df_mining = prep_county_coal_data()

    # create variable names to reduce dataset to other mining water values
    water_types = ['fresh_surfacewater','fresh_groundwater', 'saline_surfacewater', 'saline_groundwater']
    variable_list = []
    for type in water_types:
        other_mining_prefix = 'MIN_other_total_total_total_mgd_from_'
        other_mining_suffix = 'WSW_' + type + '_total_total_total_mgd'
        other_mining_total = other_mining_prefix + other_mining_suffix
        variable_list.append(other_mining_total)
    variable_list.append('FIPS')

    # reduce dataframe to only required variables
    df_mining = df_mining[variable_list]

    # bring in petroleum and natural gas variables
    df_energy = rename_natgas_petroleum_data()
    e_var_list = []
    energy_types = ['petroleum_conventional', 'petroleum_unconventional', 'natgas_unconventional']
    water_types = ['fresh_surfacewater', 'fresh_groundwater']

    # create variable names and calculate water use
    for e in energy_types:
        for w in water_types:
            production_name = 'MIN_' + e + '_total_total_bbtu_from_MIN_' + e + '_total_total_bbtu'
            water_int_name = 'MIN_' + e + '_withdrawal_total_mgd_from_MIN_' + e + '_total_total_bbtu_intensity'
            water_src_name = 'MIN_' + e + '_withdrawal_total_mgd_from_WSW_' + w + '_total_total_mgd_fraction'

            # calculate water withdrawal
            water_name = w + "_" + e + '_withdrawal'
            df_energy[water_name] = df_energy[production_name] * df_energy[water_int_name] * df_energy[water_src_name]
            e_var_list.append(water_name)
    e_var_list.append('FIPS')

    # reduce variable list
    df_energy = df_energy[e_var_list]

    # calculate fresh surface water total
    df_energy['fsw_total'] = df_energy['fresh_surfacewater_petroleum_conventional_withdrawal'] + \
                             df_energy['fresh_surfacewater_petroleum_unconventional_withdrawal'] + \
                             df_energy['fresh_surfacewater_natgas_unconventional_withdrawal']

    # calculate fresh groundwater total
    df_energy['fgw_total'] = df_energy['fresh_groundwater_petroleum_conventional_withdrawal']+ \
                           df_energy['fresh_groundwater_petroleum_unconventional_withdrawal']+\
                           df_energy['fresh_groundwater_natgas_unconventional_withdrawal']

    # reduce energy dataframe to totals
    df_energy = df_energy[['FIPS', 'fsw_total', 'fgw_total']]

    # merge energy and mining dataframes
    df_mining = pd.merge(df_mining, df_energy, how='left', on=['FIPS'])

    # Subtract natural gas and petroleum water use from other mining
    fsw_name = 'MIN_other_total_total_total_mgd_from_WSW_fresh_surfacewater_total_total_total_mgd'
    fgw_name = 'MIN_other_total_total_total_mgd_from_WSW_fresh_groundwater_total_total_total_mgd'
    df_mining[fsw_name] = np.where((df_mining[fsw_name] - df_mining['fsw_total']) < 0,
                                   0,
                                   (df_mining[fsw_name] - df_mining['fsw_total']))

    df_mining[fgw_name] = np.where((df_mining[fgw_name] - df_mining['fgw_total']) < 0,
                                   0,
                                   (df_mining[fgw_name] - df_mining['fgw_total']))

    # reduce dataframe
    df_mining = df_mining[variable_list]

    # merge with full county list
    df = pd.merge(df_loc, df_mining, how='left', on='FIPS')

    return df


def prep_county_ethanol_production_data() -> pd.DataFrame:
    """ Takes 2015 eia data on ethanol plant capacity with locational data and combines with state level biomass
     (ethanol) production from prep_state_fuel_production_data() to split out state total by county. Returns a
     dataframe of ethanol production (bbtu) by county FIPS for each county in the US for 2015.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """
    # get data
    ethanol_data = 'input_data/eia819_ethanolcapacity_2015.csv'  # ethanol location data
    df_ethanol_loc = pd.read_csv(ethanol_data, dtype={'FIPS': str}, skiprows=1)
    df_ethanol_production = prep_state_fuel_production_data()  # ethnaol production data
    df_loc = prep_water_use_2015()  # read in FIPS codes and states from 2015 water dataset

    # gallons per bbtu for ethanol production
    btu_per_gal = 80430
    bbtu_per_gal_ethanol = btu_per_gal / 1000000000

    # gallon of water per gallon of ethanol
    gal_per_gal = 3
    mg_per_gal = gal_per_gal / 1000000

    # water intensity
    ethanol_intensity = mg_per_gal / bbtu_per_gal_ethanol

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

    # change from annual biomass production to daily
    df_biomass['biomass_production_bbtu'] = df_biomass['biomass_production_bbtu'] / 365

    df_biomass = df_biomass[['FIPS', 'biomass_production_bbtu']]
    df_biomass = df_biomass.rename(columns=
                                   {'biomass_production_bbtu':
                                        'IND_biomass_ethanol_total_total_bbtu_from_IND_biomass_ethanol_total_total_bbtu'})

    df_biomass['IND_biomass_ethanol_total_total_bbtu_to_EPD_biomass_total_total_total_bbtu_fraction'] = 1

    # create intensity variable
    df_biomass[
        'IND_biomass_ethanol_total_total_mgd_from_IND_biomass_ethanol_total_total_bbtu_intensity'] = ethanol_intensity

    # assume all ethanol production water comes from fresh surfacewater
    df_biomass['IND_biomass_ethanol_total_total_mgd_from_WSW_fresh_surfacewater_withdrawal_total_bbtu_fraction'] = 1
    df_biomass['IND_biomass_ethanol_total_total_mgd_to_SRD_total_total_total_total_mgd_fraction'] = 1

    # merge with full county data to distribute value to each county in a state and include all FIPS
    df_biomass = pd.merge(df_loc, df_biomass, how='left', on='FIPS')
    df_biomass.fillna(0, inplace=True)

    return df_biomass


def prep_county_water_corn_biomass_data() -> pd.DataFrame:
    """ Produces a dataframe of water (MGD) for corn irrigation for ethanol by county. Water intensity applied to all
    crop irrigation is applied to the irrigation used in the production of corn for ethanol.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """
    # read in corn data
    corn_irr_data = 'input_data/USDA_FRIS.csv'
    df_corn = pd.read_csv(corn_irr_data)

    # corn production data
    prod_data = 'input_data/USDA_NASS_CornProd_2015.csv'
    df_corn_prod = pd.read_csv(prod_data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})

    # read in 2015 crop irrigation data
    df_irr_water = prep_water_use_2015(variables=['State',
                                                  'ACI_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                                                  'ACI_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd'
                                                  ])
    df_loc = prep_water_use_2015()

    data_state = 'input_data/State_FIPS_Code.csv'
    df_state_abb = pd.read_csv(data_state, dtype={'State_FIPS': str})

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

    # calculate the total amount of water mgd applied to corn grown for ethanol
    df_corn["ethanol_corn_mgal"] = df_corn["irr_intensity"] * df_corn["corn_prod"]
    df_corn["ethanol_corn_mgal"] = (df_corn["ethanol_corn_mgal"] / 365).round(4)  # convert to million gallons per day

    # calculate surface water vs. groundwater fraction in corn irrigation
    df_corn["surface_total"] = df_corn["Off"] + df_corn["Surface"]  # adds off-farm and surface together for surface
    df_corn["water_total"] = df_corn["surface_total"] + df_corn["Ground"]  # sum surface water and groundwater
    df_corn['surface_frac'] = df_corn["surface_total"] / df_corn["water_total"]  # surface water fraction

    # calculate irrigation surface water to groundwater ratio for each state from 2015 USGS water dataset
    df_irr_water = df_irr_water.groupby("State", as_index=False).sum()
    df_irr_water['surface_frac_fill'] = df_irr_water[
                                            'ACI_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd'] \
                                        / (df_irr_water[
                                               'ACI_fresh_surfacewater_withdrawal_total_mgd_from_WSW_fresh_surfacewater_total_total_mgd']
                                           + df_irr_water[
                                               'ACI_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd'])
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
    df_corn = df_corn[['State', 'sw_ethanol_corn', 'gw_ethanol_corn', 'ethanol_corn_mgal']]

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
    df_corn_prod = df_corn_prod[['FIPS', 'sw_ethanol_corn',
                                 'gw_ethanol_corn',
                                 'ethanol_corn_mgal']]  # reduce dataframe

    # create new crop irrigation flows for corn ethanol irrigation
    df_corn_prod = df_corn_prod.rename(columns={'sw_ethanol_corn':
                                                    'ACI_fresh_surfacewater_withdrawal_ethanol_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
                                                'gw_ethanol_corn':
                                                    'ACI_fresh_groundwater_withdrawal_ethanol_mgd_from_WSW_fresh_groundwater_total_total_mgd',
                                                })

    df_corn_prod = pd.merge(df_loc, df_corn_prod, how='left', on='FIPS')  # merge dataframes
    df_corn_prod.fillna(0, inplace=True)  # replace blank values with zero

    return df_corn_prod



# def combine_data():
#   x1 = prep_water_use_2015(all_variables=True)
#   x2 = calc_pws_deliveries()
#   x3 = prep_pws_to_pwd()
#   x4 = calc_discharge_fractions()
#   x5 = calc_hydro_water_intensity()
#   x6 = prep_wastewater_data()
#   x7a = prep_generation_fuel_flows()
#   x7b = prep_electricity_cooling_flows()
#   x8 = prep_irrigation_fuel_data()
#   x9 = prep_pumping_intensity_data()
#   x10 = recalc_irrigation_consumption()
#   x11 = prep_consumption_fraction()
#   x12 = prep_interbasin_transfer_data()
#   x13 = prep_electricity_demand_data()
#   x14 = prep_fuel_demand_data()
#   x15 = prep_county_petroleum_production_data()
#   x16 = prep_county_natgas_production_data()
#   x17 = prep_petroleum_gas_discharge_data()
#   x18 = prep_county_coal_production_data()
#   x19 = prep_county_coal_water_source_fractions()
#   x20 = prep_county_ethanol_production_data()
#   x21 = remove_petroleum_double_counting_from_mining()
#   x1 = x1.drop(['population', 'fresh_groundwater_total_irrigation_mgd', 'fresh_surfacewater_total_irrigation_mgd',
#                 'fresh_wastewater_total_irrigation_mgd', 'golf_irrigation_fresh_consumption_mgd',
#                 'crop_irrigation_fresh_consumption_mgd', 'total_irrigation_fresh_consumption',
#                 'total_pws_withdrawals_mgd', 'fresh_groundwater_thermoelectric_mgd',
#                 'saline_groundwater_thermoelectric_mgd', 'fresh_surfacewater_thermoelectric_mgd',
#                 'saline_surfacewater_thermoelectric_mgd', 'wastewater_thermoelectric_mgd',
#                 'fresh_pws_thermoelectric_mgd', 'total_irrigation_consumption_fraction',
#                 'ACI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
#                 'ACI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
#                 'ACI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
#                 'AGI_fresh_groundwater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
#                 'AGI_fresh_surfacewater_withdrawal_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
#                 'AGI_reclaimed_wastewater_import_total_mgd_to_CMP_total_total_total_total_mgd_fraction',
#                 'MIN_other_total_fresh_groundwater_mgd_from_WSW_fresh_groundwater_total_total_mgd',
#                 'MIN_other_total_fresh_surfacewater_mgd_from_WSW_fresh_surfacewater_total_total_mgd',
#                 'MIN_other_total_saline_groundwater_mgd_from_WSW_saline_groundwater_total_total_mgd',
#                 'MIN_other_total_saline_surfacewater_mgd_from_WSW_saline_surfacewater_total_total_mgd'
#                 ], axis=1)
#   #x7 = x7.drop(['EPD_solar_total_total_total_bbtu_from_EPS_solar_total_total_total_bbtu',
#   #              'EPD_wind_total_total_total_bbtu_from_EPS_wind_total_total_total_bbtu'
#   #              ], axis=1)
#
#   out_df = pd.merge(x1, x2, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x3, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x4, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x5, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x6, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x7a, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x7b, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x8, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x9, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x10, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x11, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x12, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x13, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x14, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x15, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x16, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x17, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x18, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x19, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x20, how='left', on=['FIPS', 'State', 'County'])
#   out_df = pd.merge(out_df, x21, how='left', on=['FIPS', 'State', 'County'])
#   #out_df = out_df[out_df.State == 'CA']
#   value_columns = out_df.columns[3:].to_list()
#   out_df = pd.melt(out_df, value_vars=value_columns, var_name='flow_name', value_name='value', id_vars=['FIPS'])
#   out_df = out_df[out_df.value != 0]
#   i = out_df.columns.get_loc('flow_name')
#   df2 = out_df['flow_name'].str.split("_", expand=True)
#   out_df = pd.concat([out_df.iloc[:, :i], df2, out_df.iloc[:, i + 1:]], axis=1)
#   col = ['FIPS', 't1', 't2', 't3', 't4', 't5', 'T_unit', 'to', 's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter',
#          'value']
#   out_df.columns = col
#   out_df['parameter'].fillna('flow_value', inplace=True)
#   out_df['type'] = np.where(out_df['parameter'] == 'flow_value', 'A_collect', np.nan)
#   out_df['type'] = np.where(out_df['parameter'] == 'intensity', 'B_calculate', out_df['type'])
#   out_df['type'] = np.where((out_df['to'] == 'from') & (out_df['parameter'] == 'fraction'), 'C_source',
#                             out_df['type'])
#   out_df['type'] = np.where((out_df['to'] == 'to') & (out_df['parameter'] == 'fraction'), 'D_discharge',
#                             out_df['type'])
#   out_df = out_df.sort_values(by=['FIPS', 'type', 't1', 't2', 't3', 't4', 't5'])
#   out_df = out_df[['FIPS', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
#                    's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value']]
#   return out_df


x = prep_interbasin_transfer_data()
# print(x)
# for col in x.columns:
#    print(col)
x.to_csv(r"C:\Users\mong275\Local Files\Repos\flow\sample_data\test_output.csv", index=False)
import os

os.startfile(r"C:\Users\mong275\Local Files\Repos\flow\sample_data\test_output.csv")
