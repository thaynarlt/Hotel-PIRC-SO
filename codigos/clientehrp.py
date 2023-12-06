import socket
import sys
from servidorhrp import menu

TAM_MSG = 1024         # Tamanho do bloco de mensagem
HOST = '127.0.0.1'     # IP do Servidor
PORT = 40000           # Porta que o Servidor escuta

if len(sys.argv) > 1:
    HOST = sys.argv[1]
print('Servidor:', HOST+':'+str(PORT))

# Lógica de conexão ao servidor
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

# É criado um loop infinito que será executado enquanto o cliente se manter conectado ao servidor, sendo quebrado apenas quando o cliente solicitar que a conexão se encerre.
while True:
        # Impressão do menu atráves da função importada da classe GestorReservas.
        menu_str = menu.exibir_menu()

        # O código numérico da função que o cliente escolher será atribuida à variável "seletor".
        seletor = input('\033[1;34m'+'HRP> ')

        # O código escolhido é enviado ao servidor para ser impresso no log do servidor a função requisitada e o cliente que a requisitou.
        sock.send(str.encode(seletor))

        # Estrutura de decisão para validar o código enviado pelo cliente.
        # Se o código for '1', o cliente deseja ver as reservas já feitas.
        if seletor == '1':
            # A função de ver as reservas é executada no servidor, que envia o retorno para o cliente através de sockets, essa resposta é guardada na variável "reservas_feitas".
            reservas_feitas = sock.recv(TAM_MSG).decode()
            # Impressão do retorno da função enviado pelo servidor.
            print(reservas_feitas)

        # Se o código for '2', o cliente deseja ver os quartos disponíveis para reserva.
        elif seletor == '2':
            # A função de ver os quartos disponíveis é executada no servidor, que envia o retorno para o cliente através de sockets, essa resposta é guardada na variável "quartos_disponiveis".
            quartos_disponiveis = sock.recv(TAM_MSG).decode()
            # Impressão do retorno da função enviado pelo servidor.
            print(quartos_disponiveis)

        # Se o código for '3', o cliente deseja fazer a reserva de um quarto.
        elif seletor == '3':

            # O cliente deve informar o seu nome para realizar a reserva.
            nome = input("Digite o nome do cliente: ")

            # Validação para garantir que o nome fornecido pelo cliente seja composto por apenas letras.
            while not nome.isalpha():
                print("Por favor, digite um nome válido contendo apenas letras. (Code 30)")
                nome = input("Digite o nome do cliente: ")

            # O nome do cliente é enviado ao servidor, sendo usado como parâmetro para a execução da função.
            sock.send(str.encode(nome))

            # O cliente deve informar o número do quarto que deseja reservar.
            quarto = input("Digite o número do quarto: ")

            # O número de quarto escolhido é enviado ao servidor, sendo usado como parâmetro para a execução da função
            sock.send(str.encode(quarto))

            # Impressão para indicar funcionamento da requisição
            print('Processando reserva...')

            # Após a função ser executada no servidor, o servidor retorna uma resposta ao cliente, sendo atribuída à variável "resposta" que é recebida pelo cliente.
            resposta = sock.recv(TAM_MSG).decode()

            # Impressão do retorno da execução.
            print(resposta)

        # Se o código for '4', o cliente deseja realizar o cancelamento de uma reserva.
        elif seletor == '4':

            # O cliente deve informar o número do quarto reservado que ele deseja cancelar.

            numero = input("Digite o número do quarto para cancelar a reserva: ")
            # Validação para garantir que o cliente informe um número.
            while not numero:
                print("Por favor, digite um número inteiro. (Code 30)")
                numero = input("Digite o número do quarto para cancelar a reserva: ")

            # O número do quarto é enviado ao servidor para execução da função.
            sock.send(str.encode(numero))

            # Após a execução da função, o servidor retorna uma resposta ao cliente, sendo atribuída à variável "resposta" que é recebida pelo cliente.
            resposta = sock.recv(TAM_MSG).decode()

            # Impressão do retorno da execução
            print(resposta)
        
        # Se o código for '5', o cliente deseja ver o dicionário de códigos da aplicação, mostrando o significado dos códigos utilizados nas funções e retornos para indicar status.
        elif seletor == '5':

            # O cliente recebe a resposta da execução da função do servidor, atribuindo-a à variável dicionario
            dicionario = sock.recv(TAM_MSG).decode()

            # Impressão da resposta
            print(dicionario)

        # Se o código for '6', o cliente deseja encerrar a sessão.
        elif seletor == '6':

            # Impressão de despedida.
            print('Até mais!')

            # Encerramento da conexão e quebra do loop infinito.
            sock.close()
            break

        # Se o código informado pelo cliente não for válido, será impressa uma mensagem de erro e o loop irá ser reiniciado.
        else:
            print("Opção inválida. (Code 30)")
sock.close()
