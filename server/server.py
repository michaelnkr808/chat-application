import socket
import threading
from utils.common import validate_username

HOST = '0.0.0.0'
PORT = 9999
clients = []
usernames = {}
ERROR_MESSAGES = {
    "empty": "Username cannot be empty.",
    "too_long": "Username max 24 characters.",
    "invalid_chars": "Letters only (no numbers or symbols).",
    "taken": "That username is currently in use."
}

def handle_connections(conn, addr):
    with conn: 
        print("Connected by:", addr)
        while True:
            try:
                conn.sendall(("Enter your username (max: 24 characters and no numbers or symbols): ").encode())
                username = conn.recv(1024).decode()
                if not username:
                    clients.remove(conn)
                    if conn in usernames:
                        del usernames[conn]
                    return
                #imported from utils
                validated_name = validate_username(username)
                if any(validated_name == n.lower() for n in usernames.values()):
                    conn.sendall((ERROR_MESSAGES["taken"] + "\n").encode())
                    continue
                usernames[conn] = validated_name
                break
            except ValueError as e:
                error_code = str(e)
                message = ERROR_MESSAGES.get(error_code, "Invalid username.")
                conn.sendall((message + "\n").encode())
                continue
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    clients.remove(conn)
                    if conn in usernames:
                        del usernames[conn]
                    break
            except OSError:
                break
            for client in clients:
                try:
                    client.sendall(f"[{validated_name}]: {data.decode()}".encode())
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
        


    


    