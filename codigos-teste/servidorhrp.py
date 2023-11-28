import socket
import os
import threading
from main import GestorReservas
# from queue import Queue

TAM_MSG = 1024  # Tamanho do bloco de mensagem
HOST = '0.0.0.0'  # IP do Servidor
PORT = 40000  # Porta que o Servidor escuta

# fila_espera = Queue()
menu = GestorReservas()
funcoes = {'1': 'requisição para ver os quartos já reservados.',
           '2': 'requisição para fazer uma reserva.',
           '3': 'requisição para cancelar uma reserva.',
           '4': 'requisição para encerrar a conexão.'}


def processa_msg_cliente(msg, con, cliente):
    msg = msg.decode()
    print('Cliente', cliente, 'enviou', funcoes[msg])
    if msg == '1':
        reservas = menu.ver_reservas()
        con.send(str.encode(reservas))

    elif msg == '2':
        global mutex
        # global fila_espera
        nome = con.recv(TAM_MSG)
        nome = nome.decode()
        numero = con.recv(TAM_MSG)
        numero = numero.decode()
        resposta = menu.fazer_reserva(nome, numero)
        con.send(str.encode(resposta))
        
        ## Tentar adquirir o semáforo
        # if mutex.acquire(blocking=False):
        #     try:
        #         resposta = menu.fazer_reserva(nome, numero)
        #         con.send(str.encode(resposta))
        #     finally:
        #         # Liberar o semáforo
        #         mutex.release()
        # else:
        #     # Se o semáforo estiver bloqueado, adicionar cliente à fila de espera
        #     fila_espera.put((con, cliente, nome, numero))


    elif msg == '3':
        numero = con.recv(TAM_MSG)
        numero = numero.decode()
        resposta = menu.cancelar_reserva(numero)
        con.send(str.encode(resposta))

    else:
        con.send(str.encode('-ERR Invalid command\n'))
    return True

def processa_cliente(con, cliente):
    print('Cliente conectado', cliente)
    while True:
        msg = con.recv(TAM_MSG)
        processa_msg_cliente(msg, con, cliente)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv = (HOST, PORT)
    sock.bind(serv)
    sock.listen(50)

    while True:
        try:
            con, cliente = sock.accept()
            # Inicia uma nova thread para lidar com o cliente
            threading.Thread(target=processa_cliente, args=(con, cliente)).start()
        except Exception as e:
            print('Erro ao aceitar a conexão:', e)

# def processa_fila_espera():
#      while True:
#          global mutex

#         #  global fila_espera

#          # Obter próximo cliente da fila (bloqueante)
#          con, cliente, nome, numero = fila_espera.get()

#          # Tentar adquirir o semáforo
#          if mutex.acquire(blocking=False):
#              try:
#                  resposta = menu.fazer_reserva(nome, numero)
#                  con.send(str.encode(resposta))
#              finally:
#                  # Liberar o semáforo
#                  mutex.release()

##Iniciar uma thread para processar a fila de espera
# thread_fila_espera = threading.Thread(target=processa_fila_espera)
# thread_fila_espera.start()

if __name__ == "__main__":
    main()