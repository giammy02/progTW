from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    foto = models.ImageField(upload_to='profile_pics', blank=True, null=False, default='profile_pics/default_profile_pic.png')

    class Meta:
        verbose_name_plural = 'Utenti'


class Impianto(models.Model):
    gestore = models.ForeignKey(Users, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(blank=False, null=False, unique=True)
    foto = models.ImageField(upload_to='media', blank=True, null=False, default='media/default_impianto_photo.jpg')
    numero_campi = models.IntegerField(blank=False, null=False)
    posizione = models.CharField(max_length=255, blank=False, null=False)
    orari = models.CharField(max_length=255)
    prezzi = models.CharField(max_length=100)
    contatti = models.CharField(max_length=100)
    caratteristiche = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Impianti'


class Campo(models.Model):
    numero = models.IntegerField(blank=False, null=False)
    tipologia = models.CharField(max_length=50, blank=False, null=False)
    impianto = models.ForeignKey(Impianto, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Campi'


class Prenotazione(models.Model):
    cliente = models.ForeignKey(Users, on_delete=models.CASCADE)
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    impianto = models.ForeignKey(Impianto, on_delete=models.CASCADE)
    data = models.DateField(blank=False, null=False, verbose_name='')
    ora_inizio = models.TimeField(blank=False, null=False)
    ora_fine = models.TimeField(blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Prenotazioni'


class Partita(models.Model):
    prenotazione = models.ForeignKey(Prenotazione, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Users, on_delete=models.CASCADE)
    risultato = models.CharField(max_length=50)
    giocatori = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Partite'


class News(models.Model):
    gestore = models.ForeignKey(Users, on_delete=models.CASCADE)
    impianto = models.ForeignKey(Impianto, on_delete=models.CASCADE)
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=501)
    data = models.DateField(blank=False, null=False, default=timezone.now)

    class Meta:
        verbose_name_plural = 'News'
