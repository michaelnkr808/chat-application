import socket
import threading

HOST = 'localhost'
PORT = 9999
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
        enter_username = s.recv(1024).decode().strip()
        username = input(enter_username)
        if(username):
            s.send(username.encode())
            enter_username = s.recv(1024).decode().strip()
            if(enter_username.startswith("Welcome")):
                authenticated_username = True
                break
            else:
                print(enter_username)
    #check for valid username
    if(authenticated_username):
        send_thread = threading.Thread(target=send_message, args=(s,))
        send_thread.daemon = True
        send_thread.start()
    while True:
        if(authenticated_username):
            try:
                data = s.recv(1024)
                if not data:
                    print("Client exited successfully")
                    break
                print(data.decode())
                print(PROMPT, end='', flush=True)
            except Exception:
                print("Client exited successfully")
                break
            
       

