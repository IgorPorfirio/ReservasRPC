# ReservasRPC
Trabalho da disciplina sistemas distribuídos para implementar um sistema de Reserva de Salas de Reunião com RPC ou WebServices, segundo os requísitos.


Trabalho
Reserva de Salas de Reunião com RPC ou WebServices
Objetivo:
Desenvolver uma aplicação distribuída, no paradigma cliente/servidor usando RPC ou
WebServices, para reserva de salas de reunião. A aplicação servidora pode armazenar os dados da
forma que o grupo achar mais simples de implementar e deverá fornecer uma API em RPC ou
WebServices para a manipulação das reservas. A aplicação cliente pode ser executada em linha de
comando ou ser uma interface gráfica simples, que vai utilizar os métodos fornecidos pela API do
servidor para apresentar dados ao usuário.
API do servidor RPC:
Segue abaixo a descrição dos métodos que devem ser implementados pelo servidor:
Nome: cadastrar_reserva
Parâmetros: usuario, sala, data, hora
Função: Deve verificar se a sala está disponível na data e hora. Em caso afirmativo, efetuar a reserva
para o usuário. Caso contrário, retornar mensagem de erro.
Nome: remover_reserva
Parâmetros: usuario, sala, data, hora
Função: Deve verificar se a sala está reservada na data e hora para o usuário. Em caso afirmativo,
remover a reserva para o usuário. Caso contrário, retornar mensagem de erro.
Nome: consultar_reserva
Parâmetros: sala, data, hora
Função: Deve retornar se a sala está reservada na data e hora informados.
Nome: consultar_reservas_sala
Parêmtros: sala
Função: Deve retornar uma lista com todos os usuários que fizeram/possuem reserva para a sala.
Nome: consultar_reservas_usuario
Parâmetros: usuário
Função: Deve retorna uma lista com todas as reservas de salas realizadas pelo usuário.
Cliente:
A aplicação cliente pode ser uma interface (texto ou gráfica) que permita executar cada um
dos tipos de funções disponíveis na API. No caso de WebServices, pode ser também uma página Web.
