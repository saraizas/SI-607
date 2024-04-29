import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import requests

odf_df = pd.read_csv('/Users/shirleyaraizasantaella/Documents/UMich/Grad School Year 2/Semester_2/SI_507_IntermediateProgramming/SI-607/ODF Project/ODF_Fire_Occurrence_Data_2000-2022_20240323.csv')

odf_df.head(5)

odf_df.columns

odf_df['GeneralCause'].unique()

odf_df['SpecificCause'].unique()

odf_df['County'].unique()

odf_df['DistrictName'].unique()

odf_df['FireName']

#API Request:

url = "https://api.census.gov/data/2019/acs/acs5"
params = {
    "get": "NAME,B01001_001E",
    "for": "county:*",
    "in": "state:41"
}

response = requests.get(url, params=params)
data = response.json()
print(data)

census_df = pd.DataFrame(data[1:], columns=data[0])
print(census_df.head())

census_df['NAME'] = census_df['NAME'].str.split(' County', expand=True)[0]

print(census_df)

census_df = census_df.rename(columns={
    'NAME': 'CountyName',
    'Population': 'Population',
    'state': 'StateCode',
    'county': 'CountyCode'
})

census_df.head()

#check for missing values 
odf_df.isnull().sum()

census_df.to_csv('updated_county_data.csv', index=False)

#check for formats
odf_df.dtypes

census_county_df = pd.read_csv('updated_county_data.csv')
odf_df = pd.read_csv('ODF_Fire_Occurrence_Data_2000-2022_20240323.csv')

fire_census_df = pd.merge(census_county_df, odf_df, left_on='CountyName', right_on='County', how='inner')

print(fire_census_df.head(2))

fire_census_df.to_csv('fire_census_data.csv', index=False)

import geopandas as gpd
import folium

print(fire_census_df.columns)

import shapely
from shapely.geometry import Point

fire_census_df['geometry'] = fire_census_df.apply(lambda row: Point(float(row.Long_DD), float(row.Lat_DD)), axis=1)
geo_data = gpd.GeoDataFrame(fire_census_df, geometry='geometry')

# Set the coordinate reference system (CRS) for longitude/latitude
geo_data.set_crs(epsg=4326, inplace=True)

map = folium.Map(location=[44.0, -120.5], zoom_start=7)

for idx, row in geo_data.iterrows():
    # Check if the point is not empty
    if not row['geometry'].is_empty:
        folium.Marker(
            location=[row['geometry'].y, row['geometry'].x],
            popup=f"Fire Name: {row['FireName']}<br>Year: {row['FireYear']}<br>Size: {row['EstTotalAcres']} acres",
            icon=folium.Icon(color='red', icon='fire')
        ).add_to(map)
    else:
        print(f"Skipping empty geometry for index {idx}")

map.save('oregon_wildfires.html')

from shapely.geometry import Point
import folium
import ipywidgets as widgets
from IPython.display import display, clear_output

fire_census_df = pd.read_csv('fire_census_data.csv')

# Create GeoDataFrame
fire_census_df['geometry'] = fire_census_df.apply(lambda row: Point(float(row.Long_DD), float(row.Lat_DD)), axis=1)
geo_data = gpd.GeoDataFrame(fire_census_df, geometry='geometry')
geo_data.set_crs(epsg=4326, inplace=True)

# Create dropdowns for Year and County
year_dropdown = widgets.Dropdown(
    options=sorted(geo_data['FireYear'].unique()),
    description='Year:',
    disabled=False,
)

county_dropdown = widgets.Dropdown(
    options=['All'] + sorted(geo_data['CountyName'].unique().tolist()),
    description='County:',
    disabled=False,
)



