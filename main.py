from geopy.distance import geodesic

# Define two locations (latitude, longitude)
new_york = (40.7128, -74.0060)
los_angeles = (34.0522, -118.2437)

# Calculate the distance between the two points
distance = geodesic(new_york, los_angeles).miles

print(f"Hello, World!")
print(f"The distance between New York City and Los Angeles is approximately {distance:.2f} miles.")

