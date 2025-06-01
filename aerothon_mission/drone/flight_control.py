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
        print("⏳ Waiting for drone to arm...")
        time.sleep(1)

    vehicle.simple_takeoff(target_altitude)

    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f"🔼 Current Altitude: {current_alt:.2f} m")
        if current_alt >= target_altitude * 0.95:
            print("✅ Reached target altitude.")
            break
        time.sleep(1)

def goto_point(vehicle, lat, lon, alt):
    """
    Commands the drone to fly to a specific GPS coordinate at given altitude.
    Waits until the drone is close enough to the target.
    """
    print(f"➡️ Navigating to waypoint: ({lat:.6f}, {lon:.6f}, {alt:.2f} m)")
    target_location = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(target_location)

    while True:
        current = vehicle.location.global_relative_frame
        dist_lat = abs(current.lat - lat)
        dist_lon = abs(current.lon - lon)
        dist_alt = abs(current.alt - alt)

        print(f"📍 Current Position: ({current.lat:.6f}, {current.lon:.6f}, {current.alt:.2f} m)")

        if dist_lat < 0.00005 and dist_lon < 0.00005 and dist_alt < 1.0:
            print("✅ Reached waypoint.")
            break

        time.sleep(1)
