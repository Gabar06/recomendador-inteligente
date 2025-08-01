#from __future__ import annotations

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



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

#lOGIN DOCENTE
class DocenteManager(BaseUserManager):
    """Gestor personalizado para el modelo Docente.

    Proporciona métodos convenientes para crear usuarios y superusuarios. El
    identificador único utilizado es la ``cedula`` en lugar del nombre de usuario.
    """

    def create_user(self, cedula: str, nombre: str, apellido: str, email: str, password: str | None = None, **extra_fields: object) -> "Docente":
        """Crea y guarda un nuevo usuario Docente.

        Args:
            cedula: Cédula de identidad del docente, utilizada como nombre de usuario.
            nombre: Nombre del docente.
            apellido: Apellido del docente.
            email: Dirección de correo electrónico.
            password: Contraseña en texto plano. Será hasheada internamente.
            extra_fields: Campos adicionales para el modelo.

        Returns:
            Una instancia del modelo Docente recién creada.
        """
        if not cedula:
            raise ValueError("El campo 'Cédula' es obligatorio")
        if not email:
            raise ValueError("El campo 'Correo Electrónico' es obligatorio")
        email = self.normalize_email(email)
        user = self.model(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula: str, nombre: str, apellido: str, email: str, password: str | None = None, **extra_fields: object) -> "Docente":
        """Crea y guarda un superusuario Docente.

        Asegura que las banderas ``is_staff`` e ``is_superuser`` estén establecidas
        correctamente. La contraseña es obligatoria para superusuarios.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if password is None:
            raise ValueError("Superuser must have a password.")
        return self.create_user(cedula, nombre, apellido, email, password, **extra_fields)

class Docente(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado para docentes.

    Utiliza la cédula de identidad como ``USERNAME_FIELD``. Incluye campos
    adicionales de nombre, apellido y correo electrónico. Se añade un
    ``reset_code`` para manejar el proceso de restablecimiento de contraseña.
    """

    cedula: models.CharField = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Cédula de Identidad",
    )
    nombre: models.CharField = models.CharField(
        max_length=50,
        verbose_name="Nombre",
    )
    apellido: models.CharField = models.CharField(
        max_length=50,
        verbose_name="Apellido",
    )
    email: models.EmailField = models.EmailField(
        unique=True,
        verbose_name="Correo Electrónico",
    )
    is_staff: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=True)
    date_joined: models.DateTimeField = models.DateTimeField(default=timezone.now)
    reset_code: models.CharField = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Código de restablecimiento",
    )

    objects: DocenteManager = DocenteManager()

    USERNAME_FIELD: str = "cedula"
    REQUIRED_FIELDS: list[str] = ["nombre", "apellido", "email"]

    class Meta:
            verbose_name = "Docente"
            verbose_name_plural = "Docentes"

    def __str__(self) -> str:
            return f"{self.cedula} - {self.nombre} {self.apellido}"

#LOGIN ESTUDIANTE
class EstudianteManager(BaseUserManager):
    def create_user(self, cedula, email, nombre, apellido, password=None):
        if not email:
            raise ValueError('Debe proporcionar un correo electrónico válido.')

        estudiante = self.model(
            cedula=cedula,
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
        )

        estudiante.set_password(password)
        estudiante.save(using=self._db)
        return estudiante

class Estudiante(AbstractBaseUser):
    cedula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    reset_code = models.CharField(max_length=6, blank=True, null=True)

    objects = EstudianteManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



