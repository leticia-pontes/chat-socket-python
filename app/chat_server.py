import socket
import threading

# Lista para manter o controle dos clientes conectados
clients = []
# Função para lidar com cada cliente conectado
def handle_client(client_socket, client_address):
    print(f"[+] Nova conexão de {client_address}")
    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024)
            if message:
                # Transmite a mensagem para os outros clientes
                broadcast(message, client_socket)
            else:
                # Remove o cliente se a mensagem estiver vazia
                remove_client(client_socket)
                break
        except:
            continue

# Função para transmitir mensagens a todos os clientes conectados
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Remove o cliente se houver um erro ao enviar
                remove_client(client)
# Função para remover um cliente da lista e fechar o socket
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()
        print(f"[-] Conexão encerrada com {client_socket}")

def main():
    server_host = '0.0.0.0'  # Escuta em todas as interfaces de rede
    server_port = 5000  # Porta do servidor

    # Cria o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"[+] Servidor ouvindo em {server_host}:{server_port}")

    while True:
        # Aceita novas conexões de clientes
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"[+] Conexão estabelecida com {client_address}")

        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
if __name__ == "__main__":
    main()