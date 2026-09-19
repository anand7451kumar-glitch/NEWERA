import platform
import os
print("System:", platform.system())
print("macOS:", platform.mac_ver()[0])
print("Processor:", platform.processor())
print("CPU cores:", os.cpu_count())
print("Computer:", platform.machine())
