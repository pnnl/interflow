**************************
Commercial Sector (COM)
**************************

Water in Commercial Sector
################################################
Commercial water use includes "water for motels, hotels, restaurants, office buildings, other commercial facilities, military and nonmilitary institutions" (Dieter et al. [1])


**Water Demand**
**********************************

*Water Supply Withdrawals*
-----------------------------

No withdrawal (self-supply) values are provided in the 2015 USGS dataset (Dieter et al. [1]) and none are assumed for the commercial sector. All water for the commercial sector is assumed to be delivered from the public water supply.

*Public Water Deliveries*
-----------------------------
Public water deliveries (public water demand) to the commercial sector are not directly provided in Dieter et al. [1] for 2015 for each county. The most recent year these values are provided is for 1995 from the USGS 1995 water use report (Solley et al. [7]). In order to estimate public water deliveries to the commercial sector, the ratio of deliveries to the commercial sector compared to deliveries to the commercial and thermoelectric cooling in aggregated in 1995 is applied to 2015 commercial and thermoelectric cooling delivery values. That is, if the 1995 ratio of commercial water deliveries from public water supply was half that of public water deliveries to the commercial sector and thermoelectric cooling in aggregate in an individual county, then the 2015 public water deliveries to the commercial sector would be equal to half the public water deliveries to the commercial sector and thermoelectric cooling in aggregate for 2015.

For 1995 counties that do not have public water deliveries to the commercial sector, the average ratio for the given state is applied instead. Note that this may overestimate public water deliveries to commercial sector in some counties. No counties that have at least some public deliveries to either the commercial sector or thermoelectric cooling will have 0 public water deliveries to the commercial sector.

**Water Discharges/Consumption**
**********************************

*Consumption/Evaporation*
-----------------------------
Consumption of water by the commercial sector is not provided in Dieter et al. [1]. The most recent year with data available is the 1995 USGS water use report. Instead of directly using the consumptive use (mgd) from the commercial sector from the 1995 factor, a consumption fraction (%) was calculated based on the ratio of water consumed by the commercial sector and total water flows to the commercial sector in 1995. In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted.

*Discharge to Wastewater Supply*
---------------------------------------
It is assumed that all public water deliveries to the commercial sector are discharged to wastewater supply. Since no self-supply is assumed for the commercial sector, there are no other discharges assumed.

Energy in Commercial Sector
################################################

**Energy Demand**
**********************************

*Fuel Demand*
-----------------------------
Energy demand by the commercial sector is supplied on a state-basis from U.S. EIA for 2015. EIA provides information on energy supply (fuels) that go to sectors other than electricity generation in their SEDS dataset [8]. Each fuel is given in BTUs per year and is categorized by a specific MSN code. For the commercial sector, this includes the following MSN codes.

* NGCCB - Natural gas consumed by (delivered to) the commercial sector
* PACCB - All petroleum products consumed by the commercial sector
* WWCCB - Wood and waste energy consumed in the commercial sector
* CLCCB - Coal consumed by the commercial sector
* GECCB - Geothermal energy consumed by the commercial sector
* SOCCB - Solar energy consumed by the commercial sector
* WYCCB - Wind energy consumed by the commercial sector

Values are adjusted to BBTU per day.

To split up state total values to individual counties within a state, total values are split out based on county population. For example, if County 1 in State A makes up 10% of the total state population, then 10% of the state total natural gas deliveries to the commercial sector are in that county. County population data for 2015 is directly provided in Dieter et al. [1]

*Electricity Demand*
-----------------------------

Electricity demand by the residential sector is also supplied by US EIA for 2015. Electricity delivery values are used from the Electric Power Annual dataset for residential, commercial, industrial, and transportation sectors [9]. Values are originally provided in annual MWh and are converted to BBTU per day. State level values are broken up into county-level approximations based on population following the same methodology as the fuel deliveries.

**Energy Discharge**
**********************************

*Energy Services*
-----------------------------
The commercial sector is assumed to have an efficiency of 65%, in line with estimates provided in Greenberg et al. [4]. Therefore, 65% of all energy used in the commercial sector is assumed to go to energy services.

*Rejected Energy*
-----------------------------
Given the assumed efficiency of 65%, 35% of energy in the commercial sector is assumed to go to rejected energy.