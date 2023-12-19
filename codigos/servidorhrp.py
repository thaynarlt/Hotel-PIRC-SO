# Coisas pra fzr:

# Finalizar e revisar documentação geral do código. 
# Revisar código no fim.
# Rezar pra tirar um 10 e passar em protocolos. (Importante!!!)

import socket
import threading
from main import GestorReservas

TAM_MSG = 1024  # Tamanho do bloco de mensagem
HOST = '0.0.0.0'  # IP do Servidor
PORT = 40000  # Porta que o Servidor escuta

# Criação de um objeto menu para a classe GestorReservas que possui todas as funcionalidades da aplicação, sendo o mesmo objeto usado para todos os clientes, assim, virando uma espécie de banco de dados, fornecendo as mesmas informações e mudanças para todos os clientes.
menu = GestorReservas()

# Dicionário para traduzir os códigos enviados das requisições dos clientes para o log do servidor.
funcoes = {'1': 'requisição para ver os quartos já reservados.',
           '2': 'requisição para ver os quartos disponiveis.',
           '3': 'requisição para fazer uma reserva.',
           '4': 'requisição para cancelar uma reserva.',
           '5': 'requisição para consulta do dicionário de códigos'}

# Função que processa as requisições enviadas pelos clientes, utilizando o código enviado na mensagem para acionar sua respectiva função.
def processa_msg_cliente(msg, con, cliente):
    
    # Decodificação da mensagem(código) enviada pelo cliente.
    msg = msg.decode()
    # Impressão para o log do servidor, especificando o endereço do cliente e sua requisição. Caso a mensagem enviada esteja vazia, significa que o cliente pediu para encerrar a conexão, portanto não será impresso um item do dicionário, e sim a string alternativa "requisição para encerrar a conexão".
    print('Cliente', cliente, 'enviou', funcoes.get(msg, 'requisição para encerrar a conexão'))

    # Estrutura de decisão para identificar a funcionalidade requisitada pelo cliente.
    match msg:
        # Se o código enviado pelo cliente for '1', ele deseja ver as reservas que já existem.
        case '1':
            # A execução da funçar ver_reservas() do menu retorna uma string com as reservas feitas(se existirem), sendo armazenada na variável 'reservas'.
            reservas = menu.ver_reservas()

            # A variável 'reservas' é enviada ao cliente para ser impressa.
            con.send(str.encode(reservas))

        # Se o código enviado pelo cliente for '2', ele deseja ver os quartos disponíveis que ainda não foram reservados.
        case '2':
            # A execução da funçar ver_quartos_disponiveis() do menu retorna uma string com os quartos disponíveis para reserva, sendo armazenada na variável 'quartos'.
            quartos = menu.ver_quartos_disponiveis()

            # A variável 'quartos' é enviada ao cliente para ser impressa.
            con.send(str.encode(quartos))


        # Se o código enviado pelo cliente for '3', ele deseja fazer uma reserva.
        case '3':
            # O servidor espera receber um input enviado pelo cliente com o nome da pessoa que deseja fazer a reserva, guardando esse dado na variável 'nome'
            nome = con.recv(TAM_MSG)
            # Decodificação do nome enviado pelo cliente
            nome = nome.decode()

            # O servidor espera receber um input enviado pelo cliente com o número do quarto que ele deseja reservar, guardando esse dado na variável 'numero'
            numero = con.recv(TAM_MSG)
            # Decodificação do número do quarto enviado pelo cliente
            numero = numero.decode()

            # A execução da função fazer_reserva do menu irá fazer a reserva desejada pelo cliente(caso o quarto desejado esteja disponível e/ou exista), usando o nome e número de quarto fornecido, retornando uma mensagem que indica o status da requisição(se a reserva foi feita ou se falhou por determinado motivo), guardando esse retorno na variável 'resposta'.
            resposta = menu.fazer_reserva(nome, numero)
            # A variável 'resposta' é enviada ao cliente para impressão.
            con.send(str.encode(resposta))


        # Se o código enviado pelo cliente for '4', ele deseja fazer o cancelamento de uma reserva.
        case '4':
            # O servidor espera receber um input enviado pelo cliente contendo o número do quarto que ele deseja realizar o cancelamento, guardando esse dado na variável 'numero'.
            numero = con.recv(TAM_MSG)
            # Decodificação do número recebido.
            numero = numero.decode()

            # A execução da função cancelar_reserva do menu irá cancelar a reserva do quarto(caso o quarto esteja reservado e/ou exista) utilizando o número recebido do cliente como parâmetro, retornando uma mensagem que indica o status da requisição(se a reserva foi cancelada com sucesso ou se falhou por determinado motivo), guardando esse retorno na variável 'resposta'.
            resposta = menu.cancelar_reserva(numero)
            # A variável 'resposta' é enviada ao cliente para impressão.
            con.send(str.encode(resposta))

        case '5':
            dicionario = menu.ver_dicionario()
            con.send(str.encode(dicionario))



# Função que processa os clientes que vão se conectando ao servidor
def processa_cliente(con, cliente):
    # Impressão para o log do servidor, informando quando um cliente se conecta, especficando o endereço e porta do mesmo
    print(f'Cliente conectado', {cliente}, ' (Code 20 -OK)' )
    # Iniciação de um loop para ficar escutando qualquer requisição que o cliente fizer
    while True:
        # Recebe a requisição do cliente e guarda na variável 'msg'
        msg = con.recv(TAM_MSG)
        # Se a mensagem enviada pelo cliente estiver vazia, significa que ele requisitou para encerrar a conexão.
        if not msg:
            # Impressão para o log do servidor.
            print(f'Cliente {cliente} encerrou a conexão (Code 20 -OK)')
            # Quebra do loop de escuta para o cliente que se desconectou.
            break
        # Quando um cliente envia uma requisição, a função de processsar sua requisição é chamada, sendo passados a mensagem(código) e endereço do cliente como parâmetros
        processa_msg_cliente(msg, con, cliente)


# Função principal para rodar o servidor
def main():
    # Criação de um servidor TCP usando sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv = (HOST, PORT)
    sock.bind(serv)
    # Instrução para o servidor "escutar" possíveis clientes que tentarem se conectar
    sock.listen(50)

    # Criação de um loop infinito para ficar escutando clientes que tentem se conectar
    while True:
        try:
            # O servidor aceita a conexão do cliente
            con, cliente = sock.accept()
            # Inicia uma nova thread para lidar com o cliente (transformando o servidor em multiprocesso, sendo capaz de lidar com diversos clientes de uma só vez devido as threads que são usadas para surprir as necessidades de cada um).
            threading.Thread(target=processa_cliente, args=(con, cliente)).start()
        # Impressão de erro caso a conexão cliente-servidor não tenha sucesso por algum motivo.
        except Exception as e:
            print('Erro ao aceitar a conexão:', e, ' (Code 60 -ERR)')

# Execução do servidor
if __name__ == "__main__":
    main()