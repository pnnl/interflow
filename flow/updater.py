import numpy as np
import pandas as pd
from .reader import *
import flow.clean as cl
import flow.configure as conf
import flow.construct as co
import calc_water_in_energy as esw
import flow.collect_water as cw
import flow.collect_energy as ce
import flow.calc_ww_water_demand as wwd
import flow.calc_water_sector_water_totals as ws
import flow.calc_water_sector_energy as wse


def calculate_flows_and_updates(data=None, level=5, regions=3):
    """Runs energy and water calculations for each region and then reruns calculations to remove double counting.

        :param data:                        dataframe of baseline values to run calculations off of. Default is set to
                                            baseline dataframe specified in configuration.
        :type data:                         DataFrame

        :param level:                       Specifies what level of granularity to provide results. Must be an integer
                                            between 1 and 5, inclusive. Level 5 is the highest granularity, showing
                                            results down to the 5th level of specificity in each sector. Level 1 is the
                                            lowest level of granularity, showing results summed to the major sector
                                            level.
        :type level:                        int

        :param regions:                     The number of columns (inclusive) in the baseline dataset that include
                                            region identifiers (e.g. "Country", "State"). Reads from the first column
                                            in the dataframe onwards. Is used to combine various datasets to match
                                            values to each region included. Default number of regions is set to 3.
        :type regions:                      int

        :return:                            DataFrame of calculated water and energy sector flow values by region at
                                            specified level of granularity (see 'level' parameter)

        """

    # load baseline data
    if data:
        df = data
    else:
        df = test_baseline()    # TODO unlock this later when the load_baseline_data is hooked up to a data reader

    # construct a copy of the baseline dataset to update
    df_updated = df.copy()

    # run calculations for each sector and combine ouptut
    d1 = esw.calc_energy_direct_demand_water_use()
    d2 = cw.calc_collect_water_use()
    d3 = ce.calc_collect_energy_use()
    d4 = wwd.calc_wastewater_water_demand()
    d5 = ws.calc_water_sector_water()
    d6 = wse.calc_water_sector_energy()

    calc_df = d1
    rem_list = [d2,d3,d4,d5,d6]
    for item in rem_list:
        calc_df = pd.merge(calc_df, item, how='left', on = df.columns[:regions].tolist())

    update_file = test_update_data()
    t_dict = co.construct_nested_dictionary(update_file)

    if t_dict.shape[1] > 15:
        raise ValueError('Input source parameter data does not have correct number of levels')

    elif t_dict.shape[1] > 20:
        raise ValueError('Input target parameter data does not have correct number of levels')

    else:
        # initialize output dictionaries with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # use collected and estimated water values and associated intensities to calculate energy
        for set_num in t_dict:  # WWD
            for t1 in t_dict[set_num]:
                for t2 in t_dict[set_num][t1]:
                    for t3 in t_dict[set_num][t1][t2]:
                        for t4 in t_dict[set_num][t1][t2][t3]:
                            for t5 in t_dict[set_num][t1][t2][t3][t4]:
                                for s1 in t_dict[set_num][t1][t2][t3][t4][t5]:
                                    for s2 in t_dict[set_num][t1][t2][t3][t4][t5][s1]:
                                        for s3 in t_dict[set_num][t1][t2][t3][t4][t5][s1][s2]:
                                            for s4 in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3]:
                                                for s5 in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3][s4]:
                                                    for units in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3][s4][s5]:
                                                        for calc_type in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3][s4][s5][units]:
                                                            if calc_type == 'keep':
                                                                l5_keep_t_name = f'{t1}_{t2}_{t3}_{t4}_{t5}'
                                                                l5_keep_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_{units}'
                                                                l5_keep_name = l5_keep_t_name + '_to_' + l5_keep_s_name
                                                                if l5_keep_name in calc_df:
                                                                    l5_keep_value = calc_df[l5_keep_name]
                                                                    l5_keep_name = f'{set_num}_keep'
                                                                    l5_dict.update({l5_keep_name: l5_keep_value})
                                                                else:
                                                                    pass
                                                            elif calc_type == 'remove':
                                                                l5_rem_t_name = f'{t1}_{t2}_{t3}_{t4}_{t5}'
                                                                l5_rem_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_{units}'
                                                                l5_rem_name = l5_rem_t_name + '_to_' + l5_rem_s_name
                                                                if l5_rem_name in df_updated.columns:
                                                                    remove_name = f'{set_num}_keep'
                                                                    if remove_name in l5_dict:
                                                                        remove_value = l5_dict[remove_name]
                                                                        original_value  = df_updated[l5_rem_name]
                                                                        df_updated[l5_rem_name] = original_value \
                                                                                                  - remove_value
                                                                    else:
                                                                        pass
                                                                else:
                                                                    pass

    #rerun updated baseline data through functions

    d1 = esw.calc_energy_direct_demand_water_use(data=df_updated, level=level, regions=regions)
    d2 = cw.calc_collect_water_use(data=df_updated, level=level, regions=regions)
    d3 = ce.calc_collect_energy_use(data=df_updated, level=level, regions=regions)
    d4 = wwd.calc_wastewater_water_demand(data=df_updated, level=level, regions=regions)
    d5 = ws.calc_water_sector_water(data=df_updated, level=level, regions=regions)
    d6 = wse.calc_water_sector_energy(data=df_updated, level=level, regions=regions)

    out_df = d1.copy()
    rem_list = [d2, d3, d4, d5, d6]
    for item in rem_list:
        out_df = pd.merge(out_df, item, how='left', on=df.columns[:regions].tolist())

        return out_df
