import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from interflow.analyze import *


def plot_sankey(data, unit_type1, output_level=1, unit_type2=None, region_name=None, strip=None, remove_sectors=None):
    """Plots interactive sankey diagram(s) for a given region at a given level of granularity from package output
    data. Requires that variable naming is consistent with flow package output variable naming. At least one unit type
    must be specified as a parameter. Output level can be specified to display sankey diagrams at different levels of
    granularity. Sankey diagram(s) can only display a single region at a time. If no region name is
    specified, the flow data provided must be for a single region. Contains the option to strip strings from node names
    to remove replicated placeholder names such as 'total'. On hover, the flow values are displayed. Note that an 'm'
    following a value indicates that the value shown is a decimal. For example, 80m is equivalent to .80.


    :param data:                        dataframe of flow values from source to target, must be provided at level
                                        5 granularity.
    :type data:                         DataFrame

    :param unit_type1:                  units of the first set of flow values (e.g., mgd)
    :type unit_type1:                   string

    :param output_level:                level of granularity of values returned in the figure.
    :type output_level:                 int

    :param unit_type2:                  units of the second set of flow values (e.g., bbtu)
    :type unit_type2:                   string

    :param region_name:                 Name of region to display values for if input data includes multiple.
                                        If none is specified, data must be for a single region.
    :type region_name:                  string

    :param strip:                       Optional parameter. Provides a string to remove from variable labels.
    :type strip:                        string

    :param remove_sectors:              Optional parameter to remove all flows into and out of a level 1 sector.
                                        Removes values at all levels for specified sector.
    :type remove_sectors:               list

    :return:                            interactive Sankey diagram of flow values

        """

    # get data
    df = data

    # check that the correct number of columns is provided
    if len(df.columns) != 13:
        m = 'Data provided is not at the correct granularity level. Must be at granularity level 5.'
        raise ValueError(m)
    else:
        pass

    # remove sectors specified
    if remove_sectors is None:
        pass
    else:
        subset = remove_sectors
        df = df[~df['S1'].isin(subset)]
        df = df[~df['T1'].isin(subset)]

    # create a dataframe that only includes unit_type1
    df_1 = df[df.units == unit_type1]

    # if no region name is provided
    if region_name is None:
        # check if region column has a single unique value
        if len(df['region'].unique().tolist()) == 1:
            df_1 = df_1
        else:
            m = 'More than one region included in dataset, reduce dataset to single region ' \
                'or specify desired region.'
            raise ValueError(m)

    # reduce to specified region
    else:
        df_1 = df_1[df_1.region == region_name]

    # group results
    df_1 = group_results(df_1, output_level=output_level)

    available_levels = [1, 2, 3, 4, 5]
    remove = f'-{strip}'

    # if the granularity level specified is appropriate
    if output_level in available_levels:

        # if the specified level of granularity is equal to 1
        if output_level == 1:
            sankey_number = pd.unique(df_1[['S1', 'T1']].values.ravel('K'))  # get unique nodes in a flattened array
            var_dict = dict()  # create an empty dictionary
            for index, value in enumerate(sankey_number):
                var_dict[index] = value  # add index value and node name to the empty dictionary
            var_dict = {y: x for x, y in var_dict.items()}  # set node name to be the key in the dictionary

            df_1["source"] = df_1["S1"].apply(lambda x: var_dict.get(x))  # assign the numerical node value to source
            df_1["target"] = df_1["T1"].apply(lambda x: var_dict.get(x))  # assign the numerical node value to target

        # if the specified level of granularity is equal to 2, repeat with level 2 names and values
        elif output_level == 2:
            df_1['S12'] = df_1['S1'] + '-' + df_1['S2']
            df_1['T12'] = df_1['T1'] + '-' + df_1['T2']

            # if no string is specified to be removed from labels
            if strip is None:
                df_1['S12'] = df_1['S12']
                df_1['T12'] = df_1['T12']

            # if a string is specified to be removed from labels
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

        # if the specified level of granularity is equal to 3
        elif output_level == 3:

            df_1['S123'] = df_1['S1'] + '-' + df_1['S2'] + '-' + df_1['S3']
            df_1['T123'] = df_1['T1'] + '-' + df_1['T2'] + '-' + df_1['T3']

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

        # if the specified level of granularity is equal to 4
        elif output_level == 4:
            df_1['S1234'] = df_1['S1'] + '-' + df_1['S2'] + '-' + df_1['S3'] + '-' + df_1['S4']
            df_1['T1234'] = df_1['T1'] + '-' + df_1['T2'] + '-' + df_1['T3'] + '-' + df_1['T4']

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

        # if the specified level of granularity is equal to 5
        else:

            df_1['S12345'] = df_1['S1'] + '-' + df_1['S2'] + '-' + df_1['S3'] + '-' + df_1['S4'] + '-' + df_1['S5']
            df_1['T12345'] = df_1['T1'] + '-' + df_1['T2'] + '-' + df_1['T3'] + '-' + df_1['T4'] + '-' + df_1['T5']

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
                color='rgba(63, 125, 152, 1)'
            ),
            link=dict(
                source=source_list,  # list of source node indices
                target=target_list,  # list of target node indices
                value=value_list,  # list of values between source and target at indices
                color='rgba(102, 195, 216, 0.7)'
            ))])

        fig.update_layout(title_text=f"{unit_type1} Flows for Region {region_name}", font_size=12)  # title
        fig.update_traces(valuesuffix=f'{unit_type1}', selector=dict(type='sankey'))  # adds value suffix

        # show figure
        fig.show()

        # if a second unit is specified, repeat process with secondary unit
        if unit_type2 is None:
            pass
        else:
            df_2 = df[df.units == unit_type2]

            # if no region name is provided
            if region_name is None:
                # check if region column has a single unique value
                if len(df['region'].unique().tolist()) == 1:
                    df_2 = df_2
                else:
                    m = 'More than one region included in dataset, reduce dataset to single region ' \
                        'or specify desired region.'
                    raise ValueError(m)
            # reduce to specified region
            else:
                df_2 = df_2[df_2.region == region_name]

            df_2 = group_results(df_2, output_level=output_level)

            available_levels = [1, 2, 3, 4, 5]
            remove = f'-{strip}'

            if output_level in available_levels:

                if output_level == 1:
                    sankey_number = pd.unique(df_2[['S1', 'T1']].values.ravel('K'))
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

                    df_2['S12345'] = df_2['S1'] + '-' + df_2['S2'] + '-' + df_2['S3'] + '-' + df_2['S4'] + '-' + df_2[
                        'S5']
                    df_2['T12345'] = df_2['T1'] + '-' + df_2['T2'] + '-' + df_2['T3'] + '-' + df_2['T4'] + '-' + df_2[
                        'T5']

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
                        pad=20,  # space between nodes
                        thickness=10,  # node thickness
                        line=dict(color="black", width=1),  # node border color and thickness
                        label=sankey_number,  # node label, refers to list of indexed names
                        color='rgba(209, 155, 30, 1)'
                    ),
                    link=dict(
                        source=source_list,  # list of source node indices
                        target=target_list,  # list of target node indices
                        value=value_list,  # list of values between source and target at indices
                        color='rgba(252, 230, 112, 1)'
                    ))])

                fig.update_layout(title_text=f"{unit_type2} Flows for Region {region_name}", font_size=12)  # title
                fig.update_traces(valuesuffix=f'{unit_type2}', selector=dict(type='sankey'))  # adds value suffix

                fig.show()

    else:
        m = 'Incorrect level specified. Level must be an integer between 1 and 5, inclusive.'


