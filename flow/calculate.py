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

    df['electricity_rejected_energy_bbtu'] = 0
    retain_list = []
    for type in generation_type_list:
        fuel_type = type + "_fuel_bbtu"
        gen_type = type + "_gen_bbtu"

        if (fuel_type in df.columns) and (gen_type in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] - df[gen_type]
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
        elif (fuel_type in df.columns) and (gen_type not in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 - generation_efficiency)
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
        elif (fuel_type not in df.columns) and (gen_type in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 / (1 - generation_efficiency))
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')

        else:
            df[f'electricity_{type}_rejected_energy_bbtu'] = 0
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                           + df[f'electricity_{type}_rejected_energy_bbtu']

    if total:
        column_list = df.columns[:regions].tolist()
        column_list.append('electricity_rejected_energy_bbtu')
        df = df[column_list]
    else:
        column_list = df.columns[:regions].tolist()
        for item in retain_list:
            column_list.append(item)
        column_list.append('electricity_rejected_energy_bbtu')
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


def calc_sectoral_use_water_discharge(data: pd.DataFrame, sector_types=None, discharge_types=None,
                                      regions=3, total=False):
    """calculates water consumption and discharge in mgd for various sectors. Consumption is calculated first based on
    assumed consumption fractions provided either in the dataset on a regional level or using the values in the
    sector_types dictionary. Additional discharge locations (e.g., surface discharge, ocean discharge) are determined
    by the remaining water delivered to each sector that is not consumed. Discharge fractions can be used from the data
    if available, otherwise values in the discharge_types dictionary are used.

        :param data:                        DataFrame of input data containing fuel demand data for each sector
        :type data:                         DataFrame

        :param sector_types:                a nested dictionary of water consumption fractions by sector types, water
                                            source, and water type.
        :type sector_types:                 dictionary

        :param water_types:                 a nested dictionary of discharge fractions for each discharge type, listed
                                            by water source and water type.
        :type water_types:                  dictionary

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
                                            and total energy services by sector instead of by fuel type
        :type total:                        bool

        :return:                            DataFrame of water discharge estimates from various sectors

        """

    # load data
    df = data

    if sector_types is None:
        sector_consumption_dict = {'residential': {'groundwater': {'saline': 0, 'fresh': .3},
                                                   'surfacewater': {'saline': 0, 'fresh': .3},
                                                   'pws': {'fresh': .3}},
                            'commercial': {'groundwater': {'saline': 0, 'fresh': .15},
                                           'surfacewater': {'saline': 0, 'fresh': .15},
                                           'pws': {'fresh': .15}},
                            'industrial':{'groundwater': {'saline': .003, 'fresh': .15},
                                          'surfacewater': {'saline': .003, 'fresh': .15},
                                          'pws': {'fresh': .15}},
                            'mining': {'groundwater': {'saline': .03, 'fresh': .15},
                                       'surfacewater': {'saline': .03, 'fresh': .15}},
                            'crop_irrigation': {'groundwater': {'saline': 0, 'fresh': .3},
                                                'surfacewater': {'saline': 0, 'fresh': .3}},
                            'livestock':  {'groundwater': {'saline': 0, 'fresh': .87},
                                           'surfacewater': {'saline': 0, 'fresh': .87}},
                            'aquaculture': {'groundwater': {'saline': 0, 'fresh': .5},
                                            'surfacewater': {'saline': 0, 'fresh': .5}}}
    else:
        sector_consumption_dict = sector_types
    if discharge_types is None:
        water_discharge_dict = {'surfacewater': {'fresh': {'wastewater': 0, 'ocean': 0, 'surface': 1},
                                                 'saline': {'wastewater': 0, 'ocean': 1, 'surface': 0}},
                                'groundwater': {'fresh': {'wastewater': 0, 'ocean': 0, 'surface': 1},
                                                'saline': {'wastewater': 0, 'ocean': 1, 'surface': 0}},
                                'pws': {'fresh': {'wastewater': 1, 'ocean': 0, 'surface': 0}}}
    else:
        water_discharge_dict = discharge_types

    column_list = df.columns[:regions].tolist()
    output_df = df[column_list].copy()
    total_df = df[column_list].copy()

    for sector_type in sector_consumption_dict:
        consumptive_use_total_name = f'{sector_type}_consumption_mgd'
        total_df[consumptive_use_total_name] = 0
        for water_source in sector_consumption_dict[sector_type]:
            for water_type in sector_consumption_dict[sector_type][water_source]:
                consumptive_use_name = f'{sector_type}_{water_type}_{water_source}_consumption_mgd'
                output_df[consumptive_use_name] = 0

    # calculate consumptive use
    for sector_type in sector_consumption_dict:
        for water_source in sector_consumption_dict[sector_type]:
            for water_type in sector_consumption_dict[sector_type][water_source]:
                water_withdrawal_name = f'{water_type}_{water_source}_{sector_type}_mgd'
                if water_withdrawal_name in df.columns:
                    consumptive_use_total_name = f'{sector_type}_consumption_mgd'
                    consumptive_use_name = f'{sector_type}_{water_type}_{water_source}_consumption_mgd'
                    if consumptive_use_name in df.columns:
                        output_df[consumptive_use_name] = df[consumptive_use_name]
                        total_df[consumptive_use_total_name] = total_df[consumptive_use_total_name] \
                                                               + df[consumptive_use_name]
                    else:
                        consumptive_fraction_name = f'{sector_type}_{water_type}_{water_source}_consumption_fraction'
                        if consumptive_fraction_name in df.columns:
                            consumptive_use_value = df[consumptive_fraction_name] * df[water_withdrawal_name]
                            output_df[consumptive_use_name] = output_df[consumptive_use_name] + consumptive_use_value
                            total_df[consumptive_use_total_name] = total_df[consumptive_use_total_name] \
                                                                   + consumptive_use_value
                        else:
                            consumptive_use_value = sector_consumption_dict[sector_type][water_source][water_type]\
                                                    * df[water_withdrawal_name]
                            output_df[consumptive_use_name] = output_df[consumptive_use_name] \
                                                              + consumptive_use_value
                            total_df[consumptive_use_total_name] = total_df[consumptive_use_total_name] \
                                                                   + consumptive_use_value
                else:
                    pass

    #set initial discharge total value
    for sector_type in sector_consumption_dict: # residential, commercial, etc.
        for water_source in water_discharge_dict: # groundwater, pws, etc.
            for water_type in water_discharge_dict[water_source]: # fresh, saline
                water_withdrawal_name = f'{water_type}_{water_source}_{sector_type}_mgd'
                if water_withdrawal_name in df.columns:
                    consumptive_use_name = f'{sector_type}_{water_type}_{water_source}_consumption_mgd'
                    if consumptive_use_name in output_df.columns:
                        for discharge_type in water_discharge_dict[water_source][water_type]:
                            discharge_total_name = f'{sector_type}_{discharge_type}_discharge_mgd'
                            total_df[discharge_total_name] = 0

     # calculate discharge
    for sector_type in sector_consumption_dict: # residential, commercial, etc.
        for water_source in water_discharge_dict: # groundwater, pws, etc.
            for water_type in water_discharge_dict[water_source]: # fresh, saline
                water_withdrawal_name = f'{water_type}_{water_source}_{sector_type}_mgd'
                if water_withdrawal_name in df.columns:
                    consumptive_use_name = f'{sector_type}_{water_type}_{water_source}_consumption_mgd'
                    if consumptive_use_name in output_df.columns:
                        for discharge_type in water_discharge_dict[water_source][water_type]:
                            discharge_total_name = f'{sector_type}_{discharge_type}_discharge_mgd'
                            discharge_name = f'{sector_type}_{water_type}_{water_source}_{discharge_type}_discharge_mgd'
                            # if the discharge quantity is already in the baseline dataset, use it
                            if discharge_name in df.columns:
                                output_df[discharge_name] = df[discharge_name]
                                total_df[discharge_total_name] = total_df[discharge_total_name] + df[discharge_name]

                            # otherwise calculate it
                            else:
                                # if there's region-level discharge fractions, use that
                                discharge_fraction_name = f'{sector_type}_{water_type}_{water_source}_{discharge_type}_fraction'
                                if discharge_fraction_name in df.columns:
                                    output_df[discharge_name] = df[discharge_fraction_name] \
                                                                * (df[water_withdrawal_name]
                                                                   - output_df[consumptive_use_name])
                                    total_df[discharge_total_name] = total_df[discharge_total_name] + output_df[discharge_name]

                                #otherwise calculate from default fraction assumptions in dictionary
                                else:
                                    output_df[discharge_name] = water_discharge_dict[water_source][water_type][discharge_type] \
                                                                * (df[water_withdrawal_name]-output_df[consumptive_use_name])

                                    total_df[discharge_total_name] = total_df[discharge_total_name] + output_df[discharge_name]
                    else:
                        pass
                else:
                    pass

    # if total is True, only return total rejected energy and energy services by sector
    if total:
        df = total_df
    else:
        df = output_df
    return df


