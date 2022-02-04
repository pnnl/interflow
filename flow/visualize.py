import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from .calculate import *
from .analyze import *

def plot_bar(data, x, y, region, y_axis="Value", x_axis_title="Region",  y_axis_title="Value"):
    """Plot the results of a cerf run on a map where each technology has its own color.
    :param df:                       Result data frame from running 'cerf.run()'
    :type df:                        DataFrame
    :param boundary_shp:                    Full path to a boundary shapefile with file name and extension.  If no file
                                            provided, the default boundary for the CONUS will be used.
    :type boundary_shp:                     str
    :param regions_shp:                     Full path to a regions shapefile with file name and extension.  If no file
                                            provided, the default regions for the CONUS will be used.
    :type regions_shp:                      str
    :param column:                          Column to plot
    :type column:                           str
    :param markersize:                      Size of power plant marker
    :type markersize:                       int
    :param cmap:                            Custom matplotlib colormap object or name
    :param save_figure:                     If True, figure is saved to file and 'output_file' must be set
    :type save_figure:                      bool
    :param output_file:                     If 'save_figure' is True, specify full path with file name and extension
                                            for the file to be saved to
    """

    fig = plt.subplots(figsize=(20, 10))

    df = data

    df = df.groupby(region, as_index=False).mean()
    df = df.sort_values(y, ascending=False)

    x = df[x].tolist()
    y = df[y].tolist()

    plt.bar(x, y, align='center', alpha=0.5)
    plt.xlabel(f"{x_axis_title}")
    plt.ylabel(f"{y_axis_title}")
    plt.title(f"Barchart of {y_axis_title} by {x_axis_title}, Averaged across {region}")
    plt.show()


