#!/usr/bin/env python3
import socket
import sys
from servidorhrp import menu

TAM_MSG = 1024         # Tamanho do bloco de mensagem
HOST = '127.0.0.1'     # IP do Servidor
PORT = 40000           # Porta que o Servidor escuta

if len(sys.argv) > 1:
    HOST = sys.argv[1]
print('Servidor:', HOST+':'+str(PORT))

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

while True:
        menu_str = menu.exibir_menu()
        seletor = input('\033[1;34m'+'HRP> ')

        sock.send(str.encode(seletor))

        if seletor == '1':
            reservas_feitas = sock.recv(TAM_MSG).decode()
            print(reservas_feitas)

        elif seletor == '2':
            quartos_disponiveis = sock.recv(TAM_MSG).decode()
            print(quartos_disponiveis)

        elif seletor == '3':
            nome = input("Digite o nome do cliente: ")
            while not nome.isalpha():
                print("Por favor, digite um nome válido contendo apenas letras. (Code 30)")
                nome = input("Digite o nome do cliente: ")
            sock.send(str.encode(nome))
            quarto = input("Digite o número do quarto: ")
            sock.send(str.encode(quarto))
            print('Processando reserva...')
            resposta = sock.recv(TAM_MSG).decode()
            print(resposta)

        elif seletor == '4':
            numero = input("Digite o número do quarto para cancelar a reserva: ")
            while not numero:
                print("Por favor, digite um número inteiro. (Code 30)")
                numero = input("Digite o número do quarto para cancelar a reserva: ")
            sock.send(str.encode(numero))
            resposta = sock.recv(TAM_MSG).decode()
            print(resposta)
        
        elif seletor == '5':
            dicionario = sock.recv(TAM_MSG).decode()
            print(dicionario)

        elif seletor == '6':
            print('Até mais!')
            sock.close()
            break

        else:
            print("Opção inválida. (Code 30)")
sock.close()
