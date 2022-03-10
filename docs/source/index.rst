.. interflow documentation master file, created by
   sphinx-quickstart on Thu Mar 10 11:13:53 2022.


Welcome to interflow
=====================================

Intro
##############################

**interflow** is an open-source python package for collecting, calculating, organizing, and visualizing cross-sectoral resource interdependencies and flows.

Background
##############################
**interflow** was created to provide a flexible, adaptable, and updatable method to evaluate the interdependencies between sectors and across regions for multiple resource types. The interdependencies and relationships between sectors offer multi-faceted and multi-scale opportunities as well as vulnerabilities. Whether it is water, energy, or otherwise, resources pass from source to discharge by flowing through sectors and are oftentimes a critical component of a sector's functionality. Well known examples of some of these dependencies include the water required by energy-application sectors (e.g., thermoelectric cooling in the electricity generation sector) and the energy required by water-application sectors (e.g., electricity in the public water supply sector). The ties between sectors can be complex to track, visualize, and/or pull meaningful information from. Many sectors rely on the uninterrupted flow between an "upstream" sector and themselves, leaving them vulnerable to adverse effects should something interrupt that resource handoff or compromise it in some way. The impacts of an event occurring in one sector or subsector may not necessarily be contained within that sector but may instead flow through its connecting network. This package was developed to offer a flexible way to organize known flows, trace resource flows between sectors, calculate new resource flows from existing alternative resource flow values based on sectoral intensity factors, and visualize the results on both a sectoral and regional basis.

Being able to understand the ties between sectors, trace the flow of resources, and evaluate where the greatest cross-sectoral intensities exist can reveal opportunities for enhancement in the system at a whole.

In addition to being flexible in handling any number of resource types (e.g., energy and water), the **interflow** package is also flexible in its ability to handle:
* Any number of regions to conduct calculations across
* Any sector type (e.g., public water supply, electricity generation)
* Handle up to five levels of granularity within each sector

The package collects known flow values between sectors provided by the user, calculates other sector connections based on provided resource intensity estimates, source sector fractions, and downstream sector fractions, and compiles the results in a way that can be utilized in a variety of data visualizations. The output of the package can be used to compare dependencies between all sectors as well as compare relative contributions by subsectors to overall sectoral flow values. Given that **interflow** collects and calculates values for each region provided in the input data, the output can additionally be used for region-wise comparisons of flows and intensities.






.. toctree::
   :maxdepth: 2

   getting_started

   user_guide

   quickstarter

   api

   sample_data

   contributing

   authors

   license

   acknowledgement



