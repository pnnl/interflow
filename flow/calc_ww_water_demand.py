from .reader import *
import flow.construct as co
import flow.collect_water as cw


def calc_wastewater_water_demand(data=None, level=5, regions=3):
    """ Determines wastewater sector water demand as equal to either 1) aggregate calculated sector water discharge to
    wastewater supply values (e.g., residential discharge to wastewater supply) or 2) wastewater water demand values if
    available in the baseline dataset. Gives the ability to introduce actual wastewater treatment water data by county
    if available, rather than relying on estimates calculated from sector discharge to wastewater.

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

        :return:                            DataFrame of aggregated wastewater treatment water demand values by region.
        """

    # load baseline data
    if data:
        df = data
    else:
        df = read_baseline_data()

    # load discharges to wastewater supply values from collect_water module
    ww_supply = cw.collect_water_use()

    # load target parameters for building flow names to wastewater supply
    target_types = read_cwwwd_water_flow_targets()
    flow_dict = co.construct_nested_dictionary(target_types)

    # check for correct number of columns in parameter data
    if target_types.shape[1] != 12:
        m = 'Input source parameter data does not have correct number of levels'
        raise ValueError(m)

    else:
        # initialize output dictionaries with region identifier data for each level from baseline dataset
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # build flow names for wastewater demand to check baseline dataframe for
        for x1 in flow_dict:  # level 1 flow
            l1_demand_name = 'WWD_to_WWD_mgd'  # level 1 flow demand name
            l1_demand_value = 0  # initialize level 1 flow demand value
            for x2 in flow_dict[x1]:
                l2_demand_value = 0
                l2_demand_name = f'WWD_{x2}_to_WWD_{x2}_mgd'
                for x3 in flow_dict[x1][x2]:
                    l3_demand_value = 0
                    l3_demand_name = f'WWD_{x2}_{x3}_to_WWD_{x2}_{x3}_mgd'
                    for x4 in flow_dict[x1][x2][x3]:
                        l4_demand_value = 0
                        l4_demand_name = f'WWD_{x2}_{x3}_{x4}_to_WWD_{x2}_{x3}_{x4}_mgd'
                        for x5 in flow_dict[x1][x2][x3][x4]:
                            l5_demand_name = f'WWD_{x2}_{x3}_{x4}_{x5}_to_WWD_{x2}_{x3}_{x4}_{x5}_mgd'

                            # build flows into wastewater supply
                            for s1 in flow_dict[x1][x2][x3][x4][x5]:  # level 1 discharge to wastewater
                                l1_supply_name = f'{s1}_to_{x1}_mgd'  # level 1 discharge to wastewater name
                                l1_supply_value = 0  # initialize level 1 discharge to wastewater value
                                for s2 in flow_dict[x1][x2][x3][x4][x5][s1]:
                                    l2_supply_name = f'{s1}_{s2}_to_{x1}_{x2}_mgd'
                                    l2_supply_value = 0
                                    for s3 in flow_dict[x1][x2][x3][x4][x5][s1][s2]:
                                        l3_supply_name = f'{s1}_{s2}_{s3}_to_{x1}_{x2}_{x3}_mgd'
                                        l3_supply_value = 0
                                        for s4 in flow_dict[x1][x2][x3][x4][x5][s1][s2][s3]:
                                            l4_supply_name = f'{s1}_{s2}_{s3}_{s4}_to_{x1}_{x2}_{x3}_{x4}_mgd'
                                            l4_supply_value = 0
                                            for s5 in flow_dict[x1][x2][x3][x4][x5][s1][s2][s3][s4]:
                                                l5_supply_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{x1}_{x2}_{x3}_{x4}_{x5}_mgd'

                                                # check if discharge to wastewater supply is in water discharge calcs
                                                if l5_supply_name in ww_supply:

                                                    # set supply value for each level water discharge value
                                                    l5_supply_value = ww_supply[l5_supply_name]
                                                    l4_supply_value = l4_supply_value + l5_supply_value
                                                    l3_supply_value = l3_supply_value + l5_supply_value
                                                    l2_supply_value = l2_supply_value + l5_supply_value
                                                    l1_supply_value = l1_supply_value + l5_supply_value

                                                    # check baseline data for wastewater demand data
                                                    if l5_demand_name in df.columns:

                                                        # if demand data in baseline, set demand equal to demand
                                                        l5_demand_value = df[l5_demand_name]
                                                        l4_demand_value = l4_demand_value + l5_demand_value
                                                        l3_demand_value = l3_demand_value + l5_demand_value
                                                        l2_demand_value = l2_demand_value + l5_demand_value
                                                        l1_demand_value = l1_demand_value + l5_demand_value

                                                        # update dictionary
                                                        l1_dict.update({l1_demand_name: l1_demand_value})
                                                        l2_dict.update({l2_demand_name: l2_demand_value})
                                                        l3_dict.update({l3_demand_name: l3_demand_value})
                                                        l4_dict.update({l4_demand_name: l4_demand_value})
                                                        l5_dict.update({l5_demand_name: l5_demand_value})

                                                    # if no demand data in baseline data, set demand equal to supply
                                                    else:
                                                        l5_demand_value = l5_supply_value
                                                        l4_demand_value = l4_supply_value + l5_supply_value
                                                        l3_demand_value = l3_supply_value + l5_supply_value
                                                        l2_demand_value = l2_supply_value + l5_supply_value
                                                        l1_demand_value = l1_supply_value + l5_supply_value

                                                        # update dictionaries
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
