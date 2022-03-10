*****************
User Guide
*****************

Fundamental Concepts
################################

Basic Methodology
**********************************

At its most basic level **interflow** collects input values connecting two sectors in specified units (e.g., water delivered to the agriculture sector),
calculates additional sector flows in alternative units based on intensity factors (e.g., energy demand based on water delivered to the agriculture sector),
and builds connections to and from additional sectors to carry those values (e.g., electricity sector connected to agriculture sector to deliver the energy)

**interflow** goes through the following steps in completing calculations:

1. Collects a Unit 1 "flow" value connecting Node A to Node B
2. Calculates a Unit 2 value associated with Node B based on a provided Unit 2 per Unit 1 intensity factor for Node B.
3. Builds a Unit 2 flow value from Node C to Node B as a "source" flow based on the provided fraction of the calculated Unit2 value assumed to come from Node C.
4. Builds a flow value from Node B to Node D to "discharge" the estimated value based on the provided fraction of the calculated value assumed to go to Node D.

This process is repeated for all nodal relationships within each region provided in the input data.

A real-world example of the above would be:

1. The total gallons of water withdrawn from the water supply (Node A) and delivered to the public water supply (Node B) is 100 gallons.
2. The energy required to withdraw a gallon of water from the water supply (Node A) by the public water supply sector (Node B) is 5 british thermal units (btu) per gallon. This calculates out to 500 btu in total based on the initial flow value.
3. The fraction of energy used in the public water supply sector that is supplied by the electricity sector (Node C) is estimated to be 100%. Therefore, the energy flow value connecting the electricity sector (Node C) to the public water supply sector (Node B) is 500 btu.
4. The fraction of energy used in the public water supply sector (Node B) that is lost to rejected energy (efficiency losses) is 35%. Therefore, the energy flow value connecting the public water supply sector (Node B) and the rejected energy node (Node D) is 0.35*500 = 175 btu.

The diagram below shows each of these steps.

