from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from .models import Especialista, DiaSemana, Agenda, Horario
from .serializers import EspecialistaSerializer, DiaSemanaSerializer, AgendaSerializer, HorarioSerializer

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Lista todos os especialistas."))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Cadastra um especialista (Apenas Admin)."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Busca um especialista pelo ID."))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Atualiza um especialista (Apenas Admin)."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_description="Atualiza parcialmente um especialista (Apenas Admin)."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Exclui um especialista (Apenas Admin)."))
class EspecialistaViewSet(viewsets.ModelViewSet):
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer

    def get_permissions(self):
        # Apenas Admins podem criar, editar ou deletar. 
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Lista os dias da semana disponíveis no sistema."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Busca um dia da semana pelo ID."))
class DiaSemanaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiaSemana.objects.all()
    serializer_class = DiaSemanaSerializer
    permission_classes = [permissions.IsAuthenticated]

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Lista todas as agendas."))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Cria uma agenda (Apenas Admin). Os horários são gerados automaticamente."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Busca uma agenda pelo ID."))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Atualiza uma agenda (Apenas Admin)."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_description="Atualiza parcialmente uma agenda (Apenas Admin)."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Exclui uma agenda (Apenas Admin)."))
class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def get_permissions(self):
        # Apenas Admins podem mexer na estrutura das agendas
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Lista os horários disponíveis e reservados."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Busca os detalhes de um horário específico."))
class HorarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Horario.objects.all().order_by('data', 'hora')
    serializer_class = HorarioSerializer
    permission_classes = [permissions.IsAuthenticated]

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

    # Rota customizada de reserva
    @swagger_auto_schema(operation_description="Reserva um horário disponível para o paciente logado. Previne dupla reserva.")
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def reservar(self, request, pk=None):
        # transaction.atomic() garante que o banco só vai salvar se nada der errado no meio do caminho
        with transaction.atomic():
            try:
                # Se duas pessoas clicarem no mesmo milissegundo, o banco manda a segunda pessoa esperar na fila
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
            horario.paciente = request.user
            horario.save()

        # Devolve o objeto atualizado
        serializer = self.get_serializer(horario)
        return Response(serializer.data, status=status.HTTP_200_OK)