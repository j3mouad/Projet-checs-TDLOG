import socket

HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Same port as the C++ server

# Create a socket (IPv4, TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to the server.")

    while True:
        # Receive data from the C++ server
        data = s.recv(1024)
        if not data:
            break
        print("Received from server:", data.decode())

        # Send a response back to the server
        message = "Hello from Python client!"
        s.sendall(message.encode())
