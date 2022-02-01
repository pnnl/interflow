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


def plot_sankey(data, region_name, unit_type, output_level, strip=None):
    """
    Must give it dataframe, a region, a unit type, and a level of output
    """
    df = data
    df = df[df.units == unit_type]
    df = df[df.region == region_name]

    group_results(df, output_level=output_level)

    available_levels = [1, 2, 3, 4, 5]
    remove = f'-{strip}'

    if output_level in available_levels:

        if output_level == 1:

            sankey_number = pd.unique(df[['S1', 'T1']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df["source"] = df["S1"].apply(lambda x: var_dict.get(x))
            df["target"] = df["T1"].apply(lambda x: var_dict.get(x))

        elif output_level == 2:

            df['S12'] = df['S1'] + '-' + df['S2']
            df['T12'] = df['T1'] + '-' + df['T2']

            if strip is None:
                df['S12'] = df['S12']
                df['T12'] = df['T12']
            else:
                df['S12'] = df['S12'].str.strip(remove)
                df['T12'] = df['T12'].str.strip(remove)


            sankey_number = pd.unique(df[['S12', 'T12']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df["source"] = df["S12"].apply(lambda x: var_dict.get(x))
            df["target"] = df["T12"].apply(lambda x: var_dict.get(x))


        elif output_level == 3:

            df['S123'] = df['S1'] + '-' + df['S2']+ '-' + df['S3']
            df['T123'] = df['T1'] + '-' + df['T2']+ '-' + df['T3']

            if strip is None:
                df['S123'] = df['S123']
                df['T123'] = df['T123']
            else:
                df['S123'] = df['S123'].str.strip(remove)
                df['T123'] = df['T123'].str.strip(remove)

            sankey_number = pd.unique(df[['S123', 'T123']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df["source"] = df["S123"].apply(lambda x: var_dict.get(x))
            df["target"] = df["T123"].apply(lambda x: var_dict.get(x))

        elif output_level == 4:

            df['S1234'] = df['S1'] + '-' + df['S2']+ '-' + df['S3']+ '-' + df['S4']
            df['T1234'] = df['T1'] + '-' + df['T2']+ '-' + df['T3']+ '-' + df['T4']

            if strip is None:
                df['S1234'] = df['S1234']
                df['T1234'] = df['T1234']
            else:
                df['S1234'] = df['S1234'].str.strip(remove)
                df['T1234'] = df['T1234'].str.strip(remove)

            sankey_number = pd.unique(df[['S1234', 'T1234']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df["source"] = df["S1234"].apply(lambda x: var_dict.get(x))
            df["target"] = df["T1234"].apply(lambda x: var_dict.get(x))

        else:

            df['S12345'] = df['S1'] + '-' + df['S2']+ '-' + df['S3']+ '-' + df['S4']+ '-' + df['S5']
            df['T12345'] = df['T1'] + '-' + df['T2']+ '-' + df['T3']+ '-' + df['T4']+ '-' + df['T5']

            if strip is None:
                df['S12345'] = df['S12345']
                df['T12345'] = df['T12345']
            else:
                df['S12345'] = df['S12345'].str.strip(remove)
                df['T12345'] = df['T12345'].str.strip(remove)

            sankey_number = pd.unique(df[['S12345', 'T12345']].values.ravel('K'))

            var_dict = dict()
            for index, value in enumerate(sankey_number):
                var_dict[index] = value
            var_dict = {y: x for x, y in var_dict.items()}

            df["source"] = df["S12345"].apply(lambda x: var_dict.get(x))
            df["target"] = df["T12345"].apply(lambda x: var_dict.get(x))

        if strip is None:
            source_list = df['source'].tolist()
            target_list = df['target'].tolist()
            value_list = df['value'].to_list()
        else:

            source_list = df['source'].tolist()

            target_list = df['target'].tolist()
            value_list = df['value'].to_list()

        # create the figure
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=35,  # space between nodes (vertically)
                thickness=40,  # node thickness
                line=dict(color="black", width=1),  # node border color and thickness
                label=sankey_number  # node label, refers to list of indexed names
                # color = color_list                                 #color of nodes, refers to list of hex codes
            ),
            link=dict(
                source=source_list,  # list of source node indices
                target=target_list,  # list of target node indices
                value=value_list,  # list of values between source and target at indices
            ))])

        # fig.update_layout(title_text="Interactive Sankey Diagram of Select Variables", font_size=12)  #title

        fig.update_traces(valuesuffix=f'{unit_type}', selector=dict(type='sankey'))  # adds value suffix

        fig.show()
    else:
        m = 'Incorrect level specified. Level must be an integer between 1 and 5, inclusive.'