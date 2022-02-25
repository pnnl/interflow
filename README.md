[![build](https://github.com/kmongird/flow/actions/workflows/build.yml/badge.svg)](https://github.com/kmongird/flow/actions/workflows/build.yml)

# flow

flow is an open-source python package that organizes, calculates, and evaluates cross-sectoral interdependencies.
The package was developed as part of the Integrated Water Power Resilience project at Pacific Northwest National 
Laboratory.

## Purpose
Interdependencies between sectors can be complex to evaluate and understand despite the potentially 
opportunities to leverage them. One of the most well documented examples of cross-sectoral dependency 
is between the water sector and energy sector. Electricity generation can require water to cool thermoelectric
generating plants, to operate hydroelectric facilities, or in other applications. Likewise, moving water from one
location to another or treating it for consumption takes energy. In addition to the energy-water-nexus, 
other sectors are additionally dependent on their production and availability including food or land. The list of
connections is vast and the linkages between sectors can be a complicated network of dependency and reliance. Few
tools exist that can aid in understanding these connections and visualizing their dependencies. 

The flow package was created to:

* Provide a framework to aggregate and track how energy, water, or other units flow through various sectors within 
a region
* Build additional flows in alternative units based on the flows in another
* Provide data output that can be used to generate visualizations and analysis between and within any number of sectors.

The visualization of the flows and interconnections between water and energy has been done at various scales 
and levels and in a variety of ways. Sankey diagrams, which provide a proportional representation of processes 
and major transfers within a system, are one of the most popular visualization methods for this research area 
but can be notoriously difficult to build data for.

![image](https://user-images.githubusercontent.com/74064300/135877886-91cac5ec-614a-4fee-b9d2-3561bb69d62c.png)


## Project Background

The motivation of the Integrated Water Power Resilience Project is to identify and develop opportunities to 
improve resilience in the water and power sectors through coordinated planning, investment, and operations 
and thereby provide benefits to power and water utilities, consumers, and the environment. 

Water and power utilities are interdependent, subject to many of the same natural and manmade hazards, and 
critical for the well-being of communities and society. Because of the interconnectedness of water and power 
systems there are substantial economic, social, and environmental benefits to co-managing the market sectors 
for resilience, instead of managing them separately.
