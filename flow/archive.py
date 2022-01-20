def calc_electricity_rejected_energy(data: pd.DataFrame, generation_types=None, regions=3,
                                         generation_efficiency=.30, total=False):

    for type in generation_type_list:
        fuel_type = type + "_fuel_bbtu"
        gen_type = type + "_gen_bbtu"

        if (fuel_type in df.columns) and (gen_type in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] - df[gen_type]
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
        elif (fuel_type in df.columns) and (gen_type not in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 - generation_efficiency)
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')
        elif (fuel_type not in df.columns) and (gen_type in df.columns):
            df[f'electricity_{type}_rejected_energy_bbtu'] = df[fuel_type] * (1 / (1 - generation_efficiency))
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                     + df[f'electricity_{type}_rejected_energy_bbtu']
            retain_list.append(f'electricity_{type}_rejected_energy_bbtu')

        else:
            df[f'electricity_{type}_rejected_energy_bbtu'] = 0
            df['electricity_rejected_energy_bbtu'] = df['electricity_rejected_energy_bbtu'] \
                                                     + df[f'electricity_{type}_rejected_energy_bbtu']

    if total:
        column_list = df.columns[:regions].tolist()
        column_list.append('electricity_rejected_energy_bbtu')
        df = df[column_list]
    else:
        column_list = df.columns[:regions].tolist()
        for item in retain_list:
            column_list.append(item)
        column_list.append('electricity_rejected_energy_bbtu')
        df = df[column_list]

    return df