def display_map(year, county):
    clear_output(wait=True)
    display(year_dropdown, county_dropdown)
    # Filter data
    filtered_data = geo_data[(geo_data['FireYear'] == year)]
    if county != 'All':
        filtered_data = filtered_data[filtered_data['CountyName'] == county]

    # Create map
    folium_map = folium.Map(location=[44.0, -120.5], zoom_start=7)
    for idx, row in filtered_data.iterrows():
        if not row['geometry'].is_empty:
            folium.Marker(
                [row['geometry'].y, row['geometry'].x],
                popup=(
                    f"Fire Name: {row['FireName']}<br>"
                    f"Year: {row['FireYear']}<br>"
                    f"Size: {row['EstTotalAcres']} acres"
                ),
                icon=folium.Icon(color='red', icon='fire')
            ).add_to(folium_map)

    # Display the map in the notebook
    display(folium_map)


def on_dropdown_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        display_map(year_dropdown.value, county_dropdown.value) 

year_dropdown.observe(on_dropdown_change, names='value')
county_dropdown.observe(on_dropdown_change, names='value')

display(year_dropdown, county_dropdown)
display_map(year_dropdown.value, county_dropdown.value)

import networkx as nx
import warnings
warnings.filterwarnings('ignore')

#make a copy of fire_census_df
fire_census_copy = fire_census_df.copy()

fire_census_copy.columns

average_fire_size_by_county = fire_census_copy.groupby('CountyName')['EstTotalAcres'].mean().round(3)

print(average_fire_size_by_county)

average_protected_acres_by_county = fire_census_copy.groupby('CountyName')['Protected_Acres'].mean().round(3)
average_protected_acres_by_county

human_lightning_by_county = fire_census_copy.groupby('CountyName')['HumanOrLightning'].apply(lambda x: x.mode()[0])
human_lightning_by_county


cause_by_county = fire_census_copy.groupby('CountyName')['CauseBy'].apply(lambda x: x.mode()[0])
cause_by_county

general_cause_by_county = fire_census_copy.groupby('CountyName')['GeneralCause'].apply(lambda x: x.mode()[0])
general_cause_by_county

# Convert to datetime if necessary
fire_census_copy['Ign_DateTime'] = pd.to_datetime(fire_census_copy['Ign_DateTime'])
fire_census_copy['Control_DateTime'] = pd.to_datetime(fire_census_copy['Control_DateTime'])

# Calculate duration of each fire
fire_census_copy['FireDuration'] = fire_census_copy['Control_DateTime'] - fire_census_copy['Ign_DateTime']

# Calculate average fire duration by county
average_fire_duration_by_county = fire_census_copy.groupby('CountyName')['FireDuration'].mean()

print(average_fire_duration_by_county)

data = {

    'AvgAcresBurned': average_fire_size_by_county,
    'AvgProtectedAcres': average_protected_acres_by_county,
    'HumanOrLightning': human_lightning_by_county,
    'GeneralCause': general_cause_by_county,
    'AvgFireDuration': average_fire_duration_by_county
}

networks = pd.DataFrame(data)

networks['GeneralCause'].unique()

networks.head(3)

from sklearn.preprocessing import LabelEncoder
# Create a LabelEncoder
# Create two LabelEncoders
le_general_cause = LabelEncoder()
le_human_or_lightning = LabelEncoder()

# Fit and transform the 'GeneralCause' column
networks['GeneralCause'] = le_general_cause.fit_transform(networks['GeneralCause'])

# Fit and transform the 'HumanOrLightning' column
networks['HumanOrLightning'] = le_human_or_lightning.fit_transform(networks['HumanOrLightning'])

# Print the classes for 'GeneralCause'
for i in range(len(le_general_cause.classes_)):
    print(f"GeneralCause: {le_general_cause.inverse_transform([i])[0]} is labeled as {i}")

# Print the classes for 'HumanOrLightning'
for i in range(len(le_human_or_lightning.classes_)):
    print(f"HumanOrLightning: {le_human_or_lightning.inverse_transform([i])[0]} is labeled as {i}")


networks.head(3)

updated_county_data = pd.read_csv('updated_county_data.csv')
merged_networks = networks.merge(updated_county_data[['CountyName', 'B01001_001E']], on='CountyName')
merged_networks

merged_networks.to_csv('merged_networks.csv', index=False)

merged_networks.head(3)

merged_networks.dtypes

merged_networks = pd.DataFrame(merged_networks)
merged_networks['AvgFireDuration'] = merged_networks['AvgFireDuration'].astype(str)

