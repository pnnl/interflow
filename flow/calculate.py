import numpy as np
import pandas as pd

from .reader import *
import flow.clean as cl

def calc_public_water_supply_energy(water_data_path=None, surface_pumping_intensity=145, ground_pumping_intensity=920,
                                    surface_treatment_intensity=405, ground_treatment_intensity=205,
                                    distribution_intensity=1040, total=False):
    """calculate energy usage by the public water supply sector. Takes a dataframe of public water supply withdrawals
    from surface water and groundwater sources and calculates total energy use for surface water pumping, groundwater
    pumping, surface water treatment, groundwater treatment, and distribution. Returns a DataFrame of energy use for
    each category in billion btu per year.

    :return:                DataFrame of energy use in public water supply

    """
    # load data
    if water_data_path:
        df = pd.read_csv(water_data_path)
    else:
        df = cl.prep_water_use_2015(variables=['County', 'State', 'FIPS', 'fresh_groundwater_pws_mgd',
                                               'fresh_surface_water_pws_mgd',
                                               'saline_groundwater_pws_mgd', 'saline_surface_water_pws_mgd'])

    # TODO link to irrigation pumping intensity based on average well depth
    # TODO add in saline water for pumping electricity

    # electricity in public water supply surface water pumping
    df['electricity_pws_surface_pumping'] = surface_pumping_intensity * df["fresh_surface_water_pws_mgd"]

    # electricity in public water supply groundwater pumping
    df['electricity_pws_ground_pumping'] = ground_pumping_intensity * df["fresh_groundwater_pws_mgd"]

    # electricity in public water supply surface water treatment
    df['electricity_pws_surface_treatment'] = surface_treatment_intensity * df["fresh_surface_water_pws_mgd"]

    # electricity in public water supply groundwater treatment
    df['electricity_pws_ground_treatment'] = ground_treatment_intensity * df["fresh_groundwater_pws_mgd"]

    # electricity in public water supply distribution
    df['electricity_pws_distribution'] = (distribution_intensity *
                                    (df["fresh_surface_water_pws_mgd"] + df["fresh_groundwater_pws_mgd"]))

    electricity_list = ['electricity_pws_surface_pumping','electricity_pws_ground_pumping',
                        'electricity_pws_surface_treatment', 'electricity_pws_ground_treatment',
                        'electricity_pws_distribution']

    # TODO add in saline water for treatment electricity

    # desalination treatment from EPRI 2013
    #13, 600    kWh / MG

    for column in electricity_list:
        df[column] = convert_kwh_bbtu(df[column])

    # if total:
    # add all energy parameters together

    return df


def calc_pws_discharge() -> pd.DataFrame:
    # TODO prepare test

    """calculating public water supply demand for the commercial and industrial sectors along with total
        public water supply exports or imports for each row of dataset.

    :return:                DataFrame of public water supply demand by sector, pws imports, and pws exports

    """

    # read in cleaned water use data variables for 2015
    df = cl.prep_water_use_2015(variables=["FIPS", 'State', 'County', 'PS-Wtotl', 'DO-PSDel', 'PT-PSDel'])

    # read in dataframe of commercial and industrial pws ratios
    df_pws = calc_pws_frac()

    # merge dataframes
    df = pd.merge(df, df_pws, how="left", on="FIPS")

    # calculate public water supply deliveries to commercial and industrial sectors
    df['CO-PSDel'] = df["CO_PWS_frac"] * (df['DO-PSDel'] + df['PT-PSDel'])
    df['IN-PSDel'] = df["IN_PWS_frac"] * (df['DO-PSDel'] + df['PT-PSDel'])

    # calculate total deliveries from public water supply to all sectors
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
    """converts MWh to billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.003412

    return bbtu

def convert_kwh_bbtu(x: float) -> float:
    """converts kWh to billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.000003412140

    return bbtu


def calc_population_county_weight(df: pd.DataFrame) -> pd.DataFrame:
    # TODO move to weighting.py

    """calculates the percentage of state total population by county and merges to provided dataframe
    by 'State'

    :return:                DataFrame of water consumption fractions for various sectors by county

    """
    df_state = cl.prep_water_use_2015(variables=["FIPS", "State", "County", "population"])
    df_state_sum = df_state.groupby("State", as_index=False).sum()
    df_state_sum = df_state_sum.rename(columns={"population": "state_pop_sum"})
    df_state = pd.merge(df_state, df_state_sum, how='left', on='State')
    df_state['pop_weight'] = df_state['population'] / df_state['state_pop_sum']
    df_state = df_state[['FIPS', 'State', 'County', 'pop_weight']]

    df_state = pd.merge(df_state, df, how="left", on="State")

    return df_state
