from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from agendamentos.models import Especialista, DiaSemana

class Command(BaseCommand):
    help = 'Popula o banco de dados com especialistas e usuários de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\nIniciando o SETUP...'))

        # Criação do Usuário Admin (A Clínica)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@clinica.com', 'admin123')

        # Criação dos Usuários Clientes (Os Pacientes)
        if not User.objects.filter(username='paciente1').exists():
            User.objects.create_user('paciente1', 'paciente1@email.com', 'senha123')
            
        if not User.objects.filter(username='paciente2').exists():
            User.objects.create_user('paciente2', 'paciente2@email.com', 'senha123')

        if not User.objects.filter(username='paciente3').exists():
                    User.objects.create_user('paciente3', 'paciente3@email.com', 'senha123')

        # Criação de Especialistas
        Especialista.objects.get_or_create(nome='Dra. Ana Costa', especialidade='Cardiologia')
        Especialista.objects.get_or_create(nome='Dr. João Silva', especialidade='Ortopedia')

        v = self.style.SUCCESS      
        a = self.style.WARNING           
        c = self.style.MIGRATE_HEADING

        resumo = f"""
        {v('==============================================')}
        {v('🚀 SETUP FINALIZADO!')}
        {v('==============================================')}

        {v('👤 ADMIN')}
        {v('   - Login:')} {a('admin')}
        {v('   - Senha:')} {a('admin123')}

        {v('🧑‍⚕️ PACIENTES')}
        {v('   - Logins:')} {a('paciente1, paciente2, paciente3')}
        {v('   - Senha :')} {a('senha123')}

        {v('🩺 ESPECIALISTAS')}
        {v('   - Dra. Ana Costa (Cardiologia)')}
        {v('   - Dr. João Silva (Ortopedia)')}

        {v('🌐 LINKS RÁPIDOS')}
        {v('   - Front-End (Vue) :')} {c('http://localhost:5173')}
        {v('   - API Base URL    :')} {c('http://localhost:8000/api/')}
        {v('   - API Docs (Swag.):')} {c('http://localhost:8000/swagger/')}
        {v('   - Admin Django    :')} {c('http://localhost:8000/admin/')}
        {v('==================================================')}
        """

        self.stdout.write(resumo)