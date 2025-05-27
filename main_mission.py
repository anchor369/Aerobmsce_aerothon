from connect_vehicle import connect_drone
from arm_and_takeoff import arm_and_takeoff
from spiral_search import spiral_search
from payload_drop import drop_payload
from rtl_home import return_to_home
from dronekit import LocationGlobalRelative
import time

def hover_and_confirm_disaster(vehicle, lat, lon):
    print("👁 Hovering to confirm disaster...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, 15))
    time.sleep(3)
    print("✅ Confirmed: Actual disaster detected.")
    return True

# Step 1: Connect to vehicle
vehicle = connect_drone()

# Step 2: Take off
arm_and_takeoff(vehicle, 15)

# Step 3: Determine geofence center
current = vehicle.location.global_relative_frame
center_lat = current.lat
center_lon = current.lon

# Step 4: Place disaster somewhere inside geofence (mock)
disaster_location = (center_lat + 0.00025, center_lon + 0.0002)  # ~30m offset

# Step 5: Fly to outer edge of geofence
start_lat = center_lat + (50 / 111111)  # ~50m north
start_lon = center_lon
print("🛫 Flying to outer edge of geofence...")
vehicle.simple_goto(LocationGlobalRelative(start_lat, start_lon, 15))
time.sleep(10)

# Step 6: Begin inward spiral search
disaster = spiral_search(
    vehicle=vehicle,
    center_lat=center_lat,
    center_lon=center_lon,
    disaster_location=disaster_location,
    detection_radius=10,
    max_geofence_radius=50  # meters
)

# Step 7: Handle detection
if disaster:
    lat, lon = disaster
    if hover_and_confirm_disaster(vehicle, lat, lon):
        print("⬇️ Descending to 10m...")
        vehicle.simple_goto(LocationGlobalRelative(lat, lon, 10))
        time.sleep(5)

        drop_payload()

        print("⬆️ Climbing back to 15m...")
        vehicle.simple_goto(LocationGlobalRelative(lat, lon, 15))
        time.sleep(5)

# Step 8: Return home
return_to_home(vehicle)
vehicle.close()
