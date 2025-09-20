from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Docente, Estudiante

@receiver(post_save, sender=Usuario)
def sync_profiles_from_user(sender, instance: Usuario, **kwargs):
    data = dict(cedula=instance.cedula, nombre=instance.nombre, apellido=instance.apellido)
    if hasattr(instance, 'docente'):
        Docente.objects.filter(user=instance).update(**data)
    if hasattr(instance, 'estudiante'):
        Estudiante.objects.filter(user=instance).update(**data)
