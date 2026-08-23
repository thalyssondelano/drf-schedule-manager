from datetime import datetime, timedelta, date
from .models import Agenda, Horario

def gerar_horarios_para_agenda(agenda: Agenda):
    """
    Lê a agenda, calcula a duração das frações e gera os slots no banco
    """
    # Lista de dias da semana
    dias_permitidos = list(agenda.dias_semana.values_list('dia', flat=True))
    
    # Duração de cada slot em minutos
    hora_inicio_dt = datetime.combine(date.today(), agenda.hora_inicio)
    hora_fim_dt = datetime.combine(date.today(), agenda.hora_fim)
    
    minutos_totais = (hora_fim_dt - hora_inicio_dt).total_seconds() / 60
    
    if agenda.vagas_por_dia <= 0 or minutos_totais <= 0:
        return
        
    duracao_slot_minutos = minutos_totais / agenda.vagas_por_dia
    
    horarios_para_criar = []
    
    # Iteração sobre o intervalo de datas (data_inicio até data_fim)
    dia_atual = agenda.data_inicio
    while dia_atual <= agenda.data_fim:
        
        # Se o dia da semana atual bate com os dias configurados na agenda
        if dia_atual.weekday() in dias_permitidos:
            horario_slot = hora_inicio_dt
            
            # Gera as frações de horário para a quantidade de vagas
            for _ in range(agenda.vagas_por_dia):
                horarios_para_criar.append(
                    Horario(
                        agenda=agenda,
                        data=dia_atual,
                        hora=horario_slot.time(),
                        status='disponivel'
                    )
                )
                # Avança o tempo para o próximo slot
                horario_slot += timedelta(minutes=duracao_slot_minutos)
                
        dia_atual += timedelta(days=1)
        
    # Salva no banco de dados
    if horarios_para_criar:
        Horario.objects.bulk_create(horarios_para_criar, ignore_conflicts=True)