# Projeto Integrador  HRP - Documentação

Criado em: December 20, 2023 11:40 AM

> O código inteiro ja está documentado, esse PDF é apenas um complemento.
> 

## Documentação do Código  `clientehrp.py`

1. **Conexão ao servidor:**
    
    ```python
    serv = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(serv)
    ```
    
    - Cria um objeto de soquete (**`sock`**) e o conecta ao servidor usando o endereço IP (**`HOST`**) e a porta (**`PORT`**).
2. **Loop principal:**
    
    ```python
    while True:
    ```
    
    - Inicia um loop infinito que só será interrompido quando o cliente decidir encerrar a conexão.
3. **Exibição do menu e entrada do usuário:**
    
    ```python
    menu_str = menu.exibir_menu()
    seletor = input('\033[1;34m'+'HRP> ')
    ```
    
    - Exibe o menu usando a função **`exibir_menu`** e aguarda a entrada do usuário.
4. **Envio do código selecionado para o servidor:**
    
    ```python
    sock.send(str.encode(seletor))
    ```
    
    - Envia o código da opção selecionada pelo usuário para o servidor.
5. **Processamento da opção do usuário:**
    
    ```python
    match seletor:
        case '1':
            # ...
        case '2':
            # ...
        # ... (casos para as opções 3, 4, 5, 6)
        case _:
            # ...
    ```
    
    - Utiliza a nova estrutura **`match`** do Python 3.10 para lidar com diferentes opções selecionadas pelo usuário.
    - Códigos basicamente iguais em que correspondem ao menu estabilizado no “main.py”
        
        ```python
        match seletor:
            case '1':
                reservas_feitas = sock.recv(TAM_MSG).decode()
                print(reservas_feitas)
        ```
        
        - Se o **`seletor`** for igual a '1', isso significa que o usuário escolheu a opção para ver as reservas feitas. O cliente recebe a resposta do servidor (reservas feitas) e imprime na tela.
        
        ```python
           case '2':
                quartos_disponiveis = sock.recv(TAM_MSG).decode()
                print(quartos_disponiveis)
        ```
        
        - Se o **`seletor`** for igual a '2', o usuário deseja ver os quartos disponíveis para reserva. O cliente recebe a resposta do servidor (quartos disponíveis) e imprime na tela.
        
        ```python
            case '3':
                nome = input("Digite o nome do cliente: ")
                while not nome.isalpha():
                    print("Por favor, digite um nome válido contendo apenas letras. (Code 30 -ERR)")
                    nome = input("Digite o nome do cliente: ")
                sock.send(str.encode(nome))
        
                quarto = input("Digite o número do quarto: ")
                while not quarto or not quarto.isnumeric():
                    print("Por favor, digite um número inteiro. (Code 30 -ERR)")
                    quarto = input("Digite o número do quarto: ")
        
                sock.send(str.encode(quarto))
                print('Processando reserva...')
                resposta = sock.recv(TAM_MSG).decode()
                print(resposta)
        ```
        
        - Se o **`seletor`** for igual a '3', o usuário deseja fazer uma reserva. O cliente coleta o nome do cliente e o número do quarto, valida as entradas e as envia para o servidor. O cliente recebe uma resposta do servidor (indicando o resultado da operação) e imprime na tela.
        
        ```python
            case '4':
                numero = input("Digite o número do quarto para cancelar a reserva: ")
                while not numero or not numero.isnumeric():
                    print("Por favor, digite um número inteiro. (Code 30 -ERR)")
                    numero = input("Digite o número do quarto para cancelar a reserva: ")
        
                sock.send(str.encode(numero))
                resposta = sock.recv(TAM_MSG).decode()
                print(resposta)
        ```
        
        - Se o **`seletor`** for igual a '4', o usuário deseja cancelar uma reserva. O cliente coleta o número do quarto a ser cancelado, valida a entrada e envia para o servidor. O cliente recebe uma resposta do servidor e imprime na tela.
        
        ```python
            case '5':
                dicionario = sock.recv(TAM_MSG).decode()
                print(dicionario)
        ```
        
        - Se o **`seletor`** for igual a '5', o usuário deseja ver o dicionário de códigos da aplicação. O cliente recebe a resposta do servidor (dicionário) e imprime na tela.
        
        ```python
          	case '6':
                print('Até mais!')
                sock.close()
                break
        ```
        
        - Se o **`seletor`** for igual a '6', o usuário deseja encerrar a sessão. O cliente imprime uma mensagem de despedida, fecha a conexão com o servidor e quebra o loop.
        
        ```python
           case _:
               print("Opção inválida. (Code 30 -ERR)")
        ```
        
        - Se o **`seletor`** não corresponder a nenhum dos casos anteriores, imprime uma mensagem de erro indicando que a opção é inválida.
        
        Essa estrutura **`match`** torna o código mais legível e estruturado, melhorando a manutenção e a compreensão do fluxo de controle do programa.
        
