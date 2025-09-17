import socket
import threading
from utils.common import HOST, PORT, PROMPT, BUF_SIZE, WELCOME_PREFIX

PROMPT = "Enter a message ('quit' to close): "
authenticated_username = False

def send_message(s):
    while True:
        try:
            message = input(PROMPT)
            s.sendall(message.encode())
            if message == "quit":
                try:
                    s.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                try:
                    s.close()
                except Exception:
                    pass
                break
        except(BrokenPipeError, OSError):
            print("Client exited successfully")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
            
       

