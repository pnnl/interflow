*****************************
Transportation Sector (TRA)
*****************************

Water in Transportation Sector
################################################

No water is assumed to be delivered to the transportation sector.

Energy in Transportation Sector
################################################

Energy Demand
**********************************

Fuel Demand
-----------------------------
Energy demand by the transportation sector is supplied on a state-basis from U.S. EIA for 2015. EIA provides information on energy supply (fuels) that go to sectors other than electricity generation in their SEDS dataset [8]. Each fuel is given in BTUs per year and is categorized by a specific MSN code. For the transportation sector, this includes the following MSN codes.

* "NGACB" - Natural gas consumed by the transportation sector
* "PAACB" - All petroleum products consumed by the transportation sector
* "EMACB" - Fuel ethanol, excluding denaturant, consumed by the transportation sector

Values are adjusted to BBTU per day.

To split up state total values to individual counties within a state, total values are split out based on county population. For example, if County 1 in State A makes up 10% of the total state population, then 10% of the state total natural gas deliveries to the transportation sector are in that county. County population data for 2015 is directly provided in Dieter et al. [1]

Electricity Demand
-----------------------------
Electricity demand by the residential sector is also supplied by US EIA for 2015. Electricity delivery values are used from the Electric Power Annual dataset for residential, commercial, industrial, and transportation sectors [9]. Values are originally provided in annual MWh and are converted to BBTU per day. State level values are broken up into county-level approximations based on population following the same methodology as the fuel deliveries.

Energy Discharge
**********************************

Energy Services
-----------------------------
The transportation sector is assumed to have an efficiency of 21%, in line with estimates provided in Greenberg et al. [4]. Therefore, 21% of all energy used in the transportation sector is assumed to go to energy services.

Rejected Energy
-----------------------------
Given the assumed efficiency of 21%, 79% of energy in the transportation sector is assumed to go to rejected energy.
