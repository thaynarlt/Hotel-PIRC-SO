import socket

class GestorReservas:
    def __init__(self):
        self.reservas = {}
        self.server_address = ('localhost', 12345)  # Use o mesmo endereço e porta do servidor

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
        # Envia comando GET para o servidor
        self.enviar_comando('GET')

    def fazer_reserva(self):
        nome_cliente = input("Digite o nome do cliente: ")
        numero_quarto = input("Digite o número do quarto: ")

        # Envia comando CWD para o servidor
        self.enviar_comando(f'CWD {nome_cliente} {numero_quarto}')

    def cancelar_reserva(self):
        numero_quarto = input("Digite o número do quarto para cancelar a reserva: ")

        # Envia comando QUIT para o servidor
        self.enviar_comando(f'QUIT {numero_quarto}')

    def enviar_comando(self, comando):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(comando.encode())
            data = s.recv(1024)

        print('Resposta do servidor:', data.decode())

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
