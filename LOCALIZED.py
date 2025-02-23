import numpy as np
import webbrowser
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter  # Import the filter
import math

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

    webbrowser.open(map_url)




def readfile(file_path):
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


    # Print the extracted POSA values
    for values in posa_values:
        List_2D_posa.append(values)

    List_2D_Lat_long = []
    for values in lat_long:
        List_2D_Lat_long.append(values)

    np.array(List_2D_posa)

    return [List_2D_Lat_long, List_2D_posa, velocity_list]




def geodicToCartesian(geodic_list): #geodic list contains latitude, longitude, and altitude
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
    
    # Apply Savitzky-Golay filter to smooth the data
    window_length = 21  # Must be odd; adjust based on your data
    polyorder = 3       # Polynomial order; typically 2-5

    x_smooth = savgol_filter(x, window_length, polyorder)
    y_smooth = savgol_filter(y, window_length, polyorder)
    z_smooth = savgol_filter(z, window_length, polyorder)

    # Create a 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot smoothed trajectory
    ax.plot(x_smooth, y_smooth, z_smooth, 'b-', linewidth=2, label='Post-Processed Path')

    # Customize the plot
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
        c=velocities,  # Map velocity values to colors
        cmap='plasma',  # Choose a colormap (e.g., 'plasma', 'coolwarm')
        s=10,
        marker='o',
        label='Points'
    )

    # Add colorbar
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

print("Welcome to our GHacks Data visualization tool, please type in the filename containing PDPPOSA and PDPVELA data")
file_path = input("Filename(.txt Included) Filename in this case is \"Glide.txt\" \n")
while Program_in_use:
    data_list = readfile(file_path)
    List_2D_Lat_long = data_list[0]
    List_2D_posa = data_list[1]
    velocities = data_list[2]

    print("")
    print("Please Select an Option to continue")
    print("1.) Google Maps Plot Visualization \n2.) 3D plots including Raw, Processed, and velocity route map\n0.) for Exiting Program \n")
    print("=" * 80)
    user_choice = (input(""))
    if user_choice == '1':
        plot_google_maps_path(List_2D_Lat_long)
    elif user_choice == '2':
        
        cartesian = []

        for line in List_2D_posa:
            cartesian.append(geodicToCartesian(line))
        
        plot(cartesian, velocities)

        
    elif user_choice == '0':
        Program_in_use = False
        print("Thank you for using our program")
    else:
        print("Invalid input please try again")


