**************************
Public Water Sector (PWS)
**************************

Water in Public Water Supply
################################################

Water Demand
**********************************

Water Withdrawals/Deliveries
----------------------------------------------------------
Water withdrawals to public water supply are provided by US Geological Survey (USGS) (Dieter et al. [1]) and are provided in million gallons per day (mgd) for each county. Public supply is defined as "water withdrawn by public and private water suppliers that provide water to at least 25 people or have a minimum of 15 connections." Public supply withdrawals include fresh/saline and surface/ groundwater.

Water Supply Imports (Interbasin transfers)
----------------------------------------------------------
Interbasin transfer flows and energy intensities in each county are provided through data from two sources. For western states, county-level water flows were available from Tidwell et al. [2]. For the state of Texas, county-level interbasin transfers between specified counties were collected from the Texas Water Development Board [3]. No data is currently available for interbasin transfers in eastern US counties. For these counties, the value is assumed to be zero.

Interbasin transfers are used for both public water supply as well as for irrigation purposes. To determine how much of the total interbasin transfer flows in each county goes to crop irrigation versus public water supply, the methodology from Greenberg et al. [4] is adapted which uses the ratio of water flows to crop irrigation vs. public water supply to split the values. The ratio is determined by taking the ratio of all water withdrawals to crop irrigation (Fresh surface water and fresh groundwater) over the sum of all water withdrawals to crop irrigation and water withdrawals by the public water supply from Dieter et al. [1]. This determines the percent of total flows to both sectors that goes to crop irrigation. This fraction is multiplied by the total interbasin transfer flow to determine how much of the interbasin transfer flow goes to crop irrigation. Any interbasin transfer flow that does not go to crop irrigation is assumed to go to the public water supply. It should be noted that interbasin transfers are only assumed to go to crop irrigation and are not used for other agricultural applications such as golf irrigation or livestock.

USGS 2015 [1] defines irrigation water use as all “water that is applied by an irrigation system to sustain plant growth in agricultural and horticultural practices” and “includes self-supplied withdrawals and deliveries from irrigation companies or districts, cooperatives, or governmental entities.” This is interpreted to mean that the water demand provided in the USGS data includes all water withdrawn from local surface and groundwater as well as all water delivered via interbasin transfers. For this reason, the interbasin transfers for agriculture and public water supply are considered only for the purpose of determining the energy demand by these sectors and should not be included in aggregate with the other water withdrawals by these sectors.

**Texas Interbasin Transfers**
""""""""""""""""""""""""""""""""""""""""""""""""""

To calculate the total interbasin transfer flows in each Texas county, information from the Texas Water Development Board historical municipal water flow data was used. The data tracks self-supply and purchased water supplies for counties in Texas and tracks their source and used county. To track interbasin transfer flows, only flows that occurred between different counties in the year 2015 were included. That is to say, counties that delivered to themselves were not included. A small number of data rows had missing values for the source county, these data points were removed from the dataset.

The difference in elevation between counties is used in the formula to calculate required pumping power to transfer water. Elevation data for each of the counties was taken from USGS's GNIS dataset [16] for the state of Texas. The dataset tracks elevation for a variety of locations within counties. The average elevation for all items included in the dataset for each county was assumed as the elevation for that county. The difference in elevation between the source and target counties was calculated. Only transfers that were delivered to a higher elevation were included in the dataset on the assumption that water deliveries to lower elevations would be predominantly gravity-based. Note that the USGS elevation dataset and associated county FIPS codes have been added into the same datafile as the water transfer data from the Texas Water Development Board and these were not included in the original water data file.

Water flows were provided on a gallons/year basis. This was converted to million gallons per day.

**Western States Interbasin Water Transfers**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Interbasin transfer flows were available for various western states. Most rows in the dataset provided water flow values on a cubic feet per second basis, which were converted to mgd (1 cfs = 0.646317 mgd). For rows that did not provide cfs, acre-ft per year were provided and converted to mgd using the same methodology as the Texas calculation described above.

Water Discharges/Consumption
**********************************

Public water supply is not assumed to have any consumption values. Evaporation estimates are not included at this time. It is assumed that all water in public water supply is either send to public water demand (and onward to residential, commercial, and industrial end users) or it is sent to exports (i.e., exported to another county). The total amount of water that is sent to public water demand is assumed to be equal to the sum of public water demand to residential, commercial, and industrial sectors (see the respective Residential, Commercial, and Industrial methodology sections for more information on these flows). Taking the total water in public water supply (including both withdrawals and interbasin transfer deliveries) and substracting the total public water demand allows us to determine the total public water export in each county. In counties where the total public water supply is less than or equal to the total public water demand, the amount of exports is equal to zero. Following this methodology, if the total public water demand is greater than the total public water supply in a county, the difference established the total public water demand that is imported from another county.


