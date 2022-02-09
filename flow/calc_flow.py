from .reader import *
import pandas as pd
import flow.construct as co
import flow.deconstruct as de


def calculate(data=None, level=5, region_name=None, remove_loops=True, output_file_name=None):
    """Loops through input data for each region provided or specified and (1) collects flows for input data, (2)
    calculates totals for input flows at level 1 through level 5 granularity (2) calculates any cross unit flows based
    on input flow intensity values at level 1 through level 5 granularity (3) builds source flows for calculated
    intensities based on source fraction assumptions at level 1 through level 5 granularity, and (4) builds discharge
    flows for calculated intensities and input data based on discharge fractions at level 1 through level 5 granularity.
    This function also removes all self-provided (i.e., looped) flows if remove_loops parameter is set to True.


    :param data:                        Pandas DataFrame of input flow values, intensities, and fractions
    :type data:                         DataFrame

    :param level:                       Desired level of granularity of output data. Must be an integer between 1
                                        and 5, inclusive.
    :type level:                        int

    :param region_name:                 Name of region to conduct analysis of. If none is specified, calculations are
                                        run for all regions included in the input data.
    :type region_name:                  str

    :param remove_loops:                Boolean indicating whether looped values (i.e., nodes whose output is its own
                                        input value) should be removed from output dataset. Default is True.
    :type remove_loops:                 bool

    :param output_file_name:            Desired name of output file (saved as a .csv) to output path specified in config
                                        yaml file. Default is set to None (no output saved)
    :type output_file_name:             str

    :return:                            DataFrame of flow run output at specified level of granularity for specified
                                        region(s)

    """
    # check that the granularity level specified is within range
    acceptable_values = [1, 2, 3, 4, 5]
    if level in acceptable_values:
        pass
    else:
        m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
        raise ValueError(m)

    # load baseline data
    if data is None:
        df = read_data()  # read DataFrame from configuration file
    else:
        df = data  # or read DataFrame from parameter input

    # check to make sure data is a DataFrame and has correct number of columns
    if type(df) == pd.DataFrame:
        if len(df.columns.to_list()) == 16:
            pass
        else:
            m = 'Input data does not have the correct number of columns. 16 required.'
            raise ValueError(m)
    else:
        m = 'Input data not in DataFrame format'
        raise TypeError(m)

    # if no region is provided as a parameter
    if region_name is None:
        df = df
    else:
        # check that provided region_name is in the input data
        region_column = df.columns[0]
        if region_name in data[region_column].tolist():
            pass
        else:
            m = 'Region provided is not in the input data.'
            raise ValueError(m)

        # reduce input DataFrame to region specified
        df[df.columns[0]] = df[df.columns[0]].astype(str)
        reg_col = df.columns[0]
        df = df.loc[df[reg_col] == region_name]

    # construct nested dictionary from input data
    f_dict = co.construct_nested_dictionary(df)

    total_dict = {}
    l5_dict = {}
    l4_dict = {}
    l3_dict = {}
    l2_dict = {}
    l1_dict = {}

    fraction_dict = {}

    # initialize values
    for r in f_dict:
        for type in f_dict[r]:
            if type == 'A_collect':
                for t1 in f_dict[r][type]:
                    s1_value = 0
                    l1_value = 0
                    t1_value = 0
                    for t2 in f_dict[r][type][t1]:
                        l2_value = 0
                        for t3 in f_dict[r][type][t1][t2]:
                            l3_value = 0
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    l4_value = 0
                                    l5_total_value = 0
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        # collect direct draw flows (water withdraws or energy demand)
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                            s1_name = f'{r}_{s1}_{u1}'
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    l5_value = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
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

                                                                    l5_total_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                    l5_total_value = l5_total_value + l5_value
                                                                    total_dict.update({l5_total_name: l5_total_value})

                                                                    t1_value = t1_value + l5_value
                                                                    total_dict.update({t1_name: t1_value})

                                                                    #s1_value = s1_value + l5_value
                                                                    #total_dict.update({s1_name: s1_value})

                 # calculate the fraction of source location that feed into each target
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            if l5_name in l5_dict:
                                                                l5_fraction_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}_fraction'
                                                                l5_fraction_value = l5_dict[l5_name]/total_dict[t1_name]
                                                                fraction_dict.update({l5_fraction_name: l5_fraction_value})
                                                            else:
                                                                pass

            # calculate energy or water for water and energy sectors
            elif type == 'B_calculate':

                for t1 in f_dict[r][type]:
                    l5t_value_total = 0
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                    intensity = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
                                                                    if l5s_name in total_dict:
                                                                        l5s_value = total_dict[l5s_name]  # flow value it's based on
                                                                        l5t_value = l5s_value * intensity  # calculated value
                                                                        l5t_value_total = l5t_value_total + l5t_value  # calculated total
                                                                        total_dict.update({l5t_name: l5t_value_total})
                                                                    else:
                                                                        pass

                                    # split water and energy values into individual sources
            elif type == 'C_source':
                l5_s_value = 0
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                            sl1_value = 0
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                sl2_value = 0
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                    sl3_value = 0
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                        sl4_value = 0
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'

                                                            # PWD_total_total_total_total_mgd
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    # if it's not blank
                                                                    if f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p] > 0:
                                                                        if l5t_name in total_dict:
                                                                            l5t_value = total_dict[l5t_name]
                                                                            fraction = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
                                                                            sl5_value = l5t_value * fraction
                                                                            sl4_value = sl4_value + sl5_value
                                                                            sl3_value = sl3_value + sl5_value
                                                                            sl2_value = sl2_value + sl5_value
                                                                            sl1_value = sl1_value + sl5_value
                                                                            # update output dictionaries
                                                                            l1_dict.update({l1_name: sl1_value})
                                                                            l2_dict.update({l2_name: sl2_value})
                                                                            l3_dict.update({l3_name: sl3_value})
                                                                            l4_dict.update({l4_name: sl4_value})
                                                                            l5_dict.update({l5_name: sl5_value})


                                                                            l5_s_value = l5_s_value + sl5_value
                                                                            total_dict.update({l5s_name: l5_s_value})

                                                                        else:
                                                                            pass
                                                                    else:
                                                                        if l5t_name in total_dict:
                                                                            l5t_value = total_dict[l5t_name]
                                                                            l5_fraction_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}_fraction'

                                                                            fraction = fraction_dict[l5_fraction_name]
                                                                            sl5_value = l5t_value * fraction
                                                                            sl4_value = sl4_value + sl5_value
                                                                            sl3_value = sl3_value + sl5_value
                                                                            sl2_value = sl2_value + sl5_value
                                                                            sl1_value = sl1_value + sl5_value
                                                                            # update output dictionaries
                                                                            l1_dict.update({l1_name: sl1_value})
                                                                            l2_dict.update({l2_name: sl2_value})
                                                                            l3_dict.update({l3_name: sl3_value})
                                                                            l4_dict.update({l4_name: sl4_value})
                                                                            l5_dict.update({l5_name: sl5_value})


            elif type == 'D_discharge':

                for t1 in f_dict[r][type]:
                    l5_s_value = 0
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{t1}_to_{s1}_{u1}'
                                            dl1_value = 0
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                l2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
                                                dl2_value = 0
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    l3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
                                                    dl3_value = 0
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        l4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
                                                        dl4_value = 0
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    if l5t_name in total_dict:
                                                                        l5t_value = total_dict[l5t_name]
                                                                        fraction = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]

                                                                        # calculate split to discharge
                                                                        dl5_value = l5t_value * fraction
                                                                        dl4_value = dl4_value + dl5_value
                                                                        dl3_value = dl3_value + dl5_value
                                                                        dl2_value = dl2_value + dl5_value
                                                                        dl1_value = dl1_value + dl5_value

                                                                    # update output dictionaries
                                                                        l1_dict.update({l1_name: dl1_value})
                                                                        l2_dict.update({l2_name: dl2_value})
                                                                        l3_dict.update({l3_name: dl3_value})
                                                                        l4_dict.update({l4_name: dl4_value})
                                                                        l5_dict.update({l5_name: dl5_value})

                                                                        l5_s_value = l5_s_value + dl5_value
                                                                        total_dict.update({l5s_name:l5_s_value})
                                                                    else:
                                                                        pass
                                # calculate the fraction of source location that feed into each target
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        if t1_name in total_dict:
                                            for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                                for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                    for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                if l5_name in l5_dict:
                                                                    l5_fraction_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}_fraction'
                                                                    l5_fraction_value = l5_dict[l5_name] / \
                                                                                        total_dict[t1_name]
                                                                    fraction_dict.update({l5_fraction_name: l5_fraction_value})
                                                                else:
                                                                    pass
                                        else:
                                            pass
    # loop through and remove circular loops
    if remove_loops:
        for r in f_dict:
            for type in f_dict[r]:
                if type == 'A_collect':
                    for t1 in f_dict[r][type]:
                        for t2 in f_dict[r][type][t1]:
                            for t3 in f_dict[r][type][t1][t2]:
                                for t4 in f_dict[r][type][t1][t2][t3]:
                                    for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                        for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                            for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                                for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                    for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                    t1_name = f'{r}_{t1}_to_{t1}_{u1}'
                                                                    s1_name = f'{r}_{s1}_to_{s1}_{u2}'
                                                                    t2_name = f'{r}_{t1}_{t2}_to_{t1}_{t2}_{u1}'
                                                                    s2_name = f'{r}_{s1}_{s2}_to_{s1}_{s2}_{u2}'
                                                                    t3_name = f'{r}_{t1}_{t2}_{t3}_to_{t1}_{t2}_{t3}_{u1}'
                                                                    s3_name = f'{r}_{s1}_{s2}_{s3}_to_{s1}_{s2}_{s3}_{u2}'
                                                                    t4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                                    s4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{s1}_{s2}_{s3}_{s4}_{u2}'
                                                                    t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                    s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                    if t1_name in l1_dict:
                                                                        del l1_dict[t1_name]
                                                                    else:
                                                                        pass
                                                                    if t2_name in l2_dict:
                                                                        del l2_dict[t2_name]
                                                                    else:
                                                                        pass
                                                                    if t3_name in l3_dict:
                                                                        del l3_dict[t3_name]
                                                                    else:
                                                                        pass
                                                                    if t4_name in l4_dict:
                                                                        del l4_dict[t4_name]
                                                                    else:
                                                                        pass
                                                                    if t5_name in l5_dict:
                                                                        del l5_dict[t5_name]
                                                                    else:
                                                                        pass

                                                                    if s1_name in l1_dict:
                                                                        del l1_dict[s1_name]
                                                                    else:
                                                                        pass
                                                                    if s2_name in l2_dict:
                                                                        del l2_dict[s2_name]
                                                                    else:
                                                                        pass
                                                                    if s3_name in l3_dict:
                                                                        del l3_dict[s3_name]
                                                                    else:
                                                                        pass
                                                                    if s4_name in l4_dict:
                                                                        del l4_dict[s4_name]
                                                                    else:
                                                                        pass
                                                                    if s5_name in l5_dict:
                                                                        del l5_dict[s5_name]

                                                                    else:
                                                                        pass
    else:
        pass

    # return output at specified level of granularity
    if level == 1:
        df = de.deconstruct_dictionary(l1_dict)
    elif level == 2:
        df = de.deconstruct_dictionary(l2_dict)
    elif level == 3:
        df = de.deconstruct_dictionary(l3_dict)
    elif level == 4:
        df = de.deconstruct_dictionary(l4_dict)
    elif level == 5:
        df = de.deconstruct_dictionary(l5_dict)
    else:
        m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
        raise ValueError(m)

    return df
