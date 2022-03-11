**************************************
Wastewater Treatment Sector (WWD)
**************************************

Water in Wastewater Treatment
################################################

Water Deliveries
**********************************

Water flow data for wastewater treatment is available at the treatment plant level from US EPA's Clean Watersheds Needs Survey data [10] . Both flows from municipal sources and infiltration flows are provided per plant where infiltration flows are considered inflows due to "The estimated portion of the wastewater flow that is entering the collection system via defective joints, connections, or manhole walls." (US EPA [11]). Note that the dataset is for the year 2012, the most recent year available. It is assumed that wastewater treatment values did not vary significantly between 2012 and 2015.

Water flow values are summed for all plants in each county. This represents wastewater demand (water flows into wastewater treatment in a county). This value can include local (inner county wastewater), infiltration, or wastewater flows that are imported from another county. For this reason, wastewater demand may not align with wastewater supply (the total discharges from the residential, commercial, and industrial sectors to wastewater supply).

For the state of South Carolina, no wastewater treatment plant data was available in the EPA data [10]. Therefore, wastewater treatment water values for that state were assumed to match the residential, commercial, and industrial sector discharges to wastewater supply. It is assumed that all water flows to wastewater from residential, commercial, and industrial sectors in each South Carolina county are treated in the same county, i.e., no wastewater supply exports.

Discharge
**********************************

The dataset on wastewater treatment facility water flows additionally includes information on the discharge locations of each plant. The discharge values to each of the below locations were collected and grouped into the following bins:

+------------------------------------------+------------------------------+
| Original Discharge Location              | Binned Discharge Location    |
+==========================================+==============================+
| outfall to surface waters                | surface discharge            |
+------------------------------------------+------------------------------+
| ocean discharge                          | ocean discharge              |
+------------------------------------------+------------------------------+
| deep well                                | ground discharge             |
+------------------------------------------+------------------------------+
| reuse: industrial                        | industrial sector            |
+------------------------------------------+------------------------------+
| evaporation                              | consumption/evaporation      |
+------------------------------------------+------------------------------+
| spray irrigation                         | crop irrigation              |
+------------------------------------------+------------------------------+
| overland flow no discharge               | wastewater demand            |
+------------------------------------------+------------------------------+
| overland flow with discharge             | surface discharge            |
+------------------------------------------+------------------------------+
| discharge to another facility            | wastewater demand            |
+------------------------------------------+------------------------------+
| combined sewer overflow (cso) discharge  | surface discharge            |
+------------------------------------------+------------------------------+
| other                                    | surface discharge            |
+------------------------------------------+------------------------------+
| discharge to groundwater                 | ocean discharge              |
+------------------------------------------+------------------------------+
| no discharge, unknown                    | wastewater demand            |
+------------------------------------------+------------------------------+
| reuse: irrigation                        | crop irrigation              |
+------------------------------------------+------------------------------+
| reuse: other non-potable                 | surface discharge            |
+------------------------------------------+------------------------------+
| reuse: indirect potable                  | surface discharge            |
+------------------------------------------+------------------------------+
| reuse: potable                           | public water supply          |
+------------------------------------------+------------------------------+
| reuse: groundwater recharge              | ground discharge             |
+------------------------------------------+------------------------------+

The percent of water discharged to each discharge location is available in the EPA dataset [10]. The highest discharge percentage for wastewater facilities is to other wastewater facilities.

+---------------------------+------------+
| Discharge Location        | US Avg. %  |
+===========================+============+
| Surface                   |   25.39 %  |
+---------------------------+------------+
| Other Wastewater Facility |   62.68 %  |
+---------------------------+------------+
| Groundwater               |    6.61 %  |
+---------------------------+------------+
| Irrigation                |    2.93 %  |
+---------------------------+------------+
| Consumption / Evaporation |    1.90 %  |
+---------------------------+------------+
| Ocean                     |    0.44 %  |
+---------------------------+------------+
| Industrial Facility       |    0.05 %  |
+---------------------------+------------+

Given that such a high percent of facilities don't discharge outside of the wastewater treatment system, these discharges to other wastewater facilities are redistributed to other discharge locations. This follows the assumption that a wastewater facility will pass water along to another treatment plant that then discharges its water instead of passing it on to yet another wastewater treatment plant. 68% of discharges to other wastewater facilities is redistributed to surface discharge, 19% is redistributed to groundwater discharge, 8% is redistributed to irrigation discharge, and 5% is redistributed to consumption/evaporation. These estimates were derived from the approximate percentage of remaining discharge percentage once discharge to wastewater facilities was removed. Note that this methodology also assumed that the secondary wastewater treatment plant that is receiving the flows exists in the same county as the original wastewater treatment facility.

Discharge fractions for all plants within each county were averaged to get the discharge percent per discharge location per county.

For counties in the state of South Carolina, given that no wastewater treatment facility data was provided, 68% were assumed to be discharged to the surface, 19% to groundwater, 8% to irrigation, and 5% to consumption.

Energy in Wastewater Treatment
################################################

Energy in wastewater treatment is dependent on the level of treatment applied at the wastewater facility. The EPA [10] dataset that includes water flow data by wastewater treatment facility also includes information on the treatment type of each facility. The treatment types listed in the data were binned into primary, secondary, advanced, and no treatment as follows:

+---------------------------------+------------------------+-----------------------------+
|Original Treatment Name          | Binned Treatment Name  | Energy Intensity (kwh/mg)   |
+=================================+========================+=============================+
|raw discharge                    | no treatment           | 0                           |
+---------------------------------+------------------------+-----------------------------+
|primary (45mg/l< bod)            | primary treatment      | 750                         |
+---------------------------------+------------------------+-----------------------------+
|advanced primary                 | advanced treatment     | 2690                        |
+---------------------------------+------------------------+-----------------------------+
|secondary wastewater treatment   | secondary treatment    | 2080                        |
+---------------------------------+------------------------+-----------------------------+
|secondary                        | secondary treatment    | 2080                        |
+---------------------------------+------------------------+-----------------------------+

The energy intensity estimates used for each treatment level were adapted from Pabi et al. [12]. Treatment type percentages for all plants within each county were averaged to get the treatment type percentages use for each county.

Of the 14,611 wastewater treatment plants included in the treatment dataset, 5,481 (37.51%) were advanced treatment, 6 had no treatment, 30 had primary treatment (0.21%), and 9,094 (62.24%) had secondary treatment.

Note that for the state of South Carolina, given that no wastewater treatment facility data was provided, treatment types are assumed to be 60% secondary and 40% advanced.

Energy Demand
**********************************

Fuel Demand
-----------------------------

No estimates currently exist regarding source of fuel for energy in wastewater treatment plants though there is likely a non-negligible percent that use alternative methods than electricity.

Electricity Demand
-----------------------------

All energy demand by wastewater treatment plants are assumed to be sourced from electricity generation supply.

Energy Discharge
**********************************

Energy Services
-----------------------------
Wastewater facilities are estimated to have a 65% efficiency rate (Greenberg et al. [4]). No county or state level efficiencies are available. 65% of all energy in wastewater treatment is assumed to go to energy services.

Rejected Energy
-----------------------------
Wastewater facilities are estimated to have a 65% efficiency rate (Greenberg et al. [4]). No county or state level efficiencies are available. 35% of all energy in wastewater treatment, therefore, is assumed to go to energy services.
