from django.shortcuts import render, redirect, get_object_or_404
from .models import Administrador,Alumnos,Asignatura,Asistencia,Categorias,Nota,Soporte
from django.http import HttpResponse
################
from .models import Contenido, Libro
from .forms import ContenidoForm
from django.contrib import messages
import language_tool_python
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import analizar_respuestas, gemini_chat
import markdown
from django.db.models import Q
import google.generativeai as genai
####################
#ACENTUACIÓN CON LOGIN PERSONALIZADO
from .models import IntentoAcentuacion, MovimientoAcentuacion



import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

"""
from .forms import ForgotPasswordDocente, LoginDocente, RegisterDocente, ResetPasswordDocente
from .forms import ForgotPasswordEstudiante, LoginEstudiante, EstudianteRegistrationForm, ResetPasswordEstudiante
from .models import Docente, Estudiante"""

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


#####################
from .forms import LoginDocente,RegisterDocente, ForgotPasswordDocente, ResetPasswordDocente
from .forms import LoginEstudiante, EstudianteRegistrationForm, ForgotPasswordEstudiante, ResetPasswordEstudiante
from .models import Docente, Estudiante
##########################
#REACT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Libro
from .serializer import LibroSerializer

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

class LibroListCreate(APIView):
    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibroDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Libro, id=id)

    def get(self, request, id):
        libro = self.get_object(id)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)

    def put(self, request, id):
        libro = self.get_object(id)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        libro = self.get_object(id)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

# Instancia del cliente OpenAI con tu API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)
ALLOWED_EXTENSIONS = ['pdf', 'epub']

# Instancia del cliente Gemini con tu API Key
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')


# Create your views here.
#Administrador
def home(request):
    return render(request, "base.html")
def inicio(request):
    return render(request, "inicio.html")
def administrador(request):
    AdministradorListados = Administrador.objects.all()
    return render(request, "Administrador.html", { "administrador":AdministradorListados})

def nuevo(request):
    AdministradorListados = Administrador.objects.all()
    return render(request, "Administrador_Nuevo.html", {"administrador": AdministradorListados})

def registrar(request):
    nombre = request.POST['txtNombre']
    login = request.POST['txtLogin']
    contrasenha = request.POST['txtContrasenha']

    administrador = Administrador.objects.create(
        nombre=nombre,login=login,clave=contrasenha )
    return redirect('/Adm')

def edicion(request, id):
    administrador = Administrador.objects.get(id=id)
    return render(request, "Administrador_Editar.html", {"administrador": administrador})

def editar(request,id):
    nombre = request.POST['txtNombre']
    login = request.POST['txtLogin']
    clave = request.POST['txtClave']

    administrador = Administrador.objects.get(id=id)
    administrador.nombre = nombre
    administrador.login = login
    administrador.clave = clave
    administrador.save()
    return redirect('/Adm')

def eliminacion(request, id):
    administrador = Administrador.objects.get(id=id)
    return render(request, "Administrador_Eliminar.html", {"administrador": administrador})

def eliminar(request,id):

    administrador = Administrador.objects.get(id=id)
    administrador.delete()
    return redirect('/Adm')
def buscar(request):
    nombre = request.POST['txtNombre']
    administrador = Administrador.objects.filter(nombre=nombre)
    return render(request, "Administrador.html", {"administrador": administrador})

#Alumnos
def alumnos(request):
    AlumnosListados = Alumnos.objects.all()
    return render(request, "Alumnos.html", { "alumnos":AlumnosListados})

def alumnos_nuevo(request):
    AlumnosListados = Alumnos.objects.all()
    return render(request, "Alumnos_Nuevo.html", {"alumnos": AlumnosListados})
def alumnos_registrar(request):
    nombre = request.POST['txtNombre']
    curso = request.POST['txtCurso']
    sexo = request.POST['txtSexo']

    alumnos = Alumnos.objects.create(
        nombre=nombre,curso=curso,sexo=sexo )
    return redirect('/Alu')

