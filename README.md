# Aerobmsce_aerothon

nano /home/pi/drone-mission/env/lib/python3.*/site-packages/dronekit/__init__.py

Traceback (most recent call last):
  File "/home/aadish/drone-mission/main_mission.py", line 1, in <module>
    from connect_vehicle import connect_drone
  File "/home/aadish/drone-mission/connect_vehicle.py", line 1, in <module>
    from dronekit import connect
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/dronekit/__init__.py", line 2689, in <module>
    class Parameters(collections.MutableMapping, HasObservers):
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'collections' has no attribute 'MutableMapping'


Connecting to vehicle on localhost:14550 (SITL/Mission Planner)...
Traceback (most recent call last):
  File "/home/aadish/drone-mission/main_mission.py", line 9, in <module>
    vehicle = connect_drone()
              ^^^^^^^^^^^^^^^
  File "/home/aadish/drone-mission/connect_vehicle.py", line 5, in connect_drone
    return connect('udp:192.168.68.108:14550', wait_ready=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/dronekit/__init__.py", line 3159, in connect
    handler = MAVConnection(ip, baud=baud, source_system=source_system, source_component=source_component, use_native=use_native)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/dronekit/mavlink.py", line 130, in __init__
    self.master = mavutil.mavlink_connection(ip, baud=baud, source_system=source_system, source_component=source_component)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/pymavlink/mavutil.py", line 1888, in mavlink_connection
    return mavudp(device[4:], input=input, source_system=source_system, source_component=source_component, use_native=use_native)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/pymavlink/mavutil.py", line 1055, in __init__
    self.port.bind((a[0], int(a[1])))
OSError: [Errno 99] Cannot assign requested address
