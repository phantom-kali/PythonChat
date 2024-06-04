import socket
import threading
import sqlite3
import base64

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = {}

        self.init_db()

    def init_db(self):
        self.conn = sqlite3.connect('chat_server.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (username TEXT PRIMARY KEY,
                             password TEXT)''')
        self.conn.commit()

    def register_user(self, username, password):
        conn = sqlite3.connect('chat_server.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def verify_user(self, username, password):
        conn = sqlite3.connect('chat_server.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone() is not None
        conn.close()
        return result

    def broadcast(self, message, sender_socket):
        for client_socket in self.clients.values():
            if client_socket != sender_socket:
                try:
                    encrypted_message = self.encrypt_message(message)
                    client_socket.send(encrypted_message)
                except Exception as e:
                    print(f"Failed to send message to {client_socket}: {e}")

    def encrypt_message(self, message):
        message_bytes = message.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes

    def decrypt_message(self, encrypted_message):
        base64_bytes = encrypted_message
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('utf-8')

    def handle_client(self, client_socket):
        try:
            while True:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break

                message = self.decrypt_message(encrypted_message)
                if message.startswith("register|"):
                    _, username, password = message.split("|")
                    if self.register_user(username, password):
                        client_socket.send(self.encrypt_message("register|success"))
                    else:
                        client_socket.send(self.encrypt_message("register|failure"))
                elif message.startswith("login|"):
                    _, username, password = message.split("|")
                    if self.verify_user(username, password):
                        if username in self.clients:
                            client_socket.send(self.encrypt_message("login|success"))
                            self.update_users()
                        else:
                            self.clients[username] = client_socket
                            client_socket.send(self.encrypt_message("login|success"))
                            self.update_users()
                    else:
                        client_socket.send(self.encrypt_message("login|failure"))
                else:
                    self.broadcast(message, client_socket)
        except Exception as e:
            print(f"Client handling error: {e}")
        finally:
            for username, socket in self.clients.items():
                if socket == client_socket:
                    del self.clients[username]
                    break
            client_socket.close()
            self.update_users()

    def update_users(self):
        user_list = "update_users|" + ",".join(self.clients.keys())
        for client_socket in self.clients.values():
            try:
                encrypted_message = self.encrypt_message(user_list)
                client_socket.send(encrypted_message)
            except Exception as e:
                print(f"Failed to update user list: {e}")

    def start(self):
        print("Server started")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
