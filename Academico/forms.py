from django import forms
from .models import Contenido, Docente, Estudiante

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'descripcion', 'archivo', 'materia']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    # Validación 1: título no duplicado
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Contenido.objects.filter(titulo__iexact=titulo).exists():
            raise forms.ValidationError("Ya existe un contenido con este título.")
        return titulo

    # Validación 2: archivo obligatorio
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo:
            raise forms.ValidationError("Debe subir un archivo.")
        # Validación 4: tipos de archivo permitidos
        extensiones_permitidas = ['pdf', 'docx', 'pptx']
        if archivo.name.split('.')[-1].lower() not in extensiones_permitidas:
            raise forms.ValidationError("Solo se permiten archivos PDF, DOCX o PPTX.")
        return archivo

################
#LOGIN DOCENTE
class LoginDocente(forms.Form):
    """Formulario de inicio de sesión para docentes.

    Valida la combinación de cédula y contraseña mediante la función
    ``authenticate`` de Django. Si la autenticación falla o la cuenta
    está inactiva, lanza errores correspondientes.
    """

    cedula = forms.CharField(max_length=20, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        cedula = cleaned_data.get("cedula")
        password = cleaned_data.get("password")
        if cedula and password:
            user = authenticate(username=cedula, password=password)
            if user is None:
                raise forms.ValidationError("Credenciales incorrectas.")
            if not user.is_active:
                raise forms.ValidationError("Cuenta deshabilitada.")
            # Guardamos el usuario para usarlo en la vista
            self.user = user  # type: ignore[attr-defined]
        return cleaned_data

class RegisterDocente(forms.ModelForm):
    """Formulario de registro para nuevos docentes.

    Incluye dos campos de contraseña que deben coincidir. Utiliza el
    modelo Docente para crear una nueva instancia y establecer la
    contraseña de forma segura mediante ``set_password``.
    """

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Docente
        fields = ("cedula", "nombre", "apellido", "email")

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit: bool = True) -> Docente:
        user: Docente = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ForgotPasswordDocente(forms.Form):
    """Formulario para solicitar un código de restablecimiento.

    Se requieren la cédula y el correo del docente. La vista asociada
    buscará el usuario correspondiente y enviará un código por correo.
    """

    email = forms.EmailField(label="Correo Electrónico")
    cedula = forms.CharField(max_length=20, label="Cédula")

class ResetPasswordDocente(forms.Form):
    """Formulario para restablecer la contraseña con un código.

    El usuario debe proporcionar el código recibido por correo y dos
    campos de contraseña. Se valida que las contraseñas coincidan.
    """

    code = forms.CharField(max_length=10, label="Código de verificación")
    password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    

################
#LOGIN ESTUDIANTE
class LoginEstudiante(AuthenticationForm):
    cedula = forms.CharField(max_length=20, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
       

class EstudianteRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Estudiante
        fields = ('cedula', 'email', 'nombre', 'apellido', 'password')
    
    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

class ForgotPasswordEstudiante(forms.Form):
    email = forms.EmailField()

class ResetPasswordEstudiante(forms.Form):
    code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
