import socket

host = input("Host: ")
port = int(input("Port: "))

sock = socket.socket()
sock.settimeout(2)

try:
    sock.connect((host, port))
    print("Port is open")
except:
    print("Port is closed or unreachable")
finally:
    sock.close()