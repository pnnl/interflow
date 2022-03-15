---
title: 'interflow: A Python package to organize, calculate, and visualize sectoral interdependency flow data’
tags:
  - Python
  - sectoral interdependencies
  - sankey diagrams
  - flow diagrams 
authors:
  - name: Kendall L. Mongird
    orcid: 0000-0003-2807-7088
    affiliation: 1
  - name: Konstantinos Oikonomou
    affiliation: 1
  - name: Juliet S. Homer
    affiliation: 1
  - name: Jennie S. Rice
    affiliation: 1
affiliations:
  - name: Pacific Northwest National Laboratory, Richland, WA, USA
    index: 1
date: 1 April 2022
bibliography: paper.bib
---

# Summary

Investigating interdependencies and relationships between sectors can reveal multi-faceted opportunities and risks. Many sectors have cross-resource intensities where their demand of one resource (e.g., energy) is directly tied to their production or usage of an alternative resource (e.g., water). Well known examples of these kinds of sectoral relationships include water demand by energy-application sectors (e.g., thermoelectric cooling for nuclear generation) [@webber2017; @grubert2018] and energy demand by water-application sectors (e.g., electricity required to treat water in the public water sector) [@copeland2017]. These sectors often rely on an uninterrupted supply from an “upstream” sector to conduct their primary functions, leaving them vulnerable to adverse effects should that resource flow be interrupted or compromised [@epa2010; @oecd2017]. Being able to calculate and document the transfer of resources from sector to sector and evaluate where the greatest cross-sectoral intensities and flows exist can reveal opportunities for enhancement throughout the network. Despite the implications and potential impacts with regards to resource security and resiliency, however, these interconnections and flows have been historically complex to organize and pull meaningful information from. 
The `interflow` package is presented as a flexible tool to organize, calculate, and visualize sectoral flow values for multiple resource types. Its output can help decision makers, researchers, and other audiences analyze and utilize their data on the interdependencies between sectors, within sectors, and across regions. The `interflow` package can help us answer questions such as (1) which sectors have high cross-resource dependencies, (2) how does demand for a resource in various sectors compare across regions, and (3) where are the sectoral and regional opportunities for enhancement and resiliency development based on the dependencies presented. 

# Statement of Need

To the best of our knowledge, there is no software available for calculating, organizing, and visualizing sectoral interdependencies in one tool. Software exists for visualizing sectoral flow values as Sankey diagrams such as the proprietary e!Sankey software [@esankey2022] or the Python library matplotlib [@hunter2007], but these tools can only visualize known flow values. They do not offer a way to calculate the demand of a second resource type based on intensity factors and build out flow diagrams based on the result. The interflow package aims to fill this gap and serve as a flexible and open-source option for conducting multi-resource sectoral interdependency data calculations while also visualizing the results from a variety of perspectives. 
Sectoral interdependency analysis itself is not a new area of research with countless studies documenting the interconnections between water, energy, land, and other resource types [@curmi2013; @liu2016; @greenberg2017]. However, the articles and research publications in this area typically only return the end-product of their analysis (e.g., output values or diagrams). The detailed methodology or algorithms developed to conduct their calculations is often not provided openly, freely, or in a transparent manner. Researchers looking to build upon or modify the existing assumptions and data are left to redevelop the calculation structure from scratch as a result. The interflow package will offer a solution to this problem through a consistent and open-source calculation framework that can be utilized in a repeated manner so long as the input data is provided in the correct form. 

# Design and Methodology

The `interflow` package iterates through user-provided tabular input data to (1) collect known resource flow values (e.g., water demand) between provided sectors, (2) calculate new sector flow values for a secondary resource type from the initial flow (e.g., energy demand based on the water flow) using provided cross-resource intensity coefficients, and (3) build upstream and downstream sector connections to carry those calculated flows. Collected and calculated flows are then compiled in a way that can be utilized in a variety of data visualization functions offered in the package. 
The basic methodology described above is repeated for all regions provided by the user, offering a highly flexible tool that can conduct calculations for multiple areas and at multiple levels of granularity. Though the ‘interflow’ package comes equipped with sample data to evaluate U.S. county-level water and energy flows across various sectors, it can conduct analysis for any region (e.g., country, province, postal code), any sector or group of sectors (e.g., electricity generation, agriculture), and any type of resource (e.g., water, energy, food, carbon, land) and is limited only by the input data that the user provides. Information on the input data requirements is provided in the [generalizability documentation]( https://kmongird.github.io/interflow/user_guide.html#generalizability)
A Pandas DataFrame [@mckinney2010] containing collected and calculated flow values between sectors for each region is returned as an output from the `calculate()` function. The output from the model is described in greater detail in the [output documentation]( https://kmongird.github.io/interflow/user_guide.html#key-outputs). The DataFrame output can be directly used with other package functions to generate a variety of visualizations which utilize the Plotly Python package [@plotly2015] including (1) Sankey diagrams showing the network of flows across sectors for a chosen region, (2) stacked bar charts of inflow and outflow values for sectors in a region, and (3) a cloropleth map to compare flow values across regions. The visualizations can be used to compare dependencies across and between sectors at various levels of sub-sector granularity. Given that interflow collects and calculates values for each region provided in the input data, the output can additionally be used for region-wise comparisons of flows and intensities.

# Acknowledgements

This research was supported by the U.S. Department of Energy, Water Power Technologies Office, as part of research in Integrated Water Power Resilience.

# References
