import socket

server = socket.socket()
server.bind(("0.0.0.0", 5000))
server.listen(1)

print("Waiting for connection...")

client, address = server.accept()
print("Connected:", address)

while True:
    message = client.recv(1024).decode()

    if not message:
        break

    print("Client:", message)

    reply = input("You: ")
    client.send(reply.encode())

client.close()
server.close()
