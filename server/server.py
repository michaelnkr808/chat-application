import socket
import threading

HOST = '0.0.0.0'
PORT = 9999
clients = []
usernames = {}

def handle_connections(conn, addr):
    with conn: 
        print("Connected by:", addr)
        conn.send(("Enter your username: ").encode())
        username = conn.recv(1024).decode().strip()
        usernames[conn] = username
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    clients.remove(conn)
                    break
            except OSError:
                break
            for client in clients:
                try:
                    client.sendall(f"[{username}]: {data.decode()}".encode())
                except Exception as e:
                    print(f"Error sending to client {e}")
                    client.close()
                    clients.remove(client)
                    del usernames[client] 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen(5)
    while True: 
        conn, addr = serversocket.accept()
        connectThread = threading.Thread(target=handle_connections, args=(conn, addr))
        clients.append(conn)
        connectThread.start()
        


    


    