import numpy as np
import pandas as pd

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
                      'MI-WSWSa', 'IC-WGWFr', 'IC-WSWFr', 'IC-CUsFr', 'IG-WGWFr', 'IG-WSWFr',
                      'IG-CUsFr'
                      ]
    # reducing dataframe to variables in variables_list
    df = df[variables_list]

    return df


def prep_water_use_1995() -> pd.DataFrame:
    """prepping USGS 2015 water use data by replacing missing values, fixing FIPS codes,
     and reducing to needed variables

    :return:                DataFrame of a number of water values for 1995 at the county level

    """

    # read in water use data for 2015 in million gallons per day by county
    df = get_water_use_2015()

    # replacing characters for missing USGS data with value of zero
    df.replace("--", 0, inplace=True)

    # creating a list of required variables from full dataset
    variables_list = ['StateCode', 'CountyCode', 'DO-CUTot', 'DO-WDelv', 'CO-CUTot', 'IN-CUsFr', 'CO-WDelv',
                      'IN-WFrTo', 'IN-PSDel', 'IN-CUsSa', 'IN-WSaTo', 'MI-CUTot', 'MI-WTotl',
                      'PT-WSWFr', 'MI-CUsFr', 'MI-WFrTo', 'MI-CUsSa', 'MI-WSaTo', 'LV-CUTot',
                      'LV-WTotl', 'LA-CUTot', 'LA-WTotl', 'IR-CUTot', 'IR-WTotl', 'HY-InUse',
                      'HY-InPow', 'IR-CLoss'
                      ]
    # reducing dataframe to variables in variables_list
    df = df[variables_list]

    return df
