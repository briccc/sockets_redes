import socket
import threading

clients = {}
usernames = {}

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        clients[client_socket] = username
        client_socket.send(f"Te has conectado como {username}.\n".encode('utf-8'))

        welcome_message = f"{username} se ha unido al chat."
        broadcast(welcome_message, exclude_client=client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                raise ConnectionResetError
            
            if message == '/listar':
                user_list = "Usuarios conectados: " + ", ".join(usernames.values())
                client_socket.send(user_list.encode('utf-8'))
            elif message == '/quitar':
                goodbye_message = f"{username} se ha desconectado."
                broadcast(goodbye_message)
                print(goodbye_message)
                break
            else:
                full_message = f"{username}: {message}"
                print(full_message)
                broadcast(full_message)
    except (ConnectionResetError, OSError):
        print(f"{usernames.get(client_socket, 'Un usuario')} se ha desconectado.")
    finally:
        if client_socket in clients:
            del clients[client_socket]
        if client_socket in usernames:
            del usernames[client_socket]
        client_socket.close()

def broadcast(message, exclude_client=None):
    for client in clients.keys():
        if client != exclude_client: 
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje a un cliente: {str(e)}")
                del clients[client]


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1430))
server_socket.listen(5)

print("Servidor en ejecución, esperando conexiones...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}")
    clients[client_socket] = None

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
