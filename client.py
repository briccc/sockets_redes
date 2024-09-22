import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                raise ConnectionResetError
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
        except (ConnectionAbortedError, ConnectionResetError, OSError):
            messagebox.showwarning("Conexión Perdida", "Se ha perdido la conexión con el servidor.")
            client_socket.close()
            break

def send_message(event=None):
    message = message_entry.get()
    if message: 
        if message.startswith('/listar'):
            client_socket.send(message.encode('utf-8'))
            message_entry.delete(0, tk.END)
        elif message.startswith('/quitar'):
            client_socket.send(message.encode('utf-8'))
            messagebox.showinfo("Desconexión", "Te has desconectado del chat.")
            client_socket.close()
            window.quit()  
        else:
            try:
                client_socket.send(message.encode('utf-8'))
                message_entry.delete(0, tk.END)
            except OSError:
                messagebox.showwarning("Error", "No se puede enviar el mensaje. Conexión perdida.")

def start_chat():
    global username, client_socket, chat_box, message_entry

    username = simpledialog.askstring("Nombre de Usuario", "Introduce tu nombre de usuario:", parent=window)
    
    if username:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(('localhost', 1430))
            client_socket.send(username.encode('utf-8'))

            chat_box.config(state=tk.NORMAL)
            chat_box.config(state=tk.DISABLED)

            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()

            window.deiconify()
        except ConnectionRefusedError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor.")
            client_socket.close()
            window.quit()

window = tk.Tk()
window.title("Chat")
window.withdraw()


background_color = "#e6ddd2"
button_color = "#f3eee8"
text_color = "#000000"
bg_color_input = "#ffffff"

window.configure(bg=background_color)

chat_box = scrolledtext.ScrolledText(window, bg=background_color, fg=text_color)
chat_box.pack(padx=10, pady=10)
chat_box.config(state=tk.DISABLED)

message_entry = tk.Entry(window, font=("Arial", 11), width=82, bg=bg_color_input, fg=text_color)
message_entry.pack(padx=10, pady=10)

message_entry.bind("<Return>", send_message)  

send_button = tk.Button(window, text="Enviar", command=send_message, bg=button_color, fg=text_color, font=("Arial", 11))
send_button.pack(padx=10, pady=10)

start_chat()
window.mainloop()
