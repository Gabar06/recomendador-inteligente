from django.apps import AppConfig


class AcademicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Academico'
    
    def ready(self):
        import Academico.signals  # noqa