from django.contrib import admin

# Register your models here.
from django.contrib import admin
from.models import Administrador,Docentes,Alumnos,Asignatura,Asistencia,Categorias,Cuota,Nota,Soporte,Sucursal
################
from .models import Usuario, Estudiante, Docente, Materia, Contenido, Guia

admin.site.register(Administrador)
admin.site.register(Docentes)
admin.site.register(Alumnos)
admin.site.register(Asignatura)
admin.site.register(Asistencia)
admin.site.register(Categorias)
admin.site.register(Cuota)
admin.site.register(Nota)
admin.site.register(Soporte)
admin.site.register(Sucursal)

#############################

admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Docente)
admin.site.register(Materia)
admin.site.register(Contenido)
admin.site.register(Guia)