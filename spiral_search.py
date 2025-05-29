import math
import time
from dronekit import LocationGlobalRelative
from camera_disaster_detector import detect_disaster_and_direction


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_offset_location(vehicle, direction, offset_meters):
    """
    Shift the current vehicle position based on detected direction in camera view.
    LEFT/RIGHT = longitude change, CENTER = forward (latitude increase).
    """
    lat = vehicle.location.global_relative_frame.lat
    lon = vehicle.location.global_relative_frame.lon
    offset_deg = offset_meters / 111111  # ~111111 meters per degree latitude

    if direction == "left":
        return LocationGlobalRelative(lat, lon - offset_deg, 15)
    elif direction == "right":
        return LocationGlobalRelative(lat, lon + offset_deg, 15)
    elif direction == "center":
        return LocationGlobalRelative(lat + offset_deg, lon, 15)
    else:
        return LocationGlobalRelative(lat, lon, 15)


def spiral_search(vehicle, center_lat, center_lon, detection_radius, max_geofence_radius, camera):
    """
    Perform inward spiral search from outer geofence.
    Use YOLO-based detection to divert to disaster if seen.
    """
    print("🌀 Starting inward spiral search with camera-based detection...")

    step_angle = math.pi / 6  # 30° per step (12 points per loop)
    i = 0
    disaster_found = None
    visited = set()

    r = max_geofence_radius / 111111  # Convert meters to approx degrees

    while r > 0.00005:
        angle = i * step_angle
        lat = center_lat + r * math.cos(angle)
        lon = center_lon + r * math.sin(angle)

        distance_from_center = haversine_distance(center_lat, center_lon, lat, lon)
        if distance_from_center > max_geofence_radius:
            i += 1
            continue

        coord_key = (round(lat, 6), round(lon, 6))
        if coord_key in visited:
            i += 1
            continue
        visited.add(coord_key)

        point = LocationGlobalRelative(lat, lon, 15)
        print(f"[{i+1}] Goto: ({lat:.6f}, {lon:.6f}) | Radius: {distance_from_center:.2f}m")
        vehicle.simple_goto(point)
        time.sleep(4)

        # 🔍 Real-time disaster detection using camera
        detected, direction = detect_disaster_and_direction(camera)
        if detected:
            print(f"🚨 Disaster detected in direction: {direction.upper()}")
        
            # Ensure we're in GUIDED mode
            from dronekit import VehicleMode
            vehicle.mode = VehicleMode("GUIDED")
            time.sleep(1)
        
            target_location = get_offset_location(vehicle, direction, 10)
            print(f"🚁 Redirecting to: {target_location.lat:.6f}, {target_location.lon:.6f}")
            vehicle.simple_goto(target_location)
            time.sleep(4)
        
            current = vehicle.location.global_relative_frame
            disaster_found = (current.lat, current.lon)
            break

        if (i + 1) % 12 == 0:
            r *= 0.9  # shrink spiral after each full loop
        i += 1

    if not disaster_found:
        print("✅ Spiral search complete. No disaster detected.")
    return disaster_found
