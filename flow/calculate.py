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
    # TODO expects a column with fuel percent, does not currently allow for getting rejected energy if total energy is
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
    for fuel_type in fuel_type_dict:
        df[f'{fuel_type}_wastewater_total_bbtu'] = 0
    df['wastewater_rejected_energy_total_bbtu'] = 0
    df['wastewater_energy_services_total_bbtu'] = 0

    # TODO add in option for fuel efficiency column like in agriculture

    # loops through each treatment type and fuel source to calculate electricity, rejected energy, and energy services
    for treatment_type in treatment_type_dict:
        treatment_flow_type = "wastewater_" + treatment_type + "_" + "treatment_mgd"
        for fuel_type in fuel_type_dict:
            fuel_pct = f"wastewater_{fuel_type}" + "_" + "fuel_pct"
            fuel_efficiency = f"wastewater_{fuel_type}" + "_" + "efficiency_fraction"
            if treatment_flow_type in df.columns:
                df[f'{fuel_type}_wastewater_{treatment_type}_bbtu'] = df[treatment_flow_type] \
                                                                      * convert_kwh_bbtu(
                    treatment_type_dict[treatment_type]) \
                                                                      * df[fuel_pct]

                df[f'wastewater_{treatment_type}_rejected_energy_bbtu'] = df[
                                                                              f'{fuel_type}_wastewater_{treatment_type}_bbtu'] \
                                                                          * (1 - fuel_type_dict[fuel_type])

                df[f'wastewater_{treatment_type}_energy_services_bbtu'] = df[
                                                                              f'{fuel_type}_wastewater_{treatment_type}_bbtu'] \
                                                                          * (fuel_type_dict[fuel_type])

                # add to list of retained variables
                retain_list.append(f'{fuel_type}_wastewater_{treatment_type}_bbtu')
                retain_list.append(f'wastewater_{treatment_type}_rejected_energy_bbtu')
                retain_list.append(f'wastewater_{treatment_type}_energy_services_bbtu')

                # add on to totals
                df[f'{fuel_type}_wastewater_total_bbtu'] = df[f'{fuel_type}_wastewater_total_bbtu'] \
                                                           + df[f'electricity_wastewater_{treatment_type}_bbtu']
                df['wastewater_rejected_energy_total_bbtu'] = df['wastewater_rejected_energy_total_bbtu'] \
                                                              + df[f'wastewater_{treatment_type}_rejected_energy_bbtu']
                df['wastewater_energy_services_total_bbtu'] = df['wastewater_energy_services_total_bbtu'] \
                                                              + df[f'wastewater_{treatment_type}_energy_services_bbtu']
            else:
                pass

    # add totals to retained lists of variables
    for fuel_type in fuel_type_dict:
        retain_list.append(f'{fuel_type}_wastewater_total_bbtu')
        total_list.append(f'{fuel_type}_wastewater_total_bbtu')
    retain_list.append('wastewater_rejected_energy_total_bbtu')
    retain_list.append('wastewater_energy_services_total_bbtu')
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


