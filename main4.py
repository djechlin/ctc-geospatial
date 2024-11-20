import geopandas as gpd

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

# Group by division and calculate percentages
grouped = intersections.groupby('DIVISION_N')
print("division,tract")
for division, group in grouped:
    total_area = divisions[divisions['DIVISION_N'] == division]['total_area'].iloc[0]
    max = None
    max_percentage = -1
    for _, row in group.iterrows():
        percentage = (row['intersection_area'] / total_area) * 100
        if percentage > max_percentage:
            max = row['GEOID']
            max_percentage = percentage
    print(f"{division},{max}")
