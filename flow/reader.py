import pkg_resources
import pandas as pd
from .read_config import *


def read_data():
    """Read in input data as DataFrame.

        :return:                        dataframe of input flow values

        """

    # collect path to file
    path = read_config()

    # collect file
    data = pkg_resources.resource_filename('flow', path)

    # return as DataFrame
    return pd.read_csv(data)