def calc_sector_water_exports(data: pd.DataFrame, sector_types=None, regions=3, total=False):
    """calculates wastewater exports by region and sector, imports to wastewater treatment by region, and net exports
    by region. The function relies on discharge to wastewater values calculated from the calc_sector_discharge module(),
    and total municipal wastewater processed from the baseline data. If no data fpr total municipal wastewater flows
    is available in the baseline data, it is assumed that all estimated discharges to wastewater from each sector is
    processed by wastewater treatment facilities in the same region, and that there are no exports or imports between
    regions.

        :param data:                        DataFrame of input data containing fuel demand data for each sector
        :type data:                         DataFrame

        :param sector_types:                a list of sectors to include in analysis
        :type sector_types:                 list

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of identifier columns and total rejected energy
                                            and total energy services by sector instead of by fuel type
        :type total:                        bool

        :return:                            DataFrame of wastewater exports, imports, and net exports by region

        """

    # load data
    df = data

    # sector discharge data
    df_sector_discharge = calc_sectoral_use_water_discharge(data=data, total=True)

    # establish list of sector types
    if sector_types is None:
        sector_list = ['residential', 'commercial', 'industrial']
    else:
        sector_list = sector_types

    # initialize output dataframes
    column_list = df.columns[:regions].tolist()
    output_df = df[column_list].copy()
    total_df = df[column_list].copy()

    # initialize values
    output_df['total_wastewater_discharge'] = 0

    # calculate total wastewater discharge from sectors and discharge ratios
    for sector in sector_list:
        output_df[f'{sector}_wastewater_discharge_mgd'] = df_sector_discharge[f'{sector}_wastewater_discharge_mgd']
        output_df['total_wastewater_discharge'] = output_df['total_wastewater_discharge'] \
                                                  + df_sector_discharge[f'{sector}_wastewater_discharge_mgd']
        total_df['total_wastewater_discharge'] = output_df['total_wastewater_discharge']

    # calculate the discharge ratio
    for sector in sector_list:
        output_df[f'{sector}_wastewater_discharge_ratio'] = output_df[f'{sector}_wastewater_discharge_mgd'] / \
                                                     output_df['total_wastewater_discharge']

    # if separate municipal wastewater flow data exists in the dataset, use it to calculate exports from sectors
    if 'municipal_wastewater_mgd' in df.columns:
        # calculate exports/imports as the different between total discharges from sectors and collections by wastewater
        output_df['wastewater_export_mgd'] = np.where((df['municipal_wastewater_mgd']
                                                       - output_df['total_wastewater_discharge']) < 0,
                                               (output_df['total_wastewater_discharge']
                                                - df['municipal_wastewater_mgd']),
                                               0)
        output_df['wastewater_import_mgd'] = np.where((df['municipal_wastewater_mgd']
                                                       - output_df['total_wastewater_discharge']) > 0,
                                               (df['municipal_wastewater_mgd']
                                                - output_df['total_wastewater_discharge']),
                                               0)

        output_df['wastewater_net_export_mgd'] = output_df['wastewater_export_mgd'] \
                                                 - output_df['wastewater_import_mgd']

        # add to total dataframe
        total_df['municipal_wastewater_mgd'] = df['municipal_wastewater_mgd']
        total_df['wastewater_export_mgd'] = output_df['wastewater_export_mgd']
        total_df['wastewater_import_mgd'] = output_df['wastewater_import_mgd']
        total_df['wastewater_net_export_mgd'] = output_df['wastewater_net_export_mgd']

        # calculate portion of wastewater exports from each sector
        for sector in sector_list:
            output_df[f'{sector}_wastewater_export_mgd'] = output_df[f'{sector}_wastewater_discharge_ratio'] \
                                                           * output_df['wastewater_export_mgd']
            total_df[f'{sector}_wastewater_export_mgd'] = output_df[f'{sector}_wastewater_export_mgd']

    # otherwise, wastewater total flows is equal to total discharge from sectors and imports/exports are assumed zero
    else:
        output_df['municipal_wastewater_mgd'] = output_df['total_wastewater_discharge']
        output_df['wastewater_export_mgd'] = 0
        output_df['wastewater_import_mgd'] = 0

    if total:
        df = total_df
    else:
        df = output_df
    return df


