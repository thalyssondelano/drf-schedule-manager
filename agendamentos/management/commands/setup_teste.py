from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from agendamentos.models import Especialista, DiaSemana

class Command(BaseCommand):
    help = 'Popula o banco de dados com dias da semana, especialistas e usuários de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando o setup do banco de dados...'))

        # 1. Criação dos Dias da Semana
        dias_nomes = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        for i, nome in enumerate(dias_nomes):
            DiaSemana.objects.get_or_create(dia=i)
        self.stdout.write(self.style.SUCCESS('✅ Dias da semana criados.'))

        # 2. Criação do Usuário Admin (A Clínica)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@clinica.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Usuário Admin criado (Login: admin / Senha: admin123).'))

        # 3. Criação dos Usuários Clientes (Os Pacientes)
        if not User.objects.filter(username='paciente1').exists():
            User.objects.create_user('paciente1', 'paciente1@email.com', 'senha123')
            
        if not User.objects.filter(username='paciente2').exists():
            User.objects.create_user('paciente2', 'paciente2@email.com', 'senha123')
            
        self.stdout.write(self.style.SUCCESS('✅ 2 Usuários Pacientes criados (Senhas: senha123).'))

        # 4. Criação de Especialistas
        Especialista.objects.get_or_create(nome='Dra. Ana Costa', especialidade='Cardiologia')
        Especialista.objects.get_or_create(nome='Dr. João Silva', especialidade='Ortopedia')
        self.stdout.write(self.style.SUCCESS('✅ Especialistas de teste criados.'))

        self.stdout.write(self.style.SUCCESS('🚀 Setup finalizado!'))