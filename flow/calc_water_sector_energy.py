import numpy as np
import pandas as pd
from .reader import *
import flow.clean as cl
import flow.configure as conf
import flow.construct as co
import flow.collect_water as cw
import flow.calc_ww_water_demand as wwd
import flow.collect_water_sector_water as ws


def calc_water_sector_energy(output='l5', regions=3):
    """Calculates rejected energy (losses) and total generation from electricity generation
    by generating type for each region.


        :param data:                        DataFrame of input data containing electricity generation fuel and total
                                            electricity generation by type
        :type data:                         DataFrame


        """

    # load baseline data
    df = test_baseline()
    # TODO unlock this later when the load_baseline_data is hooked up to a data reader

    # bring in wastewater total
    df_ww = wwd.calc_wastewater_water_demand()

    # bring in water sector totals
    df_ws = ws.calc_water_sector_water()

    # combine water estimates
    region_identifiers = df.columns[:regions].tolist()
    df_water = pd.merge(df_ww, df_ws, how='left', on=region_identifiers)

    # get input parameters for fuel types, sub_fuel_types, and associated efficiency ratings and change to nested dict

    sector_types = test_water_sector_energy()
    t_dict = co.construct_nested_dictionary(sector_types)

    target_types = test_water_sector_energy_discharge()
    split_dict = co.construct_nested_dictionary(target_types)


    if target_types.shape[1] > 15:
        raise ValueError('Input source parameter data does not have correct number of levels')

    elif target_types.shape[1] > 20:
        raise ValueError('Input target parameter data does not have correct number of levels')

    else:
        # initialize output dictionaries with region identifiers
        l5_dict = df[df.columns[:regions].tolist()].to_dict()
        l4_dict = df[df.columns[:regions].tolist()].to_dict()
        l3_dict = df[df.columns[:regions].tolist()].to_dict()
        l2_dict = df[df.columns[:regions].tolist()].to_dict()
        l1_dict = df[df.columns[:regions].tolist()].to_dict()

        # use collected and estimated water values and associated intensities to calculate energy
        for t1 in t_dict:  # WWD
            l1_water_name = f'{t1}_mgd'
            for t2 in t_dict[t1]:
                l2_water_name = f'{t1}_{t2}_mgd'
                for t3 in t_dict[t1][t2]:
                    l3_water_name = f'{t1}_{t2}_{t3}_mgd'
                    for t4 in t_dict[t1][t2][t3]:
                        l4_water_name = f'{t1}_{t2}_{t3}_{t4}_mgd'
                        for t5 in t_dict[t1][t2][t3][t4]:
                            l5_water_name = f'{t1}_{t2}_{t3}_{t4}_{t5}_mgd'
                            if l5_water_name in df_water.columns:
                                l5_water_value = df_water[l5_water_name]
                                for s1 in t_dict[t1][t2][t3][t4][t5]:
                                    l1_energy_name = f'{s1}_bbtu'
                                    l1_energy_value = 0
                                    for s2 in t_dict[t1][t2][t3][t4][t5][s1]:
                                        l2_energy_name = f'{s1}_{s2}_bbtu'
                                        l2_energy_value = 0
                                        for s3 in t_dict[t1][t2][t3][t4][t5][s1][s2]:
                                            l3_energy_name = f'{s1}_{s2}_{s3}_bbtu'
                                            l3_energy_value = 0
                                            for s4 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3]:
                                                l4_energy_name = f'{s1}_{s2}_{s3}_{s4}_bbtu'
                                                l4_energy_value = 0
                                                for s5 in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4]:
                                                    l5_energy_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_bbtu'
                                                    for param in t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5]:
                                                        intensity = t_dict[t1][t2][t3][t4][t5][s1][s2][s3][s4][s5][param]
                                                        l5_energy_value = df_water[l5_water_name] * intensity

                                                        l4_energy_value = l4_energy_value + l5_energy_value
                                                        l3_energy_value = l3_energy_value + l5_energy_value
                                                        l2_energy_value = l2_energy_value + l5_energy_value
                                                        l1_energy_value = l1_energy_value + l5_energy_value

                                                        l1_dict.update({l1_energy_name: l1_energy_value})
                                                        l2_dict.update({l2_energy_name: l2_energy_value})
                                                        l3_dict.update({l3_energy_name: l3_energy_value})
                                                        l4_dict.update({l4_energy_name: l4_energy_value})
                                                        l5_dict.update({l5_energy_name: l5_energy_value})
        for x1 in split_dict:
            l1_energy_name = f'{x1}_bbtu'
            for x2 in split_dict[x1]:
                l2_energy_name = f'{x1}_{x2}_bbtu'
                for x3 in split_dict[x1][x2]:
                    l3_energy_name = f'{x1}_{x2}_{x3}_bbtu'
                    for x4 in split_dict[x1][x2][x3]:
                        l4_energy_name = f'{x1}_{x2}_{x3}_{x4}_bbtu'
                        for x5 in split_dict[x1][x2][x3][x4]:
                            l5_energy_name = f'{x1}_{x2}_{x3}_{x4}_{x5}_mgd'
                            if l5_energy_name in l5_dict:
                                l5_energy_value = l5_dict[l5_energy_name]
                                for m_type in split_dict[x1][x2][x3][x4][x5]:

                                    # calculate source
                                    if m_type == 'source':
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:
                                            l1_name = f'{s1}_to_{x1}_bbtu'
                                            l1_value = 0
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][s1]:
                                                l2_s_name = f'{s1}_{s2}'
                                                l2_x_name = f'{x1}_{x2}'
                                                l2_name = l2_s_name + '_to_' + l2_x_name + '_bbtu'
                                                l2_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2]:
                                                    l3_s_name = f'{s1}_{s2}_{s3}'
                                                    l3_x_name = f'{x1}_{x2}_{x3}'
                                                    l3_name = l3_s_name + '_to_' + l3_x_name + 'bbtu'
                                                    l3_value = 0
                                                    for s4 in \
                                                    split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3]:
                                                        l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                        l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                        l4_name = l4_s_name + '_to_' + l4_x_name + 'bbtu'
                                                        l4_value = 0
                                                        for s5 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4]:
                                                            l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                            l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                            l5_name = l5_s_name + '_to_' + l5_x_name + 'bbtu'
                                                            for p in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5]:
                                                                frac_name = l5_s_name + '_to_' + l5_x_name + '_fraction'
                                                                if frac_name in df.columns:
                                                                    frac = df[frac_name]
                                                                else:
                                                                    frac = split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3][s4][s5][p]
                                                                l5_value = l5_energy_value * frac
                                                                l4_value = l4_value + l5_value
                                                                l3_value = l3_value + l5_value
                                                                l2_value = l2_value + l5_value
                                                                l1_value = l1_value + l5_value

                                                                l1_dict.update({l1_name: l1_value})
                                                                l2_dict.update({l2_name: l2_value})
                                                                l3_dict.update({l3_name: l3_value})
                                                                l4_dict.update({l4_name: l4_value})
                                                                l5_dict.update({l5_name: l5_value})

                                    elif m_type == 'discharge':
                                        for s1 in split_dict[x1][x2][x3][x4][x5][m_type]:
                                            l1_s_name = f'{s1}'
                                            l1_x_name = f'{x1}'
                                            l1_name = l1_x_name + '_to_' + l1_s_name + '_bbtu'
                                            l1_value = 0
                                            for s2 in split_dict[x1][x2][x3][x4][x5][m_type][s1]:
                                                l2_s_name = f'{s1}_{s2}'
                                                l2_x_name = f'{x1}_{x2}'
                                                l2_name = l2_x_name + '_to_' + l2_s_name + '_bbtu'
                                                l2_value = 0
                                                for s3 in split_dict[x1][x2][x3][x4][x5][m_type][s1][s2]:
                                                    l3_s_name = f'{s1}_{s2}_{s3}'
                                                    l3_x_name = f'{x1}_{x2}_{x3}'
                                                    l3_name = l3_x_name + '_to_' + l3_s_name + '_bbtu'
                                                    l3_value = 0
                                                    for s4 in \
                                                            split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][s3]:
                                                        l4_s_name = f'{s1}_{s2}_{s3}_{s4}'
                                                        l4_x_name = f'{x1}_{x2}_{x3}_{x4}'
                                                        l4_name = l4_x_name + '_to_' + l4_s_name + '_bbtu'
                                                        l4_value = 0
                                                        for s5 in \
                                                                split_dict[x1][x2][x3][x4][x5][m_type][s1][s2][
                                                                    s3][
                                                                    s4]:
                                                            l5_s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}'
                                                            l5_x_name = f'{x1}_{x2}_{x3}_{x4}_{x5}'
                                                            l5_name = l5_x_name + '_to_' + l5_s_name + '_bbtu'
                                                            for p in \
                                                                    split_dict[x1][x2][x3][x4][x5][m_type][s1][
                                                                        s2][
                                                                        s3][s4][s5]:
                                                                frac_name = l5_x_name + '_to_' + l5_s_name + '_fraction'
                                                                if frac_name in df.columns:
                                                                    frac = df[frac_name]
                                                                else:
                                                                    frac = \
                                                                        split_dict[x1][x2][x3][x4][x5][m_type][
                                                                            s1][s2][s3][s4][s5][p]
                                                                l5_value = l5_energy_value * frac

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
