import threading

#Criando um semáforo para lidar com a exclusão mútua.
mutex = threading.Semaphore(1)

# Classe do objeto "menu" que será criado, contendo todas as funções da aplicação e servido como uma espécie de banco de dados do servidor, garantindo que todos os cliente sejam fornecidos os mesmos dados.
class GestorReservas:
    # Construtor
    def __init__(self):

        #Lista de quartos disponíveis para reserva.
        self.quartos = [101, 102, 103, 104, 105, 106, 107, 108, 109, 201, 202, 203, 204, 205, 206, 207, 208, 209, 301, 302, 303, 304, 305, 307, 308, 309]
        #Dicionário para armazenar as reservas feitas pelos clientes.
        self.reservas = {}
        #Dicionário de códigos que são atribuídos a todas as operações realizadas dentro da aplicação, indicando de forma universal se a operação obteve sucesso ou falhou(e o motivo).
        self.codigos = {'20' : 'Operação realizada com sucesso.',
                        '30' : 'Operação falhou(argumento inválido)',
                        '40' : 'Operação falhou(quarto indisponível)',
                        '50' : 'Operação recusada(permissão negada)',
                        '60' : 'Erro de conexão'}

    #Função para exibir o menu do sistema do Hotel para o cliente.
    def exibir_menu(self):
        print('\033[1;34m' + '----------------------------------------')
        print('\033[1;34m' + 'Bem-vindo ao Hotel Reservation Protocol!')
        print('\033[1;34m' + '----------------------------------------')
        print('')
        print('\033[1;33m' + "Menu de Reservas:")
        print('\033[1;32m' + "1. Ver reservas")
        print('\033[1;32m' + "2. Ver quartos disponiveis")
        print('\033[1;32m' + "3. Fazer uma reserva")
        print('\033[1;32m' + "4. Cancelar uma reserva")
        print('\033[1;32m' + "5. Ver dicionário de códigos de resposta")
        print('\033[1;31m' + "6. Sair" + '\033[0m')

    #Função para ver reservas já feitas:
    def ver_reservas(self):

        # Declaração da variável global do mutex, garantindo que a mesma seja usada em todas as funções para que a exclusão mútua seja realizada de forma correta.
        global mutex 

        # A função tenta adquirir o semáforo, caso consiga, bloqueia o acesso às seções críticas do código para garantir exclusividade de acesso e integridade dos dados. Caso falhe em obter o semáforo, pelo fato de outro cliente estar usando em uma função atualmente, o processamento dessa função será bloqueado, esperando até que o mutex seja liberado para que execute novamente.
        mutex.acquire() 

        # Verificação para sabe se já existem reservas feitas.
        if self.reservas:
            # Criação da variável "result" que será usada para guardar o retorno da função
            result = "Reservas:\n" 

            # Itera sobre os itens (chave-valor) no dicionário self.reservas.
            for numero, nome in self.reservas.items():
                #   Adiciona uma string formatada ao resultado para cada reserva encontrada.
                result += f"Quarto {numero} reservado para {nome}. (Code 20 -OK)\n"
            # Libera o semáforo, permitindo que outras threads acessem seções críticas do código.
            mutex.release() 
            # Retorna o resultado para ser impresso para o cliente. 
            return result
        # Executado caso o dicionário de reservas esteja vazio.
        else:
            # Libera o semáforo já que não será acessada nenhuma região crítica.
            mutex.release()
            # Retorna uma mensagem ao cliente.
            return "Nenhuma reserva encontrada. (Code 20 -OK)" 
        

    # Função para exibir todos os quartos disponíveis
    def ver_quartos_disponiveis(self):
        global mutex # -> Semáforo usado para garantir acesso exclusivo a seções críticas do código.
        mutex.acquire()
        # Adquire o semáforo, bloqueando outros threads de entrarem na seção crítica. Isso é feito para garantir operações atômicas na lista de quartos.
        if self.quartos: #Verifica se a lista de quartos (self.quartos) não está vazia.
            self.quartos.sort() #Ordena a lista de quartos em ordem crescente.
            result = "Quartos disponiveis: " + ', '.join(map(str, self.quartos)) + ' (Code 20 -OK)'
            # Cria uma string formatada que contém a mensagem indicando os quartos disponíveis, formatando a lista de quartos como uma string separada por vírgulas.
            mutex.release()
            #Libera o semáforo, permitindo que outros threads possam entrar na seção crítica.
            return result
            #Retorna a mensagem formatada contendo os quartos disponíveis.
        else:
            mutex.release()
            return "Não possuímos nenhum quarto disponível no momento. (Code 20 -OK)"

    #Função para fazer uma reserva
    def fazer_reserva(self, nome, numero):
        # Verificar se o número do quarto já está reservado
        global mutex
        #mutex -> Garantir que a operação crítica de fazer a reserva seja realizada de maneira exclusiva, evitando condições de corrida
        mutex.acquire()
        if numero in self.reservas: #Verifica se o número do quarto (numero) já está presente no dicionário de reservas (self.reservas)
            mutex.release()
            return f"Desculpe, o quarto {numero} já está reservado. (Code 40 -ERR)"
        # Verifica se o número do quarto é válido
        elif int(numero) not in self.quartos: #Verifica se está presente na lista de quartos disponíveis (self.quartos).
            mutex.release()
            return f"Número de quarto inexistente. (Code 30 -ERR)"
        else: #Se tudo for válido:
            # Faz a reserva e atualiza a lista de quartos disponíveis
            self.reservas[numero] = nome # Cria uma reserva associando o número do quarto (numero) ao nome do cliente (nome) no dicionário de reservas (self.reservas).
            self.quartos.remove(int(numero)) #Vai retirar o quarto da lista de quartos disponíveis, pois foi reservado
            mutex.release()
            return f"Reserva para {nome} no quarto {numero} realizada com sucesso. (Code 20 -OK)"
            
    #Função para cancelar uma reserva
    def cancelar_reserva(self, numero):
        # Verificar se o número do quarto está reservado
        global mutex
        mutex.acquire()
        if numero in self.reservas: #Verifica se o número do quarto está presente no dicionário de reservas.
            # Remove a reserva e atualiza a lista de quartos disponíveis
            nome_cliente = self.reservas.pop(numero) #Remove a reserva associada ao número do quarto, obtendo o nome do cliente que estava no quarto reservado.
            self.quartos.append(int(numero)) #Adiciona o número do quarto de volta à lista de quartos disponíveis, convertendo para inteiro, pois os quartos são representados como strings.
            mutex.release()
            return f"Reserva para {nome_cliente} no quarto {numero} cancelada com sucesso. (Code 20 -OK)"
        else:
            mutex.release() #Não é possivel cancelar a reserva de um quarto que não foi reservado anteriormente.
            return f"Desculpe, o quarto {numero} não está reservado ou não existe. (Code 30 -ERR)"
        
    #Função para exibir o dicionário de códigos de resposta
    def ver_dicionario(self):
    # "ver_dicionario" -> tem o propósito de gerar uma representação formatada do dicionário de códigos de resposta (self.codigos).
        result = "Dicionário de código: (Code 20 -OK)\n"
        for codigo, descricao in self.codigos.items(): #iterar sobre os itens do dicionário "self.codigos.codigo" representa a chave (código) e descricao representa o valor associado (descrição).
            result += f"Código {codigo} = {descricao}\n" #: Para cada par chave-valor no dicionário, adiciona uma linha ao resultado contendo a representação formatada do código e sua descrição.
        return result