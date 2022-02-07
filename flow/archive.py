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

# WATER DISCHARGE FROM SECTORS
if sector_types is None:
    sector_consumption_dict = {'residential': {'groundwater': {'saline': 0, 'fresh': .3},
                                               'surfacewater': {'saline': 0, 'fresh': .3},
                                               'pws': {'fresh': .3}},
                               'commercial': {'groundwater': {'saline': 0, 'fresh': .15},
                                              'surfacewater': {'saline': 0, 'fresh': .15},
                                              'pws': {'fresh': .15}},
                               'industrial': {'groundwater': {'saline': .003, 'fresh': .15},
                                              'surfacewater': {'saline': .003, 'fresh': .15},
                                              'pws': {'fresh': .15}},
                               'mining': {'groundwater': {'saline': .03, 'fresh': .15},
                                          'surfacewater': {'saline': .03, 'fresh': .15}},
                               'crop_irrigation': {'groundwater': {'saline': 0, 'fresh': .3},
                                                   'surfacewater': {'saline': 0, 'fresh': .3}},
                               'livestock': {'groundwater': {'saline': 0, 'fresh': .87},
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

    ## TODO need to add different level updaters
    # for r in c_dict:
    #    for set in c_dict[r]:
    #        for type in c_dict[r][set]:
    #            #left split (need to add right split)
    #            if type == 'match':
    #                for t1 in c_dict[r][set][type]:
    #
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        t_total_name = f'{r}_{t1}_{u1}'
    #                                        t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                        t5_frac_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}_fraction'
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                            s5_total_name = f'{r}_{s1}_{u1}'
    #                                                            s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #
    #                                                            # calculate s fraction ( don't need frac function anymore)
    #                                                            #TODO next three lines need to be reworked to accomodate right split
    #                                                            t5_value = total_dict[t5_name]
    #                                                            #t5_total_value = total_dict[t_total_name]
    #                                                            #t5_fraction = t5_value/t5_total_value
    #
    #                                                            s5_value = total_dict[s5_name]
    #                                                            s5_total_value = total_dict[s5_total_name]
    #                                                            s5_fraction = s5_value/s5_total_value
    #
    #                                                            # calculate t5 amount * fraction
    #                                                            t5_split_value = t5_value * s5_fraction
    #
    #                                                            # if the flows are equal
    #                                                            if t5_split_value == s5_value:
    #                                                                l5_dict.update({t_s_5_name: t5_split_value})
    #
    #                                                            # if the inflow is greater
    #                                                            elif t5_split_value > s5_value:
    #                                                                l5_dict.update({t_s_5_name: s5_value})
    #                                                                export_value = t5_value - s5_value
    #                                                                export_dict.update({t5_name:export_value})
    #
    #                                                            # if the inflow is smaller
    #                                                            #TODO check if correct
    #                                                            else:
    #                                                                l5_dict.update({t_s_5_name: t5_split_value})
    #                                                                import_value = s5_value - t5_split_value
    #                                                                import_dict.update({s5_name: import_value})
    #            elif type == 'export':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                            if t5_name in export_dict:
    #                                                                flow_value = export_dict[t5_name]
    #                                                                l5_dict.update({t_s_5_name:flow_value})
    #                                                            else:
    #                                                                pass
    #            elif type == 'import':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                            if s5_name in import_dict:
    #                                                                flow_value = import_dict[s5_name]
    #                                                                l5_dict.update({t_s_5_name: flow_value})
    #                                                            else:
    #                                                                pass
    #            else:
    #                pass

    # TODO DROP loop == true
    # find any l5 to l5 and drop

    #    #TODO see if adding fraction components on both sides will remove the need for left/right split
    #    # one of the split should be equal to one

    # TODO add a function to remove flows
    #
    #
    #
    #    #        for t1 in f_dict[r][type]:
    #    #            for t2 in f_dict[r][type][t1]:
    #    #                for t3 in f_dict[r][type][t1][t2]:
    #                    for t4 in f_dict[r][type][t1][t2][t3]:
    #                        for t5 in f_dict[r][type][t1][t2][t3][t4]:
    #                            for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
    #                                for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
    #                                    for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                        for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                            for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                    l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                    if l5_name in l5_dict:
    #                                                        sum_dict.update({l5_name: l5_dict[l5_name]})
    #                                                    else:
    #                                                        pass

    ## create a dataframe to sum values by target to link disconnected nodes
    # sum_df = de.deconstruct_nested_dictionary(sum_dict)
    # group_column_list = ['region', 'T1','T2','T3','T4','T5','units']
    # sum_df = sum_df.groupby(group_column_list, as_index=False).sum()
    # for col in group_column_list[:-1]:
    #    sum_df[col] = sum_df[col] + '_'
    # sum_df['l5_sum_name'] = sum_df[group_column_list].sum(axis=1)
    # sum_dict = dict(zip(sum_df.l5_sum_name, sum_df.value))
    #
    # for r in c_dict:
    #    for set in c_dict[r]:
    #        for type in c_dict[r][set]:
    #            if type == 'build':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            l1_loop_name = f'{r}_{t1}_to_{t1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                l2_loop_name = f'{r}_{t1}_{t2}_to_{t1}_{t2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    l3_loop_name = f'{r}_{t1}_{t2}_{t3}_to_{t1}_{t2}_{t3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        l4_loop_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #
    #                                                            # anything that's left in the loop after subtracting earlier
    #                                                            # assign to new flow name
    #                                                            l5_loop_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                                            if l5_loop_name in l5_dict:
    #                                                                l5_loop_value = l5_dict[l5_loop_name]
    #                                                                l5_dict.update({t_s_5_name: l5_loop_value})
    #                                                                del l5_dict[l5_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l4_loop_name in l4_dict:
    #                                                                l4_loop_value = l4_dict[l4_loop_name]
    #                                                                l4_dict.update({t_s_4_name: l4_loop_value})
    #                                                                del l4_dict[l4_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l3_loop_name in l3_dict:
    #                                                                l3_loop_value = l3_dict[l3_loop_name]
    #                                                                l3_dict.update({t_s_3_name: l3_loop_value})
    #                                                                del l3_dict[l3_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l2_loop_name in l2_dict:
    #                                                                l2_loop_value = l2_dict[l2_loop_name]
    #                                                                l2_dict.update({t_s_2_name: l2_loop_value})
    #                                                                del l2_dict[l2_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l1_loop_name in l1_dict:
    #                                                                l1_loop_value = l1_dict[l1_loop_name]
    #                                                                l1_dict.update({t_s_1_name: l1_loop_value})
    #                                                                del l1_dict[l1_loop_name]
    #                                                            else:
    #                                                                pass
    #
    #
    #            elif type == 'match':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                        if t5_name in sum_dict:
    #                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                                t_s_1_value = 0
    #                                                l1_loop_name = f'{r}_{s1}_to_{s1}_{u1}'
    #                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                    t_s_2_value = 0
    #                                                    l2_loop_name = f'{r}_{s1}_{s2}_to_{s1}_{s2}_{u1}'
    #                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                        t_s_3_value = 0
    #                                                        l3_loop_name = f'{r}_{s1}_{s2}_{s3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                            t_s_4_value = 0
    #                                                            l4_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                                s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                if s5_name in total_dict:
    #                                                                    s5_fraction_name = s5_name + '_fraction'
    #                                                                    t5_split_value = sum_dict[t5_name] * fraction_dict[s5_fraction_name]
    #                                                                    flow_value = min(t5_split_value, total_dict[s5_name])
    #
    #                                                                    l5_dict.update({t_s_5_name: flow_value})
    #                                                                    t_s_4_value = t_s_4_value + flow_value
    #                                                                    t_s_3_value = t_s_3_value + flow_value
    #                                                                    t_s_2_value = t_s_2_value + flow_value
    #                                                                    t_s_1_value = t_s_1_value + flow_value
    #
    #                                                                    l4_dict.update({t_s_4_name: t_s_4_value})
    #                                                                    l3_dict.update({t_s_3_name: t_s_3_value})
    #                                                                    l2_dict.update({t_s_2_name: t_s_2_value})
    #                                                                    l1_dict.update({t_s_1_name: t_s_1_value})
    #
    #
    #                                                                    # save value to discharge dictionary
    #                                                                    discharge_dict.update({t5_name: flow_value})
    #
    #                                                                    #remove value from looped variable at all levels
    #                                                                    l5_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                    if l5_loop_name in l5_dict:
    #                                                                        l5_loop_value = l5_dict[l5_loop_name]
    #                                                                        if l5_loop_value - flow_value <= 0:
    #                                                                            l5_dict.update({l5_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l5_loop_value - flow_value
    #                                                                            l5_dict.update({l5_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l4_loop_name in l4_dict:
    #                                                                        l4_loop_value = l4_dict[l4_loop_name]
    #                                                                        if l4_loop_value - t_s_4_value <= 0:
    #                                                                            l4_dict.update({l4_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l4_loop_value - t_s_4_value
    #                                                                            l4_dict.update(
    #                                                                                {l4_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l3_loop_name in l3_dict:
    #                                                                        l3_loop_value = l3_dict[l3_loop_name]
    #                                                                        if l3_loop_value - t_s_3_value <= 0:
    #                                                                            l3_dict.update({l3_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l3_loop_value - t_s_3_value
    #                                                                            l3_dict.update(
    #                                                                                {l3_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l2_loop_name in l2_dict:
    #                                                                        l2_loop_value = l2_dict[l2_loop_name]
    #                                                                        if l2_loop_value - t_s_2_value <= 0:
    #                                                                            l2_dict.update({l2_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l2_loop_value - t_s_2_value
    #                                                                            l2_dict.update(
    #                                                                                {l2_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l1_loop_name in l1_dict:
    #                                                                        l1_loop_value = l1_dict[l1_loop_name]
    #                                                                        if l1_loop_value - t_s_1_value <= 0:
    #                                                                            l1_dict.update({l1_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l1_loop_value - t_s_1_value
    #                                                                            l1_dict.update(
    #                                                                                {l1_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #
    #
    #            elif type == 'replace':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            l1_loop_name = f'{r}_{s1}_to_{s1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                l2_loop_name = f'{r}_{s1}_{s2}_to_{s1}_{s2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    l3_loop_name = f'{r}_{s1}_{s2}_{s3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        l4_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #
    #                                                            # anything that's left in the loop after subtracting earlier
    #                                                            # assign to new flow name
    #                                                            l5_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                            if l5_loop_name in l5_dict:
    #                                                                l5_loop_value = l5_dict[l5_loop_name]
    #                                                                l5_dict.update({t_s_5_name: l5_loop_value})
    #                                                                del l5_dict[l5_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l4_loop_name in l4_dict:
    #                                                                l4_loop_value = l4_dict[l4_loop_name]
    #                                                                l4_dict.update({t_s_4_name: l4_loop_value})
    #                                                                del l4_dict[l4_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l3_loop_name in l3_dict:
    #                                                                l3_loop_value = l3_dict[l3_loop_name]
    #                                                                l3_dict.update({t_s_3_name: l3_loop_value})
    #                                                                del l3_dict[l3_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l2_loop_name in l2_dict:
    #                                                                l2_loop_value = l2_dict[l2_loop_name]
    #                                                                l2_dict.update({t_s_2_name: l2_loop_value})
    #                                                                del l2_dict[l2_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l1_loop_name in l1_dict:
    #                                                                l1_loop_value = l1_dict[l1_loop_name]
    #                                                                l1_dict.update({t_s_1_name: l1_loop_value})
    #                                                                del l1_dict[l1_loop_name]
    #                                                            else:
    #                                                                pass
    #
    #            elif type == 'surplus':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                        if t5_name in sum_dict:
    #                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                                l1_surplus_value = 0
    #                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                    l2_surplus_value = 0
    #                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                        l3_surplus_value = 0
    #                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                            l4_surplus_value = 0
    #                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                if t5_name in discharge_dict:
    #                                                                    discharge_value = discharge_dict[t5_name]
    #                                                                    inflow_value = sum_dict[t5_name]
    #                                                                    if discharge_value < inflow_value:
    #                                                                        l5_surplus_value = inflow_value - discharge_value
    #                                                                        l5_dict.update({t_s_5_name: l5_surplus_value})
    #
    #                                                                        l4_surplus_value = l4_surplus_value + l5_surplus_value
    #                                                                        l3_surplus_value = l3_surplus_value + l5_surplus_value
    #                                                                        l2_surplus_value = l2_surplus_value + l5_surplus_value
    #                                                                        l1_surplus_value = l1_surplus_value + l5_surplus_value
    #
    #                                                                        l4_dict.update({t_s_4_name: l4_surplus_value})
    #                                                                        l3_dict.update({t_s_3_name: l3_surplus_value})
    #                                                                        l2_dict.update({t_s_2_name: l2_surplus_value})
    #                                                                        l1_dict.update({t_s_1_name: l1_surplus_value})
    #
    #                                                                    else:
    #                                                                        pass
    #
    #            else:
    #                pass

    # TODO add updater that runs this, updates a copy of the data, reruns this
    # run.py function should run the updater and then deconstruct the output, take below

    calc_energy_sector_water:
    file1:
    name: 'energy_flow_targets'
    path: 'data/configuration_data/cesw_energy_flow_targets.csv'
file2:
name: 'energy_sector_water_split_fractions'
path: 'data/configuration_data/cesw_energy_sector_water_split_fractions.csv'

collect_water:
file1:
name: 'water_flow_targets'
path: 'data/configuration_data/cw_water_flow_targets.csv'

collect_energy:
file1:
name: 'energy_flow_targets'
path: 'data/configuration_data/ce_energy_flow_targets.csv'

calc_ww_water_demand:
file1:
name: 'water_flow_targets'
path: 'data/configuration_data/cwwd_water_flow_targets.csv'

calc_water_sector_water_demand:
file1:
name: 'water_flow_targets'
path: 'data/configuration_data/cwswd_water_flow_targets.csv'

calc_water_sector_energy:
file1:
name: 'water_flow_targets'
path: 'data/configuration_data/cwse_water_flow_targets.csv'
file2:
name: 'water_sector_energy_split_fractions'
path: 'data/configuration_data/cwse_water_sector_energy_split_fractions.csv'

update:
file1:
name: 'update_flow_data'
path: 'data/configuration_data/flow_value_updates.csv'



def read_cesw_energy_flow_targets():
    """Read in energy flow target data for calculating water in energy sector and output as DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_energy_sector_water', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cesw_energy_sector_water_split_fractions():
    """Read in water split data for calculating water sources to and discharges from the energy sector and output as a
    DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_energy_sector_water', 'file2')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cw_water_flow_targets():
    """Read in water flow target data for collecting water flows to non-energy sectors. Provides output as a DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('collect_water', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_ce_energy_flow_targets():
    """Read in energy flow target data for collecting energy flows to non-water sectors. Provides output as a DataFrame.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('collect_energy', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwwwd_water_flow_targets():
    """Read in water flow to wastewater target data.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_ww_water_demand', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwswd_water_flow_targets():
    """Read in water flows to water-sector data, not including wastewater sector.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_water_sector_water_demand', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwse_water_flow_targets():
    """Read in water_sector water target data and energy intensities.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_water_sector_energy', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_cwse_water_sector_energy_split_fractions():
    """Read in water sector energy split data to determine energy sources and energy discharge locations.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('calc_water_sector_energy', 'file2')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


def read_update_data():
    """Read in flow value update sets to update flow output and remove double counting.

        :return:                        dataframe of values

        """

    # collect path to file
    path = r.read_config('update_flow_data', 'file1')

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)



# TODO ###### BELOW TO BE DELETED #######
# TODO ######


def test_EP_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/EP_test_param.csv')

    return pd.read_csv(data)

def test_EP_flows():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_nested.csv')

    return pd.read_csv(data)

def test_collect_water_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_collect_water.csv')

    return pd.read_csv(data)

def test_collect_energy_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_collect_energy.csv')

    return pd.read_csv(data)

def test_ww_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/water_sector_params.csv')

    return pd.read_csv(data)

def test_water_sector_param():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_water_sector_water_param.csv')

    return pd.read_csv(data)

def test_water_sector_energy():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_water_sector_energy_param.csv')

    return pd.read_csv(data)

def test_water_sector_energy_discharge():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_water_sector_energy_discharge.csv')

    return pd.read_csv(data)


def test_update_data():
    """Read in .

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/test_updater.csv')

    return pd.read_csv(data)









def get_fuel_demand_target_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/EC_to_EG_Energy_Target_Parameters.csv')

    return pd.read_csv(data)

def get_water_demand_source_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/WS_to_PWS_and_NonWater_Source_Parameters.csv')

    return pd.read_csv(data)

def get_water_demand_target_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/WS_to_PWS_and_NonWater_Target_Parameters.csv')

    return pd.read_csv(data)

def get_electricity_dict():
    """Read in a dataframe of 2015 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/electricity_generation_dict.csv')

    return pd.read_csv(data)

def load_baseline_data():
    """Read in a dataframe of 2015 USGS Water Use Data.

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow', 'data/baseline_data.csv')

    return pd.read_csv(data)

def get_electricity_generation_efficiency_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/electricitygeneration_efficiency_parameters.csv')

    return pd.read_csv(data)

def get_sectoral_efficiency_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/sectoral_efficiency_parameters.csv')

    return pd.read_csv(data)

def get_sectoral_water_consumption_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/sector_water_consumption_fractions.csv')

    return pd.read_csv(data)



def get_sectoral_water_discharge_parameters():
    """Read in .

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/configuration_data/sector_water_discharge_fractions.csv')

    return pd.read_csv(data)






# Items below are for US sample data

def get_water_use_2015():
    """Read in a dataframe of 2015 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/usco2015v2.0.csv')

    return pd.read_csv(data, skiprows=1, dtype={'FIPS': str})


def get_water_use_1995():
    """Read in a dataframe of 1995 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/usco1995.csv')

    return pd.read_csv(data,  dtype={'StateCode': str, 'CountyCode': str})


def get_county_identifier_data():
    """Read in a dataframe of FIPS code - Interconnect crosswalk.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/county_interconnect_list.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data, dtype={'FIPS': str,'STATEFIPS': str })


def get_wastewater_flow_data():
    """Read in a dataframe of wastewater treatment facility water flows (MGD) by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Flow.csv')

    # read in wastewater treatment facility water flow data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_type_data():
    """Read in a dataframe of wastewater treatment facility type by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Type.csv')

    # read in wastewater treatment facility type data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_loc_data():
    """Read in a dataframe of wastewater treatment facility location by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Loc.csv')

    # read in wastewater treatment facility location data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_wastewater_facility_discharge_data():
    """Read in a dataframe of wastewater treatment facility discharge by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Discharge.csv')

    # read in wastewater treatment facility discharge data
    return pd.read_csv(data, dtype={'CWNS_NUMBER': str})


def get_electricity_generation_data():
    """Read in a dataframe of electricity generation by power plant

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow',
                                           'data/EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.csv')

    # read in wastewater treatment facility discharge data
    return pd.read_csv(data, skiprows=5)

def get_power_plant_county_data():
    """Read in a dataframe of power plant locations

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow',
                                           'data/EIA860_Generator_Y2015.csv')

    # read in data
    return pd.read_csv(data, skiprows=1, usecols= ['Plant Code', "State", 'County'])

def get_powerplant_primary_data():
    """Read in a dataframe of power plant primary generation type by power plant ID

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow',
                                           'data/eia_powerplant_primary_2020.csv')

    # read in data
    return pd.read_csv(data, usecols=['Plant_Code', "StateName", 'County', 'PrimSource'])


