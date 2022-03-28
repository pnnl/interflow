**************************
Sample Data
**************************

Introduction
##############

The sample data provided for the interflow package includes water and energy resource values at the U.S. county level for a variety of sectors. This page documents the data sources, the methodology used to convert (where necessary) and organize the input data values. This sample data was aggregated as a subtask of the Integrated Water Power Resilience Project at Pacific Northwest National Laboratory.

Project Background
############################

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

For the full list of US counties and their corresponding FIPS codes, see the `county list <https://pnnl.github.io/interflow/county_list.html>`_

GeoJSON
**********************************

In order to plot county-level outputs from the US 2015 dataset, a GeoJSON file containing geometry information for the US counties is required. The file used and included in the sample data is from Plotly's sample datafiles. The raw JSON datafile can be found in Plotly [19]. A small number of counties included in the GeoJSON file required adjustment to match the baseline county list for the sample data. The FIPS codes for these counties were adjusted accordingly in the GeoJSON file. Note that the modified version of this file is included in the input data, not the raw GeoJSON file.

For more information on the base map configuration for Plotly's cloropleth maps, see the `Plotly cloropleth map documentation <https://plotly.com/python/choropleth-maps/>`_


Methodology
####################

The pages linked below document the methodology, data, and assumptions used in building the us county input data. Information is presented by sector. Note that energy production is not represented in the final dataset as a separate sector but is split out between the industrial and mining sectors depending on a variety of factors. A separate page documenting its methodology has been provided however for additional clarity.

Sectors
******************************************************************************************************

`Agriculture Sector <https://pnnl.github.io/interflow/agriculture_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Commercial Sector <https://pnnl.github.io/interflow/commercial_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Electricity Generation Sector <https://pnnl.github.io/interflow/electricity_gen_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Energy Production <https://pnnl.github.io/interflow/energy_production.html>`_
-------------------------------------------------------------------------------------------------------------

`Industrial Sector <https://pnnl.github.io/interflow/industrial_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Mining Sector <https://pnnl.github.io/interflow/mining_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Public Water Sector <https://pnnl.github.io/interflow/public_water_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Residential Sector <https://pnnl.github.io/interflow/residential_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Transportation Sector <https://pnnl.github.io/interflow/transportation_sector.html>`_
-------------------------------------------------------------------------------------------------------------

`Wastewater Treatment Sector <https://pnnl.github.io/interflow/wastewater_sector.html>`_
-------------------------------------------------------------------------------------------------------------


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
16. USGS (2021). US Board on Geographic Names. https://www.usgs.gov/u.s.-board-on-geographic-names/download-gnis-data
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
