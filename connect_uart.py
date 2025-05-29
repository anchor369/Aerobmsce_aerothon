from dronekit import connect
import time

def connect_uart_device():
    """
    Establishes a UART connection to Pixhawk from Raspberry Pi using DroneKit.
    Returns the connected vehicle instance.
    """
    uart_port = "/dev/serial0"  # Use /dev/ttyAMA0 or /dev/ttyS0 if needed
    baud_rate = 57600

    print(f"🔌 Connecting to Pixhawk on UART port {uart_port} at {baud_rate} baud...")
    
    try:
        vehicle = connect(uart_port, wait_ready=True, baud=baud_rate)
        print("✅ Connection successful!")
        return vehicle
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

if __name__ == "__main__":
    vehicle = connect_uart_device()
    if vehicle:
        print(f" Mode: {vehicle.mode.name}")
        print(f" GPS: {vehicle.gps_0}")
        print(f" Battery: {vehicle.battery}")
        vehicle.close()
