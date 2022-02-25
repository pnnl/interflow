import pkg_resources
import pandas as pd


def read_input_data(path: str, leading_zeros=None) -> pd.DataFrame:
    """Read in input csv data as a Pandas DataFrame.
        :param path:                    path to a csv file with flow values
        :type path:                     str

        :param leading_zeros:           Optional parameter to add leading zeros to the region column to ensure the
                                        regional identifier has the correct number of data positions.
        :type leading_zeros:            int

        :return:                        Pandas Dataframe of input flow values and parameters

        """

    # collect file
    df = pd.read_csv(path)

    # read the region column as a string
    region_col = df.columns[0]
    df[region_col] = df[region_col].astype(str)

    # add leading zeros to region if necessary
    if leading_zeros is None:
        df = df
    else:
        df[region_col] = df[region_col].apply(lambda x: x.zfill(leading_zeros))

    # return as DataFrame
    return df


