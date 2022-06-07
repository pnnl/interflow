**************************
Energy (Fuels) Production
**************************

Energy in Energy Production
################################################

The following energy production (fuel) types are included in the analysis:

* Natural gas
* Petroleum
* Coal
* Biomass

For all of the fuel production types except coal, data by type is taken from US EIA SEDS state-level data for 2015 [8]. Data is provided in BBTU/yr. Information is provided at the state level and broken up based on various methodologies described in greater detail below.

MSN codes used from the EIA SEDS [8] dataset include:

* "PAPRB": Crude oil production (including lease condensate)
* "EMFDB": Biomass inputs (feedstock) to the production of fuel ethanol
* "NGMPB": Natural gas marketed production

Coal production data is provided in an alternative mine-level dataset [17] that allows us to aggregate production to the county level. This is discussed in greater detail later on this page.

Note that for energy sources that are not direct fuels (e.g., solar, nuclear), any production is directly consumed and values are captured in electricity production or fuel demand by end use sectors.

Various methods are used to break up state-level energy production values into county level values. These are described for each of the four fuel types below.

**Coal Production**
**********************************
Coal production at the county level is provided from two separate datasets. The first dataset, US EIA E-7 [17], includes coal production data (tons), coal mine type (surface or underground), as well as the Mine ID number for 2015. The Mine ID number provided in the US EIA dataset is used to map coal mine data to the secondary dataset (coal mine data provided by the US Department of Labor - Mine Safety and Health Administration [18]). The latter of these datasets includes the county FIPS codes for each Mine ID that is used to aggregate production to the county level. While information is provided for Refuse coal mines in the EIA dataset in addition to surface and underground mines, these mines are not included in this analysis.

Coal production for each mine type is provided in short tons per year. This is converted to bbtu where one short ton is equal to 0.02009 bbtu. Production values by mine type are aggregated to the county level.

**Biomass (Ethanol) Production**
**********************************
County level ethanol production is estimated using the EIA 819 dataset containing individual ethanol plant capacities as of January 1 2016 [24] and county locational information for each ethanol plant name provided by the State of Nebraska [25]. Open source data on plant production for the year 2015 was not found, leading to the capacity estimates serving as a proxy for production. State-level production inputs from EIA SEDS [8] are distributed to individual counties within a state based on the fraction of total state ethanol production capacity.

The state of Wyoming appears in the EIA SEDS [8] dataset as having ethanol production but does not appear in the ethanol plant data file. Information on which county the ethanol production takes place in, therefore, is filled in with information from [25]. Only one ethanol plant is included for the state of Wyoming as of January 2016 in Torrington County.

**Natural Gas Production**
**********************************
To obtain county-level estimates of natural gas production from state-level estimates for 2015, a 2011 USDA Economic Research Service dataset [26] of county-level natural gas production is used. The data provides production values for onshore production in the lower 48 states. No data for years 2012 onwards was found and the data product has since been discontinued by USDA. The fraction of state production for each county within a given state was multiplied by state level natural gas production values provided from EIA SEDS [8] to get county-level estimates.

The state production dataset from EIA SEDS [8] includes state-level values for states that are not included in the county-level production data from USDA [26]. For these states, production by county are individually assessed from a variety of sources, described below.

For the state of Idaho, all production of natural gas is estimated to come from a single county (Payette County) according to a 2016 data release by the Idaho Department of Lands [27]

Data from the State of Alaska's Oil and Gas Conservation Commission [28] helps to pinpoint which regions of the state are the primary producers of natural gas. The large majority of natural gas production comes from the North Slope area of Alaska (>96%) while the remainder is produced in the Cook Inlet Basin (Kenai Peninsula). These percentages are used to split up total state natural gas production for 2015.

For the state of Maryland, natural gas production was found to occur in two different counties (Garret County and Allegany County) according to a state energy analysis provided by EIA [29]. No information was found on the relative production within each county. As a result, it is assumed that production is split evenly between the two counties. No year is associated with these county estimates, however, it is assumed that the location of recoverable natural gas in the state will not change substantially. Both counties are in the western part of the state and overlie part of the Marcellus Shale. Note that, since 2017 Maryland enacted a permanent ban on hydraulic fracturing for natural gas and oil production.

Very low natural gas production exists for the state of Nevada. The production that did occur in 2015 is estimated to originate from Nye County. This estimate is predominantly formed upon the basis that the largest number of oil and gas well potential appears clustered within that county. Information for this estimate is provided through potential oil and gas well maps from the University of Nevada - Reno [30].

