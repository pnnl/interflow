*****************
Getting started
*****************

About
########

The interflow model (interflow) gives us the capability to organize and evaluate the interdependencies and linkages between sectors at various levels of granularity and across regions. We can use **interflow** to gain an understanding of topics such as:
1. which sectors have a high reliance on upstream sectors?
2. which sectors represent pivotal nodes for passing on resource flows to downstream flows?
3. How do resource intensities in sectors compare across regions?
4. What does the network map of resource flows in a region look like visually?
5. Where are the opportunities for network enhancement, optimization, and resiliency improvement?

Though **interflow** provides sample data to run water and energy resource data for each county of the US for 2015, it can be extended to function for any set of regions (e.g., province, country, zip code, neighborhood) so long as the correct prerequisite data has been provided. Additionally, while **interflow** was constructed to build water and energy interdependencies, units and sectors are customizable by the user, meaning that interflow can be used to evaluate interdependencies between any sectors (e.g., water-food, energy-land) so long as the correct prerequisite data is provided. The prerequisite data must be in the form of two-dimensional tabular data including (1) An initial column containing rows of region identifiers (e.g., county FIPS code), (2) additional columns documenting initial interflow values (e.g., water withdrawals to the public water supply), intensity factor assumptions (e.g., unit of energy required per unit of water withdrawn in the public water supply), and source/discharge fraction assumptions (e.g., 35% of electricity used in the public water supply sector is discharged to rejected energy). This prerequisite data is used by the model to iteratively build the specified connections between sectors for each region specified. In addition to building connections between sectors (e.g., electricity demand to public water supply sector), input data can be specified up to five levels of sub-sector granularity. For example, flows between total electricity demand and public water supply can be split into individual applications within the public water supply sector such as fresh surface water pumping, fresh groundwater treatment, and others.

In addition to calculating and organizing flows across sectors, **interflow** also provides visualization and analysis functions to digest the aggregated data output. These include: Sankey diagrams of each unit (water and energy) showing flows between sectors in a given region, bar charts of specified sectors showing the breakdown of subsector components (e.g., electricity use by application in public water supply), and an interactive map to compare output values across included regions. Note that the geospatial maps require additional prerequisite data.


Python version support
###################################
Python 3.7, 3.8, and 3.9


Installation
###################################

**interflow** can be installed via pip by running the following from a terminal window::

pip install interflow

interflow is not currently configured to support installation via Conda/Miniconda.

Dependencies
###################################

+------------+------------------+
| Dependency | Minimum Version  |
+============+==================+
|numpy       | 1.19.4           |
+------------+------------------+
|pandas      | 1.3.4            |
+------------+------------------+
|plotly      | 5.5.0            |
+------------+------------------+
|json5       | 0.9.6            |
+------------+------------------+


