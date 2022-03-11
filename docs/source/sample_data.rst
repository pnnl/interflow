**************************
Sample Data
**************************

Introduction
##############

The motivation of the Integrated Water Power Resilience Project is to identify and develop opportunities to improve resilience in the water and power sectors through coordinated planning, investment, and operations and thereby provide benefits to power and water utilities, consumers, and the environment.
Water and power utilities are interdependent, subject to many of the same natural and manmade hazards, and critical for the well-being of communities and society. Because of the interconnectedness of water and power systems there are substantial economic, social, and environmental benefits to co-managing the market sectors for resilience, instead of managing them separately.
To support this initiative and future research in this area, the **interflow** model was developed to build, calculate, and visualize interconnections in water and energy between various sectors.


Overview
####################

The following list of assumptions are applicable to the 2015 US sample data:

*  Calculations are for the year 2015, the most recent year available for comprehensive county-level water use data in the US. When data was unavailable for 2015, the closest year available was applied or methods were developed to develop data for 2015 based on factors from previous years.
*  Many calculation methodologies and intensity parameters are informed by the literature. References for these methodologies are noted in the methodology descriptions as applicable.
*  Water values are provided in million gallons per day (MGD) and energy values are provided in billion British thermal units (BBTU) per day
*  Data was available at various levels of granularity across the US including plant-level, county-level, state-level, and aggregate estimates for the entire US. Data was aggregated or split out appropriately so that the resulting dataset contains values on the county-level, given by county FIPS code. When data collected was provided at the state-level, state-level totals are divided among state counties through an appropriate method (e.g. population weighting). When information was available at the plant level (e.g. power plant generation), information on plant county were used to sum plant values to achieve a county total. US level estimates were predominantly related to intensity factors or fractions. For example, the fraction of all corn grown for ethanol fuel is a US-level estimate and applied to county-level corn production.

All data used in the 2015 US Case Study including input flow values, energy or water intensity values, discharge fractions, and others are described in the various methodology sections. References to each can be found on the references page. A folder containing all input data is also provided with the package.

Geospatial Information
##############################

US Counties
**********************************

In order to get values at the county-level across multiple datasets in a consistent manner, a set of counties was established as the base county list for 2015. This list contains all US counties (not including US Territories) included in the USGS 2015 water use dataset (Dieter et al. [1]). Given that some datasets used in compiling the full sample dataset are from multiple years, some of the county-level FIPS codes required modification in order to match those provided in the 2015 base list. These modifications include mapping older FIPS codes to the 2015 ones or adding new FIPS codes when new counties were created. These modifications were mostly required for values used in from the 1995 USGS dataset Solley et al. [7]).

For the full list of US counties and their corresponding FIPS codes, see the `county list <https://kmongird.github.io/interflow/county_list.html>`_

GeoJSON
**********************************

In order to plot county-level outputs from the US 2015 dataset, a GeoJSON file containing geometry information for the US counties is required. The file used and included in the sample data is from Plotly's sample datafiles. The raw JSON datafile can be found in Plotly [19]. A small number of counties included in the GeoJSON file required adjustment to match the baseline county list for the sample data. The FIPS codes for these counties were adjusted accordingly in the GeoJSON file. Note that the modified version of this file is included in the input data, not the raw GeoJSON file.

For more information on the base map configuration for Plotly's cloropleth maps, see the `Plotly cloropleth map documentation <https://plotly.com/python/choropleth-maps/>`_


Methodology
####################

This section documents the methodology, data, and assumptions used in building the us county input data. Information is presented by sector and then subdivided by resource (water and energy).

Agriculture Sector
**********************************
Crop irrigation, golf irrigation, livestock, and aquaculture

Water in Agriculture
-------------------------------------------------------------------------------------------------------------------------------

Water Demand
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Water Supply Withdrawals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Water withdrawals to the various agriculture sectors are provided by US Geological Survey (USGS) (Dieter et al. [1]) and are provided in million gallons per day (mgd) for each county in 2015. This includes fresh and saline water from both surface and ground sources.
For crop irrigation and golf irrigation, a subset of states did not provide water withdrawal values for these sectors but did provide total irrigation withdrawals (fresh surface and fresh groundwater). For these states, the water withdrawals to total irrigation were used as the values for water withdrawals to crop irrigation. In these states, no water withdrawals were estimated to golf irrigation.

