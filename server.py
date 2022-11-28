import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080

# Create socket (ipv4 + stream)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket to 127.0.0.1 (localhost) on port 8080
    s.bind((HOST, PORT))
    # Listen to bound socket for connection
    s.listen(1)
    while True:
        try:
            # Wait for connection
            conn, addr = s.accept()
            print("Connection from", addr)
            while True:
                data = conn.recv(2048)
                now = datetime.now()
                if not data:
                    break
                with open("logger.log", 'a') as f:
                    f.write('{}	{}\n'.format(now, str(data.decode())))

                conn.sendall(data)
        finally:
            conn.close()