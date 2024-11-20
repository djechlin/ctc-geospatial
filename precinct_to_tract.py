import geopandas as gpd

# Load the shapefile
tracts = gpd.read_file('cb_2020_us_tract_500k.shp')

# Specify the tract we're interested in
target_tract_id = '42101002801'

# Filter for the specific tract
target_tract = tracts[tracts['GEOID'] == target_tract_id]

if not target_tract.empty:
    print(f"Data for Census Tract {target_tract_id}:")
    
    # Iterate through all columns and print their values
    for column in target_tract.columns:
        if column != 'geometry':
            value = target_tract.iloc[0][column]
            print(f"{column}: {value}")
    
    # Print basic information about the geometry
    print("\nGeometry Information:")
    print(f"Geometry Type: {target_tract.iloc[0]['geometry'].geom_type}")
    print(f"Area: {target_tract.iloc[0]['geometry'].area:.6f} square degrees")
    print(f"Boundary Length: {target_tract.iloc[0]['geometry'].length:.6f} degrees")
    
    # Calculate and print the centroid
    centroid = target_tract.iloc[0]['geometry'].centroid
    print(f"\nCentroid of the tract:")
    print(f"Latitude: {centroid.y:.6f}")
    print(f"Longitude: {centroid.x:.6f}")
else:
    print(f"Census Tract {target_tract_id} not found in the shapefile.")