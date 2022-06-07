[![build](https://github.com/pnnl/interflow/actions/workflows/build.yml/badge.svg)](https://github.com/pnnl/interflow/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/pnnl/interflow/branch/main/graph/badge.svg)](https://codecov.io/gh/pnnl/interflow)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pnnl/interflow/main?labpath=Quickstarter.ipynb)
[![status](https://joss.theoj.org/papers/ae736aa6e75758498cf79ab8ec3fa886/status.svg)](https://joss.theoj.org/papers/ae736aa6e75758498cf79ab8ec3fa886)



# interflow

`interflow` is an open-source Python package for collecting, calculating, organizing, and visualizing cross-sectoral 
resource interdependencies and flows.

## Purpose
`interflow` provides a flexible, adaptable, and updatable method to evaluate the interdependencies 
between sectors and across regions for multiple resource types. The interdependencies and relationships between 
sectors offer multi-faceted and multi-scale opportunities as well as vulnerabilities. Whether it is water, energy, 
or otherwise, resources pass from source to discharge by flowing through sectors and are oftentimes a critical 
component of a sector's functionality.

The `interflow` package was created to:

* Provide a framework to aggregate and organize known resource flows through various sectors within a region
* Calculate and build additional flows between sectors in alternative units based on interdependency 
intensity values
* Provide data output and visualizations in a format that can be used to answer questions about cross-sectoral 
dependencies, how resources flow through sectors in an individual region, and how these dependencies compare across 
regions.

![fig](https://user-images.githubusercontent.com/74064300/160175598-a48f218c-ac9f-4226-a599-4072a280733c.png)


Though the package comes equipped with sample data for water and energy values across multiple sectors at the US county 
level, the interflow package can be used for any region, set of regions, set of sectors, and resource type so long as
the appropriate data is provided by the user. 

For more information on how the interflow package works, how to generalize it with your own data, see [the 
documentation](https://pnnl.github.io/interflow/).

## Installation

interflow can be installed via pip by running the following from a terminal window:

```bash
pip install interflow
```

## Quickstarter

See interflow in action with our [Quickstarter Jupyter Notebook](https://mybinder.org/v2/gh/pnnl/interflow/main?labpath=Quickstarter.ipynb) hosted on binder!

## User Guide

If you're interested in background information and explanations on how the model works visit out [User Guide](https://pnnl.github.io/interflow/user_guide.html)

## Contributing to interflow

Spotted a bug or have a suggestion to improve the model? We'd love your input! See our [guidelines for contributing](https://pnnl.github.io/interflow/contributing.html).


