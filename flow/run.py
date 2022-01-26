import numpy as np
import pandas as pd
import flow.update as up


def run(level=5, regions=3, output_file_path=None):
    """Runs each energy and water calculation for each region, updates calculations to remove double counting, and
    produces output in the form of a Pandas DataFrame with the option to save output to a csv.


        :param level:                       Specifies what level of granularity to provide results. Must be between
                                            1 and 5, inclusive. Level 5 is the highest granularity, showing results down
                                            to the 5th level of specificity in each sector. Level 1 is the lowest level
                                            of granularity, showing results summed to the major sector level.
        :type level:                        int

        :param regions:                     The number of columns (inclusive) in the baseline dataset that include
                                            region identifiers (e.g. "Country", "State"). Reads from the first column
                                            in the dataframe onwards. Is used to combine various datasets to match
                                            values to each region included. Default number of regions is set to 3.
        :type regions:                      int

        :param output_file_path:            Optional parameter to provide a path to save run output as a csv. Must be
                                            provided as a string. File path must include '[filename].csv' at the end
                                            of the path where [filename] is the chosen name of the csv file. Default is
                                            to not save output.
        :type output_file_path:             str

        :return:                            DataFrame of calculated water and energy sector flow values by region at
                                            specified level of granularity (see 'level' parameter)

        """

    # run calculations and updater
    output = up.calculate_flows_and_updates(level=level, regions=regions)

    # save output to .csv if specified
    if output_file_path:
        output.to_csv(output_file_path)
    else:
        pass

    return output
