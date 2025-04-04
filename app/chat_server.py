import socket
import threading
import sys

clients = {}  # Dicionário {socket: username}
server_running = True  # Flag para controlar o loop do servidor

def handle_client(client_socket, client_address):
    global server_running
    print(f"[+] Nova conexão de {client_address}")

    try:
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        print(f"[+] Usuário {username} conectado de {client_address}")

        broadcast(f"🔵 {username} entrou no chat!", client_socket)

        while server_running:
            message = client_socket.recv(1024)
            if message:
                broadcast(f"{username}: {message.decode()}", client_socket)
            else:
                remove_client(client_socket)
                break
    except:
        remove_client(client_socket)

def broadcast(message, sender_socket):
    for client in list(clients.keys()):  # Copia para evitar erro ao remover clientes
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"[-] {username} saiu do chat.")
        del clients[client_socket]
        client_socket.close()
        broadcast(f"🔴 {username} saiu do chat.", None)

def server_shutdown(server_socket):
    global server_running
    while True:
        command = input()
        if command.lower() == 'q':
            print("\n[!] Desligando o servidor...")
            server_running = False

            # Fecha todos os clientes conectados
            for client in list(clients.keys()):
                client.send("Servidor encerrado.".encode())
                client.close()
            clients.clear()

            # Fecha o servidor
            server_socket.close()
            sys.exit()

def main():
    server_host = '0.0.0.0'
    server_port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"[+] Servidor ouvindo em {server_host}:{server_port}")
    print("[!] Pressione 'q' e Enter para fechar o servidor.")

    # Inicia a thread para monitorar o comando 'q'
    shutdown_thread = threading.Thread(target=server_shutdown, args=(server_socket,))
    shutdown_thread.daemon = True  # Encerra a thread ao fechar o programa
    shutdown_thread.start()

    while server_running:
        try:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except OSError:
            break  # Sai do loop se o socket for fechado

if __name__ == "__main__":
    main()
