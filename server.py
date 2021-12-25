import os, socket, threading


connections = []


def handleClientConnection(connection, address):

    while True:
        try:
            msg = connection.recv(1024)
        except:
            print(f'{address[0]}:{address[1]} - DISCONNECT')
            removeConnection(connection)
            break

        msg = msg.decode()
        
        if msg == "exit":
            print(f'{address[0]}:{address[1]} - DISCONNECT')
            removeConnection(connection)
            break
        elif msg !="":
            print(f'{address[0]}:{address[1]} - {msg}')
            
            mess = f'From {address[0]}:{address[1]} - {msg}'
            broadcast(mess, connection)

def broadcast(message: str, connection: socket.socket) -> None:
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                client_conn.send(message.encode())
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)
                
def removeConnection(connect):
    if connect in connections:
        connect.close()
        connections.remove(connect)


def server():
    local_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip.connect(("8.8.8.8", 80))
    SERVER_ADDRESS = local_ip.getsockname()[0]

    port = input("Input port: ")
    PORT = int(str(port))
    
    try:
        print("Initialize...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((SERVER_ADDRESS, PORT))
        sock.listen(4)
        print("Listening...")
        
        print('Server running ip ( ' + SERVER_ADDRESS + ') port(' + str(PORT) + ')')
        print("Waiting for connection...")
        
        while True:
            socket_connection, address = sock.accept()

            connections.append(socket_connection)
            print(f'{address[0]}:{address[1]} - CONNECT')
            serverThread = threading.Thread(target=handleClientConnection, args=[socket_connection, address])
            serverThread.start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
       
        if len(connections) > 0:
            for conn in connections:
                removeConnection(conn)

        sock.close()

if __name__ == "__main__":
    server()
