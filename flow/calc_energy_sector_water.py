import numpy as np
import pandas as pd
from .reader import *
import flow.construct as co


def calc_energy_sector_water_demand(data=None, level=5, regions=3):
    """ Collects energy flows to energy sectors (sectors whose water demand is dependent on their energy) from baseline
    dataset and calculates total water withdrawn and produced (if applicable) based on assumed water intensity
    coefficients. Total water withdrawal and production values are then 1) split by water source based on provided water
    source fractions to determine water flows into the energy sectors and 2) split by water discharge locations based
    on provided discharge fractions to determine water flows from energy sectors. Calculations are conducted for each
    region provided in the baseline dataset.

        :param data:                        dataframe of baseline values to run calculations off of. Default is set to
                                            baseline dataframe specified in configuration file.
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

    # load energy target + water intensity parameters and construct nested dictionary
    energy_targets = read_cesw_energy_flow_targets()
    t_dict = co.construct_nested_dictionary(energy_targets)

    # load water split parameters and construct nested dictionary
    split_types = read_cesw_energy_sector_water_split_fractions()
    split_dict = co.construct_nested_dictionary(split_types)

    # check for correct number of columns in parameter data
    if energy_targets.shape[1] != 12:
        m = 'Input energy flow target parameter data does not have correct number of columns. Expects 12 columns.'
        raise ValueError(m)

    elif split_types.shape[1] != 14:
        m = 'Input water split parameter data does not have correct number of columns. Expects 14 columns.'
        raise ValueError(m)

    else:

        # initialize output dictionaries with region identifier data for each level from baseline dataset
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # loop through energy target dictionary to collect energy flows from baseline and calculate water
        for t1 in t_dict:  # level 1 target
            l1_w_name = f'{t1}_withdrawal_mgd'  # level 1 water withdrawal name
            l1_w_value = 0  # initialize level 1 water withdrawal value
            l1_p_name = f'{t1}_produced_mgd'  # level 2 produced water name
            l1_p_value = 0  # initialize level 2 produced water value

            for t2 in t_dict[t1]:  # level 2 target
                l2_w_name = f'{t1}_{t2}_withdrawal_mgd'
                l2_w_value = 0
                l2_p_name = f'{t1}_{t2}_produced_mgd'
                l2_p_value = 0

                for t3 in t_dict[t1][t2]:  # level 3 target
                    l3_w_name = f'{t1}_{t2}_{t3}_withdrawal_mgd'
                    l3_w_value = 0
                    l3_p_name = f'{t1}_{t2}_{t3}_produced_mgd'
                    l3_p_value = 0

                    for t4 in t_dict[t1][t2][t3]:  # level 4 target
                        l4_w_name = f'{t1}_{t2}_{t3}_{t4}_withdrawal_mgd'
                        l4_w_value = 0
                        l4_p_name = f'{t1}_{t2}_{t3}_{t4}_produced_mgd'
                        l4_p_value = 0

                        for t5 in t_dict[t1][t2][t3][t4]:  # level 5 target

                            # construct energy flow names and values to retrieve from baseline data
                            for s1 in t_dict[t1][t2][t3][t4][t5]:
                                l1_ep_name = f'{s1}_to_{t1}_bbtu'  # level 1 energy flow name
                                l1_ep_value = 0  # initialize level 1 energy flow value
                                for s2 in t_dict[t1][t2][t3][t4][t5][s1]:
                                    l2_ep_name = f'{s1}_{s2}_to_{t1}_{t2}_bbtu'
                                    l2_ep_value = 0
                                    for s3 in t_dict[t1][t2][t3][t4][t5][s1][s2]:
                                        l3_ep_name = f'{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_bbtu'
                                        l3_ep_value = 0
                                        for s4 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3]:
                                            l4_ep_name = f'{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_bbtu'
                                            l4_ep_value = 0
                                            for s5 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4]:
                                                l5_ep_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_bbtu'

                                                # if the flow is in the baseline data
                                                if l5_ep_name in df.columns:
                                                    # energy value is equal to baseline data value
                                                    l5_ep_value = df[l5_ep_name]

                                                    for water_type in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5]:
                                                        # if the water type is a withdrawal
                                                        if water_type == 'withdrawal':
                                                            l5_w_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_withdrawal_mgd'
                                                            with_int_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_withdrawal_intensity'

                                                            # if there are regional water withdrawal intensity values
                                                            if with_int_name in df.columns:
                                                                with_int_value = df[with_int_name]

                                                            # otherwise use parameter input water intensity estimate
                                                            else:
                                                                with_int_value = \
                                                                    t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5][
                                                                        water_type]

                                                            # calculate level 5 water withdrawal based on intensity
                                                            l5_w_value = l5_ep_value * with_int_value

                                                            # recalculate total water withdrawal for levels 1-4
                                                            l4_w_value = l4_w_value + l5_w_value
                                                            l3_w_value = l3_w_value + l5_w_value
                                                            l2_w_value = l2_w_value + l5_w_value
                                                            l1_w_value = l1_w_value + l5_w_value

                                                            # update each level's respective dictionary with values
                                                            l1_dict.update({l1_w_name: l1_w_value})
                                                            l2_dict.update({l2_w_name: l2_w_value})
                                                            l3_dict.update({l3_w_name: l3_w_value})
                                                            l4_dict.update({l4_w_name: l4_w_value})
                                                            l5_dict.update({l5_w_name: l5_w_value})

                                                        # repeat the same process for produced water
                                                        elif water_type == 'produced':
                                                            l5_p_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_produced_mgd'
                                                            prod_int_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_produced_intensity'
                                                            if prod_int_name in df.columns:
                                                                prod_int_value = df[prod_int_name]
                                                            else:
                                                                prod_int_value = \
                                                                    t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5][
                                                                        water_type]
                                                            l5_p_value = l5_ep_value * prod_int_value

                                                            l4_p_value = l4_p_value + l5_p_value
                                                            l3_p_value = l3_p_value + l5_p_value
                                                            l2_p_value = l2_p_value + l5_p_value
                                                            l1_p_value = l1_p_value + l5_p_value

                                                            l1_dict.update({l1_p_name: l1_p_value})
                                                            l2_dict.update({l2_p_name: l2_p_value})
                                                            l3_dict.update({l3_p_name: l3_p_value})
                                                            l4_dict.update({l4_p_name: l4_p_value})
                                                            l5_dict.update({l5_p_name: l5_p_value})
                                                        else:
                                                            pass

                                                    # recalculate total energy flows for levels 1-4
                                                    l4_ep_value = l4_ep_value + l5_ep_value
                                                    l3_ep_value = l3_ep_value + l5_ep_value
                                                    l2_ep_value = l2_ep_value + l5_ep_value
                                                    l1_ep_value = l1_ep_value + l5_ep_value

                                                    # update output dictionaries with energy flow values
                                                    l1_dict.update({l1_ep_name: l1_ep_value})
                                                    l2_dict.update({l2_ep_name: l2_ep_value})
                                                    l3_dict.update({l3_ep_name: l3_ep_value})
                                                    l4_dict.update({l4_ep_name: l4_ep_value})
                                                    l5_dict.update({l5_ep_name: l5_ep_value})
                                                else:
                                                    pass
        # loop through water split dictionary
        for x1 in split_dict:
            for x2 in split_dict[x1]:
                for x3 in split_dict[x1][x2]:
                    for x4 in split_dict[x1][x2][x3]:
                        for x5 in split_dict[x1][x2][x3][x4]:
                            for m_type in split_dict[x1][x2][x3][x4][x5]:
                                for w_type in split_dict[x1][x2][x3][x4][x5][m_type]:
                                    l5_w_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_{w_type}_mgd'

                                    # if the water withdrawal name is in the output dictionary
                                    if l5_w_name in l5_dict:
                                        l5_w_value = l5_dict[l5_w_name]

                                        # split water by water source
                                        if m_type == "source":
                                            for s1 in split_dict[x1][x2][x3][x4][x5][m_type][w_type]:
                                                l1_s_name = f'{s1}'
                                                l1_x_name = f'{x1}'
                                                l1_name = l1_s_name + '_to_' + l1_x_name + '_mgd'
                                                l1_value = 0
                                                for s2 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1]:
                                                    l2_s_name = f'{s1}_{s2}'
                                                    l2_x_name = f'{x1}_{x2}'
                                                    l2_name = l2_s_name + '_to_' + l2_x_name + '_mgd'
                                                    l2_value = 0
                                                    for s3 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2]:
                                                        l3_s_name = f'{s1}_{s2}_{s3}'
                                                        l3_x_name = f'{x1}_{x2}_{x3}'
                                                        l3_name = l3_s_name + '_to_' + l3_x_name + '_mgd'
                                                        l3_value = 0
                                                        for s4 in \
                                                                split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][
                                                                    s3]:
                                                            l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                            l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                            l4_name = l4_s_name + '_to_' + l4_x_name + '_mgd'
                                                            l4_value = 0
                                                            for s5 in \
                                                                    split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][
                                                                        s2][s3][
                                                                        s4]:
                                                                l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                                l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                                l5_name = l5_s_name + '_to_' + l5_x_name + '_mgd'
                                                                for p in \
                                                                        split_dict[x1][x2][x3][x4][x5][m_type][w_type][
                                                                            s1][s2][
                                                                            s3][s4][s5]:
                                                                    frac_name = l5_s_name + '_to_' \
                                                                                + l5_x_name + '_fraction'

                                                                    # if there's a region-level water fraction
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]
                                                                    else:
                                                                        frac = \
                                                                            split_dict[x1][x2][x3][x4][x5][m_type][
                                                                                w_type][
                                                                                s1][s2][s3][s4][s5][p]
                                                                    # calculate split water value
                                                                    l5_value = l5_w_value * frac

                                                                    # recalculate totals for levels 1-4
                                                                    l4_value = l4_value + l5_value
                                                                    l3_value = l3_value + l5_value
                                                                    l2_value = l2_value + l5_value
                                                                    l1_value = l1_value + l5_value

                                                                    # update output dictionaries
                                                                    l1_dict.update({l1_name: l1_value})
                                                                    l2_dict.update({l2_name: l2_value})
                                                                    l3_dict.update({l3_name: l3_value})
                                                                    l4_dict.update({l4_name: l4_value})
                                                                    l5_dict.update({l5_name: l5_value})

                                        # split water by discharge location
                                        else:
                                            for s1 in split_dict[x1][x2][x3][x4][x5][m_type][w_type]:
                                                l1_s_name = f'{s1}'
                                                l1_x_name = f'{x1}'
                                                l1_name = l1_x_name + '_to_' + l1_s_name + '_mgd'
                                                l1_value = 0
                                                for s2 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1]:
                                                    l2_s_name = f'{s1}_{s2}'
                                                    l2_x_name = f'{x1}_{x2}'
                                                    l2_name = l2_x_name + '_to_' + l2_s_name + '_mgd'
                                                    l2_value = 0
                                                    for s3 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2]:
                                                        l3_s_name = f'{s1}_{s2}_{s3}'
                                                        l3_x_name = f'{x1}_{x2}_{x3}'
                                                        l3_name = l3_x_name + '_to_' + l3_s_name + '_mgd'
                                                        l3_value = 0
                                                        for s4 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][
                                                            s2][s3]:
                                                            l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                            l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                            l4_name = l4_x_name + '_to_' + l4_s_name + '_mgd'
                                                            l4_value = 0
                                                            for s5 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][
                                                                s1][s2][s3][s4]:
                                                                l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                                l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                                l5_name = l5_x_name + '_to_' + l5_s_name + '_mgd'
                                                                for p in split_dict[x1][x2][x3][x4][x5][m_type][w_type][
                                                                    s1][s2][s3][s4][s5]:

                                                                    # create water split fraction name
                                                                    frac_name = l5_x_name + '_to_' \
                                                                                + l5_s_name + '_fraction'

                                                                    # if there's a region-level water fraction
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]
                                                                    else:
                                                                        frac = \
                                                                            split_dict[x1][x2][x3][x4][x5][m_type][
                                                                                w_type][
                                                                                s1][s2][s3][s4][s5][p]

                                                                    # calculate split water value
                                                                    l5_value = l5_w_value * frac

                                                                    # recalculate totals for levels 1-4
                                                                    l4_value = l4_value + l5_value
                                                                    l3_value = l3_value + l5_value
                                                                    l2_value = l2_value + l5_value
                                                                    l1_value = l1_value + l5_value

                                                                    # update output dictionaries
                                                                    l1_dict.update({l1_name: l1_value})
                                                                    l2_dict.update({l2_name: l2_value})
                                                                    l3_dict.update({l3_name: l3_value})
                                                                    l4_dict.update({l4_name: l4_value})
                                                                    l5_dict.update({l5_name: l5_value})
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
