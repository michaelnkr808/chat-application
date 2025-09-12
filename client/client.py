import socket
import threading

HOST = ''
PORT = 9999

def send_message(s):
    while True:
        message = input("Enter a message ('quit') to close): ")
        s.sendall(message.encode())
        if message == "quit":
            try:
                s.close()
            except Exception:
                print("Client excited successfully") 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    enter_username = s.recv(1024).decode()
    print(enter_username)
    send_thread = threading.Thread(target=send_message, args=(s,))
    send_thread.start()
    while True:
        try:
            print(s.recv(1024).decode())
        except Exception:
            print("Client exited successfully")
            break
        
       

