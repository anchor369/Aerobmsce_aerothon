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

# Step 1: Connect to vehicle
vehicle = connect_drone()

# Step 2: Initialize camera
init_camera()

# Step 3: Takeoff to mission altitude
takeoff_to_altitude(vehicle, MISSION_ALTITUDE)

# Step 4: Generate grid waypoints within the circular geofence
tile_w, tile_h = get_tile_size(MISSION_ALTITUDE, CAMERA_HFOV, CAMERA_VFOV)
waypoints = generate_circular_grid(GEOFENCE_CENTER, GEOFENCE_RADIUS_M, tile_w, tile_h)

# Step 5: Navigate to entry point of the geofence (first waypoint)
entry_point = waypoints[0]
print(f"Navigating to geofence entry point at {entry_point}")
goto_point(vehicle, entry_point[0], entry_point[1], MISSION_ALTITUDE)

# Step 6: Begin grid search with object detection and disaster monitoring
disaster_location = None

for lat, lon in waypoints:
    goto_point(vehicle, lat, lon, MISSION_ALTITUDE)
    frame = capture_frame()

    detect_objects(frame)

    if not disaster_location:
        found, direction = detect_disaster_and_direction(frame)
        if found:
            print(f"Disaster detected in {direction} direction.")
            disaster_location = (lat, lon)

# Step 7: Drop payload if disaster detected
if disaster_location:
    print("Navigating to disaster location for payload drop...")
    drop_payload(vehicle, disaster_location[0], disaster_location[1])

# Step 8: Return to launch point
print("Returning to launch...")
vehicle.mode = VehicleMode("RTL")

# Step 9: Log mission results
log_mission_result(object_counts, disaster_location)

vehicle.close()
print("Mission complete.")
