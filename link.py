import socket

HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to listen on

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is listening for connections...")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            # Receive data from C++ client
            data = conn.recv(1024)
            if not data:
                break
            print("Received from client:", data.decode())
            
            # Send a response back
            response = "Hello from Python server!"
            conn.sendall(response.encode())
