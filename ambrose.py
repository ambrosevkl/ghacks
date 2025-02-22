import webbrowser
from DataProcessing import List_2D_posa

def plot_google_maps_path(coordinates):
    """
    Opens Google Maps in a web browser with a path plotted using given latitude and longitude coordinates.

    Args:
        coordinates (list of lists): 2D list of [latitude, longitude] pairs.
    """
    base_url = "https://www.google.com/maps/dir/"

    # Format coordinates into a path
    path = "/".join([f"{lat},{lng}" for lat, lng in coordinates])

    # Construct full URL
    map_url = f"{base_url}{path}"

    print("Opening Google Maps with path:", map_url)
    webbrowser.open(map_url)

import numpy as np


# Define the path to your text file
file_path = "data1.txt"  # Replace with the actual path to your file

# Initialize empty lists to store the POSA and VELA values
List_2D_posa = []
posa_values = []  # 2D list for POSA values
vela_values = []  # 2D list for VELA values

# Open the file and read its contents
with open(file_path, "r") as file:
    # Iterate through each line in the file
    for line in file:
        # Check if the line starts with #PDPPOSA
        if line.startswith("#PDPPOSA"):
            # Split the line into parts using commas
            parts = line.strip().split(",")
            # Extract the values at positions 11, 12, and 13 (latitude, longitude, altitude)
            latitude = float(parts[11])
            longitude = float(parts[12])
            #altitude = float(parts[13])
            # Append the values as a list to the 2D list
            posa_values.append([latitude, longitude])
    

# Print the extracted POSA values
print("POSA Values (2D List):")
for values in posa_values:
    List_2D_posa.append(values)

# Example usage
coordinates = [
    [51.0795, -114.1315],
    [51.0800, -114.1300],
    [51.0810, -114.1285],
    [51.0820, -114.1270]
]
np.array(List_2D_posa)
print(List_2D_posa)

plot_google_maps_path(List_2D_posa)