def calc_energy_agriculture(data: pd.DataFrame, pumping_types=None, agriculture_types=None, water_types=None,
                            fuel_types=None, fuel_percents=None, irrigation_ibt_pct=.5, regions=3, total=False):
    """calculates energy use, rejected energy, and energy services by fuel type for each agriculture subsector and
    water type and source (as applicable) in billion btu per year. An example output would be electricity use in
    fresh surface water pumping for crop irrigation by region. This function will use default fuel types, pumping
    efficiencies, fuel percentage shares, water types, agriculture types, pumping types, and irrigation interbasin
    transfer share unless other values are provided.

    #TODO NTS: Allows for a column of fuel efficiency at regional level. Does not currently allow for different fuel efficiencies
    by pumping type, water type, etc. Assumes one efficiency for all type of pumping (groundwater, surface, fresh, saline).
    Case study does not have this data at a county level. Assumes ibt pumping efficiency same as other pumping efficiency

        :param data:                        DataFrame of input data containing wastewater flow data in mgd
        :type data:                         DataFrame

        :param pumping_types:               a dictionary of pumping source types (e.g. groundwater) and their associated
                                            energy intensity in kWh per million gallons
        :type pumping_types:                dict

        :param agriculture_types:           a list of agriculture subsector types (e.g., crop_irrigation). Agriculture
                                            types must have an underscore between words.
        :type agriculture_types:            list

        :param fuel_types:                  a dictionary of fuel types to include (e.g., electricity, coal, petroleum)
                                            and their associated efficiency rating
        :type fuel_types:                   dict

        :param fuel_percents:               a dictionary of fuel types and their associated percentage share of total
                                            fuel for pumping
        :type fuel_percents:                dict

        :param irrigation_ibt_pct:          gives the percent share of total interbasin transfer energy used by
                                            crop irrigation
        :type irrigation_ibt_pct:           float

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
    if pumping_types is None:
        pumping_type_dict = {'groundwater': 920, 'surface_water': 145, 'wastewater': 145}
    else:
        pumping_type_dict = pumping_types

    # establish list of pumping types for irrigation
    if water_types is None:
        water_types_list = ['fresh', 'saline']
    else:
        water_types_list = water_types

    # establish list of agriculture water delivery types
    if agriculture_types is None:
        agriculture_type_list = ['crop_irrigation', 'golf_irrigation', 'livestock', 'aquaculture']
    else:
        agriculture_type_list = agriculture_types

    # TODO combine fuel_types and fuel_percents into a nested dictionary
    # establish dictionary of fuel types for agriculture applications and efficiencies
    if fuel_types is None:
        fuel_type_dict = {"electricity": .65, "natural_gas": .65, "oil": .65}
    else:
        fuel_type_dict = fuel_types

    # establish dictionary of fuel types for agriculture applications and associated fraction of pumping energy
    if fuel_percents is None:
        fuel_percent_dict = {"electricity": .6, "natural_gas": .01, "oil": .39}
    else:
        fuel_percent_dict = fuel_percents

    # initialize lists and values
    retain_list = []
    ibt_list = []
    total_list = []
    for agriculture_type in agriculture_type_list:
        df[f'{agriculture_type}_total_energy_bbtu'] = 0
        df[f'{agriculture_type}_total_energy_services_bbtu'] = 0
        df[f'{agriculture_type}_total_rejected_energy_bbtu'] = 0

    # calculate pumping energy for each fuel, agriculture, water, and pumping type
    for water_type in water_types_list:
        for pumping_type in pumping_type_dict:
            for agriculture_type in agriculture_type_list:
                pumping_flow_type = water_type + "_" + pumping_type + "_" + agriculture_type + "_mgd"
                pumping_intensity_type = pumping_type + "_pumping_bbtu_per_mg"
                for fuel_type in fuel_type_dict:
                    fuel_type_pct = fuel_type + "_pumping_pct"
                    # if the pumping type is in the dataframe
                    if pumping_flow_type in df.columns:

                        # if pumping intensity (bbtu_mg) is provided by region, use it
                        if pumping_intensity_type in df.columns:

                            # if there is a fuel percent column, use it
                            if fuel_type_pct in df.columns:
                                df[f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu'] = df[
                                                                                                             fuel_type_pct] \
                                                                                                         * df[
                                                                                                             pumping_flow_type] \
                                                                                                         * df[
                                                                                                             pumping_intensity_type]
                            # if there isn't a fuel percent column, use set percentages
                            else:
                                df[f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu'] = \
                                    fuel_percent_dict[fuel_type] * df[pumping_flow_type] * df[pumping_intensity_type]
                        # if no pumping intensity provided by region, use dict amount
                        else:
                            # if there is a fuel percent column, use it
                            if fuel_type_pct in df.columns:
                                df[f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu'] = df[
                                                                                                             fuel_type_pct] \
                                                                                                         * df[
                                                                                                             pumping_flow_type] \
                                                                                                         * convert_kwh_bbtu(
                                    pumping_type_dict[pumping_type])
                            else:  # if there isn't a fuel percent column, use set percentages
                                df[f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu'] = \
                                    fuel_percent_dict[
                                        fuel_type] \
                                    * df[pumping_flow_type] \
                                    * convert_kwh_bbtu(pumping_type_dict[pumping_type])
                        df[f'{agriculture_type}_total_energy_bbtu'] = df[f'{agriculture_type}_total_energy_bbtu'] \
                                                                      + df[
                                                                          f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu']

                        retain_list.append(f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu')

                    else:
                        pass

    # convert to bbtu per year from bbtu per day
    for item in retain_list:
        df[item] = df[item] * 365

    # calculate interbasin transfers for irrigation
    for fuel_type in fuel_type_dict:
        fuel_type_efficiency = 'agriculture_' + fuel_type + "_efficiency_pct"
        interbasin_fuel_type = f"{fuel_type}_interbasin_bbtu"
        if interbasin_fuel_type in df.columns:
            if 'crop_irrigation' in agriculture_type_list:
                if 'irrigation_ibt_pct' in df.columns:
                    df[f'{fuel_type}_irrigation_ibt_bbtu'] = df[f"{fuel_type}_interbasin_bbtu"] * df[
                        'irrigation_ibt_pct']
                else:
                    df[f'{fuel_type}_irrigation_ibt_bbtu'] = df[f"{fuel_type}_interbasin_bbtu"] * irrigation_ibt_pct

                df['crop_irrigation_total_energy_bbtu'] = df['crop_irrigation_total_energy_bbtu'] \
                                                          + df[f'{fuel_type}_irrigation_ibt_bbtu']

                if fuel_type_efficiency in df.columns:
                    df[f'{fuel_type}_irrigation_ibt_rejected_energy_bbtu'] = df[f'{fuel_type}_irrigation_ibt_bbtu'] \
                                                                             * (1 - df[fuel_type_efficiency])
                    df[f'{fuel_type}_irrigation_ibt_energy_services_bbtu'] = df[f'{fuel_type}_irrigation_ibt_bbtu'] \
                                                                             * (df[fuel_type_efficiency])
                else:
                    df[f'{fuel_type}_irrigation_ibt_rejected_energy_bbtu'] = df[f'{fuel_type}_irrigation_ibt_bbtu'] \
                                                                             * (1 - fuel_type_dict[fuel_type])
                    df[f'{fuel_type}_irrigation_ibt_energy_services_bbtu'] = df[f'{fuel_type}_irrigation_ibt_bbtu'] \
                                                                             * (fuel_type_dict[fuel_type])

                retain_list.append(f'{fuel_type}_irrigation_ibt_rejected_energy_bbtu')
                retain_list.append(f'{fuel_type}_irrigation_ibt_energy_services_bbtu')
                retain_list.append(f'{fuel_type}_irrigation_ibt_bbtu')

            else:
                pass
        else:
            pass

    # calculate rejected energy and energy services for each fuel, agriculture, water, and pumping type
    for water_type in water_types_list:
        for pumping_type in pumping_type_dict:
            for agriculture_type in agriculture_type_list:
                for fuel_type in fuel_type_dict:
                    fuel_type_efficiency = 'agriculture_' + fuel_type + "_efficiency_pct"
                    if f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu' in retain_list:
                        # if there's a fuel efficiency column
                        if fuel_type_efficiency in df.columns:
                            df[f'{agriculture_type}_{water_type}_{pumping_type}_rejected_energy_bbtu'] = (1 - df[
                                fuel_type_efficiency]) * df[
                                                                                                             f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu']
                            df[f'{agriculture_type}_{water_type}_{pumping_type}_energy_services_bbtu'] = (df[
                                fuel_type_efficiency]) * df[
                                                                                                             f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu']
                        # if there's no fuel efficiency column, use defaults
                        else:
                            df[f'{agriculture_type}_{water_type}_{pumping_type}_rejected_energy_bbtu'] = (1 -
                                                                                                          fuel_type_dict[
                                                                                                              fuel_type]) \
                                                                                                         * df[
                                                                                                             f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu']
                            df[f'{agriculture_type}_{water_type}_{pumping_type}_energy_services_bbtu'] = (
                                                                                                         fuel_type_dict[
                                                                                                             fuel_type]) \
                                                                                                         * df[
                                                                                                             f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu']
                        df[f'{agriculture_type}_total_rejected_energy_bbtu'] = df[
                                                                                   f'{agriculture_type}_total_rejected_energy_bbtu'] \
                                                                               + df[
                                                                                   f'{agriculture_type}_{water_type}_{pumping_type}_rejected_energy_bbtu']
                        df[f'{agriculture_type}_total_energy_services_bbtu'] = df[
                                                                                   f'{agriculture_type}_total_energy_services_bbtu'] \
                                                                               + df[
                                                                                   f'{agriculture_type}_{water_type}_{pumping_type}_energy_services_bbtu']
                        retain_list.append(f'{agriculture_type}_{water_type}_{pumping_type}_rejected_energy_bbtu')
                        retain_list.append(f'{agriculture_type}_{water_type}_{pumping_type}_energy_services_bbtu')

                    else:
                        pass

    # add ibt to crop irrigation total energy, rejected energy, and energy services
    for fuel_type in fuel_type_dict:
        if ('crop_irrigation_total_energy_bbtu' in df.columns) and (f'{fuel_type}_irrigation_ibt_bbtu' in df.columns):
            df['crop_irrigation_total_energy_bbtu'] = df['crop_irrigation_total_energy_bbtu'] \
                                                      + df[f'{fuel_type}_irrigation_ibt_bbtu']
            df['crop_irrigation_total_rejected_energy_bbtu'] = df['crop_irrigation_total_rejected_energy_bbtu'] \
                                                               + df[f'{fuel_type}_irrigation_ibt_rejected_energy_bbtu']
            df['crop_irrigation_total_energy_services_bbtu'] = df['crop_irrigation_total_energy_services_bbtu'] \
                                                               + df[f'{fuel_type}_irrigation_ibt_energy_services_bbtu']
        else:
            pass

    for agriculture_type in agriculture_type_list:
        total_list.append(f'{agriculture_type}_total_energy_bbtu')
        total_list.append(f'{agriculture_type}_total_rejected_energy_bbtu')
        total_list.append(f'{agriculture_type}_total_energy_services_bbtu')

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


def calc_energy_pws(data: pd.DataFrame, water_energy_types=None, fuel_types=None, pws_ibt_pct=.5, regions=3, total=False):
    """calculates energy use, rejected energy, and energy services by fuel type for each agriculture subsector and
    water type and source (as applicable) in billion btu per year. An example output would be electricity use in
    fresh surface water pumping for crop irrigation by region. This function will use default fuel types, pumping
    efficiencies, fuel percentage shares, water types, agriculture types, pumping types, and irrigation interbasin
    transfer share unless other values are provided

    ONLY CALCULATES TOTAL FOR TOTAL PWS, not by subcategory


        :param data:                        DataFrame of input data containing wastewater flow data in mgd
        :type data:                         DataFrame

        :param water_energy_types:          A nested dictionary containing energy intensity (kWh per mg) by water type
                                            (fresh, saline, etc.), water source (groundwater, surface, etc.), and energy
                                            demand type (pumping, treatment, distribution, etc.). If no dictionary is
                                            provided, default values are used. The function uses the water type, source,
                                            and energy application values to look for associated columns in the
                                            data.
        :type water_energy_types:           dict

        :param fuel_types:                  a nested dictionary of efficiency values (fraction) and fuel percentages
                                            (fraction) for a given fuel type (e.g., electricity, natural gas, petroleum).
                                            If columns with regional data are not provided on fuel efficiency and fuel
                                            percentages, values from this dictionary are applied to all regions.
        :type fuel_types:                   dict

        :param pws_ibt_pct:                 gives the percent share of total interbasin transfer energy used by
                                            public water supply to apply to all regions in DataFrame.
        :type pws_ibt_pct:                  float

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
                                            and total energy services by sector instead of by fuel type
        :type total:                        bool

        :return:                            DataFrame of energy use, rejected energy, and energy services for the public
                                            water sector by energy application (e.g., pumping, treatment) in billion btu

        """

    # load data
    df = data



    if water_energy_types is None:
        types_dict = {'fresh':
                          {'groundwater': {'pumping': 920, 'treatment': 205, 'distribution': 1040},
                           'surface_water': {'pumping': 145, 'treatment': 405, 'distribution': 1040}},
                      'saline':
                          {'groundwater':{'pumping': 920, 'treatment': 13805, 'distribution': 1040},
                           'surface_water':{'pumping': 145, 'treatment': 14005, 'distribution': 1040}}}
    else:
        types_dict = water_energy_types

    # establish dictionary of fuel types along with their associated efficiencies and percent of energy demand
    if fuel_types is None:
        fuel_type_dict = {"electricity": {'efficiency': .65, 'fuel_pct': 1}}
    else:
        fuel_type_dict = fuel_types

    # initialize lists and values
    retain_list = []
    total_list = []
    df[f'pws_total_energy_bbtu'] = 0
    df[f'pws_total_energy_services_bbtu'] = 0
    df[f'pws_total_rejected_energy_bbtu'] = 0
    for water_type in types_dict:
        for source_type in types_dict[water_type]:
            for energy_type in types_dict[water_type][source_type]:
                df[f'pws_{energy_type}_total_energy_bbtu'] = 0
                df[f'pws_{energy_type}_total_energy_services_bbtu'] = 0
                df[f'pws_{energy_type}_total_rejected_energy_bbtu'] = 0

    # build loop for calculations
    for water_type in types_dict:
        df[f'{water_type}_total_energy_bbtu'] = 0
        for source_type in types_dict[water_type]:
            flow_type = water_type + "_" + source_type + "_pws_mgd"  # look for columns with pws values
            if flow_type in df.columns:
                for energy_type in types_dict[water_type][source_type]:
                    for fuel_type in fuel_type_dict:
                        fuel_type_efficiency = 'pws_' + fuel_type + "_efficiency_pct"
                        fuel_type_pct = 'pws_' + fuel_type + "_fuel_pct"
                        #calculate energy use
                        df[f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] = (df[flow_type] *
                                                                                                fuel_type_dict[
                                                                                                    fuel_type][
                                                                                                    'fuel_pct']) * 365 \
                                                                                               * convert_kwh_bbtu(
                                                                                               types_dict[water_type][
                                                                                                   source_type][
                                                                                                   energy_type])
                        #calculate energy services and rejected energy
                        if fuel_type_efficiency in df.columns:
                            df[f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu'] = df[f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                       * (1 - df[fuel_type_efficiency])
                            df[f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu'] = df[
                                                                                                           f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                       * df[fuel_type_efficiency]
                        else:
                            df[f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu'] = df[f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                     * (1 - fuel_type_dict[fuel_type]['efficiency'])
                            df[f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu'] = df[f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                     * (fuel_type_dict[fuel_type]['efficiency'])

                        #add to totals
                        df[f'pws_{energy_type}_total_energy_bbtu'] = df[f'pws_{energy_type}_total_energy_bbtu'] + df[f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu']
                        df[f'pws_{energy_type}_total_energy_services_bbtu'] = df[f'pws_{energy_type}_total_energy_services_bbtu'] \
                                                                     + df[f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu']
                        df[f'pws_{energy_type}_total_rejected_energy_bbtu'] = df[f'pws_{energy_type}_total_rejected_energy_bbtu'] \
                                                                          + df[f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu']

                        df[f'pws_total_energy_bbtu'] = df[f'pws_total_energy_bbtu'] + df[
                                                                         f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu']
                        df[f'pws_total_energy_services_bbtu'] = df[f'pws_total_energy_services_bbtu']  \
                                                                              + df[
                                                                                  f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu']
                        df[f'pws_total_rejected_energy_bbtu'] = df[f'pws_total_rejected_energy_bbtu'] \
                                                                              + df[
                                                                                  f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu']
                        # add to retain list
                        retain_list.append(f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu')
                        retain_list.append(f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu')
                        retain_list.append(f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu')

            else:
                pass

    # add columns to total list
    total_list.append('pws_total_energy_bbtu')
    total_list.append('pws_total_rejected_energy_bbtu')
    total_list.append('pws_total_energy_services_bbtu')

    for water_type in types_dict:
        for source_type in types_dict[water_type]:
            for energy_type in types_dict[water_type][source_type]:
                if f'pws_{energy_type}_total_energy_bbtu' in total_list:
                    pass
                else:
                    total_list.append(f'pws_{energy_type}_total_energy_bbtu')
                if f'pws_{energy_type}_total_energy_services_bbtu' in total_list:
                    pass
                else:
                    total_list.append(f'pws_{energy_type}_total_energy_services_bbtu')
                if f'pws_{energy_type}_total_rejected_energy_bbtu' in total_list:
                    pass
                else:
                    total_list.append(f'pws_{energy_type}_total_rejected_energy_bbtu')

    # set initial total interbasin transfer values
    df['pws_total_ibt_energy_bbtu'] = 0
    df['pws_total_ibt_energy_services_bbtu'] = 0
    df['pws_total_ibt_rejected_energy_bbtu'] = 0

    # calculate interbasin transfers for public water supply
    for fuel_type in fuel_type_dict:
        fuel_type_efficiency = 'pws_' + fuel_type + "_efficiency_pct"
        interbasin_fuel_type = f"{fuel_type}_interbasin_bbtu"
        if interbasin_fuel_type in df.columns:
            if 'pws_ibt_pct' in df.columns:
                df[f'{fuel_type}_pws_ibt_bbtu'] = df[f"{fuel_type}_interbasin_bbtu"] * df['pws_ibt_pct']
            else:
                df[f'{fuel_type}_pws_ibt_bbtu'] = df[f"{fuel_type}_interbasin_bbtu"] * pws_ibt_pct

            if fuel_type_efficiency in df.columns:
                df[f'{fuel_type}_pws_ibt_rejected_energy_bbtu'] = df[f'{fuel_type}_pws_ibt_bbtu'] \
                                                                         * (1 - df[fuel_type_efficiency])
                df[f'{fuel_type}_pws_ibt_energy_services_bbtu'] = df[f'{fuel_type}_pws_ibt_bbtu'] \
                                                                         * (df[fuel_type_efficiency])
            else:
                df[f'{fuel_type}_pws_ibt_rejected_energy_bbtu'] = df[f'{fuel_type}_pws_ibt_bbtu'] \
                                                                         * (1 - fuel_type_dict[fuel_type]['efficiency'])
                df[f'{fuel_type}_pws_ibt_energy_services_bbtu'] = df[f'{fuel_type}_pws_ibt_bbtu'] \
                                                                         * (fuel_type_dict[fuel_type]['efficiency'])

            # add to total IBT energy
            df['pws_total_ibt_energy_bbtu'] = df['pws_total_ibt_energy_bbtu'] + df[f'{fuel_type}_pws_ibt_bbtu']
            df['pws_total_ibt_rejected_energy_bbtu'] = df['pws_total_ibt_rejected_energy_bbtu'] + df[f'{fuel_type}_pws_ibt_rejected_energy_bbtu']
            df['pws_total_ibt_energy_services_bbtu'] = df['pws_total_ibt_energy_services_bbtu'] + df[f'{fuel_type}_pws_ibt_energy_services_bbtu']

            # add columns to retained data list
            retain_list.append(f'{fuel_type}_pws_ibt_bbtu')
            retain_list.append(f'{fuel_type}_pws_ibt_rejected_energy_bbtu')
            retain_list.append(f'{fuel_type}_pws_ibt_energy_services_bbtu')

            # add columns to total list
            total_list.append(f'{fuel_type}_pws_ibt_bbtu')
            total_list.append(f'{fuel_type}_pws_ibt_rejected_energy_bbtu')
            total_list.append(f'{fuel_type}_pws_ibt_energy_services_bbtu')

            # add on to total energy
            df[f'pws_total_energy_bbtu'] = df[f'pws_total_energy_bbtu'] + df['pws_total_ibt_energy_bbtu']
            df[f'pws_total_energy_services_bbtu'] = df[f'pws_total_energy_services_bbtu'] + df['pws_total_ibt_energy_services_bbtu']
            df[f'pws_total_rejected_energy_bbtu'] = df[f'pws_total_rejected_energy_bbtu'] + df['pws_total_ibt_rejected_energy_bbtu']

        else:
            pass

    # establish list of region columns to include in output
    column_list = df.columns[:regions].tolist()

    # determine which subset of columns to produce in output
    if total:
        for item in total_list:
            column_list.append(item)
        df = df[column_list]
    else:
        for item in retain_list:
            column_list.append(item)
        df = df[column_list]

    return df



# move to clean, add to configure
def calc_pws_discharge() -> pd.DataFrame:
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
