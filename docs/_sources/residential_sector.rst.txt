**************************
Residential Sector (RES)
**************************

Water in Residential Sector
################################################

Water Demand
**********************************

Water Supply Withdrawals
-----------------------------
Water withdrawals to the residential sector are taken from Dieter et al. [1] for 2015 for each county in mgd.

Public Water Deliveries
-----------------------------

Public water deliveries (public water demand) to the residential sector are provided directly in Dieter et al. [1] for 2015 for each county in mgd. These are collected as public water demand flows to residential public water.

Water Discharge
**********************************

Consumption/Evaporation
-----------------------------

Consumption of water by the residential sector is not provided in the Dieter et al. [1] water dataset. The most recent year with data available is the 1995 USGS water use report (Solley et al. [7]). Instead of directly using the consumptive use (mgd) from the residential sector from the 1995 factor, a consumption fraction (%) was calculated based on the ratio of water consumed by the residential sector and total water flows to the residential sector in 1995. It is assumed that fresh surface water, fresh groundwater, and public water are consumed at the same rate by the residential sector.

In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted.

Discharge to surface
-----------------------------

It is assumed that all water that is not from public water sources (self-supplied water) that is not consumed, is discharged to the surface. No water is assumed to be discharged to the ocean or ground by the residential sector.

Discharge to Wastewater Supply
----------------------------------------------------------


It is assumed that all public water deliveries to the residential sector are discharged to wastewater supply.

Energy in Residential Sector
################################################

Energy Demand
**********************************

Fuel Demand
----------------------------------------------------------

Energy demand by the residential sector is supplied on a state-basis from U.S. EIA for 2015. EIA provides information on energy supply (fuels) that go to sectors other than electricity generation in their SEDS dataset [8]. Each fuel is given in BTUs per year and is categorized by a specific MSN code. For the residential sector, this includes the following MSN codes.

* "NGRCB" - Natural gas consumed by (delivered to) the residential sector
* "PARCB" - All petroleum products consumed by the residential sector
* "WDRCB" - Wood energy consumed by the residential sector
* "GERCB" - Geothermal energy consumed by the residential sector
* "SORCB" -  Solar energy consumed by the residential sector

To split up state total values to individual counties within a state, total values are split out based on county population. For example, if County 1 in State A makes up 10% of the total state population, then 10% of the state total natural gas deliveries to the residential sector are in that county. County population data for 2015 is directly provided in Dieter et al. [1]

Electricity Demand
----------------------------------------------------------
Electricity demand by the residential sector is also supplied by US EIA for 2015. Electricity delivery values are used from the Electric Power Annual dataset for residential, commercial, industrial, and transportation sectors [9]. Values are originally provided in annual MWh and are converted to BBTU per day. State level values are broken up into county-level approximations based on population following the same methodology as the fuel deliveries.

Energy Discharge
**********************************

Energy Services
-----------------------------

The residential sector is assumed to have an efficiency of 65%, in line with estimates provided in Greenberg et al. [4]. Therefore, 65% of all energy used in the residential sector is assumed to go to energy services.

Rejected Energy
-----------------------------

Given the assumed efficiency of 65%, 35% of energy in the residential sector is assumed to go to rejected energy.
