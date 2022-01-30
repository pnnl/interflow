from .reader import *
import flow.construct as co
import flow.deconstruct as de


def calculate(data=None, level=5):
    """Collects water demand data to water sectors (sectors whose energy demand is strictly dependent on their water
    demand) that directly withdraw their water from the water supply (e.g., public water supply) and aggregates the
    values.
    """
    # load baseline data
    if data:
        df = data
    else:
        #df = read_baseline_data()
        df = pd.read_csv(r"C:\Users\mong275\Local Files\Repos\flow\flow\data\configuration_data\test_data_01-28.csv")

    f_dict = co.construct_nested_dictionary(df)

    total_dict = {}

    l5_dict = {}
    l4_dict = {}
    l3_dict = {}
    l2_dict = {}
    l1_dict = {}

    # initialize values
    for r in f_dict:
        for type in f_dict[r]:
            if type == 'A_collect':
                for t1 in f_dict[r][type]:
                    l1_value = 0
                    for t2 in f_dict[r][type][t1]:
                        l2_value = 0
                        for t3 in f_dict[r][type][t1][t2]:
                            l3_value = 0
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    l4_value = 0
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
                                    # collect direct draw flows (water withdraws or energy demand)
                                        for s1 in f_dict[r][type][t1][t2][t3][t4][t5][u1]:
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
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
                                                                    l5_total_value = l5_value
                                                                    total_dict.update({l5_total_name: l5_total_value})
                                    # calculate energy or water for water and energy sectors
            elif type == 'B_calculate':
                for t1 in f_dict[r][type]:
                    for t2 in f_dict[r][type][t1]:
                        for t3 in f_dict[r][type][t1][t2]:
                            for t4 in f_dict[r][type][t1][t2][t3]:
                                for t5 in f_dict[r][type][t1][t2][t3][t4]:
                                    for u1 in f_dict[r][type][t1][t2][t3][t4][t5]:
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
                                                                    l5s_value = total_dict[l5s_name]
                                                                    l5t_value = l5s_value * intensity
                                                                    total_dict.update({l5t_name: l5t_value})



                                    # split water and energy values into individual sources
            elif type == 'C_source':
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
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
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

            elif type == 'D_discharge':
                for t1 in f_dict[r][type]:
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
                                                                for p in f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2]:
                                                                    l5t_value = total_dict[l5t_name]
                                                                    fraction = f_dict[r][type][t1][t2][t3][t4][t5][u1][s1][s2][s3][s4][s5][u2][p]
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

                                else:
                                    pass

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

    return df
