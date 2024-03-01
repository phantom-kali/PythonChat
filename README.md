Chat Application Documentation

Client (client.py)

Overview:

    The client.py script represents the client side of a simple chat application.

Dependencies:

    The script uses the socket module for networking.
    It employs multi-threading to simultaneously handle message reception and user input.

Connection:

    The client connects to a server using the specified host and port.

User Input:

    The user is prompted to choose a name (client_name) before connecting to the server.

Message Reception (receive Function):

    Continuously listens for incoming messages from the server.
    When a message is received, it is decoded and displayed.
    If the message is a request for the client's name, it sends the chosen name to the server.

Message Sending (write Function):

    Allows the user to input messages.
    Messages are sent to the server with the user's name.

Server (server.py)

Overview:

    The server.py script represents the server side of the chat application.

Dependencies:

    The script uses the socket module for networking.
    It utilizes multi-threading to handle multiple client connections concurrently.

Connection:

    The server binds to the specified host and port and listens for incoming connections.

Client Management:

    Keeps track of connected clients, their names, and the chat history.

Broadcasting (broadcast Function):

    Sends a message to all connected clients.

Client Handling (handle Function):

    Listens for messages from a specific client.
    Adds received messages to the chat history.
    Broadcasts the message to all clients.

Connection Handling (receive Function):

    Accepts new client connections.
    Sends a request for the client's name.
    Adds the client to the list of connected clients.
    Starts a thread to handle communication with the new client.

Welcome Message:

    Welcomes the first connected client with a special message.

User Interaction:

    Displays messages about clients joining and leaving the chat.

Usage:

Starting the Server:


```python server.py```

Connecting Clients:

    Run multiple instances of client.py to simulate multiple clients connecting to the server.

```python client.py```

Chatting:

    Clients can send and receive messages in the chat.
