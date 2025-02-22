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

np.array(List_2D_posa)
print(List_2D_posa)

'''
lattitude = [row[0] for row in List_2D_posa]
longitude = [row[1] for row in List_2D_posa]


# Print the result
print("Lattitude:", lattitude)
print("=" * 50)  # Prints 50 dashes
print("Lattitude:", longitude)
'''
