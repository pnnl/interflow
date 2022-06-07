**************************
Agriculture Sector (AGR)
**************************
The agriculture sector consists of crop irrigation, golf irrigation, livestock, and aquaculture.

Water in Agriculture
################################################

Water Demand
**********************************

Water Supply Withdrawals
-----------------------------
Water withdrawals to the various agriculture sectors are provided by US Geological Survey (USGS) (Dieter et al. [1]) and are provided in million gallons per day (mgd) for each county in 2015. This includes fresh and saline water from both surface and ground sources.
For crop irrigation and golf irrigation, a subset of states did not provide water withdrawal values for these sectors but did provide total irrigation withdrawals (fresh surface and fresh groundwater). For these states, the water withdrawals to total irrigation were used as the values for water withdrawals to crop irrigation. In these states, no water withdrawals were estimated to golf irrigation.
USGS 2015 (Dieter et al. [1]) defines irrigation water use as all “water that is applied by an irrigation system to sustain plant growth in agricultural and horticultural practices” and “includes self-supplied withdrawals and deliveries from irrigation companies or districts, cooperatives, or governmental entities.” This is interpreted to mean that the water demand provided in the USGS data includes all water withdrawn from local surface and groundwater as well as all water delivered via interbasin transfers, described below.

Water Supply Imports (Interbasin transfers)
---------------------------------------------------------
Interbasin transfer flows and energy intensities in each county are provided through data from two sources. For western states, county-level water flows were available from Tidwell et al. [2]. For the state of Texas, county-level interbasin transfers between specified counties were collected from the Texas Water Development Board [3]. No data is currently available for interbasin transfers in eastern US counties. For these counties, the value is assumed to be zero.

Interbasin transfers are used for both public water supply as well as for irrigation purposes. To determine how much of the total interbasin transfer flows in each county goes to crop irrigation versus public water supply, the methodology from Greenberg et al. [4] is adapted which uses the ratio of water flows to crop irrigation vs. public water supply to split the values. The ratio is determined by taking the ratio of all water withdrawals to crop irrigation (Fresh surface water and fresh groundwater) over the sum of all water withdrawals to crop irrigation and water withdrawals by the public water supply from Dieter et al. [1]. This determines the percent of total flows to both sectors that goes to crop irrigation. This fraction is multiplied by the total interbasin transfer flow to determine how much of the interbasin transfer flow goes to crop irrigation. Any interbasin transfer flow that does not go to crop irrigation is assumed to go to the public water supply. It should be noted that interbasin transfers are only assumed to go to crop irrigation and are not used for other agricultural applications such as golf irrigation or livestock.

USGS 2015 [1] defines irrigation water use as all “water that is applied by an irrigation system to sustain plant growth in agricultural and horticultural practices” and “includes self-supplied withdrawals and deliveries from irrigation companies or districts, cooperatives, or governmental entities.” This is interpreted to mean that the water demand provided in the USGS data includes all water withdrawn from local surface and groundwater as well as all water delivered via interbasin transfers. For this reason, the interbasin transfers for agriculture and public water supply are considered only for the purpose of determining the energy demand by these sectors and should not be included in aggregate with the other water withdrawals by these sectors.

**Texas interbasin transfer Methodology**
""""""""""""""""""""""""""""""""""""""""""""""""""
To calculate the total interbasin transfer flows in each Texas county, information from the Texas Water Development Board historical municipal water flow data was used. The data tracks self-supply and purchased water supplies for counties in Texas and tracks their source and used county. To track interbasin transfer flows, only flows that occured between different counties in the year 2015 were included. A small number of data rows had missing values for the source county, these data points were removed from the dataset.

The difference in elevation between counties is used in the formula to calculate required pumping power to transfer water. Elevation data for each of the counties was taken from USGS's GNIS dataset [16] for the state of Texas. The dataset tracks elevation for a variety of locations within counties. The average elevation for all items included in the dataset for each county was assumed as the elevation for that county. The difference in elevation between the source and target counties was calculated. Only transfers that were delivered to a higher elevation were included in the dataset on the assumption that water deliveries to lower elevations would be predominantly gravity-based. Note that the USGS elevation dataset and associated county FIPS codes have been added into the same datafile as the water transfer data from the Texas Water Development Board and these were not included in the original water data file.

