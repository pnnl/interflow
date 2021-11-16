import matplotlib.pyplot as plt

from .calculate import *

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
