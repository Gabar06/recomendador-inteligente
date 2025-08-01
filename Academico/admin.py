from django.contrib import admin

# Register your models here.
from.models import Administrador,Alumnos,Asignatura,Asistencia,Categorias,Nota,Soporte
################
from .models import Materia, Contenido, Docente, Estudiante

#LOGIN


##############
admin.site.register(Administrador)
admin.site.register(Alumnos)
admin.site.register(Asignatura)
admin.site.register(Asistencia)
admin.site.register(Categorias)
admin.site.register(Nota)
admin.site.register(Soporte)

#############################

admin.site.register(Materia)
admin.site.register(Contenido)
admin.site.register(Docente)
admin.site.register(Estudiante)


