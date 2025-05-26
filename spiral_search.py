import math
import time
from dronekit import LocationGlobalRelative

def haversine_distance(lat1, lon1, lat2, lon2):
    """Returns distance in meters between two lat/lon points"""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def spiral_search(vehicle, center_lat, center_lon, disaster_location, loops=2, radius=0.00015, detection_radius=10):
    print("Starting spiral search...")
    step_angle = math.pi / 4
    disaster_found = None

    for i in range(int(loops * 8)):
        angle = i * step_angle
        r = radius * (1 + 0.5 * i)
        lat = center_lat + r * math.cos(angle)
        lon = center_lon + r * math.sin(angle)
        point = LocationGlobalRelative(lat, lon, 15)

        print(f"[{i+1}] Goto: ({lat:.6f}, {lon:.6f})")
        vehicle.simple_goto(point)
        time.sleep(5)  # Simulate travel

        # 🔍 Fake camera detection by distance
        distance = haversine_distance(lat, lon, disaster_location[0], disaster_location[1])
        print(f"📷 Checking with camera... Distance to disaster: {distance:.2f}m")
        if distance < detection_radius:
            print("🚨 Camera DETECTED disaster at this location!")
            disaster_found = (lat, lon)
            break

    if not disaster_found:
        print("✅ No disaster detected in spiral.")
    return disaster_found