Water Supply Imports (Interbasin transfers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Interbasin transfer flows and energy intensities in each county are provided through data from two sources. For western states, county-level water flows were available from Tidwell et al. [2]. For the state of Texas, county-level interbasin transfers between specified counties were collected from the Texas Water Development Board [3]. No data is currently available for interbasin transfers in eastern US counties. For these counties, the value is assumed to be zero.

Interbasin transfers are used for both public water supply as well as for irrigation purposes. To determine how much of the total interbasin transfer flows in each county goes to crop irrigation versus public water supply, the methodology from Greenberg et al. [4] is adapted which uses the ratio of water flows to crop irrigation vs. public water supply to split the values. The ratio is determined by taking the ratio of all water withdrawals to crop irrigation (Fresh surface water and fresh groundwater) over the sum of all water withdrawals to crop irrigation and water withdrawals by the public water supply from Dieter et al. [1]. This determines the percent of total flows to both sectors that goes to crop irrigation. This fraction is multiplied by the total interbasin transfer flow to determine how much of the interbasin transfer flow goes to crop irrigation. Any interbasin transfer flow that does not go to crop irrigation is assumed to go to the public water supply. It should be noted that interbasin transfers are only assumed to go to crop irrigation and are not used for other agricultural applications such as golf irrigation or livestock.

Texas interbasin transfer Methodology
.................................................

To calculate the total interbasin transfer flows in each Texas county, information from the Texas Water Development Board historical municipal water flow data was used. The data tracks self-supply and purchased water supplies for counties in Texas and tracks their source and used county. To track interbasin transfer flows, only flows that occured between different counties in the year 2015 were included. A small number of data rows had missing values for the source county, these data points were removed from the dataset.

The difference in elevation between counties is used in the formula to calculate required pumping power to transfer water. Elevation data for each of the counties was taken from USGS's GNIS dataset [16] for the state of Texas. The dataset tracks elevation for a variety of locations within counties. The average elevation for all items included in the dataset for each county was assumed as the elevation for that county. The difference in elevation between the source and target counties was calculated. Only transfers that were delivered to a higher elevation were included in the dataset on the assumption that water deliveries to lower elevations would be predominantly gravity-based. Note that the USGS elevation dataset and associated county FIPS codes have been added into the same datafile as the water transfer data from the Texas Water Development Board and these were not included in the original water data file.

Water flows were provided on a gallons/year basis. This was converted to million gallons per day.

Western States interbasin transfer Methodology
..............................................................
Interbasin transfer flows were available for the states of Idaho, California, Arizona, Utah, Washington, Nevada, Colorado, Oregon, Montana, New Mexico, and Wyoming in Tidwell et al. [2]. Most rows in the dataset provided water flow values on a cubic feet per second basis, which were converted to mgd (1 cfs = 0.646317 mgd). For rows that did not provide cfs, acre-ft per year were provided and converted to mgd using the same methodology as the Texas calculation described above.

Water Supply Imports (Reclaimed wastewater)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Reclaimed wastewater deliveries to crop irrigation are directly provided in Dieter et al. [1] at the county level. For states where crop irrigation water values are not provided but total irrigation values are supplied, crop irrigation water values are assumed to be equal to total irrigation water flows. Following the same methodology, reclaimed wastewater flows to total irrigation are used as the values for reclaimed wastewater deliveries to crop irrigation.

Public Water Deliveries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
No public water deliveries to agriculture are provided and none are assumed.

Water Discharges/Consumption
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Consumption/Evaporation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Crop irrigation and golf irrigation consumptive use values are directly available in Dieter et al. [1]. Consumption fractions for fresh surface water and fresh groundwater were directly calculated from these values. In some counties, the amount of water consumed in irrigation was greater than the amount withdrawn. For these counties, the consumption fraction is set to 1.

Consumption fractions of water by aquaculture and livestock are not provided in Dieter et al. [1]. The most recent year with data available is the 1995 USGS water use report (Solley et al. [7]). Instead of directly using the consumptive use (mgd) provided, consumption fractions (%) for fresh water and saline water were individually calculated based on the ratio of water consumed by each agricultural sector and total water flows to that agricultural sector in 1995.

In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted. For states that were missing values for all of their counties the US average was substituted. For counties that had consumption fractions greater than one (presumably due to inconsistent data reporting), the consumption fraction was set to 1.

Irrigation Conveyance Losses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Irrigation conveyance loss values are not available in Dieter et al. [1] but are available in Solley et al. [7] for 1995. These mgd conveyance loss values are converted to conveyance loss fractions by taking the ratio of water lost to conveyance in 1995 to the total water delivered to irrigation in 1995. Specific values for crop irrigation and golf irrigation are not available in the 1995 dataset. Therefore, it is assumed that the conveyance loss fraction for both crop irrigation and golf irrigation are equal to the conveyance loss fraction per county for total irrigation for 1995.

For counties within a state that have conveyance loss fractions of zero, the state average (inclusive of zero values) is supplied. For states with no conveyance loss values for any county, the US average conveyance loss fraction is applied. Note that, through this method, there will be no counties in the US that have 0 conveyance losses if they have water flows to crop or golf irrigation.

The conveyance loss fractions calculated per county include values assumed to be outliers (some greater than 150% of their flows lost to conveyance losses) and are assumed to be data collection errors. In order to account for these values, a conveyance loss fraction cap was implemented where the maximum amount of water lost to conveyance losses in irrigation is 90% of water flows. This value is still considerably high, however, without more detailed and recent information, it is difficult to determine accuracy.

No conveyance losses are currently assumed for non-irrigation agriculture sectors. No adjustments have been made to convert 1995 values to 2015 values.

Discharge to surface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is assumed that all fresh water delivered to agriculture sectors to that is not consumed or lost during conveyance, is discharged to the surface.

Discharge to ocean
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is assumed that all saline water delivered to agriculture sectors that is not consumed or lost during conveyance, is discharged to the ocean.

## Energy in Agriculture
-------------------------------------------------------------------------------------------------------------------------------
Energy Demand
""""""""""""""""""""""""""""""""
Water Withdrawal Pumping Energy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
USDA FRIS [5] provides information on the breakdown of power type per pump in irrigation applications for each state. This includes the percentage breakdown between electricity, propane, diesel, and gas. For simplification purposes, propane and diesel have been binned into the same fuel category. These percentages are used for all counties in each given state to determine what fraction of the total energy in agriculture comes from each fuel source. It is assumed that the same breakdown applies to all agriculture applications, not just irrigation.

USDA's Farm and Ranch Irrigation Survey (FRIS) [5] provides state-by-state data on irrigation groundwater depth and average irrigation pressurization levels for irrigation within a state, enabling the calculation of pump electricity consumption for both groundwater and surface water pumping. The 2013 survey is the closest year available to 2015 values. It is assumed that values do not vary significantly between the two years.

The methodology for calculating groundwater and surface water pumping energy is described in Pabi et al [12]. The function presents a way to calculate the required kwh per day to pump water based on an assumed flow rate (gallons per minute), pumping head (total differential height inclusive of pressurization), and the assumed pump efficiency. This formula is reproduced below. Note that 3960 is the water horsepower, 0.746 is the conversion factor between horsepower and kilowatts, and 24 is simply the number of hours in a day.

Electricity (kWh/day) = ((Flow (gpm) x pumping head (ft)) / (3960 x pumping efficiency)) x 0.746 x 24

The above equation was modified to produce a bbtu per million gallon pumping intensity rate by setting the flow value to the gallons per minute equivalent to 1 million gallons per day (694.4 gpm) and converting kwh to bbtu.

While some research uses well depth to water to calculate total differential height, the total well depth is used here instead as a way to offset some of the losses due to friction that would occur in the piping, as described in Lawrence Berkeley National Laboratory (LBNL) Home Energy Saver & Score: Engineering Documentation [6]. Pump efficiency is assumed to be the average (46.5%) of the range (34-59%) listed in Tidwell et al. [2]. State-level intensity rates are calculated here and applied to the county level water in the agriculture sectors.

In order to calculate surface water pumping energy, the same methodology is used as calculating groundwater but the well-depth is set to 0 ft.

Interbasin-transfer Pumping Energy
.........................................
The energy intensity required for interbasin transfers was calculated on a per-county basis from values provided in Tidwell et al. [2] and the Texas Water Development Board [3].

Texas Interbasin Transfers
::::::::::::::::::::::::::::::::::::::::::::::::

To calculate the power required for interbasin transfers in Texas, the equation for power required to perform a static lift presented in Tidwell et al. [2] was used. The power required is equal to the product of the mass flow rate of water (cubic meters/hr), the liquid density of water (997 kg/m^3), the acceleration due to gravity (9.81 m/s^2), and the differential height (meters). This product is then divided by the assumed pumping efficiency (46% here). This gives the total watts per hour required to pump the water from one county to the other which is then converted to bbtu/day.

Each value in the Texas interbasin transfer data is associated with two counties (source and target county). Given a lack of more detailed data, it is assumed that half of the water flow and half of the subsequent energy required is split evenly between the two counties.

The energy intensity of interbasin transfers in Texas is the ratio of energy required per day to water moved per day.

Western States Interbasin Transfers
::::::::::::::::::::::::::::::::::::::::::::::::

Energy for interbasin transfers in the west was provided directly in Tidwell et al. [2] for the states included. Low (mwh/yr) and high (mwh/yr) values were provided . The average of these values was taken for this analysis and converted to bbtu/day.

The energy intensity for interbasin transfers in western counties is the ratio of energy demand per day to water moved per day.

Energy Services
""""""""""""""""""""""""""""""""
Each subsector in the agriculture sector is assumed to have 65% efficiency following estimates provided in Greenberg et al. [4]. Therefore, 65% of all energy in each agriculture sector is assumed to go to energy services.

Rejected Energy
""""""""""""""""""""""""""""""""
All energy that does not go to energy services is assumed to go to rejected energy, therefore, it is assumed that each agriculture sub-sector sends 35% of its energy to rejected energy.


Commercial Sector
**********************************

Water in Commercial Sector
-------------------------------------------------------------------------------------------------------------------------------

Water Demand
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Water Supply Withdrawals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No withdrawal (self-supply) values are provided in the 2015 USGS dataset (Dieter et al. [1]) and none are assumed for the commercial sector. All water for the commercial sector is assumed to be delivered from the public water supply.

Public Water Deliveries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Public water deliveries (public water demand) to the commercial sector are not directly provided in Dieter et al. [1] for 2015 for each county. The most recent year these values are provided is for 1995 from the USGS 1995 water use report (Solley et al. [7]). In order to estimate public water deliveries to the commercial sector, the ratio of deliveries to the commercial sector compared to deliveries to the commercial and thermoelectric cooling in aggregated in 1995 is applied to 2015 commercial and thermoelectric cooling delivery values. That is, if the 1995 ratio of commercial water deliveries from public water supply was half that of public water deliveries to the commercial sector and thermoelectric cooling in aggregate in an individual county, then the 2015 public water deliveries to the commercial sector would be equal to half the public water deliveries to the commercial sector and thermoelectric cooling in aggregate for 2015.

For 1995 counties that do not have public water deliveries to the commercial sector, the average ratio for the given state is applied instead. Note that this may overestimate public water deliveries to commercial sector in some counties. No counties that have at least some public deliveries to either the commercial sector or thermoelectric cooling will have 0 public water deliveries to the commercial sector.

Water Discharges/Consumption
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Consumption/Evaporation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Consumption of water by the commercial sector is not provided in Dieter et al. [1]. The most recent year with data available is the 1995 USGS water use report. Instead of directly using the consumptive use (mgd) from the commercial sector from the 1995 factor, a consumption fraction (%) was calculated based on the ratio of water consumed by the commercial sector and total water flows to the commercial sector in 1995. In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted.

Discharge to wastewater supply
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is assumed that all public water deliveries to the commercial sector are discharged to wastewater supply. Since no self-supply is assumed for the commercial sector, there are no other discharges assumed.

## Energy in Commercial Sector
-------------------------------------------------------------------------------------------------------------------------------

Energy Demand
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Fuel Demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

Electricity Demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Electricity demand by the residential sector is also supplied by US EIA for 2015. Electricity delivery values are used from the Electric Power Annual dataset for residential, commercial, industrial, and transportation sectors [9]. Values are originally provided in annual MWh and are converted to BBTU per day. State level values are broken up into county-level approximations based on population following the same methodology as the fuel deliveries.


### Energy Discharge
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Energy Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The commercial sector is assumed to have an efficiency of 65%, in line with estimates provided in Greenberg et al. [4]. Therefore, 65% of all energy used in the commercial sector is assumed to go to energy services.

Rejected Energy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Given the assumed efficiency of 65%, 35% of energy in the commercial sector is assumed to go to rejected energy.



Electricity Generation Sector
**********************************

Energy in Electricity Generation
-------------------------------------------------------------------------------------------------------------------------------

Energy Demand (fuel)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Data regarding both the fuel input for each power plant on an annual basis and the electricity generated by each power plant is provided by the US EIA in their 923 dataset for 2015 [13]. The EIA data provides generator types at a higher level of granularity than desired, therefore, power plants were sorted into various simplified generator bins through the following mapping from the AER fuel type codes in the EIA dataset:

+--------------+---------------------------------------------------+---------------+
| AER Code     | AER Code Description                              | Bin           |
+==============+===================================================+===============+
| SUN          | solar                                             | solar         |
+--------------+---------------------------------------------------+---------------+
| COL          | coal                                              | coal          |
+--------------+---------------------------------------------------+---------------+
| DFO          | distillate petroleum                              | petroleum     |
+--------------+---------------------------------------------------+---------------+
| GEO          | geothermal                                        | geothermal    |
+--------------+---------------------------------------------------+---------------+
| HPS          | hydro pumped storage                              | hydro         |
+--------------+---------------------------------------------------+---------------+
| HYC          | hydro conventional                                | hydro         |
+--------------+---------------------------------------------------+---------------+
| MLG          | biogenic municipal solid waste and landfill gas   | biomass       |
+--------------+---------------------------------------------------+---------------+
| NG           | natural gas                                       | natgas        |
+--------------+---------------------------------------------------+---------------+
| NUC          | nuclear                                           | nuclear       |
+--------------+---------------------------------------------------+---------------+
| OOG          | other gases                                       | other         |
+--------------+---------------------------------------------------+---------------+
| ORW          | other renewables                                  | other         |
+--------------+---------------------------------------------------+---------------+
| OTH          | other                                             | other         |
+--------------+---------------------------------------------------+---------------+
| PC           | petroleum coke                                    | petroleum     |
+--------------+---------------------------------------------------+---------------+
| RFO          | residual petroleum                                | petroleum     |
+--------------+---------------------------------------------------+---------------+
| WND          | wind                                              | wind          |
+--------------+---------------------------------------------------+---------------+
| WOC          | waste coal                                        | coal          |
+--------------+---------------------------------------------------+---------------+
| WOO          | waste oil                                         | petroleum     |
+--------------+---------------------------------------------------+---------------+
| WWW          | wood and wood waste                               | biomass       |
+--------------+---------------------------------------------------+---------------+

In addition to primary power plant type, the information on the sub-generation type is also included from the EIA 923 dataset. This includes information such as what kind of turbine a plant uses (e.g., combustion turbine vs. steam). These prime mover acronyms are similarly binned using the following mapping:

+------------------+----------------------------------+
| Prime Mover Code | Bin                              |
+==================+==================================+
|HY                | instream                         |
+------------------+----------------------------------+
|CA                | combinedcycle                    |
+------------------+----------------------------------+
|CT                | combinedcycle                    |
+------------------+----------------------------------+
|ST                | steam                            |
+------------------+----------------------------------+
|GT                | combustionturbine                |
+------------------+----------------------------------+
|IC                | internalcombustion               |
+------------------+----------------------------------+
|WT                | onshore                          |
+------------------+----------------------------------+
|PV                | photovoltaic                     |
+------------------+----------------------------------+
|CS                | combinedcycle                    |
+------------------+----------------------------------+
|CE                | compressedair                    |
+------------------+----------------------------------+
|BT                | binarycycle                      |
+------------------+----------------------------------+
|OT                | other                            |
+------------------+----------------------------------+
|FC                | fuelcell                         |
+------------------+----------------------------------+
|CP                | csp                              |
+------------------+----------------------------------+

Note that pumped storage and batteries appear in the raw EIA data but are not included in the final dataset.

To obtain the cooling type for each of the power plants included in the EIA dataset [13], information is mapped from Harris et. al [14]. Harris et al. [14] provides plant level thermoelectric cooling estimates for the year 2015. Cooling types were mapped to the EIA data by plant code. Note that the dataset in [14] did not provide values for all power plants included in [13]. For these plants, the cooling type was set to 'complex'. For plants that do not require cooling, the cooling type was set to "NoCooling".

Cooling types from [14] were binned in the following way:

+----------------------+----------------------------------+
| Cooling Type         | Bin                              |
+======================+==================================+
|Complex               | Complex                          |
+----------------------+----------------------------------+
|Once-through Fresh    | Oncethrough                      |
+----------------------+----------------------------------+
|Recirculating Tower   | Tower                            |
+----------------------+----------------------------------+
|Recirculating Pond    | Pond                             |
+----------------------+----------------------------------+
|Once-through Saline   | Oncethrough                      |
+----------------------+----------------------------------+

Energy flows into each electricity generator were based on the provided input fuel amount in the EIA dataset. These values were converted from bbtu per year to bbtu per day. Power plants with zero generation and zero fuel were removed from the dataset. For power plants that were missing fuel inputs but had generation outputs provided, an assumed efficiency rating of 30% was used to generate fuel input values. For example, if the generation output for a plant was 10 bbtu per day but no fuel input was provided, the fuel input was estimated to be (1/.3) * 10 bbtu.

Individual power plants were mapped to county FIPS codes based on the listed county within the EIA dataset.

Energy Discharge
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Energy Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Energy services from each generator type is generally equal to the ratio of total electricity generation over the total fuel input from each power plant. However, given that some of the power plants included in the EIA dataset provided generation amounts but no fuel amounts, efficiency fractions for these plants were set to .30. For all other plants, the efficiency rating was set to the ratio of generation over fuel inputs

 Values are summed by generator type within each county to get electricity generation by each generator type by FIPS code. The ratio between energy generation and fuel inputs in each plant gives the overall efficiency rating for that plant. For plants that did not provide fuel input quantities, a 30% efficiency rating was assumed. For some power plants, the fuel input was less than the generation output in bbtu. For these plants, a 30% efficiency rating was assumed.

 The discharge to energy services fraction can be interpreted as the fraction of fuel used in a power plant that is successfully converted to electricity. These flows from electricity generation supply are directly connected to the electricity generation demand node.

Rejected Energy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Rejected energy from electricity generation for each county is calculated as 1 minus the fraction sent to energy services (i.e., electricity generation demand).

Water in Electricity Generation
-------------------------------------------------------------------------------------------------------------------------------

Water Demand
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Withdrawals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Thermoelectric Cooling Water Withdrawals
..............................................

Estimates for water withdrawn for thermoelectric cooling were provided by two sources, Harris et al. [14] and Macknick et al. [15]. The first dataset includes water withdrawals (mgd) and consumption (mgd) by EIA power plant code ID. Some water withdrawal, consumption, and discharge estimates were missing for many of the plants provided in [14] when mapped to the EIA 923 [13] power plant generation data by plant code.

To fill in estimates for the remaining power plants, Macknick et al. [15] values were used. Given that the cooling type of each power plant is unknown, the average cooling water intensity for all cooling types for each generation technology (e.g., nuclear, natural gas) was used from [15]. No values were available for petroleum in [15]. For this generation type, the average of all other technologies was assumed. This same methodology was also applied to 'other' generation types. Though some renewable technologies such as Solar CSP require cooling, no withdrawal values were provided in [15]. Total water withdrawal per plant for missing estimates was calculated as the water withdrawal intensity (gallons/mwh of generation) multiplied by the estimated power plant generation in EIA 923 [13]. The same methodology was applied for consumption quantities using consumption intensity estimates from Macknick et al. [15].

Harris et al. [14] additionally provides information on the water source and water type for each withdrawal flow for each power plant. These values were used to map water withdrawal flows for each power plant to a specific water source node. For simplicity, water types were binned into categories as follows:

* 'SW': 'surfacewater'  (river, canal, bay)
* 'GW': 'groundwater',  (well, aquifer)
* 'PD': 'wastewater',  (PD = plant discharge)
* "-nr-": "surfacewater",  (all blanks assumed to be surface water)
* "GW & PD": "groundwater",  (all GW+PD are assumed to be groundwater only)
* "GW & SW": 'surfacewater',  (all GW+SW combinations are assumed to be surface water)
* "OT": "surfacewater" (all "other" water source is assumed to be surface water)

Similarly, information on water type were binned in the following way:
* 'FR': 'fresh'
* 'SA': 'saline'
* 'OT': 'fresh'  (all other source is assumed to be fresh water)
* "FR & BE": 'fresh'  (all combinations with fresh and BE are assumed to be fresh)
* "BE": "fresh"  (reclaimed wastewater set to fresh)
* "BR": "saline" (all brackish is set to saline)
* "": "fresh"  (all blanks are assumed to be fresh)

It is assumed that all water withdrawal estimates not provided in [14] and generated by water withdrawal intensity estimates in [15] come from fresh surface water and the cooling type has been set to 'Complex'.

Note that some power plants have fuel inputs and generation amounts but had 0 water withdrawals in Harris et al. [14]. These values are not adjusted as they are assumed to be recirculating cooling type with negligible water withdrawals.

Hydropower Water Use
..............................................
Water use in hydropower is not available in the 2015 USGS water dataset (Dieter et al. [1]), however, it is available in the 1995 USGS water use dataset (Solley et al. [7]). The 1995 dataset provides water use for instream hydropower by county and the annual energy (mwh) generated by hydropower plants in the same county. Water use in hydropower here is associated with all water that passes through the hydropower gates. It can be interpreted as an immediate withdrawal and discharge from surface water.

To calculate hydropower water use intensity rates by county, the ratio was taken between total water withdrawals for instream hydropower per county to total daily power generation per county from the 1995 dataset. This is converted to million gallons per bbtu of energy generated. A number of counties had large outlier water withdrawal intensity values. For example, the county with the highest intensity had an intensity value 6x that of the next highest value. For this reason, the decision was made to cap hydropower withdrawal intensities at 6 million mgd/bbtu (approximately the 90th percentile). This changed values for 396 counties in the dataset.

To account for counties that may have gained hydropower between 1995 and 2015 and would have no intensity estimate from the 1995 dataset, the 1995 counties with zero hydropower generation had their withdrawal intensities set to the state average. For states with no hydropower, their counties were filled in with the US average.

These water intensities are used with hydro electricity generation from the EIA 923 [13] dataset for 2015.

Water Discharge
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Consumption/Evaporation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Thermoelectric Cooling Water Consumption/Evaporation
........................................................
Estimates for water consumption were collected from Harris et al. [14] in the same way that the withdrawal values were collected. These estimates were converted into discharge fractions by taking the ratio of total consumption to total withdrawal per plant. For missing power plants in the Harris et. al [14] dataset, consumption values were filled in using the same methodology as with withdrawal where consumption intensity values from Macknick et al. [15] were applied to generation (mwh) estimates from EIA [13].

Hydropower Water Consumption/Evaporation
........................................................
Given that water use in hydropower is estimated as the instantaneous withdrawal and discharge of water from surface water sources, no consumption or evaporation is estimated.

Discharge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Thermoelectric Cooling Water Discharge
........................................................
Discharge estimates to both the surface and the ocean are provided in Harris et al. [14]. Within the dataset, some of the discharge locations were missing for a number of power plants. An attempt was made to fill these gaps using other information in the dataset such as the name of the water source (e.g., Pacific Ocean).

An assumption was made that if a water source for a power plant came from any of the following sources, it would discharge to the ocean:
* Any source containing the word "ocean"
* Any source containing the word "bay"
* Any source containing the word "harbor" that also had saline water for water type
* Any source containing the word "Channel" that also had saline water for water type
* Any source containing the word "Sound" that also had saline water for water type

All other blank discharge locations were assumed to be discharged to the surface. All water withdrawal estimates from Macknick et al. [15] are assumed to be discharged to the surface.

Hydropower Water Discharge
........................................................
All water withdrawn for hydropower generation is assumed to be discharged to the surface.


Energy (Fuels) Production Sector
**********************************

Energy in Energy Production
-------------------------------------------------------------------------------------------------------------------------------
The following energy production (fuel) types are included in the analysis:
- Natural gas
- Petroleum
- Coal
- Biomass

For all of the fuel production types except coal, data by type is taken from US EIA SEDS state-level data for 2015 [8]. Data is provided in BBTU/yr. Information is provided at the state level and broken up based on various methodologies described in greater detail below.

MSN codes used from the EIA SEDS [8] dataset include:
- "PAPRB": Crude oil production (including lease condensate)
- "EMFDB": Biomass inputs (feedstock) to the production of fuel ethanol
- "NGMPB": Natural gas marketed production

Coal production data is provided in an alternative mine-level dataset [17] that allows us to aggregate production to the county level. This is discussed in greater detail later on this page.

Note that for energy sources that are not direct fuels (e.g., solar, nuclear), any production is directly consumed and values are captured in electricity production or fuel demand by end use sectors.

Various methods are used to break up state-level energy production values into county level values. These are described for each of the four fuel types below.

Coal Production
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Coal production at the county level is provided from two separate datasets. The first dataset, US EIA E-7 [17], includes coal production data (tons), coal mine type (surface or underground), as well as the Mine ID number for 2015. The Mine ID number provided in the US EIA dataset is used to map coal mine data to the secondary dataset (coal mine data provided by the US Department of Labor - Mine Safety and Health Administration [18]). The latter of these datasets includes the county FIPS codes for each Mine ID that is used to aggregate production to the county level. While information is provided for Refuse coal mines in the EIA dataset in addition to surface and underground mines, these mines are not included in this analysis.

Coal production for each mine type is provided in short tons per year. This is converted to bbtu where one short ton is equal to 0.02009 bbtu. Production values by mine type are aggregated to the county level.

Biomass (Ethanol) Production
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

County level ethanol production is estimated using the EIA 819 dataset containing individual ethanol plant capacities as of January 1 2016 [24] and county locational information for each ethanol plant name provided by the State of Nebraska [25]. Open source data on plant production for the year 2015 was not found, leading to the capacity estimates serving as a proxy for production. State-level production inputs from EIA SEDS [8] are distributed to individual counties within a state based on the fraction of total state ethanol production capacity.

The state of Wyoming appears in the EIA SEDS [8] dataset as having ethanol production but does not appear in the ethanol plant data file. Information on which county the ethanol production takes place in, therefore, is filled in with information from [25]. Only one ethanol plant is included for the state of Wyoming as of January 2016 in Torrington County.

County-level Natural Gas Production
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To obtain county-level estimates of natural gas production from state-level estimates for 2015, a 2011 USDA Economic Research Service dataset [26] of county-level natural gas production is used. The data provides production values for onshore production in the lower 48 states. No data for years 2012 onwards was found and the data product has since been discontinued by USDA. The fraction of state production for each county within a given state was multiplied by state level natural gas production values provided from EIA SEDS [8] to get county-level estimates.

The state production dataset from EIA SEDS [8] includes state-level values for states that are not included in the county-level production data from USDA [26]. For these states, production by county are individually assessed from a variety of sources, described below.

For the state of Idaho, all production of natural gas is estimated to come from a single county (Payette County) according to a 2016 data release by the Idaho Department of Lands [27]

Data from the State of Alaska's Oil and Gas Conservation Commission [28] helps to pinpoint which regions of the state are the primary producers of natural gas. The large majority of natural gas production comes from the North Slope area of Alaska (>96%) while the remainder is produced in the Cook Inlet Basin (Kenai Peninsula). These percentages are used to split up total state natural gas production for 2015.

For the state of Maryland, natural gas production was found to occur in two different counties (Garret County and Allegany County) according to a state energy analysis provided by EIA [29]. No information was found on the relative production within each county. As a result, it is assumed that production is split evenly between the two counties. No year is associated with these county estimates, however, it is assumed that the location of recoverable natural gas in the state will not change substantially. Both counties are in the western part of the state and overlie part of the Marcellus Shale. Note that, since 2017 Maryland enacted a permanent ban on hydraulic fracturing for natural gas and oil production.

Very low natural gas production exists for the state of Nevada. The production that did occur in 2015 is estimated to originate from Nye County. This estimate is predominantly formed upon the basis that the largest number of oil and gas well potential appears clustered within that county. Information for this estimate is provided through potential oil and gas well maps from the University of Nevada - Reno [30].

For the state of Oregon, only one county is listed for gas production (Columbia County) associated with the Mist Gas Field. Information for this estimate is provided by the State of Oregon Department of Geology and Mineral Industries [31]. The data on production under this gas field is provided annually with values available for 2015. All state natural gas production for Oregon for 2015 is assigned to this county.

Petroleum Production
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Limited information exists on a county-level for petroleum production that differentiates between conventional and unconventional production. According to the US EIA, 63% of all oil is shale (unconventional) [32]. Until additional information is available, it is assumed that state-level petroleum production is divided out into the two categories by this fraction.

Unconventional Oil (Petroleum)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To obtain county-level estimates of unconventional petroleum production from state-level estimates for 2015, a 2011 USDA Economic Research Service dataset [26] of county-level petroleum production is used. The data provides production values for onshore production in the lower 48 states. No data for years 2012 onwards was found and the data product has since been discontinued by USDA. The fraction of state production for each county within a given state was multiplied by state level petroleum production values provided from EIA SEDS [8] to get county-level estimates.

Two states appear in the EIA SEDS [8] petroleum production datafile that do not appear in the 2011 USDA [26] county level production and must be filled in individually, these are described below.

For the state of Idaho, all production of unconventional petroleum is estimated to come from a single county (Payette County) according to a 2016 data release by the Idaho Department of Lands [27]

Data from the State of Alaska's Oil and Gas Conservation Commission [28] helps to pinpoint which regions of the state are the primary producers of unconventional petroleum. The large majority of unconventional production comes from the North Slope area of Alaska (>97%) while the remainder is produced in the Cook Inlet Basin (Kenai Peninsula). These percentages are used to split up total state unconventional petroleum production for 2015.

Conventional Oil (Petroleum)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Following the assumption that 63% of all petroleum production is unconventional petroleum production, the remainder falls to conventional production. State-level petroleum production values are split into conventional and unconventional petroleum through this fraction. The amount of state-level petroleum production that is conventional is split into individual counties using the same methodology applied to unconventional production using the 2011 USDA county-level petroleum production [26].

Water in Energy Production
-------------------------------------------------------------------------------------------------------------------------------

Water in energy production is calculated for the following energy types:
- Coal (specifically, dust control in mining)
- Biomass (specifically, water used in corn growth for ethanol production and water use in the production of ethanol from corn grain)
- Natural gas (water used in unconventional natural gas wells)
- Petroleum (water used in conventional and unconventional oil wells)

Each of these are described in more detail below.

Water in Coal
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water Withdrawal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To determine the amount of water used in the production of coal from each type of coal mine (surface vs. underground), the assumptions from Greenberg et al. [4] are used. Greenberg et al. [4] estimates that surface mines withdraw 7 gallons of water per ton of coal and underground mines withdraw 29 gallons per ton. To determine water source/type for mining dust control, it is assumed that the source of the water withdrawal for coal mining follows the same distribution of water use for other types of mining in the same county. For example, if 50% of water withdrawals for all mining in a county are estimated to come from fresh surface water, the same percentage is applied to coal mining. Water withdrawals for all mining types is provided in the USGS 2015 water use dataset [1].

Given that water withdrawals for coal mining are implicitly included in the water withdrawals for all mining in the USGS 2015 [1] dataset, the estimated water withdrawals for coal mining are subtracted from the water withdrawals to all mining to avoid double counting. This is completed by multiplying the county-level coal production for both surface and underground mines in bbtu by the estimated water intensity values described above. The outcome is substracted from the water withdrawals to mining provided in Dieter et al. [1] for the year 2015. For counties where the estimated water use for coal mining exceeded the amount of water in all mining presented in the USGS data file (Dieter et al. [1]), the amount of water to non-coal mining was set to zero.

Water use in coal mining is represented as water withdrawals delivered to the mining sector under the coal subsector category.

Water Consumption/Evaporation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Estimates for consumed water from coal mining follow the same consumption fractions as for all mining water consumed. These values are not available in the 2015 dataset and are instead calculated from the 1995 USGS dataset on a county basis (Sulley et al.). For more information on how these values were derived, see the Mining sector page.

Water Discharge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Very few coal mines exist in coastal areas of the united states. Therefore, following in line with assumptions made in Greenberg et al. [4], 100% of water not consumed in the production of coal is
assumed to be discharged to the surface.

Water in Biomass
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Agricultural Irrigation of Corn for Ethanol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Water use in the production of ethanol is included in two forms in this analysis: (1) water use in the agriculture sector that is put towards the irrigation of corn used in the production of ethanol and (2) water used in the industrial sector to process the corn and produce ethanol. These flow values are provided separately and are described in greater detail below.

Water Withdrawal
.................................................
Data on water used in corn growth for ethanol production does not exist explicitly at any level of granularity and must be calculated out from larger state-level totals of irrigation water and corn production. The general methodology for calculating the water use in biomass follows that outlined in Greenberg et al. [4], however, a national average percent of corn grown for ethanol (described below) is used in place of their ethanol fraction estimate.

The assumed percent of all corn grown for ethanol in the US was used from the US DOE Alternative Fuels Data Center [20]. Total corn production for ethanol (5.22 billion bushels) was divided by total corn production (13.6 billion bushels) for 2015 and calculated to be 38.406%. Data on a state or county level for this estimate does not exist in a public database, therefore, this percentage is applied to all states with corn production. A state-level fraction of corn used for ethanol production could be calculated from the amount of ethanol produced in a state and applying an assumption of corn required per unit of ethanol, however, this would lead to data anomalies such as states like California producing an ethanol fraction of nearly 900% of their total corn production. Given that we are unable to determine which states the imported corn for ethanol would be coming from, the decision was made to apply the US total fraction to all states.

Total water used in the production of corn for ethanol is therefore the assumed 38.406% multiplied by the product of the total amount of irrigated acres of corn and the calculated irrigation intensity for that state (total acres applied to all crops / total acres irrigated, all crops) provided from USDA Census of Agriculture Irrigation and Water Management Survey (Perdue et al [22]), Table 35 and Table 4, respectively. The irrigation intensity for corn is assumed to be equivalent to the irrigation intensity for all crops given that state-level corn irrigation intensity data is not available.

To split the total water applied to crop irrigation for corn growth for ethanol between fresh surface water and fresh groundwater, USDA FRIS Census of Agriculture [21] data on surface water (surface water + off farm water) as a percent of total water (including groundwater) in corn production is used from Table 37 of [21]. Off-farm sources are assumed to be surface water.

Note: the state of New York (NY) does not have data on ground vs. surface water sources for corn irrigation. It is assumed, therefore, for this state, that the ratio between surface water and groundwater in corn growth for ethanol matches the average ratio from all other states.

To split state-level water use values into county-level values, county-level corn production data is used from USDA NASS [22]. It is assumed that the county level corn production as a fraction of state level corn production is an adequate way to split up state-level water withdrawal quantities. The county-level corn production fractions are multiplied by the state level water withdrawal values to obtain county-level water withdrawal values.

Water withdrawals for corn growth for ethanol are represented as a sub-subsector in the Agriculture-crop irrigation sector in the dataset. To avoid double counting in the data, the estimated water used in corn growth for ethanol is substracted from the water use in all crop irrigation.

Water Consumption/Evaporation
.................................................
Water consumption fraction estimates for corn growth for ethanol used in biomass are expected to follow the same consumption fraction estimates for all crop irrigation. This information is provided directly in in Dieter et al. [1].

Water Discharge
.................................................
Water discharge estimates for corn growth for ethanol used in biomass are expected to follow the same discharge estimates for all crop irrigation. All water discharged from crop irrigation is expected to be to the surface.

Industrial Ethanol Production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Water Withdrawal
.................................................

Water is used in the industrial sector to produce ethanol in the fermentation process. The current estimate for water intensity (gallons of water per gallon of ethanol) is approximately 3 gallons. This estimate is provided from Argonne National Laboratory [23]. All water used in the fermentation of ethanol is assumed to come from fresh surface water.

Water withdrawals in the industrial sector for the production of ethanol is separated out as an individual subsector under the Industrial sector. To avoid double counting of water flows to the industrial sector, the values calculated for ethanol production are subtracted out from total water use in industrial applications provided by Dieter et al. [1].

Water Consumption/Evaporation
.................................................
Water consumption fraction estimates for the industrial production in ethanol are expected to follow the same consumption fraction estimates for all industrial applications in a given county. For more information on these estimates, see the Industrial sector section.

Water Discharge
.................................................
Water discharged from the industrial production of ethanol is assumed to be equal to all water that is not consumed. All water not consumed by this sector is assumed to be discharged to the surface, following the same discharge fraction assumptions for other industrial applications.


Water in Natural Gas
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Water Withdrawal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No county level water use or water intensity estimates exist for natural gas for the year 2015. Water use estimates for natural gas extraction for this analysis are used from Greenberg et al. [4].  Only state-level values for unconventional petroleum and natural gas extraction are available in their dataset. State-level values are split into county-level values following the same methodology used to split up the state-level natural gas production values described previously.

The intensity of water use in unconventional natural gas drilling was determined by taking the total water to unconventional natural gas production in each county and dividing it by the total natural gas production per day in the same county. The average intensity value (million gallons per bbtu) was applied to counties that recorded unconventional natural gas production in 2015 but no water estimates were available.

It is assumed that 80% of water withdrawals by natural gas production are from fresh surface water sources and the remainder is from fresh groundwater sources following the methodology in Greenberg et al. [4]. No saline water is assumed to be used in the production of natural gas and no water flows to natural gas are assumed to come from wastewater reuse.

Produced Water
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When water is injected into the ground for natural gas production, some additional water is extracted or "produced". No exact values exist regarding produced water for oil and natural gas individually. Veil [32] provided an analysis for 2017 on produced water by state and Greenberg et al. [4] adapted these to provide values for states with missing data. The information from both of these sources is used here. Produced water values are converted to million gallons of water per bbtu and applied to unconventional natural gas production by county. For states without a value, the US average is supplied.

The water-oil-ratio (WOR) (barrels of water/barrel of oil) and water-gas-ratio (WGR) [barrels of water/million cubic feet (mmcf) of natural gas] from Greenberg et al. [4] were applied to 2015 data on oil and gas production to estimate total produced water. For the state of Idaho, which did not have a WOR value in the dataset, the WOR and WGR was assumed to be the average of both Montana and Wyoming. This produced water was split out into injection, surface discharge, and consumption/evaporation based on percentage breakdowns by state provided in [32]. Note that offsite disposal of water is assumed to be injected

Water Consumption/Evaporation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same resource (Veil [32]) that provided produced water intensities for natural gas also supplied discharge percentages to surface, injection (ground), and consumption for each state. These estimates do not differentiate between natural gas and petroleum drilling. The assumption is made that these values are equivalent and are applied appropriately. For states without estimates, the national average is applied.

Water Discharge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See the Water Consumption/Evaporation section above.

Water in Petroleum
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water Withdrawal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
No county level water use or water intensity estimates exist for unconventional petroleum for the year 2015. Water use estimates for unconventional petroleum extraction for this analysis are used from Greenberg et al. [4].  Only state-level values for unconventional petroleum and natural gas extraction are available in their dataset. State-level values are split into county-level values following the same methodology used to split up the state-level unconventional petroleum production values described previously.

For conventional petroleum water intensity, gallon of water per gallon of oil (WOR) estimates were provided by Greenberg et al. [4]. For states that were not included in the dataset but had 2015 conventional petroleum production, the average US WOR value was applied.

It is assumed that 80% of water withdrawals for petroleum production are from fresh surface water sources and the remainder is from fresh groundwater sources following Greenberg et al. [4]. No saline water is assumed to be used in the production of petroleum. 0% of water flows to natural gas are assumed to come from wastewater reuse.

#### Produced Water
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The methodology for petroleum produced water follows that of natural gas. See the Natural Gas Produced water section above for more information.

#### Water Consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Consumption - Consumption estimates for petroleum follow the same as those as natural gas and are applied to all water (withdrawals + produced) in petroleum (conventional and unconventional). These values are estimated from Veil [32].
#### Water Discharge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Discharge estimates for petroleum follow the same as those as natural gas and are applied to all water (withdrawals + produced) in petroleum (conventional and unconventional). Note that offsite disposal of water is assumed to be injected.



Industrial Sector
**********************************
## Water in the Industrial Sector
-------------------------------------------------------------------------------------------------------------------------------
Water Demand
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water Withdrawals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Water withdrawal (self-supply) values are directly provided in the Dieter et al. [1] at a county level and are used directly. This includes fresh and saline water from both surface and ground sources.
Public Water Deliveries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Public water deliveries (public water demand) to the industrial sector are not directly provided in Dieter et al. [1] for 2015 for each county. The most recent year these values are provided is for 1995 from the USGS 1995 water use report (Solley et al. [7]). In order to estimate public water deliveries to the industrial sector, the ratio of deliveries to the industrial sector compared to deliveries to the residential and thermoelectric cooling in aggregated in 1995 is applied to 2015 residential and thermoelectric cooling delivery values. That is, if the 1995 ratio of industrial water deliveries from public water supply was half that of public water deliveries to the residential sector and thermoelectric cooling in aggregate in an individual county, then the 2015 public water deliveries to the industrial sector would be equal to half the public water deliveries to the residential sector and thermoelectric cooling in aggregate for 2015.

For 1995 counties that do not have public water deliveries to the industrial sector, the average ratio for the given state is applied instead. Note that this may overestimate public water deliveries to industrial sector in some counties. No counties that have at least some public deliveries to either the residential sector or thermoelectric cooling will have 0 public water deliveries to the industrial sector.
Water Discharges/Consumption
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Consumption/Evaporation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Consumption of water by the industrial sector is not provided in the Dieter et al. [1] water dataset. The most recent year with data available is the 1995 USGS water use report (Solley et al. [7]). Instead of directly using the consumptive use (mgd) from the industrial sector from the 1995 factor, consumption fractions (%) for fresh water and saline water were individually calculated based on the ratio of water consumed by the industrial sector and total water flows to the industrial sector in 1995. In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted.

Discharge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Discharge to Surface
.................................................
It is assumed that all fresh water and all saline groundwater that is not from public water sources and is not consumed, is discharged to the surface.

Discharge to ocean
.................................................
It is assumed that all saline surface water withdrawn by the industrial sector and not consumed, is discharged to the ocean.
Discharge to wastewater supply
.................................................
It is assumed that all public water deliveries to the industrial sector are discharged to wastewater supply.

Energy in the Industrial Sector
-------------------------------------------------------------------------------------------------------------------------------
Energy Demand
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Fuel Demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Energy demand by the industrial sector is supplied on a state-basis from U.S. EIA for 2015. EIA provides information on energy supply (fuels) that go to sectors other than electricity generation in their SEDS dataset [8]. Each fuel is given in BTUs per year and is categorized by a specific MSN code. For the industrial sector, this includes the following MSN codes.

* PAICB - All petroleum products consumed by the industrial sector
* WWICB - Wood and waste energy consumed in the industrial sector
* NGICB - Natural gas consumed by the industrial sector
* CLICB - Coal consumed by the industrial sector

Values are adjusted to BBTU per day.

To split up state total values to individual counties within a state, total values are split out based on county population. For example, if County 1 in State A makes up 10% of the total state population, then 10% of the state total natural gas deliveries to the industrial sector are in that county. County population data for 2015 is directly provided in Dieter et al. [1]

Electricity Demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Electricity demand by the residential sector is also supplied by US EIA for 2015. Electricity delivery values are used from the Electric Power Annual dataset for residential, commercial, industrial, and transportation sectors [9]. Values are originally provided in annual MWh and are converted to BBTU per day. State level values are broken up into county-level approximations based on population following the same methodology as the fuel deliveries.

Energy Discharge
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Energy Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The industrial sector is assumed to have an efficiency of 49%, in line with estimates provided in Greenberg et al. [4]. Therefore, 49% of all energy used in the industrial sector is assumed to go to energy services.
Rejected Energy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Given the assumed efficiency of 49%, 51% of energy in the industrial sector is assumed to go to rejected energy.


Mining Sector
**********************************

Public Water Sector
**********************************

Residential Sector
**********************************

Transportation Sector
**********************************

Wastewater Treatment Sector
**********************************


References
####################

The following list includes references for data sources and calculation methodology development for the 2015 US sample data.
Reference numbers correspond with those included in the Methodology subsections.

1.	Dieter, C. A., Maupin, M. A., Caldwell, R. R., Harris, M. A., Ivahnenko, T. I., Lovelace, J. K., Barber, N. L., & Linsey, K. S. (2018). Estimated use of water in the United States in 2015.
2.	Tidwell, V. C., Moreland, B., & Zemlick, K. (2014). Geographic Footprint of Electricity Use for Water Services in the Western U.S. Environmental Science & Technology, 48(15), 8897-8904. https://doi.org/10.1021/es5016845
3.	Texas Water Development Board. (2022). Water Use Survey Historical Municipal Use by Region. Texas Water Development Board. Retrieved February 10, 2022 from https://www3.twdb.texas.gov/apps/reports/WU/HistoricalMunicipal
4.	Greenberg, H. R., Simon, A. J., Singer, S. L., & Shuster, E. P. (2017). Development of Energy-Water Nexus State-level Hybrid Sankey Diagrams for 2010 (LLNL-TR-669059). https://flowcharts.llnl.gov/content/assets/docs/2010_United-States_EnergyWater.pdf
5.	Vilsack, T. (2014). 2013 Farm and Ranch Irrigation Survey Part 1 (AC-12-SS1). (2012 Census of Agriculture, Issue. https://www.nass.usda.gov/Publications/AgCensus/2012/Online_Resources/Farm_and_Ranch_Irrigation_Survey/fris13.pdf
6.	Lawrence Berkeley National Laboratory (LBNL). (2021). Well-pump energy calculation method. LBNL. Retrieved August 12 from http://hes-documentation.lbl.gov/calculation-methodology/calculation-of-energy-consumption/major-appliances/miscellaneous-equipment-energy-consumption/well-pump-energy-calculation-method
7.	Solley, W. B., Pierce, R. R., & Perlman, H. A. (1998). Estimated use of water in the United States in 1995 Report. (Circular, Issue. U. S. G. S. U.S. Dept. of the Interior & S. Branch of Information. http://pubs.er.usgs.gov/publication/cir1200
8.	U.S. EIA (2016). State Energy Data System (SEDS): 1960-2019 (complete). U.S EIA. Retrieved July 17 from https://www.eia.gov/state/seds/seds-data-complete.php?sid=US
9.	U.S. EIA. (2016). Electric Power Annual 2015. U.S. EIA. Retrieved Feb 17, 2022 from https://www.eia.gov/electricity/annual/xls/epa_02_02.xlsx
10.	U.S. EPA. (2016). Clean Watersheds Needs Survey 2012: Report to Congress (EPA-830-R-15005). https://www.epa.gov/sites/default/files/2015-12/documents/cwns_2012_report_to_congress-508-opt.pdf
11.	U.S. EPA. (2016). Clean Watersheds Needs Survey – 2012 Data Dictionary. https://19january2017snapshot.epa.gov/sites/production/files/2016-01/documents/cwns-2012-data_dictionary2.pdf
12.	Pabi, S., Amarnath, A., Goldstein, R., & Reekie, L. (2013). Electricity Use and Management in the Municipal Water Supply and Wastewater Industries (3002001433). https://www.epri.com/research/products/000000003002001433
13. U.S. Energy Information Administration (EIA). (2016). Form EIA-923 detailed data with previous form data (EIA-906/920). U.S. EIA. Retrieved January 15 from https://www.eia.gov/electricity/data/eia923/
14. Harris, M.A., and Diehl, T.H., 2019, Withdrawal and consumption of water by thermoelectric power plants in the United States, 2015: U.S. Geological Survey Scientific Investigations Report 2019–5103, p., https://doi.org/10.3133/sir20195103.
15. Macknick et al. (2012) Environ. Res. Lett.7 045802. https://iopscience.iop.org/article/10.1088/1748-9326/7/4/045802/meta
16. https://www.usgs.gov/u.s.-board-on-geographic-names/download-gnis-data
17. U.S. EIA (2016). Annual Coal Report 2015. https://www.eia.gov/coal/annual/
18. U.S. Department of Labor- Mine Safety and Health Administration. (2021). Mine Data Retrieval System. Mine Safety and Health Administration. Retrieved September 13 from https://www.msha.gov/mine-data-retrieval-system
19. Plotly. 2022. GeooJSON-Counties-FIPS. https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json
20. U.S. DOE. (2021). U.S. Corn Production and Portion Used for Fuel Ethanol. U.S., DOE. Retrieved September 10 from https://afdc.energy.gov/data/10339
21. Perdue, S. (2019). 2018 Irrigation and Water Management Survey (Special Studies, Issue. https://www.nass.usda.gov/Publications/AgCensus/2017/Online_Resources/Farm_and_Ranch_Irrigation_Survey/fris.pdf
22. USDA. (2015). National Agricultural Statistics Service. https://quickstats.nass.usda.gov/
23. Argonne National Laboratory. 2018. Consumptive Water Use in the Production of Ethanol and Petroleum Gasoline — 2018 Update. Energy Systems Division. ANL/ESD/09-1 Rev. 2. https://publications.anl.gov/anlpubs/2019/01/148043.pdf
24. US. EIA. 2016. U.S. Fuel Ethanol Plant Production Capacity Archives. https://www.eia.gov/petroleum/ethanolcapacity/archive/2016/index.php
25. State of Nebraska. 2016. Ethanol Facilities Capacities by State and Plant. https://neo.ne.gov/programs/stats/122/2015/122_201512.htm
26. USDA. 2020. County-level Oil and Gas Production in the U.S. https://www.ers.usda.gov/data-products/county-level-oil-and-gas-production-in-the-us.aspx
27. State of Idaho. 2016. State of Idaho releases oil and gas production data. https://ogcc.idaho.gov/wp-content/uploads/sites/3/2017/06/2016-10-6-state-of-idaho-releases-oil-gas-production-data.pdf
28. State of Alaska. Undated. Alaska Oil and Gas Conservation Commission. Department of Commerce, Community, and Economic Development. Retrieved December 3, 2021 from https://www.commerce.alaska.gov/web/aogcc/Data.aspx
29. U.S. EIA. 2021. Maryland: State Profile and Energy Estimates. https://www.eia.gov/state/analysis.php?sid=MD#34
30. University of Nevada - Reno. 2011. Oil and Gas Wells Information. Retrieved November 18, 2021 from https://gisweb.unr.edu/OilGas/
31. State of Oregon. 2021. Oil & Gas Permits and Production Information. Department of Geology and Mineral Industries. Retrieved November 18 from https://www.oregongeology.org/mlrr/oilgas-report.htm
32. Veil, J. (2020). U.S. Produced Water Volumes and Management Practices in 2017. http://www.veilenvironmental.com/publications/pw/pw_report_2017_final.pdf
