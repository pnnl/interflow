from .reader import *
import flow.construct as co

def calc_water_sector_water(data=None, level=5):
    """Collects water demand data to water sectors (sectors whose energy demand is strictly dependent on their water
    demand) that directly withdraw their water from the water supply (e.g., public water supply) and aggregates the
    values.
    """
    # load baseline data
    if data:
        df = data
    else:
        df = read_baseline_data()

    f_dict = {}


    total_dict = {}

    l5_dict = {}
    l4_dict = {}
    l3_dict = {}
    l2_dict = {}
    l1_dict = {}

    for r in f_dict:
        for t1 in f_dict[r]:
            for t2 in f_dict[r][t1]:
                for t3 in f_dict[r][t1][t2]:
                    for t4 in f_dict[r][t1][t2][t3]:
                        for t5 in f_dict[r][t1][t2][t3][t4]:
                            for u1 in f_dict[r][t1][t2][t3][t4][t5]:
                                for type in f_dict[r][t1][t2][t3][t4][t5][u1]:

                                    # collect direct draw flows (water withdraws or energy demand)
                                    if type == 'collect':
                                        for s1 in f_dict[r][t1][t2][t3][t4][t5][u1][type]:
                                            l1_value = 0
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1]:
                                                l2_value = 0
                                                l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2]:
                                                    l3_value = 0
                                                    l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3]:
                                                        l4_value = 0
                                                        l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4]:
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2]:
                                                                    l5_value = f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2][p]
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
                                    elif type == 'calculate':
                                        l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                        for s1 in f_dict[r][t1][t2][t3][t4][t5][u1][type]:
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1]:
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2]:
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3]:
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4]:
                                                            for u2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2]:
                                                                    l5s_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_{u2}'
                                                                    intensity = f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2][p]
                                                                    l5s_value = total_dict[l5s_name]
                                                                    l5t_value = l5s_value * intensity
                                                                    total_dict.update({l5t_name: l5t_value})



                                    # split water and energy values into individual sources
                                    elif type == 'source':
                                        for u in f_dict[r][t1][t2][t3][t4][t5][u1][type]:
                                            for s1 in f_dict[r][t1][t2][t3][t4][t5][u1][type]:
                                                l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                                l1_value = 0
                                                for s2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1]:
                                                    l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                    l2_value = 0
                                                    for s3 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2]:
                                                        l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                        l3_value = 0
                                                        for s4 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3]:
                                                            l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                            l4_value = 0
                                                            for s5 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4]:
                                                                l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                                for u2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5]:
                                                                    for p in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2]:
                                                                        l5t_value = total_dict[l5t_name]
                                                                        fraction = f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2][p]
                                                                        l5_value = l5t_value * fraction
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

                                    elif type == 'discharge':
                                        for u in f_dict[r][t1][t2][t3][t4][t5][u1][type]:
                                            for s1 in f_dict[r][t1][t2][t3][t4][t5][u1][type]:
                                            l1_name = f'{r}_{s1}_to_{t1}_{u1}'
                                            l1_value = 0
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1]:
                                                l2_name = f'{r}_{s1}_{s2}_to_{t1}_{t2}_{u1}'
                                                l2_value = 0
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2]:
                                                    l3_name = f'{r}_{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u1}'
                                                    l3_value = 0
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3]:
                                                        l4_name = f'{r}_{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u1}'
                                                        l4_value = 0
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4]:
                                                            l5t_name = f'{r}_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            l5_name = f'{r}_{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u1}'
                                                            for u2 in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5]:
                                                                for p in f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2]:
                                                                    l5t_value = total_dict[l5t_name]
                                                                    fraction = f_dict[r][t1][t2][t3][t4][t5][u1][type][s1][s2][s3][s4][s5][u2][p]
                                                                    l5_value = l5t_value * fraction
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

                                else:
                                    pass