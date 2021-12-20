import numpy as np
import pandas as pd

from .reader import *
import flow.clean as cl
import flow.configure as co


def calc_electricity(data: pd.DataFrame, generation_efficiency=.33):
    """calculates total electricity generation and rejected energy (losses) by region.

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe.
        :type regions:                      int


        :return:                            DataFrame of energy use in public water supply

        """

    # load data
    df = data

    # convert generation to bbtu

biomass_fuel_bbtu
coal_fuel_bbtu
geothermal_fuel_bbtu
hydro_fuel_bbtu
natgas_fuel_bbtu
nuclear_fuel_bbtu
oil_fuel_bbtu
other_fuel_bbtu
solar_fuel_bbtu
wind_fuel_bbtu
biomass_gen_mwh
coal_gen_mwh
geothermal_gen_mwh
hydro_gen_mwh
natgas_gen_mwh
nuclear_gen_mwh
oil_gen_mwh
other_gen_mwh
solar_gen_mwh
wind_gen_mwh

def calc_electricity_public_water_supply(data: pd.DataFrame, regions=3, total=False, gw_pump_kwh_per_mg=920,
                                         gw_pws_fraction=.5, sw_pump_kwh_per_mg=145, desalination_kwh_mg=13600,
                                         sw_treatment_kwh_per_mg=405, gw_treatment_kwh_per_mg=205,
                                         distribution_kwh_per_mg=1040, ibt_fraction=.5, gw_pump_efficiency=.65,
                                         sw_pump_efficiency=.65, desalination_efficiency=.65,
                                         sw_treatment_efficiency=.65,
                                         gw_treatment_efficiency=.65, distribution_efficiency=.65,
                                         ibt_efficiency=.65):
    """calculate energy usage by the public water supply sector. Takes a dataframe of public water supply withdrawals
    fand calculates total energy use for surface water pumping, groundwater pumping, surface water treatment,
    groundwater treatment, and distribution. If individual flow values for groundwater and surface water to public
    water supply are not provided, the total water flows to public water supply are used and multiplied by the
    assumed percentage of each (default is set to 50%). This function REQUIRES that at minimum, the total water
     flows to public water supply are available. Returns a DataFrame of energy use for each category in billion
    btu per year.

    :param regions:                     gives the number of columns in the dataset that should be treated as region
                                        identifiers (e.g. "Country", "State"). Reads from the first column in the
                                        dataframe.
    :type regions:                      int


    :return:                            DataFrame of energy use in public water supply

    """

    # load data
    df = data

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
        df['electricity_pws_gw_pumping_bbtu'] = total_pws_groundwater * df['gw_pump_bbtu_per_mg']
    else:
        df['electricity_pws_gw_pumping_bbtu'] = total_pws_groundwater * convert_kwh_bbtu(gw_pump_kwh_per_mg)

    # calculate total electricity in surface water pumping for public water supply
    if 'sw_pump_bbtu_per_mg' in df.columns:
        df['electricity_pws_sw_pumping_bbtu'] = total_pws_surface_water * df['sw_pump_bbtu_per_mg']
    else:
        df['electricity_pws_sw_pumping_bbtu'] = total_pws_surface_water * convert_kwh_bbtu(sw_pump_kwh_per_mg)

    # calculate total electricity in desalination for pws
    if 'pws_desalination_bbtu_per_mg' in df.columns:
        df['electricity_pws_desalination_bbtu'] = total_pws_saline * df['pws_desalination_bbtu_per_mg']
    else:
        df['electricity_pws_desalination_bbtu'] = total_pws_saline * convert_kwh_bbtu(desalination_kwh_mg)

    # calculate electricity in surface water treatment for public water supply
    if 'pws_surface_water_treatment_bbtu_per_mg' in df.columns:
        df['electricity_pws_surface_treatment_bbtu'] = total_pws_surface_water \
                                                       * df['pws_surface_water_treatment_bbtu_per_mg']
    else:
        df['electricity_pws_surface_treatment_bbtu'] = total_pws_surface_water \
                                                       * convert_kwh_bbtu(sw_treatment_kwh_per_mg)

    # calculate electricity in groundwater treatment for public water supply
    if 'pws_groundwater_treatment_bbtu_per_mg' in df.columns:
        df['electricity_pws_groundwater_treatment_bbtu'] = total_pws_groundwater \
                                                           * df['pws_groundwater_treatment_bbtu_per_mg']
    else:
        df['electricity_pws_groundwater_treatment_bbtu'] = total_pws_groundwater \
                                                           * convert_kwh_bbtu(gw_treatment_kwh_per_mg)

    # calculate electricity in distribution of public water supply
    if 'pws_distribution_bbtu_per_mg' in df.columns:
        df['electricity_pws_distribution_bbtu'] = df['total_pws_mgd'] * df['pws_distribution_bbtu_per_mg']
    else:
        df['electricity_pws_distribution_bbtu'] = df['total_pws_mgd'] * convert_kwh_bbtu(distribution_kwh_per_mg)

    # calculate interbasin transfer energy to public water supply
    if 'interbasin_bbtu' in df.columns:
        if 'pws_ibt_pct' in df.columns:
            df['electricity_pws_ibt_bbtu'] = df['interbasin_bbtu'] * df['pws_ibt_pct']
        else:
            df['electricity_pws_ibt_bbtu'] = df['interbasin_bbtu'] * ibt_fraction
    else:
        df['electricity_pws_ibt_bbtu'] = 0

    # calculate total energy in public water supply
    df['total_electricity_pws_bbtu'] = df['electricity_pws_gw_pumping_bbtu'] \
                                       + df['electricity_pws_sw_pumping_bbtu'] \
                                       + df['electricity_pws_desalination_bbtu'] \
                                       + df['electricity_pws_surface_treatment_bbtu'] \
                                       + df['electricity_pws_groundwater_treatment_bbtu'] \
                                       + df['electricity_pws_distribution_bbtu'] \
                                       + df['electricity_pws_ibt_bbtu']

    # calculate rejected energy in public water supply
    df['pws_gw_pumping_rejected_energy_bbtu'] = gw_pump_efficiency \
                                                * df['electricity_pws_gw_pumping_bbtu']
    df['pws_sw_pumping_rejected_energy_bbtu'] = sw_treatment_efficiency \
                                                * df['electricity_pws_sw_pumping_bbtu']
    df['pws_desalination_rejected_energy_bbtu'] = desalination_efficiency \
                                                  * df['electricity_pws_desalination_bbtu']
    df['pws_surface_treatment_rejected_energy_bbtu'] = sw_treatment_efficiency \
                                                       * df['electricity_pws_surface_treatment_bbtu']
    df['pws_groundwater_treatment_rejected_energy_bbtu'] = gw_treatment_efficiency \
                                                           * df['electricity_pws_groundwater_treatment_bbtu']
    df['pws_distribution_rejected_energy_bbtu'] = distribution_efficiency \
                                                  * df['electricity_pws_distribution_bbtu']
    df['pws_ibt_rejected_energy_bbtu'] = ibt_efficiency \
                                         * df['electricity_pws_ibt_bbtu']

    # total rejected energy
    df['total_pws_rejected_energy_bbtu'] = df['pws_gw_pumping_rejected_energy_bbtu'] \
                                       + df['pws_sw_pumping_rejected_energy_bbtu'] \
                                       + df['pws_desalination_rejected_energy_bbtu'] \
                                       + df['pws_surface_treatment_rejected_energy_bbtu'] \
                                       + df['pws_groundwater_treatment_rejected_energy_bbtu'] \
                                       + df['pws_distribution_rejected_energy_bbtu'] \
                                       + df['pws_ibt_rejected_energy_bbtu']

    # calculate rejected energy in public water supply
    df['pws_gw_pumping_energy_services_bbtu'] = (1 - gw_pump_efficiency) \
                                                * df['electricity_pws_gw_pumping_bbtu']
    df['pws_sw_pumping_energy_services_bbtu'] = (1 - sw_treatment_efficiency) \
                                                * df['electricity_pws_sw_pumping_bbtu']
    df['pws_desalination_energy_services_bbtu'] = (1 - desalination_efficiency) \
                                                  * df['electricity_pws_desalination_bbtu']
    df['pws_surface_treatment_energy_services_bbtu'] = (1 - sw_treatment_efficiency) \
                                                       * df['electricity_pws_surface_treatment_bbtu']
    df['pws_groundwater_treatment_energy_services_bbtu'] = (1 - gw_treatment_efficiency) \
                                                           * df['electricity_pws_groundwater_treatment_bbtu']
    df['pws_distribution_energy_services_bbtu'] = (1 - distribution_efficiency) \
                                                  * df['electricity_pws_distribution_bbtu']
    df['pws_ibt_energy_services_bbtu'] = (1 - ibt_efficiency) \
                                         * df['electricity_pws_ibt_bbtu']

    # total energy services
    df['total_pws_energy_services_bbtu'] = df['pws_gw_pumping_energy_services_bbtu'] \
                                       + df['pws_sw_pumping_energy_services_bbtu'] \
                                       + df['pws_desalination_energy_services_bbtu'] \
                                       + df['pws_surface_treatment_energy_services_bbtu'] \
                                       + df['pws_groundwater_treatment_energy_services_bbtu'] \
                                       + df['pws_distribution_energy_services_bbtu'] \
                                       + df['pws_ibt_energy_services_bbtu']

    # if total is set to true, return total amounts for electricity use, energy services, and rejected energy
    if total:
        column_list = df.columns[:regions].tolist()
        column_list.append('total_electricity_pws_bbtu')
        column_list.append('total_pws_rejected_energy_bbtu')
        column_list.append('total_pws_energy_services_bbtu')
        df = df[column_list]
    else:
        column_list = df.columns[:regions].tolist()
        retain_list = df.columns[-24:].tolist()
        for item in retain_list:
            column_list.append(item)
        df = df[column_list]

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
