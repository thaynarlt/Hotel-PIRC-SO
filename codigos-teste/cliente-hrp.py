#!/usr/bin/env python3
import socket
import sys
from servidorhrp import menu

TAM_MSG = 1024         # Tamanho do bloco de mensagem
HOST = '127.0.0.1'     # IP do Servidor
PORT = 40000           # Porta que o Servidor escuta


def decode_cmd_usr(cmd_usr):
    cmd_map = {
        'exit': 'quit',
        '1' : '1',
        '2' : '2',
        '3' : '3',
        '4' : '4',
    }
    
    tokens = cmd_usr.split()
    if tokens[0].lower() in cmd_map:
        tokens[0] = cmd_map[tokens[0].lower()]
        return " ".join(tokens)
    else:
        return False
    
if len(sys.argv) > 1:
    HOST = sys.argv[1]
print('Servidor:', HOST+':'+str(PORT))

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)
print('Para encerrar use EXIT, CTRL+D ou CTRL+C\n')


# ... (código existente)

while True:
    try:
        menu_str = menu.exibir_menu()
        seletor = input('HRP> ')
        sock.send(str.encode(seletor))
        resposta_servidor = sock.recv(TAM_MSG).decode()
        print(resposta_servidor)
    except:
        seletor = 'EXIT'
        sock.send(str.encode(seletor))

# ... (código existente)


        # if seletor == '1':
        #     resposta = sock.recv(TAM_MSG).decode()
        #     print(resposta)

        # elif seletor == '2':
        #     resposta = sock.recv(TAM_MSG).decode()
        #     print(resposta)

        # elif seletor == '3':
        #     resposta = sock.recv(TAM_MSG).decode()
        #     print(resposta)
        
        # elif seletor == '4':
        #     print('Saindo...')
        #     sock.close()
        #     break



        # dados = sock.recv(TAM_MSG)
        # if not dados: break
        # msg_status = dados.decode().split('\n')[0]
        # dados = dados[len(msg_status)+1:]
        # print(msg_status)
        # cmd = cmd.split()
        # cmd[0] = cmd[0].upper()
        # if cmd[0] == 'QUIT':
        #     break


        # if seletor == '1':
        #     reservas = menu.ver_reservas()


            # num_arquivos = int(msg_status.split()[1])
            # dados = dados.decode()
            # while True:
            #     arquivos = dados.split('\n')
            #     residual = arquivos[-1]  # último sem \n fica para próxima
            #     for arq in arquivos[:-1]:
            #         print(arq)
            #         num_arquivos -= 1
            #     if num_arquivos == 0: break
            #     dados = sock.recv(TAM_MSG)
            #     if not dados: break
            #     dados = residual + dados.decode()


        # elif seletor == '2':
        #     fazer_reserva = menu.fazer_reserva()
        

            # nome_arq = " ".join(cmd[1:])
            # print('Recebendo:', nome_arq)
            # arq = open(nome_arq, "wb")
            # tam_arquivo = int(msg_status.split()[1])
            # while True:
            #     arq.write(dados)
            #     tam_arquivo -= len(dados)
            #     if tam_arquivo == 0: break
            #     dados = sock.recv(TAM_MSG)
            #     if not dados: break
            #arq.close()


        # elif seletor == '3':
        #     cancelar_reserva = menu.cancelar_reserva()
        

        # elif seletor == '4':
        #     break
    

sock.close()
