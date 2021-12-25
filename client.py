import socket, threading

def handle_messages(connection):
    while True:
        try:
        
            msg = connection.recv(1024)
        except:
            connection.close()
            break

        msg = msg.decode()
        if msg !="":
            print(msg)

def client():

    SERVER_ADDRESS = input('Enter server address: ')
    SERVER_PORT = int(input('Enter port number: '))

    try:
        client = socket.socket()
        client.connect((SERVER_ADDRESS, SERVER_PORT))

        thread = threading.Thread(target=handle_messages, args=[client])
        thread.start()

        print('Connected to server successful')

        while True:
            msg = input("Input text:")
            

            if msg == 'exit':
                client.send(msg.encode())
                break
            client.send(msg.encode())

        client.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        client.close()


if __name__ == "__main__":
    client()
