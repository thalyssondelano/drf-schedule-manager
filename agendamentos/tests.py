from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date, time

from agendamentos.models import Especialista, DiaSemana, Agenda, Horario

class ClinicaAPITestCase(APITestCase):
    
    # Cria um banco de dados temporario.
    def setUp(self):
        # Cria usuarios para os testes
        self.admin = User.objects.create_superuser('admin_teste', 'admin@teste.com', 'senha123')
        self.paciente = User.objects.create_user('paciente_teste', 'paciente@teste.com', 'senha123')
        
        # Cria dados básicos
        self.medico = Especialista.objects.create(nome="Dr. House")
        self.segunda = DiaSemana.objects.create(dia=0)
        
        # URL da API de agendas
        self.url_agendas = '/api/agendas/'

    def test_01_paciente_toma_erro_ao_criar_agenda(self):
        """Garante que um paciente logado (não admin) não pode criar agendas"""
        # Força o login como paciente
        self.client.force_authenticate(user=self.paciente)
        
        payload = {
            "especialista": self.medico.id,
            "dias_semana": [self.segunda.id],
            "data_inicio": "2026-08-24",
            "data_fim": "2026-08-30",
            "hora_inicio": "08:00:00",
            "hora_fim": "12:00:00",
            "vagas_por_dia": 4
        }
        
        # Faz a requisição POST
        response = self.client.post(self.url_agendas, payload)
        
        # Verifica se a API respondeu exatamente com 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_02_admin_cria_agenda_e_motor_gera_horarios(self):
        """Garante que a agenda divide os horários corretamente"""
        # Força login como Admin
        self.client.force_authenticate(user=self.admin)
        
        payload = {
            "especialista": self.medico.id,
            "dias_semana": [self.segunda.id], # ID da Segunda-feira
            "data_inicio": "2026-08-24",      # Cai numa segunda
            "data_fim": "2026-08-30",
            "hora_inicio": "08:00:00",
            "hora_fim": "12:00:00",
            "vagas_por_dia": 4,
            "ativa": True
        }
        
        response = self.client.post(self.url_agendas, payload)
        
        # Verifica se salvou (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Busca no banco temporario se o gatilho gerou os 4 horários previstos
        horarios_gerados = Horario.objects.filter(agenda_id=response.data['id'])
        self.assertEqual(horarios_gerados.count(), 4)

    def test_03_paciente_consegue_reservar_com_sucesso(self):
        """Garante que o paciente reserva e o status muda no banco"""
        # Prepara a Agenda e o Horário direto no banco do teste
        agenda = Agenda.objects.create(
            especialista=self.medico, data_inicio=date(2026, 8, 24), data_fim=date(2026, 8, 30),
            hora_inicio=time(8, 0), hora_fim=time(12, 0), vagas_por_dia=4
        )
        agenda.dias_semana.add(self.segunda)
        horario = Horario.objects.create(
            agenda=agenda, data=date(2026, 8, 24), hora=time(8, 0), status='disponivel'
        )
        
        # Loga como paciente e faz a requisição na rota customizada
        self.client.force_authenticate(user=self.paciente)
        url_reserva = f'/api/horarios/{horario.id}/reservar/'
        
        response = self.client.patch(url_reserva, {})
        
        # Verifica se retornou 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Atualiza o objeto com os dados do banco e valida se a reserva foi feita com sucesso
        horario.refresh_from_db()
        self.assertEqual(horario.status, 'reservado')
        self.assertEqual(horario.paciente.username, 'paciente_teste')

    def test_04_paciente_nao_consegue_reservar_horario_ja_ocupado(self):
        """Garante que a API bloqueia dupla reserva com Erro 400"""
        # Cria um horário que JÁ ESTÁ reservado no banco
        agenda = Agenda.objects.create(especialista=self.medico, data_inicio=date(2026, 8, 24), data_fim=date(2026, 8, 30), hora_inicio=time(8, 0), hora_fim=time(12, 0), vagas_por_dia=4)
        horario = Horario.objects.create(agenda=agenda, data=date(2026, 8, 24), hora=time(8, 0), status='reservado', paciente=self.admin)
        
        # Loga como paciente e tenta pegar a mesma reserva
        self.client.force_authenticate(user=self.paciente)
        response = self.client.patch(f'/api/horarios/{horario.id}/reservar/', {})
        
        # Verifica se o sistema barrou com Erro 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_05_admin_nao_cria_agenda_com_data_fim_no_passado(self):
        """Garante que a API bloqueia data de fim anterior à data de início"""
        self.client.force_authenticate(user=self.admin)
        payload = {
            "especialista": self.medico.id,
            "dias_semana": [self.segunda.id],
            "data_inicio": "2026-08-30",
            "data_fim": "2026-08-24", 
            "hora_inicio": "08:00:00",
            "hora_fim": "12:00:00",
            "vagas_por_dia": 4
        }
        response = self.client.post(self.url_agendas, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_06_admin_nao_cria_agenda_com_hora_invalida(self):
        """Garante que a API bloqueia turnos de zero minutos ou invertidos"""
        self.client.force_authenticate(user=self.admin)
        payload = {
            "especialista": self.medico.id,
            "dias_semana": [self.segunda.id],
            "data_inicio": "2026-08-24",
            "data_fim": "2026-08-30",
            "hora_inicio": "08:00:00",
            "hora_fim": "08:00:00",
            "vagas_por_dia": 4
        }
        response = self.client.post(self.url_agendas, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_07_admin_nao_cria_agenda_com_dia_inexistente_no_intervalo(self):
        """Garante que barra agendas fantasmas (dia da semana fora do calendário)"""
        self.client.force_authenticate(user=self.admin)
        
        domingo = DiaSemana.objects.create(dia=6)
        
        payload = {
            "especialista": self.medico.id,
            "dias_semana": [domingo.id], 
            "data_inicio": "2026-08-24", 
            "data_fim": "2026-08-25",
            "hora_inicio": "08:00:00",
            "hora_fim": "12:00:00",
            "vagas_por_dia": 4
        }
        response = self.client.post(self.url_agendas, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_08_admin_nao_cria_agenda_sobreposta(self):
        """Garante que a API impede choque de horários do especialista"""
        self.client.force_authenticate(user=self.admin)
        
        payload = {
            "especialista": self.medico.id,
            "dias_semana": [self.segunda.id],
            "data_inicio": "2026-08-24",
            "data_fim": "2026-08-30",
            "hora_inicio": "08:00:00",
            "hora_fim": "12:00:00",
            "vagas_por_dia": 4
        }
        self.client.post(self.url_agendas, payload)
        
        response2 = self.client.post(self.url_agendas, payload)
        
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)