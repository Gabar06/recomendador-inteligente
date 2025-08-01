from .models import Estudiante
from .models import Contenido, Guia
from django.utils import timezone

def recomendar_contenido(estudiante):
    """
    Retorna una lista de contenidos recomendados para un estudiante
    en base a su rendimiento académico.
    """
    if estudiante.rendimiento_academico >= 80:
        nivel = 'avanzado'
    elif estudiante.rendimiento_academico >= 50:
        nivel = 'medio'
    else:
        nivel = 'basico'

    # Filtrar contenidos que contengan esa palabra clave en la descripción
    return Contenido.objects.filter(descripcion__icontains=nivel)

def asignar_recomendaciones(estudiante):
    contenidos = recomendar_contenido(estudiante)
    for contenido in contenidos:
        Guia.objects.get_or_create(estudiante=estudiante, contenido=contenido, defaults={'fecha_asignacion': timezone.now()})
