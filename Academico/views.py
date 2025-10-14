from django.shortcuts import render, redirect, get_object_or_404
from .models import Administrador,Alumnos,Asignatura,Asistencia,Categorias,Nota,Soporte
from django.http import HttpResponse, Http404

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

from .models import Usuario, Docente, Estudiante, PasswordResetCode

from .forms import LoginForm, RegisterForm, ResetRequestForm, ResetVerifyForm
from datetime import timedelta
from django.utils import timezone
from .decorators import role_login_required
from django.utils.http import url_has_allowed_host_and_scheme
##########################
#REACT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Libro
from .serializer import LibroSerializer

#######################
#Ejercicio1 Acentuación
import json, uuid, os
from decimal import Decimal
from typing import Dict, Any

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import ExerciseAttempt, ExplanationRequest, ActionLog, ResultSummary

#Ejercicio2 Acentuación
from .models import Exercise2Attempt, Exercise2Result
from django.views.decorators.http import require_POST
from django.urls import reverse

#Puntuación Final
from .models import PunctuationAttempt, PunctuationResult
from typing import List, Dict, Any

# === ReportLab (PDF) ===
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

#Calendario
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Min, Max, Count

#Ecuesta
from .models import SurveyAttempt, SurveyResult

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
def home(request, title):
    return render(request, "base.html", {"rol":title})
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
        #resultado_md = gemini_chat(data)
        #Chat gpt
        resultado_md = analizar_respuestas(data) 
        
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
def _redirect_next_or(request, fallback_name):
    nxt = request.GET.get("next")
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        return redirect(nxt)
    return redirect(fallback_name)

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def menu_estudiante(request):
    return render(request, "menu/estudiante/menu.html", {"rol": "Estudiante", "user": request.user})

@role_login_required(Usuario.DOCENTE, login_url_name="login_docente")
def menu_docente(request):
    return render(request, "menu/docente/menu.html", {"rol": "Docente", "user": request.user})

def guia_aprendizaje(request):
    return render(request, "menu/estudiante/guia_aprendizaje.html")

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
    return _login_role(request, role=Usuario.DOCENTE, title="Login Docente")

def login_estudiante(request):
    return _login_role(request, role=Usuario.ESTUDIANTE, title="Login Estudiante")

def _login_role(request, role, title):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
            cedula = form.cleaned_data['cedula']
            password = form.cleaned_data['password']
            user = authenticate(request, username=cedula, password=password)
            if user is None:
                messages.error(request, "Credenciales inválidas.")
            elif user.role != role:
                messages.error(request, "Rol incorrecto para este login.")

            elif user and user.role == 'DOCENTE':
                login(request, user)
                messages.success(request, f"¡Bienvenido, {user.nombre}!")
                return redirect("menu_docente")            
            elif user and user.role == 'ESTUDIANTE':
                login(request, user)
                messages.success(request, f"¡Bienvenido, {user.nombre}!")
                return redirect("menu_estudiante")
            else:
                messages.error(request,"Credenciales inválidas o rol incorrecto")
    else:
        form = LoginForm()
    return render(request, "login/login.html", {"form": form, "title": title})

# ======== Registro ========
def register_docente(request):
    return _register_role(request, role=Usuario.DOCENTE, title="Crear cuenta Docente")

def register_estudiante(request):
    return _register_role(request, role=Usuario.ESTUDIANTE, title="Crear cuenta Estudiante")

