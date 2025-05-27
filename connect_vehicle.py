from dronekit import connect

def connect_drone():
	print("🔌 Connecting to SITL on UDP port 14550...")

	# Use TCP connection for ArduPilot SITL
	vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
	print("✅ Connected to simulated drone!")
	return vehicle