def alumnos_edicion(request, id):
    alumnos = Alumnos.objects.get(id=id)
    return render(request, "Alumnos_Editar.html", {"alumnos": alumnos})
def alumnos_editar(request,id):
    nombre = request.POST['txtNombre']
    curso = request.POST['txtCurso']
    sexo = request.POST['txtSexo']

    alumnos = Alumnos.objects.get(id=id)
    alumnos.nombre = nombre
    alumnos.curso = curso
    alumnos.sexo = sexo
    alumnos.save()
    return redirect('/Alu')

def alumnos_eliminacion(request, id):
    alumnos = Alumnos.objects.get(id=id)
    return render(request, "Alumnos_Eliminar.html", {"alumnos": alumnos})

def alumnos_eliminar(request,id):
    alumnos = Alumnos.objects.get(id=id)
    alumnos.delete()
    return redirect('/Alu')
def alumnos_buscar(request):
    nombre = request.POST['txtNombre']
    alumnos = Alumnos.objects.filter(nombre=nombre)
    return render(request, "Alumnos.html", {"alumnos": alumnos})

#Asignatura
def asignatura(request):
    AsignaturaListados = Asignatura.objects.all()
    return render(request, "Asignatura.html", { "asignatura":AsignaturaListados})

def asignatura_nuevo(request):
    AsignaturaListados = Asignatura.objects.all()
    return render(request, "Asignatura_Nuevo.html", {"asignatura": AsignaturaListados})
def asignatura_registrar(request):
    nombre = request.POST['txtNombre']

    asignatura = Asignatura.objects.create(
        nombre=nombre )
    return redirect('/Asi')

def asignatura_edicion(request, id):
    asignatura = Asignatura.objects.get(id=id)
    return render(request, "Asignatura_Editar.html", {"asignatura": asignatura})
def asignatura_editar(request,id):
    nombre = request.POST['txtNombre']

    asignatura = Asignatura.objects.get(id=id)
    asignatura.nombre = nombre
    asignatura.save()
    return redirect('/Asi')

def asignatura_eliminacion(request, id):
    asignatura = Asignatura.objects.get(id=id)
    return render(request, "Asignatura_Eliminar.html", {"asignatura": asignatura})

def asignatura_eliminar(request,id):
    asignatura = Asignatura.objects.get(id=id)
    asignatura.delete()
    return redirect('/Asi')

def asignatura_buscar(request):
    nombre = request.POST['txtNombre']
    asignatura = Asignatura.objects.filter(nombre=nombre)
    return render(request, "Asignatura.html", {"asignatura": asignatura})

#Asistencia
def asistencia(request):
    AsistenciaListados = Asistencia.objects.all()
    return render(request, "Asistencia.html", { "asistencia":AsistenciaListados})

def asistencia_nuevo(request):
    AsistenciaListados = Asistencia.objects.all()
    return render(request, "Asistencia_Nuevo.html", {"asistencia": AsistenciaListados})
def asistencia_registrar(request):
    materia = request.POST['txtMateria']
    horas = request.POST['numHoras']

    asistencia = Asistencia.objects.create(
        materia=materia, horas=horas)
    return redirect('/Asis')

def asistencia_edicion(request, id):
    asistencia = Asistencia.objects.get(id=id)
    return render(request, "Asistencia_Editar.html", {"asistencia": asistencia})
def asistencia_editar(request,id):
    materia = request.POST['txtMateria']
    horas = request.POST['numHoras']

    asistencia = Asistencia.objects.get(id=id)
    asistencia.materia = materia
    asistencia.horas = horas
    asistencia.save()
    return redirect('/Asis')

def asistencia_eliminacion(request, id):
    asistencia = Asistencia.objects.get(id=id)
    return render(request, "Asistencia_Eliminar.html", {"asistencia": asistencia})

def asistencia_eliminar(request,id):
    asistencia = Asistencia.objects.get(id=id)
    asistencia.delete()
    return redirect('/Asis')

