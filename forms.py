from django import forms

klasy = []

def ustawKlasy(kl):
    for k in kl:
        klasy.append(("kl",k))
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ClassesForm(forms.Form):
    kl = []
    klasa = forms.ChoiceField()
    def __init__(self, lista_klas):
         super().__init__()
         for l in lista_klas:
             self.kl.append((str(l),l))
         self.fields['klasa'].choices = self.kl

class AddMarkForm(forms.Form):
    uczen = forms.ChoiceField()
    oceny = [('1',1),('2',2),('3',3),('4',4),('5',5),('6',6)]
    stopien = forms.ChoiceField(choices=oceny)
    kategoria = forms.CharField()
    waga = forms.FloatField()
    opis = forms.CharField()
    lista = []
    def __init__(self, lista_uczniow):
        super().__init__()
        for l in lista_uczniow:
            self.lista.append((str(l.nr_dziennik),str(l.nr_dziennik)+" " + str(l.imie)+ " " + str(l.nazwisko)))
        self.fields['uczen'].choices = self.lista




