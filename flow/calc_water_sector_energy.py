from .reader import *
import flow.construct as co
import flow.calc_ww_water_demand as wwd
import flow.calc_water_sector_water_demand as ws


def calc_water_sector_energy_demand(data=None, level=5, regions=3):
    """Calculates energy demand flows in water sectors (i.e., those that have their energy demand dependent on their
    water demand). Total energy demand values are then 1) split by energy sector source based on provided energy sector
    source fractions to determine energy flows into the water sectors (e.g., electricity generation to public water
    supply and 2) split by energy discharge locations based on provided discharge fractions to determine energy flows
    from water sectors (e.g., flows to rejected energy based on efficiency). Calculations are conducted for each region
    provided in the baseline dataset.

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
                                            specified level of granularity (see 'level' parameter) updated for
                                            double counting.

        """

    # load baseline data
    if data:
        df = data
    else:
        df = read_baseline_data()

    # load wastewater water demand data
    df_ww = wwd.calc_wastewater_water_demand()

    # load water sector water demand
    df_ws = ws.calc_water_sector_water()

    # combine wastewater water demand data and other water sector water demand data
    region_identifiers = df.columns[:regions].tolist()
    df_water = pd.merge(df_ww, df_ws, how='left', on=region_identifiers)

    # load water flow target and source combinations + associated energy intensity, convert to nested dict.
    target_types = read_cwse_water_flow_targets()
    t_dict = co.construct_nested_dictionary(target_types)

    # load energy split fractions to determine target to discharge energy flow values
    split_types = read_cwse_water_sector_energy_split_fractions()
    split_dict = co.construct_nested_dictionary(split_types)

    # check that input data has correct number of columns
    if target_types.shape[1] != 13:
        m = 'Input parameter data does not have correct number of columns. Expects 13 columns.'
        raise ValueError(m)

    elif split_types.shape[1] != 13:
        m = 'Input parameter data does not have correct number of columns. Expects 13 columns.'
        raise ValueError(m)

    else:
        # initialize output dictionaries with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # loop through target water names
        for t1 in t_dict:
            for t2 in t_dict[t1]:
                for t3 in t_dict[t1][t2]:
                    for t4 in t_dict[t1][t2][t3]:
                        for t5 in t_dict[t1][t2][t3][t4]:
                            l5_water_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_mgd'

                            # if level 5 water flow name is in calculated water values
                            if l5_water_name in df_water.columns:
                                l5_water_value = df_water[l5_water_name]

                                # loop through target energy names
                                for s1 in t_dict[t1][t2][t3][t4][t5]:  # level 1 energy
                                    l1_energy_name = f'{s1}_bbtu'  # level 1 energy name
                                    l1_energy_value = 0  # initialize level 1 energy value
                                    for s2 in t_dict[t1][t2][t3][t4][t5][s1]:
                                        l2_energy_name = f'{s1}_{s2}_bbtu'
                                        l2_energy_value = 0
                                        for s3 in t_dict[t1][t2][t3][t4][t5][s1][s2]:
                                            l3_energy_name = f'{s1}_{s2}_{s3}_bbtu'
                                            l3_energy_value = 0
                                            for s4 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3]:
                                                l4_energy_name = f'{s1}_{s2}_{s3}_{s4}_bbtu'
                                                l4_energy_value = 0
                                                for s5 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4]:
                                                    l5_energy_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_bbtu'
                                                    for param in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5]:

                                                        # create energy intensity name
                                                        intensity_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_intensity'

                                                        # if region-level intensity available
                                                        if intensity_name in df.columns:
                                                            intensity = df[intensity_name]

                                                        # otherwise use dictionary paramater value
                                                        else:
                                                            intensity = t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5][
                                                                param]

                                                        # calculate energy demand
                                                        l5_energy_value = l5_water_value * intensity

                                                        # recalculate energy demand values for levels 1-4
                                                        l4_energy_value = l4_energy_value + l5_energy_value
                                                        l3_energy_value = l3_energy_value + l5_energy_value
                                                        l2_energy_value = l2_energy_value + l5_energy_value
                                                        l1_energy_value = l1_energy_value + l5_energy_value

                                                        # update dictionaries with values
                                                        l1_dict.update({l1_energy_name: l1_energy_value})
                                                        l2_dict.update({l2_energy_name: l2_energy_value})
                                                        l3_dict.update({l3_energy_name: l3_energy_value})
                                                        l4_dict.update({l4_energy_name: l4_energy_value})
                                                        l5_dict.update({l5_energy_name: l5_energy_value})

        # loop through targets to build energy demand names
        for x1 in split_dict:  # level 1 target
            l1_energy_name = f'{x1}_bbtu'  # level 1 target energy name
            for x2 in split_dict[x1]:  # level 2 target
                l2_energy_name = f'{x1}_{x2}_bbtu'  # level 2 target energy name
                for x3 in split_dict[x1][x2]:
                    l3_energy_name = f'{x1}_{x2}_{x3}_bbtu'
                    for x4 in split_dict[x1][x2][x3]:
                        l4_energy_name = f'{x1}_{x2}_{x3}_{x4}_bbtu'
                        for x5 in split_dict[x1][x2][x3][x4]:
                            l5_energy_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_bbtu'
                            if l5_energy_name in l5_dict:
                                l5_energy_value = l5_dict[l5_energy_name]
                                for m_type in split_dict[x1][x2][x3][x4][x5]:  # movement type

                                    # if movement type is a source, calculate source to target energy flow
                                    if m_type == 'source':

                                        # build energy source names
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:  # level 1 energy source
                                            l1_name = f'{s1}_to_{x1}_bbtu'  # level 1 source to target flow name
                                            l1_value = 0  # initialize level 1 source to target flow value
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][s1]:
                                                l2_s_name = f'{s1}_{s2}'
                                                l2_x_name = f'{x1}_{x2}'
                                                l2_name = l2_s_name + '_to_' + l2_x_name + '_bbtu'
                                                l2_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2]:
                                                    l3_s_name = f'{s1}_{s2}_{s3}'
                                                    l3_x_name = f'{x1}_{x2}_{x3}'
                                                    l3_name = l3_s_name + '_to_' + l3_x_name + '_bbtu'
                                                    l3_value = 0
                                                    for s4 in \
                                                            split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3]:
                                                        l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                        l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                        l4_name = l4_s_name + '_to_' + l4_x_name + '_bbtu'
                                                        l4_value = 0
                                                        for s5 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][
                                                            s4]:
                                                            l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                            l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                            l5_name = l5_s_name + '_to_' + l5_x_name + '_bbtu'

                                                            for p in \
                                                            split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5]:

                                                                # build source fraction name
                                                                frac_name = l5_s_name + '_to_' + l5_x_name + '_fraction'

                                                                # if region-level source fraction name in baseline data
                                                                if frac_name in df.columns:
                                                                    frac = df[frac_name]

                                                                # otherwise use dictionary value
                                                                else:
                                                                    frac = \
                                                                    split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][
                                                                        s4][s5][p]

                                                                # calculate source to target energy flow value
                                                                l5_value = l5_energy_value * frac

                                                                # update source to target energy flow values
                                                                l4_value = l4_value + l5_value
                                                                l3_value = l3_value + l5_value
                                                                l2_value = l2_value + l5_value
                                                                l1_value = l1_value + l5_value

                                                                # update dictionary with values
                                                                l1_dict.update({l1_name: l1_value})
                                                                l2_dict.update({l2_name: l2_value})
                                                                l3_dict.update({l3_name: l3_value})
                                                                l4_dict.update({l4_name: l4_value})
                                                                l5_dict.update({l5_name: l5_value})
                                    # if movement type is discharge, calculate target to discharge flows
                                    elif m_type == 'discharge':
                                        # build discharge name
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]: # level 1 discharge
                                            l1_s_name = f'{s1}'  # level 1 discharge
                                            l1_x_name = f'{x1}'  # level 1 target
                                            l1_name = l1_x_name + '_to_' + l1_s_name + '_bbtu'  # level 1 flow name
                                            l1_value = 0  # initialize level 1 flow value
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][s1]:
                                                l2_s_name = f'{s1}_{s2}'
                                                l2_x_name = f'{x1}_{x2}'
                                                l2_name = l2_x_name + '_to_' + l2_s_name + '_bbtu'
                                                l2_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2]:
                                                    l3_s_name = f'{s1}_{s2}_{s3}'
                                                    l3_x_name = f'{x1}_{x2}_{x3}'
                                                    l3_name = l3_x_name + '_to_' + l3_s_name + '_bbtu'
                                                    l3_value = 0
                                                    for s4 in \
                                                            split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3]:
                                                        l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                        l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                        l4_name = l4_x_name + '_to_' + l4_s_name + '_bbtu'
                                                        l4_value = 0
                                                        for s5 in \
                                                                split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][
                                                                    s3][
                                                                    s4]:
                                                            l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                            l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                            l5_name = l5_x_name + '_to_' + l5_s_name + '_bbtu'
                                                            for p in \
                                                                    split_dict[x1][x2][x3][x4][x5][m_type][s1][
                                                                        s2][
                                                                        s3][s4][s5]:

                                                                # create fraction name
                                                                frac_name = l5_x_name + '_to_' + l5_s_name + '_fraction'

                                                                # if region-level fractions available in baseline data
                                                                if frac_name in df.columns:
                                                                    frac = df[frac_name]

                                                                # otherwise use dictionary value
                                                                else:
                                                                    frac = \
                                                                        split_dict[x1][x2][x3][x4][x5][m_type][
                                                                            s1][s2][s3][s4][s5][p]

                                                                # calculate target to discharge energy flow value
                                                                l5_value = l5_energy_value * frac

                                                                # update level values
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
