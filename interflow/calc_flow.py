from .reader import *
import interflow.construct as co
import interflow.deconstruct as de
import interflow.analyze as an


def calculate(data: pd.DataFrame, level=5, region_name=None, remove_loops=True, output_file_path=None) -> pd.DataFrame:
    """Loops through input data for each region provided or specified and (1) collects flows for input data,  (2)
    calculates any cross unit flows based on input flow intensity values, (3) builds source flows for calculated
    intensities based on source fraction assumptions, and (4) builds discharge flows for calculated intensities and
    input data based on discharge fractions. Finally, outputs are aggregated to specified level of granularity.
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

    :param output_file_path:            Optional parameter to give a file path, inclusive of file name, to save
                                        dataframe output as a csv. Default is set to None (no output saved)
    :type output_file_path:             str

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

    # load input data
    df = data

    # check to make sure data has correct number of columns
    if len(df.columns.to_list()) == 16:
        pass
    else:
        m = 'Input data does not have the correct number of columns. 16 required.'
        raise ValueError(m)

    # if no region is provided as a parameter
    if region_name is None:
        df = df
    else:
        # check that provided region_name is in the input data
        region_column = df.columns[0]
        if region_name in df[region_column].tolist():
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

    # establish empty dictionaries to add calculated values to
    total_dict = {}  # dictionary of sector totals
    l5_dict = {}  # dictionary of level 5 granularity flows

    # loop through data
    for r in f_dict:
        for f_type in f_dict[r]:
            if f_type == 'A_collect':
                # collect input flow values
                for t1 in f_dict[r][f_type]:
                    for t2 in f_dict[r][f_type][t1]:
                        for t3 in f_dict[r][f_type][t1][t2]:
                            for t4 in f_dict[r][f_type][t1][t2][t3]:
                                for t5 in f_dict[r][f_type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][f_type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:

                                                                    # collect level 5 flow value
                                                                    l5_value = f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
                                                                    l5_dict.update({l5_name: l5_value})

                                                                    # update total dictionary with level 5 value
                                                                    l5_total_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                    if l5_total_name in total_dict:
                                                                        l5_total_value = total_dict[
                                                                                             l5_total_name] + l5_value
                                                                    else:
                                                                        l5_total_value = l5_value
                                                                    total_dict.update({l5_total_name: l5_total_value})

            # calculate new flows based on intensity values
            elif f_type == 'B_calculate':
                for t1 in f_dict[r][f_type]:
                    for t2 in f_dict[r][f_type][t1]:
                        for t3 in f_dict[r][f_type][t1][t2]:
                            for t4 in f_dict[r][f_type][t1][t2][t3]:
                                for t5 in f_dict[r][f_type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][f_type][t1][t2][t3][t4][t5]:
                                        l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'

                                        # check if a total value already exists for calculated flow to add on to
                                        if l5t_name in total_dict:
                                            l5t_value_total = total_dict[l5t_name]
                                        else:
                                            l5t_value_total = 0

                                            for s1 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1]:
                                                for s2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1]:
                                                    for s3 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        for s4 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            for s5 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                for u2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                    for p in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                        l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                        intensity = f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]

                                                                        # determine if the required input data is there
                                                                        if l5s_name not in total_dict:
                                                                            pass
                                                                        else:
                                                                            # flow value new value is based on
                                                                            l5s_value = total_dict[l5s_name]

                                                                            # new flow value
                                                                            l5t_value = l5s_value * intensity

                                                                            # add to total
                                                                            l5t_value_total = l5t_value_total + l5t_value

                                                                            # update total dictionary
                                                                            total_dict.update({l5t_name: l5t_value_total})

            # split total flow values into source flows from source fractions
            elif f_type == 'C_source':
                l5_s_value = 0
                for t1 in f_dict[r][f_type]:
                    for t2 in f_dict[r][f_type][t1]:
                        for t3 in f_dict[r][f_type][t1][t2]:
                            for t4 in f_dict[r][f_type][t1][t2][t3]:
                                for t5 in f_dict[r][f_type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][f_type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                for p in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:

                                                                    # check if the value is in the total dictionary
                                                                    if l5t_name not in total_dict:
                                                                        pass
                                                                    else:
                                                                        # collect total value from total dictionary
                                                                        l5t_value = total_dict[l5t_name]

                                                                        # determine source fraction
                                                                        fraction = f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]

                                                                        # calculate source to target flow value
                                                                        sl5_value = l5t_value * fraction

                                                                        # update output dictionary
                                                                        l5_dict.update({l5_name: sl5_value})

                                                                        # update total dictionary
                                                                        l5_s_value = l5_s_value + sl5_value
                                                                        total_dict.update({l5s_name: l5_s_value})

            # split total flow values into discharge flows from discharge fractions
            elif f_type == 'D_discharge':
                for t1 in f_dict[r][f_type]:
                    l5_s_value = 0
                    for t2 in f_dict[r][f_type][t1]:
                        for t3 in f_dict[r][f_type][t1][t2]:
                            for t4 in f_dict[r][f_type][t1][t2][t3]:
                                for t5 in f_dict[r][f_type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][f_type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                            for u2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                for p in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    # check if the value is in the total dictionary
                                                                    if l5t_name not in total_dict:
                                                                        pass
                                                                    else:
                                                                        # collect l5 value from total dictionary
                                                                        l5t_value = total_dict[l5t_name]

                                                                        # collection discharge fraction value
                                                                        fraction = f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]

                                                                        # calculate split to discharge
                                                                        dl5_value = l5t_value * fraction
                                                                        l5_dict.update({l5_name: dl5_value})

                                                                        # add to total dictionary
                                                                        l5_s_value = l5_s_value + dl5_value
                                                                        total_dict.update({l5s_name: l5_s_value})

    # loop through output dictionaries and and remove circular loop values
    if remove_loops:
        for r in f_dict:
            for f_type in f_dict[r]:
                for t1 in f_dict[r][f_type]:
                    for t2 in f_dict[r][f_type][t1]:
                        for t3 in f_dict[r][f_type][t1][t2]:
                            for t4 in f_dict[r][f_type][t1][t2][t3]:
                                for t5 in f_dict[r][f_type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][f_type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            for u2 in f_dict[r][f_type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:

                                                                # create level names for target and source
                                                                t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'

                                                                # level 5 dictionary
                                                                if t5_name in l5_dict:
                                                                    del l5_dict[t5_name]
                                                                else:
                                                                    pass

                                                                # level 5 dictionary
                                                                if s5_name in l5_dict:
                                                                    del l5_dict[s5_name]
                                                                else:
                                                                    pass
    else:
        pass

    # deconstruct nested dictionary into dataframe
    df = de.deconstruct_dictionary(l5_dict)

    # return output at specified level of granularity
    if level == 1:
        df = an.group_results(df=df, output_level=1)
    elif level == 2:
        df = an.group_results(df=df, output_level=2)
    elif level == 3:
        df = an.group_results(df=df, output_level=3)
    elif level == 4:
        df = an.group_results(df=df, output_level=4)
    elif level == 5:
        df = df
    else:
        m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
        raise ValueError(m)

    # save output to csv if output file path specified
    if output_file_path is None:
        pass
    else:
        df.to_csv(output_file_path)

    return df
