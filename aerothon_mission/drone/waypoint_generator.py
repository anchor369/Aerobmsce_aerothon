# drone/waypoint_generator.py

import math
import numpy as np
from geopy.distance import geodesic

def get_tile_size(altitude, h_fov_deg, v_fov_deg):
    """
    Calculates real-world tile width and height (in meters) based on
    camera field of view and altitude.
    """
    w = 2 * altitude * math.tan(math.radians(h_fov_deg / 2))
    h = 2 * altitude * math.tan(math.radians(v_fov_deg / 2))
    return w, h

def generate_circular_grid(center, radius_m, tile_w, tile_h):
    """
    Generates zigzag lawnmower-style waypoints covering a circular geofence.
    """
    lat_c, lon_c = center
    waypoints = []

    y_range = np.arange(-radius_m, radius_m + tile_h, tile_h * 0.8)
    for y in y_range:
        row = []
        x_range = np.arange(-radius_m, radius_m + tile_w, tile_w * 0.8)
        for x in x_range:
            if x**2 + y**2 <= radius_m**2:  # Inside circle
                lat_offset = geodesic(meters=y).destination((lat_c, lon_c), 0)
                full_point = geodesic(meters=x).destination(lat_offset, 90)
                row.append((full_point[0], full_point[1]))
        if len(waypoints) % 2 == 1:
            row.reverse()  # Zigzag sweep
        waypoints.extend(row)

    return waypoints
