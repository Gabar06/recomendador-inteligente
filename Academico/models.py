#from __future__ import annotations

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings



#########################

# Create your models here.
class Administrador(models.Model):
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

class Nota(models.Model):
    id = models.AutoField(primary_key=True)
    materia = models.CharField(max_length=60)
    calificacion = models.IntegerField()

class Soporte(models.Model):
    id = models.AutoField(primary_key=True)
    mantenimiento = models.CharField(max_length=60)
    reparacion = models.CharField(max_length=60)

    
############################

CURSOS = [
    ('1', '1er Curso'),
]

    
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

###############
###ACENTUACIÓN###
class IntentoAcentuacion(models.Model):
    usuario = models.CharField(max_length=50)   # Si tienes autenticación, pon ForeignKey al User
    fecha = models.DateTimeField(auto_now_add=True)
    #puntaje = models.IntegerField(default=0)    # O porcentaje de aciertos
    #errores = models.IntegerField(default=0)     # Total de errores en ese intento

class MovimientoAcentuacion(models.Model):
    intento = models.ForeignKey(IntentoAcentuacion, on_delete=models.CASCADE, related_name='movimientos')
    palabra_incorrecta = models.CharField(max_length=100)
    palabra_correcta = models.CharField(max_length=100)
    clasificacion = models.CharField(max_length=50)
    #acierto = models.BooleanField()  # True si el usuario acertó, False si falló

class UsuarioManager(BaseUserManager):
    def create_user(self, cedula, email, nombre, apellido, role, password=None):
        if not cedula: raise ValueError("La cédula es obligatoria")
        if not email:  raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        u = self.model(
            cedula=cedula, email=email,
            nombre=nombre, apellido=apellido,
            role=role, is_active=True
        )
        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, cedula, email, nombre="Admin", apellido="User", role="DOCENTE", password=None):
        u = self.create_user(cedula, email, nombre, apellido, role, password)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class Usuario(AbstractBaseUser, PermissionsMixin):
    DOCENTE = "DOCENTE"
    ESTUDIANTE = "ESTUDIANTE"
    ROLE_CHOICES = [(DOCENTE, "Docente"), (ESTUDIANTE, "Estudiante")]

    cedula = models.CharField("Cédula de Identidad", max_length=20, unique=True)
    email = models.EmailField("Correo Electrónico", unique=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'role']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.cedula} - {self.nombre} {self.apellido} ({self.role})"

class PasswordResetCode(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reset_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self):
        return (not self.used) and (timezone.now() <= self.expires_at)

# Si tenés perfiles:
class Docente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='docente')
    cedula = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)

class Estudiante(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='estudiante')
    cedula = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)


#######################
#Ejercicio1 Acentuación

class ExerciseAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=64, db_index=True)  # agrupa una “pasada” del set
    exercise_number = models.PositiveSmallIntegerField()
    user_answer = models.TextField()
    correct_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 0–1
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

class ExplanationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attempt = models.ForeignKey(ExerciseAttempt, on_delete=models.CASCADE, related_name="explanations")
    model_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ActionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=64, db_index=True)
    exercise_number = models.PositiveSmallIntegerField()
    action = models.CharField(max_length=64)  # visit/submit/explain/continue
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ResultSummary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=64, db_index=True)
    total_items = models.PositiveIntegerField()
    correct_items = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    breakdown = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Exercise2Attempt(models.Model):
    """Almacena un intento de una pregunta del ejercicio 2 de acentuación.

    Cada vez que un estudiante responde a una pregunta se crea una
    instancia de este modelo, guardando quién la respondió, el número
    de la pregunta, la opción seleccionada, cuál era la opción
    correcta y si la respuesta fue correcta o no.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_number = models.PositiveSmallIntegerField()
    selected_option = models.CharField(max_length=10)
    correct_option = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Intento de ejercicio 2"
        verbose_name_plural = "Intentos de ejercicio 2"

    def __str__(self) -> str:  # pragma: no cover - función de representación
        return f"Ejercicio2Preg{self.question_number} ({'✓' if self.is_correct else '✗'})"


class Exercise2Result(models.Model):
    """Guarda el resultado final del ejercicio 2 para un estudiante.

    Tras completar las tres preguntas del ejercicio 2, se almacena
    cuántas respondió correctamente y el porcentaje obtenido.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_questions = models.PositiveSmallIntegerField(default=3)
    correct_answers = models.PositiveSmallIntegerField()
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resultado de ejercicio 2"
        verbose_name_plural = "Resultados de ejercicio 2"

    def __str__(self) -> str:  # pragma: no cover - función de representación
        return f"Resultado Ej2 ({self.percentage:.1f}%)"