Water flows were provided on a gallons/year basis. This was converted to million gallons per day.

**Western States interbasin transfer Methodology**
""""""""""""""""""""""""""""""""""""""""""""""""""""
Interbasin transfer flows were available for various western states in Tidwell et al. [2]. Most rows in the dataset provided water flow values on a cubic feet per second basis, which were converted to mgd (1 cfs = 0.646317 mgd). For rows that did not provide cfs, acre-ft per year were provided and converted to mgd using the same methodology as the Texas calculation described above.

Water Supply Imports (Reclaimed wastewater)
---------------------------------------------------------
Reclaimed wastewater deliveries to crop irrigation are directly provided in Dieter et al. [1] at the county level. For states where crop irrigation water values are not provided but total irrigation values are supplied, crop irrigation water values are assumed to be equal to total irrigation water flows. Following the same methodology, reclaimed wastewater flows to total irrigation are used as the values for reclaimed wastewater deliveries to crop irrigation.

Public Water Deliveries
---------------------------------------------------------
No public water deliveries to agriculture are provided and none are assumed.

Water Discharges/Consumption
**********************************

Consumption/Evaporation
---------------------------------------------------------
Crop irrigation and golf irrigation consumptive use values are directly available in Dieter et al. [1]. Consumption fractions for fresh surface water and fresh groundwater were directly calculated from these values. In some counties, the amount of water consumed in irrigation was greater than the amount withdrawn. For these counties, the consumption fraction is set to 1.

Consumption fractions of water by aquaculture and livestock are not provided in Dieter et al. [1]. The most recent year with data available is the 1995 USGS water use report (Solley et al. [7]). Instead of directly using the consumptive use (mgd) provided, consumption fractions (%) for fresh water and saline water were individually calculated based on the ratio of water consumed by each agricultural sector and total water flows to that agricultural sector in 1995.

In order to fill consumption fraction values for counties that did not have consumed water values in 1995 but may have consumed water in 2015, the state average consumption fraction was substituted. For states that were missing values for all of their counties the US average was substituted. For counties that had consumption fractions greater than one (presumably due to inconsistent data reporting), the consumption fraction was set to 1.

Irrigation Conveyance Losses
---------------------------------------------------------
Irrigation conveyance loss values are not available in Dieter et al. [1] but are available in Solley et al. [7] for 1995. These mgd conveyance loss values are converted to conveyance loss fractions by taking the ratio of water lost to conveyance in 1995 to the total water delivered to irrigation in 1995. Specific values for crop irrigation and golf irrigation are not available in the 1995 dataset. Therefore, it is assumed that the conveyance loss fraction for both crop irrigation and golf irrigation are equal to the conveyance loss fraction per county for total irrigation for 1995.

For counties within a state that have conveyance loss fractions of zero, the state average (inclusive of zero values) is supplied. For states with no conveyance loss values for any county, the US average conveyance loss fraction is applied. Note that, through this method, there will be no counties in the US that have 0 conveyance losses if they have water flows to crop or golf irrigation.

The conveyance loss fractions calculated per county include values assumed to be outliers (some greater than 150% of their flows lost to conveyance losses) and are assumed to be data collection errors. In order to account for these values, a conveyance loss fraction cap was implemented where the maximum amount of water lost to conveyance losses in irrigation is 90% of water flows. This value is still considerably high, however, without more detailed and recent information, it is difficult to determine accuracy.

No conveyance losses are currently assumed for non-irrigation agriculture sectors. No adjustments have been made to convert 1995 values to 2015 values.

Discharge
---------------------------------------------------------

*Discharge to Surface*
""""""""""""""""""""""""""""""""
It is assumed that all fresh water delivered to agriculture sectors to that is not consumed or lost during conveyance, is discharged to the surface.

*Discharge to Ocean*
""""""""""""""""""""""""""""""""
It is assumed that all saline water delivered to agriculture sectors that is not consumed or lost during conveyance, is discharged to the ocean.

Energy in Agriculture
################################################

Energy Demand
**********************************

Water Withdrawal Pumping Energy
---------------------------------------------------------
USDA FRIS [5] provides information on the breakdown of power type per pump in irrigation applications for each state. This includes the percentage breakdown between electricity, propane, diesel, and gas. For simplification purposes, propane and diesel have been binned into the same fuel category. These percentages are used for all counties in each given state to determine what fraction of the total energy in agriculture comes from each fuel source. It is assumed that the same breakdown applies to all agriculture applications, not just irrigation.

USDA's Farm and Ranch Irrigation Survey (FRIS) [5] provides state-by-state data on irrigation groundwater depth and average irrigation pressurization levels for irrigation within a state, enabling the calculation of pump electricity consumption for both groundwater and surface water pumping. The 2013 survey is the closest year available to 2015 values. It is assumed that values do not vary significantly between the two years.

The methodology for calculating groundwater and surface water pumping energy is described in Pabi et al [12]. The function presents a way to calculate the required kwh per day to pump water based on an assumed flow rate (gallons per minute), pumping head (total differential height inclusive of pressurization), and the assumed pump efficiency. This formula is reproduced below. Note that 3960 is the water horsepower, 0.746 is the conversion factor between horsepower and kilowatts, and 24 is simply the number of hours in a day.

Electricity (kWh/day) = ((Flow (gpm) x pumping head (ft)) / (3960 x pumping efficiency)) x 0.746 x 24

The above equation was modified to produce a bbtu per million gallon pumping intensity rate by setting the flow value to the gallons per minute equivalent to 1 million gallons per day (694.4 gpm) and converting kwh to bbtu.

While some research uses well depth to water to calculate total differential height, the total well depth is used here instead as a way to offset some of the losses due to friction that would occur in the piping, as described in Lawrence Berkeley National Laboratory (LBNL) Home Energy Saver & Score: Engineering Documentation [6]. Pump efficiency is assumed to be the average (46.5%) of the range (34-59%) listed in Tidwell et al. [2]. State-level intensity rates are calculated here and applied to the county level water in the agriculture sectors.

In order to calculate surface water pumping energy, the same methodology is used as calculating groundwater but the well-depth is set to 0 ft.


Interbasin-transfer Pumping Energy
---------------------------------------------------------
The energy intensity required for interbasin transfers was calculated on a per-county basis from values provided in Tidwell et al. [2] and the Texas Water Development Board [3].

**Texas Interbasin Transfers**
""""""""""""""""""""""""""""""""

To calculate the power required for interbasin transfers in Texas, the equation for power required to perform a static lift presented in Tidwell et al. [2] was used. The power required is equal to the product of the mass flow rate of water (cubic meters/hr), the liquid density of water (997 kg/m^3), the acceleration due to gravity (9.81 m/s^2), and the differential height (meters). This product is then divided by the assumed pumping efficiency (46% here). This gives the total watts per hour required to pump the water from one county to the other which is then converted to bbtu/day.

Each value in the Texas interbasin transfer data is associated with two counties (source and target county). Given a lack of more detailed data, it is assumed that half of the water flow and half of the subsequent energy required is split evenly between the two counties.

The energy intensity of interbasin transfers in Texas is the ratio of energy required per day to water moved per day.

**Western States Interbasin Transfers Energy**
"""""""""""""""""""""""""""""""""""""""""""""""""
Energy for interbasin transfers in the west was provided directly in Tidwell et al. [2] for the states included. Low (mwh/yr) and high (mwh/yr) values were provided . The average of these values was taken for this analysis and converted to bbtu/day.

The energy intensity for interbasin transfers in western counties is the ratio of energy demand per day to water moved per day.

Energy Discharge
**********************************

**Energy Services**
---------------------------------------------------------
Each subsector in the agriculture sector is assumed to have 65% efficiency following estimates provided in Greenberg et al. [4]. Therefore, 65% of all energy in each agriculture sector is assumed to go to energy services.

**Rejected Energy**
---------------------------------------------------------
All energy that does not go to energy services is assumed to go to rejected energy, therefore, it is assumed that each agriculture sub-sector sends 35% of its energy to rejected energy.
