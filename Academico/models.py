from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Administrador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    login = models.CharField(max_length=60)
    clave = models.CharField(max_length=60)

class Docentes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    login = models.CharField(max_length=60)
    clave = models.CharField(max_length=60)

class Alumnos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    curso = models.CharField(max_length=60)
    sexo = models.CharField(max_length=60)

class Asignatura(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
#
class Asistencia(models.Model):
    id = models.AutoField(primary_key=True)
    materia = models.CharField(max_length=60)
    horas = models.IntegerField()

class Categorias(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=60)

class Cuota(models.Model):
    id = models.AutoField(primary_key=True)
    mes = models.CharField(max_length=60)
    monto = models.IntegerField()

class Nota(models.Model):
    id = models.AutoField(primary_key=True)
    materia = models.CharField(max_length=60)
    calificacion = models.IntegerField()

class Soporte(models.Model):
    id = models.AutoField(primary_key=True)
    mantenimiento = models.CharField(max_length=60)
    reparacion = models.CharField(max_length=60)

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=60)
    nr_sucursal = models.IntegerField()
    
############################

CURSOS = [
    ('1', '1er Curso'),
]

class Usuario(AbstractUser):
    is_estudiante = models.BooleanField(default=False)
    is_docente = models.BooleanField(default=False)

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    curso = models.CharField(max_length=2, choices=CURSOS, default='1')
    rendimiento_academico = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='Promedio de notas (0.00 - 100.00)')
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - Curso {self.curso}"

class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    materias = models.ManyToManyField('Materia')

    def __str__(self):
        return self.usuario.get_full_name()
    
NIVELES = [
    ('1', '1er Curso'),
]

class Materia(models.Model):
    nombre = models.CharField(max_length=100, default='Lengua Castellana y Literatura')
    nivel = models.CharField(max_length=2, choices=NIVELES, default='1')

    def __str__(self):
        return f"{self.nombre} - Nivel {self.nivel}"

class Contenido(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='contenidos/')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Guia(models.Model):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Guía {self.contenido.titulo} para {self.estudiante.usuario.username}"

######################################
def libro_upload(instance, filename):
    return f'libros/{instance.titulo}_{filename}'

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    año = models.PositiveIntegerField()
    archivo = models.FileField(upload_to=libro_upload)

    def __str__(self):
        return self.titulo