import numpy as np
import pandas as pd

from .reader import get_water_use_1995, get_water_use_2015


def prep_water_2015(df_interconnect: pd.DataFrame) -> pd.DataFrame:
    """The 2015 USGS water data is merged with the interconnect by county file to link the 2015 water data to each
    interconnect.

    :param df_interconnect:                 A data frame of ...
    :type df_interconnect:                  pd.DataFrame

    :return:                                DataFrame of a number of water values for 2015 at the county level

    """

    # read in base water use data for 2015
    df_wateruse = get_water_use_2015()

    # merging datafiles
    df = pd.merge(df_wateruse, df_interconnect, how="left", on=["FIPS"])

    # replacing characters for missing USGS data with value of zero
    df.replace("--", 0, inplace=True)

    return df


def prep_water_1995():
    """asdf"""

    # read in base water use data for 1995
    df_1995 = get_water_use_1995()

    # creating a single FIPS code from hte state and county codes to be able to merge with other dataframes
    df_1995["FIPS"] = df_1995["StateCode"] + df_1995["CountyCode"]

    # calculate 1995 Residential (domestic) consumption fraction
    df_1995["DO_CF"] = df_1995["DO-CUTot"] / df_1995["DO-WDelv"]

    # 1995 industrial & commercial (INCO) consumption fractions combined
    # commercial only consumes fresh water so all consumptive use is used here instead of separating out
    df_1995["INCO_CF_Fr"] = ((df_1995["CO-CUTot"] +
                              df_1995["IN-CUsFr"])) / (df_1995["CO-WDelv"] + (df_1995["IN-WFrTo"] + df_1995["IN-PSDel"]))
    df_1995["INCO_CF_Sa"] = (df_1995["IN-CUsSa"]) / (df_1995["IN-WSaTo"])

    # 1995 mining consumption fractions for fresh (MI_CF_Fr) and saline water (MI_CF_Sa)
    df_1995["MI_CF"] = df_1995["MI-CUTot"] / df_1995["MI-WTotl"]  # total consumption fraction
    df_1995["MI_CF_Fr"] = df_1995["MI-CUsFr"] / df_1995["MI-WFrTo"]  # fresh water consumption fraction
    df_1995["MI_CF_Sa"] = df_1995["MI-CUsSa"] / df_1995["MI-WSaTo"]  # saline water consumption fraction

    # 1995 livestock (LV_CF), auquaculture (LA_CF), and irrigation (IR_CF) consumption fractions
    df_1995["LV_CF"] = df_1995["LV-CUTot"] / df_1995["LV-WTotl"]
    df_1995["LA_CF"] = df_1995["LA-CUTot"] / df_1995["LA-WTotl"]
    df_1995["IR_CF"] = df_1995["IR-CUTot"] / df_1995["IR-WTotl"]

    # Replacing infinite (from divide by zero) with nan and filling with 0
    df_1995.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_1995.fillna(0, inplace=True)

    return df_1995

