# Hotel Reservation Protocol

Projeto integrado das disciplinas Sistemas Operacionais e Protocolos de Interconexão de Redes de Computadores.<br>
<strong>Professores:</strong> Gustavo Wagner Diniz Mendes e Leonidas Francisco de Lima Júnior<br>
<strong>Alunos:</strong> Silas Leao Rocha Albuquerque e Thayná Rodrigues Lopes Tolentino

## 🚀 Descrição e Pré-requisitos de Instalação

Atender de forma simultânea clientes que podem fazer reservas de quartos de hotéis, como também solicitar do servidor os quartos da lista que já estão reservados.

Pacotes/Bibliotecas que precisam ser instalados, o propósito de cada um deles e como instalá-los antes de executar o código:
<!--Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto. !-->
```
import socket
import os
import threading
import sys
```

## 📋 Pré-requisitos do Projeto
<ul>
  <li>Desenvolvimento de um aplicativo distribuído em uma arquitetura cliente/servidor</li>
  <li>Usando estruturas de dados e a lógica implementada com base na API de Sockets</li>
  <li>Deverá usar um protocolo de aplicação para realizar a comunicação</li>
  <li>Servidor deverá ser capaz de atender, de forma simultânea, a diversas instâncias de clientes que solicitem os seus serviços.</li>
  <li>Identificar dados que podem causar condições de corrida se acessados simultaneamente</li>
  <li>Usar um protocolo de transporte (UDP ou TCP dependendo da aplicação)</li>
</ul>


### 🔧 Arquivos do Projeto

Tabela contendo o nome de cada arquivo e uma descrição sobre o seu papel (responsabilidade) na aplicação;<br>

<strong>_clientehrp.py_ :</strong> Contém o código do cliente que irá interagir com o Servidor

```
clientehrp.py
```
<strong>_main.py_ :</strong> Contém o código do Menu disponível ao Cliente que deseja realizar alguma ação no Hotel
```
main.py
```
<strong>_servidorhrp.py_ :</strong> Contém o código do Servidor que irá interagir com os diversos Clientes
```
servidorhrp.py
```
---
## ⚙️ Protocolo de Aplicação

Documentação de cada uma das mensagens utilizadas no protocolo, indicando os parâmetros enviados e as respostas a serem devolvidas;

## 🔩 Instruções para execução

Passo a passo para colocar a aplicação cliente/servidor para rodar:

_Abra um terminal e execute o código do Servidor:_
```
python .\servidorhrp.py
```
_Abra outro terminal e execute o código do cliente:_
```
python .\cliente-hrp.py (IP do servidor)
```
---

## 📄 Licença

Este projeto está sob a licença (MIT) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

Feito por
[Silas Leão](https://github.com/SilasLeao) e 
[Thayná Tolentino](https://github.com/thaynarlt)
