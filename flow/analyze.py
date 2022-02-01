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


