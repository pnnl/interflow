from .reader import *


def construct_nested_dictionary(df: pd.DataFrame):
    """Takes in a DataFrame of values and returns a nested dictionary up to the number of columns provided

            :param df:                        dataframe of values to convert to nested dictionary
            :type df:                         DataFrame

            :return:                          Nested dictionary of dataframe values

            """

    # check number of columns in DataFrame and build appropriate number of nests if greater than 12 columns
    if len(df.columns) < 12:
        d = 'Not enough columns passed to construct dictionary'

    # 12 column dataframes
    elif len(df.columns) == 12:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        group5 = df.columns[4]
        group6 = df.columns[5]
        group7 = df.columns[6]
        group8 = df.columns[7]
        group9 = df.columns[8]
        group10 = df.columns[9]

        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(
            lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(
            lambda c: dict(c.groupby(group4).apply(
            lambda d: dict(d.groupby(group5).apply(
            lambda e: dict(e.groupby(group6).apply(
            lambda f: dict(f.groupby(group7).apply(
            lambda g: dict(g.groupby(group8).apply(
            lambda h: dict(h.groupby(group9).apply(
            lambda i: dict(i.groupby(group10).apply(
            lambda x: dict(zip(x[parameter], x[value])))))))))))))))))))))
        d = d.to_dict()

    # 13 column dataframes
    elif len(df.columns) == 13:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        group5 = df.columns[4]
        group6 = df.columns[5]
        group7 = df.columns[6]
        group8 = df.columns[7]
        group9 = df.columns[8]
        group10 = df.columns[9]
        group11 = df.columns[10]

        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(
            lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(
            lambda c: dict(c.groupby(group4).apply(
            lambda d: dict(d.groupby(group5).apply(
            lambda e: dict(e.groupby(group6).apply(
            lambda f: dict(f.groupby(group7).apply(
            lambda g: dict(g.groupby(group8).apply(
            lambda h: dict(h.groupby(group9).apply(
            lambda i: dict(i.groupby(group10).apply(
            lambda k: dict(k.groupby(group11).apply(
            lambda x: dict(zip(x[parameter], x[value])))))))))))))))))))))))
        d = d.to_dict()

    # 14 column dataframes
    elif len(df.columns) == 14:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        group5 = df.columns[4]
        group6 = df.columns[5]
        group7 = df.columns[6]
        group8 = df.columns[7]
        group9 = df.columns[8]
        group10 = df.columns[9]
        group11 = df.columns[10]
        group12 = df.columns[11]

        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(
            lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(
            lambda c: dict(c.groupby(group4).apply(
            lambda d: dict(d.groupby(group5).apply(
            lambda e: dict(e.groupby(group6).apply(
            lambda f: dict(f.groupby(group7).apply(
            lambda g: dict(g.groupby(group8).apply(
            lambda h: dict(h.groupby(group9).apply(
            lambda i: dict(i.groupby(group10).apply(
            lambda k: dict(k.groupby(group11).apply(
            lambda k: dict(k.groupby(group12).apply(
            lambda x: dict(zip(x[parameter], x[value])))))))))))))))))))))))))
        d = d.to_dict()

    # 14 column dataframes
    elif len(df.columns) == 16:
        group1 = df.columns[0]
        group2 = df.columns[1]
        group3 = df.columns[2]
        group4 = df.columns[3]
        group5 = df.columns[4]
        group6 = df.columns[5]
        group7 = df.columns[6]
        group8 = df.columns[7]
        group9 = df.columns[8]
        group10 = df.columns[9]
        group11 = df.columns[10]
        group12 = df.columns[11]
        group13 = df.columns[12]
        group14 = df.columns[13]

        parameter = df.columns[-2]
        value = df.columns[-1]
        d = df.groupby(group1).apply(
            lambda a: dict(a.groupby(group2).apply(
            lambda b: dict(b.groupby(group3).apply(
            lambda c: dict(c.groupby(group4).apply(
            lambda d: dict(d.groupby(group5).apply(
            lambda e: dict(e.groupby(group6).apply(
            lambda f: dict(f.groupby(group7).apply(
            lambda g: dict(g.groupby(group8).apply(
            lambda h: dict(h.groupby(group9).apply(
            lambda i: dict(i.groupby(group10).apply(
            lambda k: dict(k.groupby(group11).apply(
            lambda l: dict(l.groupby(group12).apply(
            lambda m: dict(m.groupby(group13).apply(
            lambda n: dict(n.groupby(group14).apply(
            lambda x: dict(zip(x[parameter], x[value])))))))))))))))))))))))))))))
        d = d.to_dict()

    else:
        d = 'Too many columns in dataframe'

    return d


#TODO DELETE/MOVE Below
def calc_dictionary_levels(d:dict):
    nest_count = max(calc_dictionary_levels(v) if isinstance(v, dict) else 0 for v in d.values()) + 1
    return nest_count








