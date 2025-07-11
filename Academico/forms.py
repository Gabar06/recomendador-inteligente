from django import forms
from .models import Contenido

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
