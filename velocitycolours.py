import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter  # Import the filter
from matplotlib import cm

# Constants
rad = math.pi / 180
E = 0.006694
a = 6378137.0

def geodicToCartesian(geodic_list):
    n_fi = a / (math.sqrt(1 - E * (math.sin(geodic_list[0] * rad))**2))
    x = (n_fi + geodic_list[2]) * math.cos(geodic_list[0] * rad) * math.cos(geodic_list[1] * rad)
    y = (n_fi + geodic_list[2]) * math.cos(geodic_list[0] * rad) * math.sin(geodic_list[1] * rad)
    z = ((1 - E) * n_fi + geodic_list[2]) * math.sin(geodic_list[0] * rad)
    return [x, y, z]

# Sample input data (replace with real data parsing)
List_2D_posa = [...]  # PDPPOSA data parsed into [[lat, lon, alt], ...]
List_2D_vela = [...]  # PDPVELA data parsed into speed magnitudes

cartesian = [geodicToCartesian(line) for line in List_2D_posa]

x = [point[0] for point in cartesian]
y = [point[1] for point in cartesian]
z = [point[2] for point in cartesian]

# Apply Savitzky-Golay filter to smooth the data
window_length = 15  # Must be odd; adjust based on your data
polyorder = 3       # Polynomial order; typically 2-5

x_smooth = savgol_filter(x, window_length, polyorder)
y_smooth = savgol_filter(y, window_length, polyorder)
z_smooth = savgol_filter(z, window_length, polyorder)

# Extract speed magnitudes from PDPVELA
speed_magnitudes = [line[15] for line in List_2D_vela]

# Normalize speed values between 0 (blue) and 2 (red)
speed_magnitudes = np.clip(speed_magnitudes, 0, 2)  # Ensure values are in range
norm_speeds = speed_magnitudes / 2  # Normalize to [0,1] for colormap
colors = cm.coolwarm(norm_speeds)  # Use a blue-red colormap

# Create a 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot trajectory with color-mapped speed
sc = ax.scatter(x, y, z, c=speed_magnitudes, cmap='coolwarm', s=10, marker='o')
plt.colorbar(sc, label='Speed Magnitude (m/s)')

# Customize the plot
ax.set_xlabel('X Axis', fontsize=12)
ax.set_ylabel('Y Axis', fontsize=12)
ax.set_zlabel('Z Axis', fontsize=12)
ax.set_title('3D Trajectory Colored by Speed', fontsize=14)
ax.grid(True)

# Show the plot
plt.savefig("Trajectory_Colored.png")
plt.show()
