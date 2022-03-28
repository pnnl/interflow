.. interflow documentation master file, created by
   sphinx-quickstart on Thu Mar 10 11:13:53 2022.


Welcome to interflow
=====================================

Intro
##############################

**interflow** is an open-source python package for collecting, calculating, organizing, and visualizing cross-sectoral resource interdependencies and flows.

Background
##############################
The interdependencies and relationships between sectors can offer multi-faceted and multi-scale opportunities as well as vulnerabilities. Well known examples of sectoral interdependencies include the water required by energy-application sectors (e.g., thermoelectric cooling in the electricity generation sector) or the energy required by water-application sectors (e.g., electricity in the public water supply sector). Many economic sectors such as these rely on a consistent upstream supply of a resource type to conduct their primary operations and may be compromised if a break in the resource flow were to occur.

Ties between sectors can be complex to track, visualize, and/or pull meaningful information from. Understanding these interdependencies and evaluating where the greatest cross-sectoral intensities and flows exist can reveal opportunities to enhance the overall network. **interflow** was created to provide a flexible, adaptable, and updatable method to evaluate the interdependencies between sectors within and across regions for multiple resource types.

In addition to being flexible in handling any number of resource types (e.g., energy, water, food), the **interflow** package is also flexible in its ability to handle:

* Any number of regions to conduct calculations across
* Any sector type (e.g., public water supply, electricity generation, agriculture)
* Handle up to five levels of granularity within each sector (major sector + 4 levels of subsectors)

The package collects known flow values between sectors provided by the user and calculates additional sector connections based on provided resource intensity estimates, source sector fractions, or downstream sector discharge fractions. Collected and calculated flows are then compiled in a way that can be utilized in a variety of data visualizations offered in the package. The primary output is a Pandas DataFrame of resource flows between each sector which can be used to compare dependencies between all sectors as well as compare relative contributions by subsectors to overall sectoral flow values. Given that **interflow** collects and calculates values for each region provided in the input data, the output can additionally be used for region-wise comparisons of flows and intensities.


Statement of Need
#########################################

Existing tools in this research space are oftentimes limited to the visualization of known sectoral flow values. These are typically in the form of Sankey diagrams which are valuable for evaluation relationships between sectors, but these tools can generally only visualize known flow values, they do not offer a way to calculate the demand of a cross-resource type and build out new sectoral connections based on the result. The **interflow** package aims to fill this gap and serve as a flexible and open-source option for conducting multi-resource sectoral interdependency data calculations while also visualizing the results in a variety of ways.


Using interflow
###################################
For information on installation, dependencies, and other similar topics, see the `Getting Started <https://kmongird.github.io/interflow/getting_started.html>`_ page.

Quickstarter
###################################
A Jupyter Notebook quickstarter for **interflow** is available (see `Quickstarter.ipynb <https://github.com/pnnl/interflow/blob/main/Quickstarter.ipynb>`_) both as a standalone file and on binder so that it can be opened in an executable environment without the user having to install or download the package (`interflow Quickstarter on binder <https://mybinder.org/v2/gh/pnnl/interflow/main?labpath=Quickstarter.ipynb>`_).


Navigation
##############################

.. toctree::
   :maxdepth: 2

   getting_started

   user_guide

   quickstarter

   api_docs

   sample_data

   contributing

   authors

   license

   acknowledgement


Disclaimer
##############################

This material was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any of their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

PACIFIC NORTHWEST NATIONAL LABORATORY

operated by

BATTELLE

for the

UNITED STATES DEPARTMENT OF ENERGY

under Contract DE-AC05-76RL01830


