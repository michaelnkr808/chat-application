import socket
import threading

HOST = ''
PORT = 9999

def handleConnections(conn, addr):
    with conn: 
        print("Connected by:", addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen(5)
    while True: 
        conn, addr = serversocket.accept()
        connectThread = threading.Thread(target=handleConnections, args=(conn, addr))
        connectThread.start()

    


    