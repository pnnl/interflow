import numpy as np

from .reader import *


def prep_water_use_2015() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values and reducing to needed variables

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    # replacing characters for missing USGS data with value of zero
    df.replace("--", 0, inplace=True)

    # creating a list of required variables from full dataset
    variables_list = ['FIPS', 'STATE', 'COUNTY', 'PS-WGWFr', 'PS-WSWFr', 'PS-WGWSa', 'PS-WSWSa',
                      'DO-PSDel', 'PS-Wtotl', 'DO-WGWFr', 'DO-WSWFr', 'PT-WGWFr', 'PT-WGWSa',
                      'PT-WSWFr', 'PT-WSWSa', 'PT-RecWW', 'PT-PSDel', 'PT-CUTot', 'IN-WGWFr',
                      'IN-WSWFr', 'IN-WGWSa', 'IN-WSWSa', 'MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa',
                      'MI-WSWSa', 'IR-WGWFr', 'IR-WSWFr', 'IR-CUsFr'
                      ]
    # reducing dataframe to variables in variables_list
    df = df[variables_list]

    # change column names
    df = df.rename(columns={"COUNTY": "County"})
    df = df.rename(columns={"STATE": "State"})

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
                      'CO-CUTot', 'IN-CUsFr',
                      'CO-WDelv', 'IN-WFrTo', 'IN-PSDel', 'IN-CUsSa', 'IN-WSaTo', 'MI-CUTot',
                      'MI-WTotl', 'PT-WSWFr', 'MI-CUsFr', 'MI-WFrTo', 'MI-CUsSa', 'MI-WSaTo',
                      'LV-CUTot', 'LV-WTotl', 'LA-CUTot', 'LA-WTotl', 'IR-CUTot', 'IR-WTotl',
                      'HY-InUse', 'HY-InPow', 'IR-CLoss'
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


def prep_population_data() -> pd.DataFrame:
    """prepping population by county data by creating single FIPS code, filling in missing population data,
        and making sure population data is available for all counties in main dataset.

    :return:                DataFrame of population data at the county level

    """

    # read in population data by county
    df = get_population_data()
    df_statenames = get_state_fips_data()

    # Add leading zeros to County FIPS and State FIPS
    df["STATE FIPS"] = df["STATE FIPS"].apply(lambda x: '{0:0>2}'.format(x))
    df["COUNTY FIPS"] = df["COUNTY FIPS"].apply(lambda x: '{0:0>3}'.format(x))

    # creating a single FIPS columns from state and county FIPS
    df["FIPS"] = df["STATE FIPS"] + df["COUNTY FIPS"]

    # Fixing missing county population & state name data
    df['2015 POPULATION'] = np.where(df['FIPS'] == "46102", 13881.5, df['2015 POPULATION'])  # Oglala County, SD
    df['STATE/TERRITORY NAME'] = np.where(df['FIPS'] == "46102", "South Dakota", df['STATE/TERRITORY NAME'])
    df['2015 POPULATION'] = np.where(df['FIPS'] == "02158", 7913.5, df['2015 POPULATION'])  # Kusilvak Census Area, AK
    df['STATE/TERRITORY NAME'] = np.where(df['FIPS'] == "02158", "Alaska", df['STATE/TERRITORY NAME'])
    df['2015 POPULATION'] = np.where(df['FIPS'] == "78010", 50601, df['2015 POPULATION'])  # St. Croix, VI
    df['2015 POPULATION'] = np.where(df['FIPS'] == "78020", 4170, df['2015 POPULATION'])  # St. John, VI
    df['2015 POPULATION'] = np.where(df['FIPS'] == "78030", 51634, df['2015 POPULATION'])  # St. Thomas, VI

    # merge state abbreviation and state name crosswalk data to supply common State column
    df = pd.merge(df, df_statenames, how="left", on="STATE/TERRITORY NAME")

    # change column names
    df = df.rename(columns={"2015 POPULATION": "Population"})
    df = df.rename(columns={"COUNTY NAME": "County"})

    # reduce variables to required
    variables_list = ['FIPS', 'State', 'County', 'Population']
    df = df[variables_list]

    return df
