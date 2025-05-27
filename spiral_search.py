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
    print("🌀 Starting inward spiral search within circular geofence...")

    step_angle = math.pi / 6  # 30° per step
    i = 0
    disaster_found = None
    visited = set()

    # Convert meters to degrees (~111111 meters per degree)
    r = max_geofence_radius / 111111

    while r > 0.00005:  # spiral until close to center
        angle = i * step_angle
        lat = center_lat + r * math.cos(angle)
        lon = center_lon + r * math.sin(angle)

        # Skip if too far (edge case)
        distance_from_center = haversine_distance(center_lat, center_lon, lat, lon)
        if distance_from_center > max_geofence_radius:
            i += 1
            continue

        coord_key = (round(lat, 6), round(lon, 6))
        if coord_key in visited:
            i += 1
            continue
        visited.add(coord_key)

        point = LocationGlobalRelative(lat, lon, 15)
        print(f"[{i+1}] Goto: ({lat:.6f}, {lon:.6f}) | Dist from center: {distance_from_center:.2f}m")
        vehicle.simple_goto(point)
        time.sleep(4)

        distance_to_disaster = haversine_distance(lat, lon, disaster_location[0], disaster_location[1])
        print(f"📷 Checking with camera... Distance to disaster: {distance_to_disaster:.2f}m")

        if distance_to_disaster < detection_radius:
            print("🚨 Disaster DETECTED!")
            disaster_found = (lat, lon)
            break

        # Shrink radius inward every 12 points (1 full loop)
        if (i + 1) % 12 == 0:
            r *= 0.9  # shrink spiral
        i += 1

    if not disaster_found:
        print("✅ No disaster detected within circular geofence.")
    return disaster_found