def _register_role(request, role, title):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = Usuario.objects.create_user(
                cedula=form.cleaned_data['cedula'],
                email=form.cleaned_data['email'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                role=role,
                password=form.cleaned_data['password1'],
            )
            if role == Usuario.DOCENTE:
                Docente.objects.create(user=user, cedula=user.cedula, nombre=user.nombre, apellido=user.apellido)
            else:
                Estudiante.objects.create(user=user, cedula=user.cedula, nombre=user.nombre, apellido=user.apellido)
        
            messages.success(request, "Cuenta creada. Ya podés iniciar sesión.")
            return redirect("login_docente" if role == Usuario.DOCENTE else "login_estudiante")
    else:
        form = RegisterForm()
    return render(request, "login/registro.html", {"form": form, "title": title})


def logout_docente(request):
    """Cierra la sesión del usuario y redirige al inicio de sesión."""
    logout(request)
    return redirect("login_docente")

# ======== Reset por Código (2 pasos) ========
def reset_request(request):
    if request.method == "POST":
        form = ResetRequestForm(request.POST)
        if form.is_valid():
            ident = form.cleaned_data["identificador"]
            user = _find_user_by_ident(ident)
            if not user:
                messages.error(request, "Usuario no encontrado.")
            else:
                code = f"{random.randint(0, 999999):06d}"
                prc = PasswordResetCode.objects.create(
                    user=user,
                    code=code,
                    expires_at=timezone.now() + timedelta(minutes=10)
                )
                _send_code_email(user, code)
                messages.success(request, "Te enviamos el código a tu correo.")
                return redirect("reset_verify")
    else:
        form = ResetRequestForm()
    return render(request, "login/reset_request.html", {"form": form, "title": "Recuperar contraseña"})

def reset_verify(request):
    if request.method == "POST":
        form = ResetVerifyForm(request.POST)
        if form.is_valid():
            ident = form.cleaned_data["identificador"]
            user = _find_user_by_ident(ident)
            if not user:
                messages.error(request, "Usuario no encontrado.")
            else:
                code = form.cleaned_data["code"]
                prc = PasswordResetCode.objects.filter(user=user, code=code, used=False).order_by('-created_at').first()
                if not prc or not prc.is_valid():
                    messages.error(request, "Código inválido o vencido.")
                else:
                    user.set_password(form.cleaned_data["new_password1"])
                    user.save()
                    prc.used = True
                    prc.save()
                    messages.success(request, "Contraseña actualizada. Iniciá sesión.")
                    return redirect("login_docente" if user.role == Usuario.DOCENTE else "login_estudiante")
    else:
        form = ResetVerifyForm()
    return render(request, "login/reset_verify.html", {"form": form, "title": "Verificar código"})


def logout_estudiante(request):
    """Cierra la sesión del usuario y redirige al inicio de sesión."""
    logout(request)
    return redirect("login_estudiante")

# ======== Helpers ========
def _send_code_email(user, code):
    subject = "Tu código de recuperación"
    body = f"Hola {user.nombre},\n\nTu código de verificación es: {code}\nTiene validez de 10 minutos.\n\nSi no solicitaste esto, ignorá este correo."
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

def _find_user_by_ident(ident):
    try:
        if "@" in ident:
            return Usuario.objects.get(email__iexact=ident)
        return Usuario.objects.get(cedula=ident)
    except Usuario.DoesNotExist:
        return None


#######################
#Ejercicio1 Acentuación

# ---------- utilidades ----------
def _ensure_run_id(request: HttpRequest) -> str:
    run_id = request.session.get("run_id")
    if not run_id:
        run_id = uuid.uuid4().hex[:12]
        request.session["run_id"] = run_id
    return run_id

def _log(user, run_id: str, exercise_number: int, action: str, metadata: Dict[str, Any] = None):
    ActionLog.objects.create(
        user=user, run_id=run_id, exercise_number=exercise_number, action=action, metadata=metadata or {}
    )

def _openai_explain(prompt: str) -> str:
    """
    Llama a OpenAI si hay clave y librería instalada; si no, devuelve explicación local.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return prompt  # caemos al prompt (que ya contiene buena explicación)
    try:
        # Cliente nuevo (openai>=1.x)
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=api_key)
        msg = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Eres un profesor de lengua conciso. Explica ortografía del español con ejemplos."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=220,
        )
        return msg.choices[0].message.content or "No se obtuvo texto de la IA."
    except Exception:
        # fallback “old school” por si cambia el SDK
        return prompt

# ---------- Ejercicio 1 ----------
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def exercise1(request: HttpRequest) -> HttpResponse:
    run_id = _ensure_run_id(request)
    _log(request.user, run_id, 1, "visit")
    options = ["rapido", "rapidó", "rápido"]
    # distinto por usuario: reordenamos
    options.sort(key=lambda x: (hash(request.user.id + hash(run_id + x)) % 10))
    context = {"options": options}
    return render(request, "acento/ejercicio_1/e1.html", context)

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
@require_http_methods(["POST"])
def exercise1_submit(request: HttpRequest) -> JsonResponse:
    run_id = _ensure_run_id(request)
    selected = request.POST.get("answer", "")
    correct = "rápido"
    is_correct = (selected == correct)
    attempt = ExerciseAttempt.objects.create(
        user=request.user,
        run_id=run_id,
        exercise_number=1,
        user_answer=selected,
        correct_answer=correct,
        is_correct=is_correct,
        score=Decimal("1.00") if is_correct else Decimal("0.00"),
    )
    _log(request.user, run_id, 1, "submit", {"selected": selected, "is_correct": is_correct})

    if is_correct:
        feedback = "¡Así se hace!"
    else:
        feedback = "¡Incorecta!, La palabra correcta es <b>rápido</b>"

    return JsonResponse({
        "ok": True,
        "attempt_id": attempt.id,
        "correct": is_correct,
        "feedback_html": feedback,
        "next_url": "/acento_1/2/",
    })

# ---------- Ejercicio 2 ----------
WORDS2 = {
    "Atención": "Agudas",
    "Árbol": "Llanas",
    "Número": "Esdrújulas",
    "Cálidamente": "Sobresdrújulas",
}

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def exercise2(request: HttpRequest) -> HttpResponse:
    run_id = _ensure_run_id(request)
    _log(request.user, run_id, 2, "visit")
    # orden aleatorio/consistente por usuario
    items = list(WORDS2.items())
    items.sort(key=lambda kv: (hash(request.user.id + hash(run_id + kv[0])) % 10))
    categories = ["Agudas", "Llanas", "Esdrújulas", "Sobresdrújulas"]
    return render(request, "acento/ejercicio_1/e2.html", {"items": items, "categories": categories})

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
@require_http_methods(["POST"])
def exercise2_submit(request: HttpRequest) -> JsonResponse:
    run_id = _ensure_run_id(request)
    answers = {}
    for word in WORDS2.keys():
        answers[word] = request.POST.get(word, "")

    mistakes = []
    correct_count = 0
    for word, expected in WORDS2.items():
        user_val = answers.get(word)
        ok = (user_val == expected)
        if ok:
            correct_count += 1
        else:
            mistakes.append((word, expected))
        # guardamos intento por cada palabra (para granularidad y trazabilidad)
        attempt=ExerciseAttempt.objects.create(
            user=request.user,
            run_id=run_id,
            exercise_number=2,
            user_answer=json.dumps({word: user_val}),
            correct_answer=json.dumps({word: expected}),
            is_correct=ok,
            score=Decimal("1.00") if ok else Decimal("0.00"),
            meta={"word": word},
        )

    _log(request.user, run_id, 2, "submit", {"answers": answers, "correct_count": correct_count})

    total = len(WORDS2)
    if correct_count == total:
        feedback = "<div class='big-ok'>¡Acertaste todas!</div>"
    elif correct_count == 0:
        lines = [
            "<div class='big-warn'>Resultados:</div>",
            "La palabra Atención es <b>Aguda</b>",
            "La palabra Árbol es <b>Llana o grave</b>",  # llanas/graves
            "La palabra Número es <b>Esdrújula</b>",
            "La palabra Cálidamente es <b>Sobresdrújula</b>",
            "<div class='big-hint'>Falta reforzar un poco, ¡Ánimo!</div>",
        ]
        feedback = "<br>".join(lines)
    else:
        lines = []
        for w, exp in mistakes:
            lines.append(f"La palabra <b>{w}</b> es <b>{exp}</b>")
        lines.append(f"<div class='big-ok'>¡Felicidades acertaste {correct_count} de {total}!</div>")
        feedback = "<br>".join(lines)

    return JsonResponse({
        "ok": True,
        "attempt_id": attempt.id,  # ya se guardó 1 por palabra
        "feedback_html": feedback,
        "next_url": "/acento_1/3/",
    })

# ---------- Ejercicio 3 ----------
QUESTION3 = {"word": "exhibición", "correct": "Agudas"}
CATEGORIES3 = ["Agudas", "Llanas", "Esdrújulas", "Sobresdrújulas"]

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def exercise3(request: HttpRequest) -> HttpResponse:
    run_id = _ensure_run_id(request)
    _log(request.user, run_id, 3, "visit")
    # reordenamos categorías para “ser diferente” por usuario
    cats = CATEGORIES3[:]
    cats.sort(key=lambda c: (hash(request.user.id + hash(run_id + c)) % 10))
    return render(request, "acento/ejercicio_1/e3.html", {"word": QUESTION3["word"], "categories": cats})

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
@require_http_methods(["POST"])
def exercise3_submit(request: HttpRequest) -> JsonResponse:
    run_id = _ensure_run_id(request)
    selected = request.POST.get("answer", "")
    correct = QUESTION3["correct"]
    is_correct = (selected == correct)

    attempt = ExerciseAttempt.objects.create(
        user=request.user,
        run_id=run_id,
        exercise_number=3,
        user_answer=selected,
        correct_answer=correct,
        is_correct=is_correct,
        score=Decimal("1.00") if is_correct else Decimal("0.00"),
        meta={"word": QUESTION3["word"]},
    )
    _log(request.user, run_id, 3, "submit", {"selected": selected, "is_correct": is_correct})

    if is_correct:
        txt = f"¡Correcta! la palabra <b>{QUESTION3['word']}</b> es <b>{correct}</b>."
    else:
        txt = f"¡Incorrecta! la palabra <b>{QUESTION3['word']}</b> es <b>{correct}</b>."
    return JsonResponse({
        "ok": True,
        "attempt_id": attempt.id,
        "feedback_html": f"{txt}",
        "next_url": "/acento_1/resultados/",
    })

# ---------- Explicación (IA) ----------
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
@require_http_methods(["POST"])
def explain_attempt(request: HttpRequest, attempt_id: int) -> JsonResponse:
    attempt = get_object_or_404(ExerciseAttempt, pk=attempt_id, user=request.user)
    run_id = attempt.run_id
    _log(request.user, run_id, attempt.exercise_number, "explain", {"attempt_id": attempt_id})

    # prompt base según ejercicio
    if attempt.exercise_number == 1:
        body = (
            "Explica por qué en la frase 'El perro come muy rápido' la forma correcta es 'rápido'. "
            "Incluye: tipo de palabra (esdrújula), regla de acentuación y 1 ejemplo extra."
        )
    elif attempt.exercise_number == 2:
        body = (
            "Explica brevemente las categorías de acentuación: agudas, llanas, esdrújulas y sobresdrújulas. "
            "Justifica la clasificación de: Atención (Aguda), Árbol (Llana), Número (Esdrújula), Cálidamente (Sobresdrújula)."
        )
    else:
        body = (
            "Explica por qué 'exhibición' es aguda: termina en 'n' o 's' o vocal y se acentúa cuando la sílaba tónica es la última "
            "y requiere tilde por terminación. Da 1 ejemplo adicional."
        )

    # Si fue incorrecto, pide también marcar el error
    correctness = "El estudiante acertó su respuesta." if attempt.is_correct else "El estudiante se equivocó."
    prompt = f"{correctness} {body}"

    resp = _openai_explain(prompt)
    ExplanationRequest.objects.create(user=request.user, attempt=attempt, model_response=resp)
    return JsonResponse({"ok": True, "explanation_html": f"<div class='explanation'>{resp}</div>"})

# ---------- Resultados ----------
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def results_view(request: HttpRequest) -> HttpResponse:
    run_id = _ensure_run_id(request)

    # Tareas totales: 1 (e1) + 4 (e2) + 1 (e3) = 6
    attempts = ExerciseAttempt.objects.filter(user=request.user, run_id=run_id)
    correct = sum(1 for a in attempts if a.is_correct)
    total = 6
    percentage = (correct / total) * 100 if total else 0

    breakdown = {
        "e1": {"correct": sum(1 for a in attempts if a.exercise_number == 1 and a.is_correct), "total": 1},
        "e2": {"correct": sum(1 for a in attempts if a.exercise_number == 2 and a.is_correct), "total": 4},
        "e3": {"correct": sum(1 for a in attempts if a.exercise_number == 3 and a.is_correct), "total": 1},
    }

    ResultSummary.objects.update_or_create(
        user=request.user, run_id=run_id,
        defaults={
            "total_items": total, "correct_items": correct,
            "percentage": round(Decimal(percentage), 2), "breakdown": breakdown
        }
    )

    # mensaje final
    if percentage == 100:
        title = "¡Completaste todos los ejercicios sin errores, sigue así! 100%"
        rec = None
    elif percentage > 60:
        title = f"¡Felicidades acertaste el {int(round(percentage))}%!"
        rec = "Recomendación: Reforzar más en el capítulo de Acentuación del libro *Ortografía de la lengua española* (RAE)."
    else:
        title = f"¡Faltaría reforzar más, solo acertaste el {int(round(percentage))}%!"
        rec = "Recomendación: Reforzar el capítulo de Acentuación del libro *Ortografía de la lengua española* (RAE)."

    _log(request.user, run_id, 4, "visit", {"percentage": percentage})
    # Limpia el run para un nuevo intento cuando vuelvan a empezar
    request.session.pop("run_id", None)
    return render(request, "acento/ejercicio_1/r.html", {"title": title, "recommendation": rec})


#Evaluaciones y Reportes

################################################################################
# Evaluations (Resultados de unidades y reporte PDF)
################################################################################

# Mapping between units and the exercise numbers that belong to each unit.  You
# should adjust this mapping to reflect the actual exercises per unit in your
# application.  For example, if Unidad I incluye los ejercicios 1 y 2, coloca
# esos números en la lista.  Si hay nuevas unidades, añádelas aquí.
UNIT_MAPPING = {
    "Unidad I: Acentuación": [1, 2, 3],
    "Unidad II: Puntuación": [4, 5, 6],
    "Unidad III: Reglas de las Letras": [7, 8, 9],
}


def _get_color_class(percent: int) -> str:
    """Return a CSS class name based on a percentage value."""
    if percent >= 100:
        return "complete"
    if percent >= 80:
        return "green"
    if percent >= 60:
        return "lime"
    if percent >= 40:
        return "yellow"
    if percent >= 20:
        return "orange"
    return "red"


# Mapea % → etiqueta de dominio (ajusta si querés otros nombres/umbrales)
def _domain_label(p: int | None) -> str:
    if p is None:
        return "N/A"
    if p >= 90: return "Excelente"
    if p >= 80: return "Muy Satisfactorio"
    if p >= 60: return "Satisfactorio"
    if p >= 40: return "Básico"
    return "Insuficiente"

def _student_name(user) -> str:
    full = (user.nombre + " " + user.apellido or "").strip()
    return full if full else user.nombre + " " + user.apellido

def _student_id(user) -> str:
    for attr in ("cedula", "dni", "documento"):
        if hasattr(user, attr) and getattr(user, attr):
            return str(getattr(user, attr))
    prof = getattr(user, "profile", None)
    if prof:
        for attr in ("cedula", "dni", "documento"):
            if hasattr(prof, attr) and getattr(prof, attr):
                return str(getattr(prof, attr))
    return "—"

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def evaluaciones(request: HttpRequest) -> HttpResponse:
    # Configura tus unidades reales (IDs de ejercicios por unidad)
    UNITS = [
        {"key": "U1", "title": "Acentuación",             "exercises": [1, 2, 3]},
        {"key": "U2", "title": "Puntuación",               "exercises": [4, 5]},
        {"key": "U3", "title": "Mayúscula y Minúscula",    "exercises": [6, 7]},
        {"key": "U4", "title": "Reglas de las Letras",     "exercises": [8]},  # si no usás, queda N/A
    ]

    rows = []
    for u in UNITS:
        ex_numbers = u["exercises"]

        # intentos por unidad
        stats_qs = (
            ExerciseAttempt.objects
            .filter(user=request.user, exercise_number__in=ex_numbers)
        )
        total = stats_qs.count()
        correct = stats_qs.filter(is_correct=True).count()
        percent = None if total == 0 else int(round((correct / total) * 100))

        # ¿usó IA? (al menos una explicación en esos ejercicios)
        used_ia = ExplanationRequest.objects.filter(
            attempt__user=request.user,
            attempt__exercise_number__in=ex_numbers
        ).exists()

        rows.append({
            "unidad": u["title"],
            "percent": percent,                         # None → N/A
            "dominio": _domain_label(percent),
            "ia": ("N/A" if total == 0 else ("Sí" if used_ia else "No")),
        })

    context = {
        "student_name": _student_name(request.user),
        "student_id": _student_id(request.user),
        "rows": rows,
    }
    return render(request, "reporte/evaluaciones.html", context)


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def evaluaciones_report(request: HttpRequest) -> HttpResponse:
    """
    PDF con ReportLab (canvas) – formato anterior (fuentes más grandes),
    eliminando la columna 'Uso de IA'.
    """
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import Color, black, white
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    # === Datos ===
    UNITS = [
        {"key": "U1", "title": "Acentuación",             "exercises": [1, 2, 3]},
        {"key": "U2", "title": "Puntuación",               "exercises": [4, 5]},
        {"key": "U3", "title": "Mayúscula y Minúscula",    "exercises": [6, 7]},
        {"key": "U4", "title": "Reglas de las Letras",     "exercises": [8]},
    ]
    rows = []
    for u in UNITS:
        ex_numbers = u["exercises"]
        qs = ExerciseAttempt.objects.filter(user=request.user, exercise_number__in=ex_numbers)
        total = qs.count()
        correct = qs.filter(is_correct=True).count()
        percent = None if total == 0 else int(round((correct/total)*100))
        # seguimos calculando lo demás si querés, pero ya no lo mostramos
        rows.append({
            "unidad": u["title"],
            "percent": percent,
            "dominio": _domain_label(percent),
        })

    # === Layout (estilo anterior) ===
    PAGE_W, PAGE_H = A4
    mm = 72 / 25.4
    M_L, M_R, M_T, M_B = 20*mm, 20*mm, 18*mm, 18*mm

    GREEN = Color(86/255, 140/255, 0/255)
    GREEN_LIGHT = Color(235/255, 246/255, 220/255)

    try:
        pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
        FONT_REG, FONT_BOLD = "DejaVu", "DejaVu-Bold"
    except Exception:
        FONT_REG, FONT_BOLD = "Helvetica", "Helvetica-Bold"

    def strw(txt, font, size): return pdfmetrics.stringWidth(txt, font, size)

    def draw_center(c, x, w, y, txt, font, size, col=black):
        c.setFont(font, size); c.setFillColor(col)
        c.drawString(x + (w - strw(txt, font, size))/2.0, y, txt)

    def wrap(txt, font, size, max_w):
        out, line = [], ""
        for w in txt.split():
            probe = (line + " " + w).strip()
            if strw(probe, font, size) <= max_w or not line:
                line = probe
            else:
                out.append(line); line = w
        if line: out.append(line)
        return out

    buf = BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
    c.setTitle("Reporte de Evaluaciones")

    y = PAGE_H - M_T

    # Título (caja, tamaño “anterior”)
    TITLE = "Reporte de Evaluaciones"
    c.setStrokeColor(GREEN); c.setLineWidth(2)
    c.setFont(FONT_BOLD, 20)
    tw = strw(TITLE, FONT_BOLD, 20)
    x_title = (PAGE_W - tw)/2.0
    c.roundRect(x_title - 12, y - 10, tw + 24, 28, 6, stroke=1, fill=0)
    c.drawString(x_title, y, TITLE)
    y -= 36

    # Información del educando (tamaños “anteriores”)
    c.setFont(FONT_BOLD, 14); c.setFillColor(black)
    c.drawString(M_L, y, "Información del Educando")
    y -= 18
    c.setFont(FONT_REG, 12)
    c.drawString(M_L, y, f"Nombre:  {_student_name(request.user)}"); y -= 16
    c.drawString(M_L, y, f"Cédula:  {_student_id(request.user)}");   y -= 24

    # === TABLA (3 columnas) ===
    headers = ["Unidad", "Puntuación", "Dominio"]
    table_w = PAGE_W - M_L - M_R
    # ancho por columnas: más espacio a “Unidad”
    props = [0.60, 0.18, 0.22]     # 60% / 18% / 22%
    col_w = [table_w*p for p in props]
    x_cols = [M_L, M_L+col_w[0], M_L+col_w[0]+col_w[1], M_L+table_w]  # 4 puntos, 3 columnas

    header_h = 20
    row_h    = 22
    PAD_X    = 6

    # Header verde
    c.setFillColor(GREEN); c.setStrokeColor(GREEN)
    c.rect(M_L, y - header_h, table_w, header_h, fill=1, stroke=1)
    c.setFillColor(white)
    draw_center(c, x_cols[0], col_w[0], y - header_h + 5, headers[0], FONT_BOLD, 11, white)
    draw_center(c, x_cols[1], col_w[1], y - header_h + 5, headers[1], FONT_BOLD, 11, white)
    draw_center(c, x_cols[2], col_w[2], y - header_h + 5, headers[2], FONT_BOLD, 11, white)
    y -= header_h

    # Filas
    c.setStrokeColor(GREEN)
    for i, r in enumerate(rows):
        # fondo alterno
        c.setFillColor(GREEN_LIGHT if i % 2 == 0 else white)
        c.rect(M_L, y - row_h, table_w, row_h, fill=1, stroke=1)

        # líneas verticales
        for xx in x_cols[1:-1]:
            c.line(xx, y - row_h, xx, y)

        # 👇 IMPORTANTE: volver a negro para el texto
        c.setFillColor(black)

        # Col 1: Unidad (wrap a 2 líneas)
        c.setFont(FONT_REG, 11)
        lines = wrap(r["unidad"], FONT_REG, 11, col_w[0] - 2*PAD_X)[:2]
        total_h = len(lines)*11 + (len(lines)-1)*2
        base_y = y - (row_h + total_h)/2 + 2
        for j, line in enumerate(lines):
            c.drawString(x_cols[0] + PAD_X, base_y + j*(11+2), line)

        # Col 2: Puntuación (centrado)
        pct_text = "N/A" if r["percent"] is None else f"{r['percent']}%"
        draw_center(c, x_cols[1], col_w[1], y - row_h + 5, pct_text, FONT_REG, 11, black)

        # Col 3: Dominio (centrado)
        draw_center(c, x_cols[2], col_w[2], y - row_h + 5, r["dominio"], FONT_REG, 11, black)

        y -= row_h
        if y < M_B + 40:
            c.showPage()
            y = PAGE_H - M_T
            # redibujar header...
            c.setFillColor(GREEN); c.setStrokeColor(GREEN)
            c.rect(M_L, y - header_h, table_w, header_h, fill=1, stroke=1)
            c.setFillColor(white)
            draw_center(c, x_cols[0], col_w[0], y - header_h + 5, headers[0], FONT_BOLD, 11, white)
            draw_center(c, x_cols[1], col_w[1], y - header_h + 5, headers[1], FONT_BOLD, 11, white)
            draw_center(c, x_cols[2], col_w[2], y - header_h + 5, headers[2], FONT_BOLD, 11, white)
            y -= header_h


    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()

    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'inline; filename="reporte_evaluaciones.pdf"'
    return resp




###########################
#Calendario
###########################
# Mapa de unidades -> ejercicios (ajusta a tus IDs reales)
UNITS = [
    {"key": "U1", "title": "Acentuación",             "exercises": [1, 2, 3]},
    {"key": "U2", "title": "Puntuación",               "exercises": [4, 5]},
    {"key": "U3", "title": "Mayúscula y Minúscula",    "exercises": [6, 7]},
    {"key": "U4", "title": "Reglas de las Letras",     "exercises": [8]},
]
# Diccionario rápido: ejercicio -> nombre de unidad
EX_TO_UNIT = {ex: u["title"] for u in UNITS for ex in u["exercises"]}

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def calendario(request):
    """Render del calendario del alumno logueado."""
    today = timezone.localdate()
    return render(request, "calendario/calendario.html", {"today": today})

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def calendario_events(request):
    """
    Devuelve eventos agrupados por día:
    - start: 'YYYY-MM-DD'
    - title: cantidad (para pintar badge)
    - extendedProps.units: lista única de unidades trabajadas ese día
    """
    # podés filtrar por rango si querés (start/end de FullCalendar):
    # start = request.GET.get("start")  # 'YYYY-MM-DD'
    # end   = request.GET.get("end")

    attempts = (
        ExerciseAttempt.objects
        .filter(user=request.user)
        .values("created_at", "exercise_number")
    )

    per_day = defaultdict(lambda: {"count": 0, "units": set()})
    for a in attempts:
        # ✅ usar fecha LOCAL (America/Asuncion) para agrupar
        local_dt = timezone.localtime(a["created_at"])
        day = local_dt.date()
        per_day[day]["count"] += 1
        per_day[day]["units"].add(EX_TO_UNIT.get(a["exercise_number"], "Unidad"))


    events = []
    for day, info in per_day.items():
        events.append({
            "id": str(day),
            "start": day.isoformat(),
            "title": str(info["count"]),            # badge
            "allDay": True,
            "extendedProps": {
                "units": sorted(info["units"]),
            },
        })
    return JsonResponse(events, safe=False)

@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def calendario_detalle(request):
    """Lista de actividades por unidad del día seleccionado (rango local [00:00, 24:00))."""
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"items": []})

    try:
        y, m, d = map(int, date_str.split("-"))
    except Exception:
        return JsonResponse({"items": []})

    # --- Rango del día en zona LOCAL (America/Asuncion) ---
    tz = timezone.get_current_timezone()
    base_start = datetime(y, m, d, 0, 0, 0)              # naive
    if settings.USE_TZ:
        # 🟢 zoneinfo: usar make_aware (NO .localize)
        start_local = timezone.make_aware(base_start, tz)
    else:
        start_local = base_start
    end_local = start_local + timedelta(days=1)

    qs = (
        ExerciseAttempt.objects
        .filter(
            user=request.user,
            created_at__gte=start_local,
            created_at__lt=end_local,
        )
        .values("exercise_number")
        .annotate(
            start=Min("created_at"),
            end=Max("created_at"),
            total=Count("id"),
        )
        .order_by("start")
    )

    def fmt_local(dt):
        if not dt:
            return "—"
        if settings.USE_TZ:
            dt = timezone.localtime(dt, tz)   # a hora local
        return dt.strftime("%I:%M:%S %p")

    items = []
    for row in qs:
        unidad = EX_TO_UNIT.get(row["exercise_number"], "Unidad")
        items.append({
            "unidad": unidad,
            "inicio": fmt_local(row["start"]),
            "fin": fmt_local(row["end"]),
            "total": row["total"],
        })

    return JsonResponse({"date": date_str, "items": items})

###############
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def perfil_estudiante(request):
    """
    Renderiza la página de perfil del estudiante.

    Obtiene los datos del usuario autenticado a través de `request.user`
    y los envía a la plantilla `menu/estudiante/perfil.html`.  También
    suministra un porcentaje de progreso de la guía de aprendizaje.
    Este valor es 100 por defecto, pero puede ajustarse según el avance
    real de la persona.
    """
    usuario = request.user
    # Por ahora se establece el progreso al 100%.  Ajustalo según tus
    # necesidades o calcula el valor real de manera dinámica.
    progreso = 100
    return render(request, "perfil/perfil.html", {"usuario": usuario, "progress": progreso})


#####################
#Ejercicio 2
#####################

# ---------- Constantes de configuración para el ejercicio ----------

# Definición de preguntas y respuestas correctas.  Se utiliza un
# diccionario para que sea fácil añadir más preguntas o cambiar las
# existentes sin modificar la lógica de las vistas.
EXERCISE2_QUESTIONS: Dict[int, Dict[str, Any]] = {
    1: {
        "question": "¿Cuál es la forma correcta?",
        "options": {
            "a": "huímos",
            "b": "huimos",
            "c": "huimós",
            "d": "húimos",
        },
        "correct": "b",
        "feedback_correct": "¡Así se hace!",
        # Se emplea este mensaje cuando la respuesta es errónea.
        "feedback_incorrect": "¡Incorrecta!, la palabra correcta es <b>huimos</b>",
    },
    2: {
        "question": "Palabra correctamente tildada por hiato:",
        "options": {
            "a": "pais",
            "b": "país",
            "c": "raices",
            "d": "héroe",
        },
        "correct": "b",
        "feedback_correct": "¡Bien hecho!",
        "feedback_incorrect": "¡Incorrecta!, la palabra tildada correctamente por hiato es <b>país</b>",
    },
    3: {
        "question": "Completa: “___ vienes y ___ hermano también.”",
        "options": {
            "a": "Tu / tú",
            "b": "Tú / tu",
            "c": "Tú / tú",
            "d": "Tu / tu",
        },
        "correct": "b",
        "feedback_correct": "¡Correcta!",
        "feedback_incorrect": "¡Incorrecta!, la opción correcta es b, <b>Tú / tu</b>",
    },
}


def _get_question_context(question_number: int) -> Dict[str, Any]:
    """Construye el contexto de una pregunta para pasar a la plantilla.

    Parametros:
        question_number: Número de la pregunta (1, 2 o 3).

    Devuelve:
        Un diccionario con la pregunta, las opciones y rutas para el envío
        y explicación, así como el número de pregunta.
    """
    q = EXERCISE2_QUESTIONS[question_number]
    context = {
        "num": question_number,
        "question": q["question"],
        "options": q["options"],
        # URL al que se enviará la respuesta mediante AJAX.  Se pasa el
        # número de pregunta como parámetro para distinguir las tres vistas.
        "submit_url": reverse("exercise2_question{}_submit".format(question_number)),
        # Endpoint para explicar la respuesta.  El id del intento se
        # añadirá desde el cliente tras recibir la respuesta del servidor.
        "explain_endpoint": reverse("explain_attempt2"),
    }
    return context


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def exercise2_question1(request: HttpRequest) -> HttpResponse:
    """Muestra la primera pregunta del ejercicio 2."""
    context = _get_question_context(1)
    return render(request, "acento/ejercicio_2/question.html", context)


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def exercise2_question2(request: HttpRequest) -> HttpResponse:
    """Muestra la segunda pregunta del ejercicio 2."""
    context = _get_question_context(2)
    return render(request, "acento/ejercicio_2/question.html", context)


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def exercise2_question3(request: HttpRequest) -> HttpResponse:
    """Muestra la tercera pregunta del ejercicio 2."""
    context = _get_question_context(3)
    return render(request, "acento/ejercicio_2/question.html", context)


@require_POST
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def exercise2_question1_submit(request: HttpRequest) -> JsonResponse:
    """Procesa la respuesta de la pregunta 1 y devuelve JSON con el resultado."""
    return _process_submission(request, 1)


@require_POST
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def exercise2_question2_submit(request: HttpRequest) -> JsonResponse:
    """Procesa la respuesta de la pregunta 2 y devuelve JSON con el resultado."""
    return _process_submission(request, 2)


@require_POST
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def exercise2_question3_submit(request: HttpRequest) -> JsonResponse:
    """Procesa la respuesta de la pregunta 3 y devuelve JSON con el resultado."""
    return _process_submission(request, 3)


def _process_submission(request: HttpRequest, question_number: int) -> JsonResponse:
    """Función interna para manejar la lógica de respuesta y guardado.

    Parametros:
        request: Petición HTTP con los datos enviados desde el formulario.
        question_number: Número de la pregunta que se está procesando.

    Devuelve:
        Un JsonResponse con campos:
            - correct (bool): indica si el estudiante acertó.
            - message (str): texto a mostrar de inmediato en pantalla.
            - next_url (str): URL a la siguiente pregunta o a resultados.
            - attempt_id (int): identificador del intento guardado en BD.
    """
    user = request.user
    selected_option = request.POST.get("option")
    if not selected_option:
        return JsonResponse({"error": "No se recibió ninguna opción."}, status=400)

    q_data = EXERCISE2_QUESTIONS[question_number]
    correct_option = q_data["correct"]
    is_correct = selected_option == correct_option

    # Guardar el intento en la base de datos
    attempt = Exercise2Attempt.objects.create(
        user=user,
        question_number=question_number,
        selected_option=selected_option,
        correct_option=correct_option,
        is_correct=is_correct,
    )

    # Calcular la URL de la siguiente vista
    if question_number < 3:
        next_url = reverse(f"exercise2_question{question_number + 1}")
    else:
        next_url = reverse("results2")

    message = q_data["feedback_correct"] if is_correct else q_data["feedback_incorrect"]

    return JsonResponse(
        {
            "correct": is_correct,
            "message": message,
            "next_url": next_url,
            "attempt_id": attempt.id,
        }
    )


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def explain_attempt2(request: HttpRequest) -> JsonResponse:
    """Devuelve una explicación sobre la respuesta del estudiante.

    Recibe mediante parámetros GET el `attempt_id` y opcionalmente el número
    de pregunta.  Utiliza el modelo de lenguaje de OpenAI para generar
    una explicación amigable y clara sobre por qué la opción escogida
    es correcta o incorrecta.  Si no está disponible la integración con
    OpenAI se genera un texto explicativo básico.
    """
    attempt_id = request.GET.get("attempt_id")
    if not attempt_id:
        return JsonResponse({"error": "Parámetro attempt_id ausente."}, status=400)
    try:
        attempt = Exercise2Attempt.objects.get(pk=attempt_id, user=request.user)
    except Exercise2Attempt.DoesNotExist:
        return JsonResponse({"error": "Intento no encontrado."}, status=404)

    question_data = EXERCISE2_QUESTIONS[attempt.question_number]
    selected_text = question_data["options"][attempt.selected_option]
    correct_text = question_data["options"][question_data["correct"]]

    # Construir el prompt para el modelo de lenguaje.  Intentamos dar un
    # tono pedagógico y cercano, explicando las reglas de acentuación
    # involucradas.
    prompt = (
        f"Explica al estudiante de forma concisa y amigable por qué la opción\n"
        f"'{selected_text}' {'es correcta' if attempt.is_correct else 'es incorrecta'}\n"
        f"en la pregunta: '{question_data['question']}'.\n"
        f"También menciona cuál es la forma correcta y la regla de acentuación aplicada.\n"
        f"Redacta en español sencillo y en un tono motivador."
    )

    explanation = None
    if OpenAI is not None:
        # Intentar generar la explicación utilizando la API de OpenAI si se
        # encuentra instalada y se dispone de una clave.  En caso de
        # cualquier error, se recurrirá a una explicación manual.
        try:
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if api_key:
                openai.api_key = api_key  # type: ignore[assignment]
                completion = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                    model="gpt-5-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                )
                explanation = completion.choices[0].message["content"].strip()  # type: ignore[index]
        except Exception:
            explanation = None

    if not explanation:
        # Explicación genérica si no hay acceso a la API.
        if attempt.question_number == 1:
            explanation = (
                "En español, la forma correcta del pasado de 'huir' en primera persona del plural"
                " es 'huimos' (sin tilde) porque la combinación 'ui' forma un diptongo y la "
                "sílaba tónica recae en 'ui'. Es una palabra llana que termina en 's', por ello"
                " no lleva tilde."
            )
        elif attempt.question_number == 2:
            explanation = (
                "La palabra 'país' lleva tilde en la 'í' para romper el diptongo 'ai' y formar"
                " un hiato: se pronuncia pa-ís. En cambio, 'pais' no tiene hiato y por eso"
                " sería incorrecto. 'Héroe' también es un hiato correctamente tildado, pero"
                " la pregunta pedía escoger entre las opciones dadas la que corresponde a"
                " un hiato simple de dos letras."
            )
        elif attempt.question_number == 3:
            explanation = (
                "En la frase, la primera forma debe ser 'tú' con tilde porque se trata del"
                " pronombre personal ('you' en inglés). La segunda forma es 'tu' sin tilde"
                " porque indica posesión (tu hermano). Recuerda: los pronombres personales"
                " llevan tilde diacrítica para distinguirlos de los determinantes posesivos."
            )
        else:
            explanation = "No se encontró una explicación para esta pregunta."

    return JsonResponse({"explanation": explanation})


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def results_view2(request: HttpRequest) -> HttpResponse:
    """Muestra al estudiante su puntaje final del ejercicio 2.

    Calcula el porcentaje de respuestas correctas en función de los
    intentos realizados y guarda dicho resultado.  A continuación,
    selecciona el mensaje y la recomendación apropiada según el
    porcentaje alcanzado.
    """
    user = request.user
    attempts = Exercise2Attempt.objects.filter(user=user)
    total_q = 3
    correct_count = sum(1 for a in attempts if a.is_correct)
    percentage = (correct_count / total_q) * 100

    # Guardar el resultado final
    Exercise2Result.objects.create(
        user=user,
        total_questions=total_q,
        correct_answers=correct_count,
        percentage=percentage,
    )

    # Determinar el mensaje y la recomendación según el porcentaje
    if correct_count == total_q:
        headline = "¡Completaste todos los ejercicios sin errores, sigue así!"
        recommendation = None
    elif percentage >= 60:
        headline = f"¡Felicidades acertaste el {percentage:.0f}%!"
        recommendation = (
            "Recomendación: Reforzar más en el capítulo del libro sobre acentuación. "
            "Consulta la 'Ortografía de la lengua española' de la RAE para profundizar."
        )
    else:
        headline = f"¡Faltaría reforzar un poco más, acertaste solo el {percentage:.0f}%!"
        recommendation = (
            "Recomendación: Repasa el capítulo sobre acentuación de un buen libro "
            "de ortografía, por ejemplo la 'Ortografía de la lengua española' editada "
            "por la RAE."
        )

    context = {
        "headline": headline,
        "percentage": f"{percentage:.0f}%",
        "recommendation": recommendation,
    }
    return render(request, "acento/ejercicio_2/result.html", context)


# -----------------------------------------------------------------------------
##########################################################
# Datos del ejercicio: texto sin signos de puntuación y posiciones correctas
#
# A continuación se define la lista de palabras que componen el texto y las
# posiciones (índices) en las que el estudiante debe insertar un signo de
# puntuación.  Cada posición se indica mediante el índice de la palabra
# después de la cual debe aparecer el signo.  Por ejemplo, si el índice es 7,
# significa que entre la palabra 7 y la palabra 8 se debe colocar la coma.

# Texto original adaptado del artículo “Propulsor de la educación paraguaya”.
TEXT_WORDS: List[str] = [
    "El", "Congreso", "Nacional", "reunido", "en", "marzo", "de", "1841", "el", "gobierno",
    "consular", "decretó", "el", "30", "de", "noviembre", "de", "1841", "el",
    "establecimiento", "de", "la", "Academia", "Literaria", "El", "plan", "de",
    "estudios", "comprendía", "Latinidad", "Idioma", "Castellano", "y", "Bellas", "Letras",
    "Filosofía", "Racional", "Teología", "Dogmática", "Historia", "Eclesiástica", "y",
    "Oratoria", "Sagrada", "solo", "se", "proveyó", "de", "las", "dos", "primeras",
    "cátedras", "mencionadas", "que", "se", "confiaron", "a", "los", "P", "P", "Marco",
    "Antonio", "Maíz", "simultáneamente", "director", "del", "instituto", "y", "José",
    "Joaquín", "Palacios", "Don", "Carlos", "Antonio", "López", "fue", "el", "primer",
    "presidente", "Constitucional", "del", "Paraguay", "y", "gran", "visionario", "en",
    "temas", "de", "educación", "pues", "comprendía", "que", "la", "formación",
    "académica", "era", "clave", "para", "el", "desarrollo", "de", "una", "Nación", "Una",
    "de", "las", "prácticas", "más", "reconocidas", "fue", "el", "otorgamiento", "de",
    "becas", "a", "un", "grupo", "de", "jóvenes", "destacados", "para", "que", "pudieran",
    "estudiar", "en", "el", "exterior", "una", "vez", "que", "se", "comprometían", "a",
    "retornar", "a", "la", "patria", "el", "gobierno", "les", "garantizaba", "el",
    "empleo", "se", "los", "enviaba", "para", "que", "completaran", "su", "preparación",
    "y", "al", "regresar", "podían", "ayudar", "a", "resolver", "los", "problemas",
    "del", "país", "En", "1858", "varios", "compatriotas", "dejaron", "Paraguay", "con",
    "el", "compromiso", "de", "que", "a", "su", "regreso", "desarrollarían", "e",
    "implementarían", "lo", "aprendido", "en", "beneficio", "del", "país", "así",
    "los", "Becarios", "de", "López", "serían", "los", "principales", "motores", "del",
    "proceso", "de", "modernización", "del", "país", "Los", "primeros", "becarios",
    "fueron", "a", "Gran", "Bretaña", "los", "mismos", "fueron", "seleccionados", "del",
    "Aula", "de", "Filosofía", "y", "asumieron", "el", "compromiso", "de", "ir", "a",
    "prepararse", "para", "la", "carrera", "de", "constructores", "entre", "ellos",
    "Juan", "Cristóstomo", "Centurión", "Gerónimo", "Pérez", "Cándido", "Bareiro",
    "Andrés", "Maíz", "y", "Gaspar", "López", "los", "jóvenes", "habían", "estudiado",
    "en", "Asunción", "y", "tenían", "una", "excelente", "formación", "jurídica",
    "Durante", "años", "Centurión", "presidió", "la", "República", "en", "el", "año",
    "1878", "y", "publicó", "cuatro", "volúmenes", "de", "Memorias", "de",
    "extraordinaria", "importancia", "en", "la", "historiografía", "paraguaya",
    "una", "novela", "y", "diversos", "artículos", "estudios", "y", "ensayos",
]

# Definición de los pasos esperados: índice de palabra después de la cual se
# debe insertar el signo y el signo correspondiente.  Se utiliza un
# diccionario para cada entrada para mayor claridad.
PUNCTUATION_STEPS: List[Dict[str, Any]] = [
    {"index": 7, "punctuation": ","},    # El Congreso ... marzo de 1841,
    {"index": 17, "punctuation": ","},   # ... noviembre de 1841,
    {"index": 23, "punctuation": "."},   # ... Academia Literaria.
    {"index": 43, "punctuation": ","},   # ... Oratoria Sagrada,
    {"index": 70, "punctuation": "."},   # ... Joaquín Palacios.
    {"index": 81, "punctuation": ","},   # ... del Paraguay,
    {"index": 126, "punctuation": ";"},  # ... el exterior; una vez
    {"index": 142, "punctuation": ";"},  # ... el empleo; se los enviaba
]


def _compute_current_progress(user) -> Dict[str, int]:
    """Calcula el número de respuestas correctas y el paso actual para un usuario.

    Busca en la base de datos los intentos ya realizados por el usuario.  El
    paso actual se determina por la cantidad de intentos almacenados; el
    siguiente signo a colocar corresponde a la entrada con ese índice en
    `PUNCTUATION_STEPS`.  También se calcula el número de respuestas correctas.

    Retorna un diccionario con claves `step` y `score`.
    """
    attempts = PunctuationAttempt.objects.filter(user=user).order_by('step_number')
    step = attempts.count()
    score = attempts.filter(is_correct=True).count()
    return {"step": step, "score": score}


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def punctuation_exercise(request: HttpRequest) -> HttpResponse:
    """Muestra la actividad interactiva de puntuación.

    Cada vez que el usuario entra en la vista, se eliminan los intentos
    anteriores para permitir que repita el ejercicio desde cero.  Luego se
    prepara el contexto con las palabras del texto, el número total de pasos y
    el progreso actual (si se utilizaran sesiones persistentes, aquí podría
    continuarse).  La plantilla generará los espacios clicables entre
    palabras y mostrará el contador de aciertos.
    """
    user = request.user
    # Reiniciar cualquier intento previo para comenzar de cero.
    PunctuationAttempt.objects.filter(user=user).delete()
    PunctuationResult.objects.filter(user=user).delete()

    progress = _compute_current_progress(user)

    context = {
        "words": TEXT_WORDS,
        "total_steps": len(PUNCTUATION_STEPS),
        "step": progress["step"],
        "score": progress["score"],
        "submit_url": reverse("punctuation_submit"),
        "explain_url": reverse("punctuation_explain"),
    }
    return render(request, "puntuación/final/exercise.html", context)


@require_POST
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def punctuation_submit(request: HttpRequest) -> JsonResponse:
    """Procesa un clic del estudiante entre dos palabras.

    El cuerpo de la petición debe incluir `index` (el índice seleccionado) y
    `step` (el paso en que se encuentra el estudiante).  La vista compara
    este índice con el índice correcto para el paso indicado en
    `PUNCTUATION_STEPS`.  Se registra un `PunctuationAttempt` y se
    devuelve un JSON con información sobre si la respuesta fue correcta,
    qué signo debía colocarse, cuál es el índice correcto, el número de
    aciertos acumulados y si el ejercicio ha finalizado.
    """
    user = request.user
    try:
        index = int(request.POST.get("index", "-1"))
        step = int(request.POST.get("step", "0"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Parámetros inválidos"}, status=400)

    # Verificar que el paso esté dentro de los límites
    total_steps = len(PUNCTUATION_STEPS)
    if step < 0 or step >= total_steps:
        return JsonResponse({"error": "Paso fuera de rango"}, status=400)

    correct_entry = PUNCTUATION_STEPS[step]
    correct_index = correct_entry["index"]
    expected_punct = correct_entry["punctuation"]
    is_correct = index == correct_index

    # Guardar el intento en la base de datos
    attempt = PunctuationAttempt.objects.create(
        user=user,
        step_number=step,
        selected_index=index,
        correct_index=correct_index,
        expected_punctuation=expected_punct,
        is_correct=is_correct,
    )

    # Calcular la puntuación acumulada y el siguiente paso
    progress = _compute_current_progress(user)
    next_step = progress["step"] + 1 if is_correct else progress["step"] + 1  # siempre avanzamos al siguiente

    # Mensajes de retroalimentación
    if is_correct:
        message = "¡Correcto!"
    else:
        message = f"Incorrecto, debía ir '{expected_punct}' después de la palabra seleccionada."

    response_data: Dict[str, Any] = {
        "is_correct": is_correct,
        "message": message,
        "correct_index": correct_index,
        "expected_punctuation": expected_punct,
        "attempt_id": attempt.id,
        "score": progress["score"] + (1 if is_correct else 0),
        "next_step": next_step,
        "total_steps": total_steps,
    }

    if next_step >= total_steps:
        # Se ha completado el ejercicio
        response_data["finished"] = True
        response_data["result_url"] = reverse("punctuation_result")
    else:
        response_data["finished"] = False
    return JsonResponse(response_data)


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def punctuation_explain(request: HttpRequest) -> JsonResponse:
    """Devuelve una explicación personalizada sobre un intento de puntuación.

    Se espera recibir el parámetro `attempt_id` en la cadena de consulta.  La
    explicación se genera utilizando la API de OpenAI cuando está disponible.
    Si la integración no se encuentra disponible, se proporcionan
    explicaciones predefinidas según el signo de puntuación que corresponda.
    Además de explicar por qué el signo es correcto o incorrecto, se
    recomienda consultar el capítulo de la OLE (Ortografía de la lengua
    española) relacionado con los signos ortográficos.
    """
    attempt_id = request.GET.get("attempt_id")
    if not attempt_id:
        return JsonResponse({"error": "Falta attempt_id"}, status=400)
    try:
        attempt = PunctuationAttempt.objects.get(pk=attempt_id, user=request.user)
    except PunctuationAttempt.DoesNotExist:
        return JsonResponse({"error": "Intento no encontrado"}, status=404)

    # Determinar la explicación genérica en caso de no tener acceso a OpenAI
    if attempt.expected_punctuation == ".":
        generic_explanation = (
            "El punto indica una pausa que da fin a un enunciado y siempre se escribe "
            "mayúscula la palabra siguiente"  # sin tilde
        )
    elif attempt.expected_punctuation == ",":
        generic_explanation = (
            "La coma marca una pausa breve dentro del enunciado. Se usa para separar "
            "miembros de una enumeración o para aislar incisos y vocativos"
        )
    elif attempt.expected_punctuation == ";":
        generic_explanation = (
            "El punto y coma se emplea para separar oraciones largas que ya contienen "
            "comas o para separar elementos complejos de una enumeración"
        )
    else:
        generic_explanation = "Este signo no está contemplado en las reglas de este ejercicio."

    explanation = None
    if OpenAI is not None:
        try:
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if api_key:
                openai.api_key = api_key  # type: ignore[assignment]
                # Construir el prompt para OpenAI
                correctness = "correcta" if attempt.is_correct else "incorrecta"
                selected = TEXT_WORDS[attempt.selected_index]
                expected_desc = {
                    ",": "una coma",
                    ".": "un punto",
                    ";": "un punto y coma",
                }[attempt.expected_punctuation]
                prompt = (
                    f"El estudiante seleccionó la posición después de la palabra '{selected}', pero la respuesta fue {correctness}. "
                    f"Explícale de manera breve y amigable por qué {('se debía colocar ' + expected_desc) if not attempt.is_correct else 'esa posición es la adecuada'} "
                    f"y menciona la regla principal de uso de {expected_desc}. Finaliza recomendando revisar el capítulo III sobre el uso de los signos ortográficos en la 'Ortografía de la lengua española' de la RAE."
                )
                completion = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.5,
                )
                explanation = completion.choices[0].message["content"].strip()  # type: ignore[index]
        except Exception:
            explanation = None

    if not explanation:
        explanation = (
            f"{generic_explanation}. Para más información, consulta el capítulo III "
            "de la 'Ortografía de la lengua española' de la Real Academia Española."
        )

    return JsonResponse({"explanation": explanation})


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def punctuation_result(request: HttpRequest) -> HttpResponse:
    """Muestra el resultado final del ejercicio de puntuación.

    Calcula el número total de aciertos del usuario, determina un porcentaje
    y genera una recomendación de lectura mediante OpenAI (si está
    disponible).  Guarda el resultado en la base de datos y muestra
    asimismo un recordatorio de las reglas básicas de puntuación.
    """
    user = request.user
    attempts = PunctuationAttempt.objects.filter(user=user).order_by('step_number')
    total_steps = len(PUNCTUATION_STEPS)
    correct_steps = sum(1 for a in attempts if a.is_correct)
    percentage = (correct_steps / total_steps) * 100 if total_steps else 0

    # Generar recomendación mediante OpenAI
    recommendation = None
    if OpenAI is not None:
        try:
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if api_key:
                openai.api_key = api_key  # type: ignore[assignment]
                prompt = (
                    f"Un estudiante obtuvo un {percentage:.0f}% de aciertos en un ejercicio de puntuación. "
                    "Recomienda de manera amigable qué capítulo de un libro de ortografía debería estudiar "
                    "para mejorar su dominio de las reglas de los puntos, comas y puntos y coma, y motívalo a seguir practicando."
                )
                completion = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                    model="gpt-5-mini",
                    messages=[{"role": "user", "content": prompt}],

                )
                recommendation = completion.choices[0].message["content"].strip()  # type: ignore[index]
        except Exception:
            recommendation = None
    if not recommendation:
        recommendation = (
            "Te sugerimos estudiar el capítulo III, 'El uso de los signos ortográficos', de la "
            "Ortografía de la lengua española de la RAE, que aborda con detalle el uso del punto, "
            "la coma y el punto y coma."
        )

    # Guardar el resultado en la base de datos
    PunctuationResult.objects.create(
        user=user,
        total_steps=total_steps,
        correct_steps=correct_steps,
        percentage=percentage,
        recommendation=recommendation,
    )

    # Mensaje principal según el desempeño
    if correct_steps == total_steps:
        headline = "¡Excelente! Completaste todos los signos correctamente."
    elif percentage >= 60:
        headline = f"¡Buen trabajo! Asertaste el {percentage:.0f}% de los signos."
    else:
        headline = f"¡A practicar! Tu porcentaje de aciertos fue del {percentage:.0f}%."

    # Reglas breves de recordatorio (basadas en la fuente citada)
    reminder = (
        "Recuerda que el punto indica el fin de un enunciado y siempre se escribe mayúscula la palabra siguiente; "
        "la coma señala una pausa breve y se usa para separar elementos de una enumeración y para aislar incisos; "
        "y el punto y coma marca una pausa superior a la de la coma e inferior a la del punto, separando oraciones largas "
        "o elementos complejos de una lista"
    )

    context = {
        "headline": headline,
        "score": correct_steps,
        "total_steps": total_steps,
        "percentage": f"{percentage:.0f}%",
        "recommendation": recommendation,
        "reminder": reminder,
    }
    return render(request, "puntuación/final/result.html", context)

###########################
#SELECCIÓN MÚLTIPLE
############################

"""
Vistas genéricas para ejercicios de opción múltiple.

Este módulo implementa seis ejercicios de selección múltiple: dos de
puntuación, dos de uso de mayúsculas y minúsculas y dos de reglas
ortográficas de las letras.  Cada ejercicio consta de tres preguntas
y una pantalla final de resultados.  El flujo es similar al del
ejercicio de acentuación: el estudiante responde una pregunta,
recibe retroalimentación inmediata, puede solicitar una explicación
mediante la API de OpenAI y continúa a la siguiente pregunta.  Al
terminar se almacena el puntaje y se muestra un mensaje con una
recomendación de estudio.

Las rutas para estos ejercicios se definen de forma dinámica a
través del parámetro ``exercise_slug`` (por ejemplo, 'puntuacion1',
'mayus2', etc.) y ``question_number`` (1, 2 o 3).  La vista de
resultado utiliza únicamente el ``exercise_slug``.  Para simplificar
la configuración, todas las preguntas usan la misma plantilla y
script JavaScript.
"""


import json
from typing import Dict, Any

from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST


from .models import MultipleChoiceAttempt, MultipleChoiceResult


###########################
#Todos los ejercicios de opción múltiple
# -----------------------------------------------------------------------------
# Definición de las preguntas para cada ejercicio
#
# Cada entrada contiene un diccionario con las claves:
#   "question": enunciado de la pregunta
#   "options": mapa de clave de opción (a, b, c, d) a texto de la opción
#   "correct": clave de la opción correcta
#   "feedback_correct": mensaje a mostrar cuando el estudiante acierta
#   "feedback_incorrect": mensaje a mostrar cuando el estudiante falla.  Se
#       permiten etiquetas HTML (por ejemplo, <strong>) para destacar la
#       respuesta correcta.  El script JavaScript interpreta este campo
#       como HTML seguro.

MC_QUESTIONS: Dict[str, Dict[int, Dict[str, Any]]] = {
    # Ejercicio 1 de puntuación
    "puntuacion1": {
        1: {
            "question": "Colocación correcta de comas con “sin embargo”:",
            "options": {
                "a": "Llegó tarde sin embargo aprobó.",
                "b": "Llegó tarde, sin embargo aprobó.",
                "c": "Llegó tarde sin embargo, aprobó.",
                "d": "Llegó tarde, sin embargo, aprobó.",
            },
            "correct": "d",
            "feedback_correct": "¡Bien hecho!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Llegó tarde, sin embargo, aprobó.</strong>",
        },
        2: {
            "question": "Punto y coma para separar elementos con comas internas:",
            "options": {
                "a": "Llevé frutas: manzanas, verdes; peras, maduras; y plátanos, pequeños.",
                "b": "Llevé frutas: manzanas, verdes, peras, maduras; y plátanos, pequeños.",
                "c": "Llevé frutas; manzanas, verdes; peras, maduras; y plátanos, pequeños.",
                "d": "Llevé frutas: manzanas verdes; peras maduras; y plátanos pequeños.",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Llevé frutas: manzanas, verdes; peras, maduras; y plátanos, pequeños.</strong>",
        },
        3: {
            "question": "Comillas recomendadas en español para cita breve:",
            "options": {
                "a": "“Mañana hay examen”.",
                "b": "«Mañana hay examen».",
                "c": "(Mañana hay examen).",
                "d": "“Mañana hay examen».",
            },
            "correct": "b",
            "feedback_correct": "¡Así se hace!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>«Mañana hay examen».</strong>",
        },
    },
    # Ejercicio 2 de puntuación
    "puntuacion2": {
        1: {
            "question": "Aposición explicativa (comas bien colocadas):",
            "options": {
                "a": "Mi hermana que vive en Villarrica, vendrá.",
                "b": "Mi hermana, que vive en Villarrica vendrá.",
                "c": "Mi hermana, que vive en Villarrica, vendrá.",
                "d": "Mi hermana que vive en Villarrica vendrá.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Mi hermana, que vive en Villarrica, vendrá.</strong>",
        },
        2: {
            "question": "¿Cuál de las siguientes oraciones utiliza correctamente la puntuación en una enumeración compleja?",
            "options": {
                "a": "Los países visitados fueron: España, con sus ciudades históricas; Francia, famosa por su gastronomía, e Italia, conocida por su arte.",
                "b": "Los países visitados fueron: España, con sus ciudades históricas; Francia, famosa por su gastronomía; e Italia, conocida por su arte.",
                "c": "Los países visitados fueron: España con sus ciudades históricas, Francia famosa por su gastronomía e Italia conocida por su arte.",
                "d": "Los países visitados fueron: España, con sus ciudades históricas, Francia, famosa por su gastronomía, e Italia, conocida por su arte.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>segunda oración</strong> es la correcta.",
        },
        3: {
            "question": "Elige la opción correctamente puntuada.",
            "options": {
                "a": "Quiero ir al cine pero, si empieza tarde me quedo en casa.",
                "b": "Quiero ir al cine pero si empieza tarde me quedo en casa.",
                "c": "Quiero ir al cine, pero si empieza tarde, me quedo en casa.",
                "d": "Quiero ir al cine; pero si empieza tarde me quedo en casa.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Quiero ir al cine, pero si empieza tarde, me quedo en casa.</strong>",
        },
    },
    # Ejercicio 1 de mayúsculas y minúsculas
    "mayus1": {
        1: {
            "question": "El uso correcto de la mayúscula es:",
            "options": {
                "a": "La Ley de Educación Superior tiene por objeto la formación personal, académica y profesional de los estudiantes.",
                "b": "La ley de Educación Superior tiene por objeto la formación personal, académica y profesional de los estudiantes.",
                "c": "La Ley de educación superior tiene por objeto la formación personal, académica y profesional de los estudiantes.",
                "d": "La Ley de Educación Superior tiene por objeto la formación Personal, Académica y Profesional de los estudiantes",
            },
            # Según el enunciado proporcionado por el usuario, la segunda oración es la correcta.
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>segunda oración</strong> es la correcta.",
        },
        2: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "El Lunes 3 de Abril vamos a viajar a asunción.",
                "b": "El lunes 3 de abril vamos a viajar a Asunción.",
                "c": "el lunes 3 de Abril vamos a viajar a Asunción.",
                "d": "El lunes 3 de Abril vamos a viajar a asunción.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>El lunes 3 de abril vamos a viajar a Asunción.</strong>",
        },
        3: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "Estudio Español y Literatura Paraguaya, pero nací en paraguay.",
                "b": "Estudio español y literatura paraguaya, pero nací en Paraguay.",
                "c": "Estudio español y Literatura paraguaya, pero nací en Paraguay.",
                "d": "Estudio Español y literatura paraguaya, pero nací en Paraguay.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Estudio español y literatura paraguaya, pero nací en Paraguay.</strong>",
        },
    },
    # Ejercicio 2 de mayúsculas y minúsculas
    "mayus2": {
        1: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "Mañana rindo en la universidad nacional de asunción; la Universidad cierra temprano.",
                "b": "Mañana rindo en la Universidad Nacional de Asunción; la Universidad cierra temprano.",
                "c": "Mañana rindo en la Universidad Nacional de Asunción; la universidad cierra temprano.",
                "d": "Mañana rindo en la Universidad nacional de Asunción; la universidad cierra temprano.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>tercera oración</strong> es la correcta.",
        },
        2: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "Aviso: Mañana no hay clases.",
                "b": "Aviso: mañana no hay clases.",
                "c": "Aviso: Mañana No Hay Clases.",
                "d": "Aviso: mañana No hay clases.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Aviso: mañana no hay clases.</strong>",
        },
        3: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "El Artículo 5 de la Constitución nacional establece derechos básicos.",
                "b": "El Artículo 5 de la Constitución Nacional establece Derechos Básicos.",
                "c": "El artículo 5 de la constitución nacional establece derechos básicos.",
                "d": "El artículo 5 de la Constitución Nacional establece derechos básicos.",
            },
            "correct": "d",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>El artículo 5 de la Constitución Nacional establece derechos básicos.</strong>",
        },
    },
    
    # Ejercicio Final de mayúsculas y minúsculas
    "mayus3": {
        1: {
            "question": "Elige la opción con mayúsculas correctas en cargo y nombre oficial:",
            "options": {
                "a": "El Presidente de la República del Paraguay, Santiago Peña, habló.",
                "b": "El presidente de la república del Paraguay, Santiago Peña, habló.",
                "c": "El presidente de la República del Paraguay, Santiago Peña, habló.",
                "d": "El Presidente de la República Del Paraguay, Santiago Peña, habló.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>tercera oración</strong> es la correcta.",
        },
        2: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "Se presentó un informe en la facultad de Arquitectura, Diseño y Arte de la Universidad Nacional de Asunción; posteriormente, el Decano se reunió con el departamento de Matemática.",
                "b": "Se presentó un informe en la Facultad de Arquitectura, Diseño y Arte de la Universidad Nacional de Asunción; posteriormente, el decano se reunió con el Departamento de Matemática.",
                "c": "Se presentó un informe en la Facultad de arquitectura, diseño y arte de la Universidad nacional de Asunción; posteriormente, el Decano se reunió con el Departamento De Matemática.",
                "d": "Se presentó un informe en la Facultad de Arquitectura, Diseño y Arte de la universidad nacional de asunción; posteriormente, el decano se reunió con el Departamento de matemática.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es la <strong>segunda oración</strong>",
        },
        3: {
            "question": "Elige la opción con uso correcto de mayúsculas",
            "options": {
                "a": "El Presidente presentó el Plan Nacional de Desarrollo 2030; la OMS alertó sobre la COVID-19 y el Estado adoptó medidas con el Ministerio De Hacienda y la Universidad nacional de Asunción.",
                "b": "El presidente presentó el Plan Nacional de Desarrollo 2030; la OMS alertó sobre la covid-19 y el Estado adoptó medidas en coordinación con el Ministerio de Hacienda y la Universidad Nacional de Asunción.",
                "c": "El Presidente presentó el plan nacional de desarrollo 2030; la Oms alertó sobre la covid-19 y el estado adoptó medidas en coordinación con el ministerio de Hacienda y la Universidad Nacional De Asunción.",
                "d": "El presidente presentó el Plan nacional de desarrollo 2030; la OMS alertó sobre la Covid-19 y el Estado adoptó medidas en coordinación con el Ministerio de hacienda y la universidad Nacional de Asunción.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es la <strong>segunda oración</strong>",
        },
    },
    
    # Ejercicio 1 de reglas de las letras
    "letras1": {
        1: {
            "question": "La oración con el uso de g/j correctamente escrita es:",
            "options": {
                "a": "Las personas que admiten y tratan de correjir sus fallos son las mejores.",
                "b": "Los ropages del pasado hoy nadie los usaría.",
                "c": "La remera, que se quedó afuera secando, se quedó hecha jirones tras el tornado.",
                "d": "La ajilidad de los gatos me sorprenden.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>La remera, que se quedó afuera secando, se quedó hecha jirones tras el tornado.</strong>",
        },
        2: {
            "question": "La oración de uso correcto de s/c/z",
            "options": {
                "a": "En tiempos pasados, se exigía a los siervos sumición total.",
                "b": "La decisión de mi compañero asombró a todos.",
                "c": "Todas sus dotes de persuazión chocaron con un muro de indiferencia.",
                "d": "Aprovechó la ocación de disfrutar de la naturaleza.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>La decisión de mi compañero asombró a todos.</strong>",
        },
        3: {
            "question": "La oración cuyo vocablo subrayado está correctamente empleado con b/v es:",
            "options": {
                "a": "Balido mis documentos a tiempo porque se acerca el concurso.",
                "b": "Es imposible no localizar tan basta propiedad.",
                "c": "Me está costando mucho havlandar esta carne.",
                "d": "Esta mañana, mi amigo me reveló lo que vivió en su juventud.",
            },
            "correct": "d",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Esta mañana, mi amigo me reveló lo que vivió en su juventud.</strong>",
        },
    },
    # Ejercicio 2 de reglas de las letras
    "letras2": {
        1: {
            "question": "La oración incorrecta con el uso de la h está en la opción",
            "options": {
                "a": "La suerte me ha sido adversa",
                "b": "Todos anhelamos en vivir en democracia",
                "c": "¿Consideras que aún hay solución para los daños ocasionados?",
                "d": "Las alajas fueron echos por antiguos y experimentados orfebres",
            },
            # La respuesta correcta es la opción d (oración incorrecta)
            "correct": "d",
            "feedback_correct": "¡Así es!",
            "feedback_incorrect": "¡Incorrecto!, la oración incorrecta es <strong>Las alajas fueron echos por antiguos y experimentados orfebres.</strong>",
        },
        2: {
            "question": "El auto guardé en el _________ ",
            "options": {
                "a": "garage",
                "b": "garaje",
                "c": "garache",
                "d": "garague",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>garaje</strong>.",
        },
        3: {
            "question": "¿Estás __________ de los daños que el ser humano causa al planeta?",
            "options": {
                "a": "cosciente",
                "b": "conciente",
                "c": "consciente",
                "d": "consiente",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>consciente</strong>.",
        },
    },
    # Ejercicio Final de reglas de las letras
    "letras3": {
        1: {
            "question": "Selecciona la opción bien escrita:",
            "options": {
                "a": "Si el comité exije que el laboratorio proteja los datos y el editor corrige los errores, entonces el archivo es legible.",
                "b": "Si el comité exige que el laboratorio proteja los datos y el editor corrige los errores, entonces el archivo es legible.",
                "c": "Si el comité exije que el laboratorio proteja los datos y el editor corrije los errores, entonces el archivo es lejible.",
                "d": "Si el comité exige que el laboratorio protega los datos y el editor corrige los errores, entonces el archivo es legible.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>segunda oración</strong> es la correcta.",
        },
        2: {
            "question": "Elige la redacción correcta:",
            "options": {
                "a": "Se requieren precisión y expresión en los informes; conozco el proceso y los peces del estanque; las luces del pasillo fallan a veces.",
                "b": "Se requieren precición y expresion en los informes; conosco el proceso y los peces del estanque; las luces del pasillo fallan a veses.",
                "c": "Se requieren precisión y expresión en los informes; conozco el proceso y los peces del estanque; las luses del pasillo fallan a veces.",
                "d": "Se requieren presición y espresión en los informes; conozco el procezo y los peces del estanque; las luces del pasillo fallan a veces.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>primera oración</strong>",
        },
        3: {
            "question": "Marca la opción correcta:",
            "options": {
                "a": "Si te has hecho cargo del proyecto, halla la causa; hasta ahí hay avances, y no eches en saco roto las alertas.",
                "b": "Si te has echo cargo del proyecto, haya la causa; asta ahí ay avances, y no heches en saco roto las alertas.",
                "c": "Si te has hecho cargo del proyecto, haya la causa; hasta ahí hay abances, y no eches en saco roto las alertas.",
                "d": "Si te haz hecho cargo del proyecto, halla la causa; asta ahí hay avances, y no heches en saco roto las alertas.",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la <strong>primera oración</strong>",
        },
    },
    # Evaluación final con 25 preguntas combinadas de acentuación, puntuación,
    # mayúsculas/minúsculas y reglas ortográficas.  Esta evaluación
    # utiliza el mismo mecanismo de opción múltiple pero incluye un
    # conjunto de preguntas más extenso.  Cada entrada se identifica
    # por un número consecutivo.  Se sugiere acceder a esta prueba
    # mediante la ruta ``/mc/evaluacionfinal/1/``.
    "evaluacionfinal": {
        # 1. Concepto de la ortografía
        1: {
            "question": "Concepto de la ortografía",
            "options": {
                "a": "Normativas de la escritura correcta",
                "b": "Reglas de comportamientos",
                "c": "Escritura errónea de las palabras",
                "d": "Dificultad de la comprensión escrita",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>Normativas de la escritura correcta</strong>.",
        },
        # 2. Definición de palabras llanas o graves
        2: {
            "question": "La siguiente definición: “Llevan tilde en la penúltima sílaba cuando no terminan en vocales y consonantes n y s” y corresponde según su acentuación a la palabra",
            "options": {
                "a": "Aguda",
                "b": "Llana o grave",
                "c": "Esdrújula",
                "d": "Sobreesdrújula",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>Llana o grave</strong>.",
        },
        # 3. Definición de palabras esdrújulas
        3: {
            "question": "Llevan tilde en la antepenúltima sílaba y a todas las palabras se les marca la tilde, esta regla equivale a la palabra",
            "options": {
                "a": "Aguda",
                "b": "Llana o grave",
                "c": "Esdrújula",
                "d": "Sobreesdrújula",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>Esdrújula</strong>.",
        },
        # 4. Definición de palabras agudas
        4: {
            "question": "La normativa: Las palabras llevan tilde en la última sílaba cuando terminan en vocales y consonantes n y s” y corresponde según su acentuación a la palabra",
            "options": {
                "a": "Aguda",
                "b": "Llana o grave",
                "c": "Esdrújula",
                "d": "Sobreesdrújula",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>Aguda</strong>.",
        },
        # 5. Definición de palabras sobreesdrújulas
        5: {
            "question": "Cuando siempre llevan la tilde en la anterior antepenúltima sílaba se está refiriendo a la palabra",
            "options": {
                "a": "Aguda",
                "b": "Llana o grave",
                "c": "Esdrújula",
                "d": "Sobreesdrújula",
            },
            "correct": "d",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>Sobreesdrújula</strong>.",
        },
        # 6. Interrogativos bien acentuados
        6: {
            "question": "Señala la oración con signos interrogativos bien acentuados:",
            "options": {
                "a": "Como te llamas? Donde vives?",
                "b": "¿Cómo te llamas? ¿Dónde vives?",
                "c": "¿Como te llamas? ¿Donde vives?",
                "d": "¿Cómo te llamas? ¿Donde vives?",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>¿Cómo te llamas? ¿Dónde vives?</strong>.",
        },
        # 7. Uso correcto de la mayúscula
        7: {
            "question": "El uso correcto de la mayúscula es:",
            "options": {
                "a": "La Ley de Educación Superior tiene por objeto la formación personal, académica y profesional de los estudiantes.",
                "b": "La ley de Educación Superior tiene por objeto la formación personal, académica y profesional de los estudiantes.",
                "c": "La Ley de educación superior tiene por objeto la formación personal, académica y profesional de los estudiantes.",
                "d": "La Ley de Educación Superior tiene por objeto la formación Personal, Académica y Profesional de los estudiantes",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>La ley de Educación Superior tiene por objeto la formación personal, académica y profesional de los estudiantes.</strong>",
        },
        # 8. Oración correctamente puntuada
        8: {
            "question": "La oración correctamente puntuada es:",
            "options": {
                "a": "Cristo dijo: “Quien esté libre de pecado que lance la primera piedra”.",
                "b": "Esfuerzo y constancia; Éstas son las armas para triunfar",
                "c": "Se llama borrego al cordero de pocos meses, que aún sigue, dócilmente, a su madre, la oveja.",
                "d": "Sonó la alarma lo pillaron in fraganti.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Se llama borrego al cordero de pocos meses, que aún sigue, dócilmente, a su madre, la oveja.</strong>",
        },
        # 9. Uso correcto de g/j
        9: {
            "question": "La oración con el uso de g/j correctamente escrita es:",
            "options": {
                "a": "Las personas que admiten y tratan de correjir sus fallos son las mejores.",
                "b": "Los ropages del pasado hoy nadie los usaría.",
                "c": "La remera, que se quedó afuera secando, se quedó hecha jirones tras el tornado.",
                "d": "La ajilidad de los gatos me sorprenden.",
            },
            "correct": "c",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>La remera, que se quedó afuera secando, se quedó hecha jirones tras el tornado.</strong>",
        },
        # 10. Uso correcto de s/c/z
        10: {
            "question": "La oración de uso correcto de s/c/z es:",
            "options": {
                "a": "En tiempos pasados, se exigía a los siervos sumición total",
                "b": "La decisión de mi compañero asombró a todos",
                "c": "Todas sus dotes de persuazión chocaron con un muro de indiferencia",
                "d": "Aprovechó la ocación de disfrutar de la naturaleza.",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>La decisión de mi compañero asombró a todos.</strong>",
        },
        # 11. Uso correcto de b/v
        11: {
            "question": "La oración cuyo vocablo subrayado está correctamente empleado con b/v es:",
            "options": {
                "a": "Balido mis documentos a tiempo porque se acerca el concurso.",
                "b": "Es imposible no localizar tan basta propiedad",
                "c": "Me está costando mucho havlandar esta carne",
                "d": "Esta mañana, mi amigo me reveló lo que vivió en su juventud.",
            },
            "correct": "d",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>Esta mañana, mi amigo me reveló lo que vivió en su juventud.</strong>",
        },
        # 12. Uso incorrecto de h
        12: {
            "question": "La oración incorrecta con el uso de la h está en la opción:",
            "options": {
                "a": "La suerte me ha sido adversa",
                "b": "Todos anhelamos en vivir en democracia",
                "c": "¿Consideras que aún hay solución para los daños ocasionados?",
                "d": "Las alajas fueron echos por antiguos y experimentados orfebres",
            },
            "correct": "d",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración incorrecta es <strong>Las alajas fueron echos por antiguos y experimentados orfebres.</strong>",
        },
        # 13. Uso correcto de “etc.” en lista
        13: {
            "question": "Uso correcto de “etc.” en lista:",
            "options": {
                "a": "Trae papel, lápiz, cuaderno, etc.",
                "b": "Trae papel, lápiz, cuaderno etc.",
                "c": "Trae papel, lápiz, cuaderno; etc.",
                "d": "Trae papel, lápiz, cuaderno: etc.",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>Trae papel, lápiz, cuaderno, etc.</strong>.",
        },
        # 14. Palabra esdrújula bien acentuada
        14: {
            "question": "¿Cuál es esdrújula y está bien acentuada?",
            "options": {
                "a": "telefono",
                "b": "teléfono",
                "c": "cafe",
                "d": "pared",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la respuesta correcta es <strong>teléfono</strong>.",
        },
        # 15. Oración incorrecta
        15: {
            "question": "La oración incorrecta es:",
            "options": {
                "a": "El león rugía tras las rejas de su jaula",
                "b": "La enbarcación crujía con el fuerte oleaje.",
                "c": "Asistió a la reunión acompañado de su cónyuge",
                "d": "No transigiré en mis decisiones",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración incorrecta es <strong>La enbarcación crujía con el fuerte oleaje.</strong>",
        },
        # 16. Completar con vello/bello
        16: {
            "question": "Completa: El ………… sale en los brazos y piernas.",
            "options": {
                "a": "vello",
                "b": "bello",
                "c": "valla",
                "d": "baya",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>vello</strong>.",
        },
        # 17. Completar con honda/onda
        17: {
            "question": "Completa: Esa alberca no es muy ………………..",
            "options": {
                "a": "onda",
                "b": "honda",
                "c": "hondo",
                "d": "honra",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>honda</strong>.",
        },
        # 18. Completar con asta/hasta
        18: {
            "question": "Completa: Llegaremos ……………………. tu casa.",
            "options": {
                "a": "asta",
                "b": "hasta",
                "c": "hacia",
                "d": "hazta",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>hasta</strong>.",
        },
        # 19. Completar con hierba/hierva
        19: {
            "question": "Completa: Jugaremos en la …………………………..",
            "options": {
                "a": "hierva",
                "b": "hierba",
                "c": "hierro",
                "d": "yerba",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>hierba</strong>.",
        },
        # 20. Completar con ojeada/hojeada
        20: {
            "question": "Completa: De una …………., el profesor pudo saber cuántos alumnos había.",
            "options": {
                "a": "ojeada",
                "b": "hojeada",
                "c": "ojea",
                "d": "hojea",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>ojeada</strong>.",
        },
        # 21. Completar con tubo/tuvo
        21: {
            "question": "Completa la oración con las palabras adecuadas (tubo/tuvo): El …… se rompió, por eso se ………… que comprar otro.",
            "options": {
                "a": "El tubo se rompió, por eso se tuvo que comprar otro.",
                "b": "El tuvo se rompió, por eso se tubo que comprar otro.",
                "c": "El tubo se rompió, por eso se tubo que comprar otro.",
                "d": "El tuvo se rompió, por eso se tuvo que comprar otro.",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la oración correcta es <strong>El tubo se rompió, por eso se tuvo que comprar otro.</strong>",
        },
        # 22. Completar con ay/hay
        22: {
            "question": "Completa: ¡____! ¡Cómo pudiste revelar nuestro más grande secreto!",
            "options": {
                "a": "ay",
                "b": "hay",
                "c": "ahí",
                "d": "ahy",
            },
            "correct": "a",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>ay</strong>.",
        },
        # 23. Completar con cayó/calló
        23: {
            "question": "Completa: El vaso ……………….. al suelo.",
            "options": {
                "a": "calló",
                "b": "cayó",
                "c": "callo",
                "d": "cayo",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>cayó</strong>.",
        },
        # 24. Completar con término/terminó
        24: {
            "question": "Completa: El ……………… del texto fue difícil de pronunciar.",
            "options": {
                "a": "termino",
                "b": "término",
                "c": "terminó",
                "d": "ternero",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>término</strong>.",
        },
        # 25. Completar con sé/se
        25: {
            "question": "Completa: Yo …………… las reglas ortográficas.",
            "options": {
                "a": "se",
                "b": "sé",
                "c": "sè",
                "d": "séé",
            },
            "correct": "b",
            "feedback_correct": "¡Correcto!",
            "feedback_incorrect": "¡Incorrecto!, la palabra correcta es <strong>sé</strong>.",
        },
    },
}


# Títulos descriptivos para cada ejercicio.  Se muestran en la cabecera de
# las páginas de pregunta y en la página de resultados.
EXERCISE_TITLES: Dict[str, str] = {
    "puntuacion1": "Ejercicio 1 de puntuación",
    "puntuacion2": "Ejercicio 2 de puntuación",
    "mayus1": "Ejercicio 1 de mayúsculas y minúsculas",
    "mayus2": "Ejercicio 2 de mayúsculas y minúsculas",
    "mayus3": "Ejercicio Final de mayúsculas y minúsculas",
    "letras1": "Ejercicio 1 de reglas ortográficas",
    "letras2": "Ejercicio 2 de reglas ortográficas",
    "letras3": "Ejercicio Final de reglas ortográficas",
    # Evaluación final abarca todos los temas
    "evaluacionfinal": "Evaluación final",
}

# Recomendaciones por ejercicio para mostrar al final en caso de no obtener
# el 100 %.  Se pueden personalizar con referencias a libros o capítulos.
EXERCISE_RECOMMENDATIONS: Dict[str, str] = {
    "puntuacion1": (
        "Recomendación: repasa el capítulo dedicado a los signos de puntuación en un buen libro de ortografía, "
        "por ejemplo en la 'Ortografía de la lengua española' de la Real Academia Española."
    ),
    "puntuacion2": (
        "Recomendación: estudia con atención las reglas de uso de comas, puntos y puntos y coma. "
        "El capítulo sobre puntuación de la 'Ortografía de la lengua española' te será de gran ayuda."
    ),
    "mayus1": (
        "Recomendación: revisa el capítulo sobre uso de mayúsculas y minúsculas en tu libro de ortografía. "
        "Recuerda que solo los nombres propios y títulos oficiales llevan mayúscula inicial."
    ),
    "mayus2": (
        "Recomendación: consulta la sección dedicada al uso de mayúsculas en nombres propios y entidades. "
        "También ten presente que, tras dos puntos, la palabra puede ir en minúscula si no inicia un enunciado independiente."
    ),
    "mayus3": (
        "Recomendación: consulta la sección dedicada al uso de mayúsculas en nombres propios y entidades. "
        "También ten presente que, tras dos puntos, la palabra puede ir en minúscula si no inicia un enunciado independiente."
    ),
    "letras1": (
        "Recomendación: repasa las reglas ortográficas de g, j, s, c, z, b y v. "
        "Un buen recurso es el capítulo sobre reglas de las letras en la 'Ortografía de la lengua española'."
    ),
    "letras2": (
        "Recomendación: profundiza en las normas sobre el uso de la h, así como la escritura de algunas palabras "
        "de origen extranjero (como garaje) y concéntrate en las reglas de uso de consonantes en términos derivados."
    ),
    "letras3": (
        "Recomendación: repasa las reglas ortográficas de g, j, s, c, z, b y v. "
        "Un buen recurso es el capítulo sobre reglas de las letras en la 'Ortografía de la lengua española'."
    ),
    # Recomendación general para la evaluación final
    "evaluacionfinal": (
        "Recomendación: repasa todos los contenidos de ortografía estudiados durante el curso, incluyendo acentuación, "
        "puntuación, uso de mayúsculas y minúsculas, y reglas ortográficas de las letras. Practica con ejercicios "
        "adicionales y consulta tus apuntes para reforzar las áreas en las que hayas tenido dudas."
    ),
}


def _get_mc_question_context(slug: str, number: int) -> Dict[str, Any]:
    """Construye el contexto para una pregunta de un ejercicio de opción múltiple.

    Parámetros:
        slug: Identificador del ejercicio (puntuacion1, mayus2, etc.).
        number: Número de la pregunta (1, 2 o 3).

    Devuelve:
        Un diccionario con los datos para rellenar la plantilla de pregunta.
    """
    q_data = MC_QUESTIONS.get(slug, {}).get(number)
    if not q_data:
        raise ValueError(f"Pregunta no encontrada: {slug} #{number}")
    context = {
        "exercise_slug": slug,
        "exercise_title": EXERCISE_TITLES.get(slug, slug),
        "num": number,
        "question": q_data["question"],
        "options": q_data["options"],
        "submit_url": reverse("mc_submit", args=(slug, number)),
        "explain_endpoint": reverse("mc_explain"),
    }
    return context


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def mc_question_view(request: HttpRequest, slug: str, qnum: int) -> HttpResponse:
    """Muestra una de las preguntas de un ejercicio de opción múltiple.

    Si se accede a la primera pregunta de un ejercicio, se reinician
    previamente los intentos y resultados almacenados para ese usuario y
    ejercicio, de modo que pueda comenzar de nuevo sin interferencia de
    respuestas anteriores.
    """
    # Validar que el ejercicio y la pregunta existan
    if slug not in MC_QUESTIONS or qnum not in MC_QUESTIONS[slug]:
        return HttpResponse("Ejercicio o pregunta no encontrada", status=404)
    # Reiniciar intentos y resultados al comenzar el ejercicio
    if qnum == 1:
        MultipleChoiceAttempt.objects.filter(user=request.user, exercise_slug=slug).delete()
        MultipleChoiceResult.objects.filter(user=request.user, exercise_slug=slug).delete()
    context = _get_mc_question_context(slug, qnum)
    return render(request, "mc/question.html", context)


@require_POST
@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def mc_submit_view(request: HttpRequest, slug: str, qnum: int) -> JsonResponse:
    """Procesa la respuesta de una pregunta de un ejercicio de opción múltiple.

    Recibe la opción seleccionada y registra el intento.  Devuelve un
    JSON con información sobre si la respuesta fue correcta, un mensaje
    de retroalimentación, la URL de la siguiente vista y el ID del
    intento guardado.
    """
    # Validar que el ejercicio y la pregunta existan
    if slug not in MC_QUESTIONS or qnum not in MC_QUESTIONS[slug]:
        return JsonResponse({"error": "Ejercicio o pregunta no encontrada."}, status=404)
    selected_option = request.POST.get("option")
    if not selected_option:
        return JsonResponse({"error": "No se recibió ninguna opción."}, status=400)
    q_data = MC_QUESTIONS[slug][qnum]
    correct_option = q_data["correct"]
    is_correct = (selected_option == correct_option)
    # Guardar el intento
    attempt = MultipleChoiceAttempt.objects.create(
        user=request.user,
        exercise_slug=slug,
        question_number=qnum,
        selected_option=selected_option,
        correct_option=correct_option,
        is_correct=is_correct,
    )
    # Calcular la URL siguiente
    if qnum < 3:
        next_url = reverse("mc_question", args=(slug, qnum + 1))
    else:
        next_url = reverse("mc_result", args=(slug,))
    # Seleccionar el mensaje apropiado
    message = q_data["feedback_correct"] if is_correct else q_data["feedback_incorrect"]
    return JsonResponse({
        "correct": is_correct,
        "message": message,
        "next_url": next_url,
        "attempt_id": attempt.id,
    })


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def mc_explain(request: HttpRequest) -> JsonResponse:
    """Devuelve una explicación para un intento de un ejercicio de opción múltiple.

    Utiliza la API de OpenAI para generar una explicación personalizada.
    Si no se dispone de la API, se devuelve una explicación genérica.
    """
    attempt_id = request.GET.get("attempt_id")
    if not attempt_id:
        return JsonResponse({"error": "Falta attempt_id"}, status=400)
    try:
        attempt = MultipleChoiceAttempt.objects.get(pk=attempt_id, user=request.user)
    except MultipleChoiceAttempt.DoesNotExist:
        return JsonResponse({"error": "Intento no encontrado"}, status=404)
    # Obtener datos de la pregunta y las opciones
    slug = attempt.exercise_slug
    qnum = attempt.question_number
    q_data = MC_QUESTIONS.get(slug, {}).get(qnum)
    if not q_data:
        return JsonResponse({"error": "Pregunta no encontrada"}, status=404)
    selected_text = q_data["options"].get(attempt.selected_option, "")
    correct_text = q_data["options"].get(q_data["correct"], "")

    # Construir prompt genérico para OpenAI
    prompt = (
        f"Explica al estudiante por qué la opción '{selected_text}' "
        f"{'es correcta' if attempt.is_correct else 'es incorrecta'} en la pregunta: "
        f"'{q_data['question']}'. Indica cuál es la forma correcta ('{correct_text}') "
        f"y menciona la regla ortográfica relevante. Usa un tono amigable y motivador "
        f"y redacta en español."
    )
    explanation = None
    if OpenAI is not None:
        try:
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if api_key:
                openai.api_key = api_key  # type: ignore[assignment]
                completion = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                    model="gpt-5-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                explanation = completion.choices[0].message["content"].strip()  # type: ignore[index]
        except Exception:
            explanation = None
    if not explanation:
        # Explicación genérica en caso de no disponer de API
        if attempt.is_correct:
            explanation = (
                f"Tu respuesta es correcta. La opción '{selected_text}' se ajusta a la regla "
                f"indicada para esta pregunta. Sigue practicando para reforzar tus conocimientos."
            )
        else:
            explanation = (
                f"La opción que seleccionaste no cumple con la regla correspondiente. "
                f"La forma correcta es '{correct_text}'. Revisa las normas ortográficas y "
                f"trata de identificar por qué esta opción es la adecuada."
            )
    return JsonResponse({"explanation": explanation})


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def mc_result_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Muestra la pantalla de resultados de un ejercicio de opción múltiple.

    Calcula el número de aciertos y el porcentaje obtenido por el usuario
    en el ejercicio indicado.  Se genera y guarda un objeto
    ``MultipleChoiceResult``.  Se determina un titular y una
    recomendación según el desempeño.
    """
    # Validar ejercicio
    if slug not in MC_QUESTIONS:
        return HttpResponse("Ejercicio no encontrado", status=404)
    user = request.user
    attempts = MultipleChoiceAttempt.objects.filter(user=user, exercise_slug=slug)
    total_questions = 3
    correct_answers = sum(1 for a in attempts if a.is_correct)
    percentage = (correct_answers / total_questions) * 100 if total_questions else 0
    # Guardar resultado
    MultipleChoiceResult.objects.create(
        user=user,
        exercise_slug=slug,
        total_questions=total_questions,
        correct_answers=correct_answers,
        percentage=percentage,
        recommendation="",  # se asignará más abajo si corresponde
    )
    # Determinar el mensaje principal y la recomendación
    if correct_answers == total_questions:
        headline = "¡Completaste todos los ejercicios sin errores, sigue así!"
        recommendation = None
    elif percentage >= 60:
        headline = f"¡Felicidades acertaste el {percentage:.0f}%!"
        recommendation = EXERCISE_RECOMMENDATIONS.get(slug)
    else:
        headline = f"¡Faltaría reforzar un poco más, acertaste solo el {percentage:.0f}%!"
        recommendation = EXERCISE_RECOMMENDATIONS.get(slug)
    context = {
        "exercise_title": EXERCISE_TITLES.get(slug, slug),
        "headline": headline,
        "percentage": f"{percentage:.0f}%",
        "recommendation": recommendation,
    }
    return render(request, "mc/result.html", context)
#############
#Instrucciones
#############
# Mapeo de identificadores de unidad a archivos PDF en la carpeta static/pdfs.
# Definimos un slug corto por unidad para que las URLs sean más intuitivas.
# Cada entrada vincula el slug con el PDF correspondiente dentro de static/pdfs.
UNIT_PDFS = {
    "acento": "pdfs/acento_instr.pdf",
    "puntuacion": "pdfs/puntuacion_instr.pdf",
    "mayuscula": "pdfs/mayus_instr.pdf",
    "letras": "pdfs/letras_instr.pdf",
}

# Títulos descriptivos para cada unidad
UNIT_TITLES = {
    "acento": "Unidad I: Acentuación",
    "puntuacion": "Unidad II: Puntuación",
    "mayuscula": "Unidad III: Mayúsculas y Minúsculas",
    "letras": "Unidad IV: Reglas de las Letras",
}


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def instruccion_view(request: HttpRequest, unit_slug: str) -> HttpResponse:
    """Muestra la página de instrucción para la unidad especificada.

    Args:
        request: Petición HTTP recibida.
        unit_slug: Identificador de la unidad (p. ej. 'acentuacion').

    Devuelve:
        Una respuesta HTTP con la plantilla renderizada.  Si el slug
        no corresponde a una unidad conocida, se lanza un ``Http404``.
    """
    if unit_slug not in UNIT_PDFS:
        raise Http404("Unidad no encontrada")
    pdf_relative_path = UNIT_PDFS[unit_slug]
    # Construir la URL estática al PDF utilizando el helper de plantillas
    # La plantilla hará uso de la etiqueta 'static' para concatenar esta ruta.
    context = {
        "unit_slug": unit_slug,
        "unit_title": UNIT_TITLES.get(unit_slug, unit_slug),
        "pdf_path": pdf_relative_path,
    }
    return render(request, "instruccion/unidad.html", context)

###############################
# ----------------------------------------------------------------------------
# Definición de las preguntas de la encuesta
#
# Cada entrada del diccionario SURVEY_QUESTIONS representa una
# pregunta de la encuesta.  Las claves son números consecutivos
# empezando en 1.  Cada pregunta contiene el enunciado y un mapa de
# opciones (a, b, c, etc.) a sus textos.  No se incluye un campo
# "correct" porque no existen respuestas correctas o incorrectas.

SURVEY_QUESTIONS: Dict[int, Dict[str, Any]] = {
    1: {
        "question": "¿Qué edad tiene?",
        "options": {
            "a": "Menos de 15 años",
            "b": "16 años",
            "c": "17 años",
            "d": "18 años",
            "e": "Más de 18 años",
        },
    },
    2: {
        "question": "¿Cuál es su sexo?",
        "options": {
            "a": "Femenino",
            "b": "Masculino",
        },
    },
    3: {
        "question": "¿Qué nivel de formación académica posee?",
        "options": {
            "a": "Educación Escolar Básica",
            "b": "Educación Media y Técnica",
            "c": "Educación Universitaria",
        },
    },
    # Preguntas sobre la disponibilidad de dispositivos en la institución
    4: {
        "question": "¿Cuenta el Colegio Nacional Santa Lucía con computadora para usar en clases?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    5: {
        "question": "¿Cuenta el Colegio Nacional Santa Lucía con notebook para usar en clases?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    6: {
        "question": "¿Cuenta el Colegio Nacional Santa Lucía con teléfono celular para usar en clases?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    7: {
        "question": "¿Cuenta el Colegio Nacional Santa Lucía con tablet para usar en clases?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    8: {
        "question": "¿Tiene conocimiento de alguna herramienta tecnológica?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    # Preguntas sobre la posesión de dispositivos personales
    9: {
        "question": "¿Posee computadora de uso particular?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    10: {
        "question": "¿Posee notebook de uso particular?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    11: {
        "question": "¿Posee teléfono celular de uso particular?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    12: {
        "question": "¿Posee tablet de uso particular?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    13: {
        "question": "¿Qué mejoras tecnológicas quisiera que se realicen en su institución educativa para optimizar el rendimiento académico de la ortografía de la Lengua Castellana?",
        "options": {
            "a": "Sí a la aplicación de algún software didáctico que apoye a los estudiantes en el aprendizaje de la asignatura.",
            "b": "La no aplicación de algún software didáctico a los estudiantes durante el proceso de aprendizaje de la asignatura.",
        },
    },
    14: {
        "question": "Algunas personas opinan que los efectos negativos de la Informática han sido mayores que su contribución al mejoramiento del aprendizaje de los educandos. ¿Está de acuerdo con esta afirmación?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    15: {
        "question": "¿Cree que es prioridad promover la integración de la Informática en el Sistema Educativo Paraguayo?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    16: {
        "question": "Algunos docentes argumentan que el uso de las tecnologías como recurso didáctico no ayudaría a mejorar significativamente el aprendizaje y desempeño de los alumnos. ¿Está de acuerdo con esta percepción?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    17: {
        "question": "¿Considera que el uso didáctico de un software contribuye de manera positiva al proceso de enseñanza de su aprendizaje?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    18: {
        "question": "¿Ha utilizado algún software didáctico durante su vida académica?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    19: {
        "question": "¿Ha escuchado hablar del Software Recomendador Inteligente de Contenidos?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    20: {
        "question": "¿Tiene conocimiento de la utilidad de la aplicación del Software Recomendador Inteligente de Contenidos como guías de aprendizajes personalizadas de la ortografía de la lengua castellana?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    21: {
        "question": "¿Le gustaría que, para el desarrollo de la clase de Lengua Castellana y Literatura, específicamente de ortografía, sea utilizado el Software Recomendador Inteligente de Contenidos?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    22: {
        "question": "¿Considera que el uso del Software Recomendador Inteligente de Contenidos puede facilitar y mejorar el aprendizaje de la ortografía?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
    23: {
        "question": "¿Cree que la capacitación del docente en el uso didáctico de las tecnologías puede ejercer un impacto importante en los resultados académicos de los educandos?",
        "options": {
            "a": "Sí",
            "b": "No",
        },
    },
}


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def survey_question_view(request: HttpRequest, qnum: int) -> HttpResponse:
    """Muestra una pregunta de la encuesta.

    Si el número de pregunta excede el total de preguntas definidas, se
    redirige automáticamente a la vista de resultados de la encuesta.
    """
    total_questions = len(SURVEY_QUESTIONS)
    try:
        qnum_int = int(qnum)
    except (TypeError, ValueError):
        qnum_int = 1
    if qnum_int < 1:
        qnum_int = 1
    if qnum_int > total_questions:
        return redirect('survey_result')
    question_data = SURVEY_QUESTIONS[qnum_int]
    submit_url = reverse('survey_submit', kwargs={"qnum": qnum_int})
    return render(
        request,
        'encuesta/question.html',
        {
            'question_number': qnum_int,
            'total_questions': total_questions,
            'question': question_data['question'],
            'options': question_data['options'],
            'submit_url': submit_url,
        },
    )


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def survey_submit_view(request: HttpRequest, qnum: int) -> JsonResponse:
    """Procesa la respuesta a una pregunta de la encuesta.

    Se almacena la opción seleccionada por el usuario y se devuelve
    la URL de la siguiente pregunta o de la pantalla de resultados si
    todas las preguntas han sido respondidas.
    """
    try:
        qnum_int = int(qnum)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Número de pregunta inválido.'}, status=400)
    total_questions = len(SURVEY_QUESTIONS)
    # Obtener la opción seleccionada
    selected_option = request.POST.get('option')
    if not selected_option:
        return JsonResponse({'error': 'Debe seleccionar una opción.'}, status=400)
    # Guardar la respuesta
    SurveyAttempt.objects.create(
        user=request.user,
        question_number=qnum_int,
        selected_option=selected_option,
        survey_slug='encuesta',
    )
    # Calcular la siguiente URL
    if qnum_int >= total_questions:
        # Registrar que el usuario completó la encuesta
        # Evitar duplicados: solo crear un SurveyResult si no existe
        SurveyResult.objects.get_or_create(
            user=request.user,
            survey_slug='encuesta',
            defaults={'total_questions': total_questions},
        )
        next_url = reverse('survey_result')
    else:
        next_url = reverse('survey_question', kwargs={'qnum': qnum_int + 1})
    return JsonResponse({'message': '¡Respuesta guardada!', 'next_url': next_url})


@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")
def survey_result_view(request: HttpRequest) -> HttpResponse:
    """Muestra la pantalla final tras completar la encuesta."""
    return render(request, 'encuesta/result.html')