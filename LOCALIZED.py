import numpy as np
import webbrowser
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter  # Import the SavitzyGolay filter
import math

def plot_google_maps_path(coordinates):
    """
    Opens a Google Maps directions URL in the default web browser using a list of coordinates.

    Parameters:
         A 2D list containing Latitude and Longitude values for each datapoint

    Returns:
        None: The function constructs a Google Maps URL and opens it in a web browser.
    """

    base_url = "https://www.google.com/maps/dir/"

    # Format coordinates into a path
    path = "/".join([f"{lat},{lng}" for lat, lng in coordinates])

    # Construct full URL
    map_url = f"{base_url}{path}"

    webbrowser.open(map_url)




def readfile(file_path):
    """
    Reads a file and extracts geodetic position data (latitude, longitude, altitude) and velocity values.

    Parameters:
        file_path (str): The path to the input file containing POSA and VELA data.

    Returns:
        list: A list containing three elements:
            - List_2D_Lat_long (list of lists): A 2D list where each sublist contains [latitude, longitude].
            - List_2D_posa (list of lists): A 2D list where each sublist contains [latitude, longitude, altitude].
            - velocity_list (list of float): A list of velocity values.
    """

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
                velocity = float(parts[13])
                velocity_list.append(velocity)


    #Contain the extracted POSA values
    for values in posa_values:
        List_2D_posa.append(values)

    #Contain the extracted Latitude and Longitude Values from POSA
    List_2D_Lat_long = []
    for values in lat_long:
        List_2D_Lat_long.append(values)

    return [List_2D_Lat_long, List_2D_posa, velocity_list]




def geodicToCartesian(geodic_list): #geodic list contains latitude, longitude, and altitude
    """
    Converts geodetic coordinates (latitude, longitude, and altitude) to Cartesian coordinates (x, y, z).

    Parameters:
        geodic_list (list of float): A list containing three elements:
            - geodic_list[0]: Latitude in degrees
            - geodic_list[1]: Longitude in degrees
            - geodic_list[2]: Altitude in meters

    Returns:
        list of float: A list [x, y, z] representing the Cartesian coordinates in meters.

    """

    #Defining Constants
    rad = math.pi/180
    E = 0.006694
    a = 6378137.0
    lowercaseh = geodic_list[2] - 16.600

    n_fi = a/(math.sqrt(1-E*(math.sin(geodic_list[0] * rad))**2))
    x = (n_fi + lowercaseh)*math.cos(geodic_list[0] * rad)*math.cos(geodic_list[1] * rad)
    y = (n_fi + lowercaseh)*math.cos(geodic_list[0] * rad)*math.sin(geodic_list[1] * rad)
    z = ((1-E)*n_fi + lowercaseh)*math.sin(geodic_list[0] * rad)
    return([x,y,z])




