import socket
import threading

HOST = '127.0.0.1'
PORT = 55555
PORT_ONE = 55556
PORT_TWO = 55557

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
server.settimeout(1.0)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '/quit':
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                broadcast(f'{nickname} has left the chat.'.encode('utf-8'))
                break
            elif message == '/list':
                user_list = 'Online users: ' + ', '.join(nicknames)
                client.send(user_list.encode('utf-8'))
            else:
                broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            clients.remove(client)
            nicknames.remove(nickname)
            client.close()
            broadcast(f'{nickname} has left the chat.'.encode('utf-8'))
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of client: {nickname}')
            broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,), daemon=True)
            thread.start()

        except socket.timeout:
            continue

try:
    print('Server is listening...')
    receive()
except KeyboardInterrupt:
    print('\nServer shutting down.')
    server.close()
