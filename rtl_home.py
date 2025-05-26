import time
from dronekit import VehicleMode

def return_to_home(vehicle):
    print("Returning to launch (home)...")
    vehicle.mode = VehicleMode("RTL")
    time.sleep(5)
