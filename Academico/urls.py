from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .views import LibroViewSet
from . import views_evaluaciones

router = routers.DefaultRouter()
router.register(r'libros', LibroViewSet)


urlpatterns = [
    path('libros/', views.LibroListCreate.as_view()),
    path('libros/<int:pk>/', views.LibroDetail.as_view()),
    path('api/', include(router.urls)),
    path('inicio', views.inicio),
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
    path('menu-administrador', views.menu_administrador, name='menu_administrador'),
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
    path('login/administrador/', views.login_administrador, name='login_administrador'),
    path('register/docente/', views.register_docente, name='register_docente'),
    path('register/estudiante/', views.register_estudiante, name='register_estudiante'),
    path('register/administrador/', views.register_administrador, name='register_administrador'),
    path('reset/', views.reset_request, name='reset_request'),
    path('reset/verify/', views.reset_verify, name='reset_verify'),
    path("logout-docente/", views.logout_docente, name="logout_docente"),
    path("logout-estudiante/", views.logout_estudiante, name="logout_estudiante"),
    path("logout-administrador/", views.logout_administrador, name="logout_administrador"),
     
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
    
    
    #######################
    # Ejercicio2 Acentuación
    path("acento_2/1/", views.exercise2_question1, name="exercise2"),
    path("acento_2/1/submit/", views.exercise2_question1_submit, name="exercise2_question1_submit"),
    path("acento_2/2/", views.exercise2_question2, name="exercise2_question2"),
    path("acento_2/2/submit/", views.exercise2_question2_submit, name="exercise2_question2_submit"),
    path("acento_2/3/", views.exercise2_question3, name="exercise2_question3"),
    path("acento_2/3/submit/", views.exercise2_question3_submit, name="exercise2_question3_submit"),
    path("acento_2/explicar/", views.explain_attempt2, name="explain_attempt2"),
    path("acento_2/resultados/", views.results_view2, name="results2"),
    
    #######################
    # Ejercicio final de puntuación
    path("puntuacion/", views.punctuation_exercise, name="punctuation_final"),
    path("puntuacion/submit/", views.punctuation_submit, name="punctuation_submit"),
    path("puntuacion/explicar/", views.punctuation_explain, name="punctuation_explain"),
    path("puntuacion/resultado/", views.punctuation_result, name="punctuation_result"),

    
    #path("evaluaciones/", views.evaluaciones, name="evaluaciones"),
    #path("evaluaciones/report/", views.evaluaciones_report, name="evaluaciones_report"),
    
    # Reporte de evaluaciones: se utiliza la vista genérica de reportes
    path("evaluaciones/", views_evaluaciones.evaluaciones_view, name="evaluaciones"),
    path("evaluaciones/report/", views_evaluaciones.evaluaciones_report, name="evaluaciones_report"),
    
    # Evaluaciones para docentes: tabla con resultados de todos los estudiantes
    path("evaluaciones/docente/", views_evaluaciones.evaluaciones_docente_view, name="evaluaciones_docente"),
    path("evaluaciones/docente/report/", views_evaluaciones.evaluaciones_docente_report, name="evaluaciones_docente_report"),   
    
    path("calendario/", views.calendario, name="calendario"),
    path("calendario/events/", views.calendario_events, name="calendario_events"),
    path("calendario/detalle/", views.calendario_detalle, name="calendario_detalle"),
    
    # Perfil del estudiante
    path("perfil_estudiante/", views.perfil_estudiante, name="perfil_estudiante"),
    # Perfil del docente
    path('perfil-docente/', views.perfil_docente, name='perfil_docente'),
      # Perfil del administrador
    path('perfil-administrador/', views.perfil_administrador, name='perfil_administrador'),
    
    #######################
    # Ejercicios de opción múltiple genéricos (puntuación, mayúsculas y letras)
    # Se utilizan rutas dinámicas basadas en el identificador del ejercicio
    # (p.ej. 'puntuacion1', 'mayus2', 'letras1') y el número de pregunta.
    path("mc/explain/", views.mc_explain, name="mc_explain"),
    path("mc/<slug:slug>/<int:qnum>/submit/", views.mc_submit_view, name="mc_submit"),
    path("mc/<slug:slug>/<int:qnum>/", views.mc_question_view, name="mc_question"),
    path("mc/<slug:slug>/result/", views.mc_result_view, name="mc_result"),
    
    #Instrucciones para los ejercicios de opción múltiple
    path('instruccion/<slug:unit_slug>/',views.instruccion_view, name='instruccion'),
    
    #######################
    # Rutas para la encuesta de opinión Estudiante
    path("encuesta/<int:qnum>/", views.survey_question_view, name="survey_question"),
    path("encuesta/<int:qnum>/submit/", views.survey_submit_view, name="survey_submit"),
    path("encuesta/result/", views.survey_result_view, name="survey_result"),
    
    # Rutas para la encuesta de opinión Docente
    path("encuesta_docente/<int:qnum>/", views.survey_question_view_docente, name="survey_question_docente"),
    path("encuesta_docente/<int:qnum>/submit/", views.survey_submit_view_docente, name="survey_submit_docente"),
    path("encuesta_docente/result/", views.survey_result_view_docente, name="survey_result_docente"),
    
    path('acento_1/reiniciar/', views.reiniciar_acento, name='reiniciar_acento'),
    path('mc/<slug:slug>/reiniciar/', views.reiniciar_mc, name='reiniciar_mc'),
    
    path("encuesta/cancel/", views.survey_cancel, name="survey_cancel"),
    path("encuesta_docente/cancel/", views.survey_cancel_docente, name="survey_cancel_docente"),


]

urlpatterns += [
    # Gestión de educandos (CRUD) para docentes
    path("evaluaciones/docente/educandos/crear/", views_evaluaciones.educando_create, name="educando_create"),
    path("evaluaciones/docente/educandos/<int:user_id>/editar/", views_evaluaciones.educando_edit, name="educando_edit"),
    path("evaluaciones/docente/educandos/<int:user_id>/eliminar/", views_evaluaciones.educando_delete, name="educando_delete"),
    path('docente/evaluaciones/<int:user_id>/report/', views_evaluaciones.evaluaciones_docente_individual_report,
         name='evaluaciones_docente_individual_report'),
    
    # Gestión de usuarios (CRUD) para administradores
    path("evaluaciones/administrador/", views_evaluaciones.evaluaciones_administrador_view, name="evaluaciones_admin"),
    path("evaluaciones/administrador/report/", views_evaluaciones.evaluaciones_administrador_report, name="evaluaciones_administrador_report"),  # ← NUEVO
    path("usuarios/create/", views_evaluaciones.usuario_create, name="usuario_create"),
    path("usuarios/<int:pk>/edit/", views_evaluaciones.usuario_edit, name="usuario_edit"),
    path("usuarios/<int:pk>/delete/", views_evaluaciones.usuario_delete, name="usuario_delete"),
    path('administrador/evaluaciones/<int:user_id>/report/', views_evaluaciones.evaluaciones_administrador_individual_report,
         name='evaluaciones_administrador_individual_report'),
]

urlpatterns += [
    # Banco por unidad (Docente)
    path("docente/banco/<slug:unit>/", views.banco_list, name="banco_list"),
    path("docente/banco/<slug:unit>/crear/", views.banco_create, name="banco_create"),
    path("docente/banco/<slug:unit>/<int:pk>/editar/", views.banco_edit, name="banco_edit"),
    path("docente/banco/<slug:unit>/<int:pk>/eliminar/", views.banco_delete, name="banco_delete"),
]
