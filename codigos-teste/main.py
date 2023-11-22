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
            print("Reservas:")
            for numero, nome in self.reservas.items():
                print(f"{numero}: {nome}")
        else:
            print("Nenhuma reserva encontrada.")

    def fazer_reserva(self):
        nome_cliente = input("Digite o nome do cliente: ")
        numero_quarto = input("Digite o número do quarto: ")

        # Verificar se o número do quarto já está reservado
        if numero_quarto in self.reservas:
            print(f"Desculpe, o quarto {numero_quarto} já está reservado.")
        else:
            self.reservas[numero_quarto] = nome_cliente
            print(f"Reserva para {nome_cliente} no quarto {numero_quarto} realizada com sucesso.")

    def cancelar_reserva(self):
        numero_quarto = input("Digite o número do quarto para cancelar a reserva: ")

        # Verificar se o número do quarto está reservado
        if numero_quarto in self.reservas:
            nome_cliente = self.reservas.pop(numero_quarto)
            print(f"Reserva para {nome_cliente} no quarto {numero_quarto} cancelada com sucesso.")
        else:
            print(f"Desculpe, o quarto {numero_quarto} não está reservado.")

    def executar(self):
        while True:
            self.exibir_menu()

            opcao = input("Escolha uma opção (1-4): ")

            if opcao == "1":
                self.ver_reservas()
            elif opcao == "2":
                self.fazer_reserva()
            elif opcao == "3":
                self.cancelar_reserva()
            elif opcao == "4":
                print("Saindo do programa. Obrigado!")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    gestor = GestorReservas()
    gestor.executar()