def get_powerplant_cooling_data():
    """Read in a dataframe water withdrawals and consumption for thermoelectric cooling by power plant ID

            :return:                        dataframe of values

            """

    data = pkg_resources.resource_filename('flow',
                                           'data/2015_TE_Model_Estimates_USGS.csv')

    # read in data
    return pd.read_csv(data, usecols=['EIA_PLANT_ID', "COUNTY", 'STATE', 'NAME_OF_WATER_SOURCE','GENERATION_TYPE',
                                      'COOLING_TYPE','WATER_SOURCE_CODE','WATER_TYPE_CODE', 'WITHDRAWAL',
                                      'CONSUMPTION'])

def get_irrigation_data():
    """Read in a dataframe of irrigation well depth, pressure, and pump fuel type by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/FRIS2013tab8.csv')

    # read in irrigation well depth, pressure, and pump fuel type data
    return pd.read_csv(data, skiprows=3)


def get_tx_inter_basin_transfer_data():
    """Read in a dataframe of Texas inter-basin transfer data by FIPS

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/TX_IBT_2015.csv')

    # read in Texas inter-basin transfer data by FIPS
    return pd.read_csv(data, dtype={'Used_FIPS': str, 'Source_FIPS': str})


def get_west_inter_basin_transfer_data():
    """Read in a dataframe of western inter-basin transfer data by FIPS

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/West_IBT_county.csv')

    # read in Texas inter-basin transfer data by FIPS
    return pd.read_csv(data, dtype={'FIPS': str})


def get_residential_electricity_demand_data():
    """Read in a dataframe of residential electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table6_Res.csv')

    # read in residential electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_commercial_electricity_demand_data():
    """Read in a dataframe of commercial electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table7_Com.csv')

    # read in commercial electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_industrial_electricity_demand_data():
    """Read in a dataframe of industrial electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table8_Ind.csv')

    # read in industrial electricity sales data
    return pd.read_csv(data, skiprows=2)


