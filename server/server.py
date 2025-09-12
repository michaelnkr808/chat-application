import socket
import threading

HOST = ''
PORT = 9999
clients = []
usernames = {}

def handle_connections(conn, addr):
    with conn: 
        print("Connected by:", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                clients.remove(conn)
                break
            for client in clients:
                try:
                    client.sendall(data)
                except Exception as e:
                    print(f"Error sending to client {e}")
                    client.close()
                    clients.remove(client)
def retrieve_username(conn):
    username = input("Enter your usernmae: ")
    with conn:
        conn.send(username)
        
        


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen(5)
    while True: 
        conn, addr = serversocket.accept()
        connectThread = threading.Thread(target=handle_connections, args=(conn, addr))
        connectThread.start()
        clients.append(conn)
        


    


    