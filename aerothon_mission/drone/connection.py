def connect_drone():
    print("🔗 Connecting to drone...")
    vehicle = connect(CONNECTION_STRING, wait_ready=True)
    print("✅ Drone connected.")

    # 🛠️ Bypass arming check (only in SITL)
    vehicle.parameters['ARMING_CHECK'] = 0

    # 🛰️ Set fake starting position (only in simulation)
    from pymavlink import mavutil
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,  # type_mask: only lat/lon/alt enabled
        int(12.9716 * 1e7),   # lat (degrees * 1e7)
        int(77.5946 * 1e7),   # lon
        30,     # alt (meters)
        0, 0, 0, 0, 0, 0, 0, 0
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

    return vehicle
