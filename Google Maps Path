import webbrowser

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

# Example usage
coordinates = [
    [51.0795, -114.1315],
    [51.0800, -114.1300],
    [51.0810, -114.1285],
    [51.0820, -114.1270]
]

plot_google_maps_path(coordinates)