def calc_energy_wastewater(data: pd.DataFrame, treatment_types=None, fuel_types=None, regions=3, total=False):
    """Calculates energy, rejected energy, and energy services, in wastewater treatment in billion btu by region.

    If individual flow values by wastewater treatment type (e.g., advanced) are provided in the baseline data, energy
    estimates will be calculated directly, otherwise, total wastewater treatment flows will be split into specified
    treatment types based on assumed percentages of total and energy calculated based on the result. If total
    wastewater flows are not provided in the baseline data, estimated total wastewater flows are used from sector
    discharge to wastewater calculations. The option to supply treatment types (e.g., primary), treatment type energy
    intensity (kWh/mg), fuel types (e.g., electricity), fuel type efficiency (%), and fuel type fraction of energy
    applied (%) is available and should be provided as nested dictionaries.

        :param data:                        DataFrame of input data containing wastewater flow data in mgd
        :type data:                         DataFrame

        :param treatment_types:             a nested dictionary of wastewater treatment types that gives their
                                            energy intensity in kWh/mg and an assumed percent of total wastewater
                                            treatment type to use apply if water flows by treatment type are not
                                            available in the baseline dataset (e.g., wastewater_advance_mgd). In the
                                            latter scenario, percent of wastewater treatment assumption will be applied
                                            either to the total wastewater flows (if available in the baseline data)
                                            or apply them to the estimated wastewater data from the sector discharge
                                            function. Default values for percent of total water flows by treatment
                                            type are provided if none are supplied.
        :type treatment_types:              dictionary

        :param fuel_types:                  a nested dictionary of fuel types used in wastewater treatment
                                            (e.g., electricity, coal, petroleum) along with their associated efficiency
                                            rating and an assumption for percent of total energy use. The function will
                                            first look for columns in the baseline data with individual efficiency and
                                            percentage values by region for each fuel type. If none are found, it will
                                            apply the assumptions in the fuel_types dictionary.
        :type fuel_types:                   dictionary

        :param regions:                     gives the number of columns in the dataset that should be treated as region
                                            identifiers (e.g. "Country", "State"). Reads from the first column in the
                                            dataframe onwards.
        :type regions:                      int

        :param total:                       If true, returns dataframe of region identifier columns and aggregated
                                            output
        :type total:                        bool

        :return:                            DataFrame of energy, rejected energy, and energy services, in wastewater
                                            treatment in billion btu by region

        """

    # load data
    df = data

    # load sector discharge to wastewater estimates
    df_ww = calc_sector_water_exports(data=df)

    # establish dictionary of treatment types as keys and energy intensities as values (kWh/MG).
    if treatment_types is None:  # default key value pairs
        treatment_type_dict = {'advanced': {'intensity': 2690, 'percent': .5},
                               'secondary': {'intensity': 2080,'percent': .4},
                               'primary': {'intensity': 750, 'percent': .1}}
    else:
        treatment_type_dict = treatment_types
