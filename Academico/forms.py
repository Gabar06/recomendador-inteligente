from django import forms
from .models import Contenido, Docente, Estudiante

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

Usuario = get_user_model()

solo_numeros = RegexValidator(r'^\d+$', message='La cédula debe contener solo dígitos.')

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

class UsuarioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )

    class Meta:
        model = Usuario
        fields = ['cedula', 'email', 'nombre', 'apellido', 'role', 'is_active', 'fecha_nacimiento']
    
    def clean_cedula(self):
        ced = self.cleaned_data.get('cedula','').strip()
        if not ced.isdigit():
            raise forms.ValidationError("La cédula debe contener solo dígitos.")
        return ced

class LoginForm(forms.Form):
    cedula = forms.CharField(
        label="Cédula",
        max_length=20,
        validators=[solo_numeros],
        widget=forms.TextInput(attrs={"placeholder":"Ej: 12345678", "inputmode":"numeric"})
    )
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    

class RegisterForm(forms.ModelForm):
    cedula = forms.CharField(
        label="Cédula",
        max_length=20,
        validators=[solo_numeros],
        widget=forms.TextInput(attrs={"placeholder":"Solo dígitos", "inputmode":"numeric"})
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"type":"date"})
    )
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = ['cedula', 'email', 'nombre', 'apellido']
    
    def clean_cedula(self):
        ced = self.cleaned_data.get("cedula","").strip()
        if not ced.isdigit():
            raise forms.ValidationError("La cédula debe contener solo dígitos.")
        # opcional: chequear unicidad
        if Usuario.objects.filter(cedula=ced).exists():
            raise forms.ValidationError("Ya existe un usuario con esa cédula.")
        return ced

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "Las contraseñas no coinciden")
        return cleaned

class ResetRequestForm(forms.Form):
    identificador = forms.CharField(label="Cédula o Email", help_text="Ingresá tu cédula o tu correo")

class ResetVerifyForm(forms.Form):
    identificador = forms.CharField(label="Cédula o Email")
    code = forms.CharField(label="Código de verificación", max_length=6)
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nueva contraseña")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar nueva contraseña")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password1") != cleaned.get("new_password2"):
            self.add_error("new_password2", "Las contraseñas no coinciden")
        return cleaned