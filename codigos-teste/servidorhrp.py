# Coisas pra fzr:

# Criar dicionario de códigos de resposta(para entendimento universal) para as funções do app e implementá-los em todos os retornos de msg. 

# Documentação geral do código. 
# Revisar cores das mensagens ?????
# Revisar código de forma geral no fim.
# Rezar pra tirar um 10 e passar em protocolos. (Importante!!!)



import socket
import threading
from main import GestorReservas

TAM_MSG = 1024  # Tamanho do bloco de mensagem
HOST = '0.0.0.0'  # IP do Servidor
PORT = 40000  # Porta que o Servidor escuta

menu = GestorReservas()
funcoes = {'1': 'requisição para ver os quartos já reservados.',
           '2': 'requisição para ver os quartos disponiveis.',
           '3': 'requisição para fazer uma reserva.',
           '4': 'requisição para cancelar uma reserva.',
           '5': 'requisição para encerrar a conexão.'}


def processa_msg_cliente(msg, con, cliente):
    msg = msg.decode()
    print('Cliente', cliente, 'enviou', funcoes[msg])
    
    if msg == '1':
        reservas = menu.ver_reservas()
        con.send(str.encode(reservas))

    elif msg == '2':
        quartos = menu.ver_quartos_disponiveis()
        con.send(str.encode(quartos))

    elif msg == '3':
        nome = con.recv(TAM_MSG)
        nome = nome.decode()
        numero = con.recv(TAM_MSG)
        numero = numero.decode()
        resposta = menu.fazer_reserva(nome, numero)
        con.send(str.encode(resposta))

    elif msg == '4':
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