#
    # if no fuel type dictionary is provided, default is electricity at 65% efficiency
    if fuel_types is None:  # default key value pairs
        fuel_type_dict = {'electricity': {'efficiency': .65, 'percent': 1}}
    else:
        fuel_type_dict = fuel_types

    retain_list = []
    total_list = []

    for fuel_type in fuel_type_dict:
        df[f'{fuel_type}_wastewater_bbtu'] = 0
    df['wastewater_rejected_energy_bbtu'] = 0
    df['wastewater_energy_services_bbtu'] = 0

    # loop through treatment types and fuel types to calculate energy in wastewater (bbtu)
    for treatment_type in treatment_type_dict:
        treatment_flow_type_mgd = "wastewater_" + treatment_type + "_" + "treatment_mgd"
        treatment_energy_intensity_bbtu = convert_kwh_bbtu(treatment_type_dict[treatment_type]['intensity'])
        for fuel_type in fuel_type_dict:
            fuel_pct = f"wastewater_{fuel_type}" + "_" + "fuel_pct"
            fuel_efficiency = f"wastewater_{fuel_type}" + "_" + "efficiency_fraction"
            ww_energy_value_name = f'{fuel_type}_wastewater_{treatment_type}_bbtu'
            ww_re_name = f'wastewater_{treatment_type}_rejected_energy_bbtu'
            ww_es_name = f'wastewater_{treatment_type}_energy_services_bbtu'

            if treatment_flow_type_mgd in df.columns:
                df[treatment_flow_type_mgd] = df[treatment_flow_type_mgd]
            else:
                if 'municipal_wastewater_mgd' in df.columns:
                    df[treatment_flow_type_mgd] = df['municipal_wastewater_mgd']\
                                              *treatment_type_dict[treatment_type]['percent']
                elif 'municipal_wastewater_mgd' in df_ww.columns:
                    df[treatment_flow_type_mgd] = df_ww['municipal_wastewater_mgd'] \
                                              * treatment_type_dict[treatment_type]['percent']

            # calculate annual energy in wastewater treatment by treatment type
            if fuel_pct in df.columns:
                df[ww_energy_value_name] = df[treatment_flow_type_mgd] \
                                           * treatment_energy_intensity_bbtu \
                                           * df[fuel_pct] * 365
            else:
                df[ww_energy_value_name] = df[treatment_flow_type_mgd] \
                                           * treatment_energy_intensity_bbtu \
                                           * fuel_type_dict[fuel_type]['percent'] * 365

            if fuel_efficiency in df.columns:
                df[ww_re_name] = df[ww_energy_value_name] * (1 - df[fuel_efficiency])
                df[ww_es_name] = df[ww_energy_value_name] * (df[fuel_efficiency])
            else:
                df[ww_re_name] = df[ww_energy_value_name] * (1 - fuel_type_dict[fuel_type]['efficiency'])
                df[ww_es_name] = df[ww_energy_value_name] * (fuel_type_dict[fuel_type]['efficiency'])

            # add to list of retained variables
            retain_list.append(ww_energy_value_name)
            retain_list.append(ww_re_name)
            retain_list.append(ww_es_name)

            # add on to totals
            df[f'{fuel_type}_wastewater_bbtu'] = df[f'{fuel_type}_wastewater_bbtu'] + df[ww_energy_value_name]
            df['wastewater_rejected_energy_bbtu'] = df['wastewater_rejected_energy_bbtu'] + df[ww_re_name]
            df['wastewater_energy_services_bbtu'] = df['wastewater_energy_services_bbtu'] + df[ww_es_name]

    # add totals to retained lists of variables
    for fuel_type in fuel_type_dict:
        retain_list.append(f'{fuel_type}_wastewater_bbtu')
        total_list.append(f'{fuel_type}_wastewater_bbtu')

    retain_list.append('wastewater_rejected_energy_bbtu')
    retain_list.append('wastewater_energy_services_bbtu')
    total_list.append('wastewater_rejected_energy_bbtu')
    total_list.append('wastewater_energy_services_bbtu')

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
        pumping_type_dict = {'groundwater': 920, 'surfacewater': 145, 'wastewater': 145}
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
        fuel_type_dict = {"electricity": .65, "natural_gas": .65, "petroleum": .65}
    else:
        fuel_type_dict = fuel_types

    # establish dictionary of fuel types for agriculture applications and associated fraction of pumping energy
    if fuel_percents is None:
        fuel_percent_dict = {"electricity": .6, "natural_gas": .01, "petroleum": .39}
    else:
        fuel_percent_dict = fuel_percents

    # initialize lists and values
    energy_value_dict = {}
    rejected_energy_dict = {}
    energy_services_dict = {}

    column_list = df.columns[:regions].tolist()
    total_df = df[column_list].copy()

    for fuel_type in fuel_type_dict:
        total_df[f'{fuel_type}_agriculture_bbtu'] = 0
        total_df[f'{fuel_type}_irrigation_ibt_bbtu'] = 0

    for agriculture_type in agriculture_type_list:
        total_df[f'{agriculture_type}_total_energy_services_bbtu'] = 0
        total_df[f'{agriculture_type}_total_rejected_energy_bbtu'] = 0
        for fuel_type in fuel_type_dict:
            total_df[f'{fuel_type}_{agriculture_type}_bbtu'] = 0

    # calculate pumping energy for each fuel, agriculture, water, and pumping type
    for water_type in water_types_list:
        for pumping_type in pumping_type_dict:
            for agriculture_type in agriculture_type_list:

                pumping_flow_type = water_type + "_" + pumping_type + "_" + agriculture_type + "_mgd"
                pumping_intensity_type = pumping_type + "_pumping_bbtu_per_mg"

                for fuel_type in fuel_type_dict:

                    fuel_type_pct = fuel_type + "_pumping_pct"
                    fuel_type_efficiency = 'agriculture_' + fuel_type + "_efficiency_pct"

                    if pumping_flow_type in df.columns:
                        energy_name = f'{fuel_type}_{agriculture_type}_{water_type}_{pumping_type}_bbtu'
                        if pumping_intensity_type in df.columns:
                            if fuel_type_pct in df.columns:
                                energy_value = df[fuel_type_pct] * df[pumping_flow_type] * df[
                                    pumping_intensity_type] * 365
                            else:
                                energy_value = fuel_percent_dict[fuel_type] * df[pumping_flow_type] * df[
                                    pumping_intensity_type] * 365
                        else:
                            if fuel_type_pct in df.columns:
                                energy_value = df[fuel_type_pct] * df[pumping_flow_type] * convert_kwh_bbtu(
                                    pumping_type_dict[pumping_type]) * 365
                            else:
                                energy_value = fuel_percent_dict[fuel_type] * df[pumping_flow_type] * convert_kwh_bbtu(
                                    pumping_type_dict[pumping_type]) * 365

                        energy_value_dict.update({energy_name: energy_value})
                        total_df[f'{fuel_type}_{agriculture_type}_bbtu'] = total_df[
                                                                               f'{fuel_type}_{agriculture_type}_bbtu'] \
                                                                           + energy_value
                        total_df[f'{fuel_type}_agriculture_bbtu'] = total_df[
                                                                        f'{fuel_type}_agriculture_bbtu'] + energy_value

                        rejected_energy_name = f'{agriculture_type}_{water_type}_{pumping_type}_{fuel_type}_rejected_energy_bbtu'
                        energy_services_name = f'{agriculture_type}_{water_type}_{pumping_type}_{fuel_type}_energy_services_bbtu'

                        if fuel_type_efficiency in df.columns:
                            rejected_energy_value = (1 - df[fuel_type_efficiency]) * energy_value
                            energy_services_value = (df[fuel_type_efficiency]) * energy_value
                        else:
                            rejected_energy_value = (1 - fuel_type_dict[fuel_type]) * energy_value
                            energy_services_value = (fuel_type_dict[fuel_type]) * energy_value

                        rejected_energy_dict.update({rejected_energy_name: rejected_energy_value})
                        energy_services_dict.update({energy_services_name: energy_services_value})


                        total_re_name = f'{agriculture_type}_total_rejected_energy_bbtu'
                        total_es_name = f'{agriculture_type}_total_energy_services_bbtu'
                        total_df[total_re_name] = total_df[total_re_name] + rejected_energy_value
                        total_df[total_es_name] = total_df[total_es_name] + energy_services_value

                    else:
                        pass

    # change dictionaries to dataframes
    energy_value_df = pd.DataFrame.from_dict(energy_value_dict, orient='index').transpose()
    rejected_energy_df = pd.DataFrame.from_dict(rejected_energy_dict, orient='index').transpose()
    energy_services_df = pd.DataFrame.from_dict(energy_services_dict, orient='index').transpose()

    # calculate interbasin transfers for irrigation
    for fuel_type in fuel_type_dict:
        fuel_type_efficiency = 'agriculture_' + fuel_type + "_efficiency_pct"
        interbasin_fuel_type = f"{fuel_type}_interbasin_bbtu"
        if interbasin_fuel_type in df.columns:
            if 'crop_irrigation' in agriculture_type_list:
                energy_name = f'{fuel_type}_irrigation_ibt_bbtu'

                if 'irrigation_ibt_pct' in df.columns:
                    energy_value_df[energy_name] = df[f"{fuel_type}_interbasin_bbtu"] * df['irrigation_ibt_pct']
                else:
                    energy_value_df[energy_name] = df[f"{fuel_type}_interbasin_bbtu"] * irrigation_ibt_pct

                # Add to total
                total_df[f'{fuel_type}_agriculture_bbtu'] = total_df[f'{fuel_type}_agriculture_bbtu'] + \
                                                            energy_value_df[energy_name]
                total_df[f'{fuel_type}_irrigation_ibt_bbtu'] = total_df[f'{fuel_type}_irrigation_ibt_bbtu'] \
                                                               + energy_value_df[energy_name]

                rejected_energy_name = f'{fuel_type}_irrigation_ibt_rejected_energy_bbtu'
                energy_services_name = f'{fuel_type}_irrigation_ibt_energy_services_bbtu'

                if fuel_type_efficiency in df.columns:
                    rejected_energy_df[rejected_energy_name] = energy_value_df[energy_name] * (
                                1 - df[fuel_type_efficiency])
                    energy_services_df[energy_services_name] = energy_value_df[energy_name] * (df[fuel_type_efficiency])
                else:
                    rejected_energy_df[rejected_energy_name] = energy_value_df[energy_name] * (
                                1 - fuel_type_dict[fuel_type])
                    energy_services_df[energy_services_name] = energy_value_df[energy_name] * (
                    fuel_type_dict[fuel_type])

            else:
                pass

        else:
            pass

    # calculate totals for rejected energy and energy services
    rejected_energy_total_df = pd.DataFrame.from_dict(rejected_energy_dict, orient='index').transpose().sum(axis=1)
    energy_services_total_df = pd.DataFrame.from_dict(energy_services_dict, orient='index').transpose().sum(axis=1)

    # if total is True, only return total energy, rejected energy and energy services
    if total:
        df = total_df.copy()
    else:
        output_df = df[column_list]
        df = output_df.join(energy_value_df, how='outer')
        df = df.join(rejected_energy_df, how='outer')
        df = df.join(energy_services_df, how='outer')

    return df


