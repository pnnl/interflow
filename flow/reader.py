import pkg_resources

import pandas as pd


def get_water_use_2015():
    """Read in a dataframe of 2015 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/usco2015v2.0.csv')

    return pd.read_csv(data, skiprows=1, dtype={'FIPS': str})


def get_water_use_1995():
    """Read in a dataframe of 1995 USGS Water Use Data.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/usco1995.csv')

    return pd.read_csv(data,  dtype={'StateCode': str, 'CountyCode': str})


def get_interconnect_data():
    """Read in a dataframe of FIPS code - Interconnect crosswalk.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/county_interconnect_list.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data, dtype={'FIPS': str}, usecols=["FIPS", "Interconnect"])


def get_population_data():
    """Read in a dataframe of population by FIPS code.

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/county-population.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data, dtype={'STATE FIPS': str, 'COUNTY FIPS': str}, encoding='latin-1')


def get_wastewater_flow_data():
    """Read in a dataframe of wastewater treatment facility water flows (MGS) by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Flow.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data)


def get_wastewater_facility_type_data():
    """Read in a dataframe of wastewater treatment facility type by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Type.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data)


def get_wastewater_facility_loc_data():
    """Read in a dataframe of wastewater treatment facility location by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Facility_Loc.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data)


def get_wastewater_facility_discharge_data():
    """Read in a dataframe of wastewater treatment facility discharge location by facility ID

        :return:                        dataframe of values

        """

    data = pkg_resources.resource_filename('flow', 'data/WW_Discharge.csv')

    # read in county-interconnect crosswalk
    return pd.read_csv(data)