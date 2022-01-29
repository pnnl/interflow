from .reader import *
import flow.construct as co

def calc_water_sector_water(data=None, level=5, regions=3):
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

    #TODO might need to add region to level identifier

    total_dict = df[df.columns[:regions].tolist()].to_dict()

    l5_dict = df[df.columns[:regions].tolist()].to_dict()
    l4_dict = df[df.columns[:regions].tolist()].to_dict()
    l3_dict = df[df.columns[:regions].tolist()].to_dict()
    l2_dict = df[df.columns[:regions].tolist()].to_dict()
    l1_dict = df[df.columns[:regions].tolist()].to_dict()

    for r in f_dict:
        for t1 in f_dict[r]:
            for t2 in f_dict[r][t1]:
                for t3 in f_dict[r][t1][t2]:
                    for t4 in f_dict[r][t1][t2][t3]:
                        for t5 in f_dict[r][t1][t2][t3][t4]:
                            for type in f_dict[r][t1][t2][t3][t4][t5]:
                                if type == 'collect':
                                    for u in f_dict[r][t1][t2][t3][t4][t5][type]:
                                        for s1 in f_dict[r][t1][t2][t3][t4][t5][type][u]:
                                            l1_value = 0
                                            l1_name = f'{s1}_to_{t1}_{u}'
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][type][s1][u]:
                                                l2_value = 0
                                                l2_name = f'{s1}_{s2}_to_{t1}_{t2}_{u}'
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][u]:
                                                    l3_value = 0
                                                    l3_name = f'{s1}_{s2}_{s3}_to_{t1}_{t2}_{t3}_{u}'
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][u]:
                                                        l4_value = 0
                                                        l4_name = f'{s1}_{s2}_{s3}_{s4}_to_{t1}_{t2}_{t3}_{t4}_{u}'
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][u]:
                                                            l5_name = f'{s1}_{s2}_{s3}_{s4}_{s5}_to_{t1}_{t2}_{t3}_{t4}_{t5}_{u}'
                                                            for p in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][s5][u]:
                                                                l5_value = f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][s5][u][p]
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

                                                                l5_total_name = {t1}_{t2}_{t3}_{t4}_{t5}_{u}
                                                                l5_total_value =



                                elif type == 'calculate':
                                    for u in f_dict[r][t1][t2][t3][t4][t5][type]
                                        for s1 in f_dict[r][t1][t2][t3][t4][t5][type][u]:
                                            l1_name = f'{s1}_to_{t1}'
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][type][s1][u]:
                                                l2_name = f'{s1}_{s2}_to_{t1}_{t2}'
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][u]:
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][u]:
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][u]:
                                                            for p in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][s5][u]:





                                elif type == 'source':
                                    for u in f_dict[r][t1][t2][t3][t4][t5][type]
                                        for s1 in f_dict[r][t1][t2][t3][t4][t5][type][u]:
                                            l1_name = f'{s1}_to_{t1}'
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][type][s1][u]:
                                                l2_name = f'{s1}_{s2}_to_{t1}_{t2}'
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][u]:
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][u]:
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][u]:
                                                            for p in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][s5][u]:




                                elif type == 'discharge':
                                    for u in f_dict[r][t1][t2][t3][t4][t5][type]
                                        for s1 in f_dict[r][t1][t2][t3][t4][t5][type][u]:
                                            l1_name = f'{s1}_to_{t1}'
                                            for s2 in f_dict[r][t1][t2][t3][t4][t5][type][s1][u]:
                                                l2_name = f'{s1}_{s2}_to_{t1}_{t2}'
                                                for s3 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][u]:
                                                    for s4 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][u]:
                                                        for s5 in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][u]:
                                                            for p in f_dict[r][t1][t2][t3][t4][t5][type][s1][s2][s3][s4][s5][u]:




                                else:
                                    pass