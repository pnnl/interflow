import numpy as np
import pandas as pd

from .clean import *


def calc_consumption_frac() -> pd.DataFrame:
    # TODO prepare test for consumption fraction calculations

    """calculating consumption fractions for various sectors from 1995 water use data.

    :return:                DataFrame of water consumption fractions for various sectors by county

    """

    # read in cleaned water use data for 1995
    df = prep_water_use_1995()

    # calculate water consumption fractions as consumptive use divided by delivered water
    df["DO_CF_Fr"] = df["DO-CUTot"] / df["DO-WDelv"]  # residential (domestic) sector freshwater consumption fraction
    df["CO_CF_Fr"] = df["CO-CUTot"] / df["CO-WDelv"]  # commercial sector freshwater consumption fraction
    df["IN_CF_Fr"] = df["IN-CUsFr"] / (df["IN-WFrTo"] + df["IN-PSDel"])  # ind sector freshwater consumption fraction
    df["IN_CF_Sa"] = (df["IN-CUsSa"]) / (df["IN-WSaTo"])  # ind sector saline water consumption fraction
    df["MI_CF_Fr"] = df["MI-CUsFr"] / df["MI-WFrTo"]  # mining sector freshwater consumption fraction
    df["MI_CF_Sa"] = df["MI-CUsSa"] / df["MI-WSaTo"]  # mining sector saline water consumption fraction
    df["LV_CF_Fr"] = df["LV-CUTot"] / df["LV-WTotl"]  # livestock freshwater water consumption fraction
    df["LA_CF_Fr"] = df["LA-CUTot"] / df["LA-WTotl"]  # aquaculture freshwater water consumption fraction

    # Replacing infinite (from divide by zero) with nan and filling with 0
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    return df


def calc_conveyance_loss_frac() -> pd.DataFrame:
    # TODO prepare test for conveyance loss fraction

    """calculating the fraction of water lost during conveyance for irrigation.

    :return:                DataFrame of water consumption fractions for various sectors by county

    """

    # read in cleaned water use data for 1995
    df = prep_water_use_1995()

    # calculate conveyance loss fraction of total water withdrawn for irrigation
    df["IR_CLoss_Frac"] = df['IR-CLoss'] / df['IR-WTotl']

    return df


def calc_hydroelectric_water_intensity(intensity_cap=165) -> pd.DataFrame:
    # TODO prepare test for hydro water intensity
    """calculating the MGD used per megawatt-hour generated from hydroelectric generation.

    :return:                DataFrame of water intensity of hydroelectric generation by county

    """

    # read in cleaned water use data for 1995
    df = prep_water_use_1995()

    # calculate water intensity fraction (IF) by dividing total water use (MGD) by total generation (MWh) by county
    df["HY_IF"] = df["HY-InUse"] / df["HY-InPow"]

    # removing outlier intensities
    df = df[df.HY_IF <= intensity_cap]

    df = df[["FIPS", "HY_IF"]]

    return df
