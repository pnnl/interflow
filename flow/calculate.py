import numpy as np
import pandas as pd

from .reader import *
import flow.clean as cl
import flow.configure as co


def calc_electricity_rejected_energy(data: pd.DataFrame, generation_types=None, regions=3,
                                     generation_efficiency=.30, total=False):
    """calculates rejected energy (losses) by region and generating type in billion btu. Rejected energy is calculated
    as the difference between total fuel use in electricity generation and total output of electricity generation. If
    electricity generation is not provided, function applies a specified efficiency (default is set to 0.30). If
    generation is provided but fuel quantity is not, then the inverse of the specified efficiency is applied.
    If no generation types are specified, the function uses a default list of generator types which includes 'biomass',
    'coal', 'geothermal', 'hydro', 'natgas', and 'nuclear'.

        :param data:                        DataFrame of input data containing electricity generation fuel and total
                                            electricity generation by type
        :type data:                         DataFrame

        :param generation_types:            a list of generation types to include (e.g. ['biomass','coal'])
        :type generation_types:             list

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param generation_efficiency:       assumed efficiency rate of electricity generation
        :type generation_efficiency:        float

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
        :type total:                        bool

        :return:                            DataFrame of rejected energy in billion btu from electricity generation

        """

    # load data
    df = data

    # establish list of generation types
    if generation_types is None:
        generation_type_list = ['biomass', 'coal', 'geothermal', 'hydro', 'natgas', 'nuclear',
                                'oil', 'other', 'solar', 'wind']
    else:
        generation_type_list = generation_types

    df['electricity_total_rejected_energy_bbtu'] = 0
    retain_list = []
    for type in generation_type_list:
        fuel_type = type + "_fuel_bbtu"
        gen_type = type + "_gen_bbtu"

        if (fuel_type in df.columns) and (gen_type in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] - df[gen_type]
            df['electricity_total_rejected_energy_bbtu'] = df['electricity_total_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
        elif (fuel_type in df.columns) and (gen_type not in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 - generation_efficiency)
            df['electricity_total_rejected_energy_bbtu'] = df['electricity_total_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
        elif (fuel_type not in df.columns) and (gen_type in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 / (1 - generation_efficiency))
            df['electricity_total_rejected_energy_bbtu'] = df['electricity_total_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')

        else:
            df[f'electricity_{type}_rejected_energy_bbtu'] = 0
            df['electricity_total_rejected_energy_bbtu'] = df['electricity_total_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']

    if total:
        column_list = df.columns[:regions].tolist()
        column_list.append('electricity_total_rejected_energy_bbtu')
        df = df[column_list]
    else:
        column_list = df.columns[:regions].tolist()
        for item in retain_list:
            column_list.append(item)
        column_list.append('electricity_total_rejected_energy_bbtu')
        df = df[column_list]

    return df


def calc_sectoral_use_energy_discharge(data: pd.DataFrame, sector_types=None, fuel_types=None, regions=3, total=False):
    """calculates rejected energy (losses) and energy services for each region for each sector type in billion btu.
    Rejected energy is calculated as energy delivered multiplied by the efficiency rating for a given sector.

        :param data:                        DataFrame of input data containing fuel demand data for each sector
        :type data:                         DataFrame

        :param sector_types:                a dictionary of sector types to include and their associated efficiency
                                            (e.g. {'residential':0.65, 'commercial':0.60}. If none provided, defaults
                                            are used.
        :type sector_types:                 dictionary

        :param fuel_types:                  a list of fuel types to include (e.g., electricity, coal, petroleum)
        :type fuel_types:                   list

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
                                            and total energy services by sector instead of by fuel type
        :type total:                        bool

        :return:                            DataFrame of rejected energy in billion btu from sectors

        """

    # load data
    df = data

    # establish dictionary of sector types as keys and efficiency as value.
    if sector_types is None:  # default key value pairs
        sector_type_dict = {'residential': 0.65, 'commercial': 0.65, 'industrial': 0.49,
                            'mining': 0.65, 'transportation': 0.21}
    else:
        sector_type_dict = sector_types

    #  establish list of fuel types to include
    if fuel_types is None:  # default fuel types
        fuel_type_list = ['electricity', 'coal', 'biomass', 'geothermal', 'natgas', 'petroleum', 'solar', 'wind']
    else:
        fuel_type_list = fuel_types

    # loop through each sector + fuel pair and calculate rejected energy and energy services if in dataset
    retain_list = []
    total_list = []
    for sector_type in sector_type_dict:
        df[f'{sector_type}_total_rejected_energy_bbtu'] = 0
        df[f'{sector_type}_total_energy_services_bbtu'] = 0

        for fuel_type in fuel_type_list:
            fuel_demand_type = fuel_type + "_" + sector_type + "_bbtu"
            if fuel_demand_type in df.columns:
                df[f'{sector_type}_{fuel_type}_rejected_energy_bbtu'] = df[fuel_demand_type] \
                                                                        * (1 - sector_type_dict[sector_type])

                df[f'{sector_type}_{fuel_type}_energy_services_bbtu'] = df[fuel_demand_type] \
                                                                        * (sector_type_dict[sector_type])

                retain_list.append(f'{sector_type}_{fuel_type}_rejected_energy_bbtu')
                retain_list.append(f'{sector_type}_{fuel_type}_energy_services_bbtu')

                df[f'{sector_type}_total_rejected_energy_bbtu'] = df[f'{sector_type}_total_rejected_energy_bbtu'] \
                                                                  + df[
                                                                      f'{sector_type}_{fuel_type}_rejected_energy_bbtu']
            else:
                pass

        retain_list.append(f'{sector_type}_total_rejected_energy_bbtu')
        total_list.append(f'{sector_type}_total_rejected_energy_bbtu')

    # establish list of region columns to include in output
    column_list = df.columns[:regions].tolist()

    # if total is True, only return total rejected energy and energy services by sector
    if total:
        for item in total_list:
            column_list.append(item)
        df = df[column_list]
    else:
        for item in retain_list:
            column_list.append(item)
        df = df[column_list]

    return df


def calc_energy_wastewater(data: pd.DataFrame, treatment_types=None, fuel_types=None, regions=3, total=False):
    #TODO expects a column with fuel percent, does not currently allow for getting rejected energy if total energy is
    # TODO already provided by region
    """calculates rejected energy (losses) and energy services for each region for each sector type in billion btu.
    Rejected energy is calculated as energy delivered multiplied by the efficiency rating for a given sector.

        :param data:                        DataFrame of input data containing wastewater flow data in mgd
        :type data:                         DataFrame

        :param treatment_types:             a dictionary of wastewater treatment types to include and their associated
                                            energy intensity in kWh/mg (e.g. {'advanced':2690}. If none provided,
                                            defaults are used.
        :type treatment_types:              dictionary

        :param fuel_types:                  a dictionary of fuel types to include (e.g., electricity, coal, petroleum)
                                            and their associated efficiency
        :type fuel_types:                   dictionary

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
                                            and total energy services by sector instead of by fuel type
        :type total:                        bool

        :return:                            DataFrame of rejected energy in billion btu from sectors

        """

    # load data
    df = data

    # establish dictionary of treatment types as keys and energy intensities as values (kWh/MG).
    if treatment_types is None:  # default key value pairs
        treatment_type_dict = {'advanced': 2690, 'secondary': 2080, 'primary': 750}
    else:
        treatment_type_dict = treatment_types

    # if no fuel type dictionary is provided, default is electricity at 65% efficiency
    if fuel_types is None:  # default key value pairs
        fuel_type_dict = {'electricity': .65}
    else:
        fuel_type_dict = fuel_types

    retain_list = []
    total_list = []
    df['electricity_wastewater_total_bbtu'] = 0
    df['wastewater_rejected_energy_total_bbtu'] = 0
    df['wastewater_energy_services_total_bbtu'] = 0

    # loops through each treatment type and fuel source to calculate electricity, rejected energy, and energy services
    for treatment_type in treatment_type_dict:
        treatment_flow_type = "wastewater_" + treatment_type + "_" + "treatment_mgd"
        for fuel_type in fuel_type_dict:
            fuel_pct = f"wastewater_{fuel_type}" + "_" + "fuel_pct"
            fuel_efficiency = f"wastewater_{fuel_type}" + "_" + "efficiency_fraction"
            if treatment_flow_type in df.columns:
                df[f'{fuel_type}_wastewater_{treatment_type}_bbtu'] = df[treatment_flow_type] \
                                                                      * convert_kwh_bbtu(treatment_type_dict[treatment_type]) \
                                                                      * df[fuel_pct]

                df[f'wastewater_{treatment_type}_rejected_energy_bbtu'] = df[f'electricity_wastewater_{treatment_type}_bbtu'] \
                                                                          * (1 - fuel_type_dict[fuel_type])

                df[f'wastewater_{treatment_type}_energy_services_bbtu'] = df[f'electricity_wastewater_{treatment_type}_bbtu'] \
                                                                          * (fuel_type_dict[fuel_type])

                # add to list of retained variables
                retain_list.append(f'electricity_wastewater_{treatment_type}_bbtu')
                retain_list.append(f'wastewater_{treatment_type}_rejected_energy_bbtu')
                retain_list.append(f'wastewater_{treatment_type}_energy_services_bbtu')

                # add on to totals
                df['electricity_wastewater_total_bbtu'] = df['electricity_wastewater_total_bbtu'] \
                                                          + df[f'electricity_wastewater_{treatment_type}_bbtu']
                df['wastewater_rejected_energy_total_bbtu'] = df['wastewater_rejected_energy_total_bbtu'] \
                                                              + df[f'wastewater_{treatment_type}_rejected_energy_bbtu']
                df['wastewater_energy_services_total_bbtu'] = df['wastewater_energy_services_total_bbtu'] \
                                                              + df[f'wastewater_{treatment_type}_energy_services_bbtu']
            else:
                pass

    # add totals to retained lists of variables
    retain_list.append('electricity_wastewater_total_bbtu')
    retain_list.append('wastewater_rejected_energy_total_bbtu')
    retain_list.append('wastewater_energy_services_total_bbtu')
    total_list.append('electricity_wastewater_total_bbtu')
    total_list.append('wastewater_rejected_energy_total_bbtu')
    total_list.append('wastewater_energy_services_total_bbtu')

    # establish list of region columns to include in output
    column_list = df.columns[:regions].tolist()

    # if total is True, only return total energy to wastewater, rejected energy and energy services
    if total:
        for item in total_list:
            column_list.append(item)
        df = df[column_list]
    else:
        for item in retain_list:
            column_list.append(item)
        df = df[column_list]

    return df

def calc_energy_agriculture(data: pd.DataFrame, pumping_types=None, delivery_types=None, fuel_types=None,
                            regions=3, total=False):
    """calculates rejected energy (losses) and energy services for each region for each sector type in billion btu.
    Rejected energy is calculated as energy delivered multiplied by the efficiency rating for a given sector.

        :param data:                        DataFrame of input data containing wastewater flow data in mgd
        :type data:                         DataFrame

        :param pumping_types:            a list of water pumping types to include and their associated
                                            energy intensity in kWh/mg (e.g. {'advanced':2690}. If none provided,
                                            defaults are used.
        :type pumping_types:            list

        :param fuel_types:                  a dictionary of fuel types to include (e.g., electricity, coal, petroleum)
                                            and their associated efficiency
        :type fuel_types:                   dictionary

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
                                            and total energy services by sector instead of by fuel type
        :type total:                        bool

        :return:                            DataFrame of rejected energy in billion btu from sectors

        """

    # load data
    df = data

    # establish list of pumping types for irrigation
    if pumping_types is None:  # default list
        pumping_type_list = ['groundwater', 'surface_water', 'wastewater']
    else:
        pumping_type_list = pumping_types

    # establish list of pumping types for irrigation
    if water_types is None:  # default list
        water_type_list = ['fresh', 'saline']
    else:
        water_type_list = water_types

    # establish list of agriculture water delivery types
    if agriculture_types is None:  # default list
        agriculture_type_list = ['crop_irrigation', 'golf_irrigation', 'livestock', 'aquaculture']
    else:
        agriculture_type_list = delivery_types

    # establish dictionary of fuel types for agriculture applications and efficiency ratings
    if fuel_types is None:  # default key value pairs
        fuel_type_dict = {"electricity": 65, "natural_gas": .65, "oil": .65}
    else:
        fuel_type_dict = fuel_types

    if fuel_percents is None:
        fuel_percent_dict = {"electricity": .6, "natural_gas": .01, "oil": .39}
    else:
        fuel_percent_dict = fuel_percents

    for water_type in water_types_list:
        for pumping_type in pumping_type_list:
            for agriculture_type in agriculture_type_list:
                pumping_flow_type = water_type + "_" + pumping_type + "_" + agriculture_type + "_mgd"
                for fuel_type in fuel_type_dict:
                    fuel_type_pct = fuel_type + "_"
                    if pumping_flow_type in df.columns:
                        df[f'{fuel_type}_{water_type}_{pumping_type}']





    retain_list = []
    total_list = []
    df['electricity_agriculture_total_bbtu'] = 0
    df['agriculture_rejected_energy_total_bbtu'] = 0
    df['agriculture_energy_services_total_bbtu'] = 0

    # loops through each treatment type and fuel source to calculate electricity, rejected energy, and energy services
    for treatment_type in treatment_type_dict:
        treatment_flow_type = "wastewater_" + treatment_type + "_" + "treatment_mgd"
        for fuel_type in fuel_type_dict:
            fuel_pct = f"wastewater_{fuel_type}" + "_" + "fuel_pct"
            fuel_efficiency = f"wastewater_{fuel_type}" + "_" + "efficiency_fraction"
            if treatment_flow_type in df.columns:
                df[f'{fuel_type}_wastewater_{treatment_type}_bbtu'] = df[treatment_flow_type] \
                                                                      * convert_kwh_bbtu(treatment_type_dict[treatment_type]) \
                                                                      * df[fuel_pct]

                df[f'wastewater_{treatment_type}_rejected_energy_bbtu'] = df[f'electricity_wastewater_{treatment_type}_bbtu'] \
                                                                          * (1 - fuel_type_dict[fuel_type])

                df[f'wastewater_{treatment_type}_energy_services_bbtu'] = df[f'electricity_wastewater_{treatment_type}_bbtu'] \
                                                                          * (fuel_type_dict[fuel_type])

                # add to list of retained variables
                retain_list.append(f'electricity_wastewater_{treatment_type}_bbtu')
                retain_list.append(f'wastewater_{treatment_type}_rejected_energy_bbtu')
                retain_list.append(f'wastewater_{treatment_type}_energy_services_bbtu')

                # add on to totals
                df['electricity_wastewater_total_bbtu'] = df['electricity_wastewater_total_bbtu'] \
                                                          + df[f'electricity_wastewater_{treatment_type}_bbtu']
                df['wastewater_rejected_energy_total_bbtu'] = df['wastewater_rejected_energy_total_bbtu'] \
                                                              + df[f'wastewater_{treatment_type}_rejected_energy_bbtu']
                df['wastewater_energy_services_total_bbtu'] = df['wastewater_energy_services_total_bbtu'] \
                                                              + df[f'wastewater_{treatment_type}_energy_services_bbtu']
            else:
                pass

    # add totals to retained lists of variables
    retain_list.append('electricity_wastewater_total_bbtu')
    retain_list.append('wastewater_rejected_energy_total_bbtu')
    retain_list.append('wastewater_energy_services_total_bbtu')
    total_list.append('electricity_wastewater_total_bbtu')
    total_list.append('wastewater_rejected_energy_total_bbtu')
    total_list.append('wastewater_energy_services_total_bbtu')

    # establish list of region columns to include in output
    column_list = df.columns[:regions].tolist()

    # if total is True, only return total energy to wastewater, rejected energy and energy services
    if total:
        for item in total_list:
            column_list.append(item)
        df = df[column_list]
    else:
        for item in retain_list:
            column_list.append(item)
        df = df[column_list]

    return df



def calc_electricity_public_water_supply(data: pd.DataFrame, regions=3, total=False, gw_pump_kwh_per_mg=920,
                                         gw_pws_fraction=.5, sw_pump_kwh_per_mg=145, desalination_kwh_mg=13600,
                                         sw_treatment_kwh_per_mg=405, gw_treatment_kwh_per_mg=205,
                                         distribution_kwh_per_mg=1040, ibt_fraction=.5, gw_pump_efficiency=.65,
                                         sw_pump_efficiency=.65, desalination_efficiency=.65,
                                         sw_treatment_efficiency=.65,
                                         gw_treatment_efficiency=.65, distribution_efficiency=.65,
                                         ibt_efficiency=.65):
    # TODO redo this as a loop through energy use types
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
    df['pws_sw_pumping_rejected_energy_bbtu'] = sw_pump_efficiency \
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

# TODO calculate energy in agriculture








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
