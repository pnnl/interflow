from .reader import *
import flow.construct as co


def collect_water_use(data=None, level=5, regions=3):
    """ Collects water demand flows provided in the baseline dataset for all sectors that do not have their total
    water demand dependent on their energy use (i.e., non-energy sectors). For example, residential water demand.
    Also determines discharge of water demand values (e.g., surface discharge) based on discharge fraction assumptions.

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

        :return:                            DataFrame of water demand flows and water discharge flows for non-energy
                                            sectors for each region.
        """

    # load baseline data
    if data:
        df = data
    else:
        df = read_baseline_data()

    # load water target and source inputs + discharge fractions and construct nested dictionary
    target_types = read_cw_water_flow_targets()
    split_dict = co.construct_nested_dictionary(target_types)

    # check for correct number of columns in parameter data
    if target_types.shape[1] != 14:
        m = 'Input water flow target parameter data does not have correct number of columns. Expects 14 columns.'
        raise ValueError(m)

    else:
        # initialize output dictionaries with region identifier data for each level from baseline dataset
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # loop through water target dictionary to collect water flows from baseline dataset
        for x1 in split_dict:  # level 1 target
            for x2 in split_dict[x1]:  # level 2 target
                for x3 in split_dict[x1][x2]:  # level 3 target
                    for x4 in split_dict[x1][x2][x3]:  # level 4 target
                        for x5 in split_dict[x1][x2][x3][x4]:  # level 5 target
                            for m_type in split_dict[x1][x2][x3][x4][x5]:  # movement type

                                # if the flow pair is a source flow
                                if m_type == 'source':
                                    # build source name
                                    for w_type in split_dict[x1][x2][x3][x4][x5][m_type]:  # water type
                                        l1_total_name = f'{x1}_{w_type}_mgd'
                                        l1_total_value = 0
                                        l2_total_name = f'{x1}_{x2}_{w_type}_mgd'
                                        l2_total_value = 0
                                        l3_total_name = f'{x1}_{x2}_{x3}_{w_type}_mgd'
                                        l3_total_value = 0
                                        l4_total_name = f'{x1}_{x2}_{x3}_{x4}_{w_type}_mgd'
                                        l4_total_value = 0
                                        l5_total_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_{w_type}_mgd'
                                        l5_total_value = 0

                                        # loop through water source levels
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type][w_type]:  # level 1 source
                                            l1_s_name = f'{s1}_to_{x1}_mgd'  # level 1 source name
                                            l1_s_value = 0  # initialize level 1 source flow value
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1]:
                                                l2_s_name = f'{s1}_{s2}_to_{x1}_{x2}_mgd'
                                                l2_s_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2]:
                                                    l3_s_name = f'{s1}_{s2}_{s3}_to_{x1}_{x2}_{x3}_mgd'
                                                    l3_s_value = 0
                                                    for s4 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][
                                                        s3]:
                                                        l4_s_name = f'{s1}_{s2}_{s3}_{s4}_to_{x1}_{x2}_{x3}_{x4}_mgd'
                                                        l4_s_value = 0
                                                        for s5 in \
                                                        split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4]:
                                                            l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{x1}_{x2}_{x3}_{x4}_{x5}_mgd'

                                                            # if the flow value (source to target) in baseline dataset
                                                            if l5_s_name in df.columns:
                                                                l5_s_value = df[l5_s_name]

                                                                # recalculate level total flow values
                                                                l4_s_value = l4_s_value + l5_s_value
                                                                l3_s_value = l3_s_value + l5_s_value
                                                                l2_s_value = l2_s_value + l5_s_value
                                                                l1_s_value = l1_s_value + l5_s_value

                                                                # calculate water total values (just target demand)
                                                                l5_total_value = l5_total_value + l5_s_value
                                                                l4_total_value = l4_total_value + l5_s_value
                                                                l3_total_value = l3_total_value + l5_s_value
                                                                l2_total_value = l2_total_value + l5_s_value
                                                                l1_total_value = l1_total_value + l5_s_value

                                                                # update level dictionaries with level 5 water flow
                                                                l1_dict.update({l1_s_name: l1_s_value})
                                                                l2_dict.update({l2_s_name: l2_s_value})
                                                                l3_dict.update({l3_s_name: l3_s_value})
                                                                l4_dict.update({l4_s_name: l4_s_value})
                                                                l5_dict.update({l5_s_name: l5_s_value})

                                                                # update level dictionaries with level 5 water totals
                                                                l1_dict.update({l1_total_name: l1_total_value})
                                                                l2_dict.update({l2_total_name: l2_total_value})
                                                                l3_dict.update({l3_total_name: l3_total_value})
                                                                l4_dict.update({l4_total_name: l4_total_value})
                                                                l5_dict.update({l5_total_name: l5_total_value})
                                else:
                                    pass

        # loop through target names and calculate water discharge
        for x1 in split_dict:  # level 1 target
            for x2 in split_dict[x1]:  # level 2 target
                for x3 in split_dict[x1][x2]:  # level 3 target
                    for x4 in split_dict[x1][x2][x3]:  # level 4 target
                        for x5 in split_dict[x1][x2][x3][x4]:  # level 5 target
                            for m_type in split_dict[x1][x2][x3][x4][x5]:  # movement type

                                # if the flow pair is a discharge flow
                                if m_type == 'discharge':

                                    # build water totals
                                    for w_type in split_dict[x1][x2][x3][x4][x5][m_type]:
                                        l1_total_name = f'{x1}_{w_type}_mgd'
                                        l2_total_name = f'{x1}_{x2}_{w_type}_mgd'
                                        l3_total_name = f'{x1}_{x2}_{x3}_{w_type}_mgd'
                                        l4_total_name = f'{x1}_{x2}_{x3}_{x4}_{w_type}_mgd'
                                        l5_total_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_{w_type}_mgd'

                                        # loop through discharge locations
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type][w_type]:  # level 1 discharge
                                            l1_d_name = f'{x1}_to_{s1}_mgd'  # level 1 discharge name
                                            l1_d_value = 0  # initialize level 1 discharge value
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1]:
                                                l2_d_name = f'{x1}_{x2}_to_{s1}_{s2}_mgd'
                                                l2_d_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2]:
                                                    l3_d_name = f'{x1}_{x2}_{x3}_to_{s1}_{s2}_{s3}_mgd'
                                                    l3_d_value = 0
                                                    for s4 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][
                                                        s3]:
                                                        l4_d_name = f'{x1}_{x2}_{x3}_{x4}_to_{s1}_{s2}_{s3}_{s4}_mgd'
                                                        l4_d_value = 0
                                                        for s5 in \
                                                        split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4]:
                                                            l5_d_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_mgd'

                                                            # if the total water to target was previously calculated
                                                            if l5_total_name in l5_dict:
                                                                # name of discharge fraction
                                                                frac_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_to_' \
                                                                            f'{s1}_{s2}_{s3}_{s4}_{s5}_fraction'
                                                                for p in \
                                                                split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][
                                                                    s3][s4][s5]:

                                                                    # if region-level fractions available
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]

                                                                    # otherwise use paramater input
                                                                    else:
                                                                        frac = \
                                                                        split_dict[x1][x2][x3][x4][x5][m_type][w_type][
                                                                            s1][s2][s3][s4][s5][p]

                                                                    # calculate discharge values at each level
                                                                    l5_d_value = l5_dict[l5_total_name] * frac
                                                                    l4_d_value = l4_dict[l4_total_name] * frac
                                                                    l3_d_value = l3_dict[l3_total_name] * frac
                                                                    l2_d_value = l2_dict[l2_total_name] * frac
                                                                    l1_d_value = l1_dict[l1_total_name] * frac
                                                                    l1_dict.update({l1_d_name: l1_d_value})
                                                                    l2_dict.update({l2_d_name: l2_d_value})
                                                                    l3_dict.update({l3_d_name: l3_d_value})
                                                                    l4_dict.update({l4_d_name: l4_d_value})
                                                                    l5_dict.update({l5_d_name: l5_d_value})
                                                            else:
                                                                pass
                                else:
                                    pass

        # convert output dictionaries to dataframes
        l1_df = pd.DataFrame.from_dict(l1_dict, orient='index').transpose()
        l2_df = pd.DataFrame.from_dict(l2_dict, orient='index').transpose()
        l3_df = pd.DataFrame.from_dict(l3_dict, orient='index').transpose()
        l4_df = pd.DataFrame.from_dict(l4_dict, orient='index').transpose()
        l5_df = pd.DataFrame.from_dict(l5_dict, orient='index').transpose()

        # return output at specified level of granularity
        if level == 1:
            df = l1_df
        elif level == 2:
            df = l2_df
        elif level == 3:
            df = l3_df
        elif level == 4:
            df = l4_df
        elif level == 5:
            df = l5_df
        else:
            m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
            raise ValueError(m)

        return df
