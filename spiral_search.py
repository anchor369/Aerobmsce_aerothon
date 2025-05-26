import math
import time
from dronekit import LocationGlobalRelative
import random

def spiral_search(vehicle, center_lat, center_lon, loops=2, radius=0.00015):
    print("Starting spiral search...")
    step_angle = math.pi / 4
    disaster_found = None

    for i in range(int(loops * 8)):
        angle = i * step_angle
        r = radius * (1 + 0.5 * i)
        lat = center_lat + r * math.cos(angle)
        lon = center_lon + r * math.sin(angle)
        point = LocationGlobalRelative(lat, lon, 15)

        print(f"[{i+1}] Goto: ({lat}, {lon})")
        vehicle.simple_goto(point)
        time.sleep(5)  # Simulate travel

        # 🔥 FAKE DISASTER DETECTION
        if random.random() < 0.2:
            print("🚨 Disaster detected!")
            disaster_found = (lat, lon)
            break

    return disaster_found
