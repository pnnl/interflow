import pandas as pd


def deconstruct_nested_dictionary(input_dict:dict):

    # step
    # convert output dictionaries to dataframes
    df = pd.DataFrame.from_dict(input_dict, orient='index').transpose()

    # melt the dataframe
    value_columns = df.columns[:].to_list()
    df = pd.melt(df, value_vars=value_columns, var_name='flow_name', value_name='value')

    i = df.columns.get_loc('flow_name')
    df2 = df['flow_name'].str.split("_", expand=True)
    df = pd.concat([df.iloc[:, :i], df2, df.iloc[:, i+1:]], axis=1)

    if len(df.columns) == 6:
        col = ['region', 'S1', 'to', 't1', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 8:
        col = ['region', 'S1', 'S2', 'to', 't1', 't2', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 10:
        col = ['region', 'S1', 'S2', 'S3', 'to', 't1', 't2', 't3', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 12:
        col = ['region', 'S1', 'S2', 'S3', 'S4', 'to', 't1', 't2', 't3', 't4', 'units', 'value']
        df.columns = col
    elif len(df.columns) == 14:
        col = ['region', 'S1', 'S2', 'S3','S4', 'S5', 'to', 't1', 't2', 't3','t4', 't5', 'units', 'value']
        df.columns = col
    else:
        pass

    df = df.drop(['to'], axis=1)

    return df