![image](https://user-images.githubusercontent.com/74064300/153686911-fd0ec47d-571d-455c-bde8-e8b05a13bac0.png)

Note that **interflow** does not require node inputs and outputs to be balanced. That is to say, inflows to a node do not have to equal outflows as demonstrated above with only 35% of the energy inflow calculated for public water supply being discharged.

Additionally, while the capability is provided to calculate alternate-unit flows (step 2 above) from input values, this is not a requirement. That is to say, a user could simply provide flow values connecting various nodes in step 1 and the model will simply return those flows unless told to do otherwise.

The example walked through above is a high level example of the flow process that demonstrates what is referred to in this documentation as "level 1" granularity. **flow** is capable of calculating and handling sectors up to five levels of granularity. To equate that to the previous example, a level 1 sector would be the public water supply sector. Level 2 and beyond splits up the level 1 sector into subsectors, sub-subsectors, and so on. An example of a level 2 granularity using the above example would be Water Supply - Fresh (i.e., the portion of the total Water Supply sector that is fresh water as opposed to saline water).

Up to five levels of granularity can be specified for each node. Various examples of level 5 granularity include the following:

+------------------------+----------------+----------------+------------------------------+------------------------+
| Level 1                | Level 2        | Level 3        | Level 4                      | Level 5                |
+========================+================+================+==============================+========================+
| Electricity Generation | Natural Gas    | Combined Cycle | Carbon Capture Sequestration | Recirculating Cooling  |
+------------------------+----------------+----------------+------------------------------+------------------------+
| Electricity Generation | Natural Gas    | Combined Cycle | Carbon Capture Sequestration | Once Through Cooling   |
+------------------------+----------------+----------------+------------------------------+------------------------+
| Water Supply           | Fresh          | Surface Water  | Lake                         | Lake Michigan          |
+------------------------+----------------+----------------+------------------------------+------------------------+

More information on generalizability and input data format requirements can be found in the generalizability section.

Aggregation and Output Granularity
**************************************

While highly granular data can provide significant insight into the finer details of a sector, big picture relationships can also be informative. As **interflow** loops through the provided sectors as the various levels of granularity and builds connections, it also tracks sums for each level of granularity so that a level of output granularity can be specified when the model is run. For example, if **interflow** calculates energy demand in the public water supply sector for public water supply treatment and public water supply distribution, it will simultaneously be calculating total energy in the public water supply (i.e., their sum).

This aggregation is done based off of both initial input values and calculated values. For example, if electricity delivery to the residential sector is provided as input data, but natural gas delivery to the residential sector is later calculated based on intensity factors, the energy delivered to the residential sector (level 1 granularity) will sum both.


Generalizability
################################

Organizing input data
*************************

Introduction
-------------------------

Though the **interflow** package comes with sample data for the US for the year 2015 to calculate water and energy interdependencies, alternative input data can be provided to calculate different flows for any region or set of regions, any unit or set of units, and any sector or set of sectors so long as the input data is provided in the correct format.

The **interflow** package requires a csv file with strict guidelines as input data to run calculations. Though different types of calculations are conducted in the **interflow** package, the input into each calculation is provided in the same input file.

The four different types of calculations the **interflow** package conducts include the following:

1. Collect input starting values from Node A to Node B in unit type 1
2. Calculate an alternative unit flow value based on an intensity factor for Node B
3. Calculate a source inflow connecting Node C to Node B
4. Calculate a discharge outflow connecting Node B to Node D

Each of the above calculation types requires a specific format in the input data that are described in more detail below.

Input data descriptions
-------------------------

The input data for the flow package must have 16 columns described below and each value must be in the column order described below. The **interflow** package builds a nested dictionary of the input values leading to the various parameter values.

+---------------+------------------------------+----------+
| Column #      | Description                  | Type     |
+---------------+------------------------------+----------+
| 1             | Region                       | str      |
+---------------+------------------------------+----------+
| 2             | Calculation type             | str      |
+---------------+------------------------------+----------+
| 3             | Primary Node Level 1 Name    | str      |
+---------------+------------------------------+----------+
| 4             | Primary Node Level 2 Name    | str      |
+---------------+------------------------------+----------+
| 5             | Primary Node Level 3 Name    | str      |
+---------------+------------------------------+----------+
| 6             | Primary Node Level 4 Name    | str      |
+---------------+------------------------------+----------+
| 7             | Primary Node Level 5 Name    | str      |
+---------------+------------------------------+----------+
| 8             | Primary Node Units           | str      |
+---------------+------------------------------+----------+
| 9             | Secondary Node Level 1 Name  | str      |
+---------------+------------------------------+----------+
| 10            | Secondary Node Level 2 Name  | str      |
+---------------+------------------------------+----------+
| 11            | Secondary Node Level 3 Name  | str      |
+---------------+------------------------------+----------+
| 12            | Secondary Node Level 4 Name  | str      |
+---------------+------------------------------+----------+
| 13            | Secondary Node Level 5 Name  | str      |
+---------------+------------------------------+----------+
| 14            | Secondary Node Units         | str      |
+---------------+------------------------------+----------+
| 15            | Parameter                    | str      |
+---------------+------------------------------+----------+
| 16            | Value of parameter           | flt      |
+---------------+------------------------------+----------+


Region (columm 1)
""""""""""""""""""""""""""""""

The first item in the data should include the name of the region provided as a string. Note that **interflow** will treat inconsistent spelling of regions as multiple regions.

Calculation type (columm 2)
""""""""""""""""""""""""""""""
The value of the calculation type must equal one of the following verbatim:
* A_collect
* B_calculate
* C_source
* D_discharge

Each of these inputs tells the model what type of calculation it should be conducting for that row of data.

Primary Node Information (columms 3-8)
""""""""""""""""""""""""""""""""""""""""""""
Data positions 3 through 8 provide information on the primary node (PN). The primary node should be interpreted as the node for which inflows and outflows are determined.
Level 1 name refers to the major sector name, Level 2 refers to the sub-sector name, and so on through level 5. For more information on these levels see the Fundamental Concepts section.
Primary Node units refers to the units that that sector name (which will be assigned to a value) is associated with.

Secondary Node Information (columms 9-14)
""""""""""""""""""""""""""""""""""""""""""""

These data inputs follow the same structure as the primary node but are used to describe the node that is being linked to the primary node as either a source (inflow from),a target node (discharge to), or a node upon which an alternate unit value is calculated (described in greater detail later on this page).

Parameter (columms 15)
""""""""""""""""""""""""""""""""""""""""""""

This data item identifies the type of value in the value column (position 16). The value of this data position can be changed by the user with no effect on calculated outcome. It is provided as an optional data position for the user to organize their input data. Examples (consistent with those in the same data) are shown later on this page.

Value (columms 16)
""""""""""""""""""""""""""""""""""""""""""""

This data item providing one of the following: (1) an input flow value in primary node units, (2) an intensity coefficient (unit 2 required per unit 1) (3) a source flow fraction, or (4) a discharge flow fraction.

Creating input data for different calculations
*************************************************

Collect values
"""""""""""""""""""""""""""""""""""""""""""

To build flows between nodes and calculate cross-unit flows, initial flow values are necessary. For example, if the amount of energy required to withdraw a gallon of water from a larger water supply for the public water supply is a desired flow in the ultimate output, then the amount of water withdrawn from the water supply by the public water supply sector is a required input. Initial values must be supplied in the following way:

* The calculation type (data position 2) must be equal to "A_collect"
* The primary node information (data positions 3-8) must describe the node that is *receiving* the flow from another node
* The secondary node information (data positions 9-14) must describe the node that is discharging to the primary node
* The value (data position 16) must be equal to value of the flow from the secondary to the primary node

Note that, as shown in the below example, while all data positions must be provided, they do not have to be unique. If there is only level 1 through 3 granularity for some of the input data, the remaining levels can be the same and filled with "total" or something equivalent.

Additionally, some input flow values may be provided that the user does not have a source node for but still wants to calculate secondary unit flows based on. An example might be the production of fuels such as coal. These arguably don't have a source node since they are the original source, but we may still want to calculate water use based on a water intensity factor. These values can be provided to the model as circular flows. In this scenario, the primary node name will be equal to the secondary node name. The option is provided in the flow calculate function to remove circular flows from the output dataframe.

Example:

+----------+--------------------+--------------------+-------+---------------+-------------+-------+---------+--------------+-------+---------------+-------+-------+---------+-----------+-------+
|Region    |Calculation type    |PN L1               |PN L2  |PN L3          |PN L4        |PN L5  |PN Units |SN L1         |SN L2  |SN L3          |SN L4  |SN L5  |SN Units | Parameter | value |
+----------+--------------------+--------------------+-------+---------------+-------------+-------+---------+--------------+-------+---------------+-------+-------+---------+-----------+-------+
| Region_1 | A_collect          |Public Water Supply |Fresh  | Surface Water | Withdrawal  | Total | mgd     | Water Supply | Fresh | Surface Water | Total | Total | mgd     |flow_value | 200   |
+----------+--------------------+--------------------+-------+---------------+-------------+-------+---------+--------------+-------+---------------+-------+-------+---------+-----------+-------+


Calculate values
"""""""""""""""""""""""""""""""""""""""""""
Consistent naming and spelling with sectors is very important as values (both collected and calculated) are assigned to the node names provided. The model looks for node names at level 5 granularity to retrieve and calculate values.

In order to calculate secondary unit flow values from collected flow values, the data must be in the following format:

* The calculation type (data position 2) must be equal to "B_calculate"
* The primary node information (data positions 3-8) must describe the node that is *being built* in the secondary units (E.g., public water supply pumping energy in btu)
* The secondary node information (data positions 9-14) must describe the node that the new value is based on and be equal to a node that has been collected.
* The value (data position 16) must be equal to the intensity value to calculate the secondary unit flow from the first unit flow. Examples include kilowatt-hours per gallon, gallons per btu, etc.

Note that when calculating a secondary unit flow for a sector that has flows in both units, the names of those sectors/nodes do not have to be consistent. In the below example, we are naming the level2 through level5 different than we did for the water flows. This is because different nodes are calculated for different units.

Example:

+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------+---------------+------------+-------+---------+-----------+-------+
|Region    |Calculation type |PN L1               |PN L2  |PN L3          |PN L4      |PN L5  |PN Units |SN L1                |SN L2  |SN L3          |SN L4       |SN L5  |SN Units | Parameter | value |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------+---------------+------------+-------+---------+-----------+-------+
| Region_1 | B_calculate     |Public Water Supply |Fresh  | Surface Water | pumping   | Total | btu     | Public Water Supply |Fresh  | Surface Water | Withdrawal | Total | mgd     |intensity  | 2     |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------+---------------+------------+-------+---------+-----------+-------+

Source values
"""""""""""""""""""""""""""""""""""""""""""

Once secondary unit flow values have been calculated by the model, their aggregate value is split into individual flows from various source. For example, if the public water supply sector receives 80% its energy from the electricity sector and 20% from natural gas generators, we would want 80% of our total calculated energy value to be represented as a flow from the electricity node to the public water supply sector and the remaining 20% from the natural gas fuel supply

To split calculated values into sources, the following is required:

* The calculation type (data position 2) must be equal to "C_source"
* The primary node information (data positions 3-8) must describe the node that is *receiving* the flow from another node (e.g., energy use in public water supply)
* The secondary node information (data positions 9-14) must describe the node that is discharging to the primary node (e.g., electricity sector)
* The value (data position 16) must be the fraction of the calculated value that is coming from the secondary node.


Example:

+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------------+----------+---------+-------+---------+-----------+-------+
|Region    |Calculation type |PN L1               |PN L2  |PN L3          |PN L4      |PN L5  |PN Units |SN L1                |SN L2        |SN L3     |SN L4    |SN L5  |SN Units | Parameter | value |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------------+----------+---------+-------+---------+-----------+-------+
| Region_1 | C_source        |Public Water Supply |Fresh  | Surface Water | pumping   | Total | btu     | Electricity Gen.    |total        | total    | total   | Total | btu     |fraction   | .8    |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------------+----------+---------+-------+---------+-----------+-------+
| Region_1 | C_source        |Public Water Supply |Fresh  | Surface Water | pumping   | Total | btu     | Fuel Supply         |natural gas  | total    | total   | Total | btu     |fraction   | .2    |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+---------------------+-------------+----------+---------+-------+---------+-----------+-------+

As many source rows should be provided as there are sources for a particular value. If five nodes feed into a single node, five rows with five fractions that sum to 1 should be provided.


Discharge values
"""""""""""""""""""""""""""""""""""""""""""
Discharging values follows similar logic as determining source flows in that an aggregate value is split into multiple based on provided fractions. This time, however, the flows being determined are those that are discharged from the primary node (e.g., electricity generation to rejected energy, public water supply to conveyance losses)

To split calculated and collected values into discharges, the following is required:

* The calculation type (data position 2) must be equal to "D_discharge"
* The primary node information (data positions 3-8) must describe the node that is *discharging* the flow to another node
* The secondary node information (data positions 9-14) must describe the node that is receiving the discharged flow
* The value (data position 16) must be the fraction of the calculated value that should go to the secondary node.


Example:

+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+------------------+-------------+----------+---------+-------+---------+-----------+-------+
|Region    |Calculation type |PN L1               |PN L2  |PN L3          |PN L4      |PN L5  |PN Units |SN L1             |SN L2        |SN L3     |SN L4    |SN L5  |SN Units | Parameter | value |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+------------------+-------------+----------+---------+-------+---------+-----------+-------+
| Region_1 | C_source        |Public Water Supply |Fresh  | Surface Water | pumping   | Total | btu     | Rejected Energy  |total        | total    | total   | Total | btu     |fraction   | .3    |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+------------------+-------------+----------+---------+-------+---------+-----------+-------+
| Region_1 | C_source        |Public Water Supply |Fresh  | Surface Water | pumping   | Total | btu     | Energy Services  |total        | total    | total   | Total | btu     |fraction   | .7    |
+----------+-----------------+--------------------+-------+---------------+-----------+-------+---------+------------------+-------------+----------+---------+-------+---------+-----------+-------+


As many discharge rows should be provided as there are discharges for a particular value. If one values should be discharged to five downstream nodes, five rows with five fractions that sum to 1 should be provided.

For source and discharge fractions, it is not a strict requirement that the fractions per primary node value sum to one. Note that, not having them sum to 1 will lead to unbalanced flows (greater inflows than outflows or vice versa)

Map Data requirements
*******************************************

In order to use the optional cloropleth map visualization output that is included in the package, a GeoJSON file containing geometry information for the specified region(s) must be included. The feature.id in the GeoJSON file should match the region column in the output data in order to display correctly. The **interflow** package comes with a GeoJSON file for US counties, an example of what the GeoJSON file structure looks like is provided below:

![image](https://user-images.githubusercontent.com/74064300/157086892-edb4027d-b6c5-40d3-80c1-107060a0b07d.png)

The image above and the GeoJSON file used for the sample data is part of Plotly's sample datasets. For more information on the sample GeoJSON file, see the Geospatial section under the US Sample Data Methodology Page.

The cloropleth map output uses the plotly python package. For more information on the GeoJSON input see the GeoJSON with feature.id section within the Plotly cloropleth documentation (https://plotly.com/python/choropleth-maps/)