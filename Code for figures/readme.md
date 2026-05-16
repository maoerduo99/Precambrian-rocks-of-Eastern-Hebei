1. Overview

This repository contains 8 data visualization and processing scripts. 
category_mapping_tool.py is used for lithological classification: when plotting figures that require grouping detailed rock names into major lithological categories, this tool will be used. 
Other scripts cover sample spatial distribution mapping, major element geochemical boxplot drawing, categorical sample quantity statistical chart drawing. All generated images are high-definition vector graphic.

2. Operating Environment: Python 3.8+ / Jupyter Notebook

3. All Script List & Function Description

| Script Name | Function | Output Content |
| --- | --- | --- |
| category_mapping_tool.py | Match detailed small lithological categories to unified major rock categories; used only for plots requiring rock name grouping; support Excel/CSV input, preserve original order, export mapping results and unmatched items | Small_to_Large_Category_Mapping.xlsx, Unmatched_Small_Categories.xlsx |
| GPS coordinates.ipynb | Draw sample spatial distribution map based on WGS84 coordinates, support custom rock type column selection, add position annotation | SVG vector distribution map |
| box plot of major element.ipynb | Draw lithology-based major element boxplots, overlay sample scatter points, equip with multiple mineral classification markers | SVG vector graph, JPG high definition graph |
| Statistical data of isotopes.ipynb | Categorical Statistics Pie & Bar Chart Script : count sample quantity of classification fields, automatically merge low-frequency categories, generate two kinds of charts at the same time | SVG charts, Excel grouped detail table |
| Statistical data of major elements.ipynb | Categorical Statistics Pie & Bar Chart Script : count sample quantity of classification fields, automatically merge low-frequency categories, generate two kinds of charts at the same time | SVG charts, Excel grouped detail table |
| Statistical data of samples.ipynb | Categorical Statistics Pie & Bar Chart Script : count sample quantity of classification fields, automatically merge low-frequency categories, generate two kinds of charts at the same time | SVG charts, Excel grouped detail table |
| Statistical data of trace elements.ipynb | Categorical Statistics Pie & Bar Chart Script : count sample quantity of classification fields, automatically merge low-frequency categories, generate two kinds of charts at the same time | SVG charts, Excel grouped detail table |
| 76AGE.ipynb | Plot geochronological age distribution grouped by rock type and analytical method | Age_Distribution_Plot.svg, Analytical_Method_Count.xlsx, Rock_Type_Count.xlsx |
