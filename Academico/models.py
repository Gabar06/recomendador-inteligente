#from __future__ import annotations

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator


#########################

# Create your models here.

# validator global
solo_numeros = RegexValidator(r'^\d+$', message='La cédula debe contener solo dígitos.')

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

    def create_superuser(self, cedula, email, nombre="Admin", apellido="User", role="ADMINISTRADOR", password=None):
        u = self.create_user(cedula, email, nombre, apellido, role, password)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class Usuario(AbstractBaseUser, PermissionsMixin):
    DOCENTE = "DOCENTE"
    ESTUDIANTE = "ESTUDIANTE"
    ADMINISTRADOR = "ADMINISTRADOR"
    ROLE_CHOICES = [(DOCENTE, "Docente"), (ESTUDIANTE, "Estudiante"),(ADMINISTRADOR, "Administrador")]

    cedula = models.CharField(
        "Cédula de Identidad",
        max_length=20,
        unique=True,
        validators=[solo_numeros],   # <-- validación servidor
        help_text="Solo números, sin puntos ni guiones."
    )
    email = models.EmailField("Correo Electrónico", unique=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
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
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=True)

class Estudiante(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='estudiante')
    cedula = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=True)

class Administrador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrador')
    cedula = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=True)


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
    
    
# -----------------------------------------------------------------------------
# Modelos para el ejercicio final de puntuación
#
# Se definen modelos adicionales para almacenar las interacciones de los
# estudiantes con el ejercicio de puntuación. Cada clic que realiza el
# estudiante para colocar un signo de puntuación se registra en
# PunctuationAttempt, mientras que el resultado global del ejercicio se
# almacena en PunctuationResult.

class PunctuationAttempt(models.Model):
    """Representa un intento en el ejercicio de puntuación.

    Un intento guarda el paso (orden en el cual se realiza dentro del
    ejercicio), la posición (índice de espacio entre palabras) donde el
    estudiante hizo clic, el índice correcto esperado para ese paso, qué
    signo de puntuación se esperaba y si la respuesta fue correcta.  Se
    asocia a un usuario mediante la clave foránea `user`.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    selected_index = models.PositiveIntegerField()
    correct_index = models.PositiveIntegerField()
    expected_punctuation = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Intento de puntuación"
        verbose_name_plural = "Intentos de puntuación"

    def __str__(self) -> str:  # pragma: no cover
        status = "✓" if self.is_correct else "✗"
        return f"Paso {self.step_number} ({status})"


class PunctuationResult(models.Model):
    """Almacena el resultado final del ejercicio de puntuación para un usuario."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_steps = models.PositiveIntegerField(default=8)
    correct_steps = models.PositiveIntegerField()
    percentage = models.FloatField()
    recommendation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resultado de puntuación"
        verbose_name_plural = "Resultados de puntuación"

    def __str__(self) -> str:  # pragma: no cover
        return f"Resultado Puntuación ({self.percentage:.0f}%)"

# -----------------------------------------------------------------------------
# Modelos para ejercicios de selección múltiple (puntuación, mayúsculas y
# reglas ortográficas)
#
# Estas clases generalizan el almacenamiento de respuestas y resultados para
# cualquier ejercicio de opción múltiple de tres preguntas.  Cada intento
# registra el usuario, el ejercicio al que pertenece (p.ej. 'puntuacion1',
# 'mayus1', 'letras2'), el número de la pregunta, la opción seleccionada, la
# opción correcta y si la respuesta fue correcta.  Al finalizar las tres
# preguntas se almacena un resultado con el total de aciertos y el
# porcentaje obtenido, junto con una recomendación opcional.

