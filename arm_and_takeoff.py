from dronekit import VehicleMode
import time

def arm_and_takeoff(vehicle, target_altitude):
    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(" Altitude:", alt)
        if alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
