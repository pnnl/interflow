import plotly.graph_objects as go
import plotly.express as px
from .analyze import *


def plot_sankey(data, unit_type1, output_level, unit_type2=None, region_name=None, strip=None):
    """Plots interactive sankey diagram(s) for a given region at a given level of granularity. At least one unit type is
    required. If no region name is specified, the flow data provided must be for a single region. Contains the option
    to strip strings from node names to remove replicated placeholder names such as 'total'.

            :param data:                        dataframe of flow values from source to target
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

            :return:                            interactive sankey diagram of flow values

            """
    # get data
    df = data

    # reduce data to appropriate units
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

        fig.update_layout(title_text=f"{unit_type1} flows for {region_name}", font_size=12)  #title
        fig.update_traces(valuesuffix=f'{unit_type1}', selector=dict(type='sankey'))  # adds value suffix
        print('WSW = Water Supply Withdrawals')
        print('WSI = Water Supply Imports')


        fig.show()

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

                fig.update_layout(title_text=f"{unit_type2} flows for {region_name}", font_size=12)  # title
                fig.update_traces(valuesuffix=f'{unit_type2}', selector=dict(type='sankey'))  # adds value suffix

                fig.show()


    else:
        m = 'Incorrect level specified. Level must be an integer between 1 and 5, inclusive.'


def plot_sector_bar(data, unit_type, region_name, sector_list, inflow=True, strip=None ):

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
        # title_text = 'Expedited Process Availability by State', # Create a Title
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