class MultipleChoiceAttempt(models.Model):
    """Almacena una respuesta a una pregunta de un ejercicio de opción múltiple.

    Cada vez que un estudiante responde a una pregunta de un ejercicio
    (puntuación, mayúsculas o reglas ortográficas) se crea un registro
    indicando la identificación del ejercicio mediante `exercise_slug`, el
    número de pregunta, la opción seleccionada, la correcta y si la
    respuesta fue correcta.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_slug = models.CharField(max_length=50)
    question_number = models.PositiveSmallIntegerField()
    selected_option = models.CharField(max_length=10)
    correct_option = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    run_id = models.CharField(max_length=36, db_index=True)

    class Meta:
        verbose_name = "Intento de ejercicio de opción múltiple"
        verbose_name_plural = "Intentos de ejercicios de opción múltiple"

    def __str__(self) -> str:  # pragma: no cover
        status = "✓" if self.is_correct else "✗"
        return f"{self.exercise_slug} Q{self.question_number} ({status})"


class MultipleChoiceResult(models.Model):
    """Guarda el resultado final de un ejercicio de opción múltiple.

    Una vez que el estudiante responde las tres preguntas de un ejercicio,
    se almacena la cantidad de aciertos y el porcentaje correspondiente.
    El campo `exercise_slug` identifica a qué ejercicio pertenecen estos
    resultados (por ejemplo, 'puntuacion1' o 'letras2').  Se puede
    incluir una recomendación opcional para orientar al estudiante en
    próximos estudios.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_slug = models.CharField(max_length=50)
    total_questions = models.PositiveSmallIntegerField(default=3)
    correct_answers = models.PositiveSmallIntegerField()
    percentage = models.FloatField()
    recommendation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    run_id = models.CharField(max_length=36, db_index=True)

    class Meta:
        verbose_name = "Resultado de ejercicio de opción múltiple"
        verbose_name_plural = "Resultados de ejercicios de opción múltiple"

    def __str__(self) -> str:  # pragma: no cover
        return f"Resultado {self.exercise_slug} ({self.percentage:.0f}%)"
    
    # -----------------------------------------------------------------------------
# Modelos para la encuesta de opinión
#
# La encuesta de opinión se compone de una serie de preguntas que no
# requieren evaluación automática ni tienen respuestas correctas.  Cada
# respuesta del estudiante se guarda en SurveyAttempt y, al finalizar
# la encuesta, se registra un SurveyResult para indicar que el
# estudiante completó el formulario.  Estos modelos son similares a
# MultipleChoiceAttempt y MultipleChoiceResult, pero omiten los
# campos relacionados con la puntuación y la corrección.


