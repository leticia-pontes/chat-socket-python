import socket
import threading
import sys

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                # Se a mensagem estiver vazia, o servidor foi desconectado
                print("Conexão encerrada pelo servidor.")
                client_socket.close()
                break
        except:
            # Em caso de erro, fecha o socket
            print("Ocorreu um erro!")
            client_socket.close()
            break

def main():
    server_host = '127.0.0.1'  # Endereço IP do servidor
    server_port = 5000  # Porta do servidor

    # Cria o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Conecta ao servidor
        client_socket.connect((server_host, server_port))
    except:
        print("Não foi possível conectar ao servidor.")
        sys.exit()
    # Inicia uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    # Loop para enviar mensagens ao servidor
    while True:
        message = input()
        if message.lower() == 'sair':
            client_socket.send('O usuário saiu do chat.'.encode())
            client_socket.close()
            break
        else:
            try:
                client_socket.send(message.encode())
            except:
                print("Não foi possível enviar a mensagem.")
                client_socket.close()
                break

if __name__ == "__main__":
    main()