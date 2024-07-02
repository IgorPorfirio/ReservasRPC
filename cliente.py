import grpc
import reservasalas_pb2
import reservasalas_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import traceback

def create_timestamp(date_str, time_str):
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp
    except ValueError as e:
        print(f"Erro no formato da data/hora: {e}")
        return None

def cadastrar_reserva(stub):
    try:
        usuario = input("Usuário: ")
        sala = input("Sala: ")
        data = input("Data (DD-MM-AAAA): ")
        hora = input("Hora (HH:MM): ")
        data_hora = create_timestamp(data, hora)

        if data_hora is None:
            print("Formato de data/hora inválido. Tente novamente.")
            return

        response = stub.CadastrarReserva(reservasalas_pb2.ReservaRequest(
            usuario=usuario, sala=sala, data_hora=data_hora))
        print(f"Cadastro: {response.mensagem} (sucesso: {response.sucesso})")
    except grpc.RpcError as e:
        print(f"Erro ao cadastrar reserva: {e.details()}")
        traceback.print_exc()

def remover_reserva(stub):
    try:
        usuario = input("Usuário: ")
        sala = input("Sala: ")
        data = input("Data (DD-MM-AAAA): ")
        hora = input("Hora (HH:MM): ")
        data_hora = create_timestamp(data, hora)

        if data_hora is None:
            print("Formato de data/hora inválido. Tente novamente.")
            return

        response = stub.RemoverReserva(reservasalas_pb2.ReservaRequest(
            usuario=usuario, sala=sala, data_hora=data_hora))
        print(f"Remoção: {response.mensagem} (sucesso: {response.sucesso})")
    except grpc.RpcError as e:
        print(f"Erro ao remover reserva: {e.details()}")
        traceback.print_exc()

def consultar_reserva(stub):
    try:
        sala = input("Sala: ")
        data = input("Data (DD-MM-AAAA): ")
        hora = input("Hora (HH:MM): ")
        data_hora = create_timestamp(data, hora)

        if data_hora is None:
            print("Formato de data/hora inválido. Tente novamente.")
            return

        response = stub.ConsultarReserva(reservasalas_pb2.ConsultaRequest(
            sala=sala, data_hora=data_hora))
        print(f"Consulta: {response.mensagem} (reservada: {response.reservada})")
    except grpc.RpcError as e:
        print(f"Erro ao consultar reserva: {e.details()}")
        

def consultar_reservas_sala(stub):
    try:
        sala = input("Sala: ")
        response = stub.ConsultarReservasSala(reservasalas_pb2.SalaRequest(sala=sala))
         
        if len(response.usuarios) == 0:
            print("A Sala não tem reservas.")
        else:
            print(f"Reservas na sala: {response.usuarios}")
        
    except grpc.RpcError as e:
        print(f"Erro ao consultar reservas da sala: {e.details()}")
        

def consultar_reservas_usuario(stub):
    try:
        usuario = input("Usuário: ")
        response = stub.ConsultarReservasUsuario(reservasalas_pb2.UsuarioRequest(usuario=usuario))
        
        if len(response.reservas) == 0:
            print("O Usuário não tem reservas.")
        else: 
            for reserva in response.reservas:
                data_hora = reserva.data_hora.ToDatetime().strftime("%d-%m-%Y %H:%M")
                print(f"Reserva: sala={reserva.sala}, data_hora={data_hora}")
    except grpc.RpcError as e:
        print(f"Erro ao consultar reservas do usuário: {e.details()}")
        

def menu():
    print("\n--- Menu de Operações ---")
    print("1: Cadastrar Reserva")
    print("2: Remover Reserva")
    print("3: Consultar Reserva")
    print("4: Consultar Reservas por Sala")
    print("5: Consultar Reservas por Usuário")
    print("0: Sair")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reservasalas_pb2_grpc.ReservaSalasStub(channel)

        while True:
            menu()
            opcao = input("Escolha uma opção: ")
            if opcao == '1':
                cadastrar_reserva(stub)
            elif opcao == '2':
                remover_reserva(stub)
            elif opcao == '3':
                consultar_reserva(stub)
            elif opcao == '4':
                consultar_reservas_sala(stub)
            elif opcao == '5':
                consultar_reservas_usuario(stub)
            elif opcao == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    run()
