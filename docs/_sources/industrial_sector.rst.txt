**************************
Industrial Sector (IND)
**************************

Water in the Industrial Sector
################################################

**Water Demand**
**********************************

*Water Withdrawals*
-----------------------------
Water withdrawal (self-supply) values are directly provided in the Dieter et al. [1] at a county level and are used directly. This includes fresh and saline water from both surface and ground sources.

*Public Water Deliveries*
-----------------------------
Public water deliveries (public water demand) to the industrial sector are not directly provided in Dieter et al. [1] for 2015 for each county. The most recent year these values are provided is for 1995 from the USGS 1995 water use report (Solley et al. [7]). In order to estimate public water deliveries to the industrial sector, the ratio of deliveries to the industrial sector compared to deliveries to the residential and thermoelectric cooling in aggregated in 1995 is applied to 2015 residential and thermoelectric cooling delivery values. That is, if the 1995 ratio of industrial water deliveries from public water supply was half that of public water deliveries to the residential sector and thermoelectric cooling in aggregate in an individual county, then the 2015 public water deliveries to the industrial sector would be equal to half the public water deliveries to the residential sector and thermoelectric cooling in aggregate for 2015.

For 1995 counties that do not have public water deliveries to the industrial sector, the average ratio for the given state is applied instead. Note that this may overestimate public water deliveries to industrial sector in some counties. No counties that have at least some public deliveries to either the residential sector or thermoelectric cooling will have 0 public water deliveries to the industrial sector.

**Water Discharges/Consumption**
**********************************

*Consumption/Evaporation*
-----------------------------
Consumption of water by the industrial sector is not provided in the Dieter et al. [1] water dataset. The most recent year with data available is the 1995 USGS water use report (Solley et al. [7]). Instead of directly using the consumptive use (mgd) from the industrial sector from the 1995 factor, consumption fractions (%) for fresh water and saline water were individually calculated based on the ratio of water consumed by the industrial sector and total water flows to the industrial sector in 1995. In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted.

*Discharge*
-----------------------------

* **Water Discharge to Surface** - It is assumed that all fresh water and all saline groundwater that is not from public water sources and is not consumed, is discharged to the surface.
* **Water Discharge to Ocean** - It is assumed that all saline surface water withdrawn by the industrial sector and not consumed, is discharged to the ocean.
* **Water Discharge to Wastewater Supply** - It is assumed that all public water deliveries to the industrial sector that are not consumed are discharged to wastewater supply.

Energy in the Industrial Sector
################################################

**Energy Demand**
**********************************

*Fuel Demand*
-----------------------------
Energy demand by the industrial sector is supplied on a state-basis from U.S. EIA for 2015. EIA provides information on energy supply (fuels) that go to sectors other than electricity generation in their SEDS dataset [8]. Each fuel is given in BTUs per year and is categorized by a specific MSN code. For the industrial sector, this includes the following MSN codes.

* PAICB - All petroleum products consumed by the industrial sector
* WWICB - Wood and waste energy consumed in the industrial sector
* NGICB - Natural gas consumed by the industrial sector
* CLICB - Coal consumed by the industrial sector

Values are adjusted to BBTU per day.

To split up state total values to individual counties within a state, total values are split out based on county population. For example, if County 1 in State A makes up 10% of the total state population, then 10% of the state total natural gas deliveries to the industrial sector are in that county. County population data for 2015 is directly provided in Dieter et al. [1]

*Electricity Demand*
-----------------------------
Electricity demand by the residential sector is also supplied by US EIA for 2015. Electricity delivery values are used from the Electric Power Annual dataset for residential, commercial, industrial, and transportation sectors [9]. Values are originally provided in annual MWh and are converted to BBTU per day. State level values are broken up into county-level approximations based on population following the same methodology as the fuel deliveries.

**Energy Discharge**
**********************************

*Energy Services*
-----------------------------
The industrial sector is assumed to have an efficiency of 49%, in line with estimates provided in Greenberg et al. [4]. Therefore, 49% of all energy used in the industrial sector is assumed to go to energy services.

*Rejected Energy*
-----------------------------
Given the assumed efficiency of 49%, 51% of energy in the industrial sector is assumed to go to rejected energy.