from .calc_flow import *


def analyze_sector(df:pd.DataFrame, region_name:str, sector_name:str, unit_type:str):
    """Determines top flow values to a specified sector in a single region, in specified units.
    """
    # load baseline data
    df = df[df.region == region_name]
    df = df[df.t1 == sector_name]
    df = df[df.units == unit_type]

    df.replace('total', "", inplace=True)
    df['source_name'] = df['S1'] + " " + df['S2'] + " " + df['S3'] + " " + df['S4'] + " " + df['S5']
    df['source_name'] = df['source_name'].str.strip()
    df['target_name'] = df['t1'] + " " + df['t2'] + " " + df['t3'] + " " + df['t4'] + " " + df['t5']
    df['target_name'] = df['target_name'].str.strip()
    df['flow_name'] = df['source_name'] + ' to ' + df['target_name']
    df['flow_name'] = df['flow_name'].str.strip()

    flow_list = df['flow_name'].head().to_list()
    value_list = df['value'].round(4).head().to_list()

    dictionary = dict(zip(flow_list, value_list))

    if dictionary == {}:
        print(f'No {unit_type} flows to {sector_name} in {region_name} are available.')

    else:
        print(f'The top {unit_type} flows to {sector_name} in {region_name} are: ')
        for name in dictionary:
            print(f'{name}        {dictionary[name]}  {unit_type}')


def group_results(df, output_level=1):

    reg_col_name = df.columns[0]

    if 'S5' in df.columns:
        input_level = 5
    elif ('S5' not in df.columns) & ('S4' in df.columns):
        input_level = 4
    elif ('S5' not in df.columns) & ('S4' not in df.columns) & ('S3' in df.columns):
        input_level = 3
    elif ('S5' not in df.columns) & ('S4' not in df.columns) & ('S3' not in df.columns)& ('S2' in df.columns):
        input_level = 2
    elif ('S5' not in df.columns) & ('S4' not in df.columns) & ('S3' not in df.columns)& ('S2' not in df.columns) & ('S1' in df.columns):
        input_level = 1
    else:
        m = 'input data not formatted corrected'
        raise ValueError(m)

    if input_level == 1:
        if output_level == 1:
            df = df.groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    elif input_level == 2:
        if output_level == 1:
            df = df.groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2','units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    elif input_level == 3:
        if output_level == 1:
            df = df.groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2','units'], as_index=False).sum()
        elif output_level == 3:
            df = df.groupby([reg_col_name, 'S1', 'S2','S3', 'T1', 'T2', 'T3', 'units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)

    elif input_level == 4:
        if output_level == 1:
            df = df.groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2','units'], as_index=False).sum()
        elif output_level == 3:
            df = df.groupby([reg_col_name, 'S1', 'S2','S3', 'T1', 'T2', 'T3', 'units'], as_index=False).sum()
        elif output_level == 4:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4','units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)


    elif input_level == 5:
        if output_level == 1:
            df = df.groupby([reg_col_name, 'S1', 'T1', 'units'], as_index=False).sum()
        elif output_level == 2:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'T1', 'T2','units'], as_index=False).sum()
        elif output_level == 3:
            df = df.groupby([reg_col_name, 'S1', 'S2','S3', 'T1', 'T2', 'T3', 'units'], as_index=False).sum()
        elif output_level == 4:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4','units'], as_index=False).sum()
        elif output_level == 5:
            df = df.groupby([reg_col_name, 'S1', 'S2', 'S3', 'S4', 'S5', 'T1', 'T2', 'T3', 'T4', 'T5','units'], as_index=False).sum()
        else:
            m = 'Cannot create output level given number of input levels'
            raise ValueError(m)
    else:
        m = 'Input level specified is not an integer between 1 and 5'
        raise ValueError(m)

    return df

