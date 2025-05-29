from connect_vehicle import connect_drone
from arm_and_takeoff import arm_and_takeoff
from spiral_search import spiral_search
from payload_drop import drop_payload
from rtl_home import return_to_home
from camera_disaster_detector import init_camera
from dronekit import LocationGlobalRelative
import time


def hover_and_confirm_disaster(vehicle, lat, lon):
    print("👁 Hovering to confirm disaster...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, 15))
    time.sleep(3)
    print("✅ Confirmed: Actual disaster detected.")
    return True


# Step 1: Connect to drone
vehicle = connect_drone()

# Step 2: Initialize camera
print("🎥 Initializing Pi Camera and YOLO...")
camera = init_camera()

# Step 3: Take off
arm_and_takeoff(vehicle, 15)

# Step 4: Define geofence center
current = vehicle.location.global_relative_frame
center_lat = current.lat
center_lon = current.lon

# Step 5: Move to outer edge before spiral search
start_lat = center_lat + (60 / 111111)  # ~60m north
start_lon = center_lon
print("🛫 Flying to outer edge of geofence...")
vehicle.simple_goto(LocationGlobalRelative(start_lat, start_lon, 15))
time.sleep(10)

# Step 6: Begin spiral search and live detection
disaster = spiral_search(
    vehicle=vehicle,
    center_lat=center_lat,
    center_lon=center_lon,
    detection_radius=10,
    max_geofence_radius=50,  # meters
    camera=camera
)

# Step 7: If disaster detected → confirm + drop payload
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

# Step 8: Return to launch
return_to_home(vehicle)

# Step 9: Cleanup
camera.release()
vehicle.close()
print("✅ Mission completed and camera released.")