class SurveyAttempt(models.Model):
    """Almacena la respuesta del usuario a una pregunta de la encuesta.

    Cada vez que un estudiante responde a una pregunta de la encuesta se
    crea un registro indicando el número de la pregunta y la opción
    seleccionada.  No se registra una opción correcta ya que no existen
    respuestas correctas o incorrectas en la encuesta.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey_slug = models.CharField(max_length=50, default="encuesta")
    question_number = models.PositiveSmallIntegerField()
    selected_option = models.CharField(max_length=10)
    run_id = models.CharField(max_length=36, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Respuesta de encuesta"
        verbose_name_plural = "Respuestas de encuestas"
        unique_together = ("user", "survey_slug", "run_id", "question_number")

    def __str__(self) -> str:  # pragma: no cover
        return f"Encuesta {self.survey_slug} Q{self.question_number}: {self.selected_option}"


class SurveyResult(models.Model):
    """Registra que un usuario ha completado la encuesta.

    Este modelo almacena la cantidad de preguntas respondidas y permite
    conocer cuándo el usuario finalizó la encuesta.  No almacena
    puntuaciones ni recomendaciones, ya que la encuesta no evalúa
    conocimientos, sino que recopila opiniones y datos demográficos.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey_slug = models.CharField(max_length=50, default="encuesta")
    total_questions = models.PositiveSmallIntegerField()
    run_id = models.CharField(max_length=36, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resultado de encuesta"
        verbose_name_plural = "Resultados de encuestas"
        unique_together = ("user", "survey_slug", "run_id")

    def __str__(self) -> str:  # pragma: no cover
        return f"Resultado Encuesta {self.survey_slug} ({self.total_questions} preguntas)"
    
    
class SurveyAttemptDocente(models.Model):
    """Almacena la respuesta del usuario a una pregunta de la encuesta.

    Cada vez que un estudiante responde a una pregunta de la encuesta se
    crea un registro indicando el número de la pregunta y la opción
    seleccionada.  No se registra una opción correcta ya que no existen
    respuestas correctas o incorrectas en la encuesta.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey_slug = models.CharField(max_length=50, default="encuesta")
    question_number = models.PositiveSmallIntegerField()
    selected_option = models.CharField(max_length=10)
    run_id = models.CharField(max_length=36, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Respuesta de encuesta"
        verbose_name_plural = "Respuestas de encuestas"
        unique_together = ("user", "survey_slug", "run_id", "question_number")

    def __str__(self) -> str:  # pragma: no cover
        return f"Encuesta {self.survey_slug} Q{self.question_number}: {self.selected_option}"


class SurveyResultDocente(models.Model):
    """Registra que un usuario ha completado la encuesta.

    Este modelo almacena la cantidad de preguntas respondidas y permite
    conocer cuándo el usuario finalizó la encuesta.  No almacena
    puntuaciones ni recomendaciones, ya que la encuesta no evalúa
    conocimientos, sino que recopila opiniones y datos demográficos.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey_slug = models.CharField(max_length=50, default="encuesta")
    total_questions = models.PositiveSmallIntegerField()
    run_id = models.CharField(max_length=36, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resultado de encuesta"
        verbose_name_plural = "Resultados de encuestas"
        unique_together = ("user", "survey_slug", "run_id")

    def __str__(self) -> str:  # pragma: no cover
        return f"Resultado Encuesta {self.survey_slug} ({self.total_questions} preguntas)"

    

# -----------------------------------------------------------------------------
# Modelo para actividades del calendario
#
# Este modelo registra cada ejercicio o evaluación finalizada por el estudiante
# para que pueda visualizarse en un calendario de actividades.  Al completar
# un ejercicio o una evaluación se crea un registro en esta tabla.  La
# aplicación puede mostrar estas entradas en un calendario (por ejemplo,
# mediante la biblioteca FullCalendar) permitiendo al estudiante llevar un
# historial de su progreso.

class CalendarActivity(models.Model):
    """Almacena una actividad del calendario para un usuario.

    Cada vez que un estudiante finaliza un ejercicio o una evaluación,
    se crea un evento en el calendario con un título descriptivo, una
    descripción opcional y la fecha de realización.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_slug = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Actividad del calendario"
        verbose_name_plural = "Actividades del calendario"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.activity_slug}: {self.title} ({self.date.date()})"
    

class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.CharField(max_length=50, db_index=True)  # p.ej. u1_instr, u2_e1, u3_final
    completed_at = models.DateTimeField(auto_now_add=True)
    times_completed = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "slug")

class FinalEvalLock(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    taken = models.BooleanField(default=False)
    taken_at = models.DateTimeField(null=True, blank=True)


#Ejercicios dinámicos en la Guía de Aprendizaje
class ExerciseUnit(models.TextChoices):
    U1 = "u1", "Acentuación"
    U2 = "u2", "Puntuación"
    U3 = "u3", "Mayúsculas"
    U4 = "u4", "Letras"
    FINAL = "final", "Evaluación final"

class BankExercise(models.Model):
    unit = models.CharField(max_length=10, choices=ExerciseUnit.choices, db_index=True)
    question = models.TextField("Enunciado")
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('a','A'),('b','B'),('c','C'),('d','D')])
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="created_bank_exercises")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_unit_display()}] {self.question[:60]}..."

class StudentExerciseUse(models.Model):
    """Marca qué ejercicios del banco ya vio un estudiante (para no repetir)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.CharField(max_length=10, choices=ExerciseUnit.choices, db_index=True)
    exercise = models.ForeignKey(BankExercise, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=64, blank=True, default="")
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "exercise")
        indexes = [models.Index(fields=["user", "unit"])]