import json
import os
import dotenv
import geopandas as gpd
from census import Census
from us import states
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Initialize Census object with API key
c = Census(os.getenv('CENSUS_API_KEY'))

# Load shapefiles
tracts = gpd.read_file('cb_2020_us_tract_500k.shp')
divisions = gpd.read_file('Political_Divisions.shp')

# Ensure same CRS
if tracts.crs != divisions.crs:
    divisions = divisions.to_crs(tracts.crs)

# Perform spatial join
intersections = gpd.overlay(divisions, tracts, how='intersection')

# Calculate areas
intersections['intersection_area'] = intersections.geometry.area
divisions['total_area'] = divisions.geometry.area

# Calculate overlap percentages
intersections['overlap_percentage'] = intersections['intersection_area'] / divisions['total_area']


# Fetch census data
def get_census_data(geoids):
    data = c.acs5.state_county_tract(
        fields=('NAME', 'B19013_001E', 'B25003_002E', 'B25003_001E'),
        state_fips=states.PA.fips,
        county_fips='101',  # Philadelphia County FIPS code
        tract=geoids,
        year=2020
    )
    return pd.DataFrame(data)

# Get unique tract GEOIDs
tract_geoids = intersections['GEOID'].unique()

# Fetch census data for all tracts
census_data = get_census_data([geoid[5:11] for geoid in tract_geoids])
census_data['GEOID'] = states.PA.fips + '101' + census_data['tract']

# Calculate home ownership percentage
census_data['home_ownership_pct'] = census_data['B25003_002E'] / census_data['B25003_001E'] * 100

# Merge census data with intersections
merged_data = intersections.merge(census_data, on='GEOID', how='left')

# Calculate weighted averages for each division
results = merged_data.groupby('DIVISION_N').apply(lambda x: pd.Series({
    'weighted_median_income': (x['B19013_001E'] * x['overlap_percentage']).sum() / x['overlap_percentage'].sum(),
    'weighted_home_ownership_pct': (x['home_ownership_pct'] * x['overlap_percentage']).sum() / x['overlap_percentage'].sum()
})).reset_index()

# Print results
for _, row in results.iterrows():
    print(f"Division {row['DIVISION_N']}:")
    print(f"  Estimated Median Income: ${row['weighted_median_income']:.2f}")
    print(f"  Estimated Home Ownership %: {row['weighted_home_ownership_pct']:.2f}%")
    print()