import math
from Hackathon import List_2D_posa, velocity_list as velocities
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter  # Import the filter
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


rad = math.pi/180
E = 0.006694
a = 6378137.0


def geodicToCartesian(geodic_list): #geodic list contains latitude, longitude, and altitude
    lowercaseh = geodic_list[2] - 16.600
    n_fi = a/(math.sqrt(1-E*(math.sin(geodic_list[0] * rad))**2))
    x = (n_fi + lowercaseh)*math.cos(geodic_list[0] * rad)*math.cos(geodic_list[1] * rad)
    y = (n_fi + lowercaseh)*math.cos(geodic_list[0] * rad)*math.sin(geodic_list[1] * rad)
    z = ((1-E)*n_fi + lowercaseh)*math.sin(geodic_list[0] * rad)
    return([x,y,z])


cartesian = []

for line in List_2D_posa:
    cartesian.append(geodicToCartesian(line))

print(rad)
print(cartesian)

x = [point[0] for point in cartesian]
y = [point[1] for point in cartesian]
z = [point[2] for point in cartesian]

# Apply Savitzky-Golay filter to smooth the data
window_length = 15  # Must be odd; adjust based on your data
polyorder = 3       # Polynomial order; typically 2-5

x_smooth = savgol_filter(x, window_length, polyorder)
y_smooth = savgol_filter(y, window_length, polyorder)
z_smooth = savgol_filter(z, window_length, polyorder)

# Create a 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot raw data (original points)
ax.scatter(x, y, z, c='r', s=10, alpha=0.3, label='Raw Points')

# Plot raw trajectory (original line)
ax.plot(x, y, z, 'r-', linewidth=1, alpha=0.3, label='Raw Path')

# Plot smoothed trajectory
ax.plot(x_smooth, y_smooth, z_smooth, 'b-', linewidth=2, label='Smoothed Path')

# Customize the plot
ax.set_xlabel('X Axis', fontsize=12)
ax.set_ylabel('Y Axis', fontsize=12)
ax.set_zlabel('Z Axis', fontsize=12)
ax.set_title('3D Trajectory with Savitzky-Golay Smoothing', fontsize=14)
ax.legend()
ax.grid(True)

plt.savefig("SavitzyGolay.png")
plt.show()


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