def plot_sankey(data, unit_type1, output_level, unit_type2=None, region_name=None, strip=None):
    """
    Must give it dataframe, a region, a unit type, and a level of output
    """
    df = data
    df_1 = df[df.units == unit_type1]

    # TODO need to make sure this is unique if there's no region name specified
    if region_name is None:
        df_1 = df_1
    else:
        df_1 = df_1[df_1.region == region_name]

    group_results(df_1, output_level=output_level)

    available_levels = [1, 2, 3, 4, 5]
    remove = f'-{strip}'

    if output_level in available_levels:

        if output_level == 1:

            sankey_number = pd.unique(df[['S1', 'T1']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df_1["source"] = df_1["S1"].apply(lambda x: var_dict.get(x))
            df_1["target"] = df_1["T1"].apply(lambda x: var_dict.get(x))

        elif output_level == 2:

            df_1['S12'] = df_1['S1'] + '-' + df_1['S2']
            df_1['T12'] = df_1['T1'] + '-' + df_1['T2']

            if strip is None:
                df_1['S12'] = df_1['S12']
                df_1['T12'] = df_1['T12']
            else:
                df_1['S12'] = df_1['S12'].str.replace(remove, "")
                df_1['T12'] = df_1['T12'].str.replace(remove, "")


            sankey_number = pd.unique(df_1[['S12', 'T12']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df_1["source"] = df_1["S12"].apply(lambda x: var_dict.get(x))
            df_1["target"] = df_1["T12"].apply(lambda x: var_dict.get(x))


        elif output_level == 3:

            df_1['S123'] = df_1['S1'] + '-' + df_1['S2']+ '-' + df_1['S3']
            df_1['T123'] = df_1['T1'] + '-' + df_1['T2']+ '-' + df_1['T3']

            if strip is None:
                df_1['S123'] = df_1['S123']
                df_1['T123'] = df_1['T123']
            else:
                df_1['S123'] = df_1['S123'].str.replace(remove, "")
                df_1['T123'] = df_1['T123'].str.replace(remove, "")

            sankey_number = pd.unique(df_1[['S123', 'T123']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df_1["source"] = df_1["S123"].apply(lambda x: var_dict.get(x))
            df_1["target"] = df_1["T123"].apply(lambda x: var_dict.get(x))

        elif output_level == 4:

            df_1['S1234'] = df_1['S1'] + '-' + df_1['S2']+ '-' + df_1['S3']+ '-' + df_1['S4']
            df_1['T1234'] = df_1['T1'] + '-' + df_1['T2']+ '-' + df_1['T3']+ '-' + df_1['T4']

            if strip is None:
                df_1['S1234'] = df_1['S1234']
                df_1['T1234'] = df_1['T1234']
            else:
                df_1['S1234'] = df_1['S1234'].str.replace(remove, "")
                df_1['T1234'] = df_1['T1234'].str.replace(remove, "")

            sankey_number = pd.unique(df_1[['S1234', 'T1234']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df_1["source"] = df_1["S1234"].apply(lambda x: var_dict.get(x))
            df_1["target"] = df_1["T1234"].apply(lambda x: var_dict.get(x))

        else:

            df_1['S12345'] = df_1['S1'] + '-' + df_1['S2']+ '-' + df_1['S3']+ '-' + df_1['S4']+ '-' + df_1['S5']
            df_1['T12345'] = df_1['T1'] + '-' + df_1['T2']+ '-' + df_1['T3']+ '-' + df_1['T4']+ '-' + df_1['T5']

            if strip is None:
                df_1['S12345'] = df_1['S12345']
                df_1['T12345'] = df_1['T12345']
            else:
                df_1['S12345'] = df_1['S12345'].str.replace(remove, "")
                df_1['T12345'] = df_1['T12345'].str.replace(remove, "")

            sankey_number = pd.unique(df_1[['S12345', 'T12345']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df_1["source"] = df_1["S12345"].apply(lambda x: var_dict.get(x))
            df_1["target"] = df_1["T12345"].apply(lambda x: var_dict.get(x))

        if strip is None:
            source_list = df_1['source'].tolist()
            target_list = df_1['target'].tolist()
            value_list = df_1['value'].to_list()
        else:
            source_list = df_1['source'].tolist()
            target_list = df_1['target'].tolist()
            value_list = df_1['value'].to_list()

        # create the figure
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=40,  # space between nodes (vertically)
                thickness=10,  # node thickness
                line=dict(color="black", width=1),  # node border color and thickness
                label=sankey_number,  # node label, refers to list of indexed names
                color = 'rgba(63, 125, 152, 1)'                                 #color of nodes, refers to list of hex codes
            ),
            link=dict(
                source=source_list,  # list of source node indices
                target=target_list,  # list of target node indices
                value=value_list,  # list of values between source and target at indices
                color='rgba(102, 195, 216, 0.7)'
            ))])

        # fig.update_layout(title_text="Interactive Sankey Diagram of Select Variables", font_size=12)  #title

        fig.update_traces(valuesuffix=f'{unit_type1}', selector=dict(type='sankey'))  # adds value suffix
        print('WSW = Water Supply Withdrawals')
        print('WSI = Water Supply Imports')


        fig.show()

        if unit_type2 is None:
            pass
        else:
            df_2 = df[df.units == unit_type2]

            # TODO need to make sure this is unique if there's no region name specified
            if region_name is None:
                df_2 = df_2
            else:
                df_2 = df_2[df_2.region == region_name]

            group_results(df_2, output_level=output_level)

            available_levels = [1, 2, 3, 4, 5]
            remove = f'-{strip}'

            if output_level in available_levels:

                if output_level == 1:

                    sankey_number = pd.unique(df[['S1', 'T1']].values.ravel('K'))

                    var_dict = dict()
                    for index, value in enumerate(sankey_number):
                        var_dict[index] = value
                    var_dict = {y: x for x, y in var_dict.items()}

                    df_2["source"] = df_2["S1"].apply(lambda x: var_dict.get(x))
                    df_2["target"] = df_2["T1"].apply(lambda x: var_dict.get(x))

                elif output_level == 2:

                    df_2['S12'] = df_2['S1'] + '-' + df_2['S2']
                    df_2['T12'] = df_2['T1'] + '-' + df_2['T2']

                    if strip is None:
                        df_2['S12'] = df_2['S12']
                        df_2['T12'] = df_2['T12']
                    else:
                        df_2['S12'] = df_2['S12'].str.replace(remove, "")
                        df_2['T12'] = df_2['T12'].str.replace(remove, "")

                    sankey_number = pd.unique(df_2[['S12', 'T12']].values.ravel('K'))

                    var_dict = dict()
                    for index, value in enumerate(sankey_number):
                        var_dict[index] = value
                    var_dict = {y: x for x, y in var_dict.items()}

                    df_2["source"] = df_2["S12"].apply(lambda x: var_dict.get(x))
                    df_2["target"] = df_2["T12"].apply(lambda x: var_dict.get(x))


                elif output_level == 3:

                    df_2['S123'] = df_2['S1'] + '-' + df_2['S2'] + '-' + df_2['S3']
                    df_2['T123'] = df_2['T1'] + '-' + df_2['T2'] + '-' + df_2['T3']

                    if strip is None:
                        df_2['S123'] = df_2['S123']
                        df_2['T123'] = df_2['T123']
                    else:
                        df_2['S123'] = df_2['S123'].str.replace(remove, "")
                        df_2['T123'] = df_2['T123'].str.replace(remove, "")

                    sankey_number = pd.unique(df_2[['S123', 'T123']].values.ravel('K'))

                    var_dict = dict()
                    for index, value in enumerate(sankey_number):
                        var_dict[index] = value
                    var_dict = {y: x for x, y in var_dict.items()}

                    df_2["source"] = df_2["S123"].apply(lambda x: var_dict.get(x))
                    df_2["target"] = df_2["T123"].apply(lambda x: var_dict.get(x))

                elif output_level == 4:

                    df_2['S1234'] = df_2['S1'] + '-' + df_2['S2'] + '-' + df_2['S3'] + '-' + df_2['S4']
                    df_2['T1234'] = df_2['T1'] + '-' + df_2['T2'] + '-' + df_2['T3'] + '-' + df_2['T4']

                    if strip is None:
                        df_2['S1234'] = df_2['S1234']
                        df_2['T1234'] = df_2['T1234']
                    else:
                        df_2['S1234'] = df_2['S1234'].str.replace(remove, "")
                        df_2['T1234'] = df_2['T1234'].str.replace(remove, "")

                    sankey_number = pd.unique(df_2[['S1234', 'T1234']].values.ravel('K'))

                    var_dict = dict()
                    for index, value in enumerate(sankey_number):
                        var_dict[index] = value
                    var_dict = {y: x for x, y in var_dict.items()}

                    df_2["source"] = df_2["S1234"].apply(lambda x: var_dict.get(x))
                    df_2["target"] = df_2["T1234"].apply(lambda x: var_dict.get(x))

                else:

                    df_2['S12345'] = df_2['S1'] + '-' + df_2['S2'] + '-' + df_2['S3'] + '-' + df_2['S4'] + '-' + df_2['S5']
                    df_2['T12345'] = df_2['T1'] + '-' + df_2['T2'] + '-' + df_2['T3'] + '-' + df_2['T4'] + '-' + df_2['T5']

                    if strip is None:
                        df_2['S12345'] = df_2['S12345']
                        df_2['T12345'] = df_2['T12345']
                    else:
                        df_2['S12345'] = df_2['S12345'].str.replace(remove, "")
                        df_2['T12345'] = df_2['T12345'].str.replace(remove, "")

                    sankey_number = pd.unique(df_2[['S12345', 'T12345']].values.ravel('K'))

                    var_dict = dict()
                    for index, value in enumerate(sankey_number):
                        var_dict[index] = value
                    var_dict = {y: x for x, y in var_dict.items()}

                    df_2["source"] = df_2["S12345"].apply(lambda x: var_dict.get(x))
                    df_2["target"] = df_2["T12345"].apply(lambda x: var_dict.get(x))

                if strip is None:
                    source_list = df_2['source'].tolist()
                    target_list = df_2['target'].tolist()
                    value_list = df_2['value'].to_list()
                else:

                    source_list = df_2['source'].tolist()

                    target_list = df_2['target'].tolist()
                    value_list = df_2['value'].to_list()

                # create the figure
                fig = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=20,  # space between nodes (vertically)
                        thickness=10,  # node thickness
                        line=dict(color="black", width=1),  # node border color and thickness
                        label=sankey_number,  # node label, refers to list of indexed names
                        color = 'rgba(209, 155, 30, 1)'
                        #color of nodes, refers to list of hex codes
                    ),
                    link=dict(
                        source=source_list,  # list of source node indices
                        target=target_list,  # list of target node indices
                        value=value_list,  # list of values between source and target at indices
                        color='rgba(252, 230, 112, 1)'
                    ))])

                # fig.update_layout(title_text="Interactive Sankey Diagram of Select Variables", font_size=12)  #title

                fig.update_traces(valuesuffix=f'{unit_type2}', selector=dict(type='sankey'))  # adds value suffix

                fig.show()


    else:
        m = 'Incorrect level specified. Level must be an integer between 1 and 5, inclusive.'