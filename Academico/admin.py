from django.contrib import admin

# Register your models here.
################
from .models import Materia, Contenido, Usuario, PasswordResetCode, Docente, Estudiante, Administrador
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ExerciseAttempt, ExplanationRequest, ActionLog, ResultSummary
#LOGIN


#############################

admin.site.register(Materia)
admin.site.register(Contenido)
@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    ordering = ['cedula']
    list_display = ('cedula','nombre','apellido','email','role','is_active','is_staff')
    fieldsets = (
        (None, {'fields': ('cedula','password')}),
        ('Información personal', {'fields': ('nombre','apellido','email','role')}),
        ('Permisos', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cedula','email','nombre','apellido','role','password1','password2'),
        }),
    )
    search_fields = ('cedula','email','nombre','apellido')

admin.site.register(PasswordResetCode)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Administrador)


#######################
#Ejercicio1 Acentuación
@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "run_id", "exercise_number", "is_correct", "score", "created_at")
    list_filter = ("exercise_number", "is_correct", "created_at")
    search_fields = ("user__username", "run_id")

@admin.register(ExplanationRequest)
class ExplanationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "attempt", "created_at")

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ("user", "run_id", "exercise_number", "action", "created_at")
    list_filter = ("exercise_number", "action")

@admin.register(ResultSummary)
class ResultSummaryAdmin(admin.ModelAdmin):
    list_display = ("user", "run_id", "percentage", "total_items", "correct_items", "created_at")
    search_fields = ("user__username", "run_id")
