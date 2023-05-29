from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ClassesForm(forms.Form):
    kl = []
    klasa = forms.ChoiceField()
    def __init__(self, lista_klas, przedmiot):
         super().__init__()
         for l, p in zip(lista_klas, przedmiot):
             self.kl.append((str(p)+":"+str(l),str(p)+" "+str(l)))
         self.fields['klasa'].choices = self.kl

class ChildrenForm(forms.Form):
    ch = []
    dziecko = forms.ChoiceField()
    def __init__(self, lista_dzieci):
         super().__init__()
         for l in lista_dzieci:
             self.ch.append((str(l.nr_dziennik)+":"+str(l.klasa.nazwa),str(l.imie)+" "+str(l.nazwisko)))
         self.fields['dziecko'].choices = self.ch
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




