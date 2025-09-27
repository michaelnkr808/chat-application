import socket
import threading
import ssl
import os
from pathlib import Path
from datetime import datetime
from utils.common import HOST, PORT, BUF_SIZE, WELCOME_PREFIX, validate_username, CERT_PATH, KEY_PATH

clients = []
usernames = {}
ERROR_MESSAGES = {
    "empty": "Username cannot be empty.",
    "too_long": "Username max 24 characters.",
    "invalid_chars": "Letters and numbers only",
    "taken": "That username is currently in use."
}
LOG_FILE = None
current_time = datetime.now().strftime("%H:%M:%S")
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)

def check_logs():
    base_dir = Path(__file__).resolve().parents[1]
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir

def create_log(logs_dir: Path):
    run_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_path = logs_dir / f"chat-{run_id}.log"
    log_path.touch(exist_ok=False)
    return str(log_path)

def append_log(line: str):
    if not LOG_FILE:
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding=utf-8) as f:
            f.write(f"{ts}, {line}\n")
    except Exception:
        pass


def handle_connections(conn, addr):
    with conn: 
        print("Connected by:", addr)
        append_log(f"client connected addr={addr[0]}:{addr[1]}")
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
                append_log(f"user authenticated addr={addr[0]}:{addr[1]} user={validated_name}")
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
                    append_log(f"client quit addr={addr[0]}:{addr[1]} user={validated_name}")
                    clients.remove(conn)
                    if conn in usernames:
                        del usernames[conn]
                    break
                if not data:
                    append_log(f"client disconnected addr={addr[0]}:{addr[1]} user={validated_name}")
                    clients.remove(conn)
                    if conn in usernames:
                        del usernames[conn]
                    break
            except OSError:
                break
            data_entry = (f"[{validated_name}]: {data.decode()}")
            append_log(f"msg addr={addr[0]}:{addr[1]} user={validated_name} {data.decode()}")
            print(data_entry)
            for client in clients:
                try:
                    client.sendall(f"[{validated_name}]: {data.decode()}".encode())
                except Exception as e:
                    append_log(f"send failed addr={addr[0]}:{addr[1]} user={validated_name} error={e}")
                    print(f"Error sending to client {e}")
                    client.close()
                    clients.remove(client)
                    del usernames[client] 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen(5)
    logs_dir = check_logs()
    LOG_FILE = create_log(logs_dir)
    while True:
        conn, addr = serversocket.accept()
        tls_conn = context.wrap_socket(conn, server_side=True)
        connectThread = threading.Thread(target=handle_connections, args=(tls_conn, addr))
        clients.append(tls_conn)
        connectThread.start()
        


    


    