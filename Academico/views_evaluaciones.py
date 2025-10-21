"""
Vistas relacionadas con la sección de evaluaciones y reportes.

Este módulo define una vista que muestra un resumen de los resultados
obtenidos por el educando en las distintas unidades (Acentuación,
Puntuación, Mayúsculas y Minúsculas, y Reglas de las Letras). Para cada
unidad se consulta la base de datos en busca de los resultados
almacenados en los modelos correspondientes y se calcula un porcentaje
promedio.  Además se determina un nivel de dominio de acuerdo con ese
porcentaje (Insuficiente, Suficiente o Excelente). La página ofrece
también un botón que permite generar un reporte en formato PDF desde
el navegador mediante la librería jsPDF.

Nota: Esta vista requiere que el usuario esté autenticado y tenga el
rol de estudiante.  Las funciones de clasificación de dominio y
cálculo de promedios están encapsuladas para facilitar su mantenimiento.
"""

from __future__ import annotations

from statistics import mean
from typing import Optional, Dict, Tuple

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .decorators import role_login_required
from .models import (
    Usuario,
    ExerciseAttempt,
    ResultSummary,
    PunctuationResult,
    MultipleChoiceResult,
    CalendarActivity,
    Estudiante,
)

########
from django.http import JsonResponse, HttpRequest, HttpResponse

import io

# Condicionalmente importamos reportlab. Si está disponible, lo utilizaremos

# Condicionalmente importamos reportlab. Si está disponible, lo utilizaremos
try:
    from reportlab.pdfgen import canvas as rl_canvas  # type: ignore[import]
    from reportlab.lib.pagesizes import A4  # type: ignore[import]
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer  # type: ignore[import]
    from reportlab.lib import colors  # type: ignore[import]
    from reportlab.lib.styles import getSampleStyleSheet  # type: ignore[import]
    _HAS_REPORTLAB = True
except Exception:
    # Si reportlab no está instalado caemos en el modo de respaldo con Matplotlib
     # Si reportlab no está instalado caemos en el modo de respaldo con Matplotlib
    _HAS_REPORTLAB = False
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages


#########

# views_evaluaciones.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods

# Ya existen: _average_percentage y _classify_domain
# Vamos a usarlas también para calcular dominios por alumno.


#########

# Normaliza tipos antes de promediar
def _average_percentage(values) -> Optional[float]:
    nums = [float(v) for v in values if v is not None]
    return mean(nums) if nums else None



def _classify_domain(percentage: Optional[float]) -> str:
    """Clasifica el dominio a partir de un porcentaje.

    La clasificación utilizada es la siguiente:

    * ``None``: devuelve ``"N/A"`` (no aplica).
    * <60%: ``"Insuficiente"``
    * 60–79%: ``"Suficiente"``
    * ≥80%: ``"Excelente"``

    Args:
        percentage: Porcentaje obtenido por el estudiante.

    Returns:
        Cadena con la clasificación.
    """
    if percentage is None:
        return "N/A"
    if percentage < 40:
        return "Insuficiente"
    if percentage < 60:
        return "Básico"
    if percentage < 80:
        return "Bueno"
    if percentage < 90:
        return "Muy Bueno"
    return "Excelente"