def calc_energy_pws(data: pd.DataFrame, water_energy_types=None, fuel_types=None, pws_ibt_pct=.5, regions=3,
                    total=False):
    """calculates energy use, rejected energy, and energy services by fuel type for each public water supply energy
     application (e.g., pumping, distribution, treatment) by water type (e.g., fresh, saline), water source (e.g.,
     surface, groundwater), and fuel type (e.g., electricity, natural gas) in billion btu per year. Water type, water
     source, energy application, energy application intensity, fuel type, fuel efficiency by type, and percent of energy
     supplied by each fuel type are all customizable inputs. The function reads values provided for the described
     parameters and looks for the associated data column in the input dataframe in order to calculate energy demand,
     rejected energy, and energy services for each energy application. An example output would be electricity use in
    the treatment of saline surface water for public water supply by region. This function will use default values for
     water types, water source, energy applications, energy application intensities, fuel types, fuel efficiencies, and
     fuel type percentages unless other values are provided. The function returns all values calculated by default,
     for total values by energy application (e.g., total energy in distribution for public water supply by region),
     the parameter total must be set to True. Note that energy use in interbasin transfers for public water supply is
     not calculated from total public water supply input data but is assumed to be provided in bbtu per year by
     region.

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
                           'surfacewater': {'pumping': 145, 'treatment': 405, 'distribution': 1040}},
                      'saline':
                          {'groundwater': {'pumping': 920, 'treatment': 13805, 'distribution': 1040},
                           'surfacewater': {'pumping': 145, 'treatment': 14005, 'distribution': 1040}}}
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
                for fuel_type in fuel_type_dict:
                    df[f'{fuel_type}_pws_{energy_type}_bbtu'] = 0
                    df[f'{fuel_type}_pws_{energy_type}_energy_services_bbtu'] = 0
                    df[f'{fuel_type}_pws_{energy_type}_rejected_energy_bbtu'] = 0
                    df[f'{fuel_type}_pws_bbtu'] = 0

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
                        # calculate energy use
                        df[f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] = (df[flow_type] *
                                                                                                fuel_type_dict[
                                                                                                    fuel_type][
                                                                                                    'fuel_pct']) * 365 \
                                                                                               * convert_kwh_bbtu(
                            types_dict[water_type][
                                source_type][
                                energy_type])
                        # calculate energy services and rejected energy
                        if fuel_type_efficiency in df.columns:
                            df[f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu'] = df[
                                                                                                           f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                       * (1 - df[
                                fuel_type_efficiency])
                            df[f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu'] = df[
                                                                                                           f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                       * df[
                                                                                                           fuel_type_efficiency]
                        else:
                            df[f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu'] = df[
                                                                                                           f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                       * (1 -
                                                                                                          fuel_type_dict[
                                                                                                              fuel_type][
                                                                                                              'efficiency'])
                            df[f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu'] = df[
                                                                                                           f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu'] \
                                                                                                       * (
                                                                                                       fuel_type_dict[
                                                                                                           fuel_type][
                                                                                                           'efficiency'])

                        # add to totals
                        df[f'{fuel_type}_pws_{energy_type}_bbtu'] = df[f'{fuel_type}_pws_{energy_type}_bbtu'] + df[
                            f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu']

                        df[f'{fuel_type}_pws_{energy_type}_energy_services_bbtu'] = df[
                                                                                        f'{fuel_type}_pws_{energy_type}_energy_services_bbtu'] \
                                                                                    + df[
                                                                                        f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu']
                        df[f'{fuel_type}_pws_{energy_type}_rejected_energy_bbtu'] = df[
                                                                                        f'{fuel_type}_pws_{energy_type}_rejected_energy_bbtu'] \
                                                                                    + df[
                                                                                        f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu']

                        df[f'pws_total_energy_bbtu'] = df[f'pws_total_energy_bbtu'] + df[
                            f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu']
                        df[f'pws_total_energy_services_bbtu'] = df[f'pws_total_energy_services_bbtu'] \
                                                                + df[
                                                                    f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu']
                        df[f'pws_total_rejected_energy_bbtu'] = df[f'pws_total_rejected_energy_bbtu'] \
                                                                + df[
                                                                    f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu']

                        df[f'{fuel_type}_pws_bbtu'] = df[f'{fuel_type}_pws_bbtu'] + df[
                            f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu']

                        # add to retain list
                        retain_list.append(f'{fuel_type}_pws_{water_type}_{source_type}_{energy_type}_bbtu')
                        retain_list.append(f'pws_{water_type}_{source_type}_{energy_type}_rejected_energy_bbtu')
                        retain_list.append(f'pws_{water_type}_{source_type}_{energy_type}_energy_services_bbtu')

            else:
                pass

    for water_type in types_dict:
        for source_type in types_dict[water_type]:
            for energy_type in types_dict[water_type][source_type]:
                for fuel_type in fuel_type_dict:
                    if f'{fuel_type}_pws_bbtu' in total_list:
                        pass
                    else:
                        total_list.append(f'{fuel_type}_pws_bbtu')
                    if f'{fuel_type}_pws_{energy_type}_bbtu' in total_list:
                        pass
                    else:
                        total_list.append(f'{fuel_type}_pws_{energy_type}_bbtu')

                    if f'{fuel_type}_pws_{energy_type}_energy_services_bbtu' in total_list:
                        pass
                    else:
                        total_list.append(f'{fuel_type}_pws_{energy_type}_energy_services_bbtu')
                    if f'{fuel_type}_pws_{energy_type}_rejected_energy_bbtu' in total_list:
                        pass
                    else:
                        total_list.append(f'{fuel_type}_pws_{energy_type}_rejected_energy_bbtu')

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
            df['pws_total_ibt_rejected_energy_bbtu'] = df['pws_total_ibt_rejected_energy_bbtu'] + df[
                f'{fuel_type}_pws_ibt_rejected_energy_bbtu']
            df['pws_total_ibt_energy_services_bbtu'] = df['pws_total_ibt_energy_services_bbtu'] + df[
                f'{fuel_type}_pws_ibt_energy_services_bbtu']

            # add to total by fuel type
            df[f'{fuel_type}_pws_bbtu'] = df[f'{fuel_type}_pws_bbtu'] + df[f'{fuel_type}_pws_ibt_bbtu']

            # add columns to retained data list
            retain_list.append(f'{fuel_type}_pws_ibt_bbtu')
            retain_list.append(f'{fuel_type}_pws_ibt_rejected_energy_bbtu')
            retain_list.append(f'{fuel_type}_pws_ibt_energy_services_bbtu')

            # add columns to total list
            total_list.append(f'{fuel_type}_pws_ibt_bbtu')
            total_list.append(f'{fuel_type}_pws_ibt_rejected_energy_bbtu')
            total_list.append(f'{fuel_type}_pws_ibt_energy_services_bbtu')

            # add on to total energy
            df['pws_total_energy_bbtu'] = df['pws_total_energy_bbtu'] + df['pws_total_ibt_energy_bbtu']
            df['pws_total_energy_services_bbtu'] = df['pws_total_energy_services_bbtu'] + df[
                'pws_total_ibt_energy_services_bbtu']
            df['pws_total_rejected_energy_bbtu'] = df['pws_total_rejected_energy_bbtu'] + df[
                'pws_total_ibt_rejected_energy_bbtu']

        else:
            pass

    # add grand totals to output
    total_list.append('pws_total_energy_bbtu')
    total_list.append('pws_total_energy_services_bbtu')
    total_list.append('pws_total_rejected_energy_bbtu')

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


def calc_energy_production_exports(data: pd.DataFrame, sector_types=None, fuel_types=None, regions=3, total=False):
    """calculates total energy exports by region for each fuel type specified if production is greater than consumption.
    If production is less than consumption in a region, imports are calculated. Net exports are also calculated. Total
    consumption of each fuel type is used from the input data for specified sectors and additionally generated from the
    energy in public water supply, agriculture, and wastewater calculators.
        :param data:                        DataFrame of input data
        :type data:                         DataFrame

        :param sector_types:                A list of sectors that consume direct fuels that can be found in the input
                                            dataframe. Name must match variable naming in input dataset.
        :type sector_types:                 list

        :param fuel_types:                  A list of direct use fuel types that are produced and consumed. Name must
                                            match variable naming in input dataset.
        :type fuel_types:                   list

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

    if fuel_types is None:
        fuel_type_list = ['petroleum', 'natural_gas', 'biomass', 'coal']
    else:
        fuel_type_list = fuel_types

    if sector_types is None:
        sector_type_list = ['residential', 'commercial', 'industrial', 'transportation',
                            'pws', 'agriculture', 'wastewater']
    else:
        sector_type_list = sector_types

    # grab fuel consumption data from energy in agriculture and pws calculators
    pws_df = calc_energy_pws(data=df, total=True)
    ag_df = calc_energy_agriculture(data=df, total=True)
    wastewater_df = calc_energy_wastewater(data=df, total=True)

    # establish list of region columns to include in output
    region_list = df.columns[:regions].tolist()
    demand_df = df[region_list].copy()

    total_list = region_list.copy()

    # initialize values
    for fuel_type in fuel_type_list:
        demand_df[f'{fuel_type}_consumption_bbtu'] = 0

    # calculate total energy consumption of each fuel by region
    for fuel_type in fuel_type_list:
        if f'{fuel_type}_fuel_bbtu' in df.columns:
            demand_df[f'{fuel_type}_consumption_bbtu'] = demand_df[f'{fuel_type}_consumption_bbtu'] \
                                                               + df[f'{fuel_type}_fuel_bbtu']
            for sector_type in sector_type_list:
                if f'{fuel_type}_{sector_type}_bbtu' in df.columns:
                    demand_df[f'{fuel_type}_consumption_bbtu'] = demand_df[f'{fuel_type}_consumption_bbtu'] \
                                                                       + df[f'{fuel_type}_{sector_type}_bbtu']
                else:
                    pass
        else:
            pass

    # calculate energy consumption from pws, agriculture, and wastewater sectors
    for fuel_type in fuel_type_list:
        if f'{fuel_type}_pws_bbtu' in df.columns:
            pass
        else:
            if f'{fuel_type}_pws_bbtu' in pws_df.columns:
                demand_df[f'{fuel_type}_consumption_bbtu'] = demand_df[f'_{fuel_type}_consumption_bbtu'] \
                                                                   + pws_df[f'{fuel_type}_pws_bbtu']
            else:
                pass

        if f'{fuel_type}_agriculture_bbtu' in df.columns:
            pass
        else:
            if f'{fuel_type}_agriculture_bbtu' in ag_df.columns:
                demand_df[f'{fuel_type}_consumption_bbtu'] = demand_df[f'{fuel_type}_consumption_bbtu'] \
                                                                   + ag_df[f'{fuel_type}_agriculture_bbtu']
            else:
                pass

        if f'{fuel_type}_wastewater_bbtu' in df.columns:
            pass
        else:
            if f'{fuel_type}_wastewater_bbtu' in wastewater_df.columns:
                demand_df[f'{fuel_type}_consumption_bbtu'] = demand_df[f'{fuel_type}_consumption_bbtu'] \
                                                                   + wastewater_df[f'{fuel_type}_wastewater_bbtu']
            else:
                pass

