---
layout: default
title: Geospatial Information
parent: US Sample Data Methodology
nav_order: 2
---

# Geospatial information

## US Counties

In order to get values at the county-level across multiple datasets in a consistent manner, a set of counties was established as the base county list for 2015. This list contains all US counties (not including US Territories) included in the USGS 2015 water use dataset (Dieter et al. [1]). Given that some datasets used in compiling the full sample dataset are from multiple years, some of the county-level FIPS codes required modification in order to match those provided in the 2015 base list. These modifications include mapping older FIPS codes to the 2015 ones or adding new FIPS codes when new counties were created. These modifications were mostly required for values used in from the 1995 USGS dataset (Solley et al. [7]).

# GeoJSON

In order to plot county-level outputs from the US 2015 dataset, a GeoJSON file containing geometry information for the US counties is required. The file used and included in the sample data is from Plotly's sample datafiles. The raw JSON datafile can be found in Plotly [19]. A small number of counties included in the GeoJSON file required adjustment to match the baseline county list for the sample data. The FIPS codes for these counties were adjusted accordingly in the GeoJSON file. Note that the modified version of this file is included in the input data, not the raw GeoJSON file.

For more information on the base map configuration for Plotly's cloropleth maps, see the Plotly documentation (https://plotly.com/python/choropleth-maps/)
