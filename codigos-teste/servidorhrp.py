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
    # msg = msg.split()
    if msg == '1':
        menu.ver_reservas()

    elif msg == '2':
        menu.fazer_reserva()

    elif msg == '3':
        menu.cancelar_reserva()
    
    elif msg == '4':
        print('Teste quit')
        con.close()

    else:
        con.send(str.encode('-ERR Invalid command\n'))
    return True
    # if msg[0].upper() == 'GET':
    #     nome_arq = " ".join(msg[1:])
    #     print('Arquivo soclicitado:', nome_arq)
    #     try:
    #         status_arq = os.stat(nome_arq)
    #         con.send(str.encode('+OK {}\n'.format(status_arq.st_size)))
    #         arq = open(nome_arq, "rb")
    #         while True:
    #             dados = arq.read(TAM_MSG)
    #             if not dados:
    #                 break
    #             con.send(dados)
    #     except Exception as e:
    #         con.send(str.encode('-ERR {}\n'.format(e)))
    # elif msg[0].upper() == 'CWD':
    #     nome_dir = "".join(msg[1:])
    #     print('Diretório solicitado:', nome_dir)
    #     try:
    #         os.chdir(nome_dir)
    #         con.send(str.encode('+OK\n'))
    #     except Exception as e:
    #         con.send(str.encode('-ERR{}\n'.format(e)))
    # elif msg[0].upper() == 'LIST':
    #     lista_arq = os.listdir('.')
    #     con.send(str.encode('+OK {}\n'.format(len(lista_arq))))
    #     for nome_arq in lista_arq:
    #         if os.path.isfile(nome_arq):
    #             status_arq = os.stat(nome_arq)
    #             con.send(str.encode('arq: {} - {:.1f}KB\n'.format(nome_arq, status_arq.st_size / 1024)))
    #         elif os.path.isdir(nome_arq):
    #             con.send(str.encode('dir: {}\n'.format(nome_arq)))
    #         else:
    #             con.send(str.encode('esp: {}\n'.format(nome_arq)))
    # elif msg[0].upper() == 'QUIT':
    #     con.send(str.encode('+OK\n'))
    #     return False
    

def processa_cliente(con, cliente):
    print('Cliente conectado', cliente)
    while True:
        msg = con.recv(TAM_MSG)
        processa_msg_cliente(msg, con, cliente)
        # if not msg or not processa_msg_cliente(msg, con, cliente):
        #     break
    con.close()
    print('Cliente desconectado', cliente)

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

    sock.close()

if __name__ == "__main__":
    main()