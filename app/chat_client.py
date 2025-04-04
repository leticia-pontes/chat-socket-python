import socket
import threading
import sys


# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")  # Exibe a mensagem corretamente no console
            else:
                print("Conexão encerrada pelo servidor.")
                client_socket.close()
                break
        except:
            print("Ocorreu um erro!")
            client_socket.close()
            break


def main():
    server_host = '127.0.0.1'  # Endereço do servidor
    server_port = 5000  # Porta do servidor

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_host, server_port))
    except:
        print("Não foi possível conectar ao servidor.")
        sys.exit()

    # Pede o nome do usuário e envia para o servidor
    username = input("Digite seu nome de usuário: ")
    client_socket.send(username.encode())

    # Inicia a thread para receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'sair':
            client_socket.send("sair".encode())  # Envia comando de saída
            client_socket.close()
            break
        else:
            try:
                client_socket.send(message.encode())  # Apenas a mensagem (o servidor adiciona o nome)
            except:
                print("Não foi possível enviar a mensagem.")
                client_socket.close()
                break


if __name__ == "__main__":
    main()
