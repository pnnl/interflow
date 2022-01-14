import numpy as np
import pandas as pd

from .calculate import *
from .reader import *
from .clean import *

#TODO figure out if it makes more sense for it to load paths or have another function that loads the data
#TODO could have the other function read in everything and store it in a dataframe, which is called here.

def configure_data(data_path=None, region_data=None, region=[], use_water_use_data=True, water_use_data_path=None,
                   use_water_consumption_data=True, water_consumption_data_path=None,
                   use_hydro_water_intensity=True, hydro_water_intensity_path=None,
                   use_pws_fraction_data=True, pws_fraction_data_path=None,
                   use_pws_export_data=True, pws_export_data_path=None,
                   use_conveyance_loss_fraction=True, conveyance_loss_fraction_data_path=None,
                   use_wastewater=True, wastewater_data_path=None,
                   use_electricity=True, electricity_data_path=None,
                   use_irrigation_fuel=True, irrigation_fuel_data_path=None,
                   use_pumping_intensity=True, pumping_intensity_data_path=None,
                   use_ibt=True, ibt_data_path=None,
                   use_ibt_pws_pct_data=True, ibt_pws_pct_data_path=None,
                   use_electricity_demand=True, electricity_demand_data_path=None,
                   use_fuel_demand=True, fuel_demand_data_path=None,
                   use_petroleum_production=False, petroleum_production_data_path=None,
                   use_natgas_production=True, natgas_production_data_path=None,
                   use_coal_production=True, coal_production_data_path=None,
                   use_ethanol_production=True, ethanol_production_data_path=None,
                   use_biomass_water=True, biomass_water_data_path=None) -> pd.DataFrame:

    """ configures baseline dataset for calculations. Users can either run with default arguments which loads
    the baseline data for 2015 united states values or use a subset of the prepared 2015 US values and substitute
    data for other files (for example, swap out different estimates for electricity generation but use all other
    data provided by the tool). Can also be used to build an aggregate baseline dataframe for any region so long as
    data is provided and region name is specified.


    :return:                DataFrame of ______

    """
    if data_path:
        df = pd.read_csv(data_path)

    else:
        # establish region data
        if region_data:
            df = pd.read(region_data)
        else:
            df = cl.prep_water_use_2015(variables=['FIPS', 'State', 'County'])

        # water use data
        if (use_water_use_data == True) and (water_use_data_path is None):
            df_water_use = cl.prep_water_use_2015(all_variables=True)
            df = pd.merge(df, df_water_use, how='left', on=['FIPS', 'State', 'County'])
        elif (use_water_use_data == False) & (water_use_data_path is None):
            pass
        else:
            df_water_use = pd.read(water_use_data_path)
            df = pd.merge(df, df_water_use, how='left', on=region)

        # water consumption data
        if (use_water_consumption_data == True) and (water_consumption_data_path is None):
            df_consumption_fractions = cl.prep_consumption_fraction()
            df = pd.merge(df, df_consumption_fractions, how='left', on=['FIPS', 'State', 'County'])
        elif (use_water_consumption_data == False) & (water_consumption_data_path is None):
            pass
        else:
            df_consumption_fractions = pd.read_csv(water_consumption_data_path)
            df = pd.merge(df, df_consumption_fractions, how='left', on=region)

        # use_hydro_water_intensity data
        if (use_hydro_water_intensity == True) & (hydro_water_intensity_path is None):
            df_hydro_intensity = cl.prep_hydroelectric_water_intensity()
            df = pd.merge(df, df_hydro_intensity, how='left', on=['FIPS', 'State', 'County'])
        elif (use_hydro_water_intensity == False) & (hydro_water_intensity_path is None):
            pass
        else:
            df_hydro_intensity = pd.read_csv(hydro_water_intensity_path)
            df = pd.merge(df, df_hydro_intensity, how='left', on=region)

        # use_pws_fraction_data data
        if (use_pws_fraction_data == True) & (pws_fraction_data_path is None):
            df_pws = cl.prep_public_water_supply_fraction()
            df = pd.merge(df, df_pws, how='left', on=['FIPS', 'State', 'County'])
        elif (use_pws_fraction_data == False) & (pws_fraction_data_path is None):
            pass
        else:
            df_pws = pd.read_csv(pws_fraction_data_path)
            df = pd.merge(df, df_pws, how='left', on=region)

        # use_pws_export_data data
        if (use_pws_export_data == True) & (pws_export_data_path is None):
            df_pws_export = cl.calc_pws_discharge()
            df = pd.merge(df, df_pws_export, how='left', on=['FIPS', 'State', 'County'])
        elif (use_pws_export_data == False) & (pws_export_data_path is None):
            pass
        else:
            df_pws_export = pd.read_csv(pws_export_data_path)
            df = pd.merge(df, df_pws_export, how='left', on=region)

        # use_conveyance_loss_fraction data
        if (use_conveyance_loss_fraction == True) & (conveyance_loss_fraction_data_path is None):
            df_conveyance_loss = cl.prep_conveyance_loss_fraction()
            df = pd.merge(df, df_conveyance_loss, how='left', on=['FIPS', 'State', 'County'])
        elif (use_conveyance_loss_fraction == False) & (conveyance_loss_fraction_data_path is None):
            pass
        else:
            df_conveyance_loss = pd.read_csv(conveyance_loss_fraction_data_path)
            df = pd.merge(df, df_conveyance_loss, how='left', on=region)

        # use_wastewater data
        if (use_wastewater == True) & (wastewater_data_path is None):
            df_ww = cl.prep_wastewater_data()
            df = pd.merge(df, df_ww, how='left', on=['FIPS', 'State', 'County'])
        elif (use_wastewater == False) & (wastewater_data_path is None):
            pass
        else:
            df_ww = pd.read_csv(wastewater_data_path)
            df = pd.merge(df, df_ww, how='left', on=region)

        # use_electricity data
        if (use_electricity == True) & (electricity_data_path is None):
            df_electricity = cl.prep_electricity_generation()
            df = pd.merge(df, df_electricity, how='left', on=['FIPS', 'State', 'County'])
        elif (use_electricity == False) & (electricity_data_path is None):
            pass
        else:
            df_electricity = pd.read_csv(electricity_data_path)
            df = pd.merge(df, df_electricity, how='left', on=region)

        # use_irrigation_fuel data
        if (use_irrigation_fuel == True) & (irrigation_fuel_data_path is None):
            df_irrigation_fuel = cl.prep_irrigation_fuel_data()
            df = pd.merge(df, df_irrigation_fuel, how='left', on=['FIPS', 'State', 'County'])
        elif (use_irrigation_fuel == False) & (irrigation_fuel_data_path is None):
            pass
        else:
            df_irrigation_fuel = pd.read_csv(irrigation_fuel_data_path)
            df = pd.merge(df, df_irrigation_fuel, how='left', on=region)

        # use_pumping_intensity data
        if (use_pumping_intensity == True) & (pumping_intensity_data_path is None):
            df_pump_intensity = cl.prep_pumping_intensity_data()
            df = pd.merge(df, df_pump_intensity, how='left', on=['FIPS', 'State', 'County'])
        elif (use_pumping_intensity == False) & (pumping_intensity_data_path is None):
            pass
        else:
            df_pump_intensity = pd.read_csv(pumping_intensity_data_path)
            df = pd.merge(df, df_pump_intensity, how='left', on=region)

        # use_ibt data
        if (use_ibt == True) & (ibt_data_path is None):
            df_ibt = cl.prep_interbasin_transfer_data()
            df = pd.merge(df, df_ibt, how='left', on=['FIPS', 'State', 'County'])
        elif (use_ibt == False) & (ibt_data_path is None):
            pass
        else:
            df_ibt = pd.read_csv(ibt_data_path)
            df = pd.merge(df, df_ibt, how='left', on=region)

        # use_ibt_pws_pct_data
        if (use_ibt_pws_pct_data == True) & (ibt_pws_pct_data_path is None):
            df_ibt_pws_pct = cl.prep_irrigation_pws_ratio()
            df = pd.merge(df, df_ibt_pws_pct, how='left', on=['FIPS', 'State', 'County'])
        elif (use_ibt_pws_pct_data == False) & (ibt_pws_pct_data_path is None):
            pass
        else:
            df_ibt_pws_pct = pd.read_csv(ibt_pws_pct_data_path)
            df = pd.merge(df, df_ibt_pws_pct, how='left', on=region)

        # use_electricity_demand data
        if (use_electricity_demand == True) & (electricity_demand_data_path is None):
            df_elec_demand = cl.prep_electricity_demand_data()
            df = pd.merge(df, df_elec_demand, how='left', on=['FIPS', 'State', 'County'])
        elif (use_electricity_demand == False) & (electricity_demand_data_path is None):
            pass
        else:
            df_elec_demand = pd.read_csv(electricity_demand_data_path)
            df = pd.merge(df, df_elec_demand, how='left', on=region)

        # use_fuel_demand data
        if (use_fuel_demand == True) & (fuel_demand_data_path is None):
            df_fuel_demand = cl.prep_fuel_demand_data()
            df = pd.merge(df, df_fuel_demand, how='left', on=['FIPS', 'State', 'County'])
        elif (use_fuel_demand == False) & (fuel_demand_data_path is None):
            pass
        else:
            df_fuel_demand = pd.read_csv(fuel_demand_data_path)
            df = pd.merge(df, df_fuel_demand, how='left', on=region)

        # use_petroleum_production data
        if (use_petroleum_production == True) & (petroleum_production_data_path is None):
            df_pet_prod = cl.prep_county_petroleum_production_data()
            df = pd.merge(df, df_pet_prod, how='left', on=['FIPS', 'State', 'County'])
        elif (use_petroleum_production == False) & (petroleum_production_data_path is None):
            pass
        else:
            df_pet_prod = pd.read_csv(petroleum_production_data_path)
            df = pd.merge(df, df_pet_prod, how='left', on=region)

        # use_natgas_production data
        if (use_natgas_production == True) & (natgas_production_data_path is None):
            df_ng_prod = cl.prep_county_natgas_production_data()
            df = pd.merge(df, df_ng_prod, how='left', on=['FIPS', 'State', 'County'])
        elif (use_natgas_production == False) & (natgas_production_data_path is None):
            pass
        else:
            df_ng_prod = pd.read_csv(natgas_production_data_path)
            df = pd.merge(df, df_ng_prod, how='left', on=region)

        # use_coal_production data
        if (use_coal_production == True) & (coal_production_data_path is None):
            df_coal_prod = cl.prep_county_coal_production_data()
            df = pd.merge(df, df_coal_prod, how='left', on=['FIPS', 'State', 'County'])
        elif (use_coal_production == False) & (coal_production_data_path is None):
            pass
        else:
            df_coal_prod = pd.read_csv(coal_production_data_path)
            df = pd.merge(df, df_coal_prod, how='left', on=region)

        # use_ethanol_production data
        if (use_ethanol_production == True) & (ethanol_production_data_path is None):
            df_biomass_prod = cl.prep_county_ethanol_production_data()
            df = pd.merge(df, df_biomass_prod, how='left', on=['FIPS', 'State', 'County'])
        elif (use_ethanol_production == False) & (ethanol_production_data_path is None):
            pass
        else:
            df_biomass_prod = pd.read_csv(ethanol_production_data_path)
            df = pd.merge(df, df_biomass_prod, how='left', on=region)

        # use_biomass_water data
        if (use_biomass_water == True) & (biomass_water_data_path is None):
            df_biomass_water = cl.prep_county_water_corn_biomass_data()
            df = pd.merge(df, df_biomass_water, how='left', on=['FIPS', 'State', 'County'])
        elif (use_biomass_water == False) & (biomass_water_data_path is None):
            pass
        else:
            df_biomass_water = pd.read_csv(biomass_water_data_path)
            df = pd.merge(df, df_biomass_water, how='left', on=region)

    return df
