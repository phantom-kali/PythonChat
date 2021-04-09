import socket
import threading

host = '127.0.0.1'
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
                print('\n', message)

        except:
            print('An error occurred')
            client.close()
            break


def write():
    while True:
        message = input('>')
        if message == '':
            print('cant send an empty message!')
        else:
            message = (f"{client_name}: {message}")
            client.send(message.encode(format))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
