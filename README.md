Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 mono-complete : Depends: mono-runtime (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-runtime-sgen (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-utils (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-devel (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-mcs (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-csharp-shell (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-4.0-gac (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-4.0-service (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: monodoc-base (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: monodoc-manual (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: libmono-cil-dev (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: ca-certificates-mono (= 6.8.0.105+dfsg-3.3) but it is not going to be installed

sudo apt install gnupg ca-certificates -y
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF

echo "deb https://download.mono-project.com/repo/debian stable-raspbian$(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/mono-official.list

deb https://download.mono-project.com/repo/debian stable-raspbianbookworm main

dronekit-sitl copter --home=12.9716,77.5946,15,90 --model quad --out=udp:<your-windows-ip>:14550

dronekit-sitl copter --home=12.9716,77.5946,15,90 --model quad --out=udp::14550os: linux, apm: copter, release: stable
SITL already Downloaded and Extracted.
Ready to boot.
Traceback (most recent call last):
  File "/home/aadish/drone-mission/drone/bin/dronekit-sitl", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/dronekit_sitl/__init__.py", line 601, in main
    sitl.launch(args, verbose=True)
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/dronekit_sitl/__init__.py", line 251, in launch
    caps = ArdupilotCapabilities(self.path)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aadish/drone-mission/drone/lib/python3.11/site-packages/dronekit_sitl/__init__.py", line 160, in __init__
    process = subprocess.Popen([path, '--help'], stdout=subprocess.PIPE)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/subprocess.py", line 1024, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/usr/lib/python3.11/subprocess.py", line 1901, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
OSError: [Errno 8] Exec format error: '/home/aadish/.dronekit/sitl/copter-3.3/apm'


cat > ~/start_sitl_network.sh << 'EOF'
#!/bin/bash

# Replace with your Windows PC IP
WINDOWS_PC_IP="192.168.1.100"  # Change this to your actual Windows IP
RASPI_IP=$(hostname -I | awk '{print $1}')

echo "🚁 Starting SITL on Raspberry Pi"
echo "📡 Raspberry Pi IP: $RASPI_IP"
echo "💻 Windows PC IP: $WINDOWS_PC_IP"

# Kill existing processes
pkill -f sitl
pkill -f sim_vehicle
sleep 2

# Start SITL with multiple outputs
cd ~/ardupilot/ArduCopter
python3 sim_vehicle.py \
    --aircraft test \
    --console \
    --out udp:127.0.0.1:14550 \
    --out udp:$WINDOWS_PC_IP:14550 \
    --home=12.9716,77.5946,15,90

EOF

chmod +x ~/start_sitl_network.sh


from dronekit import connect
import time
import socket

def get_local_ip():
    """Get the local IP address of Raspberry Pi"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def connect_drone(connection_string=None):
    if connection_string is None:
        connection_string = '127.0.0.1:14550'  # Local connection on Raspberry Pi
    
    print(f"🔗 Connecting to vehicle on {connection_string}...")
    
    for attempt in range(5):
        try:
            vehicle = connect(connection_string, wait_ready=True, timeout=30)
            print("✅ Connected successfully!")
            print(f"📊 Vehicle mode: {vehicle.mode}")
            print(f"🔋 Battery: {vehicle.battery}")
            print(f"📍 Location: {vehicle.location.global_frame}")
            return vehicle
        except Exception as e:
            print(f"❌ Connection attempt {attempt + 1} failed: {e}")
            if attempt < 4:
                print("⏳ Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("💡 Make sure SITL is running: ./start_sitl_network.sh")
                raise

def connect_drone_for_mission_control():
    """Alternative connection for when Mission Control is primary"""
    local_ip = get_local_ip()
    connection_string = f'{local_ip}:14551'  # Different port to avoid conflicts
    return connect_drone(connection_string)