def plot(cartesian, velocities):
    """
    Generates three different 3D trajectory visualizations based on given Cartesian coordinates
    and velocity values.

    Parameters:
        cartesian (list of tuples): A list of (x, y, z) coordinate tuples representing the trajectory.
        velocities (list of float): A list of velocity values corresponding to each point in the trajectory.

    The function produces and saves three plots:
    1. A raw 3D trajectory plot displaying the original data points and path.
    2. A smoothed 3D trajectory plot using the Savitzky-Golay filter for noise reduction.
    3. A 3D scatter plot where points are color-coded based on velocity.

    Each plot is displayed and saved as an image file:
    - "Raw_Data.png"
    - "SavitzyGolay.png"
    - "Velocity_Colored_Plot.png"
    """
    x = [point[0] for point in cartesian]
    y = [point[1] for point in cartesian]
    z = [point[2] for point in cartesian]

    # Create a 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the trajectory
    ax.plot(x, y, z, 'b-', linewidth=1, label='Path')  # Line plot
    ax.scatter(x, y, z, c='g', s=10, marker='o', label='Points')  # Points

    # Customize the plot
    ax.set_xlabel('X Axis', fontsize=12)
    ax.set_ylabel('Y Axis', fontsize=12)
    ax.set_zlabel('Z Axis', fontsize=12)
    ax.set_title('3D Trajectory Plot (Raw Data)', fontsize=14)
    ax.legend()
    ax.grid(True)

    # Show the plot
    plt.savefig("Raw_Data.png")
    plt.show()
    
    # Apply Savitzky-Golay filter to smoothen data
    window_length = 21  
    polyorder = 3       

    x_smooth = savgol_filter(x, window_length, polyorder)
    y_smooth = savgol_filter(y, window_length, polyorder)
    z_smooth = savgol_filter(z, window_length, polyorder)

    # Create a 3D plot for Raw data
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot smoothed trajectory
    ax.plot(x_smooth, y_smooth, z_smooth, 'b-', linewidth=2, label='Post-Processed Path')

    # Customizing plot
    ax.set_xlabel('X Axis', fontsize=12)
    ax.set_ylabel('Y Axis', fontsize=12)
    ax.set_zlabel('Z Axis', fontsize=12)
    ax.set_title('3D Trajectory with Savitzky-Golay Smoothing', fontsize=14)
    ax.legend()
    ax.grid(True)

    plt.savefig("SavitzyGolay.png")
    plt.show()


    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot points colored by velocity
    scatter = ax.scatter(
        x, y, z,
        c=velocities,  # Mapping velocity values to colors
        cmap='plasma',  #Choice of colourmap
        s=10,
        marker='o',
        label='Points'
    )

    # Add colorbar legend for user
    norm = Normalize(vmin=min(velocities), vmax=max(velocities))
    cbar = plt.colorbar(ScalarMappable(norm=norm, cmap=scatter.cmap), ax=ax, shrink=0.5)
    cbar.set_label('Velocity', fontsize=12)

    # Customize the plot
    ax.set_xlabel('X Axis', fontsize=12)
    ax.set_ylabel('Y Axis', fontsize=12)
    ax.set_zlabel('Z Axis', fontsize=12)
    ax.set_title('3D Trajectory with Velocity-Dependent Colors', fontsize=14)
    ax.legend()
    ax.grid(True)

    plt.savefig("Velocity_Colored_Plot.png")
    plt.show()



Program_in_use = True

# Prompt user for the input file containing PDPPOSA and PDPVELA data
print("Welcome to our GHacks Data Visualization Tool!")
print("Please type in the filename containing PDPPOSA and PDPVELA data.")
file_path = input("Filename (.txt included). Example: \"Glide.txt\" \n")

# Main program loop
while Program_in_use:
    # Read data from the specified file
    data_list = readfile(file_path)

    # Extract relevant lists from the data into global variables
    List_2D_Lat_long = data_list[0]  # Latitude and longitude data
    List_2D_posa = data_list[1]      # Full geodetic data (lat, long, altitude)
    velocities = data_list[2]        # Velocity data

    # Display user options
    print("\nPlease select an option to continue:")
    print("1.) Google Maps Plot Visualization")
    print("2.) 3D plots including Raw, Processed, and Velocity Route Map")
    print("0.) Exit Program")
    print("=" * 80)

    # Get user input
    user_choice = input("")

    if user_choice == '1':
        # Generate and open Google Maps route visualization
        plot_google_maps_path(List_2D_Lat_long)

    elif user_choice == '2':
        # Convert geodetic coordinates to Cartesian coordinates
        cartesian = []
        for line in List_2D_posa:
            cartesian.append(geodicToCartesian(line))
        
        # Generate 3D trajectory plots (raw, processed, and velocity-mapped)
        plot(cartesian, velocities)

    elif user_choice == '0':
        # Exit the program
        Program_in_use = False
        print("Thank you for using our program!")

    else:
        # Handle invalid inputs
        print("Invalid input. Please try again.")