@role_login_required(Usuario.ESTUDIANTE, login_url_name="login_estudiante")  
def evaluaciones_view(request):
    """Muestra el reporte de evaluaciones para el estudiante actual.

    Esta vista consulta las tablas de resultados de los ejercicios de
    acentuación, puntuación, mayúsculas y reglas de las letras para
    calcular el porcentaje logrado en cada unidad.  Luego se
    construye un contexto con las calificaciones y clasificaciones
    correspondientes y se renderiza la plantilla ``evaluaciones.html``.

    Args:
        request: objeto ``HttpRequest`` de Django.

    Returns:
        ``HttpResponse`` con la página renderizada.
    """
    user = request.user

    # Acentuación: solo se dispone del resultado del ejercicio 2
    acent_values = []
    acent_slugs = ["acentuacion2","acentuacion3"]
    acent_mc = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=acent_slugs
    )
    acent_values += [res.percentage for res in acent_mc]
    
    acento_res = ResultSummary.objects.filter(user=user).order_by("-created_at").first()
       
    if acento_res:
        acent_values.append(acento_res.percentage)
    
    acent_pct = _average_percentage(acent_values)
    
    
    # Puntuación: combinamos resultados de opción múltiple y del ejercicio
    # interactivo de puntuación final. Calculamos la media de todos los
    # resultados disponibles.
    punct_slugs = ["puntuacion1", "puntuacion2" , "puntuacion3"]
    punct_mc_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=punct_slugs
    )
    punct_values: list[float] = [res.percentage for res in punct_mc_results]
    punct_final = PunctuationResult.objects.filter(user=user).order_by("-created_at").first()
    if punct_final:
        punct_values.append(punct_final.percentage)
    puntuacion_pct = _average_percentage(punct_values)

    # Mayúsculas y minúsculas
    mayus_slugs = ["mayus1", "mayus2" , "mayus3"]
    mayus_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=mayus_slugs
    )
    mayus_values: list[float] = [res.percentage for res in mayus_results]
    mayus_pct = _average_percentage(mayus_values)

    # Reglas de las letras
    letras_slugs = ["letras1", "letras2" , "letras3"]
    letras_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=letras_slugs
    )
    letras_values: list[float] = [res.percentage for res in letras_results]
    letras_pct = _average_percentage(letras_values)
    
    # Evaluación final: obtenemos el resultado más reciente del ejercicio de evaluación final
    final_res = MultipleChoiceResult.objects.filter(user=user, exercise_slug="evaluacionfinal").order_by("-created_at").first()
    final_pct = final_res.percentage if final_res else None

    # Construimos el contexto con los porcentajes y dominios
    context: Dict[str, Tuple[str, str]] = {
        "acentuacion": (f"{acent_pct:.0f}%" if acent_pct is not None else "N/A", _classify_domain(acent_pct)),
        "puntuacion": (f"{puntuacion_pct:.0f}%" if puntuacion_pct is not None else "N/A", _classify_domain(puntuacion_pct)),
        "mayusculas": (f"{mayus_pct:.0f}%" if mayus_pct is not None else "N/A", _classify_domain(mayus_pct)),
        "letras": (f"{letras_pct:.0f}%" if letras_pct is not None else "N/A", _classify_domain(letras_pct)),
        "evaluacionfinal": (f"{final_pct:.0f}%" if final_pct is not None else "N/A", _classify_domain(final_pct)),
    }

    return render(request, "menu/estudiante/evaluaciones.html", {
        "user_name": user.nombre + " " + user.apellido or "",
        "user_id": getattr(user, "cedula", ""),
        "results": context,
    })


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
def evaluaciones_report(request):
    """Genera un informe PDF con los resultados de todas las unidades.

    La función recupera los mismos datos que ``evaluaciones_view``,
    construye una tabla usando Matplotlib y devuelve un
    ``HttpResponse`` con el contenido PDF.  El archivo se descarga
    automáticamente en el navegador del usuario.
    """
    user = request.user

    # Reutilizamos el cálculo de porcentajes de la vista principal
    # Acentuación: solo se dispone del resultado del ejercicio 2
    acent_values = []
    acent_slugs = ["acentuacion2","acentuacion3"]
    acent_mc = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=acent_slugs
    )
    acent_values += [res.percentage for res in acent_mc]
    
    acento_res = ResultSummary.objects.filter(user=user).order_by("-created_at").first()
       
    if acento_res:
        acent_values.append(acento_res.percentage)
    
    acento_pct = _average_percentage(acent_values)
    # Puntuación
    punct_slugs = ["puntuacion1", "puntuacion2", "puntuacion3"]
    punct_mc_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=punct_slugs
    )
    punct_values: list[float] = [res.percentage for res in punct_mc_results]
    punct_final = PunctuationResult.objects.filter(user=user).order_by("-created_at").first()
    if punct_final:
        punct_values.append(punct_final.percentage)
    puntuacion_pct = _average_percentage(punct_values)
    # Mayúsculas
    mayus_slugs = ["mayus1", "mayus2", "mayus3"]
    mayus_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=mayus_slugs
    )
    mayus_values: list[float] = [res.percentage for res in mayus_results]
    mayus_pct = _average_percentage(mayus_values)
    # Letras
    letras_slugs = ["letras1", "letras2", "letras3"]
    letras_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=letras_slugs
    )
    letras_values: list[float] = [res.percentage for res in letras_results]
    letras_pct = _average_percentage(letras_values)

    # Evaluación final
    final_res = MultipleChoiceResult.objects.filter(user=user, exercise_slug="evaluacionfinal").order_by("-created_at").first()
    final_pct = final_res.percentage if final_res else None
    
    # Construcción de tabla para PDF
    results = {
        "Acentuación": (
            f"{acento_pct:.0f}%" if acento_pct is not None else "N/A",
            _classify_domain(acento_pct),
        ),
        "Puntuación": (
            f"{puntuacion_pct:.0f}%" if puntuacion_pct is not None else "N/A",
            _classify_domain(puntuacion_pct),
        ),
        "Mayúscula y Minúscula": (
            f"{mayus_pct:.0f}%" if mayus_pct is not None else "N/A",
            _classify_domain(mayus_pct),
        ),
        "Reglas de las Letras": (
            f"{letras_pct:.0f}%" if letras_pct is not None else "N/A",
            _classify_domain(letras_pct),
        ),
        "Evaluación final": (
            f"{final_pct:.0f}%" if final_pct is not None else "N/A",
            _classify_domain(final_pct),
        ),
    }

    # Creamos el PDF en un buffer y seleccionamos el método de generación
    buffer = io.BytesIO()
    if _HAS_REPORTLAB:
        # Utilizamos ReportLab y la clase Canvas para generar un informe
        # con un diseño similar al de la segunda imagen proporcionada.
        c = rl_canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Definimos márgenes y configuramos colores principales
        margin_x = 40
        green_primary = colors.HexColor('#7CC300')
        green_dark = colors.HexColor('#00471b')
        light_green = colors.HexColor('#f5fdf0')

        # Dibujamos el título dentro de un rectángulo de bordes redondeados
        title_text = "Reporte de Evaluaciones"
        title_width = 350
        title_height = 40
        title_x = (width - title_width) / 2
        title_y = height - 80
        c.setLineWidth(2)
        c.setStrokeColor(green_primary)
        c.setFillColor(colors.white)
        c.roundRect(title_x, title_y, title_width, title_height, 10, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(green_dark)
        c.drawCentredString(title_x + title_width / 2, title_y + 12, title_text)

        # Sección de información del educando
        info_y = title_y - 40
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(green_dark)
        c.drawString(margin_x, info_y, "Información del Educando")
        info_y -= 20
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(margin_x, info_y, f"Nombre: {user.nombre + ' ' + (user.apellido if user.apellido else '')}")
        info_y -= 18
        user_id_val = getattr(user, 'cedula', '')
        c.drawString(margin_x, info_y, f"Cédula: {user_id_val}")

        # Posición inicial de la tabla
        table_y = info_y - 40
        row_height = 24
        col_widths = [260, 120, 120]
        table_width = sum(col_widths)

        # Dibujamos el encabezado de la tabla
        c.setFillColor(green_primary)
        c.rect(margin_x, table_y, table_width, row_height, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12)
        headers = ["Unidad", "Puntuación", "Dominio"]
        x_offset = margin_x
        for idx, header in enumerate(headers):
            c.drawCentredString(x_offset + col_widths[idx] / 2, table_y + 7, header)
            x_offset += col_widths[idx]

        # Dibujamos las filas con datos
        c.setFont("Helvetica", 11)
        y_pos = table_y - row_height
        for i, (unidad, (punt, dom)) in enumerate(results.items()):
            # alternar colores de fila
            if i % 2 == 0:
                c.setFillColor(light_green)
                c.rect(margin_x, y_pos, table_width, row_height, fill=1, stroke=0)
            c.setFillColor(colors.black)
            x_pos = margin_x
            # Unidad
            c.drawString(x_pos + 5, y_pos + 7, unidad)
            x_pos += col_widths[0]
            # Puntuación
            c.drawString(x_pos + 5, y_pos + 7, punt)
            x_pos += col_widths[1]
            # Dominio
            c.drawString(x_pos + 5, y_pos + 7, dom)
            y_pos -= row_height

        # Calculamos extremos para dibujar bordes de la tabla.
        # row_count equivale a la cantidad de filas de datos. Hay una fila extra para el encabezado.
        row_count = len(results)
        table_height = row_height * (row_count + 0) #Tamaño lineas de columnas
        table_bottom_y = table_y - table_height
        c.setLineWidth(1)
        c.setStrokeColor(green_primary)

        # Líneas horizontales: dibujamos desde la parte superior de la tabla hasta la inferior
        for i in range(row_count + 1):  # incluye la línea inferior después del último dato #Tamaño lineas de filas
            y_line = table_y - i * row_height
            c.line(margin_x, y_line, margin_x + table_width, y_line)

        # Líneas verticales: dibujamos cada borde de columna y el borde derecho
        x_line = margin_x
        for width_val in col_widths:
            c.line(x_line, table_y, x_line, table_bottom_y)
            x_line += width_val
        # Línea del borde derecho
        c.line(margin_x + table_width, table_y, margin_x + table_width, table_bottom_y)

        # Cierra la página y obtiene el contenido
        c.showPage()
        c.save()
        pdf_data = buffer.getvalue()
        buffer.close()
    else:
        # Método de respaldo utilizando Matplotlib si reportlab no está disponible
        # Método de respaldo utilizando Matplotlib si reportlab no está disponible.
        # Generamos manualmente el PDF con un diseño similar para evitar filas en blanco.
        with PdfPages(buffer) as pdf:
            import matplotlib.patches as patches
            fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 tamaño aproximado
            ax.axis('off')

            # Configuración de colores
            green_primary = '#7CC300'
            green_dark = '#00471b'
            light_green = '#f5fdf0'

            # Dibujamos el título con un rectángulo de bordes redondeados
            title_w = 0.6
            title_h = 0.05
            title_x = (1 - title_w) / 2
            title_y = 0.92
            # Marco del título
            rect = patches.FancyBboxPatch((title_x, title_y), title_w, title_h,
                                         boxstyle="round,pad=0.02", edgecolor=green_primary,
                                         linewidth=2, facecolor='white', transform=ax.transAxes)
            ax.add_patch(rect)
            ax.text(0.5, title_y + title_h / 2, 'Reporte de Evaluaciones', ha='center', va='center',
                    fontsize=16, fontweight='bold', color=green_dark, transform=ax.transAxes)

            # Sección de información del educando
            info_y = title_y - 0.08
            ax.text(0.1, info_y, 'Información del Educando', fontsize=13, weight='bold', color=green_dark,
                    transform=ax.transAxes)
            info_y -= 0.04
            ax.text(0.1, info_y, f'Nombre: {user.nombre + " " + user.apellido or ""}', fontsize=11, color='black',
                    transform=ax.transAxes)
            info_y -= 0.03
            user_id_val = getattr(user, 'cedula', '')
            ax.text(0.1, info_y, f'Cédula: {user_id_val}', fontsize=11, color='black', transform=ax.transAxes)

            # Coordenadas para la tabla
            table_y = info_y - 0.07
            row_height = 0.05
            col_widths = [0.5, 0.25, 0.25]
            table_width = sum(col_widths)
            # Encabezado de la tabla
            header_y = table_y
            header_rect = patches.Rectangle((0.1, header_y - row_height), table_width, row_height,
                                           linewidth=0, facecolor=green_primary, transform=ax.transAxes)
            ax.add_patch(header_rect)
            # Texto de encabezado
            headers = ['Unidad', 'Puntuación', 'Dominio']
            x_offset = 0.1
            for idx, header in enumerate(headers):
                ax.text(x_offset + col_widths[idx] / 2, header_y - row_height / 2,
                        header, fontsize=12, weight='bold', color='white', ha='center', va='center', transform=ax.transAxes)
                x_offset += col_widths[idx]

            # Filas de datos
            # Calculamos la posición inicial de la primera fila (justo debajo del encabezado)
            y_pos = header_y - 2 * row_height
            for i, (unidad, (punt, dom)) in enumerate(results.items()):
                # Fondo alternado para filas 1,3,... según índice i
                if i % 2 == 1:
                    row_rect = patches.Rectangle((0.1, y_pos), table_width, row_height,
                                                linewidth=0, facecolor=light_green, transform=ax.transAxes)
                    ax.add_patch(row_rect)
                # Texto de la fila centrado verticalmente dentro de la celda
                x = 0.1
                ax.text(x + 0.01, y_pos + row_height / 2, unidad, fontsize=11, color='black', ha='left', va='center',
                        transform=ax.transAxes)
                x += col_widths[0]
                ax.text(x + 0.01, y_pos + row_height / 2, punt, fontsize=11, color='black', ha='left', va='center',
                        transform=ax.transAxes)
                x += col_widths[1]
                ax.text(x + 0.01, y_pos + row_height / 2, dom, fontsize=11, color='black', ha='left', va='center',
                        transform=ax.transAxes)
                # Retrocedemos la posición para la siguiente fila
                y_pos -= row_height

            # Dibujamos líneas horizontales y verticales para la tabla
            row_count = len(results)
            # Línea superior de la tabla y líneas después de cada fila
            for j in range(row_count + 1):
                y_line = header_y - j * row_height
                ax.plot([0.1, 0.1 + table_width], [y_line, y_line], color=green_primary, linewidth=1, transform=ax.transAxes)
            # Línea inferior del último registro
            y_bottom = header_y - (row_count + 1) * row_height
            ax.plot([0.1, 0.1 + table_width], [y_bottom, y_bottom], color=green_primary, linewidth=1, transform=ax.transAxes)
            # Líneas verticales (incluyendo borde derecho)
            x_line = 0.1
            for w in col_widths:
                ax.plot([x_line, x_line], [header_y, y_bottom], color=green_primary, linewidth=1, transform=ax.transAxes)
                x_line += w
            ax.plot([0.1 + table_width, 0.1 + table_width], [header_y, y_bottom], color=green_primary, linewidth=1,
                    transform=ax.transAxes)

            pdf.savefig(fig)
            plt.close(fig)
        pdf_data = buffer.getvalue()
        buffer.close()
    # Devolvemos el PDF como respuesta HTTP
    from django.http import HttpResponse
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_evaluaciones.pdf"'
    return response

#########################################
# -----------------------------------------------------------------------------
# Vistas de evaluaciones para docentes
#
# Estas funciones permiten a los usuarios con rol de docente revisar el
# desempeño de todos los estudiantes registrados.  Se calcula el
# porcentaje de cada unidad de la misma manera que para la vista de
# estudiantes, pero iterando sobre todos los alumnos.  También se
# incluye la posibilidad de generar un informe PDF con los resultados
# globales.

# views_evaluaciones.py
@login_required
@role_login_required(Usuario.DOCENTE, login_url_name="login_docente")
def evaluaciones_docente_view(request):
    User = get_user_model()

    q = request.GET.get("q", "").strip()
    per = request.GET.get("per", "10").strip().lower()
    per_page = 10 if per != "all" else 100000  # "todo" sin paginar práctico

    # Solo estudiantes
    estudiantes = User.objects.filter(role=Usuario.ESTUDIANTE) if hasattr(User, "role") \
        else User.objects.none()

    # Búsqueda por cédula, nombre, apellido, email
    if q:
        estudiantes = estudiantes.filter(
            Q(cedula__icontains=q) |
            Q(nombre__icontains=q) |
            Q(apellido__icontains=q) |
            Q(email__icontains=q)
        )

    estudiantes = estudiantes.order_by("apellido", "nombre")

    paginator = Paginator(estudiantes, per_page)
    page_obj = paginator.get_page(request.GET.get("page"))

    rows = []
    for est in page_obj.object_list:
        # ACENTUACIÓN
        acent_values = []
        for res in MultipleChoiceResult.objects.filter(user=est, exercise_slug__in=["acentuacion2","acentuacion3"]):
            acent_values.append(res.percentage)
        acento_res = ResultSummary.objects.filter(user=est).order_by("-created_at").first()
        if acento_res:
            acent_values.append(acento_res.percentage)
        acento_pct = _average_percentage(acent_values)
        acento_dom = _classify_domain(acento_pct)

        # PUNTUACIÓN
        punct_values = [r.percentage for r in MultipleChoiceResult.objects.filter(
            user=est, exercise_slug__in=["puntuacion1", "puntuacion2", "puntuacion3"]
        )]
        punct_final = PunctuationResult.objects.filter(user=est).order_by("-created_at").first()
        if punct_final:
            punct_values.append(punct_final.percentage)
        puntuacion_pct = _average_percentage(punct_values)
        puntuacion_dom = _classify_domain(puntuacion_pct)

        # MAYÚSCULAS
        mayus_values = [r.percentage for r in MultipleChoiceResult.objects.filter(
            user=est, exercise_slug__in=["mayus1", "mayus2", "mayus3"]
        )]
        mayus_pct = _average_percentage(mayus_values)
        mayus_dom = _classify_domain(mayus_pct)

        # REGLAS DE LETRAS
        letras_values = [r.percentage for r in MultipleChoiceResult.objects.filter(
            user=est, exercise_slug__in=["letras1", "letras2", "letras3"]
        )]
        letras_pct = _average_percentage(letras_values)
        letras_dom = _classify_domain(letras_pct)

        # EVALUACIÓN FINAL
        final_res = MultipleChoiceResult.objects.filter(
            user=est, exercise_slug="evaluacionfinal"
        ).order_by("-created_at").first()
        final_pct = final_res.percentage if final_res else None
        final_dom = _classify_domain(final_pct)

        # Última actividad del calendario si la usas (opcional)
        last = CalendarActivity.objects.filter(user=est).order_by("-date").first()
        last_date = last.date if last else None
        last_title = last.title if last else None

        rows.append({
            "user_id": est.id,
            "name": f"{est.nombre} {est.apellido}".strip(),
            "id": est.cedula,
            "acento_pct": f"{acentuacion:.0f}%" if (acentuacion := acento_pct) is not None else "N/A",
            "acento_dom": acento_dom,
            "puntuacion_pct": f"{puntuacion:.0f}%" if (puntuacion := puntuacion_pct) is not None else "N/A",
            "puntuacion_dom": puntuacion_dom,
            "mayus_pct": f"{mayusculas:.0f}%" if (mayusculas := mayus_pct) is not None else "N/A",
            "mayus_dom": mayus_dom,
            "letras_pct": f"{letras:.0f}%" if (letras := letras_pct) is not None else "N/A",
            "letras_dom": letras_dom,
            "final_pct": f"{final:.0f}%" if (final := final_pct) is not None else "N/A",
            "final_dom": final_dom,
            "last_date": last_date,
            "last_title": last_title,
        })

    return render(request, "menu/docente/evaluaciones.html", {
        "students": rows,
        "page_obj": page_obj,
        "q": q,
        "per": per,
    })



@login_required
@role_login_required(Usuario.DOCENTE, login_url_name="login_docente")
def evaluaciones_docente_report(request):
    """Genera un PDF con los resultados de todos los estudiantes.

    Cada fila de la tabla en el PDF representa a un estudiante con sus
    porcentajes y dominios para cada unidad.  Si ReportLab está
    disponible se utiliza la clase ``Canvas`` para lograr un diseño
    profesional; de lo contrario se recurre a un respaldo con
    Matplotlib.

    Args:
        request: objeto ``HttpRequest``.

    Returns:
        ``HttpResponse`` que contiene el PDF.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Seleccionamos estudiantes de acuerdo con el campo de rol existente en el modelo.
    if hasattr(User, 'role'):
        estudiantes = User.objects.filter(role=Usuario.ESTUDIANTE)
    elif hasattr(User, 'rol'):
        estudiantes = User.objects.filter(rol=Usuario.ESTUDIANTE)
    elif hasattr(User, 'is_student'):
        estudiantes = User.objects.filter(is_student=True)
    else:
        estudiantes = User.objects.none()
    rows_dom: list[list[str]] = []
    for est in estudiantes:
        # Cálculo de porcentajes para cada estudiante
        # Acentuación: solo se dispone del resultado del ejercicio 2
        acent_values = []
        for res in MultipleChoiceResult.objects.filter(user=est, exercise_slug__in=["acentuacion2","acentuacion3"]):
            acent_values.append(res.percentage)
        
        acento_res = ResultSummary.objects.filter(user=est).order_by("-created_at").first()    
        if acento_res:
            acent_values.append(acento_res.percentage)
        
        acento_pct = _average_percentage(acent_values)
        
        punct_vals = [res.percentage for res in MultipleChoiceResult.objects.filter(user=est, exercise_slug__in=["puntuacion1", "puntuacion2", "puntuacion3"])]
        pf = PunctuationResult.objects.filter(user=est).order_by("-created_at").first()
        if pf:
            punct_vals.append(pf.percentage)
        puntuacion_pct = _average_percentage(punct_vals)
        mayus_vals = [res.percentage for res in MultipleChoiceResult.objects.filter(user=est, exercise_slug__in=["mayus1", "mayus2", "mayus3"])]
        mayus_pct = _average_percentage(mayus_vals)
        letras_vals = [res.percentage for res in MultipleChoiceResult.objects.filter(user=est, exercise_slug__in=["letras1", "letras2", "letras3"])]
        letras_pct = _average_percentage(letras_vals)
        final_res = MultipleChoiceResult.objects.filter(user=est, exercise_slug="evaluacionfinal").order_by("-created_at").first()
        final_pct = final_res.percentage if final_res else None
        rows_dom.append([
        f"{getattr(est, 'nombre', '') or ''} {getattr(est, 'apellido', '') or ''}".strip(),
        f"{getattr(est, 'cedula', '') or ''}",
        _classify_domain(acento_pct),
        _classify_domain(puntuacion_pct),
        _classify_domain(mayus_pct),
        _classify_domain(letras_pct),
        _classify_domain(final_pct),
    ])
    buffer = io.BytesIO()
    if _HAS_REPORTLAB:
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib import colors
        from reportlab.lib.units import mm

        # Paleta
        GREEN    = colors.HexColor('#7CC300')
        DARK     = colors.HexColor('#00471b')
        BAND     = colors.HexColor('#e6f4d7')  # banda de cabecera (suave)
        STRIPE   = colors.HexColor('#f5fdf0')  # cebreado filas

        # Doc
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            leftMargin=18*mm, rightMargin=18*mm,
            topMargin=24*mm, bottomMargin=18*mm
        )
        W, H = A4

        styles = getSampleStyleSheet()
        cell = ParagraphStyle(
            "cell", parent=styles["Normal"],
            fontName="Helvetica", fontSize=9, leading=11, textColor=colors.black
        )
        cell_bold = ParagraphStyle(
            "cell_bold", parent=cell, fontName="Helvetica-Bold"
        )

        # Encabezado: banda + info del educador
        def _header(canvas, doc):
            canvas.saveState()
            # Banda verde clara
            x = doc.leftMargin
            w = W - doc.leftMargin - doc.rightMargin
            canvas.setFillColor(BAND)
            canvas.rect(x, H - doc.topMargin + 6*mm, w, 10*mm, stroke=0, fill=1)
            # Título centrado
            canvas.setFillColor(DARK)
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawCentredString(W/2, H - doc.topMargin + 9*mm, "Reporte de Evaluaciones Educador")
            # Información del Educador
            y = H - doc.topMargin - 2*mm
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x, y, "Información del Educador")
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(colors.black)
            canvas.drawString(x, y - 12, f"Nombre : {getattr(request.user, 'nombre', '')} {getattr(request.user, 'apellido', '')}".strip())
            canvas.drawString(x, y - 24, f"Cédula: {getattr(request.user, 'cedula', '')}")
            canvas.restoreState()

        # Datos
        headers = [
            "Educando", "Cédula", "Dominio Acentuación",
            "Dominio Puntuación", "Dominio Mayúscula",
            "Dominio Letras", "Dominio Final",
        ]
        # Anchuras medidas para A4
        col_widths = [40*mm, 25*mm, 25*mm, 25*mm, 25*mm, 25*mm, 25*mm]

        # Parrafos para wraps elegantes
        data = [[Paragraph(h, cell_bold) for h in headers]]
        for r in rows_dom:
            data.append([
                Paragraph(r[0], cell),  # nombre
                Paragraph(r[1], cell),  # cédula
                Paragraph(r[2], cell),
                Paragraph(r[3], cell),
                Paragraph(r[4], cell),
                Paragraph(r[5], cell),
                Paragraph(r[6], cell),
            ])

        table = Table(data, colWidths=col_widths, repeatRows=1)

        # Estilo base
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GREEN),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,0), 10),
            ('ALIGN',      (0,0), (0,-1), 'LEFT'),   # primera col a la izquierda
            ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, STRIPE]),
            ('GRID',       (0,0), (-1,-1), 0.6, GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ])

        # Colorear por dominio
        def bg_for(value: str):
            v = (value or "").strip().lower()
            if v == "excelente":     return colors.HexColor("#ffffff") #eaffea
            if v == "suficiente":    return colors.HexColor("#ffffff") #fff5e6
            if v == "insuficiente":  return colors.HexColor("#ffffff") #ffecec
            return colors.HexColor("#ffffff") #f1f5f9 # N/A

        for ridx, row in enumerate(rows_dom, start=1):   # +1 por el header
            for cidx in range(2, 7):  # solo columnas de dominio
                style.add('BACKGROUND', (cidx, ridx), (cidx, ridx), bg_for(row[cidx]))

        table.setStyle(style)

        # Dejo aire para que no invada el header
        story = [Spacer(1, 40*mm), table]
        doc.build(story, onFirstPage=_header, onLaterPages=_header)

        pdf_data = buffer.getvalue()
        buffer.close()

    from django.http import HttpResponse
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_evaluaciones_docente.pdf"'
    return response


##############################
# Crear nuevo educando
@login_required
@role_login_required(Usuario.DOCENTE, login_url_name="login_docente")
@require_http_methods(["GET", "POST"])
def educando_create(request):
    if request.method == "POST":
        cedula = request.POST.get("cedula", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        apellido = request.POST.get("apellido", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not all([cedula, nombre, apellido, email, password1, password2]):
            messages.error(request, "Completa todos los campos.")
            return redirect("educando_create")
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("educando_create")

        User = get_user_model()
        # Crea la cuenta del sistema con rol ESTUDIANTE
        user = User.objects.create_user(
            cedula=cedula, email=email, nombre=nombre, apellido=apellido,
            role=Usuario.ESTUDIANTE, password=password1
        )
        # Crea el perfil Estudiante espejo de datos
        Estudiante.objects.create(user=user, cedula=cedula, nombre=nombre, apellido=apellido)

        messages.success(request, "Educando creado correctamente.")
        return redirect("evaluaciones_docente")

    return render(request, "menu/docente/educando_form.html", {"mode": "create"})

# Editar educando existente
@login_required
@role_login_required(Usuario.DOCENTE, login_url_name="login_docente")
@require_http_methods(["GET", "POST"])
def educando_edit(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id, role=Usuario.ESTUDIANTE)

    if request.method == "POST":
        cedula = request.POST.get("cedula", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        apellido = request.POST.get("apellido", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # Actualizar datos reales del login
        user.cedula = cedula
        user.nombre = nombre
        user.apellido = apellido
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        # Espejo en perfil Estudiante (si existiera)
        try:
            est = user.estudiante
            est.cedula = cedula
            est.nombre = nombre
            est.apellido = apellido
            est.save()
        except Estudiante.DoesNotExist:
            pass

        messages.success(request, "Datos del educando actualizados.")
        return redirect("evaluaciones_docente")

    return render(request, "menu/docente/educando_form.html", {"mode": "edit", "u": user})

# Eliminar educando existente
@login_required
@role_login_required(Usuario.DOCENTE, login_url_name="login_docente")
@require_http_methods(["GET", "POST"])
def educando_delete(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id, role=Usuario.ESTUDIANTE)

    if request.method == "POST":
        user.delete()  # esto elimina también el perfil Estudiante
        messages.success(request, "Educando eliminado. Ya no podrá iniciar sesión.")
        return redirect("evaluaciones_docente")

    return render(request, "menu/docente/educando_confirm_delete.html", {"u": user})


##################
#Administrador
##################
# views_evaluaciones.py

from django import forms
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods

# Importa tus modelos de resultados y usuario
from .models import (
    Usuario, Docente, Estudiante, Administrador,
    MultipleChoiceResult, PunctuationResult, ResultSummary, CalendarActivity
)

# ---------- Formulario base para CRUD de Usuario ----------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["cedula", "email", "nombre", "apellido", "role", "is_active"]
        widgets = {
            "cedula": forms.TextInput(attrs={"class":"input"}),
            "email": forms.EmailInput(attrs={"class":"input"}),
            "nombre": forms.TextInput(attrs={"class":"input"}),
            "apellido": forms.TextInput(attrs={"class":"input"}),
            "role": forms.Select(attrs={"class":"input"}),
        }

# Helper para mantener sincronizado el perfil OneToOne según el rol
def _ensure_profile(user: Usuario) -> None:# ---------- Cálculo de métricas por usuario (igual que en estudiante/docente) ----------
    # Elimina perfiles cruzados, crea el correcto si falta
    if user.role == Usuario.DOCENTE:
        Administrador.objects.filter(user=user).delete()
        Estudiante.objects.filter(user=user).delete()
        Docente.objects.get_or_create(user=user, defaults={
            "cedula": user.cedula, "nombre": user.nombre, "apellido": user.apellido
        })
    elif user.role == Usuario.ESTUDIANTE:
        Docente.objects.filter(user=user).delete()
        Administrador.objects.filter(user=user).delete()
        Estudiante.objects.get_or_create(user=user, defaults={
            "cedula": user.cedula, "nombre": user.nombre, "apellido": user.apellido
        })
    else:  # ADMINISTRADOR
        Docente.objects.filter(user=user).delete()
        Estudiante.objects.filter(user=user).delete()
        Administrador.objects.get_or_create(user=user, defaults={
            "cedula": user.cedula, "nombre": user.nombre, "apellido": user.apellido
        })


def _metrics_for(user: Usuario):
    # Acentuación: promedio entre slugs de MC y summaries
    acent_slugs = ["acentuacion2","acentuacion3"]
    acent_mc = MultipleChoiceResult.objects.filter(user=user, exercise_slug__in=acent_slugs).values_list("percentage", flat=True)
    acento_res = ResultSummary.objects.filter(user=user).order_by("-created_at").first()
    acent_values = list(acent_mc)
    if acento_res: acent_values.append(float(acento_res.percentage))
    acento_pct = _average_percentage(acent_values)
    acento_dom = _classify_domain(acento_pct)

    # Puntuación: MC + ejercicio final
    punct_slugs = ["puntuacion1","puntuacion2","puntuacion3"]
    punct_mc = MultipleChoiceResult.objects.filter(user=user, exercise_slug__in=punct_slugs).values_list("percentage", flat=True)
    punct_values = list(punct_mc)
    punct_final = PunctuationResult.objects.filter(user=user).order_by("-created_at").first()
    if punct_final: punct_values.append(float(punct_final.percentage))
    puntuacion_pct = _average_percentage(punct_values)
    puntuacion_dom = _classify_domain(puntuacion_pct)

    # Mayúsculas
    mayus_slugs = ["mayus1","mayus2","mayus3"]
    mayus_mc = MultipleChoiceResult.objects.filter(user=user, exercise_slug__in=mayus_slugs).values_list("percentage", flat=True)
    mayus_pct = _average_percentage(list(mayus_mc))
    mayus_dom = _classify_domain(mayus_pct)

    # Reglas de las letras
    letras_slugs = ["letras1","letras2","letras3"]
    letras_mc = MultipleChoiceResult.objects.filter(user=user, exercise_slug__in=letras_slugs).values_list("percentage", flat=True)
    letras_pct = _average_percentage(list(letras_mc))
    letras_dom = _classify_domain(letras_pct)

    # Final
    final_res = MultipleChoiceResult.objects.filter(user=user, exercise_slug="evaluacionfinal").order_by("-created_at").first()
    final_pct = float(final_res.percentage) if final_res else None
    final_dom = _classify_domain(final_pct)

    # Última actividad
    last = CalendarActivity.objects.filter(user=user).order_by("-created_at").first()
    last_date = last.created_at if last else None
    last_title = last.title if last else None

    def fmt(x): return f"{x:.0f}%" if x is not None else "N/A"

    return {
        "acento_pct": fmt(acento_pct), "acento_dom": acento_dom,
        "puntuacion_pct": fmt(puntuacion_pct), "puntuacion_dom": puntuacion_dom,
        "mayus_pct": fmt(mayus_pct), "mayus_dom": mayus_dom,
        "letras_pct": fmt(letras_pct), "letras_dom": letras_dom,
        "final_pct": fmt(final_pct), "final_dom": final_dom,
        "last_date": last_date, "last_title": last_title,
    }

# ---------- LISTA ADMIN con buscador/paginación ----------
@role_login_required(Usuario.ADMINISTRADOR, login_url_name="login_administrador")
def evaluaciones_administrador_view(request):
    q = request.GET.get("q", "").strip()
    per = request.GET.get("per", "10")  # "10" | "all"

    users = Usuario.objects.all().order_by("apellido","nombre")
    if q:
        users = users.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) |
            Q(email__icontains=q)  | Q(cedula__icontains=q)
        )

    if per != "all":
        paginator = Paginator(users, 10)
        page_obj = paginator.get_page(request.GET.get("page"))
        list_users = page_obj.object_list
    else:
        page_obj = type("obj", (), {"has_previous": False, "has_next": False,
                                    "number": 1, "paginator": type("p", (), {"num_pages": 1})})()
        list_users = list(users)

    rows = []
    for u in list_users:
        m = _metrics_for(u)
        rows.append({
            "user_id": u.id,
            "name": f"{u.nombre} {u.apellido}".strip() or u.cedula,
            "id": u.cedula,
            "email": u.email,
            "role": u.role,
            "role_display": getattr(u, "get_role_display", lambda: u.role)(),
            **m,
        })

    return render(request, "menu/administrador/evaluaciones_admin.html", {
        "q": q, "per": per, "page_obj": page_obj, "students": rows  # reuso nombre 'students' para la tabla
    })

@role_login_required(Usuario.ADMINISTRADOR, login_url_name="login_administrador")
def evaluaciones_administrador_report(request):
    # 1) Obtener todos los usuarios
    users = Usuario.objects.all().order_by("apellido","nombre")

    # 2) Armar filas: nombre, cédula, rol, dominios
    rows = []
    for u in users:
        m = _metrics_for(u)  # ya devuelve dom y pct
        rows.append({
            "name": f"{u.nombre} {u.apellido}".strip() or (u.cedula or ""),
            "ced":  u.cedula or "",
            "rol":  getattr(u, "get_role_display", lambda: u.role)(),
            "acento_dom":      m["acento_dom"],
            "puntuacion_dom":  m["puntuacion_dom"],
            "mayus_dom":       m["mayus_dom"],
            "letras_dom":      m["letras_dom"],
            "final_dom":       m["final_dom"],
        })

    buffer = io.BytesIO()
    if _HAS_REPORTLAB:
        # ===== ReportLab =====
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import mm

        GREEN  = colors.HexColor('#7CC300')
        DARK   = colors.HexColor('#00471b')
        STRIPE = colors.HexColor('#f5fdf0')

        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                leftMargin=18*mm, rightMargin=18*mm,
                                topMargin=24*mm, bottomMargin=18*mm)
        W, H = A4
        styles = getSampleStyleSheet()
        cell = ParagraphStyle("cell", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=11)
        cell_bold = ParagraphStyle("cell_bold", parent=cell, fontName="Helvetica-Bold")

        def _header(canvas, doc):
            canvas.saveState()
            x = doc.leftMargin
            w = W - doc.leftMargin - doc.rightMargin
            canvas.setFillColor(colors.HexColor("#e6f4d7"))
            canvas.rect(x, H - doc.topMargin + 6*mm, w, 10*mm, stroke=0, fill=1)
            canvas.setFillColor(DARK)
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawCentredString(W/2, H - doc.topMargin + 9*mm, "Reporte de Evaluaciones (Administrador)")
            y = H - doc.topMargin - 2*mm
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x, y, "Información del Administrador")
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(colors.black)
            canvas.drawString(x, y - 12, f"Nombre : {(getattr(request.user,'nombre','') + ' ' + getattr(request.user,'apellido','')).strip()}")
            canvas.drawString(x, y - 24, f"Cédula: {getattr(request.user,'cedula','')}")
            canvas.restoreState()

        headers = ["Usuario", "Cédula", "Rol",
                   "Dom. Acentuación", "Dom. Puntuación", "Dom. Mayúsculas",
                   "Dom. Letras", "Dom. Final"]
        col_widths = [38*mm, 22*mm, 22*mm, 24*mm, 24*mm, 24*mm, 24*mm, 24*mm]

        data = [[Paragraph(h, cell_bold) for h in headers]]
        for r in rows:
            data.append([
                Paragraph(r["name"], cell),
                Paragraph(r["ced"], cell),
                Paragraph(r["rol"], cell),
                Paragraph(r["acento_dom"], cell),
                Paragraph(r["puntuacion_dom"], cell),
                Paragraph(r["mayus_dom"], cell),
                Paragraph(r["letras_dom"], cell),
                Paragraph(r["final_dom"], cell),
            ])

        table = Table(data, colWidths=col_widths, repeatRows=1)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GREEN),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,0), 10),
            ('ALIGN',      (0,0), (0,-1), 'LEFT'),
            ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, STRIPE]),
            ('GRID',       (0,0), (-1,-1), 0.6, GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ])
        table.setStyle(style)

        story = [Spacer(1, 40*mm), table]
        doc.build(story, onFirstPage=_header, onLaterPages=_header)
        pdf_data = buffer.getvalue()
        buffer.close()
    else:
        # ===== Respaldo Matplotlib =====
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        import matplotlib.patches as patches

        with PdfPages(buffer) as pdf:
            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.axis('off')
            green_primary = '#7CC300'
            green_dark = '#00471b'
            light_green = '#f5fdf0'

            rect = patches.FancyBboxPatch((0.2, 0.92), 0.6, 0.05,
                                          boxstyle="round,pad=0.02", edgecolor=green_primary,
                                          linewidth=2, facecolor='white', transform=ax.transAxes)
            ax.add_patch(rect)
            ax.text(0.5, 0.945, 'Reporte de Evaluaciones (Administrador)', ha='center', va='center',
                    fontsize=16, fontweight='bold', color=green_dark, transform=ax.transAxes)

            info_y = 0.88
            ax.text(0.1, info_y, 'Información del Administrador', fontsize=13, weight='bold', color=green_dark, transform=ax.transAxes)
            ax.text(0.1, info_y - 0.03, f'Nombre: {(getattr(request.user,"nombre","")+" "+getattr(request.user,"apellido","")).strip()}', fontsize=11, transform=ax.transAxes)
            ax.text(0.1, info_y - 0.06, f'Cédula: {getattr(request.user,"cedula","")}', fontsize=11, transform=ax.transAxes)

            headers = ['Usuario','Cédula','Rol','Dom. Acent.','Dom. Punt.','Dom. Mayus.','Dom. Letras','Dom. Final']
            col_w = [0.25,0.12,0.1,0.12,0.12,0.12,0.12,0.12]
            x0, y0, rh = 0.08, 0.78, 0.035

            ax.add_patch(patches.Rectangle((x0, y0-rh), sum(col_w), rh, linewidth=0, facecolor=green_primary, transform=ax.transAxes))
            cx = x0
            for i,h in enumerate(headers):
                ax.text(cx + col_w[i]/2, y0 - rh/2, h, fontsize=10, color='white', ha='center', va='center', transform=ax.transAxes)
                cx += col_w[i]

            y = y0 - 2*rh
            for i,r in enumerate(rows):
                if i % 2 == 1:
                    ax.add_patch(patches.Rectangle((x0, y), sum(col_w), rh, linewidth=0, facecolor=light_green, transform=ax.transAxes))
                cx = x0
                vals = [r["name"], r["ced"], r["rol"], r["acento_dom"], r["puntuacion_dom"], r["mayus_dom"], r["letras_dom"], r["final_dom"]]
                for j,v in enumerate(vals):
                    ha = 'left' if j == 0 else 'left'
                    ax.text(cx + 0.005, y + rh/2, str(v), fontsize=9, ha=ha, va='center', transform=ax.transAxes)
                    cx += col_w[j]
                y -= rh
            pdf.savefig(fig); plt.close(fig)
        pdf_data = buffer.getvalue(); buffer.close()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_evaluaciones_admin.pdf"'
    return response


# ---------- CRUD de Usuario (Administrador) ----------
@role_login_required(Usuario.ADMINISTRADOR, login_url_name="login_administrador")
def usuario_create(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # soportar contraseña al crear
            pwd1 = request.POST.get("password1", "").strip()
            pwd2 = request.POST.get("password2", "").strip()
            if pwd1 and pwd1 == pwd2:
                user.set_password(pwd1)
            user.save()
            _ensure_profile(user)  # sincroniza perfil según rol
            messages.success(request, "Usuario creado.")
            return redirect("evaluaciones_admin")
    else:
        form = UsuarioForm()
    return render(request, "menu/administrador/usuario_form.html",
                  {"form": form, "title": "Crear usuario", "mode": "create"})

@role_login_required(Usuario.ADMINISTRADOR, login_url_name="login_administrador")
def usuario_edit(request, pk: int):
    user = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            # contraseña opcional al editar
            pwd = request.POST.get("password", "").strip()
            if pwd:
                user.set_password(pwd)
            user.save()
            _ensure_profile(user)  # si cambiaron el rol, corrige el perfil
            messages.success(request, "Usuario actualizado.")
            return redirect("evaluaciones_admin")
    else:
        form = UsuarioForm(instance=user)
    return render(request, "menu/administrador/usuario_form.html",
                  {"form": form, "title": "Editar usuario", "mode": "edit"})


@role_login_required(Usuario.ADMINISTRADOR, login_url_name="login_administrador")
@require_http_methods(["POST","GET"])
def usuario_delete(request, pk: int):
    u = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        u.delete()
        messages.success(request, "Usuario eliminado.")
        return redirect("evaluaciones_admin")
    return render(request, "menu/administrador/usuario_confirm_delete.html", {"u": u})
