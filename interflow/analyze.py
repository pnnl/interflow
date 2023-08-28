import pandas as pd


def group_results(df: pd.DataFrame, output_level=1):
    """ Groups package run output to level of granularity specified. Returns a dataframe of values with
    source to target flows by region.

    :param df:                                          Dataframe of package run output values.
    :type df:                                           DataFrame

    :param output_level:                                Level of granularity output will be grouped to. Must be an
                                                        integer between one and five, inclusive. Default value is set to
                                                        level 1 granularity.
    :type output_level:                                 int

    :return:                                            DataFrame of values organized as source to target flow values
                                                        summed to level of granularity specified.
    """

    # collect region column
    reg_col_name = df.columns[0]

    # check for levels of data
    if 'S5' in df.columns:
        input_level = 5
    elif ('S5' not in df.columns) & ('S4' in df.columns):
        input_level = 4
    elif ('S5' not in df.columns) & ('S4' not in df.columns) & ('S3' in df.columns):
        input_level = 3
    elif ('S5' not in df.columns) & ('S4' not in df.columns) & ('S3' not in df.columns) & ('S2' in df.columns):
        input_level = 2
    elif ('S5' not in df.columns) & ('S4' not in df.columns) & ('S3' not in df.columns) \
            & ('S2' not in df.columns) & ('S1' in df.columns):
        input_level = 1
    else:
        m = 'input data not formatted correctly'
        raise ValueError(m)

    # level 1 granularity grouping
    if input_level == 1:
        if output_level == 1:
            df = df[[reg_col_name, 'S1', 'T1', 'units', 'value']].groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    # level 2 granularity grouping
    elif input_level == 2:
        if output_level == 1:
            df = df[[reg_col_name, 'S1', 'T1', 'units', 'value']].groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df[[reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    # level 3 granularity grouping
    elif input_level == 3:
        if output_level == 1:
            df = df[[reg_col_name, 'S1', 'T1', 'units', 'value']].groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df[[reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units'], as_index=False).sum()
        elif output_level == 3:
            df = df[[reg_col_name, 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    # level 4 granularity grouping
    elif input_level == 4:
        if output_level == 1:
            df = df[[reg_col_name, 'S1', 'T1', 'units', 'value']].groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df[[reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units'], as_index=False).sum()
        elif output_level == 3:
            df = df[[reg_col_name, 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units'], as_index=False).sum()
        elif output_level == 4:
            df = df[[reg_col_name, 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4', 'units'],
                            as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    # level 5 granularity grouping
    elif input_level == 5:
        if output_level == 1:
            df = df[[reg_col_name, 'S1', 'T1', 'units', 'value']].groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df[[reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2', 'units'], as_index=False).sum()
        elif output_level == 3:
            df = df[[reg_col_name, 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units'], as_index=False).sum()
        elif output_level == 4:
            df = df[[reg_col_name, 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4', 'units'],
                            as_index=False).sum()
        elif output_level == 5:
            df = df[[reg_col_name, 'S1', 'S2', 'S3', 'S4', 'S5', 'T1', 'T2', 'T3', 'T4', 'T5', 'units', 'value']].groupby([reg_col_name, 'S1', 'S2', 'S3', 'S4', 'S5', 'T1', 'T2', 'T3', 'T4', 'T5', 'units'],
                            as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    # return an error if an invalid granularity level is provided as a parameter.
    else:
        m = 'Input level specified is not an integer between 1 and 5'
        raise ValueError(m)

    return df