For the state of Oregon, only one county is listed for gas production (Columbia County) associated with the Mist Gas Field. Information for this estimate is provided by the State of Oregon Department of Geology and Mineral Industries [31]. The data on production under this gas field is provided annually with values available for 2015. All state natural gas production for Oregon for 2015 is assigned to this county.

**Petroleum Production**
**********************************
Limited information exists on a county-level for petroleum production that differentiates between conventional and unconventional production. According to the US EIA, 63% of all oil is shale (unconventional) [32]. Until additional information is available, it is assumed that state-level petroleum production is divided out into the two categories by this fraction.

*Unconventional Oil (Petroleum)*
----------------------------------------------------------
To obtain county-level estimates of unconventional petroleum production from state-level estimates for 2015, a 2011 USDA Economic Research Service dataset [26] of county-level petroleum production is used. The data provides production values for onshore production in the lower 48 states. No data for years 2012 onwards was found and the data product has since been discontinued by USDA. The fraction of state production for each county within a given state was multiplied by state level petroleum production values provided from EIA SEDS [8] to get county-level estimates.

Two states appear in the EIA SEDS [8] petroleum production datafile that do not appear in the 2011 USDA [26] county level production and must be filled in individually, these are described below.

For the state of Idaho, all production of unconventional petroleum is estimated to come from a single county (Payette County) according to a 2016 data release by the Idaho Department of Lands [27]

Data from the State of Alaska's Oil and Gas Conservation Commission [28] helps to pinpoint which regions of the state are the primary producers of unconventional petroleum. The large majority of unconventional production comes from the North Slope area of Alaska (>97%) while the remainder is produced in the Cook Inlet Basin (Kenai Peninsula). These percentages are used to split up total state unconventional petroleum production for 2015.

*Conventional Oil (Petroleum)*
----------------------------------------------------------
Following the assumption that 63% of all petroleum production is unconventional petroleum production, the remainder falls to conventional production. State-level petroleum production values are split into conventional and unconventional petroleum through this fraction. The amount of state-level petroleum production that is conventional is split into individual counties using the same methodology applied to unconventional production using the 2011 USDA county-level petroleum production [26].

Water in Energy Production
################################################

Water in energy production is calculated for the following energy types:
- Coal (specifically, dust control in mining)
- Biomass (specifically, water used in corn growth for ethanol production and water use in the industrial production of ethanol from corn grain)
- Natural gas (water used in unconventional natural gas wells)
- Petroleum (water used in conventional and unconventional oil wells)

Each of these are described in more detail below.

**Water in Coal**
**********************************

*Water Withdrawal*
-----------------------------
To determine the amount of water used in the production of coal from each type of coal mine (surface vs. underground), the assumptions from Greenberg et al. [4] are used. Greenberg et al. [4] estimates that surface mines withdraw 7 gallons of water per ton of coal and underground mines withdraw 29 gallons per ton. To determine water source/type for mining dust control, it is assumed that the source of the water withdrawal for coal mining follows the same distribution of water use for other types of mining in the same county. For example, if 50% of water withdrawals for all mining in a county are estimated to come from fresh surface water, the same percentage is applied to coal mining. Water withdrawals for all mining types is provided in the USGS 2015 water use dataset [1].

Given that water withdrawals for coal mining are implicitly included in the water withdrawals for all mining in the USGS 2015 [1] dataset, the estimated water withdrawals for coal mining are subtracted from the water withdrawals to all mining to avoid double counting. This is completed by multiplying the county-level coal production for both surface and underground mines in bbtu by the estimated water intensity values described above. The outcome is substracted from the water withdrawals to mining provided in Dieter et al. [1] for the year 2015. For counties where the estimated water use for coal mining exceeded the amount of water in all mining presented in the USGS data file (Dieter et al. [1]), the amount of water to non-coal mining was set to zero.

Water use in coal mining is represented as water withdrawals delivered to the mining sector under the coal subsector category.

*Water Consumption/Evaporation*
----------------------------------------------------------
Estimates for consumed water from coal mining follow the same consumption fractions as for all mining water consumed. These values are not available in the 2015 dataset and are instead calculated from the 1995 USGS dataset on a county basis (Sulley et al.). For more information on how these values were derived, see the Mining sector page.

*Water Discharge*
----------------------------------------------------------
Very few coal mines exist in coastal areas of the united states. Therefore, following in line with assumptions made in Greenberg et al. [4], 100% of water not consumed in the production of coal is
assumed to be discharged to the surface.

