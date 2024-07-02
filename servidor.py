import grpc
from concurrent import futures
import time
import reservasalas_pb2
import reservasalas_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

class ReservaSalasServicer(reservasalas_pb2_grpc.ReservaSalasServicer):

    def __init__(self):
        self.reservas = {}

    def CadastrarReserva(self, request, context):
       
        # Convertendo o Timestamp para string formatada de data e hora
        data_hora_str = request.data_hora.ToDatetime().strftime("%d-%m-%Y %H:%M")
        key = (request.sala, data_hora_str)

        # Verificando se a sala já está reservada para este horário
        if key in self.reservas:
            return reservasalas_pb2.ReservaResponse(mensagem="Sala já reservada para este horário", sucesso=False)
        
        # Registra a reserva na sala
        self.reservas[key] = request.usuario
        return reservasalas_pb2.ReservaResponse(mensagem="Reserva efetuada com sucesso", sucesso=True)

    def RemoverReserva(self, request, context):
        data_hora_str = request.data_hora.ToDatetime().strftime("%d-%m-%Y %H:%M")
        key = (request.sala, data_hora_str)
        if key in self.reservas:
            del self.reservas[key]
            return reservasalas_pb2.ReservaResponse(mensagem="Reserva removida com sucesso", sucesso=True)
        else:
            return reservasalas_pb2.ReservaResponse(mensagem="Reserva não encontrada", sucesso=False)

    def ConsultarReserva(self, request, context):
        data_hora_str = request.data_hora.ToDatetime().strftime("%d-%m-%Y %H:%M")
        key = (request.sala, data_hora_str)
        if key in self.reservas:
            return reservasalas_pb2.ConsultaResponse(mensagem="Sala reservada", reservada=True)
        else:
            return reservasalas_pb2.ConsultaResponse(mensagem="Sala disponível", reservada=False)

    def ConsultarReservasSala(self, request, context):
        usuarios = [usuario for (sala, _), usuario in self.reservas.items() if sala == request.sala]
        return reservasalas_pb2.ReservasSalaResponse(usuarios=usuarios)

    def ConsultarReservasUsuario(self, request, context):
        try:
            reservas_usuario = [reservasalas_pb2.ReservaInfo(
                sala=sala, 
                data_hora=self._convert_to_timestamp(data_hora_str)
            ) for (sala, data_hora_str), usuario in self.reservas.items() if usuario == request.usuario]
        
            return reservasalas_pb2.ReservasUsuarioResponse(reservas=reservas_usuario)        
        
        except Exception as e:
            context.set_details(f"Erro ao consultar reservas do usuário no servidor: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return reservasalas_pb2.ReservasUsuarioResponse(reservas=[])

    def _convert_to_timestamp(self, date_str):
        dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reservasalas_pb2_grpc.add_ReservaSalasServicer_to_server(ReservaSalasServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Iniciando servidor")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
