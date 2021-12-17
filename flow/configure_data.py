import numpy as np
import pandas as pd

from .calculate import *
from .reader import *


def prep_data(data_path=None) -> pd.DataFrame:
    """ Produces a dataframe containing all values in prep module to use in calculations.

    :return:                DataFrame of a number of water values for 2015 at the county level

    """

    # read in data
    if data_path is None:
        df = prep_water_use_2015(all_variables=True)
        df_2015_consumption_fractions = prep_consumption_fraction()
        df_hydro_water_intensity = prep_hydroelectric_water_intensity()
        df_pws_fraction = prep_public_water_supply_fraction()
        df_conveyance_loss_fraction = prep_conveyance_loss_fraction()
        df_wastewater = prep_wastewater_data()
        df_electricity = prep_electricity_generation()
        df_irrigation_fuel = prep_irrigation_fuel_data()
        df_pumping_intensity = prep_pumping_intensity_data()
        df_ibt = prep_interbasin_transfer_data()
        df_electricity_demand = prep_electricity_demand_data()
        df_fuel_demand = prep_fuel_demand_data()
        df_petroleum_production = prep_county_petroleum_production_data()
        df_natgas_production = prep_county_natgas_production_data()
        df_coal_production = prep_county_coal_production_data()
        df_ethanol_production = prep_county_ethanol_production_data()
        df_biomass_water = prep_county_water_corn_biomass_data()

        df_list = [df_2015_consumption_fractions,
                   df_hydro_water_intensity,
                   df_pws_fraction,
                   df_conveyance_loss_fraction,
                   df_wastewater,
                   df_electricity,
                   df_irrigation_fuel,
                   df_pumping_intensity,
                   df_ibt,
                   df_electricity_demand,
                   df_fuel_demand,
                   df_petroleum_production,
                   df_natgas_production,
                   df_coal_production,
                   df_ethanol_production,
                   df_biomass_water]

        for df_item in df_list:
            df = pd.merge(df, df_item, how='left', on= ['FIPS','State','County'])

    else:
        df = pd.read(data_path)




    return df
