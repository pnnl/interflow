[![build](https://github.com/kmongird/flow/actions/workflows/build.yml/badge.svg)](https://github.com/kmongird/flow/actions/workflows/build.yml)

# flow

flow is an open-source Python package for collecting, calculating, organizing, and visualizing cross-sectoral 
resource interdependencies and flows.

## Purpose
Interdependencies between sectors can be multi-faceted, complex to evaluate, and difficult to visualize in a way
that gives actionable interpretations. The links between sectors and their reliance on one other is not always
well-understood in either a detailed or broad context. This can leave opportunities for optimization unclaimed and 
potential cascading effects of sectoral impacts unquantified. Commonly discussed examples of cross-sectoral dependency 
include the interconnections between water and energy. The sectors with energy applications (e.g., electricity 
generation) require water to operate. Likewise, sectors that provide water services (e.g., public water supply) require
energy to pump, treat, and move water from location to another. Failure to understand these flows between sectors can 
lead to vulnerabilities should something happen "upstream" in the flow. In addition to the energy-water-nexus, other 
sectors are additionally dependent on their production and availability such as food or land. The list of connections 
is vast and the linkages between sectors can be a complicated network of dependency and reliance. The flow package was 
built to help aid in understanding and evaluating these interconnections on both a sectoral and a regional-scale.

The flow package was created to:

* Provide a framework to aggregate and organize known resource flows through various sectors within a region
* Calculate out and build additional flows between sectors in alternative units based on interdependency 
intensity values to analyze additional resource network maps.
* Provide data output and visualizations in a format that can be used conduct analysis of all flows within a region,
flows into and out of sectors within a region, and understand how flows and interdependencies vary across regions.

![image](https://user-images.githubusercontent.com/74064300/135877886-91cac5ec-614a-4fee-b9d2-3561bb69d62c.png)

For more information on how the flow package works, how to generalize it with your own data for any region or
interdependency linkages, see the documentation.

## Project Background

The motivation of the Integrated Water Power Resilience Project is to identify and develop opportunities to 
improve resilience in the water and power sectors through coordinated planning, investment, and operations 
and thereby provide benefits to power and water utilities, consumers, and the environment. 

Water and power utilities are interdependent, subject to many of the same natural and manmade hazards, and 
critical for the well-being of communities and society. Because of the interconnectedness of water and power 
systems there are substantial economic, social, and environmental benefits to co-managing the market sectors 
for resilience, instead of managing them separately.
