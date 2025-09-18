import socket
import threading
from datetime import datetime
import sys
import ssl
from utils.common import HOST, PORT, PROMPT, BUF_SIZE, WELCOME_PREFIX, SERVER_HOSTNAME, CERT_PATH

authenticated_username = False

def send_message(s):
    while True:
        try:
            datetime_sent = datetime.now().strftime("%H:%M:%S")
            message_content = input()
            full_message = (f"[{datetime_sent}] " + f"{message_content}")
            if message_content.strip() == "":
                continue
            if message_content.strip().lower() == "quit":
                try:
                    s.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                try:
                    s.close()
                except Exception:
                    pass
                break
            else:
                s.sendall(full_message.encode())
                sys.stdout.write("\r")
                sys.stdout.write("\x1b[1A")
                sys.stdout.write("\x1b[2K")
                sys.stdout.flush()
        except(BrokenPipeError, OSError):
            print("Client exited successfully")
            break

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_verify_locations(CERT_PATH)

with ssl_context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=SERVER_HOSTNAME) as s:
    s.connect((HOST, PORT))
    while True:
        enter_username = s.recv(BUF_SIZE).decode().strip()
        username = input(enter_username)
        while username.strip() == "":
            username = input(enter_username)
        if(username):
            s.send(username.encode())
            response = s.recv(BUF_SIZE).decode().strip()
            if(response.startswith(WELCOME_PREFIX)):
                authenticated_username = True
                break
            else:
                print(response)
    #check for valid username
    if(authenticated_username):
        print(PROMPT, end="", flush=True)
        send_thread = threading.Thread(target=send_message, args=(s,))
        send_thread.daemon = True
        send_thread.start()
    while True:
        if(authenticated_username):
            try:
                data = s.recv(BUF_SIZE)
                if not data:
                    print("Client exited successfully")
                    break
                print(data.decode())
            except Exception:
                print("Client exited successfully")
                break
            
       

