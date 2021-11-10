import pkg_resources

import pandas as pd


def get_water_use_2015():
    """Read in a dataframe of 2015 USGS Water Use Data.

        :return:                        Dataframe of a number of water values for 2015 at the county level

        """

    data = pkg_resources.resource_filename('flow', 'data/usco2015v2.0.xlsx')

    return pd.read_excel(data, skiprows=1, dtype={'FIPS': str})


def get_interconnect_data():
    """Read in a dataframe of FIPS code - Interconnect crosswalk.

        :return:                        Dataframe of each US county's associated electricity interconnection

        """

    data = pkg_resources.resource_filename('flow', 'data/county_interconnect_list.xlsx')

    # read in county-interconnect crosswalk
    return pd.read_excel(data, dtype={'FIPS': str}, usecols=["FIPS", "Interconnect"])


def get_water_use_1995():
     """Read in a dataframe of 1995 USGS Water Use Data.

        :return:                        Dataframe of a number of water values for 1995 at the county level

        """

    data = pkg_resources.resource_filename('flow', 'data/usco1995.xlsx')

    return pd.read_excel(data,  dtype={'StateCode': str, 'CountyCode': str})
