from rest_framework import serializers
from .models import Especialista, DiaSemana, Agenda, Horario
from datetime import timedelta
from .services import gerar_horarios_para_agenda

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = '__all__'

class DiaSemanaSerializer(serializers.ModelSerializer):
    # Representação em texto para ficar legível no JSON
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

    def validate(self, data):
        """ 
        Impede que o mesmo especialista tenha agendas com datas sobrepostas ou invalidas.
        """
        especialista = data.get('especialista')
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')
        dias_semana = data.get('dias_semana', [])
        hora_inicio = data.get('hora_inicio') 
        hora_fim = data.get('hora_fim')

        # A data final não pode ser no passado da inicial.
        if data_fim < data_inicio:
            raise serializers.ValidationError({
                "data_fim": "A data final não pode ser anterior à data de início."
            })

        # O final do horario da consulta nao pode ser no passado do inicial.
        if hora_fim <= hora_inicio:
            raise serializers.ValidationError({
                "erro": "A hora final deve ser maior que a hora de início."
            })

        # Verifica se os dias marcados existem no intervalo.
        dias_totais = (data_fim - data_inicio).days + 1
        
        if dias_totais < 7:
            # Pega os números dos dias que realmente existem nesse intervalo.
            dias_reais = set((data_inicio + timedelta(days=i)).weekday() for i in range(dias_totais))
            
            # Pega os números dos dias que o Admin marcou no frontend.
            dias_selecionados = set(ds.dia for ds in dias_semana)
            
            # Faz a interseção, se for vazio, os dias sao invalidos.
            if not dias_reais.intersection(dias_selecionados):
                raise serializers.ValidationError({
                    "dias_semana": "Os dias da semana selecionados não existem neste intervalo de datas. Verifique o calendário corretamente."
                })

        query = Agenda.objects.filter(
            especialista=especialista,
            data_inicio__lte=data_fim,
            data_fim__gte=data_inicio,
            hora_inicio__lt=hora_fim,
            hora_fim__gt=hora_inicio
        )
        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise serializers.ValidationError({
                "erro": "Este especialista já possui uma agenda que conflita com este período."
            })

        return data

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