import numpy as np
import pandas as pd

from .clean import *



def calc_water_to_pws() -> pd.DataFrame:
    """calculating required variables from within the water_use_2015 dataframe.

    :return:                DataFrame of baseline water values in MGD for 2015 at the county level

    """

    # read in cleaned water use data for 2015
    df = clean_water_use_2015()

    # create list of columns needed
    variables_list = [
        'PS-WGWFr', 'PS-WSWFr', 'PS-WGWSa', 'PS-WSWSa',
        'DO-PSDel', 'PS-Wtotl', 'PT-PSDel'
    ]

    # reduce dataframe to variable list
    df = df[variables_list]

    # calculate public water supply to industrial sector


    #calculate public wa



    return df