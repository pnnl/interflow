---
layout: default
title: Setup
parent: User Guide
nav_order: 3
---

# Setup

The **flow** package requies a pandas DataFrame with input data to run the calculations. This DataFrame can be read in using the flow.read_input_data() function which takes a file path and reads the data in as a pandas DataFrame. The flow package comes with a sample input data file with input flow values for all US counties for the year 2015 and can be found in the sample_data folder in the GitHub repository.

Though the flow package has data to run the calculations for US counties, data for other regions, sectors, and units can be provided and run through the model. For more information on how to structure the input data and required formatting, see the 'Generalizability' page.


## Calculating flows

To calculate the flows between sectors specified in the input data, the `flow.calculate()` function is used. The function takes the input data, loops through each calculation in each region included, aggregates values appropriately, and returns a pandas DataFrame of source node to target node flow values in the specified units.
