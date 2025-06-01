# drone/flight_control.py

import time
from dronekit import VehicleMode, LocationGlobalRelative

def takeoff_to_altitude(vehicle, target_altitude):
    """
    Arms the drone and initiates takeoff to a specified altitude.
    """
    print(f"🛫 Arming and taking off to {target_altitude} meters...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("⏳ Waiting for arming...")
        time.sleep(1)

    vehicle.simple_takeoff(target_altitude)

    while vehicle.location.global_relative_frame.alt < target_altitude * 0.95:
        print(f"🔼 Altitude: {vehicle.location.global_relative_frame.alt:.2f} m")
        time.sleep(1)

    print("✅ Target altitude reached.")

def goto_point(vehicle, lat, lon, alt):
    """
    Commands the drone to fly to a specific GPS coordinate at given altitude.
    """
    print(f"➡️ Navigating to waypoint: ({lat:.6f}, {lon:.6f}, {alt}m)")
    location = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(location)
    time.sleep(4)  # Adjust based on distance or use distance check
