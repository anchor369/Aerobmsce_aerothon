# main.py

from drone.connection import connect_drone
from drone.flight_control import takeoff_to_altitude, goto_point
from drone.waypoint_generator import get_tile_size, generate_circular_grid
from camera.vision import (
    init_camera,
    capture_frame,
    detect_objects,
    detect_disaster_and_direction,
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

# Step 1: Connect to drone
vehicle = connect_drone()

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

# Step 6: Perform object detection + disaster logging
disaster_location = None

for lat, lon in waypoints:
    goto_point(vehicle, lat, lon, MISSION_ALTITUDE)
    frame = capture_frame()

    detect_objects(frame)

    if not disaster_location:
        found, direction = detect_disaster_and_direction(frame)
        if found:
            print(f"[SIM] Disaster detected in {direction} direction at ({lat:.6f}, {lon:.6f})")
            disaster_location = (lat, lon)

print("✅ Grid scan complete. Proceeding to payload delivery if needed...")

# Step 7: Go to disaster location and drop payload
if disaster_location:
    print(f"Navigating to stored disaster location: {disaster_location}")
    drop_payload(vehicle, disaster_location[0], disaster_location[1])

# Step 8: Return to launch
print("Returning to launch...")
vehicle.mode = VehicleMode("RTL")

# Step 9: Save log
log_mission_result(object_counts, disaster_location)
vehicle.close()

print("✅ Mission complete.")

