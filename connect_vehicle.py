from dronekit import connect

def connect_drone():
    print("Connecting to vehicle on localhost:14550 (SITL/Mission Planner)...")
    return connect('127.0.0.1:14550', wait_ready=True)
