
from main import models

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


class Schedule(models.Model):
    """Modèle pour les programmes de la radio"""
    DAY_CHOICES = [
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
        ('sunday', 'Dimanche'),
    ]
   
    day = models.CharField(max_length=20, choices=DAY_CHOICES, verbose_name="Jour")
    title = models.CharField(max_length=200, verbose_name="Titre du Programme")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    start_time = models.TimeField(verbose_name="Heure de Début")
    end_time = models.TimeField(verbose_name="Heure de Fin")
    host = models.CharField(max_length=100, blank=True, null=True, verbose_name="Animateur Principal")
    cohost = models.CharField(max_length=100, blank=True, null=True, verbose_name="Co-Animateur")
    guest = models.CharField(max_length=200, blank=True, null=True, verbose_name="Invité")
    color = models.CharField(max_length=7, blank=True, null=True, verbose_name="Couleur (hex)", help_text="Format: #4facfe")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"
        ordering = ['day', 'order', 'start_time']
   
    def __str__(self):
        return f"{self.get_day_display()} - {self.title} ({self.start_time} - {self.end_time})"