from rest_framework import serializers
from .models import Especialista, DiaSemana, Agenda, Horario
from .services import gerar_horarios_para_agenda

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = '__all__'

class DiaSemanaSerializer(serializers.ModelSerializer):
    # Representação em texto para ficar legível no JSON da API
    nome_dia = serializers.CharField(source='get_dia_display', read_only=True)
    
    class Meta:
        model = DiaSemana
        fields = ['id', 'dia', 'nome_dia']

class HorarioSerializer(serializers.ModelSerializer):
    # Adiciona o nome do Médico direto no horário
    especialista_nome = serializers.CharField(source='agenda.especialista.nome', read_only=True)

    class Meta:
        model = Horario
        fields = ['id', 'data', 'hora', 'status', 'paciente', 'especialista_nome']
        read_only_fields = ['status', 'paciente'] # Protege para o usuário não burlar e criar horário já reservado

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'

    def create(self, validated_data):
        """
        Sobrescreve o método de criação para injetar o algoritmo
        de horários no momento em que a API recebe o POST.
        """
        # Extração dos campos
        dias_semana = validated_data.pop('dias_semana', [])
        
        # Cria a agenda principal no banco
        agenda = Agenda.objects.create(**validated_data)
        
        # Salva os dias da semana na tabela intermediária
        agenda.dias_semana.set(dias_semana)
        
        # Chama o serviço do algoritmo de horários
        gerar_horarios_para_agenda(agenda)
        
        return agenda