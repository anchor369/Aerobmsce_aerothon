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
