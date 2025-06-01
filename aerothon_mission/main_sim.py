# main.py

from drone.connection import connect_drone
from drone.flight_control import takeoff_to_altitude, goto_point
from drone.waypoint_generator import get_tile_size, generate_circular_grid
from camera.vision import (
    init_camera,
    capture_frame,
    detect_objects,
    object_counts,
)
from payload.drop_control import drop_payload
from utils.logger import log_mission_result
from config import (
    MISSION_ALTITUDE,
    GEOFENCE_CENTER,
    GEOFENCE_RADIUS_M,
    CAMERA_HFOV,
    CAMERA_VFOV,
)
from dronekit import VehicleMode

# Hardcoded disaster coordinates (inside geofence)
disaster_location = (12.97185, 77.59475)  # You can adjust this

# Step 1: Connect to drone
vehicle = connect_drone()
# ✅ Get real-time GPS coordinates from SITL
GEOFENCE_CENTER = (
    vehicle.location.global_frame.lat,
    vehicle.location.global_frame.lon
)
# Step 2: Initialize camera
init_camera()

# Step 3: Takeoff
takeoff_to_altitude(vehicle, MISSION_ALTITUDE)

# Step 4: Generate grid waypoints
tile_w, tile_h = get_tile_size(MISSION_ALTITUDE, CAMERA_HFOV, CAMERA_VFOV)
waypoints = generate_circular_grid(GEOFENCE_CENTER, GEOFENCE_RADIUS_M, tile_w, tile_h)

# Step 5: Enter geofence
entry_point = waypoints[0]
print(f"Navigating to geofence entry point at {entry_point}")
goto_point(vehicle, entry_point[0], entry_point[1], MISSION_ALTITUDE)

# Step 6: Perform full object detection sweep
for lat, lon in waypoints:
    goto_point(vehicle, lat, lon, MISSION_ALTITUDE)
    frame = capture_frame()
    detect_objects(frame)

print("✅ Grid scan complete. Proceeding to hardcoded disaster location...")

# Step 7: Navigate to hardcoded disaster location and drop payload
drop_payload(vehicle, disaster_location[0], disaster_location[1])

# Step 8: Return to launch
print("Returning to launch...")
vehicle.mode = VehicleMode("RTL")

# Step 9: Save result log
log_mission_result(object_counts, disaster_location)

vehicle.close()
print("✅ Mission complete.")
