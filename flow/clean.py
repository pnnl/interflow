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
                      'TP-TotPop', 'PS-WGWFr', 'PS-WSWFr', 'PS-WGWSa', 'PS-WSWSa','DO-PSDel',
                      'PS-Wtotl', 'DO-WGWFr', 'DO-WSWFr', 'PT-WGWFr', 'PT-WGWSa', 'PT-WSWFr',
                      'PT-WSWSa', 'PT-RecWW', 'PT-PSDel', 'PT-CUTot', 'IN-WGWFr', 'IN-WSWFr',
                      'IN-WGWSa', 'IN-WSWSa', 'MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa', 'MI-WSWSa',
                      'IR-WGWFr', 'IR-WSWFr', 'IR-CUsFr'
                      ]
    numerical_list = variables_list[3:]
    for col in numerical_list:
        df[col] = df[col].astype(float)

    # reducing dataframe to variables in variables_list
    df = df[variables_list]

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

    return df