def asistencia_buscar(request):
    materia = request.POST['txtMateria']
    asistencia = Asistencia.objects.filter(materia=materia)
    return render(request, "Asistencia.html", {"asistencia": asistencia})

#Categorias
def categorias(request):
    CategoriasListados = Categorias.objects.all()
    return render(request, "Categorias.html", { "categorias":CategoriasListados})

def categorias_nuevo(request):
    CategoriasListados = Categorias.objects.all()
    return render(request, "Categorias_Nuevo.html", {"categorias": CategoriasListados})
def categorias_registrar(request):
    descripcion = request.POST['txtDescripcion']

    categorias = Categorias.objects.create(
        descripcion=descripcion)
    return redirect('/Cat')

def categorias_edicion(request, id):
    categorias = Categorias.objects.get(id=id)
    return render(request, "Categorias_Editar.html", {"categorias": categorias})
def categorias_editar(request,id):
    descripcion = request.POST['txtDescripcion']

    categorias = Categorias.objects.get(id=id)
    categorias.descripcion = descripcion
    categorias.save()
    return redirect('/Cat')

def categorias_eliminacion(request, id):
    categorias = Categorias.objects.get(id=id)
    return render(request, "Categorias_Eliminar.html", {"categorias": categorias})

def categorias_eliminar(request,id):
    categorias = Categorias.objects.get(id=id)
    categorias.delete()
    return redirect('/Cat')

def categorias_buscar(request):
    descripcion = request.POST['txtDescripcion']
    categorias = Categorias.objects.filter(descripcion=descripcion)
    return render(request, "Categorias.html", {"categorias": categorias})

#Nota
def nota(request):
    NotaListados = Nota.objects.all()
    return render(request, "Nota.html", { "nota":NotaListados})

def nota_nuevo(request):
    NotaListados = Nota.objects.all()
    return render(request, "Nota_Nuevo.html", {"nota": NotaListados})
def nota_registrar(request):
    materia = request.POST['txtMateria']
    calificacion = request.POST['numCalificacion']

    nota = Nota.objects.create(
        materia=materia, calificacion=calificacion)
    return redirect('/Not')

def nota_edicion(request, id):
    nota = Nota.objects.get(id=id)
    return render(request, "Nota_Editar.html", {"nota": nota})
def nota_editar(request,id):
    materia = request.POST['txtMateria']
    calificacion = request.POST['numCalificacion']

    nota = Nota.objects.get(id=id)
    nota.materia = materia
    nota.calificacion = calificacion
    nota.save()
    return redirect('/Not')

def nota_eliminacion(request, id):
    nota = Nota.objects.get(id=id)
    return render(request, "Nota_Eliminar.html", {"nota": nota})

def nota_eliminar(request,id):
    nota = Nota.objects.get(id=id)
    nota.delete()
    return redirect('/Not')

def nota_buscar(request):
    materia = request.POST['txtMateria']
    nota = Nota.objects.filter(materia=materia)
    return render(request, "Nota.html", {"nota": nota})

#Soporte
def soporte(request):
    SoporteListados = Soporte.objects.all()
    return render(request, "Soporte.html", { "soporte":SoporteListados})

def soporte_nuevo(request):
    SoporteListados = Soporte.objects.all()
    return render(request, "Soporte_Nuevo.html", {"soporte": SoporteListados})
def soporte_registrar(request):
    mantenimiento = request.POST['txtMantenimiento']
    reparacion = request.POST['txtReparacion']

    soporte = Soporte.objects.create(
        mantenimiento=mantenimiento, reparacion=reparacion)
    return redirect('/Sop')

def soporte_edicion(request, id):
    soporte = Soporte.objects.get(id=id)
    return render(request, "Soporte_Editar.html", {"soporte": soporte})
def soporte_editar(request,id):
    mantenimiento = request.POST['txtMantenimiento']
    reparacion = request.POST['txtReparacion']

    soporte = Soporte.objects.get(id=id)
    soporte.mantenimiento = mantenimiento
    soporte.reparacion = reparacion
    soporte.save()
    return redirect('/Sop')

