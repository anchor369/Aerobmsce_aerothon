# drone/connection.py

from dronekit import connect
from config import CONNECTION_STRING

def connect_drone():
    """
    Connect to the drone using the given connection string.
    Returns the vehicle object.
    """
    print("🔗 Connecting to drone...")
    vehicle = connect(CONNECTION_STRING, wait_ready=True)
    print("✅ Drone connected.")
    return vehicle