def get_transportation_electricity_demand_data():
    """Read in a dataframe of transportation electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/EIA_table9_Trans.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skiprows=2)

def get_state_electricity_demand_data():
    """Read in a dataframe of transportation electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia_861m_states.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skipfooter=2, engine='python',
                       dtype={'RESIDENTIAL': float, 'COMMERCIAL': float,
                              'INDUSTRIAL': float, 'TRANSPORTATION': float})

def get_territory_electricity_demand_data():
    """Read in a dataframe of transportation electricity sales data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia_861m_terr.csv')

    # read in transportation electricity sales data
    return pd.read_csv(data, skipfooter=1, engine='python',
                       dtype={'RESIDENTIAL': float, 'COMMERCIAL': float,
                              'INDUSTRIAL': float, 'TRANSPORTATION': float}
                       )

def get_fuel_demand_data():
    """Read in a dataframe of energy production (fuel) data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/use_all_btu.csv')

    # read in energy production (fuel) data
    return pd.read_csv(data)

def get_energy_production_data():
    """Read in a dataframe of energy production (fuel) data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia_SEDS_Prod_dataset.csv')

    # read in energy production (fuel) data
    return pd.read_csv(data, skiprows=1)


def get_corn_irrigation_data():
    """Read in a dataframe of corn irrigation for biomass data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/USDA_FRIS.csv')

    # read in corn irrigation data
    return pd.read_csv(data)


