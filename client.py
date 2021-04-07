import socket
import threading

host = '102.135.170.121'
port = 55555
format = 'ascii'

client_name = input('Choose a name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode(format)
            if message == 'name':
                client.send(client_name.encode(format))
            else:
                print(message)

        except:
            print('An error occurred')
            client.close()
            break


def write():
    while True:
        message = f'{client_name} : {input(f"{client_name}> ")}'
        client.send(message.encode(format))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