Water in Biomass
**********************************

*Agricultural Irrigation of Corn for Ethanol*
----------------------------------------------------------
Water use in the production of ethanol is included in two forms in this analysis: (1) water use in the agriculture sector that is put towards the irrigation of corn used in the production of ethanol and (2) water used in the industrial sector to process the corn and produce ethanol. These flow values are provided separately and are described in greater detail below.

**Water Withdrawal**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Data on water used in corn growth for ethanol production does not exist explicitly at any level of granularity and must be calculated out from larger state-level totals of irrigation water and corn production. The general methodology for calculating the water use in biomass follows that outlined in Greenberg et al. [4], however, a national average percent of corn grown for ethanol (described below) is used in place of their ethanol fraction estimate.

The assumed percent of all corn grown for ethanol in the US was used from the US DOE Alternative Fuels Data Center [20]. Total corn production for ethanol (5.22 billion bushels) was divided by total corn production (13.6 billion bushels) for 2015 and calculated to be 38.406%. Data on a state or county level for this estimate does not exist in a public database, therefore, this percentage is applied to all states with corn production. A state-level fraction of corn used for ethanol production could be calculated from the amount of ethanol produced in a state and applying an assumption of corn required per unit of ethanol, however, this would lead to data anomalies such as states like California producing an ethanol fraction of nearly 900% of their total corn production. Given that we are unable to determine which states the imported corn for ethanol would be coming from, the decision was made to apply the US total fraction to all states.

Total water used in the production of corn for ethanol is therefore the assumed 38.406% multiplied by the product of the total amount of irrigated acres of corn and the calculated irrigation intensity for that state (total acres applied to all crops / total acres irrigated, all crops) provided from USDA Census of Agriculture Irrigation and Water Management Survey (Perdue et al [22]), Table 35 and Table 4, respectively. The irrigation intensity for corn is assumed to be equivalent to the irrigation intensity for all crops given that state-level corn irrigation intensity data is not available.

To split the total water applied to crop irrigation for corn growth for ethanol between fresh surface water and fresh groundwater, USDA FRIS Census of Agriculture [21] data on surface water (surface water + off farm water) as a percent of total water (including groundwater) in corn production is used from Table 37 of [21]. Off-farm sources are assumed to be surface water.

Note: the state of New York (NY) does not have data on ground vs. surface water sources for corn irrigation. It is assumed, therefore, for this state, that the ratio between surface water and groundwater in corn growth for ethanol matches the average ratio from all other states.

To split state-level water use values into county-level values, county-level corn production data is used from USDA NASS [22]. It is assumed that the county level corn production as a fraction of state level corn production is an adequate way to split up state-level water withdrawal quantities. The county-level corn production fractions are multiplied by the state level water withdrawal values to obtain county-level water withdrawal values.

Water withdrawals for corn growth for ethanol are represented as a sub-subsector in the Agriculture-crop irrigation sector in the dataset. To avoid double counting in the data, the estimated water used in corn growth for ethanol is substracted from the water use in all crop irrigation.

**Water Consumption/Evaporation**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water consumption fraction estimates for corn growth for ethanol used in biomass are expected to follow the same consumption fraction estimates for all crop irrigation. This information is provided directly in in Dieter et al. [1].

**Water Discharge**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water discharge estimates for corn growth for ethanol used in biomass are expected to follow the same discharge estimates for all crop irrigation. All water discharged from crop irrigation is expected to be to the surface.

*Industrial Ethanol Production*
----------------------------------------------------------

**Water Withdrawal**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water is used in the industrial sector to produce ethanol in the fermentation process. The current estimate for water intensity (gallons of water per gallon of ethanol) is approximately 3 gallons. This estimate is provided from Argonne National Laboratory [23]. All water used in the fermentation of ethanol is assumed to come from fresh surface water.

Water withdrawals in the industrial sector for the production of ethanol is separated out as an individual subsector under the Industrial sector. To avoid double counting of water flows to the industrial sector, the values calculated for ethanol production are subtracted out from total water use in industrial applications provided by Dieter et al. [1].

**Water Consumption/Evaporation**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water consumption fraction estimates for the industrial production in ethanol are expected to follow the same consumption fraction estimates for all industrial applications in a given county. For more information on these estimates, see the Industrial sector section.

**Water Discharge**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Water discharged from the industrial production of ethanol is assumed to be equal to all water that is not consumed. All water not consumed by this sector is assumed to be discharged to the surface, following the same discharge fraction assumptions for other industrial applications.


