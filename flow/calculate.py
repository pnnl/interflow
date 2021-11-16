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


def calc_conveyance_loss_frac(loss_cap=True, loss_cap_amt=.90, all_variables=False) -> pd.DataFrame:
    # TODO prepare test for conveyance loss fraction

    """calculating the fraction of water lost during conveyance for irrigation.

    :return:                DataFrame of water consumption fractions for various sectors by county

    """

    # read in cleaned water use data for 1995
    df = prep_water_use_1995()

    # calculate conveyance loss fraction of total water withdrawn for irrigation if irrigation water > 0
    df["IR_CLoss_Frac"] = np.where(df['IR-WTotl'] == 0, 0, df['IR-CLoss'] / df['IR-WTotl'])

    # if a cap is placed on irrigation loss fraction, apply state average
    if loss_cap_amt < 0 or loss_cap_amt > 1:
        raise ValueError(f"loss_cap_amt must be a float between 0 and 1")

    if loss_cap:
        df_state = df[["StateCode", "IR_CLoss_Frac"]].groupby("StateCode", as_index=False).mean()
        df_state = df_state.rename(columns={"IR_CLoss_Frac": "IR_CLoss_Frac_avg"})
        df = pd.merge(df, df_state, how="left", on="StateCode")
        df["IR_CLoss_Frac"] = np.where(df['IR_CLoss_Frac'] > loss_cap_amt, df["IR_CLoss_Frac_avg"], df["IR_CLoss_Frac"])
    else:
        df["IR_CLoss_Frac"] = df["IR_CLoss_Frac"]

    if all_variables:
        df = df
    else:
        df = df[["State", "CountyName", "FIPS", "IR_CLoss_Frac"]]

    return df


def calc_hydroelectric_water_intensity(intensity_cap=165, region_avg=True) -> pd.DataFrame:
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

    if region_avg:
        pass

    else:
        df = df[["FIPS", "HY_IF"]]

    df = df[["FIPS", "HY_IF"]]

    return df
