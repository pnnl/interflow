from .reader import *
import flow.construct as co
import flow.calc_energy_sector_water as esw
import flow.collect_water as cw
import flow.collect_energy as ce
import flow.calc_ww_water_demand as wwd
import flow.calc_water_sector_water_demand as ws
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
        df = read_baseline_data()

    # construct a copy of the baseline dataset
    df_updated = df.copy()

    # run water and energy flow calculations for each sector and combine output
    d1 = esw.calc_energy_sector_water_demand()
    d2 = cw.collect_water_use()
    d3 = ce.collect_energy_use()
    d4 = wwd.calc_wastewater_water_demand()
    d5 = ws.calc_water_sector_water()
    d6 = wse.calc_water_sector_energy_demand()

    # merge outputs from each run into a single DataFrame
    calc_df = d1
    rem_list = [d2, d3, d4,d5 ,d6]
    for item in rem_list:
        calc_df = pd.merge(calc_df, item, how='left', on = df.columns[:regions].tolist())

    # read in flow source to target pairs to update and convert to nested dictionary
    update_file = read_update_data()
    t_dict = co.construct_nested_dictionary(update_file)

    # check that input data has correct number of columns
    if t_dict.shape[1] != 14:
        m = 'Input source parameter data does not have correct number of columns'
        raise ValueError(m)
    else:
        # initialize output dictionary with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()

        # loop through update pairs to determine appropriate updates
        for set_num in t_dict:  # set number

            # loop through target names
            for t1 in t_dict[set_num]:  # level 1 target
                for t2 in t_dict[set_num][t1]:
                    for t3 in t_dict[set_num][t1][t2]:
                        for t4 in t_dict[set_num][t1][t2][t3]:
                            for t5 in t_dict[set_num][t1][t2][t3][t4]:

                                # loop through source names
                                for s1 in t_dict[set_num][t1][t2][t3][t4][t5]:
                                    for s2 in t_dict[set_num][t1][t2][t3][t4][t5][s1]:
                                        for s3 in t_dict[set_num][t1][t2][t3][t4][t5][s1][s2]:
                                            for s4 in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3]:
                                                for s5 in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3][s4]:
                                                    for units in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3][s4][s5]:
                                                        for calc_type in t_dict[set_num][t1][t2][t3][t5][s1][s2][s3][s4][s5][units]:
                                                            # if the flow is a keep flow type
                                                            if calc_type == 'keep':
                                                                # construct keep flow name
                                                                l5_keep_t_name = f'{t1}_{t2}_{t3}_{t4}_{t5}'
                                                                l5_keep_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_{units}'
                                                                l5_keep_name = l5_keep_t_name + '_to_' + l5_keep_s_name

                                                                # if the keep flow name is in the calculated run output
                                                                if l5_keep_name in calc_df:
                                                                    # collect value
                                                                    l5_keep_value = calc_df[l5_keep_name]

                                                                    # assign new name associated with set number
                                                                    l5_keep_name = f'{set_num}_keep'

                                                                    # update dictionary with name and value
                                                                    l5_dict.update({l5_keep_name: l5_keep_value})
                                                                else:
                                                                    pass

                                                            # if the flow type is a removal
                                                            elif calc_type == 'remove':
                                                                # create removal flow name
                                                                l5_rem_t_name = f'{t1}_{t2}_{t3}_{t4}_{t5}'
                                                                l5_rem_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_{units}'
                                                                l5_rem_name = l5_rem_t_name + '_to_' + l5_rem_s_name

                                                                # if the removal flow name is in the baseline data copy
                                                                if l5_rem_name in df_updated.columns:
                                                                    # rebuild associated keep name
                                                                    keep_name = f'{set_num}_keep'
                                                                    # if the keep name is in the output dictionary
                                                                    if keep_name in l5_dict:
                                                                        # grab keep value from output dictionary
                                                                        remove_value = l5_dict[keep_name]
                                                                        # grab original value from baseline data copy
                                                                        original_value = df_updated[l5_rem_name]

                                                                        # update baseline data copy with the difference
                                                                        df_updated[l5_rem_name] = original_value \
                                                                                                  - remove_value
                                                                    else:
                                                                        pass
                                                                else:
                                                                    pass

    # rerun updated baseline data through water and energy flow calculations
    d1 = esw.calc_energy_sector_water_demand(data=df_updated, level=level, regions=regions)
    d2 = cw.collect_water_use(data=df_updated, level=level, regions=regions)
    d3 = ce.collect_energy_use(data=df_updated, level=level, regions=regions)
    d4 = wwd.calc_wastewater_water_demand(data=df_updated, level=level, regions=regions)
    d5 = ws.calc_water_sector_water(data=df_updated, level=level, regions=regions)
    d6 = wse.calc_water_sector_energy_demand(data=df_updated, level=level, regions=regions)

    # merge output from all runs into single output file
    out_df = d1.copy()
    rem_list = [d2, d3, d4, d5, d6]
    for item in rem_list:
        out_df = pd.merge(out_df, item, how='left', on=df.columns[:regions].tolist())

    return out_df
