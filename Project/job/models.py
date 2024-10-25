from django.db import models

from core.models import City, Company, Position
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save
#Modalidad
class Mode(models.Model):
    description = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.description}"

#Habilidades
class Skills(models.Model):
    description = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.description}"
    

class Job(models.Model):
    title = models.CharField(max_length=30)
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, default='correo@gmail.com')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE)
    description = models.TextField(max_length=1500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f"{self.title}"



class VisitCounter(models.Model):
    count = models.IntegerField(default=0)
    last_reset = models.DateTimeField(auto_now=True)

    def increment(self):
        self.count += 1
        self.save()
        return self.count

class BrowserVisit(models.Model):
    browser_id = models.CharField(max_length=100)
    last_visit = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True)

    class Meta:
        unique_together = ('browser_id', 'ip_address')


class Postulacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ], default='pendiente')

    def __str__(self):
        return f"{self.usuario.username} - {self.job.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
     
    def __str__(self):
        return f"Profile of {self.user.username}"

# Signals para crear/actualizar el perfil automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()