6. **Lógica para cada opção:**
    - Cada opção do menu (de 1 a 6) tem uma lógica associada, como exibir reservas, quartos disponíveis, fazer reserva, cancelar reserva, ver dicionário de códigos e encerrar a sessão.
7. **Encerramento da conexão:**
    
    ```python
    sock.close()
    break
    ```
    
    - Fecha a conexão com o servidor e quebra o loop infinito quando o usuário escolhe encerrar a sessão.
8. **Tratamento de opção inválida:**
    
    ```python
    case _:
        print("Opção inválida. (Code 30 -ERR)")
    ```
    
    - Se o código fornecido pelo cliente não corresponder a nenhuma opção válida, imprime uma mensagem de erro.
    
    ---
    
    ## Documentação do Código  `servidorhrp.py`
    
    ### **Criação do Objeto Menu:**
    
    ```python
    menu = GestorReservas()
    ```
    
    - Criação de um objeto **`menu`** usando a classe ou função **`GestorReservas`**. Esse objeto é compartilhado entre todos os clientes, funcionando como uma espécie de banco de dados centralizado.
    
    ### **Dicionário de Tradução de Códigos:**
    
    ```python
    funcoes = {'1': 'requisição para ver os quartos já reservados.',
               '2': 'requisição para ver os quartos disponíveis.',
               '3': 'requisição para fazer uma reserva.',
               '4': 'requisição para cancelar uma reserva.',
               '5': 'requisição para consulta do dicionário de códigos'}
    ```
    
    - **`funcoes`**: Dicionário usado para traduzir os códigos enviados pelos clientes para mensagens legíveis no log do servidor.
    
    ### **Função para Processar Mensagens do Cliente:**
    
    ```python
    def processa_msg_cliente(msg, con, cliente):
        # ... (veja abaixo)
    ```
    
    - Função que processa as requisições enviadas pelos clientes, utilizando o código enviado na mensagem para acionar sua respectiva função.
    
    ### Estrutura **`match`**:
    
    ```python
    match msg:
        case '1':
            # ...
        case '2':
            # ...
        # ... (casos para as opções 3, 4, 5)
        case _:
            # ...
    ```
    
    - Estrutura de decisão **`match`** para identificar a funcionalidade requisitada pelo cliente com base no código enviado.
    
    A estrutura **`match`** é uma construção de controle de fluxo introduzida no Python 3.10, que fornece uma maneira mais expressiva e concisa de lidar com várias comparações de padrões. No seu código, a estrutura **`match`** é utilizada para verificar o valor da variável **`msg`** (código enviado pelo cliente) e realizar ações específicas com base nesse valor. Vamos analisar cada **`case`**:
    
    ```python
    match msg:
        case '1':
            # ...
        case '2':
            # ...
        # ... (casos para as opções 3, 4, 5)
        case _:
            # ...
    ```
    
    - **`case '1':`**: Se o valor de **`msg`** for igual a '1', significa que o cliente deseja ver as reservas já feitas. O código associado a este caso realiza o seguinte:
        
        ```python
        reservas = menu.ver_reservas()
        con.send(str.encode(reservas))
        ```
        
        - **`menu.ver_reservas()`**: Chama a função **`ver_reservas`** do objeto **`menu`** (que é uma instância da classe **`GestorReservas`**) para obter uma string representando as reservas feitas.
        - **`con.send(str.encode(reservas))`**: Envia essa string ao cliente, codificada em bytes.
    - **`case '2':`**: Se o valor de **`msg`** for igual a '2', o cliente deseja ver os quartos disponíveis para reserva. O código associado a este caso realiza o seguinte:
        
        ```python
        quartos = menu.ver_quartos_disponiveis()
        con.send(str.encode(quartos))
        ```
        
        - **`menu.ver_quartos_disponiveis()`**: Chama a função **`ver_quartos_disponiveis`** do objeto **`menu`** para obter uma string representando os quartos disponíveis.
        - **`con.send(str.encode(quartos))`**: Envia essa string ao cliente.
    - **`case '3':`**: Se o valor de **`msg`** for igual a '3', o cliente deseja fazer uma reserva. O código associado a este caso realiza o seguinte:
        
        ```python
        nome = con.recv(TAM_MSG).decode()
        numero = con.recv(TAM_MSG).decode()
        resposta = menu.fazer_reserva(nome, numero)
        con.send(str.encode(resposta))
        ```
        
        - **`con.recv(TAM_MSG)`**: Recebe dados do cliente (o nome e o número do quarto) e decodifica para string.
        - **`menu.fazer_reserva(nome, numero)`**: Chama a função **`fazer_reserva`** do objeto **`menu`**, passando o nome e o número do quarto como parâmetros, e obtém uma resposta indicando o status da reserva.
        - **`con.send(str.encode(resposta))`**: Envia essa resposta ao cliente.
    - **`case '4':`**: Se o valor de **`msg`** for igual a '4', o cliente deseja cancelar uma reserva. O código associado a este caso realiza o seguinte:
        
        ```python
        numero = con.recv(TAM_MSG).decode()
        resposta = menu.cancelar_reserva(numero)
        con.send(str.encode(resposta))
        ```
        
        - **`con.recv(TAM_MSG)`**: Recebe o número do quarto do cliente e decodifica para string.
        - **`menu.cancelar_reserva(numero)`**: Chama a função **`cancelar_reserva`** do objeto **`menu`**, passando o número do quarto como parâmetro, e obtém uma resposta indicando o status do cancelamento.
        - **`con.send(str.encode(resposta))`**: Envia essa resposta ao cliente.
    - **`case '5':`**: Se o valor de **`msg`** for igual a '5', o cliente deseja ver o dicionário de códigos da aplicação. O código associado a este caso realiza o seguinte:
        
        ```python
        dicionario = menu.ver_dicionario()
        con.send(str.encode(dicionario))
        ```
        
        - **`menu.ver_dicionario()`**: Chama a função **`ver_dicionario`** do objeto **`menu`** para obter uma string representando o dicionário de códigos.
        - **`con.send(str.encode(dicionario))`**: Envia essa string ao cliente.
    - **`case _: (underscore)`**: Este é o caso padrão, que é acionado quando **`msg`** não corresponde a nenhum dos casos anteriores. O código associado a este caso realiza o seguinte:
        
        ```python
        print("Opção inválida. (Code 30 -ERR)")
        ```
        
        - Imprime uma mensagem de erro indicando que a opção é inválida.
        
        Essencialmente, a estrutura **`match`** e os **`cases`** fornecem uma maneira mais clara de lidar com diferentes opções baseadas no valor de **`msg`**, melhorando a legibilidade e a manutenção do código.
        
    
    ### Processamento de Cada Opção:
    
    - Cada **`case`** dentro da estrutura **`match`** representa uma opção do menu.
    
    ### **Função para Processar Cliente:**
    
    ```python
    def processa_cliente(con, cliente):
        # ... (veja abaixo)
    ```
    
    - Função que processa os clientes que se conectam ao servidor.
        
        A função **`processa_cliente`** é responsável por lidar com a comunicação entre o servidor e um cliente específico. Vamos analisar cada parte da função:
        
        ```python
        def processa_cliente(con, cliente):
            print(f'Cliente conectado {cliente}  (Code 20 -OK)')
            while True:
                msg = con.recv(TAM_MSG)
                msg = msg.decode()
                if msg == '6':
                    print(f'Cliente {cliente} encerrou a conexão (Code 20 -OK)')
                    break
                processa_msg_cliente(msg, con, cliente)
        ```
        
        - **`print(f'Cliente conectado {cliente} (Code 20 -OK)')`**: Imprime uma mensagem indicando que um cliente foi conectado com sucesso, mostrando o endereço e porta do cliente. O código **`(Code 20 -OK)`** é uma espécie de identificação ou status que pode ser usado para rastrear eventos no log do servidor.
        - **`while True:`**: Inicia um loop infinito para escutar continuamente as mensagens enviadas pelo cliente.
        - **`msg = con.recv(TAM_MSG)`**: Recebe dados do cliente por meio do socket de conexão (**`con`**). **`TAM_MSG`** representa o tamanho máximo da mensagem que pode ser recebida de uma vez.
        - **`msg = msg.decode()`**: Converte os dados recebidos, que estão em formato de bytes, para uma string decodificada. O protocolo usado parece indicar que as mensagens são strings codificadas em UTF-8.
        - **`if msg == '6':`**: Verifica se a mensagem recebida do cliente é igual a '6'. No seu código, o valor '6' é associado à opção de encerrar a conexão. Se essa condição for verdadeira, o cliente solicitou encerrar a conexão.
            - **`print(f'Cliente {cliente} encerrou a conexão (Code 20 -OK)')`**: Imprime uma mensagem indicando que o cliente se desconectou, mostrando o endereço e porta do cliente. O código **`(Code 20 -OK)`** é novamente usado para indicar um status no log do servidor.
            - **`break`**: Sai do loop, encerrando a execução da função **`processa_cliente`**.
        - **`processa_msg_cliente(msg, con, cliente)`**: Se a mensagem recebida não for '6', chama a função **`processa_msg_cliente`** para processar a mensagem. Esta função recebe a mensagem, o socket de conexão e as informações do cliente como parâmetros.
        
        A função **`processa_cliente`** basicamente estabelece uma comunicação contínua entre o servidor e um cliente específico, recebendo mensagens do cliente, identificando se é uma solicitação para encerrar a conexão e chamando a função **`processa_msg_cliente`** para lidar com as outras opções do cliente. Esse design permite que o servidor lide com vários clientes simultaneamente, já que cada cliente é manipulado em uma thread separada.
        
    
    ### **Lógica Principal do Servidor:**
    
    ```python
    def main():
        # ... (veja abaixo)
    ```
    
    - Função principal para rodar o servidor.
    
    ### Criação do Servidor:
    
    ```python
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv = (HOST, PORT)
    sock.bind(serv)
    sock.listen(50)
    ```
    
    - Criação de um servidor TCP usando sockets, vinculando-o a um endereço IP e porta específicos e configurando-o para ouvir até 50 conexões pendentes.
    
    ### Loop Infinito para Aceitar Clientes:
    
    ```python
    while True:
        try:
            con, cliente = sock.accept()
            threading.Thread(target=processa_cliente, args=(con, cliente)).start()
        except Exception as e:
            print('Erro ao aceitar a conexão:', e, ' (Code 60 -ERR)')
    ```
    
    - Loop infinito para aceitar clientes. Cria uma nova thread para lidar com cada cliente que se conecta.
    
    ### **Execução do Servidor:**
    
    ```python
    if __name__ == "__main__":
        main()
    ```
    
    - Execução da função **`main()`** quando o script é executado diretamente.
    
    ## **Observações Gerais:**
    
    - O código implementa um servidor que gerencia reservas de quartos de hotel para vários clientes simultaneamente.
    - Usa threads para lidar com múltiplos clientes ao mesmo tempo.
    - O objeto **`menu`** compartilhado entre os clientes funciona como uma espécie de banco de dados centralizado.
    - O dicionário **`funcoes`** traduz códigos enviados pelos clientes para mensagens legíveis no log do servidor.
    - A estrutura **`match`** é utilizada para tomar decisões com base nos códigos enviados pelos clientes.
    - Cada função relacionada a uma opção do menu é chamada e processada conforme a escolha do cliente.
    - O servidor escuta em todas as interfaces de rede disponíveis (0.0.0.0) na porta 40000.
    
    ---
    
    ## Documentação do Código  `main.py`
    
    Analisando cada parte da classe `GestorReservas` e sua interação com a função `processa_msg_cliente`:
    
    ```python
    class GestorReservas:
        def __init__(self):
            # ... (código anterior)
    
        def exibir_menu(self):
            # ... (código anterior)
    
        def ver_reservas(self):
            global mutex
            mutex.acquire()
            if self.reservas:
                result = "Reservas:\\n"
                for numero, nome in self.reservas.items():
                    result += f"Quarto {numero} reservado para {nome}. (Code 20 -OK)\\n"
                mutex.release()
                return result
            else:
                mutex.release()
                return "Nenhuma reserva encontrada. (Code 20 -OK)"
    
        def ver_quartos_disponiveis(self):
            global mutex
            mutex.acquire()
            if self.quartos:
                self.quartos.sort()
                result = "Quartos disponiveis: " + ', '.join(map(str, self.quartos)) + ' (Code 20 -OK)'
                mutex.release()
                return result
            else:
                mutex.release()
                return "Não possuímos nenhum quarto disponível no momento. (Code 20 -OK)"
    
        def fazer_reserva(self, nome, numero):
            global mutex
            mutex.acquire()
            if numero in self.reservas:
                mutex.release()
                return f"Desculpe, o quarto {numero} já está reservado. (Code 40 -ERR)"
            elif int(numero) not in self.quartos:
                mutex.release()
                return f"Número de quarto inexistente. (Code 30 -ERR)"
            else:
                self.reservas[numero] = nome
                self.quartos.remove(int(numero))
                mutex.release()
                return f"Reserva para {nome} no quarto {numero} realizada com sucesso. (Code 20 -OK)"
    
        def cancelar_reserva(self, numero):
            global mutex
            mutex.acquire()
            if numero in self.reservas:
                nome_cliente = self.reservas.pop(numero)
                self.quartos.append(int(numero))
                mutex.release()
                return f"Reserva para {nome_cliente} no quarto {numero} cancelada com sucesso. (Code 20 -OK)"
            else:
                mutex.release()
                return f"Desculpe, o quarto {numero} não está reservado ou não existe. (Code 30 -ERR)"
    
        def ver_dicionario(self):
            result = "Dicionário de código: (Code 20 -OK)\\n"
            for codigo, descricao in self.codigos.items():
                result += f"Código {codigo} = {descricao}\\n"
            return result
    ```
    
    A classe `GestorReservas` possui métodos que encapsulam diferentes funcionalidades do sistema de reservas. Cada método é projetado para executar uma operação específica, garantindo que a exclusão mútua seja aplicada quando necessário para evitar condições de corrida.
    
    - **`ver_reservas(self):`**: Mostra as reservas feitas. Adquire o semáforo (`mutex`) para garantir a exclusão mútua ao acessar dados críticos, como o dicionário de reservas (`self.reservas`). Se há reservas, cria uma string formatada com as reservas. Caso contrário, retorna uma mensagem indicando a ausência de reservas. Libera o semáforo antes de retornar.
    - **`ver_quartos_disponiveis(self):`**: Mostra os quartos disponíveis. Adquire o semáforo (`mutex`) para garantir a exclusão mútua ao acessar dados críticos, como a lista de quartos disponíveis (`self.quartos`). Se há quartos disponíveis, cria uma string formatada com a lista de quartos. Caso contrário, retorna uma mensagem indicando a ausência de quartos disponíveis. Libera o semáforo antes de retornar.
    - **`fazer_reserva(self, nome, numero):`**: Faz uma reserva. Adquire o semáforo (`mutex`) para garantir a exclusão mútua ao acessar dados críticos, como o dicionário de reservas (`self.reservas`) e a lista de quartos disponíveis (`self.quartos`). Verifica se o quarto já está reservado e se o número do quarto é válido. Se tudo estiver correto, realiza a reserva e atualiza a lista de quartos disponíveis. Libera o semáforo antes de retornar.
    - **`cancelar_reserva(self, numero):`**: Cancela uma reserva. Adquire o semáforo (`mutex`) para garantir a exclusão mútua ao acessar dados críticos, como o dicionário de reservas (`self.reservas`) e a lista de quartos disponíveis (`self.quartos`). Verifica se o quarto está reservado. Se estiver, cancela a reserva e atualiza a lista de quartos disponíveis. Libera o