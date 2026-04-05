import socket
import threading

nickname = input('Choose your nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

quitting = False

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            if not quitting:
                print('An error occurred!')
            client.close()
            break

def write():
    global quitting
    while True:
        try:
            message = input('')
            if message.lower() == '/quit':
                quitting = True
                client.send('/quit'.encode('utf-8'))
                print('You left the chat.')
                client.close()
                break
            elif message.lower() == '/list':
                client.send('/list'.encode('utf-8'))
            else:
                client.send(f'{nickname}: {message}'.encode('utf-8'))
        except (EOFError, KeyboardInterrupt):
            quitting = True
            client.close()
            break

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

write_thread = threading.Thread(target=write, daemon=True)
write_thread.start()

write_thread.join()