from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .views import LibroViewSet

router = routers.DefaultRouter()
router.register(r'libros', LibroViewSet)


urlpatterns = [
    path('libros/', views.LibroListCreate.as_view()),
    path('libros/<int:pk>/', views.LibroDetail.as_view()),
    path('api/', include(router.urls)),
    path('inicio', views.inicio),
    path('Adm', views.administrador),
    path('AdmNuevo', views.nuevo),
    path('AdmRegistrar', views.registrar),
    path('AdmEdicion/<id>', views.edicion),
    path('AdmEditar/<id>', views.editar),
    path('AdmEliminacion/<id>', views.eliminacion),
    path('AdmEliminar/<id>', views.eliminar),
    path('Buscar', views.buscar),
    path('Alu', views.alumnos),
    path('AluNuevo', views.alumnos_nuevo),
    path('AluRegistrar', views.alumnos_registrar),
    path('AluEdicion/<id>', views.alumnos_edicion),
    path('AluEditar/<id>', views.alumnos_editar),
    path('AluEliminacion/<id>', views.alumnos_eliminacion),
    path('AluEliminar/<id>', views.alumnos_eliminar),
    path('AluBuscar', views.alumnos_buscar),
    path('Asi', views.asignatura),
    path('AsiNuevo', views.asignatura_nuevo),
    path('AsiRegistrar', views.asignatura_registrar),
    path('AsiEdicion/<id>', views.asignatura_edicion),
    path('AsiEditar/<id>', views.asignatura_editar),
    path('AsiEliminacion/<id>', views.asignatura_eliminacion),
    path('AsiEliminar/<id>', views.asignatura_eliminar),
    path('AsiBuscar', views.asignatura_buscar),
    path('Asis', views.asistencia),
    path('AsisNuevo', views.asistencia_nuevo),
    path('AsisRegistrar', views.asistencia_registrar),
    path('AsisEdicion/<id>', views.asistencia_edicion),
    path('AsisEditar/<id>', views.asistencia_editar),
    path('AsisEliminacion/<id>', views.asistencia_eliminacion),
    path('AsisEliminar/<id>', views.asistencia_eliminar),
    path('AsisBuscar', views.asistencia_buscar),
    path('Cat', views.categorias),
    path('CatNuevo', views.categorias_nuevo),
    path('CatRegistrar', views.categorias_registrar),
    path('CatEdicion/<id>', views.categorias_edicion),
    path('CatEditar/<id>', views.categorias_editar),
    path('CatEliminacion/<id>', views.categorias_eliminacion),
    path('CatEliminar/<id>', views.categorias_eliminar),
    path('CatBuscar', views.categorias_buscar),
    path('Not', views.nota),
    path('NotNuevo', views.nota_nuevo),
    path('NotRegistrar', views.nota_registrar),
    path('NotEdicion/<id>', views.nota_edicion),
    path('NotEditar/<id>', views.nota_editar),
    path('NotEliminacion/<id>', views.nota_eliminacion),
    path('NotEliminar/<id>', views.nota_eliminar),
    path('NotBuscar', views.nota_buscar),
    path('Sop', views.soporte),
    path('SopNuevo', views.soporte_nuevo),
    path('SopRegistrar', views.soporte_registrar),
    path('SopEdicion/<id>', views.soporte_edicion),
    path('SopEditar/<id>', views.soporte_editar),
    path('SopEliminacion/<id>', views.soporte_eliminacion),
    path('SopEliminar/<id>', views.soporte_eliminar),
    path('SopBuscar', views.soporte_buscar),
    path('Contacto', views.contacto),
    path('Acerca_de', views.acerca_de),
    ##################
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('lista/', views.lista_contenidos, name='lista_contenidos'),
    path('<int:id>/', views.detalle_contenido, name='detalle_contenido'),
    path('subir/', views.subir_contenido, name='subir_contenido'),
    path('guia', views.guia_ortografia, name='guia_ortografia'),
    path('vista_resultado', views.vista_resultado, name='vista_resultado'),
    path('menu-docente', views.menu_docente, name='menu_docente'),
    path('menu-estudiante', views.menu_estudiante, name='menu_estudiante'),
    path('guia_aprendizaje', views.guia_aprendizaje, name='guia_aprendizaje'),
    path('acento_final', views.acento_final, name='acento_final'),
    path("chat/", views.chat_with_openai, name="chat_openai"),
    path('api/', views.chat_con_gemini, name="chat_gemini"),
    path('gemini/', views.gemini_demo, name='gemini'),
    path("c/", views.chat_page, name="chat_page"),
    path('biblioteca/', views.biblioteca, name='biblioteca'),
    path('cargar/', views.cargar_libro, name='cargar_libro'),
    path('editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('acento_1', views.acento_1, name='acento_1'),
    path('acento_1_2', views.acento_1_2, name='acento_1_2'),
    path('', views.portal_selection, name='portal_selection'),
      
    path('login/docente/', views.login_docente, name='login_docente'),
    path('login/estudiante/', views.login_estudiante, name='login_estudiante'),
    path('register/docente/', views.register_docente, name='register_docente'),
    path('register/estudiante/', views.register_estudiante, name='register_estudiante'),
    path('reset/', views.reset_request, name='reset_request'),
    path('reset/verify/', views.reset_verify, name='reset_verify'),
    path("logout-docente/", views.logout_docente, name="logout_docente"),
    path("logout-estudiante/", views.logout_estudiante, name="logout_estudiante"),
     
    #######################
    #Ejercicio1 Acentuación
    path("acento_1/1/", views.exercise1, name="exercise1"),
    path("1/submit/", views.exercise1_submit, name="exercise1_submit"),

    path("acento_1/2/", views.exercise2, name="exercise2"),
    path("2/submit/", views.exercise2_submit, name="exercise2_submit"),

    path("acento_1/3/", views.exercise3, name="exercise3"),
    path("3/submit/", views.exercise3_submit, name="exercise3_submit"),

    path("acento_1/explicar/<int:attempt_id>/", views.explain_attempt, name="explain_attempt"),
    path("acento_1/resultados/", views.results_view, name="results"),
    
    path("evaluaciones/", views.evaluaciones, name="evaluaciones"),
    path("evaluaciones/report/", views.evaluaciones_report, name="evaluaciones_report")
   

    
]
