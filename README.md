## Implementação de um Chat Simples Usando Sockets em Python

### Como Executar o Chat
1. Salve o código do servidor em um arquivo chamado chat_server.py e o código do cliente em um arquivo chamado chat_client.py.

2. Abra um terminal e inicie o servidor:

```python
python chat_server.py
```
Você verá uma mensagem indicando que o servidor está ouvindo em 0.0.0.0:5000.

3. Abra outro terminal para cada cliente que deseja conectar e execute:

```python
python chat_client.py
```

**Observações:**

* Certifique-se de que o endereço IP e a porta no cliente correspondem aos do servidor.
* Para conectar clientes em máquinas diferentes, substitua '127.0.0.1' pelo endereço IP do servidor na rede.
* Digite mensagens no terminal do cliente e pressione Enter para enviá-las.
* Digite sair para encerrar a conexão do cliente.