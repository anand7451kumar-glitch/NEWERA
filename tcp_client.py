import socket

client = socket.socket()
client.connect(("127.0.0.1", 5000))

while True:
    message = input("You: ")

    if message.lower() == "exit":
        break

    client.send(message.encode())

    reply = client.recv(1024).decode()
    print("Server:", reply)

client.close()
