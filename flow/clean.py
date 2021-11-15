import numpy as np
import pandas as pd

from .reader import *


def prep_water_use_2015() -> pd.DataFrame:
    """replacing characters for missing USGS 2015 water data with zero

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
                      'MI-WSWSa'
                      ]
    # reducing dataframe to variables in variables_list
    df = df[variables_list]

    return df
