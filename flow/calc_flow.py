import numpy as np
from .reader import *
import flow.construct as co
import flow.deconstruct as de


def calculate(data=None, update_data = None, level=5, region_name=None):
    """Collects water demand data to water sectors (sectors whose energy demand is strictly dependent on their water
    demand) that directly withdraw their water from the water supply (e.g., public water supply) and aggregates the
    values.
    """
    # load baseline data
    if data is None:
        df = pd.read_csv(r"C:\Users\mong275\Local Files\Repos\flow\flow\data\configuration_data\test_data_01-28.csv")
    else:
        df = data
        #df = read_baseline_data()

    if region_name is None:
        df = df
    else:
        df[df.columns[0]] = df[df.columns[0]].astype(str)
        reg_col = df.columns[0]
        df = df.loc[df[reg_col] == region_name]

    c_dict = co.construct_nested_dictionary(update_data)

    f_dict = co.construct_nested_dictionary(df)

    total_dict = {}
    check_dict = {}
    discharge_dict = {}
    export_dict = {}
    import_dict = {}


    l5_dict = {}
    l4_dict = {}
    l3_dict = {}
    l2_dict = {}
    l1_dict = {}

    fraction_dict = {}
    sum_dict = {}


    # initialize values
    for r in f_dict:
        for type in f_dict[r]:
            if type == 'A_collect':
                for t1 in f_dict[r][type]:
                    s1_value = 0
                    l1_value = 0
                    t1_value = 0
                    for t2 in f_dict[r][type][t1]:
                        l2_value = 0
                        for t3 in f_dict[r][type][t1][t2]:
                            l3_value = 0
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    l4_value = 0
                                    l5_total_value = 0
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        # collect direct draw flows (water withdraws or energy demand)
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                            s1_name = f'{r}_{s1}_{u1}'
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    l5_value = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
                                                                    l4_value = l4_value + l5_value
                                                                    l3_value = l3_value + l5_value
                                                                    l2_value = l2_value + l5_value
                                                                    l1_value = l1_value + l5_value

                                                                # update output dictionaries
                                                                    l1_dict.update({l1_name: l1_value})
                                                                    l2_dict.update({l2_name: l2_value})
                                                                    l3_dict.update({l3_name: l3_value})
                                                                    l4_dict.update({l4_name: l4_value})
                                                                    l5_dict.update({l5_name: l5_value})

                                                                    l5_total_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                    l5_total_value = l5_total_value + l5_value
                                                                    total_dict.update({l5_total_name: l5_total_value})

                                                                    t1_value = t1_value + l5_value
                                                                    total_dict.update({t1_name: t1_value})

                                                                    #s1_value = s1_value + l5_value
                                                                    #total_dict.update({s1_name: s1_value})

                 # calculate the fraction of source location that feed into each target
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            if l5_name in l5_dict:
                                                                l5_fraction_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}_fraction'
                                                                l5_fraction_value = l5_dict[l5_name]/total_dict[t1_name]
                                                                fraction_dict.update({l5_fraction_name: l5_fraction_value})
                                                            else:
                                                                pass

            # calculate energy or water for water and energy sectors
            elif type == 'B_calculate':

                for t1 in f_dict[r][type]:
                    l5t_value_total = 0
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                    intensity = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
                                                                    if l5s_name in total_dict:
                                                                        l5s_value = total_dict[l5s_name]  # flow value it's based on
                                                                        l5t_value = l5s_value * intensity  # calculated value
                                                                        l5t_value_total = l5t_value_total + l5t_value  # calculated total
                                                                        total_dict.update({l5t_name: l5t_value_total})
                                                                    else:
                                                                        pass

                                    # split water and energy values into individual sources
            elif type == 'C_source':
                l5_s_value = 0
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                            sl1_value = 0
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                sl2_value = 0
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                    sl3_value = 0
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                        sl4_value = 0
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'

                                                            # PWD_total_total_total_total_mgd
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    # if it's not blank
                                                                    if f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p] > 0:
                                                                        if l5t_name in total_dict:
                                                                            l5t_value = total_dict[l5t_name]
                                                                            fraction = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
                                                                            sl5_value = l5t_value * fraction
                                                                            sl4_value = sl4_value + sl5_value
                                                                            sl3_value = sl3_value + sl5_value
                                                                            sl2_value = sl2_value + sl5_value
                                                                            sl1_value = sl1_value + sl5_value
                                                                            # update output dictionaries
                                                                            l1_dict.update({l1_name: sl1_value})
                                                                            l2_dict.update({l2_name: sl2_value})
                                                                            l3_dict.update({l3_name: sl3_value})
                                                                            l4_dict.update({l4_name: sl4_value})
                                                                            l5_dict.update({l5_name: sl5_value})


                                                                            l5_s_value = l5_s_value + sl5_value
                                                                            total_dict.update({l5s_name: l5_s_value})

                                                                        else:
                                                                            pass
                                                                    else:
                                                                        if l5t_name in total_dict:
                                                                            l5t_value = total_dict[l5t_name]
                                                                            l5_fraction_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}_fraction'

                                                                            fraction = fraction_dict[l5_fraction_name]
                                                                            sl5_value = l5t_value * fraction
                                                                            sl4_value = sl4_value + sl5_value
                                                                            sl3_value = sl3_value + sl5_value
                                                                            sl2_value = sl2_value + sl5_value
                                                                            sl1_value = sl1_value + sl5_value
                                                                            # update output dictionaries
                                                                            l1_dict.update({l1_name: sl1_value})
                                                                            l2_dict.update({l2_name: sl2_value})
                                                                            l3_dict.update({l3_name: sl3_value})
                                                                            l4_dict.update({l4_name: sl4_value})
                                                                            l5_dict.update({l5_name: sl5_value})

                                                                            check_dict.update({l5t_name: l5t_value})
                                                                            check_dict.update({l5_name: sl5_value})

            elif type == 'D_discharge':

                for t1 in f_dict[r][type]:
                    l5_s_value = 0
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:

                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:

                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{t1}_to_{s1}_{u1}'
                                            dl1_value = 0
                                            for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                l2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
                                                dl2_value = 0
                                                for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                    l3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
                                                    dl3_value = 0
                                                    for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                        l4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
                                                        dl4_value = 0
                                                        for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                l5s_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    if l5t_name in total_dict:
                                                                        l5t_value = total_dict[l5t_name]
                                                                        fraction = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]

                                                                        # calculate split to discharge
                                                                        dl5_value = l5t_value * fraction
                                                                        dl4_value = dl4_value + dl5_value
                                                                        dl3_value = dl3_value + dl5_value
                                                                        dl2_value = dl2_value + dl5_value
                                                                        dl1_value = dl1_value + dl5_value

                                                                    # update output dictionaries
                                                                        l1_dict.update({l1_name: dl1_value})
                                                                        l2_dict.update({l2_name: dl2_value})
                                                                        l3_dict.update({l3_name: dl3_value})
                                                                        l4_dict.update({l4_name: dl4_value})
                                                                        l5_dict.update({l5_name: dl5_value})

                                                                        l5_s_value = l5_s_value + dl5_value
                                                                        total_dict.update({l5s_name:l5_s_value})
                                                                    else:
                                                                        pass
                                # calculate the fraction of source location that feed into each target
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                        t1_name = f'{r}_{t1}_{u1}'
                                        if t1_name in total_dict:
                                            for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                                for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
                                                    for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                if l5_name in l5_dict:
                                                                    l5_fraction_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}_fraction'
                                                                    l5_fraction_value = l5_dict[l5_name] / \
                                                                                        total_dict[t1_name]
                                                                    fraction_dict.update({l5_fraction_name: l5_fraction_value})
                                                                else:
                                                                    pass
                                        else:
                                            pass
    for r in c_dict:
        for set in c_dict[r]:
            for type in c_dict[r][set]:
                #left split (need to add right split)
                if type == 'match':
                    for t1 in c_dict[r][set][type]:
                        for t2 in c_dict[r][set][type][t1]:
                            for t3 in c_dict[r][set][type][t1][t2]:
                                for t4 in c_dict[r][set][type][t1][t2][t3]:
                                    for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
                                        for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
                                            t_total_name = f'{r}_{t1}_{u1}'
                                            t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                            t5_frac_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}_fraction'
                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                s5_total_name = f'{r}_{s1}_{u1}'
                                                                s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                s5_frac_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}_fraction'

                                                                # calculate s fraction ( don't need frac function anymore)
                                                                t5_value = total_dict[t5_name]
                                                                s5_value = total_dict[s5_name]
                                                                s5_total_value = total_dict[s5_total_name]
                                                                s5_fraction = s5_value/s5_total_value

                                                                # calculate t5 amount * fraction
                                                                t5_split_value = t5_value * s5_fraction

                                                                # if the flows are equal
                                                                if t5_split_value == s5_value:
                                                                    l5_dict.update({t_s_5_name: t5_split_value})

                                                                # if the inflow is greater
                                                                elif t5_split_value > s5_value:
                                                                    l5_dict.update({t_s_5_name: s5_value})
                                                                    export_value = t5_split_value - s5_value
                                                                    export_dict.update({t5_name:export_value})

                                                                # if the inflow is smaller
                                                                else:
                                                                    l5_dict.update({t_s_5_name: t5_split_value})
                                                                    import_value = s5_value - t5_split_value
                                                                    import_dict.update({s5_name: import_value})
                elif type == 'export':
                    for t1 in c_dict[r][set][type]:
                        for t2 in c_dict[r][set][type][t1]:
                            for t3 in c_dict[r][set][type][t1][t2]:
                                for t4 in c_dict[r][set][type][t1][t2][t3]:
                                    for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
                                        for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
                                            t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                if t5_name in export_dict:
                                                                    flow_value = export_dict[t5_name]
                                                                    l5_dict.update({t_s_5_name:flow_value})
                                                                else:
                                                                    pass
                elif type == 'import':
                    for t1 in c_dict[r][set][type]:
                        for t2 in c_dict[r][set][type][t1]:
                            for t3 in c_dict[r][set][type][t1][t2]:
                                for t4 in c_dict[r][set][type][t1][t2][t3]:
                                    for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
                                        for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
                                                                s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
                                                                if s5_name in import_dict:
                                                                    flow_value = import_dict[s5_name]
                                                                    l5_dict.update({t_s_5_name: flow_value})
                                                                else:
                                                                    pass
                else:
                    pass
                                                                




    #        for t1 in f_dict[r][type]:
    #            for t2 in f_dict[r][type][t1]:
    #                for t3 in f_dict[r][type][t1][t2]:
    #                    for t4 in f_dict[r][type][t1][t2][t3]:
    #                        for t5 in f_dict[r][type][t1][t2][t3][t4]:
    #                            for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
    #                                for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
    #                                    for s2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                        for s3 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                            for s4 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                for s5 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                    l5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                    if l5_name in l5_dict:
    #                                                        sum_dict.update({l5_name: l5_dict[l5_name]})
    #                                                    else:
    #                                                        pass

    ## create a dataframe to sum values by target to link disconnected nodes
    #sum_df = de.deconstruct_nested_dictionary(sum_dict)
    #group_column_list = ['region', 'T1','T2','T3','T4','T5','units']
    #sum_df = sum_df.groupby(group_column_list, as_index=False).sum()
    #for col in group_column_list[:-1]:
    #    sum_df[col] = sum_df[col] + '_'
    #sum_df['l5_sum_name'] = sum_df[group_column_list].sum(axis=1)
    #sum_dict = dict(zip(sum_df.l5_sum_name, sum_df.value))
    #
    #for r in c_dict:
    #    for set in c_dict[r]:
    #        for type in c_dict[r][set]:
    #            if type == 'build':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            l1_loop_name = f'{r}_{t1}_to_{t1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                l2_loop_name = f'{r}_{t1}_{t2}_to_{t1}_{t2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    l3_loop_name = f'{r}_{t1}_{t2}_{t3}_to_{t1}_{t2}_{t3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        l4_loop_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #
    #                                                            # anything that's left in the loop after subtracting earlier
    #                                                            # assign to new flow name
    #                                                            l5_loop_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                                            if l5_loop_name in l5_dict:
    #                                                                l5_loop_value = l5_dict[l5_loop_name]
    #                                                                l5_dict.update({t_s_5_name: l5_loop_value})
    #                                                                del l5_dict[l5_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l4_loop_name in l4_dict:
    #                                                                l4_loop_value = l4_dict[l4_loop_name]
    #                                                                l4_dict.update({t_s_4_name: l4_loop_value})
    #                                                                del l4_dict[l4_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l3_loop_name in l3_dict:
    #                                                                l3_loop_value = l3_dict[l3_loop_name]
    #                                                                l3_dict.update({t_s_3_name: l3_loop_value})
    #                                                                del l3_dict[l3_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l2_loop_name in l2_dict:
    #                                                                l2_loop_value = l2_dict[l2_loop_name]
    #                                                                l2_dict.update({t_s_2_name: l2_loop_value})
    #                                                                del l2_dict[l2_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l1_loop_name in l1_dict:
    #                                                                l1_loop_value = l1_dict[l1_loop_name]
    #                                                                l1_dict.update({t_s_1_name: l1_loop_value})
    #                                                                del l1_dict[l1_loop_name]
    #                                                            else:
    #                                                                pass
    #
    #
    #            elif type == 'match':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                        if t5_name in sum_dict:
    #                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                                t_s_1_value = 0
    #                                                l1_loop_name = f'{r}_{s1}_to_{s1}_{u1}'
    #                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                    t_s_2_value = 0
    #                                                    l2_loop_name = f'{r}_{s1}_{s2}_to_{s1}_{s2}_{u1}'
    #                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                        t_s_3_value = 0
    #                                                        l3_loop_name = f'{r}_{s1}_{s2}_{s3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                            t_s_4_value = 0
    #                                                            l4_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                                s5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                if s5_name in total_dict:
    #                                                                    s5_fraction_name = s5_name + '_fraction'
    #                                                                    t5_split_value = sum_dict[t5_name] * fraction_dict[s5_fraction_name]
    #                                                                    flow_value = min(t5_split_value, total_dict[s5_name])
    #
    #                                                                    l5_dict.update({t_s_5_name: flow_value})
    #                                                                    t_s_4_value = t_s_4_value + flow_value
    #                                                                    t_s_3_value = t_s_3_value + flow_value
    #                                                                    t_s_2_value = t_s_2_value + flow_value
    #                                                                    t_s_1_value = t_s_1_value + flow_value
    #
    #                                                                    l4_dict.update({t_s_4_name: t_s_4_value})
    #                                                                    l3_dict.update({t_s_3_name: t_s_3_value})
    #                                                                    l2_dict.update({t_s_2_name: t_s_2_value})
    #                                                                    l1_dict.update({t_s_1_name: t_s_1_value})
    #
    #
    #                                                                    # save value to discharge dictionary
    #                                                                    discharge_dict.update({t5_name: flow_value})
    #
    #                                                                    #remove value from looped variable at all levels
    #                                                                    l5_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                    if l5_loop_name in l5_dict:
    #                                                                        l5_loop_value = l5_dict[l5_loop_name]
    #                                                                        if l5_loop_value - flow_value <= 0:
    #                                                                            l5_dict.update({l5_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l5_loop_value - flow_value
    #                                                                            l5_dict.update({l5_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l4_loop_name in l4_dict:
    #                                                                        l4_loop_value = l4_dict[l4_loop_name]
    #                                                                        if l4_loop_value - t_s_4_value <= 0:
    #                                                                            l4_dict.update({l4_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l4_loop_value - t_s_4_value
    #                                                                            l4_dict.update(
    #                                                                                {l4_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l3_loop_name in l3_dict:
    #                                                                        l3_loop_value = l3_dict[l3_loop_name]
    #                                                                        if l3_loop_value - t_s_3_value <= 0:
    #                                                                            l3_dict.update({l3_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l3_loop_value - t_s_3_value
    #                                                                            l3_dict.update(
    #                                                                                {l3_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l2_loop_name in l2_dict:
    #                                                                        l2_loop_value = l2_dict[l2_loop_name]
    #                                                                        if l2_loop_value - t_s_2_value <= 0:
    #                                                                            l2_dict.update({l2_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l2_loop_value - t_s_2_value
    #                                                                            l2_dict.update(
    #                                                                                {l2_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #                                                                    if l1_loop_name in l1_dict:
    #                                                                        l1_loop_value = l1_dict[l1_loop_name]
    #                                                                        if l1_loop_value - t_s_1_value <= 0:
    #                                                                            l1_dict.update({l1_loop_name: 0})
    #                                                                        else:
    #                                                                            updated_value = l1_loop_value - t_s_1_value
    #                                                                            l1_dict.update(
    #                                                                                {l1_loop_name: updated_value})
    #                                                                    else:
    #                                                                        pass
    #
    #
    #            elif type == 'replace':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                            t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                            l1_loop_name = f'{r}_{s1}_to_{s1}_{u1}'
    #                                            for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                l2_loop_name = f'{r}_{s1}_{s2}_to_{s1}_{s2}_{u1}'
    #                                                for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                    t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    l3_loop_name = f'{r}_{s1}_{s2}_{s3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                    for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                        t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        l4_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                        for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                            t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #
    #                                                            # anything that's left in the loop after subtracting earlier
    #                                                            # assign to new flow name
    #                                                            l5_loop_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                            if l5_loop_name in l5_dict:
    #                                                                l5_loop_value = l5_dict[l5_loop_name]
    #                                                                l5_dict.update({t_s_5_name: l5_loop_value})
    #                                                                del l5_dict[l5_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l4_loop_name in l4_dict:
    #                                                                l4_loop_value = l4_dict[l4_loop_name]
    #                                                                l4_dict.update({t_s_4_name: l4_loop_value})
    #                                                                del l4_dict[l4_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l3_loop_name in l3_dict:
    #                                                                l3_loop_value = l3_dict[l3_loop_name]
    #                                                                l3_dict.update({t_s_3_name: l3_loop_value})
    #                                                                del l3_dict[l3_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l2_loop_name in l2_dict:
    #                                                                l2_loop_value = l2_dict[l2_loop_name]
    #                                                                l2_dict.update({t_s_2_name: l2_loop_value})
    #                                                                del l2_dict[l2_loop_name]
    #                                                            else:
    #                                                                pass
    #                                                            if l1_loop_name in l1_dict:
    #                                                                l1_loop_value = l1_dict[l1_loop_name]
    #                                                                l1_dict.update({t_s_1_name: l1_loop_value})
    #                                                                del l1_dict[l1_loop_name]
    #                                                            else:
    #                                                                pass
    #
    #            elif type == 'surplus':
    #                for t1 in c_dict[r][set][type]:
    #                    for t2 in c_dict[r][set][type][t1]:
    #                        for t3 in c_dict[r][set][type][t1][t2]:
    #                            for t4 in c_dict[r][set][type][t1][t2][t3]:
    #                                for t5 in c_dict[r][set][type][t1][t2][t3][t4]:
    #                                    for u1 in c_dict[r][set][type][t1][t2][t3][t4][t5]:
    #                                        t5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
    #                                        if t5_name in sum_dict:
    #                                            for s1 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1]:
    #                                                l1_surplus_value = 0
    #                                                t_s_1_name = f'{r}_{t1}_to_{s1}_{u1}'
    #                                                for s2 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1]:
    #                                                    l2_surplus_value = 0
    #                                                    t_s_2_name = f'{r}_{t1}_{t2}_to_{s1}_{s2}_{u1}'
    #                                                    for s3 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2]:
    #                                                        l3_surplus_value = 0
    #                                                        t_s_3_name = f'{r}_{t1}_{t2}_{t3}_to_{s1}_{s2}_{s3}_{u1}'
    #                                                        for s4 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3]:
    #                                                            l4_surplus_value = 0
    #                                                            t_s_4_name = f'{r}_{t1}_{t2}_{t3}_{t4}_to_{s1}_{s2}_{s3}_{s4}_{u1}'
    #                                                            for s5 in c_dict[r][set][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4]:
    #                                                                t_s_5_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_to_{s1}_{s2}_{s3}_{s4}_{s5}_{u1}'
    #                                                                if t5_name in discharge_dict:
    #                                                                    discharge_value = discharge_dict[t5_name]
    #                                                                    inflow_value = sum_dict[t5_name]
    #                                                                    if discharge_value < inflow_value:
    #                                                                        l5_surplus_value = inflow_value - discharge_value
    #                                                                        l5_dict.update({t_s_5_name: l5_surplus_value})
    #
    #                                                                        l4_surplus_value = l4_surplus_value + l5_surplus_value
    #                                                                        l3_surplus_value = l3_surplus_value + l5_surplus_value
    #                                                                        l2_surplus_value = l2_surplus_value + l5_surplus_value
    #                                                                        l1_surplus_value = l1_surplus_value + l5_surplus_value
    #
    #                                                                        l4_dict.update({t_s_4_name: l4_surplus_value})
    #                                                                        l3_dict.update({t_s_3_name: l3_surplus_value})
    #                                                                        l2_dict.update({t_s_2_name: l2_surplus_value})
    #                                                                        l1_dict.update({t_s_1_name: l1_surplus_value})
    #
    #                                                                    else:
    #                                                                        pass
    #
    #            else:
    #                pass


    # TODO add updater that runs this, updates a copy of the data, reruns this
    # run.py function should run the updater and then deconstruct the output, take below

    # return output at specified level of granularity
    if level == 1:
        df = de.deconstruct_nested_dictionary(l1_dict)
    elif level == 2:
        df = de.deconstruct_nested_dictionary(l2_dict)
    elif level == 3:
        df = de.deconstruct_nested_dictionary(l3_dict)
    elif level == 4:
        df = de.deconstruct_nested_dictionary(l4_dict)
    elif level == 5:
        df = de.deconstruct_nested_dictionary(l5_dict)
    else:
        m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
        raise ValueError(m)

    return total_dict
