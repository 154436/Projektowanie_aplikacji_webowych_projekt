from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from enum import Enum

# Create your models here.
class Nauczyciel(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    haslo = models.TextField(max_length=100)
    nr_telefonu = models.IntegerField()

class Klasa(models.Model):
    id_wychowawcy = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=20)

class Uczen(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    adres_zamieszkania = models.CharField(max_length=150)
    pesel = models.IntegerField()
    email = models.CharField(max_length=50)
    haslo = models.TextField(max_length=100)
    klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE)

class Rodzic(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    haslo = models.TextField(max_length=100)
    nr_telefonu = models.IntegerField()

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
    kat_ocen = Enum('kat_ocen', ['sprawdzian','kartkówka','odpowiedz_ustna','aktywność','zadanie_domowe'])
    stopien = models.IntegerField()
    #kategoria = models.Choices(kat_ocen)
    opis = models.TextField(max_length=300)
    waga = models.IntegerField()
    data = models.DateField()
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE)
    przedmiot = models.ForeignKey(Klasa_Przedmiot, on_delete=models.CASCADE)



