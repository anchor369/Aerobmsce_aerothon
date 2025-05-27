import math
import time
from dronekit import LocationGlobalRelative

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def spiral_search(vehicle, center_lat, center_lon, disaster_location, detection_radius=10, max_geofence_radius=50):
    print("🌀 Starting spiral search with circular geofence...")

    step_angle = math.pi / 4  # 8 directions
    i = 0
    r = 0.0001  # initial radius in degrees
    disaster_found = None

    while True:
        angle = i * step_angle
        r = 0.0001 * (1 + 0.15 * i)  # increase radius slowly
        lat = center_lat + r * math.cos(angle)
        lon = center_lon + r * math.sin(angle)

        # Check if this point is inside the circular geofence (in meters)
        distance_from_center = haversine_distance(center_lat, center_lon, lat, lon)
        if distance_from_center > max_geofence_radius:
            print(f"⛔ Skipping point outside circular geofence ({distance_from_center:.2f}m): ({lat:.6f}, {lon:.6f})")
            i += 1
            continue

        point = LocationGlobalRelative(lat, lon, 15)
        print(f"[{i+1}] Goto: ({lat:.6f}, {lon:.6f})")
        vehicle.simple_goto(point)
        time.sleep(5)

        distance_to_disaster = haversine_distance(lat, lon, disaster_location[0], disaster_location[1])
        print(f"📷 Checking with camera... Distance to disaster: {distance_to_disaster:.2f}m")
        if distance_to_disaster < detection_radius:
            print("🚨 Disaster DETECTED!")
            disaster_found = (lat, lon)
            break

        if distance_from_center >= max_geofence_radius:
            print("✅ Reached edge of geofence. Stopping search.")
            break

        i += 1

    if not disaster_found:
        print("✅ No disaster detected within circular geofence.")
    return disaster_found
