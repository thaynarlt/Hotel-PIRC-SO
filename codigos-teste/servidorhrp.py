import socket
import os
import threading
from main import GestorReservas

TAM_MSG = 1024  # Tamanho do bloco de mensagem
HOST = '0.0.0.0'  # IP do Servidor
PORT = 40000  # Porta que o Servidor escuta

menu = GestorReservas()

def processa_msg_cliente(msg, con, cliente):
    msg = msg.decode()
    print('Cliente', cliente, 'enviou', msg)
    if msg == '1':
        reservas = menu.ver_reservas()
        con.send(str.encode(reservas))

    elif msg == '2':
        nome = con.recv(TAM_MSG)
        nome = nome.decode()
        numero = con.recv(TAM_MSG)
        numero = numero.decode()
<<<<<<< HEAD
        resposta = menu.fazer_reserva(nome, numero)
        con.send(str.encode(resposta))
=======
        teste = menu.fazer_reserva(nome, numero)
        con.send(str.encode(teste))
>>>>>>> 50b7d42608c769cbe93d8d3b26438c9d4e00ef42

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


if __name__ == "__main__":
    main()