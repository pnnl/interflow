from interflow.reader import *


def construct_nested_dictionary(df: pd.DataFrame) -> dict:
    """Takes in a 16 column DataFrame of values and returns a nested dictionary

            :param df:                        dataframe of values to convert to nested dictionary
            :type df:                         DataFrame

            :return:                          Nested dictionary of dataframe values

            """

    # check number of columns in DataFrame and build appropriate number of nests if greater than 12 columns
    if len(df.columns) < 16:
        d = 'Not enough columns passed to dictionary. Expects 16 columns in input dataframe'
        raise ValueError(d)

    # 16 column dataframes
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
            lambda a: dict(a.groupby(group2, sort=False).apply(
            lambda b: dict(b.groupby(group3, sort=False).apply(
            lambda c: dict(c.groupby(group4, sort=False).apply(
            lambda d: dict(d.groupby(group5, sort=False).apply(
            lambda e: dict(e.groupby(group6, sort=False).apply(
            lambda f: dict(f.groupby(group7, sort=False).apply(
            lambda g: dict(g.groupby(group8, sort=False).apply(
            lambda h: dict(h.groupby(group9, sort=False).apply(
            lambda i: dict(i.groupby(group10, sort=False).apply(
            lambda k: dict(k.groupby(group11, sort=False).apply(
            lambda l: dict(l.groupby(group12, sort=False).apply(
            lambda m: dict(m.groupby(group13, sort=False).apply(
            lambda n: dict(n.groupby(group14, sort=False).apply(
            lambda x: dict(zip(x[parameter], x[value])))))))))))))))))))))))))))))
        d = d.to_dict()

    else:
        d = 'Too many columns in dataframe. Expects 16 columns'
        raise ValueError(d)

    return d








