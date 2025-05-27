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
    # Add future camera confirmation here
    print("✅ Confirmed: Actual disaster detected.")
    return True

# Connect and takeoff
vehicle = connect_drone()
arm_and_takeoff(vehicle, 15)

# Geofence center
current = vehicle.location.global_relative_frame
center_lat = current.lat
center_lon = current.lon

# Set disaster location slightly inside geofence (mocked)
disaster_location = (center_lat + 0.00025, center_lon + 0.00025)

# Step 1: Move to spiral start point (e.g., top-left corner of geofence)
start_lat = center_lat + 0.0005
start_lon = center_lon - 0.0005
print("🛫 Flying to entry point at geofence edge...")
vehicle.simple_goto(LocationGlobalRelative(start_lat, start_lon, 15))
time.sleep(10)

# Step 2: Begin spiral search (center is still center_lat/lon)
disaster = spiral_search(
    vehicle=vehicle,
    center_lat=center_lat,
    center_lon=center_lon,
    disaster_location=disaster_location,
    detection_radius=10,
    max_geofence_radius=50  # meters
)

# Step 3: Engage if disaster found
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

# Step 4: Return home
return_to_home(vehicle)
vehicle.close()
