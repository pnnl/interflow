import numpy as np
import pandas as pd

from .reader import *
import flow.clean as cl
import flow.configure as co


def calc_electricity_public_water_supply(total=False, gw_pump_kwh_per_mg=920, gw_pws_fraction=.5,
                                         sw_pump_kwh_per_mg=145, desalination_kWh_mg=13600,
                                         sw_treatment_kwh_per_mg=405, gw_treatment_kwh_per_mg=205,
                                         distribution_kwh_per_mg=1040):
    """calculate energy usage by the public water supply sector. Takes a dataframe of public water supply withdrawals
    fand calculates total energy use for surface water pumping, groundwater pumping, surface water treatment,
    groundwater treatment, and distribution. If individual flow values for groundwater and surface water to public
    water supply are not provided, the total water flows to public water supply are used and multiplied by the
    assumed percentage of each (default is set to 50%). This function REQUIRES that at minimum, the total water
     flows to public water supply are available. Returns a DataFrame of energy use for each category in billion
    btu per year.

    :return:                DataFrame of energy use in public water supply

    """
    # load data
    df = co.configure_data()
    # electricity in groundwater pumping for public water supply

    # calculate total groundwater to public water supply
    if ('fresh_groundwater_pws_mgd' in df.columns) and ('saline_groundwater_pws_mgd' in df.columns):
        total_pws_groundwater = df['fresh_groundwater_pws_mgd'] + df['saline_groundwater_pws_mgd']
    elif ('fresh_groundwater_pws_mgd' in df.columns) and ('saline_groundwater_pws_mgd' not in df.columns):
        total_pws_groundwater = df['fresh_groundwater_pws_mgd']
    elif ('fresh_groundwater_pws_mgd' not in df.columns) and ('saline_groundwater_pws_mgd' in df.columns):
        total_pws_groundwater = df['saline_groundwater_pws_mgd']
    else:
        total_pws_groundwater = (gw_pws_fraction * df['total_pws_mgd'])

    # calculate total surface water to public water supply
    if ('fresh_surface_water_pws_mgd' in df.columns) and ('saline_surface_water_pws_mgd' in df.columns):
        total_pws_surface_water = df['fresh_surface_water_pws_mgd'] + df['saline_surface_water_pws_mgd']
    elif ('fresh_surface_water_pws_mgd' in df.columns) and ('saline_surface_water_pws_mgd' not in df.columns):
        total_pws_surface_water = df['fresh_surface_water_pws_mgd']
    elif ('fresh_surface_water_pws_mgd' not in df.columns) and ('saline_surface_water_pws_mgd' in df.columns):
        total_pws_surface_water = df['saline_surface_water_pws_mgd']
    else:
        total_pws_surface_water = ((1 - gw_pws_fraction) * df['total_pws_mgd'])

    # calculate total saline water in public water supply
    if ('saline_surface_water_pws_mgd' in df.columns) and ('saline_groundwater_pws_mgd' in df.columns):
        total_pws_saline = df['saline_surface_water_pws_mgd'] + df['saline_groundwater_pws_mgd']
    elif ('saline_surface_water_pws_mgd' in df.columns) and ('saline_groundwater_pws_mgd' not in df.columns):
        total_pws_saline = df['saline_surface_water_pws_mgd']
    elif ('saline_surface_water_pws_mgd' not in df.columns) and ('saline_groundwater_pws_mgd' in df.columns):
        total_pws_saline = df['saline_groundwater_pws_mgd']
    else:
        total_pws_saline = 0

    # calculate total public water supply withdrawals
    df['total_pws_mgd'] = total_pws_groundwater + total_pws_surface_water

    # calculate total electricity in groundwater pumping for public water supply
    if 'gw_pump_bbtu_per_mg' in df.columns:
        df['electricity_pws_gw_pumping_bbtu'] = total_pws_groundwater*df['gw_pump_bbtu_per_mg']
    else:
        df['electricity_pws_gw_pumping_bbtu'] = total_pws_groundwater * convert_kwh_bbtu(gw_pump_kwh_per_mg)

    # calculate total electricity in surface water pumping for public water supply
    if 'sw_pump_bbtu_per_mg' in df.columns:
        df['electricity_pws_sw_pumping_bbtu'] = total_pws_surface_water*df['sw_pump_bbtu_per_mg']
    else:
        df['electricity_pws_sw_pumping_bbtu'] = total_pws_surface_water * convert_kwh_bbtu(sw_pump_kwh_per_mg)

    # calculate total electricity in desalination for pws
    if 'pws_desalination_bbtu_per_mg' in df.columns:
        df['electricity_pws_desalination_bbtu'] = total_pws_saline * df['pws_desalination_bbtu_per_mg']
    else:
        df['electricity_pws_desalination_bbtu'] = total_pws_saline * convert_kwh_bbtu(desalination_kWh_mg)

    # calculate electricity in surface water treatment for public water supply
    if 'pws_surface_water_treatment_bbtu_per_mg' in df.columns:
        df['electricity_pws_surface_treatment_bbtu'] = total_pws_surface_water \
                                                       * df['pws_surface_water_treatment_bbtu_per_mg']
    else:
        df['electricity_pws_surface_treatment_bbtu'] = total_pws_surface_water \
                                                       * convert_kwh_bbtu(sw_treatment_kwh_per_mg)

    # calculate electricity in groundwater treatment for public water supply
    if 'pws_groundwater_treatment_bbtu_per_mg' in df.columns:
        df['electricity_pws_surface_treatment_bbtu'] = total_pws_groundwater \
                                                       * df['pws_groundwater_treatment_bbtu_per_mg']
    else:
        df['electricity_pws_surface_treatment_bbtu'] = total_pws_groundwater \
                                                       * convert_kwh_bbtu(gw_treatment_kwh_per_mg)

    # calculate electricity in distribution of public water supply
    if 'pws_distribution_bbtu_per_mg' in df.columns:
        df['electricity_pws_distribution_bbtu'] = df['total_pws_mgd'] * df['pws_distribution_bbtu_per_mg']
    else:
        df['electricity_pws_distribution_bbtu'] = df['total_pws_mgd'] * convert_kwh_bbtu(distribution_kwh_per_mg)

    # calculate ratio of water
    if ('interbasin_bbtu' in df.columns) \
            and ('fresh_groundwater_crop_irrigation_mgd' or 'fresh_surface_water_crop_irrigation_mgd')\
            or ('total_irrigation_mgd') :
        Ag_SW_ratio = np.where(df['AG-WSWFr'] != 0, df['AG-WSWFr'] / (df['PS-WSWFr'] + df['AG-WSWFr']), 0)

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
