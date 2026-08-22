from django.db import models
from django.contrib.auth.models import User

class Especialista(models.Model):
    nome = models.CharField(max_length=150)
    especialidade = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"

class DiaSemana(models.Model):
    """
    Entidade fixa para normalizar os dias da semana.
    Ex: 0 = Segunda, 1 = Terça, etc.
    """
    DIA_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    dia = models.IntegerField(choices=DIA_CHOICES, unique=True)

    def __str__(self):
        return self.get_dia_display()

class Agenda(models.Model):
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE, related_name='agendas')
    dias_semana = models.ManyToManyField(DiaSemana, related_name='agendas')
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    vagas_por_dia = models.PositiveIntegerField()
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agenda: {self.especialista.nome} ({self.data_inicio} até {self.data_fim})"

class Horario(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
    ]
    
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name='horarios')
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='disponivel')
    paciente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('agenda', 'data', 'hora')
        ordering = ['data', 'hora']

    def __str__(self):
        return f"{self.data} {self.hora} - {self.agenda.especialista.nome} ({self.status})"