Energy in Public Water Supply
################################################

Energy Demand
**********************************
Energy use in public water supply is determined by coefficients for energy intensity in surface water withdrawal, groundwater withdrawal intensity, surface water treatment intensity, groundwater treatment intensity, distribution intensity to end-users, and interbasin transfer pumping intensity. It is assumed that all energy used in the public water supply sector is supplied by electricity.

Pumping Energy Demand
-----------------------------

USDA's Farm and Ranch Irrigation Survey (FRIS) [5] provides state-by-state data on irrigation groundwater depth and average irrigation pressurization levels for irrigation within a state, enabling the calculation of pump electricity consumption for both groundwater and surface water pumping. The 2013 survey is the closest year available to 2015 values. It is assumed that values do not vary significantly between the two years.

The methodology for calculating groundwater and surface water pumping energy is described in Pabi et al [12]. The function presents a way to calculate the required kwh per day to pump water based on an assumed flow rate (gallons per minute), pumping head (total differential height inclusive of pressurization), and the assumed pump efficiency. This formula is reproduced below. Note that 3960 is the water horsepower, 0.746 is the conversion factor between horsepower and kilowatts, and 24 is simply the number of hours in a day.

Electricity (kWh/day) = ((Flow (gpm) x pumping head (ft)) / (3960 x pumping efficiency)) x 0.746 x 24

The above equation was modified to produce a bbtu per million gallon pumping intensity rate by setting the flow value to the gallons per minute equivalent to 1 million gallons per day (694.4 gpm) and converting kwh to bbtu.

While some research uses well depth to water to calculate total differential height, the total well depth is used here instead as a way to offset some of the losses due to friction that would occur in the piping, as described in Lawrence Berkeley National Laboratory (LBNL) Home Energy Saver & Score: Engineering Documentation [6]. Pump efficiency is assumed to be the average (46.5%) of the range (34-59%) listed in Tidwell et al. [2]. State-level intensity rates are calculated here and applied to the county level water in the agriculture sectors.

In order to calculate surface water pumping energy, the same methodology is used as calculating groundwater but the well-depth is set to 0 ft.

Treatment Energy Demand
-----------------------------

The energy intensity for public water supply treatment for fresh water is provided in Greenberg et al. [4]. Estimates for desalination (saline water treatment) are provided by Tidwell et al. [2].

Fresh surface water treatment = 405 kWh/mg
Fresh groundwater treatment = 205 kWh/mg
saline surface water treatment = 12,000 kWh/mg
saline groundwater treatment = 12,000 kWh/mg

All values are converted to bbtu/mgd.

Distribution Energy Demand
-----------------------------

The energy intensity for public water supply distribution is provided in Greenberg et al. [4] as 1040 kWh/mg. This value is converted to bbtu/mgd.

Interbasin-transfers Pumping Energy Demand
----------------------------------------------------------

The energy intensity required for interbasin transfers was calculated on a per-county basis from values provided in Tidwell et al. [2] and the Texas Water Development Board [3].

**Texas Interbasin Water Transfer Energy Demand**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To calculate the power required for interbasin transfers in Texas, the equation for power required to perform a static lift presented in Tidwell et al. [2] was used. The power required is equal to the product of the mass flow rate of water (cubic meters/hr), the liquid density of water (997 kg/m^3), the acceleration due to gravity (9.81 m/s^2), and the differential height (meters). This product is then divided by the assumed pumping efficiency (46% here). This gives the total watts per hour required to pump the water from one county to the other which is then converted to bbtu/day.

Each value in the Texas interbasin transfer data is associated with two counties (source and target county). Given a lack of more detailed data, it is assumed that half of the water flow and half of the subsequent energy required is split evenly between the two counties.

The energy intensity of interbasin transfers in Texas is the ratio of energy required per day to water moved per day.

**Western States Interbasin Water Transfer Energy Demand**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Energy for interbasin transfers was provided directly in Tidwell et al. [2] for the states included. Low (mwh/yr) and high (mwh/yr) values were provided . The average of these values was taken for this analysis and converted to bbtu/day.

The energy intensity for interbasin transfers in western counties is the ratio of energy per day to water moved per day.

Energy Discharges
**********************************

Energy Services
-----------------------------

The public water supply sector is assumed to have an efficiency level of 65%, following the assumption made in Greenberg et al. [4]. Therefore, 65% of all energy demand by the public water supply sector is assumed to go to energy services.

Rejected Energy
-----------------------------

Given the assumed efficiency level of 65%, 35% of all energy in the public water supply sector is assumed to go to rejected energy.
