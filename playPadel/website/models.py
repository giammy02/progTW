from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    is_cliente = models.BooleanField('cliente status', default=False)


class Cliente(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    foto = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Clienti'


class Gestore(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    foto = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Gestori'


class Impianto(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(null=False, unique=True, default=slugify(nome))
    foto = models.ImageField(upload_to='media/profile_pics', blank=True, null=True)
    numero_campi = models.IntegerField(blank=False, null=False)
    posizione = models.CharField(max_length=255, blank=False, null=False)
    orari = models.CharField(max_length=255)
    prezzi = models.CharField(max_length=100)
    contatti = models.CharField(max_length=100)
    caratteristiche = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Impianti'


class Campo(models.Model):
    tipologia = models.CharField(max_length=50, blank=False, null=False)
    impianto = models.ForeignKey(Impianto, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Campi'


class Prenotazione(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    impianto = models.ForeignKey(Impianto, on_delete=models.CASCADE)
    data = models.DateField(blank=False, null=False)
    ora_inizio = models.TimeField(blank=False, null=False)
    ora_fine = models.TimeField(blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Prenotazioni'


class Partita(models.Model):
    prenotazione = models.ForeignKey(Prenotazione, on_delete=models.CASCADE)
    risultato = models.CharField(max_length=50)
    giocatori = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Partite'


class News(models.Model):
    gestore = models.ForeignKey(Gestore, on_delete=models.CASCADE)
    impianto = models.ForeignKey(Impianto, on_delete=models.CASCADE)
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=501)

    class Meta:
        verbose_name_plural = 'News'
