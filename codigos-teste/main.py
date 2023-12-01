import threading
mutex = threading.Semaphore(1)
class GestorReservas:
    def __init__(self):
        self.quartos = [101, 102, 103, 104, 105, 106, 107, 108, 109, 201, 202, 203, 204, 205, 206, 207, 208, 209, 301, 302, 303, 304, 305, 307, 308, 309]
        self.reservas = {}
        self.codigos = {'20' : 'Operação realizada com sucesso.',
                        '30' : 'Operação falhou(argumento inválido)',
                        '40' : 'Operação falhou(quarto indisponível)',
                        '50' : 'Operação recusada(permissão negada)',
                        '60' : 'Erro de conexão'}

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


    def ver_reservas(self):
        global mutex
        mutex.acquire()
        if self.reservas:
            result = "Reservas:\n"
            for numero, nome in self.reservas.items():
                result += f"Quarto {numero} reservado para {nome}. (Code 20)\n"
            mutex.release()
            return result
        else:
            mutex.release()
            return "Nenhuma reserva encontrada. (Code 20)"
    
    def ver_quartos_disponiveis(self):
        global mutex
        mutex.acquire()
        if self.quartos:
            self.quartos.sort()
            result = "Quartos disponiveis: " + ', '.join(map(str, self.quartos)) + ' (Code 20)'
            mutex.release()
            return result
        else:
            mutex.release()
            return "Não possuímos nenhum quarto disponível no momento. (Code 20)"


    def fazer_reserva(self, nome, numero):
        # Verificar se o número do quarto já está reservado
        global mutex
        mutex.acquire()
        if numero in self.reservas:
            mutex.release()
            return f"Desculpe, o quarto {numero} já está reservado. (Code 40)"
        elif int(numero) not in self.quartos:
            mutex.release()
            return f"Número de quarto inexistente. (Code 30)"
        else:
            self.reservas[numero] = nome
            self.quartos.remove(int(numero))
            mutex.release()
            return f"Reserva para {nome} no quarto {numero} realizada com sucesso. (Code 20)"
            

    def cancelar_reserva(self, numero):
        # Verificar se o número do quarto está reservado
        global mutex
        mutex.acquire()
        if numero in self.reservas:
            nome_cliente = self.reservas.pop(numero)
            self.quartos.append(int(numero))
            mutex.release()
            return f"Reserva para {nome_cliente} no quarto {numero} cancelada com sucesso. (Code 20)"
        else:
            mutex.release()
            return f"Desculpe, o quarto {numero} não está reservado. (Code 30)"

    def ver_dicionario(self):
        result = "Dicionário de código: (Code 20)\n"
        for codigo, descricao in self.codigos.items():
            result += f"Código {codigo} = {descricao}\n"
        return result