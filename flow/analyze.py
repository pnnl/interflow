from .calc_flow import *


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