**Water in Natural Gas**
**********************************

*Water Withdrawal*
----------------------------------------------------------
No county level water use or water intensity estimates exist for natural gas for the year 2015. Water use estimates for natural gas extraction for this analysis are used from Greenberg et al. [4] for 2012. There was significant growth in the production of natural gas between 2012 and 2015, meaning that the water use estimates from [4] are likely significantly smaller than 2015. The values from [4] are therefore, scaled up by the growth of natural gas production between years (1.11x). Only state-level values for unconventional petroleum and natural gas extraction are available in their dataset. State-level values are split into county-level values following the same methodology used to split up the state-level natural gas production values described previously.

The intensity of water use in unconventional natural gas drilling was determined by taking the total water to unconventional natural gas production in each county and dividing it by the total natural gas production per day in the same county. The average intensity value (million gallons per bbtu) was applied to counties that recorded unconventional natural gas production in 2015 but no water estimates were available.

It is assumed that 80% of water withdrawals by natural gas production are from fresh surface water sources and the remainder is from fresh groundwater sources following the methodology in Greenberg et al. [4]. No saline water is assumed to be used in the production of natural gas and no water flows to natural gas are assumed to come from wastewater reuse.

*Produced Water*
----------------------------------------------------------
When water is injected into the ground for natural gas production, some additional water is extracted or "produced". No exact values exist regarding produced water for oil and natural gas individually. Veil [32] provided an analysis for 2017 on produced water by state and Greenberg et al. [4] adapted these to provide values for states with missing data. The information from both of these sources is used here. Produced water values are converted to million gallons of water per bbtu and applied to unconventional natural gas production by county. For states without a value, the US average is supplied.

The water-oil-ratio (WOR) (barrels of water/barrel of oil) and water-gas-ratio (WGR) [barrels of water/million cubic feet (mmcf) of natural gas] from Greenberg et al. [4] were applied to 2015 data on oil and gas production to estimate total produced water. For the state of Idaho, which did not have a WOR value in the dataset, the WOR and WGR was assumed to be the average of both Montana and Wyoming. This produced water was split out into injection, surface discharge, and consumption/evaporation based on percentage breakdowns by state provided in [32]. Note that offsite disposal of water is assumed to be injected

*Water Consumption/Evaporation*
----------------------------------------------------------
The same resource (Veil [32]) that provided produced water intensities for natural gas also supplied discharge percentages to surface, injection (ground), and consumption for each state. These estimates do not differentiate between natural gas and petroleum drilling. The assumption is made that these values are equivalent and are applied appropriately. For states without estimates, the national average is applied.

*Water Discharge*
----------------------------------------------------------
See the Water Consumption/Evaporation section above.

**Water in Petroleum**
**********************************

*Water Withdrawal*
----------------------------------------------------------
No county level water use or water intensity estimates exist for unconventional petroleum for the year 2015. Water use estimates for unconventional petroleum extraction for this analysis are used from Greenberg et al. [4].  There was significant growth in the production of petroleum between 2012 and 2015, meaning that the water use estimates from [4] are likely significantly smaller than 2015. The values from [4] are therefore, scaled up by the growth of petroleum production between years (1.48x).Only state-level values for unconventional petroleum and natural gas extraction are available in their dataset. State-level values are split into county-level values following the same methodology used to split up the state-level unconventional petroleum production values described previously.

For conventional petroleum water intensity, gallon of water per gallon of oil (WOR) estimates were provided by Greenberg et al. [4]. For states that were not included in the dataset but had 2015 conventional petroleum production, the average US WOR value was applied.

It is assumed that 80% of water withdrawals for conventional petroleum production are from fresh surface water sources and the remainder is from fresh groundwater sources following Greenberg et al. [4]. No saline water is assumed to be used in the production of petroleum. 0% of water flows to petroleum are assumed to come from wastewater reuse.

*Produced Water*
----------------------------------------------------------
The methodology for petroleum produced water follows that of natural gas. See the Natural Gas Produced water section above for more information.

*Water Consumption/Evaporation*
----------------------------------------------------------
Consumption - Consumption estimates for petroleum follow the same as those as natural gas and are applied to all water (withdrawals + produced) in petroleum (conventional and unconventional). These values are estimated from Veil [32].

*Water Discharge*
----------------------------------------------------------
Discharge estimates for petroleum follow the same as those as natural gas and are applied to all water (withdrawals + produced) in petroleum (conventional and unconventional). Note that offsite disposal of water is assumed to be injected.
