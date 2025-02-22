import numpy as np

# Define the path to your text file
file_path = "data1.txt"  # Replace with the actual path to your file

# Initialize empty lists to store the POSA and VELA values
vela_values = []  # 2D list for VELA values

# Open the file and read its contents
with open(file_path, "r") as file:
    # Iterate through each line in the file
    for line in file:
        # Check if the line starts with #PDPPOSA
        if line.startswith("#PDPVELA"):
            # Split the line into parts using commas
            parts = line.strip().split(",")
            # Extract the values at position 15 (horizontal speed)
            speed = float(parts[15])
            # Append the values as a list to the 2D list
            vela_values.append(speed)
    

# Print the extracted POSA values
print(vela_values)
