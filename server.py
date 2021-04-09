import socket
import threading

host = '127.0.0.1'
port = 55555
format = 'ascii'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
client_names = []
chats = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            chats.append(message)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            client_name = client_names[index]
            client_names.remove(client_name)
            broadcast(f'\n {client_name} left the chat!'.encode(format))
            print(f"{client_name} disconnected")
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'New Connection! {address}')

        client.send("name".encode(format))
        client_name = client.recv(1024).decode(format)
        client_names.append(client_name)
        clients.append(client)

        print(f'client name of {address} is {client_name}')
        client.send('successfully connected to the server'.encode(format))
        broadcast(f'{client_name} joined the chat!'.encode(format))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        if threading.activeCount() - 1 == 1:
            client.send(f'\n Welcome {client_name}, You can start a chat when other people connect'.encode(format))
        else:
            print(f"\n {threading.activeCount() - 1} people are connected")
            broadcast(f"{client_names} are in the chat".encode(format))
    
print('server is listening...')
receive()