# Preprocess and convert to timedelta
merged_networks['AvgFireDuration'] = merged_networks['AvgFireDuration'].str.split('.').str[0]
merged_networks['AvgFireDuration'] = pd.to_timedelta(merged_networks['AvgFireDuration'])

# Extract components
merged_networks['DurationDays'] = merged_networks['AvgFireDuration'].dt.days
merged_networks['DurationHours'] = merged_networks['AvgFireDuration'].dt.components.hours
merged_networks['DurationMinutes'] = merged_networks['AvgFireDuration'].dt.components.minutes
merged_networks['DurationSeconds'] = merged_networks['AvgFireDuration'].dt.components.seconds


merged_networks.head(3)

#Drop AvgFireDuration column
merged_networks = merged_networks.drop(columns=['AvgFireDuration'])

merged_networks.head(3)

merged_networks=merged_networks.T
merged_networks.head(3)

# Set the first row as the header
new_header = merged_networks.iloc[0]  # Take the first row for the header
merged_networks = merged_networks[1:]  # Take the data less the header row
merged_networks.columns = new_header  # Set the header row as the df header

merged_networks.head(3)

merged_networks.dtypes

# merged_networks['CountyName_encoded'] = pd.factorize(merged_networks['CountyName'])[0]

# Select numeric columns including the new 'CountyName_encoded'
numeric_cols = merged_networks.select_dtypes(include=['float64', 'int64', 'int'])
# numeric_cols = pd.concat([numeric_cols, merged_networks[['CountyName_encoded']]], axis=1)

# Recalculate the correlation matrix
corr = numeric_cols.corr()

# Generate a heatmap of the correlation matrix
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

print(corr)

import numpy as np
import networkx as nx

print(nx.__version__)

# Convert the correlation matrix DataFrame to a numpy matrix
matrix = corr.values

G = nx.from_numpy_array(matrix)

names = list(corr.index)

# Create a dictionary that maps integer node IDs to their names
mapping = dict(zip(range(len(names)), names))

# Relabel the nodes to their names
G = nx.relabel_nodes(G, mapping)

# Remove self-loops
G.remove_edges_from(nx.selfloop_edges(G))

# Create a threshold
threshold = 0.025

# Create a new graph to hold the thresholded network
G_thresholded = nx.Graph()

# Add nodes to the new graph
G_thresholded.add_nodes_from(G)

# Iterate over the edges in the original graph
for u, v, d in G.edges(data=True):
    # Check if the absolute value of the weight is greater than or equal to the threshold
    if abs(d['weight']) >= threshold:
        # If it is, add the edge to the thresholded graph
        G_thresholded.add_edge(u, v, weight=d['weight'])

# Draw the thresholded network
nx.draw(G_thresholded, with_labels=True)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 10))  # Bigger figure size
sns.set(font_scale=1.2)  # Increase font size

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")

plt.title('Improved Correlation Matrix')
plt.show()

# API Call for NOAA Weather Data
import requests
import json
import csv

#NOAA API Key
api_key = 'tvHSwWrsZQEJUzjeNsVbTbGyqdFwfyyX'

url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
params = {
    'datasetid': 'GHCND',  # Global Historical Climatology Network Daily
    'locationid': 'FIPS:41',  # Oregon's FIPS code
    'startdate': '2023-01-01',
    'enddate': '2023-01-31',
    'limit': 1000,
    'units': 'standard'
}

headers = {
    'token': api_key
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        records = data.get('results', [])

        # Define CSV file path
        csv_file_path = 'noaa_data.csv'

        # Define the headers based on the JSON structure you expect
        headers = ['station', 'date', 'datatype', 'value', 'attributes']

        # Write to CSV
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for record in records:
                writer.writerow(record)

        print(f"Data successfully written to {csv_file_path}")

    except requests.exceptions.JSONDecodeError:
        print("JSON decode error occurred:", response.text)
else:
    print("Failed to retrieve data:", response.status_code, response.text)

noaa_data = pd.read_csv('noaa_data.csv')
noaa_data.head(3)

noaa_data.shape

