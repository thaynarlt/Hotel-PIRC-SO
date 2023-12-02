import threading
#Criando um semáforo
mutex = threading.Semaphore(1)
class GestorReservas:
    def __init__(self):
        #Lista de quartos disponíveis para reserva
        self.quartos = [101, 102, 103, 104, 105, 106, 107, 108, 109, 201, 202, 203, 204, 205, 206, 207, 208, 209, 301, 302, 303, 304, 305, 307, 308, 309]
        #Dicionário paa armazenar as reservas
        self.reservas = {}
        #Dicionário de códigos para atribuir uma opração bem sucedida ou falha
        self.codigos = {'20' : 'Operação realizada com sucesso.',
                        '30' : 'Operação falhou(argumento inválido)',
                        '40' : 'Operação falhou(quarto indisponível)',
                        '50' : 'Operação recusada(permissão negada)',
                        '60' : 'Erro de conexão'}
    #Função para exibir o menu do sistema do Hotel
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

    #Função para ver reservas:
    def ver_reservas(self):
        global mutex #
        mutex.acquire() #Adquire o semáforo, bloqueando o acesso a seções críticas do código para garantir exclusividade de acesso.
        if self.reservas:
            result = "Reservas:\n" 
            for numero, nome in self.reservas.items():
            #Itera sobre os itens (chave-valor) no dicionário self.reservas.
                result += f"Quarto {numero} reservado para {nome}. (Code 20)\n"
                #Adiciona uma string formatada ao resultado para cada reserva encontrada.
            mutex.release() #mutex -> Libera o semáforo, permitindo que outras threads acessem seções críticas do código.
            return result
        else:#Executado caso o dicionário de reservas esteja vazio.
            mutex.release() # -> Libera o semáforo mesmo que não haja reservas para garantir consistência no uso do semáforo.
            return "Nenhuma reserva encontrada. (Code 20)" 
        

    #Função para exibir todos os quartos disponíveis
    def ver_quartos_disponiveis(self):
        global mutex # -> Semáforo usado para garantir acesso exclusivo a seções críticas do código.
        mutex.acquire()
        # Adquire o semáforo, bloqueando outros threads de entrarem na seção crítica. Isso é feito para garantir operações atômicas na lista de quartos.
        if self.quartos: #Verifica se a lista de quartos (self.quartos) não está vazia.
            self.quartos.sort() #Ordena a lista de quartos em ordem crescente.
            result = "Quartos disponiveis: " + ', '.join(map(str, self.quartos)) + ' (Code 20)'
            # Cria uma string formatada que contém a mensagem indicando os quartos disponíveis, formatando a lista de quartos como uma string separada por vírgulas.
            mutex.release()
            #Libera o semáforo, permitindo que outros threads possam entrar na seção crítica.
            return result
            #Retorna a mensagem formatada contendo os quartos disponíveis.
        else:
            mutex.release()
            return "Não possuímos nenhum quarto disponível no momento. (Code 20)"

    #Função para fazer uma reserva
    def fazer_reserva(self, nome, numero):
        # Verificar se o número do quarto já está reservado
        global mutex
        #mutex -> Garantir que a operação crítica de fazer a reserva seja realizada de maneira exclusiva, evitando condições de corrida
        mutex.acquire()
        if numero in self.reservas: #Verifica se o número do quarto (numero) já está presente no dicionário de reservas (self.reservas)
            mutex.release()
            return f"Desculpe, o quarto {numero} já está reservado. (Code 40)"
        # Verifica se o número do quarto é válido
        elif int(numero) not in self.quartos: #Verifica se está presente na lista de quartos disponíveis (self.quartos).
            mutex.release()
            return f"Número de quarto inexistente. (Code 30)"
        else: #Se tudo for válido:
            # Faz a reserva e atualiza a lista de quartos disponíveis
            self.reservas[numero] = nome # Cria uma reserva associando o número do quarto (numero) ao nome do cliente (nome) no dicionário de reservas (self.reservas).
            self.quartos.remove(int(numero)) #Vai retirar o quarto da lista de quartos disponíveis, pois foi reservado
            mutex.release()
            return f"Reserva para {nome} no quarto {numero} realizada com sucesso. (Code 20)"
            
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
            return f"Reserva para {nome_cliente} no quarto {numero} cancelada com sucesso. (Code 20)"
        else:
            mutex.release() #Não é possivel cancelar a reserva de um quarto que não foi reservado anteriormente.
            return f"Desculpe, o quarto {numero} não está reservado. (Code 30)"
        
    #Função para exibir o dicionário de códigos de resposta
    def ver_dicionario(self):
    # "ver_dicionario" -> tem o propósito de gerar uma representação formatada do dicionário de códigos de resposta (self.codigos).
        result = "Dicionário de código: (Code 20)\n"
        for codigo, descricao in self.codigos.items(): #iterar sobre os itens do dicionário "self.codigos.codigo" representa a chave (código) e descricao representa o valor associado (descrição).
            result += f"Código {codigo} = {descricao}\n" #: Para cada par chave-valor no dicionário, adiciona uma linha ao resultado contendo a representação formatada do código e sua descrição.
        return result