import platform
import os
import shutil
import socket
import subprocess
from pathlib import Path


def command(cmd):
    try:
        return subprocess.check_output(
            cmd, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except:
        return "Unavailable"


print("=" * 50)
print("           MAC SYSTEM INFORMATION")
print("=" * 50)

# System
print("\n--- SYSTEM ---")
print("OS:", platform.system())
print("macOS:", platform.mac_ver()[0])
print("Kernel:", platform.release())
print("Architecture:", platform.machine())
print("Hostname:", socket.gethostname())
print("Computer:", platform.node())

# Mac hardware
print("\n--- HARDWARE ---")
print("Model:", command(["sysctl", "-n", "hw.model"]))
print("Chip:", command(["sysctl", "-n", "machdep.cpu.brand_string"]))
print("CPU cores:", os.cpu_count())
print("Memory:", command(["sysctl", "-n", "hw.memsize"]))

# Memory
print("\n--- MEMORY ---")
memory = command(["sysctl", "-n", "hw.memsize"])
if memory != "Unavailable":
    print("RAM:", round(int(memory) / (1024 ** 3), 2), "GB")

# Disk
print("\n--- STORAGE ---")
disk = shutil.disk_usage("/")
print("Total:", round(disk.total / (1024 ** 3), 2), "GB")
print("Used:", round(disk.used / (1024 ** 3), 2), "GB")
print("Free:", round(disk.free / (1024 ** 3), 2), "GB")

# Network
print("\n--- NETWORK ---")
print("Local IP:", socket.gethostbyname(socket.gethostname()))
print("Wi-Fi:", command(["networksetup", "-getairportnetwork", "en0"]))

# Battery
print("\n--- BATTERY ---")
battery = command(["pmset", "-g", "batt"])
print(battery)

# Display
print("\n--- DISPLAY ---")
display = command(["system_profiler", "SPDisplaysDataType"])
print(display)

# Python
print("\n--- PYTHON ---")
print("Python:", platform.python_version())
print("Python path:", os.path.abspath(os.sys.executable))

# Shell
print("\n--- SHELL ---")
print("Shell:", os.environ.get("SHELL", "Unknown"))

print("\n" + "=" * 50)
print("System scan complete.")
print("=" * 50)
