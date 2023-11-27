import threading
import socket
import time

TAM_MSG = 1024
HOST = '26.65.86.237' #IP
PORT = 40000


def cliente_simulado(client_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        # Simulando uma operação qualquer (exemplo: fazer reserva)
        sock.send(str.encode('2'))
        time.sleep(1)
        nome = f"Cliente{client_id}"
        sock.send(str.encode(nome))
        quarto = '101'  # Número do quarto
        sock.send(str.encode(quarto))

        resposta = sock.recv(TAM_MSG).decode()
        print(f"Cliente{client_id}: {resposta}")

    except Exception as e:
        print(f"Erro no Cliente{client_id}: {e}")
    finally:
        sock.close()

# Número de clientes simulados
num_clientes = 20

# Iniciando várias threads simulando clientes concorrentes
threads_clientes = []
for i in range(num_clientes):
    cliente_thread = threading.Thread(target=cliente_simulado, args=(i,))
    threads_clientes.append(cliente_thread)
    cliente_thread.start()

# Aguardando todas as threads terminarem
for thread in threads_clientes:
    thread.join()

print("Teste de stress concluído.")