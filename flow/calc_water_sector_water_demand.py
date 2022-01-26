from .reader import *
import flow.construct as co


def calc_water_sector_water(data=None, level=5, regions=3):
    """Collects water demand data to water sectors (sectors whose energy demand is strictly dependent on their water
    demand) that directly withdraw their water from the water supply (e.g., public water supply) and aggregates the
    values.

        :param data:                        dataframe of baseline values to run calculations off of. Default is set to
                                            baseline dataframe specified in configuration.
        :type data:                         DataFrame

        :param level:                       Specifies what level of granularity to provide results. Must be an integer
                                            between 1 and 5, inclusive. Level 5 is the highest granularity, showing
                                            results down to the 5th level of specificity in each sector. Level 1 is the
                                            lowest level of granularity, showing results summed to the major sector
                                            level.
        :type level:                        int

        :param regions:                     The number of columns (inclusive) in the baseline dataset that include
                                            region identifiers (e.g. "Country", "State"). Reads from the first column
                                            in the dataframe onwards. Is used to combine various datasets to match
                                            values to each region included. Default number of regions is set to 3.
        :type regions:                      int

        :return:                            DataFrame of aggregated water demand values by source for water sectors
                                            (those whose energy demand is determined by their water demand) that
                                            withdraw their water directly from the water supply.
        """

    # load baseline data
    if data:
        df = data
    else:
        df = read_baseline_data()

    # load water source to water sector target values and convert to nested dictionary
    target_types = read_cwswd_water_flow_targets()
    split_dict = co.construct_nested_dictionary(target_types)

    # check that input data has correct number of columns
    if target_types.shape[1] > 12:
        m = 'Input parameter data does not have correct number of columns. Expects '
        raise ValueError(m)

    else:
        # initialize output dictionaries with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # build water sector water demand names
        for x1 in split_dict:  # level 1 water demand
            l1_demand_name = f'{x1}_to_{x1}_mgd'  # level 1 water demand name
            l1_demand_value = 0  # initialize level 1 water demand value
            for x2 in split_dict[x1]:
                l2_demand_name = f'{x1}_{x2}_to_{x1}_{x2}_mgd'
                l2_demand_value = 0
                for x3 in split_dict[x1][x2]:
                    l3_demand_name = f'{x1}_{x2}_{x3}_to_{x1}_{x2}_{x3}_mgd'
                    l3_demand_value = 0
                    for x4 in split_dict[x1][x2][x3]:
                        l4_demand_name = f'{x1}_{x2}_{x3}_{x4}_to_{x1}_{x2}_{x3}_{x4}_mgd'
                        l4_demand_value = 0
                        for x5 in split_dict[x1][x2][x3][x4]:
                            l5_demand_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_to_{x1}_{x2}_{x3}_{x4}_{x5}_mgd'

                            # build water source to water sector target name
                            for s1 in split_dict[x1][x2][x3][x4][x5]:
                                for s2 in split_dict[x1][x2][x3][x4][x5][s1]:
                                    for s3 in split_dict[x1][x2][x3][x4][x5][s1][s2]:
                                        for s4 in split_dict[x1][x2][x3][x4][x5][s1][s2][s3]:
                                            for s5 in split_dict[x1][x2][x3][x4][x5][s1][s2][s3][s4]:
                                                l5_supply_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{x1}_{x2}_{x3}_{x4}_{x5}_mgd'

                                                # if water source to water sector target in baseline data
                                                if l5_supply_name in df.columns:
                                                    l5_demand_value = df[l5_supply_name]

                                                    # update demand values at all levels
                                                    l4_demand_value = l4_demand_value + l5_demand_value
                                                    l3_demand_value = l3_demand_value + l5_demand_value
                                                    l2_demand_value = l2_demand_value + l5_demand_value
                                                    l1_demand_value = l1_demand_value + l5_demand_value

                                                    # update output dictionaries
                                                    l1_dict.update({l1_demand_name: l1_demand_value})
                                                    l2_dict.update({l2_demand_name: l2_demand_value})
                                                    l3_dict.update({l3_demand_name: l3_demand_value})
                                                    l4_dict.update({l4_demand_name: l4_demand_value})
                                                    l5_dict.update({l5_demand_name: l5_demand_value})
                                                else:
                                                    pass

       # convert output dictionaries to dataframes
        l1_df = pd.DataFrame.from_dict(l1_dict, orient='index').transpose()
        l2_df = pd.DataFrame.from_dict(l2_dict, orient='index').transpose()
        l3_df = pd.DataFrame.from_dict(l3_dict, orient='index').transpose()
        l4_df = pd.DataFrame.from_dict(l4_dict, orient='index').transpose()
        l5_df = pd.DataFrame.from_dict(l5_dict, orient='index').transpose()

        # return output at specified level of granularity
        if level == 1:
            df = l1_df
        elif level == 2:
            df = l2_df
        elif level == 3:
            df = l3_df
        elif level == 4:
            df = l4_df
        elif level == 5:
            df = l5_df
        else:
            m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
            raise ValueError(m)

        return df
