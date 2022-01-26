import numpy as np
import pandas as pd
from .reader import *
import flow.construct as co


def collect_energy_use(data=None, level=5, regions=3):
    """ Collects energy demand flows provided in the baseline dataset for all sectors that do not have their total
    energy demand dependent on their water use (i.e., non-water sectors). For example, natural gas energy demand by
    the residential sector or natural gas energy demand by natural gas electricity generation. Also determines discharge
    of energy demand values (e.g., rejected energy) based on efficiency assumptions.

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

        :return:                            DataFrame of energy demand flows and energy discharge flows for non-water
                                            sectors for each region.
        """

    # load baseline data
    if data:
        df = data
    else:
        df = read_baseline_data()

    # load energy target and source inputs + discharge fractions and construct nested dictionary
    target_types = read_ce_energy_flow_targets()
    split_dict = co.construct_nested_dictionary(target_types)

    # check for correct number of columns in parameter data
    if target_types.shape[1] != 13:
        m = 'Input source parameter data does not have correct number of columns'
        raise ValueError(m)

    else:
        # initialize output dictionaries with region identifier data for each level from baseline dataset
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # loop through energy target dictionary to collect energy flows from baseline dataset
        for x1 in split_dict:  # level 1 target
            for x2 in split_dict[x1]:  # level 2 target
                for x3 in split_dict[x1][x2]:  # level 3 target
                    for x4 in split_dict[x1][x2][x3]:  # level 4 target
                        for x5 in split_dict[x1][x2][x3][x4]:  # level 5 target
                            for m_type in split_dict[x1][x2][x3][x4][x5]:  # movement type

                                # if the flow pair is a source flow
                                if m_type == 'source':

                                    # build energy total names by for target levels
                                    l1_total_name = f'{x1}_bbtu'
                                    l1_total_value = 0
                                    l2_total_name = f'{x1}_{x2}_bbtu'
                                    l2_total_value = 0
                                    l3_total_name = f'{x1}_{x2}_{x3}_bbtu'
                                    l3_total_value = 0
                                    l4_total_name = f'{x1}_{x2}_{x3}_{x4}_bbtu'
                                    l4_total_value = 0
                                    l5_total_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_bbtu'
                                    l5_total_value = 0

                                    # loop through source names and build source-to-target names
                                    for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:  # level 1 source
                                        l1_s_name = f'{s1}_to_{x1}_mgd'  # create level 1 source to target flow name
                                        l1_s_value = 0  # initialize level 1 source to target flow value
                                        for s2 in split_dict[x1][x2][x3][x4][x5][m_type][s1]:
                                            l2_s_name = f'{s1}_{s2}_to_{x1}_{x2}_bbtu'
                                            l2_s_value = 0
                                            for s3 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2]:
                                                l3_s_name = f'{s1}_{s2}_{s3}_to_{x1}_{x2}_{x3}_bbtu'
                                                l3_s_value = 0
                                                for s4 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3]:
                                                    l4_s_name = f'{s1}_{s2}_{s3}_{s4}_to_{x1}_{x2}_{x3}_{x4}_bbtu'
                                                    l4_s_value = 0
                                                    for s5 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4]:
                                                        l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{x1}_{x2}_{x3}_{x4}_{x5}_bbtu'

                                                        # if the source to target flow name is in the baseline data
                                                        if l5_s_name in df.columns:
                                                            l5_s_value = df[l5_s_name]

                                                            # update source to target flow values across levels
                                                            l4_s_value = l4_s_value + l5_s_value
                                                            l3_s_value = l3_s_value + l5_s_value
                                                            l2_s_value = l2_s_value + l5_s_value
                                                            l1_s_value = l1_s_value + l5_s_value

                                                            # update total target energy values across levels
                                                            l5_total_value = l5_total_value + l5_s_value
                                                            l4_total_value = l4_total_value + l5_s_value
                                                            l3_total_value = l3_total_value + l5_s_value
                                                            l2_total_value = l2_total_value + l5_s_value
                                                            l1_total_value = l1_total_value + l5_s_value

                                                            # update dictionaries with source to target flow values
                                                            l1_dict.update({l1_s_name: l1_s_value})
                                                            l2_dict.update({l2_s_name: l2_s_value})
                                                            l3_dict.update({l3_s_name: l3_s_value})
                                                            l4_dict.update({l4_s_name: l4_s_value})
                                                            l5_dict.update({l5_s_name: l5_s_value})

                                                            # update dictionaries with target energy values
                                                            l1_dict.update({l1_total_name: l1_total_value})
                                                            l2_dict.update({l2_total_name: l2_total_value})
                                                            l3_dict.update({l3_total_name: l3_total_value})
                                                            l4_dict.update({l4_total_name: l4_total_value})
                                                            l5_dict.update({l5_total_name: l5_total_value})
                                else:
                                    pass

        # create target names by looping through dictionary
        for x1 in split_dict:
            for x2 in split_dict[x1]:
                for x3 in split_dict[x1][x2]:
                    for x4 in split_dict[x1][x2][x3]:
                        for x5 in split_dict[x1][x2][x3][x4]:
                            for m_type in split_dict[x1][x2][x3][x4][x5]:

                                # if the flow pair is a discharge flow
                                if m_type == 'discharge':

                                        # create total target energy names to match to prior calculations
                                        l1_total_name = f'{x1}_bbtu'
                                        l2_total_name = f'{x1}_{x2}_bbtu'
                                        l3_total_name = f'{x1}_{x2}_{x3}_bbtu'
                                        l4_total_name = f'{x1}_{x2}_{x3}_{x4}_bbtu'
                                        l5_total_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_bbtu'

                                        # build discharge names for target to discharge flows
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:  # level 1 discharge
                                            l1_d_name = f'{x1}_to_{s1}_bbtu'  # level 1 discharge name
                                            l1_d_value = 0  # initialize level 1 discharge value
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][s1]:
                                                l2_d_name = f'{x1}_{x2}_to_{s1}_{s2}_bbtu'
                                                l2_d_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2]:
                                                    l3_d_name = f'{x1}_{x2}_{x3}_to_{s1}_{s2}_{s3}_bbtu'
                                                    l3_d_value = 0
                                                    for s4 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3]:
                                                        l4_d_name = f'{x1}_{x2}_{x3}_{x4}_to_{s1}_{s2}_{s3}_{s4}_bbtu'
                                                        l4_d_value = 0
                                                        for s5 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4]:
                                                            l5_d_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_bbtu'

                                                            # if the target total energy value was previously calculated
                                                            if l5_total_name in l5_dict:

                                                                # calculate discharge amount
                                                                for p in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5]:
                                                                    frac_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_fraction'

                                                                    # if discharge fraction is available at region-level
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]

                                                                    # Otherwise apply dictionary value
                                                                    else:
                                                                        frac = split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5][p]

                                                                    # calculate target to discharge flow values
                                                                    l5_d_value = l5_dict[l5_total_name] * frac
                                                                    l4_d_value = l4_dict[l4_total_name] * frac
                                                                    l3_d_value = l3_dict[l3_total_name] * frac
                                                                    l2_d_value = l2_dict[l2_total_name] * frac
                                                                    l1_d_value = l1_dict[l1_total_name] * frac

                                                                    # update dictionaries with target to discharge flows
                                                                    l1_dict.update({l1_d_name: l1_d_value})
                                                                    l2_dict.update({l2_d_name: l2_d_value})
                                                                    l3_dict.update({l3_d_name: l3_d_value})
                                                                    l4_dict.update({l4_d_name: l4_d_value})
                                                                    l5_dict.update({l5_d_name: l5_d_value})
                                                            else:
                                                                pass
                                else:
                                    pass

        # convert output dictionaries to dataframe
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
