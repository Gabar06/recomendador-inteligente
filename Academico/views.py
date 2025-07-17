from django.shortcuts import render, redirect, get_object_or_404
from .models import Administrador,Docentes,Alumnos,Asignatura,Asistencia,Categorias,Cuota,Nota,Soporte,Sucursal
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
from .utils import analizar_respuestas
import markdown
from django.db.models import Q



# Instancia del cliente OpenAI con tu API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)
ALLOWED_EXTENSIONS = ['pdf', 'epub']

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

#Docentes
def docentes(request):
    DocentesListados = Docentes.objects.all()
    return render(request, "Docentes.html", { "docentes":DocentesListados})
def docentes_nuevo(request):
    DocentesListados = Docentes.objects.all()
    return render(request, "Docentes_Nuevo.html", {"docentes": DocentesListados})
def docentes_registrar(request):
    nombre = request.POST['txtNombre']
    login = request.POST['txtLogin']
    clave = request.POST['txtClave']

    docentes = Docentes.objects.create(
        nombre=nombre,login=login,clave=clave )
    return redirect('/Doc')

def docentes_edicion(request, id):
    docentes = Docentes.objects.get(id=id)
    return render(request, "Docentes_Editar.html", {"docentes": docentes})

def docentes_editar(request,id):
    nombre = request.POST['txtNombre']
    login = request.POST['txtLogin']
    clave = request.POST['txtClave']

    docentes = Docentes.objects.get(id=id)
    docentes.nombre = nombre
    docentes.login = login
    docentes.clave = clave
    docentes.save()
    return redirect('/Doc')

def docentes_eliminacion(request, id):
    docentes = Docentes.objects.get(id=id)
    return render(request, "Docentes_Eliminar.html", {"docentes": docentes})

def docentes_eliminar(request,id):
    docentes = Docentes.objects.get(id=id)
    docentes.delete()
    return redirect('/Doc')

def docentes_buscar(request):
    nombre = request.POST['txtNombre']
    docentes = Docentes.objects.filter(nombre=nombre)
    return render(request, "Docentes.html", {"docentes": docentes})

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

#Cuota
def cuota(request):
    CuotaListados = Cuota.objects.all()
    return render(request, "Cuota.html", { "cuota":CuotaListados})

def cuota_nuevo(request):
    CuotaListados = Cuota.objects.all()
    return render(request, "Cuota_Nuevo.html", {"cuota": CuotaListados})
def cuota_registrar(request):
    mes = request.POST['txtMes']
    monto = request.POST['numMonto']

    cuota = Cuota.objects.create(
        mes=mes, monto=monto)
    return redirect('/Cuo')

def cuota_edicion(request, id):
    cuota = Cuota.objects.get(id=id)
    return render(request, "Cuota_Editar.html", {"cuota": cuota})
def cuota_editar(request,id):
    mes = request.POST['txtMes']
    monto = request.POST['numMonto']

    cuota = Cuota.objects.get(id=id)
    cuota.mes = mes
    cuota.monto = monto
    cuota.save()
    return redirect('/Cuo')

def cuota_eliminacion(request, id):
    cuota = Cuota.objects.get(id=id)
    return render(request, "Cuota_Eliminar.html", {"cuota": cuota})

def cuota_eliminar(request,id):
    cuota = Cuota.objects.get(id=id)
    cuota.delete()
    return redirect('/Cuo')
def cuota_buscar(request):
    mes = request.POST['txtMes']
    cuota = Cuota.objects.filter(mes=mes)
    return render(request, "Cuota.html", {"cuota": cuota})

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

#Sucursal
def sucursal(request):
    SucursalListados = Sucursal.objects.all()
    return render(request, "Sucursal.html", { "sucursal":SucursalListados})

def sucursal_nuevo(request):
    SucursalListados = Sucursal.objects.all()
    return render(request, "Sucursal_Nuevo.html", {"sucursal": SucursalListados})
def sucursal_registrar(request):
    direccion = request.POST['txtDireccion']
    nr_sucursal = request.POST['numNr_Sucursal']

    sucursal = Sucursal.objects.create(
        direccion=direccion, nr_sucursal=nr_sucursal)
    return redirect('/Suc')

def sucursal_edicion(request, id):
    sucursal = Sucursal.objects.get(id=id)
    return render(request, "Sucursal_Editar.html", {"sucursal": sucursal})
def sucursal_editar(request,id):
    direccion = request.POST['txtDireccion']
    nr_sucursal = request.POST['numNr_Sucursal']

    sucursal = Sucursal.objects.get(id=id)
    sucursal.direccion = direccion
    sucursal.nr_sucursal = nr_sucursal
    sucursal.save()
    return redirect('/Suc')

def sucursal_eliminacion(request, id):
    sucursal = Sucursal.objects.get(id=id)
    return render(request, "Sucursal_Eliminar.html", {"sucursal": sucursal})

def sucursal_eliminar(request,id):
    sucursal = Sucursal.objects.get(id=id)
    sucursal.delete()
    return redirect('/Suc')

def sucursal_buscar(request):
    direccion = request.POST['txtDireccion']
    sucursal = Sucursal.objects.filter(direccion=direccion)
    return render(request, "Sucursal.html", {"sucursal": sucursal})

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

@csrf_exempt
def guia_ortografia(request):
    if request.method == 'POST':
        data = request.POST.get('respuestas_json')
        resultado_md  = analizar_respuestas(data)
        resultado_html = markdown.markdown(resultado_md, extensions=['fenced_code', 'tables'])
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
    
def menu(request):
    return render(request, "menu/menu.html")

def guia_aprendizaje(request):
    return render(request, "menu/guia_aprendizaje.html")

def acento_final(request):
    return render(request, "acento/final.html")


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