import threading
mutex = threading.Semaphore(1)
class GestorReservas:
    def __init__(self):
        self.reservas = {}

    def exibir_menu(self):
        print('\033[1;34m' + '----------------------------------------')
        print('\033[1;34m' + 'Bem-vindo ao Hotel Reservation Protocol!')
        print('\033[1;34m' + '----------------------------------------')
        print('')
        print('\033[1;33m' + "Menu de Reservas:")
        print('\033[1;32m' + "1. Ver reservas")
        print('\033[1;32m' + "2. Fazer uma reserva")
        print('\033[1;32m' + "3. Cancelar uma reserva")
        print('\033[1;31m' + "4. Sair" + '\033[0m')

    def ver_reservas(self):
        global mutex
        mutex.acquire()
        if self.reservas:
            result = "Reservas:\n"
            for numero, nome in self.reservas.items():
                result += f"{numero}: {nome}\n"
            mutex.release()
            return result
        else:
            mutex.release()
            return "Nenhuma reserva encontrada."

    def fazer_reserva(self, nome, numero):
        # nome_cliente = input("Digite o nome do cliente: ")
        # numero_quarto = input("Digite o número do quarto: ")

        # Verificar se o número do quarto já está reservado
        global mutex
        mutex.acquire()
        if numero in self.reservas:
            mutex.release()
            return f"Desculpe, o quarto {numero} já está reservado."
        else:
            self.reservas[numero] = nome
            mutex.release()
            return f"Reserva para {nome} no quarto {numero} realizada com sucesso."
        
            

    def cancelar_reserva(self, numero):
        # numero_quarto = input("Digite o número do quarto para cancelar a reserva: ")

        # Verificar se o número do quarto está reservado
        if numero in self.reservas:
            nome_cliente = self.reservas.pop(numero)
            return f"Reserva para {nome_cliente} no quarto {numero} cancelada com sucesso."
        else:
            return f"Desculpe, o quarto {numero} não está reservado."
