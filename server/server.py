import socket
import threading
import ssl
from utils.common import HOST, PORT, BUF_SIZE, WELCOME_PREFIX, validate_username, CERT_PATH, KEY_PATH

clients = []
usernames = {}
ERROR_MESSAGES = {
    "empty": "Username cannot be empty.",
    "too_long": "Username max 24 characters.",
    "invalid_chars": "Letters and numbers only",
    "taken": "That username is currently in use."
}

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)

def handle_connections(conn, addr):
    with conn: 
        print("Connected by:", addr)
        #username authentication
        while True:
            try:
                conn.sendall(("Enter your username (max: 24 characters and no symbols): ").encode())
                username = conn.recv(BUF_SIZE).decode()
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
                print(f"{validated_name} has entered the server.")
                conn.sendall((f"{WELCOME_PREFIX}{validated_name}\n").encode())
                break
            except ValueError as e:
                error_code = str(e)
                message = ERROR_MESSAGES.get(error_code, "Invalid username.")
                conn.sendall((message + "\n").encode())
                continue
        #message recieving logic
        while True:
            try:
                data = conn.recv(BUF_SIZE)
                if data.decode().lower() == "quit":
                    clients.remove(conn)
                    if conn in usernames:
                        del usernames[conn]
                    break
                if not data:
                    clients.remove(conn)
                    if conn in usernames:
                        del usernames[conn]
                    break
            except OSError:
                break
            print(f"[{validated_name}]: {data.decode()}")
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
        tls_conn = context.wrap_socket(conn, server_side=True)
        connectThread = threading.Thread(target=handle_connections, args=(tls_conn, addr))
        clients.append(tls_conn)
        connectThread.start()
        


    


    