def soporte_eliminacion(request, id):
    soporte = Soporte.objects.get(id=id)
    return render(request, "Soporte_Eliminar.html", {"soporte": soporte})

def soporte_eliminar(request,id):
    soporte = Soporte.objects.get(id=id)
    soporte.delete()
    return redirect('/Sop')

def soporte_buscar(request):
    id = request.POST['numId']
    soporte = Soporte.objects.filter(id=id)
    return render(request, "Soporte.html", {"soporte": soporte})

def contacto(request):
    return render(request, "Contactos.html")

def acerca_de(request):
    return render(request, "Acerca_de.html")

#################################
#################################

def lista_contenidos(request):
    contenidos = Contenido.objects.all()
    return render(request, 'contenido/lista_contenidos.html', {'contenidos': contenidos})

def detalle_contenido(request, id):
    contenido = get_object_or_404(Contenido, id=id)
    return render(request, 'contenido/detalle_contenido.html', {'contenido': contenido})
def subir_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Contenido subido exitosamente!")
            return redirect('lista_contenidos')
        else:
            messages.error(request, "Ocurrió un error. Verifica los datos ingresados.")
    else:
        form = ContenidoForm()
    
    return render(request, 'contenido/subir_contenido.html', {'form': form})

def gemini_demo(request):
    if request.method == "POST":
        prompt = request.POST.get('respuestas_json')
        if prompt:
            resultado_md  = gemini_chat(prompt)
            resultado_html = markdown.markdown(resultado_md, extensions=['fenced_code', 'tables'])
    return render(request, 'acento/final_resultado.html', {'resultado': resultado_html})

####################
#ACENTUACIÓN CON LOGIN PERSONALIZADO
def vista_resultado(request):
    if request.method == 'POST':
        data = request.POST.get('respuestas_json')
        respuestas = json.loads(data)
        
        #Gemini
        resultado_md = gemini_chat(data)
        #Chat gpt
        #resultado_md = analizar_respuestas(data) 
        
        resultado_html = markdown.markdown(resultado_md, extensions=['fenced_code', 'tables'])
        print(data)
    
        # Aquí, calcula aciertos/errores como prefieras
        #aciertos = sum(1 for r in respuestas if r.get('aciertos') is True)
        #errores = len(respuestas) - aciertos

        # Crea el intento asociado al usuario autenticado
        intento = IntentoAcentuacion.objects.create(
            usuario=str(request.user) if hasattr(request, 'user') else "anonimo",
            #puntaje=aciertos,
            #errores=errores
        )

        for r in respuestas:
            MovimientoAcentuacion.objects.create(
                intento=intento,
                palabra_incorrecta=r['incorrecta'],
                palabra_correcta=r['correcta'],
                clasificacion=r['clasificacion'],
                #acierto=r.get('acierto', False)
            )

        # ... renderizado de resultado, recomendaciones, etc.
        return render(request, 'acento/final_resultado.html', {'resultado': resultado_html})


@csrf_exempt
def guia_ortografia(request):
    if request.method == 'POST':
        data = request.POST.get('respuestas_json')
        resultado_md  = analizar_respuestas(data)
        resultado_html = markdown.markdown(resultado_md, extensions=['fenced_code', 'tables'])
        print(data)
        return render(request, 'acento/final_resultado.html', {'resultado': resultado_html})
    """
    resultado = None
    recomendaciones = []
    if request.method == 'POST':
        texto = request.POST.get('respuesta')
        tool = language_tool_python.LanguageTool('es')
        errores = tool.check(texto)

        resultado = {
            'total': len(errores),
            'errores': errores,
        }

        # Análisis simple para recomendar contenido
        palabras_clave = [e.ruleIssueType for e in errores if e.ruleIssueType == 'misspelling']
        if palabras_clave:
            recomendaciones = Contenido.objects.filter(titulo__icontains="acentuación")

    return render(request, 'guia/guia_ortografia.html', {
        'resultado': resultado,
        'recomendaciones': recomendaciones
    })"""
@login_required    
def menu(request):
    return render(request, "menu/menu.html")

