from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Especialista, DiaSemana, Agenda, Horario
from .serializers import EspecialistaSerializer, DiaSemanaSerializer, AgendaSerializer, HorarioSerializer

class EspecialistaViewSet(viewsets.ModelViewSet):
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer

class DiaSemanaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiaSemana.objects.all()
    serializer_class = DiaSemanaSerializer

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

class HorarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Paciente só tem permissão de leitura (ReadOnly).
    Só tem permissão de escrita na rota customizada "reservar".
    """
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

    # Sobrescreve o get_queryset para permitir os filtros na URL do frontend
    def get_queryset(self):
        queryset = super().get_queryset()
        especialista_id = self.request.query_params.get('especialista_id')
        status_param = self.request.query_params.get('status')
        
        if especialista_id:
            queryset = queryset.filter(agenda__especialista_id=especialista_id)
        
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        return queryset

    # Cria a rota customizada de reserva
    @action(detail=True, methods=['patch'])
    def reservar(self, request, pk=None):
        # transaction.atomic() garante que o banco só vai salvar se nada der errado no meio do caminho
        with transaction.atomic():
            try:
                # Se duas pessoas clicarem no mesmo milissegundo, o banco manda a segunda pessoa esperar na fila.
                horario = Horario.objects.select_for_update().get(pk=pk)
            except Horario.DoesNotExist:
                return Response({"erro": "Horário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # Verifica se a pessoa que esperou na fila pegou o horário já reservado
            if horario.status == 'reservado':
                return Response(
                    {"erro": "Este horário já foi reservado por outro paciente."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Efetiva a reserva
            horario.status = 'reservado'
            # Se o paciente estiver logado com JWT, vincula ele. Senão, fica None por enquanto.
            horario.paciente = request.user if request.user.is_authenticated else None
            horario.save()

        # Devolve o objeto atualizado
        serializer = self.get_serializer(horario)
        return Response(serializer.data, status=status.HTTP_200_OK)