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

    # load data
    if data:
        df = data
    else:
        df = read_baseline_data()

    # get input parameters for fuel types, sub_fuel_types, and associated efficiency ratings and change to nested dict
    target_types = read_ce_energy_flow_targets()
    split_dict = co.construct_nested_dictionary(target_types)

    if target_types.shape[1] > 15:
        raise ValueError('Input source parameter data does not have correct number of levels')

    elif target_types.shape[1] > 20:
        raise ValueError('Input target parameter data does not have correct number of levels')

    else:
        # initialize output dictionaries with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # grab production values, calculate water values
        for x1 in split_dict:
            for x2 in split_dict[x1]:
                for x3 in split_dict[x1][x2]:
                    for x4 in split_dict[x1][x2][x3]:
                        for x5 in split_dict[x1][x2][x3][x4]:
                            for m_type in split_dict[x1][x2][x3][x4][x5]:
                                if m_type == 'source':
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:
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

                                            l1_s_name = f'{s1}_to_{x1}_mgd'
                                            l1_s_value = 0
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

                                                            if l5_s_name in df.columns:
                                                                l5_s_value = df[l5_s_name]

                                                                # calculate specific values
                                                                l4_s_value = l4_s_value + l5_s_value
                                                                l3_s_value = l3_s_value + l5_s_value
                                                                l2_s_value = l2_s_value + l5_s_value
                                                                l1_s_value = l1_s_value + l5_s_value

                                                                # calculate total values
                                                                l5_total_value = l5_total_value + l5_s_value
                                                                l4_total_value = l4_total_value + l5_s_value
                                                                l3_total_value = l3_total_value + l5_s_value
                                                                l2_total_value = l2_total_value + l5_s_value
                                                                l1_total_value = l1_total_value + l5_s_value

                                                                l1_dict.update({l1_s_name: l1_s_value})
                                                                l2_dict.update({l2_s_name: l2_s_value})
                                                                l3_dict.update({l3_s_name: l3_s_value})
                                                                l4_dict.update({l4_s_name: l4_s_value})
                                                                l5_dict.update({l5_s_name: l5_s_value})

                                                                l1_dict.update({l1_total_name: l1_total_value})
                                                                l2_dict.update({l2_total_name: l2_total_value})
                                                                l3_dict.update({l3_total_name: l3_total_value})
                                                                l4_dict.update({l4_total_name: l4_total_value})
                                                                l5_dict.update({l5_total_name: l5_total_value})
                                else:
                                    pass

        # grab production values, calculate water values
        for x1 in split_dict:
            for x2 in split_dict[x1]:
                for x3 in split_dict[x1][x2]:
                    for x4 in split_dict[x1][x2][x3]:
                        for x5 in split_dict[x1][x2][x3][x4]:
                            for m_type in split_dict[x1][x2][x3][x4][x5]:
                                if m_type == 'discharge':
                                        l1_total_name = f'{x1}_bbtu'
                                        l2_total_name = f'{x1}_{x2}_bbtu'
                                        l3_total_name = f'{x1}_{x2}_{x3}_bbtu'
                                        l4_total_name = f'{x1}_{x2}_{x3}_{x4}_bbtu'
                                        l5_total_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_bbtu'

                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:
                                            l1_d_name = f'{x1}_to_{s1}_bbtu'
                                            l1_d_value = 0
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
                                                            if l5_total_name in l5_dict:

                                                                for p in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5]:
                                                                    frac_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_fraction'
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]
                                                                    else:
                                                                        frac = split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5][p]
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



       # convert output dictionaries to dataframe, merge with location information
        l1_df = pd.DataFrame.from_dict(l1_dict, orient='index').transpose()
        l2_df = pd.DataFrame.from_dict(l2_dict, orient='index').transpose()
        l3_df = pd.DataFrame.from_dict(l3_dict, orient='index').transpose()
        l4_df = pd.DataFrame.from_dict(l4_dict, orient='index').transpose()
        l5_df = pd.DataFrame.from_dict(l5_dict, orient='index').transpose()

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
