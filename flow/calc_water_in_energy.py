import numpy as np
import pandas as pd
from .reader import *
import flow.clean as cl
import flow.configure as conf
import flow.construct as co

def calc_energy_direct_demand_water_use(data = None, output='l5', regions=3):
    """Calculates rejected energy (losses) and total generation from electricity generation
    by generating type for each region.


        :param data:                        DataFrame of input data containing electricity generation fuel and total
                                            electricity generation by type
        :type data:                         DataFrame


        """

    # load data
    if data:
        df = data
    else:
        df = test_baseline()

    # TODO unlock this later when the load_baseline_data is hooked up to a data reader
    # df = load_baseline_data()

    # get input parameters for fuel types, sub_fuel_types, and associated efficiency ratings and change to nested dict
    fuel_types = test_EP_param()
    t_dict = co.construct_nested_dictionary(fuel_types)

    split_types = test_EP_flows()
    split_dict = co.construct_nested_dictionary(split_types)


    if fuel_types.shape[1] >20:
        raise ValueError('Input source parameter data does not have correct number of levels')

    elif fuel_types.shape[1]  >20:
        raise ValueError('Input target parameter data does not have correct number of levels')

    else:
        # initialize output dictionaries with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # grab production values, calculate water values
        for t1 in t_dict:  # EP
            l1_W_name = f'{t1}_withdrawal_mgd'
            l1_W_value = 0
            l1_P_name = f'{t1}_produced_mgd'
            l1_P_value = 0
            for t2 in t_dict[t1]:
               l2_W_name = f'{t1}_{t2}_withdrawal_mgd'
               l2_W_value = 0
               l2_P_name = f'{t1}_{t2}_produced_mgd'
               l2_P_value = 0
               for t3 in t_dict[t1][t2]:
                   l3_W_name = f'{t1}_{t2}_{t3}_withdrawal_mgd'
                   l3_W_value = 0
                   l3_P_name = f'{t1}_{t2}_{t3}_produced_mgd'
                   l3_P_value = 0
                   for t4 in t_dict[t1][t2][t3]:
                       l4_W_name = f'{t1}_{t2}_{t3}_{t4}_withdrawal_mgd'
                       l4_W_value = 0
                       l4_P_name = f'{t1}_{t2}_{t3}_{t4}_produced_mgd'
                       l4_P_value = 0
                       for t5 in t_dict[t1][t2][t3][t4]:
                           for s1 in t_dict[t1][t2][t3][t4][t5]:
                               l1_EP_name = f'{s1}_to_{t1}_bbtu'
                               l1_EP_value = 0
                               for s2 in t_dict[t1][t2][t3][t4][t5][s1]:
                                   l2_EP_name = f'{s1}_{s2}_to_{t1}_{t2}_bbtu'
                                   l2_EP_value = 0
                                   for s3 in t_dict[t1][t2][t3][t4][t5][s1][s2]:
                                       l3_EP_name = f'{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_bbtu'
                                       l3_EP_value = 0
                                       for s4 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3]:
                                           l4_EP_name = f'{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_bbtu'
                                           l4_EP_value = 0
                                           for s5 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4]:
                                               l5_EP_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_bbtu'
                                               if l5_EP_name in df.columns:
                                                   l5_EP_value = df[l5_EP_name]   # grab energy production value in bbtu
                                                   for water_type in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5]:
                                                        if water_type == 'withdrawal':
                                                            l5_W_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_withdrawal_mgd'
                                                            with_int_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_withdrawal_intensity'
                                                            if with_int_name in df.columns:
                                                                with_int_value = df[with_int_name]
                                                            else:
                                                                with_int_value = t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5][water_type]

                                                            l5_W_value = l5_EP_value * with_int_value

                                                            l4_W_value = l4_W_value + l5_W_value
                                                            l3_W_value = l3_W_value + l5_W_value
                                                            l2_W_value = l2_W_value + l5_W_value
                                                            l1_W_value = l1_W_value + l5_W_value

                                                            l1_dict.update({l1_W_name: l1_W_value})
                                                            l2_dict.update({l2_W_name: l2_W_value})
                                                            l3_dict.update({l3_W_name: l3_W_value})
                                                            l4_dict.update({l4_W_name: l4_W_value})
                                                            l5_dict.update({l5_W_name: l5_W_value})

                                                        elif water_type == 'produced':
                                                             l5_P_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_produced_mgd'
                                                             prod_int_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_produced_intensity'
                                                             if prod_int_name in df.columns:
                                                                 prod_int_value = df[prod_int_name]
                                                             else:
                                                                 prod_int_value = t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5][water_type]
                                                             l5_P_value = l5_EP_value * prod_int_value

                                                             l4_P_value = l4_P_value + l5_P_value
                                                             l3_P_value = l3_P_value + l5_P_value
                                                             l2_P_value = l2_P_value + l5_P_value
                                                             l1_P_value = l1_P_value + l5_P_value

                                                             l1_dict.update({l1_P_name: l1_P_value})
                                                             l2_dict.update({l2_P_name: l2_P_value})
                                                             l3_dict.update({l3_P_name: l3_P_value})
                                                             l4_dict.update({l4_P_name: l4_P_value})
                                                             l5_dict.update({l5_P_name: l5_P_value})
                                                        else:
                                                            pass

                                                   l4_EP_value = l4_EP_value + l5_EP_value
                                                   l3_EP_value = l3_EP_value + l5_EP_value
                                                   l2_EP_value = l2_EP_value + l5_EP_value
                                                   l1_EP_value = l1_EP_value + l5_EP_value

                                                   l1_dict.update({l1_EP_name: l1_EP_value})
                                                   l2_dict.update({l2_EP_name: l2_EP_value})
                                                   l3_dict.update({l3_EP_name: l3_EP_value})
                                                   l4_dict.update({l4_EP_name: l4_EP_value})
                                                   l5_dict.update({l5_EP_name: l5_EP_value})
                                               else:
                                                   pass
        for x1 in split_dict:
            for x2 in split_dict[x1]:
                for x3 in split_dict[x1][x2]:
                    for x4 in split_dict[x1][x2][x3]:
                        for x5 in split_dict[x1][x2][x3][x4]:
                            for m_type in split_dict[x1][x2][x3][x4][x5]:
                                for w_type in split_dict[x1][x2][x3][x4][x5][m_type]:
                                    l5_w_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_{w_type}_mgd'
                                    if l5_w_name in l5_dict:
                                        l5_w_value = l5_dict[l5_w_name]
                                        # source split
                                        if m_type == "source":
                                            for s1 in split_dict[x1][x2][x3][x4][x5][m_type][w_type]:
                                                l1_s_name = f'{s1}'
                                                l1_x_name = f'{x1}'
                                                l1_name = l1_s_name + '_to_' + l1_x_name + '_mgd'
                                                l1_value = 0
                                                for s2 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1]:
                                                    l2_s_name = f'{s1}_{s2}'
                                                    l2_x_name = f'{x1}_{x2}'
                                                    l2_name = l2_s_name + '_to_' + l2_x_name + '_mgd'
                                                    l2_value = 0
                                                    for s3 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2]:
                                                        l3_s_name = f'{s1}_{s2}_{s3}'
                                                        l3_x_name = f'{x1}_{x2}_{x3}'
                                                        l3_name = l3_s_name + '_to_' + l3_x_name + '_mgd'
                                                        l3_value = 0
                                                        for s4 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3]:
                                                            l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                            l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                            l4_name = l4_s_name + '_to_' + l4_x_name + '_mgd'
                                                            l4_value = 0
                                                            for s5 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4]:
                                                                l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                                l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                                l5_name = l5_s_name + '_to_' + l5_x_name + '_mgd'
                                                                for p in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4][s5]:
                                                                    frac_name = l5_s_name + '_to_' + l5_x_name + '_fraction'
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]
                                                                    else:
                                                                        frac = \
                                                                        split_dict[x1][x2][x3][x4][x5][m_type][w_type][
                                                                            s1][s2][s3][s4][s5][p]
                                                                    l5_value = l5_w_value * frac

                                                                    l4_value = l4_value + l5_value
                                                                    l3_value = l3_value + l5_value
                                                                    l2_value = l2_value + l5_value
                                                                    l1_value = l1_value + l5_value

                                                                    l1_dict.update({l1_name: l1_value})
                                                                    l2_dict.update({l2_name: l2_value})
                                                                    l3_dict.update({l3_name: l3_value})
                                                                    l4_dict.update({l4_name: l4_value})
                                                                    l5_dict.update({l5_name: l5_value})
                                        # discharge split
                                        else:
                                            for s1 in split_dict[x1][x2][x3][x4][x5][m_type][w_type]:
                                                l1_s_name = f'{s1}'
                                                l1_x_name = f'{x1}'
                                                l1_name = l1_x_name + '_to_' + l1_s_name + '_mgd'
                                                l1_value = 0
                                                for s2 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1]:
                                                    l2_s_name = f'{s1}_{s2}'
                                                    l2_x_name = f'{x1}_{x2}'
                                                    l2_name = l2_x_name + '_to_' + l2_s_name + '_mgd'
                                                    l2_value = 0
                                                    for s3 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2]:
                                                        l3_s_name = f'{s1}_{s2}_{s3}'
                                                        l3_x_name = f'{x1}_{x2}_{x3}'
                                                        l3_name = l3_x_name + '_to_' + l3_s_name + '_mgd'
                                                        l3_value = 0
                                                        for s4 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3]:
                                                            l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                            l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                            l4_name = l4_x_name + '_to_' + l4_s_name + '_mgd'
                                                            l4_value = 0
                                                            for s5 in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4]:
                                                                l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                                l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                                l5_name = l5_x_name + '_to_' + l5_s_name + '_mgd'
                                                                for p in split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4][s5]:
                                                                    frac_name = l5_x_name + '_to_' + l5_s_name + '_fraction'
                                                                    if frac_name in df.columns:
                                                                        frac = df[frac_name]
                                                                    else:
                                                                        frac = split_dict[x1][x2][x3][x4][x5][m_type][w_type][s1][s2][s3][s4][s5][p]
                                                                    l5_value = l5_w_value * frac

                                                                    l4_value = l4_value + l5_value
                                                                    l3_value = l3_value + l5_value
                                                                    l2_value = l2_value + l5_value
                                                                    l1_value = l1_value + l5_value

                                                                    l1_dict.update({l1_name: l1_value})
                                                                    l2_dict.update({l2_name: l2_value})
                                                                    l3_dict.update({l3_name: l3_value})
                                                                    l4_dict.update({l4_name: l4_value})
                                                                    l5_dict.update({l5_name: l5_value})
                                else:
                                    pass


       # convert output dictionaries to dataframe, merge with location information
        l1_df = pd.DataFrame.from_dict(l1_dict, orient='index').transpose()
        l2_df = pd.DataFrame.from_dict(l2_dict, orient='index').transpose()
        l3_df = pd.DataFrame.from_dict(l3_dict, orient='index').transpose()
        l4_df = pd.DataFrame.from_dict(l4_dict, orient='index').transpose()
        l5_df = pd.DataFrame.from_dict(l5_dict, orient='index').transpose()

        if output == 'l1':
            df = l1_df
        elif output == 'l2':
            df = l2_df
        elif output == 'l3':
            df = l3_df
        elif output == 'l4':
            df = l4_df
        elif output == 'l5':
            df = l5_df
        else:
            m = 'incorrect level of granularity specified. Must be one of the following: l1, l2, l3, l4, or l5'
            raise ValueError(m)

        return df
