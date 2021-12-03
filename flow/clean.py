import numpy as np

from .reader import *


def prep_water_use_2015(variables=None, all_variables=False) -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    # replacing characters for missing USGS data with value of zero
    df.replace("--", 0, inplace=True)

    # creating a list of required variables from full dataset
    variables_list = ['FIPS', 'STATE', 'COUNTY',
                      'TP-TotPop', 'PS-WGWFr', 'PS-WSWFr', 'PS-WGWSa', 'PS-WSWSa', 'DO-PSDel',
                      'PS-Wtotl', 'DO-WGWFr', 'DO-WSWFr', 'PT-WGWFr', 'PT-WGWSa', 'PT-WSWFr',
                      'PT-WSWSa', 'PT-RecWW', 'PT-PSDel', 'PT-CUTot', 'IN-WGWFr', 'IN-WSWFr',
                      'IN-WGWSa', 'IN-WSWSa', 'MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa', 'MI-WSWSa',
                      'IR-WGWFr', 'IR-WSWFr', 'IR-CUsFr'
                      ]

    # reducing dataframe to variables in variables_list
    df = df[variables_list]

    numerical_list = variables_list[3:]
    for col in numerical_list:
        df[col] = df[col].astype(float)

    # change column names
    df = df.rename(columns={"COUNTY": "County"})
    df = df.rename(columns={"STATE": "State"})

    if variables is None and all_variables is False:
        variables = ['FIPS', "State", "County"]
        df = df[variables]
    elif variables is None and all_variables is True:
        df = df
    else:
        df = df[variables]

    return df


