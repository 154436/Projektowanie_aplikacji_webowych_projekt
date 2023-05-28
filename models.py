from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Nauczyciel(models.Model):
    imie = models.CharField(max_length=50,default='test')
    nazwisko = models.CharField(max_length=50,default='test')
    email = models.CharField(max_length=50,default='test')
    haslo = models.TextField(max_length=100,default='test')
    nr_telefonu = models.IntegerField(default=1)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)

class Klasa(models.Model):
    id_wychowawcy = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=20)

class Uczen(models.Model):
    imie = models.CharField(max_length=50,default='test')
    nazwisko = models.CharField(max_length=50,default='test')
    adres_zamieszkania = models.CharField(max_length=150,default='test')
    pesel = models.IntegerField(default=1)
    email = models.CharField(max_length=50,default='test')
    haslo = models.TextField(max_length=100,default='test')
    klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE,default=1)
    nr_dziennik = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

class Rodzic(models.Model):
    imie = models.CharField(max_length=50,default='test')
    nazwisko = models.CharField(max_length=50,default='test')
    email = models.EmailField(max_length=50,default='test')
    haslo = models.TextField(max_length=100,default='test')
    nr_telefonu = models.IntegerField(default='1234')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


class Rodzic_Uczen(models.Model):
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE)
    rodzic = models.ForeignKey(Rodzic, on_delete=models.CASCADE)

class Przedmiot(models.Model):
    nazwa = models.TextField(max_length=100)
    opis = models.TextField(max_length=300)


class Klasa_Przedmiot(models.Model):
    klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE)
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE)
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE)

class Ocena(models.Model):
    stopien = models.IntegerField()
    kategoria = models.TextField(max_length=30,default='sprawdzian')
    opis = models.TextField(max_length=300)
    waga = models.IntegerField()
    data = models.DateField()
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE)
    przedmiot = models.ForeignKey(Klasa_Przedmiot, on_delete=models.CASCADE)



