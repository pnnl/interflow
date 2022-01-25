import numpy as np
import pandas as pd
import flow.updater as up


def run(level='l5', regions=3, output_file_path=None):
    """Calculates rejected energy (losses) and total generation from electricity generation
    by generating type for each region.


        :param level:                        DataFrame of input data containing electricity generation fuel and total
                                            electricity generation by type
        :type level:                         DataFrame


        """

    # load and combine

    output = up.calculate_flows_and_updates(level=level, regions=regions)

    if output_file_path:
        output.to_csv(output_file_path)

    else:
        pass

    return output
