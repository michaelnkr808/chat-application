import socket

HOST = ''
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen(5)
    conn, addr = serversocket.accept()
    with conn: 
        print("Connected by:", addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
    