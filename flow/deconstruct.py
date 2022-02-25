import pandas as pd


def deconstruct_dictionary(input_dict: dict) -> pd.DataFrame:
    """Takes in a nested dictionary of run values and returns a dataframe with flow information as columns.

    :param input_dict:                        nested dictionary of values to unpack into a dataframe
    :type input_dict:                         dict
    :return:                                  Pandas Dataframe
    """

    # convert the dictionaries to a dataframe
    df = pd.DataFrame.from_dict(input_dict, orient='index').transpose()

    # melt the dataframe to get all columns as rows
    value_columns = df.columns[:].to_list()
    df = pd.melt(df, value_vars=value_columns, var_name='flow_name', value_name='value')

    # split out underscore separated flow value names into separate columns
    i = df.columns.get_loc('flow_name')
    df2 = df['flow_name'].str.split("_", expand=True)
    df = pd.concat([df.iloc[:, :i], df2, df.iloc[:, i+1:]], axis=1)

    # rename the columns depending on the number of columns
    if len(df.columns) == 6:
        col = ['region', 'S1', 'to', 'T1', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 8:
        col = ['region', 'S1', 'S2', 'to', 'T1', 'T2', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 10:
        col = ['region', 'S1', 'S2', 'S3', 'to', 'T1', 'T2', 'T3', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 12:
        col = ['region', 'S1', 'S2', 'S3', 'S4', 'to', 'T1', 'T2', 'T3', 'T4', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 14:
        col = ['region', 'S1', 'S2', 'S3','S4', 'S5', 'to', 'T1', 'T2', 'T3', 'T4', 'T5', 'units', 'value']
        df.columns = col
    else:
        m = 'Input dictionary keys do not have the correct number of levels to be able to deconstruct.'
        raise ValueError(m)

    # drop 'to' column from output dataframe
    df = df.drop(['to'], axis=1)

    return df
