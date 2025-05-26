from connect_vehicle import connect_drone
from arm_and_takeoff import arm_and_takeoff
from spiral_search import spiral_search
from payload_drop import drop_payload
from rtl_home import return_to_home
from dronekit import LocationGlobalRelative
import time

vehicle = connect_drone()
arm_and_takeoff(vehicle, 15)

# 🎯 Set fixed disaster location (within your geofence)
disaster_location = (12.97129, 77.59487)  # Change to actual simulated point

current = vehicle.location.global_relative_frame
disaster = spiral_search(vehicle, current.lat, current.lon, disaster_location)

if disaster:
    lat, lon = disaster
    print("🧭 Navigating to disaster location...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, 15))
    time.sleep(5)

    print("⬇️ Descending to 10m...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, 10))
    time.sleep(5)

    drop_payload()

    print("⬆️ Climbing back to 15m...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, 15))
    time.sleep(5)

return_to_home(vehicle)
vehicle.close()
