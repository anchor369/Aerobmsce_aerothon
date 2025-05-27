from connect_vehicle import connect_drone
from arm_and_takeoff import arm_and_takeoff
from spiral_search import spiral_search
from payload_drop import drop_payload
from rtl_home import return_to_home
from dronekit import LocationGlobalRelative
import time

# Step 1: Connect to vehicle
vehicle = connect_drone()

# Step 2: Takeoff
arm_and_takeoff(vehicle, 15)

# Step 3: Get starting position (center of geofence)
current = vehicle.location.global_relative_frame
center_lat = current.lat
center_lon = current.lon

# Step 4: Simulated disaster location close to SITL origin
disaster_location = (center_lat + 0.0001, center_lon + 0.0001)  # ~11m offset

# Step 5: Run spiral search with circular geofence
disaster = spiral_search(
    vehicle=vehicle,
    center_lat=center_lat,
    center_lon=center_lon,
    disaster_location=disaster_location,
    detection_radius=10,           # in meters
    max_geofence_radius=50         # geofence radius in meters
)

# Step 6: If disaster is detected, fly to it
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

# Step 7: Return home and close
return_to_home(vehicle)
vehicle.close()
