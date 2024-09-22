import socket
import threading

clients = {}
usernames = {}

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        clients[client_socket] = username

        welcome_message = f"{username} se ha unido al chat."
        broadcast(welcome_message, client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                raise ConnectionResetError
            
            if message == '/listar':
                user_list = "Usuarios conectados: " + ", ".join(usernames.values())
                client_socket.send(user_list.encode('utf-8'))
            elif message == '/quitar':
                goodbye_message = f"{username} se ha desconectado."
                broadcast(goodbye_message, client_socket)
                print(goodbye_message)  # Imprimir en la consola del servidor
                break
            else:
                print(f"{username}: {message}")
                broadcast(f"{username}: {message}", client_socket)
    except (ConnectionResetError, OSError):
        # Manejar desconexiones inesperadas
        if client_socket in usernames:
            print(f"{usernames[client_socket]} se ha desconectado.")
    finally:
        # Este bloque se ejecuta siempre al final, incluso si ocurre un error
        if client_socket in clients:
            del clients[client_socket]
        if client_socket in usernames:
            del usernames[client_socket]
        client_socket.close()

def broadcast(message, client_socket):
    for client in clients.keys():
        if client != client_socket:  # No enviar el mensaje al cliente que lo envió
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje a un cliente: {str(e)}")
                del clients[client]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Servidor en ejecución, esperando conexiones...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}")
    clients[client_socket] = None  # Inicialmente no tiene nombre de usuario

    # Crear un hilo para manejar el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