# calculate exports, imports, and net exports
    for fuel_type in fuel_type_list:
        column_name = f'{fuel_type}_production_bbtu'
        demand_df[column_name] = df[column_name].copy()
        consumption_name = f'{fuel_type}_consumption_bbtu'
        production_name = f'{fuel_type}_production_bbtu'

        # exports
        demand_df[f'{fuel_type}_export_bbtu'] = np.where(demand_df[production_name] > demand_df[consumption_name],
                                                          demand_df[production_name] - demand_df[consumption_name],
                                                          0)
        # imports
        demand_df[f'{fuel_type}_import_bbtu'] = np.where(demand_df[production_name] < demand_df[consumption_name],
                                                          demand_df[consumption_name] - demand_df[production_name],
                                                          0)
        # net exports
        demand_df[f'{fuel_type}_net_export_bbtu'] = demand_df[f'{fuel_type}_export_bbtu'] \
                                                     - demand_df[f'{fuel_type}_import_bbtu']

        total_list.append(f'{fuel_type}_export_bbtu')
        total_list.append(f'{fuel_type}_import_bbtu')
        total_list.append(f'{fuel_type}_net_export_bbtu')

    if total:
        df = demand_df[total_list]
    else:
        df = demand_df

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


def aggregate(df_list=None, total=False, regions=3):
    print('loading baseline data...')
    data = co.configure_data()
    if df_list is None:
        df = data
        print('baseline dataset loaded...')
        print('----------')
        print('----------')
        print('starting calculations...')
        print('----------')
        if total:
            df1 = calc_electricity_rejected_energy(data=data, total=True)
            df2 = calc_sectoral_use_energy_discharge(data=data, total=True)
            df3 = calc_sectoral_use_water_discharge(data=data, total=True)
            df4 = calc_sector_water_exports(data=data, total=True)
            df5 = calc_energy_wastewater(data=data, total=True)
            df6 = calc_energy_agriculture(data=data, total=True)
            df7 = calc_energy_pws(data=data, total=True)
            df8 = calc_energy_production_exports(data=data, total=True)

        else:
            df1 = calc_electricity_rejected_energy(data=data)
            df2 = calc_sectoral_use_energy_discharge(data=data)
            df3 = calc_sectoral_use_water_discharge(data=data)
            df4 = calc_sector_water_exports(data=data)
            df5 = calc_energy_wastewater(data=data)
            df6 = calc_energy_agriculture(data=data)
            df7 = calc_energy_pws(data=data)
            df8 = calc_energy_production_exports(data=data)

        df_list = [df1, df2, df3, df4, df5, df6, df7, df8]
        i = 0
        region_list = df.columns[:regions].tolist()
        for item in df_list:
            for col in item.columns[3:]:
                pd.merge(df, item, how='left', on=region_list)
                print(col)

    else:
        df = data
        print('baseline dataset prepared')
        for item in df_list:
            df = pd.merge(df, item, how='left', on=['FIPS','State','County'])
            print(f'{item} calculation complete')
    print('----------')
    print('Calculations complete')

    return df