def guia_aprendizaje(request):
    return render(request, "menu/guia_aprendizaje.html")

def acento_1(request):
    return render(request, "acento/ejercicio_1.html")

def acento_1_2(request):
    return render(request, "acento/ejercicio_1_2.html")

def acento_final(request):
    return render(request, "acento/final.html")

@csrf_exempt
def chat_con_gemini(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mensaje = data.get("mensaje", "")
        respuesta = model.generate_content(mensaje)
        return JsonResponse({"respuesta": respuesta.text})
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def chat_with_openai(request):
    if request.method == "POST":
        try:
            data  = json.loads(request.body)
            mensaje = data.get("mensaje", "")
            if not mensaje:
                return JsonResponse({"error": "Mensaje vacío"}, status=400)
            # Petición al modelo GPT-4.1 Turbo (nuevo estilo)
            respuesta = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "Sos un asistente útil."},
                    {"role": "user", "content": mensaje}
                ]
            )

            return JsonResponse({
                "respuesta": respuesta.choices[0].message.content
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Solo se aceptan peticiones POST"}, status=405)


def chat_page(request):
    return render(request, 'chat/chat.html')


#BIBLIOTECA VIRTUAL
def biblioteca(request):
    query = request.GET.get('q', '')
    libros = Libro.objects.all()
    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(editorial__icontains=query)
        )
    else:
        libros = Libro.objects.all()
    return render(request, 'biblioteca/biblioteca.html', {'libros': libros, 'query': query})

def cargar_libro(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        autor = request.POST['autor']
        editorial = request.POST['editorial']
        año = request.POST['año']
        archivo = request.FILES['archivo']

        ext = archivo.name.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return render(request, 'cargar.html', {'error': 'Formato de archivo no permitido.'})

        Libro.objects.create(
            titulo=titulo,
            autor=autor,
            editorial=editorial,
            año=año,
            archivo=archivo
        )
        return redirect('biblioteca')
    return render(request, 'biblioteca/cargar.html')

def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.titulo = request.POST['titulo']
        libro.autor = request.POST['autor']
        libro.editorial = request.POST['editorial']
        libro.año = request.POST['año']
        if 'archivo' in request.FILES:
            archivo = request.FILES['archivo']
            ext = archivo.name.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                return render(request, 'biblioteca/editar.html', {'libro': libro, 'error': 'Formato no permitido'})
            libro.archivo = archivo
        libro.save()
        return redirect('biblioteca')
    return render(request, 'biblioteca/editar.html', {'libro': libro})

def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.delete()
        return redirect('biblioteca')
    return render(request, 'biblioteca/eliminar.html', {'libro': libro})

###PORTAL SELECCIÓN
def portal_selection(request):
    """Render a simple landing page where the user chooses which portal to use."""
    return render(request, 'menu/portal_selection.html')

#LOGIN DOCENTE
def login_docente(request):
    """Muestra el formulario de inicio de sesión y autentica al usuario.

    Si las credenciales son válidas, la sesión se inicia y se redirige
    al panel de control. De lo contrario, se muestran errores dentro del
    formulario.
    """
    if request.user.is_authenticated:
        return redirect("menu")
    form = LoginDocente(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # La autenticación ya se realiza en form.clean()
            user = form.user  # type: ignore[attr-defined]
            login(request, user)
            return redirect("menu")
    return render(request, "login/docente/login.html", {"form": form})

def register_docente(request):
    """Permite a un nuevo docente crear una cuenta.

    Utiliza ``RegisterForm`` para recoger los datos requeridos y
    crear un usuario Docente. Tras el registro, redirige al inicio
    de sesión.
    """
    if request.user.is_authenticated:
        return redirect("menu")
    form = RegisterDocente(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("login_docente")
    return render(request, "login/docente/registro.html", {"form": form})

def logout_docente(request):
    """Cierra la sesión del usuario y redirige al inicio de sesión."""
    logout(request)
    return redirect("login_docente")

def forgot_password_docente(request):
    """Solicita un código de restablecimiento enviándolo por correo.

    El usuario introduce su cédula y correo electrónico. Si se encuentra
    una coincidencia válida, se genera un código de seis dígitos y se
    envía por correo utilizando la configuración SMTP definida en
    ``settings``. El código se almacena en el campo ``reset_code`` de
    la instancia Docente y el ID del usuario se guarda en la sesión
    para la siguiente etapa.
    """
    form = ForgotPasswordDocente(request.POST or None)
    sent = False
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            cedula = form.cleaned_data["cedula"]
            try:
                user = Docente.objects.get(cedula=cedula, email=email)
                # Genera un código de seis dígitos
                code = f"{random.randint(100000, 999999)}"
                user.reset_code = code
                user.save()
                # Construye el mensaje de correo
                subject = "Código de restablecimiento de contraseña"
                message = (
                    f"Hola {user.nombre},\n\n"
                    f"Tu código de restablecimiento es: {code}\n\n"
                    "Si no solicitaste este código, puedes ignorar este correo."
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                # Guarda el ID del usuario en la sesión para la siguiente vista
                request.session["reset_user_id"] = user.id
                sent = True
            except Docente.DoesNotExist:
                form.add_error(None, "No se encontró un usuario con esa cédula y correo.")
    return render(request, "login/docente/forgot_password.html", {"form": form, "sent": sent})

def reset_password_docente(request):
    """Permite al usuario establecer una nueva contraseña utilizando un código.

    Se recupera el ID del usuario almacenado en la sesión. Si no existe,
    redirige a la vista de solicitud de código. Se compara el código
    introducido con el almacenado en el modelo. Si coincide, la
    contraseña se actualiza y se limpia el campo de código y la sesión.
    """
    user_id = request.session.get("reset_user_id")
    if not user_id:
        return redirect("forgot_password")
    try:
        user = Docente.objects.get(id=user_id)
    except Docente.DoesNotExist:
        return redirect("forgot_password")
    form = ResetPasswordDocente(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            code = form.cleaned_data["code"]
            if code != user.reset_code:
                form.add_error("code", "Código incorrecto.")
            else:
                # Restablece la contraseña y limpia el código
                user.set_password(form.cleaned_data["password1"])
                user.reset_code = ""
                user.save()
                # Limpia la sesión
                del request.session["reset_user_id"]
                return redirect("login_docente")
    return render(request, "login/docente/reset_password.html", {"form": form})

#######################
#LOGIN ESTUDIANTE
def login_estudiante(request):
    if request.method == 'POST':
        form = LoginEstudiante(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = LoginEstudiante()
    return render(request, 'login/estudiante/login.html', {'form': form})

def register_estudiante(request):
    if request.method == 'POST':
        form = EstudianteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_estudiante')
    else:
        form = EstudianteRegistrationForm()
    return render(request, 'login/estudiante/registro.html', {'form': form})

def logout_estudiante(request):
    """Cierra la sesión del usuario y redirige al inicio de sesión."""
    logout(request)
    return redirect("login_estudiante")

def forgot_password_estudiante(request):
    if request.method == 'POST':
        form = ForgotPasswordEstudiante(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = f'{random.randint(100000, 999999)}'
            estudiante = Estudiante.objects.get(email=email)
            estudiante.reset_code = code
            estudiante.save()
            send_mail('Código de recuperación', f'Su código es {code}', settings.EMAIL_HOST_USER, [email])
            return redirect('reset_password')
    else:
        form = ForgotPasswordEstudiante()
    return render(request, 'login/estudiante/forgot_password.html', {'form': form})

def reset_password_estudiante(request):
    if request.method == 'POST':
        form = ResetPasswordEstudiante(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']
            estudiante = Estudiante.objects.get(reset_code=code)
            estudiante.set_password(new_password)
            estudiante.reset_code = ''
            estudiante.save()
            return redirect('login_estudiante')
    else:
        form = ResetPasswordEstudiante()
    return render(request, 'login/estudiante/reset_password.html', {'form': form})
