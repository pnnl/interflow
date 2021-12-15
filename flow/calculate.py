import numpy as np
import pandas as pd


from .reader import *
import flow.clean as cl


def calc_pws_frac() -> pd.DataFrame:
    # TODO prepare test for consumption fraction calculations

    """calculating ratio of public water supply deliveries for the commercial and industrial sectors to the sum of
        public water supply deliveries to residential end users and thermoelectric cooling. Used in calculation
        of public water supply demand to all sectors.

    :return:                DataFrame of public water supply ratios for commercial and industrial sector.

    """

    # read in cleaned water use data for 1995
    df = cl.prep_water_use_1995()

    # calculate ratio of commercial pws to sum of domestic and thermoelectric cooling pws
    df["CO_PWS_frac"] = np.where((df['PS-DelDO'] + df['PS-DelPT']) <= 0,
                                 0,
                                 df['PS-DelCO'] / (df['PS-DelDO'] + df['PS-DelPT']))

    # calculate ratio of industrial pws to sum of domestic and thermoelectric cooling pws
    df["IN_PWS_frac"] = np.where((df['PS-DelDO'] + df['PS-DelPT']) <= 0,
                                 0,
                                 df['PS-DelIN'] / (df['PS-DelDO'] + df['PS-DelPT']))


    # reduce dataframe to required output
    df = df[["FIPS", "CO_PWS_frac", "IN_PWS_frac"]]

    return df


def calc_conveyance_loss_frac(df: pd.DataFrame, loss_cap=True, loss_cap_amt=.90) -> pd.DataFrame:
    # TODO prepare test for conveyance loss fraction

    """
    This function calculates the fraction of water lost during conveyance for irrigation for each row in the provided
    dataframe. The fraction is calculated as water lost in conveyance of irrigation water divided by total water
    withdrawn for irrigation.

    :param df:                             A pandas dataframe with required values
    :type df:                              pd.DataFrame

    :param loss_cap:                       If True, a cap is placed on the conveyance loss fraction
    :type loss_cap:                        bool

    :param loss_cap_amt:                   The amount at which irrigation losses are capped and values beyond are
                                            replaced by the specified cap amount. The default value is .90.
    :type loss_cap_amt:                    float

    :return:                               DataFrame of conveyance loss fractions by row

    """

    # calculate conveyance loss fraction of total water withdrawn for irrigation if irrigation water > 0
    df["IR_CLoss_Frac"] = df['IR-CLoss'] / df['IR-WTotl']

    # if a cap is placed on irrigation loss fraction, apply state average
    if loss_cap_amt < 0 or loss_cap_amt > 1:
        raise ValueError(f"loss_cap_amt must be a float between 0 and 1")

    if loss_cap:
        df["IR_CLoss_Frac"] = np.where(df['IR_CLoss_Frac'] > loss_cap_amt, loss_cap_amt, df["IR_CLoss_Frac"])
    else:
        df["IR_CLoss_Frac"] = df["IR_CLoss_Frac"]

    # Replacing infinite (from divide by zero) with nan and filling with 0
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    df = df[["FIPS", "State", "County", "IR_CLoss_Frac"]]

    return df






def calc_pws_discharge() -> pd.DataFrame:
    # TODO prepare test

    """calculating public water supply demand for the commercial and industrial sectors along with total
        public water supply exports or imports for each row of dataset.

    :return:                DataFrame of public water supply demand by sector, pws imports, and pws exports

    """

    # read in cleaned water use data variables for 2015
    df = cl.prep_water_use_2015(variables=["FIPS", 'State', 'County','PS-Wtotl', 'DO-PSDel', 'PT-PSDel'])

    # read in dataframe of commercial and industrial pws ratios
    df_pws = calc_pws_frac()

    # merge dataframes
    df = pd.merge(df, df_pws, how="left", on="FIPS")

    # calculate public water supply deliveries to commercial and industrial sectors
    df['CO-PSDel'] = df["CO_PWS_frac"]*(df['DO-PSDel'] + df['PT-PSDel'])
    df['IN-PSDel'] = df["IN_PWS_frac"]*(df['DO-PSDel'] + df['PT-PSDel'])

    #calculate total deliveries from public water supply to all sectors
    df['PS-del'] = df['DO-PSDel'] + df['PT-PSDel'] + df['CO-PSDel'] + df['IN-PSDel']

    # calculate public water supply imports and exports
    df['PS-IX'] = np.where(df['PS-Wtotl'] - df['PS-del'] < 0,  # if withdrawals < deliveries
                           df['PS-del'] - df['PS-Wtotl'],  # import quantity
                           0)

    df['PS-EX'] = np.where(df['PS-Wtotl'] - df['PS-del'] > 0,  # if withdrawals > deliveries
                            df['PS-Wtotl'] - df['PS-del'],  # export quantity
                           0)

    df = df[["FIPS", 'State', 'County', 'PS-Wtotl', 'DO-PSDel', 'PT-PSDel',
             "CO-PSDel", "IN-PSDel", "PS-IX", 'PS-EX', 'PS-del']]

    return df


def convert_mwh_bbtu(x: float) -> float:
    # TODO prepare test

    """calculating consumption fractions for various sectors from 1995 water use data.

    :return:                DataFrame of water consumption fractions for various sectors by county

    """
    bbtu = x*0.003412

    return bbtu

def calc_population_county_weight(df:pd.DataFrame) -> pd.DataFrame:
    # TODO move to weighting.py

    """calculates the percentage of state total population by county and merges to provided dataframe
    by 'State'

    :return:                DataFrame of water consumption fractions for various sectors by county

    """
    df_state = cl.prep_water_use_2015(variables=["FIPS", "State", "County", "population"])
    df_state_sum = df_state.groupby("State", as_index=False).sum()
    df_state_sum = df_state_sum.rename(columns={"population": "state_pop_sum"})
    df_state = pd.merge(df_state, df_state_sum, how='left', on='State')
    df_state['pop_weight'] = df_state['population']/df_state['state_pop_sum']
    df_state = df_state[['FIPS', 'State', 'County', 'pop_weight']]

    df_state = pd.merge(df_state, df, how="left", on="State")

    return df_state


