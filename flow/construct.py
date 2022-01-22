import numpy as np
import pandas as pd
from .reader import *
import flow.clean as cl
import flow.configure as co

def calc_dictionary_levels(d:dict):
    nest_count = max(calc_dictionary_levels(v) if isinstance(v, dict) else 0 for v in d.values()) + 1

    return nest_count


def construct_nested_dictionary(df: pd.DataFrame):

    if len(df.columns) == 1:
        d = df[df.columns[0]].to_list()

    elif len(df.columns) == 2:
        d = 'Not enough columns passed to construct dictionary'

    elif len(df.columns) == 3:
        group1 = df.columns[0]
        group2 = df.columns[1]
        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(lambda x: dict(zip(x[parameter], x[value])))
        d = d.to_dict()

    elif len(df.columns) == 4:
        group1 = df.columns[0]
        group2 = df.columns[1]
        parameter = df.columns[-2]
        value = df.columns[-1]

        d = df.groupby(group1).apply(lambda a: dict(a.groupby(group2).apply(lambda x: dict(zip(x[parameter], x[value])))))
        d = d.to_dict()

    elif len(df.columns) == 5:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        parameter = df.columns[-2]
        value = df.columns[-1]

        d = df.groupby(group1).apply(lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(lambda x: dict(zip(x[parameter], x[value])))))))
        d = d.to_dict()

    elif len(df.columns) == 6:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(lambda a: dict(a.groupby(group2).apply(lambda b: dict(b.groupby(group3).apply(
            lambda b: dict(b.groupby(group4).apply(lambda x: dict(zip(x[parameter], x[value])))))))))
        d = d.to_dict()

    elif len(df.columns) == 7:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        group5 = df.columns[4]
        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(
            lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(
            lambda b: dict(b.groupby(group4).apply(
            lambda b: dict(b.groupby(group5).apply(
                lambda x: dict(zip(x[parameter], x[value])))))))))))
        d = d.to_dict()

    elif len(df.columns) == 8:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        group5 = df.columns[4]
        group6 = df.columns[5]
        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(
            lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(
            lambda b: dict(b.groupby(group4).apply(
            lambda b: dict(b.groupby(group5).apply(
            lambda b: dict(b.groupby(group6).apply(
                lambda x: dict(zip(x[parameter], x[value])))))))))))))
        d = d.to_dict()

    else:
        d = 'Too many columns in dataframe'

    return d


def convert_mwh_bbtu(x: float) -> float:
    """converts MWh to billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.003412

    return bbtu


def convert_kwh_bbtu(x: float) -> float:
    """converts kWh to billion btu.

    :return:                Value in bbtu

    """
    bbtu = x * 0.000003412140

    return bbtu


def calc_population_county_weight(df: pd.DataFrame) -> pd.DataFrame:

    """calculates the percentage of state total population by county and merges to provided dataframe
    by 'State'

    :return:                DataFrame of water consumption fractions for various sectors by county

    """
    df_state = cl.prep_water_use_2015(variables=["FIPS", "State", "County", "population"])
    df_state_sum = df_state.groupby("State", as_index=False).sum()
    df_state_sum = df_state_sum.rename(columns={"population": "state_pop_sum"})
    df_state = pd.merge(df_state, df_state_sum, how='left', on='State')
    df_state['pop_weight'] = df_state['population'] / df_state['state_pop_sum']
    df_state = df_state[['FIPS', 'State', 'County', 'pop_weight']]

    df_state = pd.merge(df, df_state, how="left", on="State")

    return df_state