def get_corn_production_data():
    """Read in a dataframe of corn production for biomass data by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/USDA_NASS_CornProd_2015.csv')

    # read in corn irrigation data
    return pd.read_csv(data, dtype={'State ANSI': str, 'County ANSI': str, 'Value': float})


def get_county_oil_gas_production_data():
    """Read in a dataframe of oil and natural gas production by county

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/oilgascounty.csv')

    # read in county level oil and gas production data
    return pd.read_csv(data, dtype={'geoid': str})


def get_state_petroleum_production_data():
    """Read in a dataframe of oil production by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/petroleum_eia.csv')

    # read in state level petroleum production data
    return pd.read_csv(data, skiprows=4)


def get_state_gas_production_data():
    """Read in a dataframe of natural gas production by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/natgas_eia.csv')

    # read in read in state level natural gas production data
    return pd.read_csv(data, skiprows=4)


def get_unconventional_oil_gas_production_data():
    """Read in a dataframe of unconventional oil and natural gas production water use by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/Unconventional_Oil_NG_State.csv')

    # read in read in state level unconventional natural gas and oil production data
    return pd.read_csv(data)


def get_conventional_oil_water_intensity_data():
    """Read in a dataframe of conventional oil water intensity by state

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/PADD_intensity.csv')

    # read in read in state level water to oil intensity data
    return pd.read_csv(data)


def get_oil_gas_discharge_data():
    """Read in a dataframe of water discharge data from oil and natural gas production

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/Oil_NG_WOR_WGR.csv')

    # read in read in state level water discharge data from oil and natural gas
    return pd.read_csv(data)


def get_coal_production_data():
    """Read in a dataframe of coal production data

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/coalpublic2015.csv')

    # read in read in coal production data
    return pd.read_csv(data, skiprows=3)


def get_coal_mine_location_data():
    """Read in a dataframe of coal mine locations

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/Coal_Mine_Loc.csv')

    # read in read in coal mine data
    return pd.read_csv(data, dtype={'FIPS_CNTY_CD': str}, usecols=["MINE_ID", "STATE", "FIPS_CNTY_CD"])


def get_state_fips_data():
    """Read in a dataframe of state FIPS code by state abbreviation

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/State_FIPS_Code.csv')

    # read in read in state fips code to state abbrev. data
    return pd.read_csv(data, dtype={'State_FIPS': str})

def get_ethanol_location_data():
    """Read in a dataframe of state FIPS code by state abbreviation

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/eia819_ethanolcapacity_2015.csv')

    # read in read in state fips code to state abbrev. data
    return pd.read_csv(data, dtype={'FIPS': str}, skiprows=1)