def plot_sector_bar(data, unit_type, region_name, sector_list, inflow=True, strip=None):
    """
    Plots a stacked barchart for a single region of inflows or outflows for selected sectors in selected units. The
    stacked bars represent the highest level of granularity available for each major sector. For example, if there are
    values for water flows into the public water supply sector, specifically tied to the water flows for fresh surface
    water imports, then one of the stacked components in the public water supply bar in the chart will be equal to the
    value of this specific sub-sector flow.

    :param data:                            dataframe of flow values from source to target
    :type data:                             DataFrame

    :param unit_type:                       unit type to be displayed, must be equal to resource unit type in input data
    :type  unit_type:                       str

    :param region_name:                     name of region to display values for.
    :type  region_name:                     str

    :param sector_list:                     list of major sectors to include stacked values for as strings. Strings
                                            must be provided at level 1 granularity. For example, providing
                                            sector_list=['Public Water Supply', 'Residential'] will show all of the
                                            subsector inflows or outflows for those sectors.
    :type  sector_list:                     list

    :param inflow:                          If true, shows inflows into each specified sector. If false, shows outflows.
                                            Default is set to True. Note that inflows are reflected in terms of the
                                            destination subsector not the source of the inflow. For example, indicating
                                            public water supply as a sector and setting inflows to True will show the
                                            values attributed to each of the public water supply subsectors, e.g.,
                                            energy demand for fresh surface water pumping in the public water supply
                                            sector. Outflows, on the other hand, reflect the destination of the outflow.
                                            For example, if inflow is set to False, we would see which downstream sector
                                            the indicated major sector was sending its resources.
    :type  inflow:                          bool

    :param strip:                           optional parameter to provide a string that will be removed from the labels
                                            in the output. For example, if the input data has a repeated word such as
                                            'total' for numerous levels, the word 'total' will be stripped.
    :type  strip:                           str

    :return:                                stacked barchart for a single region of inflows or outflows for selected
                                            sectors in selected units.
    """

    # get data
    df = data

    # reduce data to appropriate units
    df_1 = df[df.units == unit_type]

    # specify region
    df_1 = df_1[df_1.region == region_name]

    # create variable to remove stripped words
    remove = f'-{strip}'

    # reduce to inflows or outflows
    if inflow:

        # reduce to specified sector inflow list
        df_1 = df_1[df_1['T1'].isin(sector_list)]
        df_1['groupname'] = df_1['T2'] + '-' + df_1['T3'] + '-' + df_1['T4'] + '-' + df_1['T5']

    else:
        # reduce to specified sector outflow list
        df_1 = df_1[df_1['S1'].isin(sector_list)]
        df_1['groupname'] = df_1['T1'] + '-' + df_1['T2'] + '-' + df_1['T3'] + '-' + df_1['T4'] + '-' + df_1['T5']

    # remove stripped words
    df_1['groupname'] = df_1['groupname'].str.replace(remove, "")

    if inflow:
        df_group = df_1.groupby(['T1', 'groupname'], as_index=False).sum()
        x_variable = 'T1'
        flow_name = 'Inflows to'
    else:
        df_group = df_1.groupby(['S1', 'groupname'], as_index=False).sum()
        x_variable = 'S1'
        flow_name = 'Outflows from'

    fig = px.bar(df_group, x=x_variable, y="value", color="groupname",
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 template="simple_white")
    fig.update_layout(
        legend_title_text='Subsector',
        legend_title_font_size=15,
        legend_font_size=15,
        legend=dict(orientation="v",
                    bordercolor='#000000',
                    borderwidth=0,
                    traceorder='normal'
                    ),
        xaxis_title="",
        yaxis_title=f"{unit_type}",
        font=dict(
            family="Arial",
            size=15,
            color="black"
        ),
        title={
            'text': f"{flow_name} Subsector/Application Values for {region_name} region ({unit_type})",
            'xanchor': 'left',
            'yanchor': 'top'},
    )

    fig.show()


