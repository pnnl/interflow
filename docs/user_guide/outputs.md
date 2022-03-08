---
layout: default
title: Model Outputs
parent: User Guide
nav_order: 4
---

# Key Outputs

## Data Output

**flow** returns a Pandas DataFrame when calling calculate(). The DataFrame
contains the following for each flow value for each region included in the input data when the level parameter is set to 5:

| Column Name | Description                               | Type  |
|:------------|:------------------------------------------|:------|
| region      | Name of region                            | str   |
| S1          | Level 1 source node name                  | str   |
| S2          | Level 2 source node name                  | str   |
| S3          | Level 3 source node name                  | str   |
| S4          | Level 4 source node name                  | str   |
| S5          | Level 5 source node name                  | str   |
| T1          | Level 1 target node name                  | str   |
| T2          | Level 2 target node name                  | str   |
| T3          | Level 3 target node name                  | str   |
| T4          | Level 4 target node name                  | str   |
| T5          | Level 5 target node name                  | str   |
| units       | unit type for value                       | str   |
| value       | value of flow connecting source to target | flt   |

Note that setting the level parameter equal to a value less than 5 will reduce the output accordingly to only show the appropriate levels, aggregated to the level specified. For example, specifying level 1 will return the following DataFrame instead.

| Column Name | Description                               | Type  |
|:------------|:------------------------------------------|:------|
| region      | Name of region                            | str   |
| S1          | Level 1 source node name                  | str   |
| T1          | Level 1 target node name                  | str   |
| units       | unit type for value                       | str   |
| value       | value of flow connecting source to target | flt   |

## Visualizations

In addition to the Pandas DataFrame output, a variety of visualization and analysis functions are pre-built into the flow package and can be used to interpret results. All visualizations in the package utilize the Plotly open source graphing library. These include the following:

### Single-unit sankey diagrams

Sankey diagrams are used to visualize flows from source nodes to target nodes where links between nodes have variable width depending on the value of the flow. The 'flow.plot_sankey()' function plots up to two sankey diagrams (one for each unit specified) based on the run output that is provided to the function. Users can specify a level of granularity to show flows from level 1 (major sector aggregates only) to level 5 (the highest level of granularity available). For more information on the specific function parameters, defaults, and other components, see the function_guide section.

![sankey_example](https://user-images.githubusercontent.com/74064300/157076964-e8a902e2-30c4-45a1-b860-f0660c68795e.png)


### Single region stacked barcharts of sectors

In addition to the Sankey diagrams, there is also the option to plot output in a stacked barchart for any number of sectors. The flow.plot_sector_bar() function takes a list input of the level 1 sector names (e.g., public water supply) and proceeds to plot inflows or outflows (chosen by the user) into that sector for the specified units. Inflows and outflows are displayed in stacked values of level 5 subsectors within each sector. The barcharts are intended to be used to compare sectors within an individual region for an individual unit.

An example output for energy flows into the agricultural and public water supply sectors for an individual US county from the sample data is shown below.
![image](https://user-images.githubusercontent.com/74064300/157077416-13e7191e-bd2c-4744-8407-32cc8f91889b.png)

Likewise, the additional figure below shows the energy outflows from those sectors for the same county.

![image](https://user-images.githubusercontent.com/74064300/157079185-d433d9f6-c6c1-4fd2-8bf9-98e95b995e44.png)


### Cloropleth map displaying single flow values across regions

The **flow** package also comes with the ability to plot flow values on a regional basis. By providing  flow.plot_map() function requires a GeoJSON file to plot a cloropleth map of a selected value. The selectable values are generated as a dropdown list of all available flow values for the specified level of granularity. For example, if level 1 granularity is specified, the drop-down list contains only flows between level 1 nodes. Users can select up to level 5 granularity when running the function and the output will respond appropriately. Below is an example of the cloropleth map output for level 1 granularity for a single flow value using the US county sample data.

![image](https://user-images.githubusercontent.com/74064300/157077774-28f4ea72-6c4e-49fc-869d-bf878d91b092.png)