def prep_water_use_1995() -> pd.DataFrame:
    """prepping USGS 1995 water use data by replacing missing values, fixing FIPS codes,
     and reducing to needed variables

    :return:                DataFrame of a number of water values for 1995 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_1995()

    # create a complete FIPS code from the sum of the state and county level FIPS codes
    df["FIPS"] = df["StateCode"] + df["CountyCode"]

    # creating a list of required variables from full 1995 dataset
    variables_list = ['FIPS', 'State', 'CountyName', 'StateCode', 'DO-CUTot', 'DO-WDelv',
                      'CO-CUTot', 'IN-CUsFr', 'CO-WDelv', 'IN-WFrTo', 'IN-PSDel', 'IN-CUsSa',
                      'IN-WSaTo', 'MI-CUTot', 'MI-WTotl', 'PT-WSWFr', 'MI-CUsFr', 'MI-WFrTo',
                      'MI-CUsSa', 'MI-WSaTo', 'LV-CUTot', 'LV-WTotl', 'LA-CUTot', 'LA-WTotl',
                      'IR-CUTot', 'IR-WTotl', 'HY-InUse', 'HY-InPow', 'IR-CLoss', 'PS-DelCO',
                      'PS-DelIN', 'PS-UsLos', 'PS-DelTO', 'PS-DelDO', 'PS-DelPT', 'PS-WTotl'
                      ]

    # reducing dataframe to variables in variables_list
    df = df[variables_list]

    # FIPS code changes between 1995 and 2015
    df['FIPS'] = np.where(df['FIPS'] == "12025", "12086", df['FIPS'])  # Miami-Dade County, FL
    df['FIPS'] = np.where(df['FIPS'] == "46113", "46102", df['FIPS'])  # Oglala Lakota County, SD
    df['FIPS'] = np.where(df['FIPS'] == "02232", "02105", df['FIPS'])  # Hoonah-Angoon Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "02270", "02158", df['FIPS'])  # Kusilvak Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "02280", "02195", df['FIPS'])  # Petersburg Borough, AK
    df['FIPS'] = np.where(df['FIPS'] == "02201", "02198", df['FIPS'])  # Wales-Hyder Census Area, AK
    df['FIPS'] = np.where(df['FIPS'] == "78001", "78010", df['FIPS'])  # St. Croix County, VI
    df['FIPS'] = np.where(df['FIPS'] == "78003", "78020", df['FIPS'])  # St. John County, VI
    df['FIPS'] = np.where(df['FIPS'] == "78004", "78030", df['FIPS'])  # St. Thomas County, VI

    # Copies data from counties that split into multiple FIPS codes between 1995 and 2015 into new rows
    wrangell_petersburg_index = df.index[df['FIPS'] == "02280"].tolist()  # Wrangell, AK from Wrangell-Petersburg, AK
    df = df.append(df.loc[wrangell_petersburg_index * 1].assign(FIPS="02275"), ignore_index=True)

    skagway_index = df.index[df['FIPS'] == "02232"].tolist()  # Hoonah-Angoon, AK from Skagway-Hoonah-Angoon, AK
    df = df.append(df.loc[skagway_index * 1].assign(FIPS="02230"), ignore_index=True)

    boulder_index = df.index[df['FIPS'] == "08013"].tolist()  # Broomfield County, CO from Boulder County, CO
    df = df.append(df.loc[boulder_index * 1].assign(FIPS="08014"), ignore_index=True)

    # change column names
    df = df.rename(columns={"CountyName": "County"})

    numerical_list = variables_list[4:]
    for col in numerical_list:
        df[col] = df[col].astype(float)

    return df

def prep_county_identifier() -> pd.DataFrame:
    """preps each wastewater treatment facility data file, cleans input,
            and brings them together to produce a single wastewater treatment datafile
            by FIPS county code.

            :return:                DataFrame county level wastewater treatment data

            """
    df = get_county_identifier_data()
    df["COUNTY_SHORT"] = df["COUNTY_SHORT"].str.replace(' ', '')  # remove spaces between words
    df['COUNTY_SHORT'] = df['COUNTY_SHORT'].str.lower()  # change to lowercase
    df["identifier"] = df["STATE"] + df["COUNTY_SHORT"]  # add identifier column
    df['FIPS'] = df['FIPS'].apply(lambda x: '{0:0>5}'.format(x))  # add leading zero
    df = df[["FIPS", 'identifier']]

    return df

def prep_wastewater_data() -> pd.DataFrame:
    """preps each wastewater treatment facility data file, cleans input,
    and brings them together to produce a single wastewater treatment datafile
    by FIPS county code.

    :return:                DataFrame county level wastewater treatment data

    """

    # read in each of the wastewater facility data files
    df_county = prep_county_identifier()
    df_ww_flow = get_wastewater_flow_data()
    df_ww_type = get_wastewater_facility_type_data()
    df_ww_loc = get_wastewater_facility_loc_data()
    df_ww_dis = get_wastewater_facility_discharge_data()

    # wastewater discharge type dictionary
    dis_dict = {'outfall to surface waters': 'ww_sd',
                'ocean discharge': 'ww_od',
                'deep well': 'ww_gd',
                "reuse: industrial": 'ww_in',
                'evaporation': 'ww_evap',
                'spray irrigation': 'ww_ir',
                'overland flow no discharge': 'ww_ww',
                'overland flow with discharge': 'ww_sd',
                'discharge to another facility': 'ww_ww',
                'combined sewer overflow (cso) discharge': 'ww_sd',
                'other': 'ww_sd',
                'discharge to groundwater': 'ww_gd',
                'no discharge, unknown': 'ww_ww',
                'reuse: irrigation': 'ww_ir',
                'reuse: other non-potable': 'ww_sd',
                'reuse: indirect potable': 'ww_sd',
                'reuse: potable': 'ww_ps',
                'reuse: groundwater recharge': 'ww_gd'}

    treat_dict = {'raw discharge': 'no_treatment',
                  'primary (45mg/l< bod)': 'ww_prim',
                  'advanced primary': 'ww_adv',
                  'secondary wastewater treatment': 'ww_sec',
                  'secondary': 'ww_sec',
                  'advanced treatment': 'ww_adv'}

    # wastewater facility locations by plant number

    df_ww_loc["PRIMARY_COUNTY"] = np.where(df_ww_loc["PRIMARY_COUNTY"] == "Mayaguez",
                                           "mayaquez",
                                           df_ww_loc["PRIMARY_COUNTY"])  # correction
    df_ww_loc["PRIMARY_COUNTY"] = np.where(df_ww_loc["PRIMARY_COUNTY"] == "Bedford City",
                                           "Bedford",
                                           df_ww_loc["PRIMARY_COUNTY"])  # correction
    df_ww_loc['PRIMARY_COUNTY'] = df_ww_loc['PRIMARY_COUNTY'].str.lower()  # change to lowercase
    df_ww_loc["PRIMARY_COUNTY"] = df_ww_loc["PRIMARY_COUNTY"].str.replace(' ', '')  # remove spaces between words
    df_ww_loc['CWNS_NUMBER'] = df_ww_loc['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero

    df_ww_loc["identifier"] = df_ww_loc["STATE"] + df_ww_loc["PRIMARY_COUNTY"]  # add identifier column
    df_ww_loc = pd.merge(df_ww_loc, df_county, how="left", on="identifier")  # merge dataframes
    df_ww_loc = df_ww_loc[["CWNS_NUMBER", "FIPS", "STATE"]]  # reducing to required variables

    # wastewater flows (MGD) by plant number
    df_ww_flow = df_ww_flow[["CWNS_NUMBER", "EXIST_INFILTRATION", "EXIST_TOTAL"]]  # reducing to required variables
    df_ww_flow = df_ww_flow.dropna(subset=["EXIST_TOTAL"])  # drop treatment plants with zero flows

    df_ww_flow["EXIST_INFILTRATION"] = df_ww_flow["EXIST_INFILTRATION"].fillna(0)
    df_ww_flow['EXIST_AVG'] = df_ww_flow["EXIST_TOTAL"] - df_ww_flow["EXIST_INFILTRATION"]  # total without infiltration
    df_ww_flow['CWNS_NUMBER'] = df_ww_flow['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero

    # merge ww flow data and ww discharge data on ww plant code
    df_ww_flow = pd.merge(df_ww_flow, df_ww_loc, how="left", on='CWNS_NUMBER')
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "AS"]
    df_ww_flow = df_ww_flow[df_ww_flow.STATE != "GU"]

    # wastewater discharge types by plant number
    df_ww_dis['DISCHARGE_METHOD'] = df_ww_dis['DISCHARGE_METHOD'].str.replace(',', '')  # remove commas
    df_ww_dis['DISCHARGE_METHOD'] = df_ww_dis['DISCHARGE_METHOD'].str.lower()  # change to lowercase
    df_ww_dis['DISCHARGE_METHOD'] = np.where(df_ww_dis['DISCHARGE_METHOD'] == "reuse: ground water recharge",
                                             "reuse: groundwater recharge",
                                             df_ww_dis['DISCHARGE_METHOD'])
    df_ww_dis['DISCHARGE_METHOD'] = np.where(df_ww_dis['DISCHARGE_METHOD'] == "cso discharge",
                                             "combined sewer overflow (cso) discharge",
                                             df_ww_dis['DISCHARGE_METHOD'])
    df_ww_dis['DISCHARGE_METHOD_BIN'] = df_ww_dis['DISCHARGE_METHOD'].map(dis_dict)  # bin discharge types
    df_ww_dis = df_ww_dis[["CWNS_NUMBER", 'DISCHARGE_METHOD_BIN', 'PRES_FLOW_PERCENTAGE']]  # keep required columns
    df_ww_dis['CWNS_NUMBER'] = df_ww_dis['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero
    df_ww_dis['PRES_FLOW_PERCENTAGE'] = df_ww_dis['PRES_FLOW_PERCENTAGE'] / 100  # convert to fraction
    df_ww_dis = pd.pivot_table(df_ww_dis, values='PRES_FLOW_PERCENTAGE', index=['CWNS_NUMBER'],
                               columns=['DISCHARGE_METHOD_BIN'],
                               aggfunc=np.sum)  # pivot to get discharge types as columns
    df_ww_dis = df_ww_dis.reset_index()  # reset index to remove multi-index from pivot table
    df_ww_dis = df_ww_dis.rename_axis(None, axis=1)  # drop index name
    discharge_col = df_ww_dis.columns[1:]  # create list of discharge columns
    for col in discharge_col:  # fill nan rows with 0
        df_ww_dis[col] = df_ww_dis[col].fillna(0)
    df_ww_dis['sum_pct'] = df_ww_dis.iloc[:, 1:].sum(axis=1)  # calculate sum of percentages
    df_ww_dis['ww_sd'] = np.where(df_ww_dis['sum_pct'] == 0, 1, df_ww_dis['ww_sd'])  # fill blanks with 100% sd
    df_ww_dis['sum_pct'] = df_ww_dis.iloc[:, 1:-1].sum(axis=1)  # recalculate sum

    # merge ww flow data and ww discharge data on ww plant code
    df_ww_flow = pd.merge(df_ww_flow, df_ww_dis)

    # wastewater treatment types by plant number
    df_ww_type = df_ww_type[['CWNS_NUMBER', 'PRES_EFFLUENT_TREATMENT_LEVEL']]
    df_ww_type['pct'] = 1  # add a percent column
    df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'] = df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'].str.lower()  # lowercase
    df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'] = np.where(df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'] ==
                                                           "primary (45mg/l is less than bod)",
                                                           "primary (45mg/l< bod)",
                                                           df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'])

    df_ww_type['TREATMENT_LEVEL_BIN'] = df_ww_type['PRES_EFFLUENT_TREATMENT_LEVEL'].map(treat_dict)  # bin treat. types
    df_ww_type = pd.pivot_table(df_ww_type, values='pct', index=['CWNS_NUMBER'],
                                columns=['TREATMENT_LEVEL_BIN'],
                                aggfunc=np.sum)  # pivot to get treatment types as columns
    df_ww_type = df_ww_type.reset_index()  # reset index to remove multi-index from pivot table
    df_ww_type = df_ww_type.rename_axis(None, axis=1)  # drop index name

    treat_col = df_ww_type.columns[1:]  # create list of treatment columns
    for col in treat_col:  # fill nan rows with 0
        df_ww_type[col] = df_ww_type[col].fillna(0)
    df_ww_type['sum_type'] = df_ww_type.iloc[:, 1:].sum(axis=1)  # calculate sum
    df_ww_type['CWNS_NUMBER'] = df_ww_type['CWNS_NUMBER'].apply(lambda x: '{0:0>11}'.format(x))  # add leading zero

    # merge ww flow data and ww treatment data on ww plant code
    df_ww_flow = pd.merge(df_ww_flow, df_ww_type, how='left', on='CWNS_NUMBER')

    # fix missing treatment levels for a small number of plants
    for col in df_ww_type.columns:  # fill nan rows with 0
        df_ww_flow[col] = df_ww_flow[col].fillna(0)
    df_ww_flow['ww_sec'] = np.where(df_ww_flow['sum_type'] < 1, 1, df_ww_flow['ww_sec'])
    df_ww_flow['sum_type'] = df_ww_flow.iloc[:, 15:-1].sum(axis=1)  # recalculate sum

    # reducing list of variables
    df_ww = df_ww_flow.drop(['sum_type', 'sum_pct'], axis = 1)

    column_list = df_ww.columns[6:]
    for column in column_list:
        df_ww[column] = df_ww[column]*df_ww['EXIST_TOTAL']

    # group by FIPS code to get wastewater treatment flows, treatment type flows, and discharge flows by county
    df_ww = df_ww.groupby("FIPS", as_index=False).sum()

    return df_ww


def prep_power_plant_location() -> pd.DataFrame:
    """prepping USGS 1995 water use data by replacing missing values, fixing FIPS codes,
     and reducing to needed variables

    :return:                DataFrame of a number of water values for 1995 at the county level

    """
    # county data
    df_county = prep_county_identifier()
    df_plant = get_power_plant_county_data()


    df_county["identifier"] = df_county['identifier'].str.replace("'", '', regex=True)
    df_county["identifier"] = df_county["identifier"].str.replace('.', '', regex=True)  # remove periods
    df_county["identifier"] = df_county["identifier"].str.replace('-', '', regex=True)  # remove dashes
    df_county["identifier"] = df_county["identifier"].str.replace(r"[^\w ]", '',  regex=True)

    df_plant = df_plant.drop_duplicates()
    df_plant = df_plant.dropna(subset=["Plant Code"])

    df_plant['County'] = df_plant['County'].str.lower()  # change to lowercase
    df_plant["County"] = df_plant["County"].str.replace(' ', '')  # remove spaces between words
    df_plant["identifier"] = df_plant["State"] + df_plant["County"]  # add identifier column
    df_plant["identifier"] = df_plant["identifier"].str.replace(r"[^\w ]", '',  regex=True)


    city_list = ['VAchesapeakecity', 'VAportsmouthcity', 'VAhopewellcity', 'VAalexandriacity',
                 'VAcovingtoncity', 'VAsuffolkcity', 'VAharrisonburgcity', 'VAsalemcity',
                 'VAlynchburgcity', 'VAdanvillecity', 'VAmanassascity', 'VAhamptoncity',
                 'VAvirginiabeachcity', 'VAbristolcity', 'MOstlouiscity']

    for i in city_list:
        df_plant["identifier"] = np.where(df_plant["identifier"] == i,
                                          df_plant["identifier"].str.replace('city', '', regex=True),
                                          df_plant["identifier"])
    df_plant["identifier"] = np.where(df_plant["identifier"] == "MEchainofponds", "MEfranklin", df_plant["identifier"])
    df_plant["identifier"] = np.where(df_plant["identifier"] == "AKwadehampton", "AKkusilvak", df_plant["identifier"])
    df_plant["identifier"] = np.where(df_plant["identifier"] == "AKprinceofwalesketchikan",
                                      "AKprinceofwaleshyder", df_plant["identifier"])
    df_plant["identifier"] = np.where(df_plant["identifier"] == "AKwrangellpetersburg",
                                      "AKpetersburg", df_plant["identifier"])
    df_plant["identifier"] = np.where(df_plant["identifier"] == "AKwrangellpetersburg",
                                      "AKpetersburg", df_plant["identifier"])

    skagway_list = [66, 7751, 56542]
    for s in skagway_list:
        df_plant["identifier"] = np.where(df_plant["Plant Code"] == s,
                                          "AKskagway",
                                          df_plant["identifier"])
    hoonah_list = [6702, 7462, 7463]
    for h in hoonah_list:
        df_plant["identifier"] = np.where(df_plant["Plant Code"] == h,
                                          "AKhoonahangoon",
                                          df_plant["identifier"])

    df_plant = pd.merge(df_plant, df_county, how="left", on="identifier")  # merge dataframes
    df_plant = df_plant.rename(columns={"Plant Code": "plant_code"})


    return df_plant

def prep_electricity_generation() -> pd.DataFrame:
    """ Provides a dataframe of electricity generation (MWh) and fuel use (BBTU) per year by generating technology type
    and by FIPS code. Can be used to estimate fuel use for electricity generation by type for each county
    and total electricity generation by county.

    :return:                DataFrame of ____________________

    """

    # read in electricity generation data by power plant id
    df = get_electricity_generation_data()

    # read in power plant location data by power plant id
    df_loc = prep_power_plant_location()

    # remove unnecessary variables
    df_loc = df_loc[['FIPS', 'plant_code']]
    df = df[['Plant Id', "AER\nFuel Type Code", "Total Fuel Consumption\nMMBtu", "Net Generation\n(Megawatthours)"]]

    # create a dictionary to bin power plant fuel types
    fuel_dict = {'SUN': 'solar',  #solar
                'COL': 'coal',  # coal
                'DFO': 'oil',  # distillate petroleum
                "GEO": 'geothermal',  # geothermal
                'HPS': 'hydro',  # hydro pumped storage
                'HYC': 'hydro',  # hydro conventional
                'MLG': 'biomass',  # biogenic municipal solid waste and landfill gas
                'NG': 'natgas',  # natural gas
                'NUC': 'nuclear',  # nuclear
                'OOG': 'other',  # other gases
                'ORW': 'other',  # other renewables
                'OTH': 'other',  # other
                'PC': 'oil',  # petroleum coke
                'RFO': 'oil',  # residual petroleum
                'WND': 'wind',  # wind
                'WOC': 'coal',  # waste coal
                'WOO': 'oil',  # waste oil
                'WWW': 'biomass'}  # wood and wood waste

    # rename columns in power plant generation data file
    df = df.rename(columns={"Plant Id": "plant_code"})
    df = df.rename(columns={"AER\nFuel Type Code": "fuel_type"})
    df = df.rename(columns={"Total Fuel Consumption\nMMBtu": "fuel_amt"})
    df = df.rename(columns={"Net Generation\n(Megawatthours)": "generation_mwh"})

    # changing string columns to numeric
    string_col = df.columns[2:]  # create list of string columns
    for col in string_col:
        df[col] = df[col].str.replace(r"[^\w ]", '',  regex=True)  # replace any non alphanumeric values
        df[col] = df[col].astype(float)  # convert to float

    # removing power plant generation rows that should not be included
    df = df[df.plant_code != 99999]  # removing state level estimated differences rows

    # dropping power plants with zero fuel use and zero output
    index_list = df[(df['fuel_amt'] <= 0) & (df['generation_mwh'] <= 0)].index  # list of indices with both zero values
    df.drop(index_list, inplace=True)  # dropping rows with zero fuel and zero generation amount

    # using fuel type dictionary to bin fuel types
    df['fuel_type'] = df['fuel_type'].map(fuel_dict)  # bin fuel types

    # converting units to billion btu from million btu
    df["fuel_amt"] = df["fuel_amt"]/1000

    # grouping rows by both plant code and fuel type
    df = df.groupby(['plant_code','fuel_type'], as_index = False).sum()

    # merging power plant location data with power plant generation data
    df = pd.merge(df, df_loc, how='left', on= 'plant_code')

    # TODO calculate fuel consumption by county
    # TODO calculate generation amount by type by county
    #  above should be in calculate

    return df

def prep_irrigation_data() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_irrigation_data()

    

    return df

def prep_interbasin_transfer_data() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    return df

def prep_electricity_demand_data() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    return df

def prep_fuel_demand_data() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    return df

def prep_fuel_production_data() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    return df