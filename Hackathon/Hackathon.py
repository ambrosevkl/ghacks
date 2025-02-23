import numpy as np

# Define the path to your text file

file_path = input("Filename (.txt Included) \n")

# Initialize empty lists to store the POSA and VELA values
List_2D_posa = []
posa_values = []  # 2D list for POSA values
velocity_list = []
lat_long = [] # 2D list for latitude and longitude values only

# Open the file and read its contents
with open(file_path, "r") as file:
    # Iterate through each line in the file
    for line in file:
        # Check if the line starts with #PDPPOSA
        if line.startswith("#PDPPOSA") or line.startswith("#BESTPOSA"):
            # Split the line into parts using commas
            parts = line.strip().split(",")
            # Extract the values at positions 11, 12, and 13 (latitude, longitude, altitude)
            latitude = float(parts[11])
            longitude = float(parts[12])
            altitude = float(parts[13])
            # Append the values as a list to the 2D list
            posa_values.append([latitude, longitude, altitude])
            lat_long.append([latitude, longitude])
        
        if line.startswith("#PDPVELA"):
            parts = line.strip().split(",")
            print(parts)
            velocity = float(parts[13])
            velocity_list.append(velocity)


# Print the extracted POSA values
for values in posa_values:
    List_2D_posa.append(values)

List_2D_Lat_long = []
for values in lat_long:
    List_2D_Lat_long.append(values)

np.array(List_2D_posa)




