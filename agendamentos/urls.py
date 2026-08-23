from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EspecialistaViewSet, DiaSemanaViewSet, AgendaViewSet, HorarioViewSet

router = DefaultRouter()
router.register(r'especialistas', EspecialistaViewSet)
router.register(r'dias-semana', DiaSemanaViewSet)
router.register(r'agendas', AgendaViewSet)
router.register(r'horarios', HorarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]