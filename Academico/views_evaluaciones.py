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
    Exercise2Result,
    PunctuationResult,
    MultipleChoiceResult,
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


########

def _average_percentage(values: list[float]) -> Optional[float]:
    """Calcula el promedio de una lista de porcentajes.

    Si la lista está vacía se retorna ``None``.  Se utiliza el módulo
    ``statistics.mean`` para evitar reinvenciones.

    Args:
        values: Lista de valores porcentuales (0 a 100).

    Returns:
        El promedio de los valores o ``None`` si la lista está vacía.
    """
    return mean(values) if values else None


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
    if percentage < 60:
        return "Insuficiente"
    if percentage < 80:
        return "Suficiente"
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
    acento_res = Exercise2Result.objects.filter(user=user).order_by("-created_at").first()
    acento_pct = acento_res.percentage if acento_res else None

    # Puntuación: combinamos resultados de opción múltiple y del ejercicio
    # interactivo de puntuación final. Calculamos la media de todos los
    # resultados disponibles.
    punct_slugs = ["puntuacion1", "puntuacion2"]
    punct_mc_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=punct_slugs
    )
    punct_values: list[float] = [res.percentage for res in punct_mc_results]
    punct_final = PunctuationResult.objects.filter(user=user).order_by("-created_at").first()
    if punct_final:
        punct_values.append(punct_final.percentage)
    puntuacion_pct = _average_percentage(punct_values)

    # Mayúsculas y minúsculas
    mayus_slugs = ["mayus1", "mayus2"]
    mayus_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=mayus_slugs
    )
    mayus_values: list[float] = [res.percentage for res in mayus_results]
    mayus_pct = _average_percentage(mayus_values)

    # Reglas de las letras
    letras_slugs = ["letras1", "letras2"]
    letras_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=letras_slugs
    )
    letras_values: list[float] = [res.percentage for res in letras_results]
    letras_pct = _average_percentage(letras_values)

    # Construimos el contexto con los porcentajes y dominios
    context: Dict[str, Tuple[str, str]] = {
        "acentuacion": (f"{acento_pct:.0f}%" if acento_pct is not None else "N/A", _classify_domain(acento_pct)),
        "puntuacion": (f"{puntuacion_pct:.0f}%" if puntuacion_pct is not None else "N/A", _classify_domain(puntuacion_pct)),
        "mayusculas": (f"{mayus_pct:.0f}%" if mayus_pct is not None else "N/A", _classify_domain(mayus_pct)),
        "letras": (f"{letras_pct:.0f}%" if letras_pct is not None else "N/A", _classify_domain(letras_pct)),
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
    # Acentuación
    acento_res = Exercise2Result.objects.filter(user=user).order_by("-created_at").first()
    acento_pct = acento_res.percentage if acento_res else None
    # Puntuación
    punct_slugs = ["puntuacion1", "puntuacion2"]
    punct_mc_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=punct_slugs
    )
    punct_values: list[float] = [res.percentage for res in punct_mc_results]
    punct_final = PunctuationResult.objects.filter(user=user).order_by("-created_at").first()
    if punct_final:
        punct_values.append(punct_final.percentage)
    puntuacion_pct = _average_percentage(punct_values)
    # Mayúsculas
    mayus_slugs = ["mayus1", "mayus2"]
    mayus_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=mayus_slugs
    )
    mayus_values: list[float] = [res.percentage for res in mayus_results]
    mayus_pct = _average_percentage(mayus_values)
    # Letras
    letras_slugs = ["letras1", "letras2"]
    letras_results = MultipleChoiceResult.objects.filter(
        user=user, exercise_slug__in=letras_slugs
    )
    letras_values: list[float] = [res.percentage for res in letras_results]
    letras_pct = _average_percentage(letras_values)

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
        c.drawString(margin_x, info_y, f"Nombre: {user.nombre + " " + user.apellido or ""}")
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