def plot_map(jsonfile: dict, data: pd.DataFrame, level=1, strip=None, center=None):
    """ Takes flow package output and plots a choropleth map of an individual value. Displaying the first flow value
     in the dataset by default and produces a drop-down menu of the remaining flows to select from and update the map.
     Requires a GeoJSON file containing the geometry information for the region of interest. The feature.id in the file
     must align with the region data column in the dataframe of input values to display. Flow values can be displayed
     on the map and represented in the dropdown menu for the indicated level of granularity (level 1 through level 5,
     inclusive). Additionally, an optional parameter is provided to display additional regional identification
     information in the hover-template when a region is hovered over. This is provided in the region_col parameter and
     points to the column in the input data with this information.

    :param jsonfile:                        loaded GeoJSON dictionary containing geometry information for the values to
                                            be plotted on the map. The feature.id in the file must align with the region
                                            data column in the dataframe of input values to display.
    :type jsonfile:                         dict

    :param data:                            dataframe of flow values from source to target by region
    :type data:                             Dataframe

    :param level:                           level of granularity to display for values. Level should be an integer
                                            between 1 and 5 inclusive. Default is set to level 1 granularity.
    :type level:                            int

    :param strip:                           optional parameter to provide a string that will be removed from the labels
                                            in the output. For example, if the input data has a repeated word such as
                                            'total' for numerous levels, the word 'total' will be stripped. Default is
                                            set so that no words are stripped.
    :type  strip:                           str

    :param center:                          dictionary of coordinates in the form of {"lat": 37.0902, "lon": -95.7129}
                                            which centers the displayed map. Default center coordinates are
                                            {"lat": 37.0902, "lon": -95.7129}.
    :type center:                           dict

    :return:                                choropleth map shaded by value for all regions provided at level specified
                                            and for specified units.
    """

    # check that the level of granularity specified is an appropriate value
    acceptable_values = [1, 2, 3, 4, 5]
    if level in acceptable_values:
        pass
    else:
        m = 'incorrect level of granularity specified. Must be an integer between 1 and 5, inclusive.'
        raise ValueError(m)

    # collect flow data
    df = data

    # collect geojson dictionary
    geo_id = jsonfile

    # set center coordinates for map
    if center is None:
        center = {"lat": 37.0902, "lon": -95.7129}
    else:
        center = center

    # build dropdown menu label depending on level of granularity specified
    if level == 1:
        # create a flow name
        df['SOURCE'] = df['S1']
        df['TARGET'] = df['T1']

    elif level == 2:
        df['SOURCE'] = df['S1'] + '-' + df['S2']
        df['TARGET'] = df['T1'] + '-' + df['T2']

    elif level == 3:
        df['SOURCE'] = df['S1'] + '-' + df['S2'] + '-' + df['S3']
        df['TARGET'] = df['T1'] + '-' + df['T2'] + '-' + df['T3']

    elif level == 4:
        df['SOURCE'] = df['S1'] + '-' + df['S2'] + '-' + df['S3'] + '-' + df['S4']
        df['TARGET'] = df['T1'] + '-' + df['T2'] + '-' + df['T3'] + '-' + df['T4']

    elif level == 5:
        df['SOURCE'] = df['S1'] + '-' + df['S2'] + '-' + df['S3'] + '-' + df['S4'] + '-' + df['S5']
        df['TARGET'] = df['T1'] + '-' + df['T2'] + '-' + df['T3'] + '-' + df['T4'] + '-' + df['T5']
    else:
        m = 'incorrect level specified. Must be an integer between 1 and 5 inclusive'

    # strip extra word from from names if provided
    if strip is None:
        pass
    else:
        remove = "-" + strip
        df['SOURCE'] = df['SOURCE'].str.replace(remove, "")
        df['TARGET'] = df['TARGET'].str.replace(remove, "")

    # build a single link name
    df['Link'] = df['SOURCE'] + ' to ' + df['TARGET'] + ', ' + df['units']

    # pivot values for each link to obtain them as columns
    df = pd.pivot_table(df, values='value', index=['region'],
                        columns=['Link'], aggfunc=np.sum)
    df = df.reset_index()  # reset index to remove multi-index from pivot table
    df = df.rename_axis(None, axis=1)  # drop index name
    df.fillna(0, inplace=True)

    # create a list of variable columns
    cols = df.columns[1:].to_list()

    # create dropdown buttons
    my_buttons = [dict(method='update',
                       label=c,
                       args=[{
                           "z": [df[c]],
                           "hovertemplate": 'Value: %{z}<extra>Region: %{customdata}</extra>'
                       }]) for c in cols]

    # create figure
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geo_id,
        locations=df['region'],
        z=df[df.columns[1]],
        customdata=df[df.columns[0]],
        hovertemplate='Value: %{z}<extra>Region: %{customdata}</extra>',
        coloraxis="coloraxis",
        marker_opacity=0.75,
        marker_line_width=0.5))

    # update map layout
    fig.update_layout(coloraxis_colorscale='Purples',
                      mapbox=dict(style='carto-positron',
                                  zoom=3,
                                  center=center))
    # update title
    fig.update_layout(title_text="Map of Selected Flow Value",
                      title_x=0.0,
                      margin={"r": 10, "t": 60, "l": 0, "b": 0})

    # update dropdown list
    fig.update_layout(updatemenus=[dict(active=0,
                                        buttons=my_buttons,
                                        x=.5,
                                        xanchor="left",
                                        y=1.12,
                                        yanchor="top")])
    fig.show()


