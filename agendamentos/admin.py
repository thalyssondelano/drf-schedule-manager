from django.contrib import admin
from .models import Especialista, DiaSemana, Agenda, Horario

@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'especialidade')
    search_fields = ('nome',)

@admin.register(DiaSemana)
class DiaSemanaAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_dia_display')

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'especialista', 'data_inicio', 'data_fim', 'vagas_por_dia', 'ativa')
    list_filter = ('ativa', 'especialista')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'agenda', 'data', 'hora', 'status', 'paciente')
    list_filter = ('status', 'data', 'agenda__especialista')