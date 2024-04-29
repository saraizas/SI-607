Data Sources Overview
======================================================================
1. Oregon Department of Forestry (ODF) Fire Occurrence Data
-----------------------------------------------------------
**Origin**: Oregon Department of Forestry
**URL**:
- Data: [ODF Fire Data](https://data.oregon.gov/Natural-Resources/ODF-Fire-Occurrence-Data-2000-2022/fbwv-q84y/about_data)
- Documentation: [ODF Documentation](https://www.oregon.gov/odf/fire/pages/firestats.aspx)

**Format**: CSV
**Access Method**:
- The data was accessed directly by downloading the csv file via the ODF's official website.
- Python's `pandas` library was used to read the CSV files.

**Caching**:
- Data was temporarily cached on local storage to reduce the number of downloads during development.

**Summary**:
- Number of Variables: 38 original variables (e.g., FireName, StartDate, EndDate, CountyName, EstTotalAcres, etc.)
- The dataset includes detailed records of wildfire occurrences in Oregon from 2000 to 2022

2. U.S. Census Bureau's American Community Survey
-------------------------------------------------
**Origin**: U.S. Census Bureau
**URL**:
- Data: [American Community Survey Data](https://data.census.gov/cedsci/)
- Documentation: [ACS Documentation](https://www.census.gov/programs-surveys/acs)

**Format**: JSON
**Access Method**:
- Accessed via the Census Bureau's API using requests in Python.
- Data was requested for demographic statistics of Oregon counties, particularly focusing on population figures.

**Caching**:
- Responses were cached using simple file-based caching to avoid redundant API calls during development.

**Summary**:
- Number of Variables: 5 (e.g., B01001_001E - Total Population, StateCode, CountyCode, etc.)
- Provides characteristic data for wildfires by county in Oregon, aiding in correlational analysis with wildfire data.

======================================================================
For more details on forestland management classifications: https://www.oregon.gov/odf/working/pages/stateforests.aspx
For further details on data processing and analysis methods, refer to the main project documentation.