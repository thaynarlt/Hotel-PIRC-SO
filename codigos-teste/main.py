class GestorReservas:
    def __init__(self):
        self.reservas = {}

    def exibir_menu(self):
        print('----------------------------------------')
        print('Bem-vindo ao Hotel Reservation Protocol!')
        print('----------------------------------------')
        print('')
        print("Menu de Reservas:")
        print("1. Ver reservas")
        print("2. Fazer uma reserva")
        print("3. Cancelar uma reserva")
        print("4. Sair")

    def ver_reservas(self):
        if self.reservas:
            result = "Reservas:\n"
            for numero, nome in self.reservas.items():
                result += f"{numero}: {nome}\n"
            return result
        else:
            return "Nenhuma reserva encontrada."

    def fazer_reserva(self, nome, numero):
        # nome_cliente = input("Digite o nome do cliente: ")
        # numero_quarto = input("Digite o número do quarto: ")

        # Verificar se o número do quarto já está reservado
        if numero in self.reservas:
            return f"Desculpe, o quarto {numero} já está reservado."
        else:
            self.reservas[numero] = nome
            return f"Reserva para {nome} no quarto {numero} realizada com sucesso."
            

    def cancelar_reserva(self, numero):
        # numero_quarto = input("Digite o número do quarto para cancelar a reserva: ")

        # Verificar se o número do quarto está reservado
        if numero in self.reservas:
            nome_cliente = self.reservas.pop(numero)
            return f"Reserva para {nome_cliente} no quarto {numero} cancelada com sucesso."
        else:
            return f"Desculpe, o quarto {numero} não está reservado."
