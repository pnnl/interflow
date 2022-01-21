#def calc_electricity_rejected_energy(data: pd.DataFrame, generation_types=None, regions=3,
#                                         generation_efficiency=.30, total=False):
#
#    for type in generation_type_list:
#        fuel_type = type + "_fuel_bbtu"
#        gen_type = type + "_gen_bbtu"
#
#        if (fuel_type in df.columns) and (gen_type in df.columns):
#            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] - df[gen_type]
#            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
#                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
#            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
#        elif (fuel_type in df.columns) and (gen_type not in df.columns):
#            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 - generation_efficiency)
#            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
#                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
#            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
#        elif (fuel_type not in df.columns) and (gen_type in df.columns):
#            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 / (1 - generation_efficiency))
#            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
#                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
#            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
#
#        else:
#            df[f'electricity_{type}_rejected_energy_bbtu'] = 0
#            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
#                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
#
#    if total:
#        column_list = df.columns[:regions].tolist()
#        column_list.append('electricity_rejected_energy_bbtu')
#        df = df[column_list]
#    else:
#        column_list = df.columns[:regions].tolist()
#        for item in retain_list:
#            column_list.append(item)
#        column_list.append('electricity_rejected_energy_bbtu')
#        df = df[column_list]
#
#    return df
#
#
#
#    # sectoral use energy discharges
#
#
#    # loop through each sector + fuel pair and calculate rejected energy and energy services if in dataset
#    retain_list = []
#    total_list = []
#    for sector_type in sector_type_dict:
#        df[f'{sector_type}_total_rejected_energy_bbtu'] = 0
#        df[f'{sector_type}_total_energy_services_bbtu'] = 0
#
#        for fuel_type in fuel_type_list:
#            fuel_demand_type = fuel_type + "_" + sector_type + "_bbtu"
#            if fuel_demand_type in df.columns:
#                df[f'{sector_type}_{fuel_type}_rejected_energy_bbtu'] = df[fuel_demand_type] \
#                                                                        * (1 - sector_type_dict[sector_type])
#
#                df[f'{sector_type}_{fuel_type}_energy_services_bbtu'] = df[fuel_demand_type] \
#                                                                        * (sector_type_dict[sector_type])
#
#                retain_list.append(f'{sector_type}_{fuel_type}_rejected_energy_bbtu')
#                retain_list.append(f'{sector_type}_{fuel_type}_energy_services_bbtu')
#
#                df[f'{sector_type}_total_rejected_energy_bbtu'] = df[f'{sector_type}_total_rejected_energy_bbtu'] \
#                                                                  + df[
#                                                                      f'{sector_type}_{fuel_type}_rejected_energy_bbtu']
#            else:
#                pass
#
#        retain_list.append(f'{sector_type}_total_rejected_energy_bbtu')
#        total_list.append(f'{sector_type}_total_rejected_energy_bbtu')
#
#    # establish list of region columns to include in output
#    column_list = df.columns[:regions].tolist()
#
#    # if total is True, only return total rejected energy and energy services by sector
#    if total:
#        for item in total_list:
#            column_list.append(item)
#        df = df[column_list]
#    else:
#        for item in retain_list:
#            column_list.append(item)
#        df = df[column_list]
#
#    return df
#