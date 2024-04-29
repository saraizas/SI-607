Oregon Department of Forestry Wildfire Occurrence and Network Analysis
============

Description:
------------
This project analyzes wildfire occurrence data from the Oregon Department of Forestry (ODF), covering the years 2000 to 2022. It comprises two main components:

1. **Mapping Wildfires**:
   - Utilizes folium, geopandas, and shapely to create interactive maps of wildfire start locations based on coordinates provided by the ODF.

2. **Data Analysis**:
   - Averages wildfire data across 36 Oregon counties over the past 22 years, incorporating population data from the US Census Bureau to assess correlations between counties based on selected variables.
   - Employs correlation matrices using Pearson's R, Spearman, and Kendall Tau's correlations to analyze data, with a focus on Kendall's Tau due to narrow variable differences across counties.
   - Visualizes county correlations through a Network Graph map with varying threshold strengths to show changes in county clustering.

Variables of Interest:
----------------------
- **AvgAcresBurned**: Average of total estimated acres burned per county.
- **AvgProtectedAcres**: Average protected acres per county, classified under The Forestland Management System by ODF.
- **HumanOrLightning**: Mode of occurrence categorized into Human (0) or Lightning (1).
- **GeneralCause**: Mode of general causes of fires encoded with specific integers (e.g., Debris Burning as 0).
- **AvgFireDuration**: Calculated by the difference between the start and end dates of each wildfire.
- **B01001_001E**: Population count per county from the US Census Bureau's 2018 American Community Survey.
======================
Installation:
Ensure you have Python installed. Install necessary libraries using:
pip install pandas seaborn numpy matplotlib requests geopandas folium shapely
======================
Usage:
Open the Jupyter notebook in an environment that supports IPython (e.g., JupyterLab). Run the cells sequentially to explore the fire occurrence data and associated analyses.

Ensure you have the original ODF Fire Occurrence dataset saved in the same location as environment. Data can be accessed here: https://data.oregon.gov/Natural-Resources/ODF-Fire-Occurrence-Data-2000-2022/fbwv-q84y/about_data
========================
API Keys:
Access to the U.S. Census API is utilized; no personal API key is required for public data endpoints.
=======================
Special Instructions:
Update the CSV file paths according to your local system setup.
=======================
Network (Graph) Organization:
Nodes represent counties in Oregon. Edges are drawn based on geographical adjacency and shared fire occurrences data between counties.

Further Information:
--------------------
For more details on forestland management classifications: https://www.oregon.gov/odf/working/pages/stateforests.aspx