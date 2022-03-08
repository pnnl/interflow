---
layout: default
title: Modules
parent: User Guide
nav_order: 5
---

# flow package
## Submodules
### flow.calculate()
Loops through input data for each region provided or specified and (1) collects flows for input data, (2) calculates totals for input flows at level 1 through level 5 granularity (2) calculates any cross unit flows based on input flow intensity values at level 1 through level 5 granularity (3) builds source flows for calculated intensities based on source fraction assumptions at level 1 through level 5 granularity, and (4) builds discharge flows for calculated intensities and input data based on discharge fractions at level 1 through level 5 granularity. This function also removes all self-provided (i.e., looped) flows if remove_loops parameter is set to True.

Params:
data – Pandas DataFrame of input flow values, intensities, and fractions
level – Desired level of granularity of output data. Must be an integer between 1 and 5, inclusive.
region_name – Name of region to conduct analysis of. If none is specified, calculations are run for all regions included in the input data.
remove_loops – Boolean indicating whether looped values (i.e., nodes whose output is its own input value) should be removed from output dataset. Default is True.
output_file_path – Optional parameter to give a file path, inclusive of file name, to save dataframe output as a csv. Default is set to None (no output saved)
Returns:
DataFrame of flow run output at specified level of granularity for specified region(s)

### flow.construct_nested_dictionary()
Takes in a 16-column DataFrame of values and returns a nested dictionary of sector flow values and assumptions
Params:
df – dataframe of values to convert to nested dictionary
Returns:
Nested dictionary of dataframe values

### flow.deconstruct_nested_dictionary()
Takes in a nested dictionary of run values and returns a dataframe with flow information as columns.
Params:
input_dict – nested dictionary of values to unpack into a dataframe
Returns:
Pandas Dataframe

### flow.reader()
Read in input csv data as a Pandas DataFrame.
Params:
path – path to a csv file with flow values
leading_zeros – Optional parameter to add leading zeros to the region column to ensure the regional identifier has the correct number of data positions.
Returns:
Pandas Dataframe of input flow values and parameters

### flow.plot_sankey()
Plots interactive sankey diagram(s) for a given region at a given level of granularity from flow package output data. Requires that variable naming is consistent with flow package output variable naming. At least one unit type must be specified as a parameter. Output level can be specified to display sankey diagrams at different levels of granularity. Sankey diagram(s) can only display a single region at a time. If no region name is specified, the flow data provided must be for a single region. Contains the option to strip strings from node names to remove replicated placeholder names such as 'total'.

Params:
data – dataframe of flow values from source to target
unit_type1 – units of the first set of flow values (e.g., mgd)
output_level – level of granularity of values returned in the figure.
unit_type2 – units of the second set of flow values (e.g., bbtu)
region_name – Name of region to display values for if input data includes multiple. If none is specified, data must be for a single region.
strip – Optional parameter. Provides a string to remove from variable labels.
remove_sectors – Optional parameter to remove all flows into and out of a level 1 sector. Removes values at all levels for specified sector.
Returns:
interactive sankey diagram of flow values

### flow.plot_sector_bar()
Plots a stacked barchart for a single region of inflows or outflows for selected sectors in selected units.
Params:
data – dataframe of flow values from source to target
unit_type – unit type to be displayed, must be equal to unit type in input data
region_name – name of region to display values for
sector_list – list of sectors to include stacked values for. Must be provided at level 1 granularity.
inflow – If true, shows inflows into each specified sector. If false, shows outflows. Default is set to True
strip – optional parameter to provide a string that will be removed from the labels in the output. For example, if the input data has a repeated word such as 'total' for numerous levels, the word 'total' will be stripped

### flow.plot_map()
Takes flow package output and plots a cloropleth map of an individual value. Displaying the first flow value in the dataset by default and produces a drop-down menu of the remaining flows to select from and update the map. Requires a GeoJSON file containing the geometry information for the region of interest. The feature.id in the file must align with the region data column in the dataframe of input values to display. Flow values can be displayed on the map and represented in the dropdown menu for the indicated level of granularity (level 1 through level 5, inclusive). Additionally, an optional parameter is provided to display additional regional identification information in the hover-template when a region is hovered over. This is provided in the region_col parameter and points to the column in the input data with this information.

Params:
jsonfile – Path to GeoJSON file containing geometry information for the values to be plotted on the map. the feature.id in the file must align with the region data column in the dataframe of input values to display.
data – dataframe of flow values from source to target by region
level – level of granularity to display for values. Level should be between 1 and 5 inclusive.
region_col – optional parameter to indicate an additional regional identifier column that can be displayed on hover in the figure. Examples include the associated US county name belonging to the region code. Default is set to no additional region information displayed.
strip – optional parameter to provide a string that will be removed from the labels in the output. For example, if the input data has a repeated word such as 'total' for numerous levels, the word 'total' will be stripped.
center – dictionary of coordinates in the form of {"lat": 37.0902, "lon": -95.7129} which centers the displayed map. Default center coordinates are for the US.
Returns:
cloropleth map shaded by value for all regions provided at level specified and for specified units.
