import socket
import tkinter as tk
import base64
from tkinter import messagebox
import threading

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration/Login")
        self.client = ChatClient()

        self.BG_COLOR = "#17202A"
        self.TEXT_COLOR = "#EAECEE"
        self.FONT = "Helvetica 14"
        self.FONT_BOLD = "Helvetica 13 bold"

        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.form_frame = tk.Frame(root, bg=self.BG_COLOR)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = tk.Label(self.form_frame, text="Registration/Login", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.register_button = tk.Button(self.form_frame, text="Register", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.show_registration_form)
        self.register_button.grid(row=1, column=0, padx=10, pady=5)

        self.login_button = tk.Button(self.form_frame, text="Login", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.show_login_form)
        self.login_button.grid(row=1, column=1, padx=10, pady=5)

        self.show_main_screen()

    def clear_form_frame(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def show_main_screen(self):
        self.clear_form_frame()

        self.title_label = tk.Label(self.form_frame, text="Registration/Login", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.register_button = tk.Button(self.form_frame, text="Register", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.show_registration_form)
        self.register_button.grid(row=1, column=0, padx=10, pady=5)

        self.login_button = tk.Button(self.form_frame, text="Login", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.show_login_form)
        self.login_button.grid(row=1, column=1, padx=10, pady=5)

    def show_registration_form(self):
        self.clear_form_frame()

        self.registration_form = tk.Frame(self.form_frame, bg=self.BG_COLOR)
        self.registration_form.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.reg_username_label = tk.Label(self.registration_form, text="Username:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT_BOLD)
        self.reg_username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.reg_username_entry = tk.Entry(self.registration_form, bg=self.TEXT_COLOR, fg=self.BG_COLOR, font=self.FONT)
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.reg_password_label = tk.Label(self.registration_form, text="Password:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT_BOLD)
        self.reg_password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.reg_password_entry = tk.Entry(self.registration_form, bg=self.TEXT_COLOR, fg=self.BG_COLOR, font=self.FONT, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.register_submit_button = tk.Button(self.registration_form, text="Register", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.register_user)
        self.register_submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.back_button = tk.Button(self.form_frame, text="Back", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.show_main_screen)
        self.back_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def show_login_form(self):
        self.clear_form_frame()

        self.login_form = tk.Frame(self.form_frame, bg=self.BG_COLOR)
        self.login_form.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.login_username_label = tk.Label(self.login_form, text="Username:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT_BOLD)
        self.login_username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.login_username_entry = tk.Entry(self.login_form, bg=self.TEXT_COLOR, fg=self.BG_COLOR, font=self.FONT)
        self.login_username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.login_password_label = tk.Label(self.login_form, text="Password:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT_BOLD)
        self.login_password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.login_password_entry = tk.Entry(self.login_form, bg=self.TEXT_COLOR, fg=self.BG_COLOR, font=self.FONT, show="*")
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_submit_button = tk.Button(self.login_form, text="Login", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.login_user)
        self.login_submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.back_button = tk.Button(self.form_frame, text="Back", font=self.FONT_BOLD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, command=self.show_main_screen)
        self.back_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def register_user(self):
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()

        if username and password:
            try:
                self.client.connect()
                self.client.send_message(f"register|{username}|{password}")
                response = self.client.receive_message()
                if response == "register|success":
                    tk.messagebox.showinfo("Registration", "Registration successful! Please log in.")
                    self.show_login_form()
                else:
                    tk.messagebox.showerror("Registration", "Username already taken. Please try again.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to register: {e}")
        else:
            tk.messagebox.showerror("Input Error", "Username and password cannot be empty.")

    def login_user(self):
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get().strip()

        if username and password:
            try:
                if not self.client.is_connected():
                    self.client.connect()
                self.client.send_message(f"login|{username}|{password}")
                response = self.client.receive_message()
                if response == "login|success":
                    self.root.destroy()
                    self.client.username = username
                    self.client.start_chat()
                else:
                    tk.messagebox.showerror("Login", "Invalid username or password. Please try again.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to login: {e}")
        else:
            tk.messagebox.showerror("Input Error", "Username and password cannot be empty.")

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000, username="User"):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = None  # Changed to None initially
        self.active_chat_user = None

    def connect(self):
        if self.client_socket is None:  # Check if socket is None
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
    
    def is_connected(self):
        return self.client_socket is not None and self.client_socket.fileno() != -1

    def send_message(self, message):
        encrypted_message = self.encrypt_message(message)
        self.client_socket.send(encrypted_message)

    def receive_message(self):
        encrypted_message = self.client_socket.recv(1024)
        return self.decrypt_message(encrypted_message)

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                message = self.decrypt_message(encrypted_message)
                if message.startswith("update_users|"):
                    users = message.split("|")[1].split(",")
                    self.chat_app.update_user_list_and_highlight(users)
                else:
                    sender, content = message.split(": ", 1)
                    self.chat_app.display_message(message)
                    if self.active_chat_user != sender:
                        idx = self.chat_app.user_list.get(0, tk.END).index(sender)
                        self.chat_app.user_list.itemconfig(idx, {'bg': 'green'})
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def start_chat(self):
        self.root = tk.Tk()
        self.chat_app = ChatApp(self.root, self)
        self.chat_app.user_list.bind("<Double-Button-1>", self.chat_app.select_user)
        self.chat_app.start_listening()
        self.root.mainloop()

    def encrypt_message(self, message):
        message_bytes = message.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes

    def decrypt_message(self, encrypted_message):
        base64_bytes = encrypted_message
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('utf-8')

class ChatApp:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title(f"Chat - {self.client.username}")

        self.BG_GRAY = "#ABB2B9"
        self.BG_COLOR = "#17202A"
        self.TEXT_COLOR = "#EAECEE"
        self.OTHER_TEXT_COLOR = "#7FFF00"
        self.FONT = "Helvetica 14"
        self.FONT_BOLD = "Helvetica 13 bold"

        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Initialize active_chat_label attribute
        self.active_chat_label = tk.Label(root, text="Chat with: None", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT_BOLD)
        self.active_chat_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.chat_text = tk.Text(self.root, bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT, state=tk.DISABLED)
        self.chat_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.entry = tk.Entry(self.root, bg="#2C3E50", fg=self.TEXT_COLOR, font=self.FONT)
        self.entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.send_button = tk.Button(self.root, text="Send", font=self.FONT_BOLD, bg=self.BG_GRAY, command=self.send)
        self.send_button.grid(row=2, column=1, padx=10, pady=10)

        self.user_list_label = tk.Label(self.root, text="Online Users", bg=self.BG_GRAY, fg=self.TEXT_COLOR, font=self.FONT_BOLD)
        self.user_list_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.user_list = tk.Listbox(self.root, bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT)
        self.user_list.grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky="ns")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.client.connect()
    
    def select_user(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            user = widget.get(index)
            self.client.active_chat_user = user
            self.active_chat_label.config(text=f"Chat with: {user}")
            self.entry.config(state=tk.NORMAL)
            self.entry.focus()

            self.user_list.itemconfig(index, {'bg': self.BG_COLOR})
    
    def start_listening(self):
        listening_thread = threading.Thread(target=self.client.receive_messages)
        listening_thread.daemon = True
        listening_thread.start()

    def send(self):
        message = self.entry.get().strip()
        if message:
            full_message = f"{self.client.username}: {message}"
            self.client.send_message(full_message)
            self.display_message(full_message)
            self.entry.delete(0, tk.END)

    def display_message(self, message):
        print(message)
        sender, content = message.split(": ", 1)
        self.chat_text.config(state=tk.NORMAL)

        if sender == self.client.username:
            self.chat_text.insert(tk.END, f"You: {content}\n", "user")
            self.chat_text.tag_config("user", foreground=self.TEXT_COLOR)
        else:
            self.chat_text.insert(tk.END,  f"{sender}: {content}\n", "other")
            self.chat_text.tag_config("other", foreground=self.OTHER_TEXT_COLOR)
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

    def update_user_list_and_highlight(self, users):
        self.user_list.delete(0, tk.END)
        for user in users:
            self.user_list.insert(tk.END, user)

            if self.client.active_chat_user != user:
                self.user_list.itemconfig(tk.END, {'bg': self.BG_COLOR})
        
        self.active_chat_label.config(text=f"Chat with: {self.client.active_chat_user or 'None'}")
        self.entry.config(state=tk.NORMAL if self.client.active_chat_user else tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()
