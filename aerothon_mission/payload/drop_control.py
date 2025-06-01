# payload/drop_control.py

import time
from dronekit import LocationGlobalRelative
from config import DROP_ALTITUDE, MISSION_ALTITUDE

def drop_payload(vehicle, lat, lon):
    """
    Simulate payload drop by descending to drop altitude and climbing back.
    """
    print("🛰 Navigating to payload drop point...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, MISSION_ALTITUDE))
    time.sleep(5)

    print("🛬 Descending to drop altitude...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, DROP_ALTITUDE))
    time.sleep(5)

    # Simulated drop
    print("🎯 Payload dropped!")

    print("🛫 Climbing back to mission altitude...")
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, MISSION_ALTITUDE))
    time.sleep(5)

    print("✅ Drop sequence completed.")
