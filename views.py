from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, ClassesForm, AddMarkForm
from django.contrib.auth.decorators import login_required
from .models import Uczen, Przedmiot, Klasa_Przedmiot, Ocena, Klasa, Nauczyciel, Rodzic, Rodzic_Uczen
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.forms import ChoiceField

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            #sprawdza dane użytkownika i zwraca jego obiekt
            user = authenticate(username=clean_data['username'], password=clean_data['password'])

            if user is not None:
                if user.is_active:
                    #umieszcza użytkownika w sesji
                    login(request, user)
                    return redirect('main/')
                    #return HttpResponse('Zalogowano')
                else:
                    return HttpResponse('Konto zablokowane')
            else:
                return HttpResponse("Nieprawidłowe dane")
    else:
        form = LoginForm()
    return render(request,'dziennik/login.html',{'form': form})

@login_required
def dashboard(request):
    return render(request,'dziennik/dashboard.html',{'section':'dashboard'})

def uczen_pobierz_oceny(request, subject):
    user = request.user
    id_student = Uczen.objects.get(user=user)
    oceny = uczen_pobierz_oceny(id_student.nr_dziennik, id_student.klasa.nazwa, subject)
    return oceny

def uczen_pobierz_oceny(id_student_class, class_name, subject):
    id_class = Klasa.objects.get(nazwa=class_name)
    id_student = Uczen.objects.get(nr_dziennik=id_student_class, klasa=id_class)
    id_subject = Przedmiot.objects.get(nazwa=subject)
    id_subject_class = Klasa_Przedmiot.objects.get(klasa=id_class, przedmiot=id_subject)
    oceny = Ocena.objects.filter(uczen=id_student, przedmiot=id_subject_class)
    return oceny

def pobierz_uczniow(class_name):
    id_class = Klasa.objects.get(nazwa=class_name)
    students = Uczen.objects.filter(klasa=id_class)
    return students

def wyznacz_uzytkownika(request):
    user = request.user
    try:
        id_student = Uczen.objects.get(user=user)
        return wyswietl_przedmioty_uczen(request)
    except Uczen.DoesNotExist:
        pass
    try:
        id_nauczyciel = Nauczyciel.objects.get(user=user)
        return wyswietl_przedmioty_nauczyciel(request)
    except Nauczyciel.DoesNotExist:
        pass
    try:
        parent = Rodzic.objects.get(user=user)
        return wyswietl_dzieci_rodzica(request)
    except Rodzic.DoesNotExist:
        return HttpResponse("Nieprawidlowo utworzony uzytkownik")



def wyswietl_przedmioty_uczen(request):
    user = request.user
    id_student = Uczen.objects.get(user=user)
    subjects = Klasa_Przedmiot.objects.filter(klasa=id_student.klasa)
    sub = []
    oceny = []
    sub_srednia = []
    for s in subjects:
        sub.append(s.przedmiot)
        o = uczen_pobierz_oceny(id_student.nr_dziennik, id_student.klasa.nazwa, s.przedmiot.nazwa)
        oceny.append(o)
        sub_srednia.append(oblicz_srednia_jeden(id_student.nr_dziennik, id_student.klasa.nazwa, s.przedmiot.nazwa))
    all_sub = zip(sub, oceny, sub_srednia)
    srednia = oblicz_srednia_wszystkie(id_student.nr_dziennik, id_student.klasa.nazwa)
    return render(request,'dziennik/subjects/subjects.html',{'uczen': id_student, 'all': all_sub, 'srednia': srednia}) #, 'user': user, 'uczen': id_student.klasa.nazwa})
@csrf_exempt
def wyswietl_przedmioty_nauczyciel(request):
    if request.method == 'POST':
        print(request.POST)
        form2 = ClassesForm(request.POST)
        klasa = dict(form2.fields['klasa'].choices)
        klasa = request.POST['klasa']
        return oceny_klasy(request, klasa, "Matematyka")

    user = request.user
    teacher = Nauczyciel.objects.get(user=user)
    subjects = Klasa_Przedmiot.objects.filter(nauczyciel=teacher)
    sub = []
    kl = []
    for s in subjects:
        sub.append(s.przedmiot)
        kl.append(s.klasa.nazwa)
    all = zip(sub, kl)
    form = ClassesForm(kl)
    #form = ChoiceField(choices = klas)
    return render(request,'dziennik/subjects/classes.html',{'nauczyciel': teacher, 'all': all, 'form': form})

def wyswietl_przedmioty_dzieci(id):
    id_student = Uczen.objects.get(id=id)
    subjects = Klasa_Przedmiot.objects.filter(klasa=id_student.klasa)
    return subjects

def wyswietl_dzieci_rodzica(request):
    user = request.user
    parent = Rodzic.objects.get(user=user)
    dzieci = Rodzic_Uczen.objects.filter(rodzic=parent)
    return dzieci.uczen

def wstaw_ocene(degree, cat, desc, weight, id_student_class, class_name, subject):
    id_class = Klasa.objects.get(nazwa=class_name)
    id_student = Uczen.objects.get(nr_dziennik=id_student_class, klasa=id_class)
    id_subject = Przedmiot.objects.get(nazwa=subject)
    id_subject_class = Klasa_Przedmiot.objects.get(klasa=id_class, przedmiot=id_subject)
    date = datetime.today()
    new_o = Ocena(stopien=degree, kategoria=cat, opis=desc, waga=weight, data=date, uczen=id_student, przedmiot=id_subject_class)
    new_o.save()

def dodaj_ocene(request):
    if 'klasa' in request.session:
        klasa = request.session['klasa']
    if 'przedmiot' in request.session:
        przedmiot = request.session['przedmiot']
    if request.method == 'POST':
        print(request.POST)
        stopien = request.POST['stopien']
        kategoria = request.POST['kategoria']
        opis = request.POST['opis']
        waga = request.POST['waga']
        uczen = request.POST['uczen']
        wstaw_ocene(stopien,kategoria,opis,waga,uczen,klasa,przedmiot)
        return HttpResponse("Dodano")

    uczniowie = pobierz_uczniow(klasa)
    form = AddMarkForm(uczniowie)
    return render(request, 'dziennik/subjects/add_marks.html', {'form': form})#, {'nauczyciel': teacher, 'all': all,)
def aktualizuj_ocene(id, degree, cat, desc, weight):
    ocena = Ocena.objects.get(id=id)
    ocena.kategoria = cat
    ocena.opis = desc
    ocena.data = datetime.today()
    ocena.stopien = degree
    ocena.waga = weight
    ocena.save()
def usun_ocene(id):
    ocena = Ocena.objects.get(id=id)
    ocena.delete()
def oceny_klasy(request, class_name, subject):
    students = pobierz_uczniow(class_name)
    request.session['klasa'] = class_name
    request.session['przedmiot'] = subject
    oceny=[]
    for student in students:
        oceny.append(uczen_pobierz_oceny(student.nr_dziennik, class_name, subject))
    all = zip(students, oceny)
    return render(request,'dziennik/subjects/class_marks.html',{'all': all, 'klasa': class_name})
def oblicz_srednia_jeden(id_student_class, class_name, subject):
    oceny = uczen_pobierz_oceny(id_student_class, class_name, subject)
    suma = 0
    if len(oceny) > 0:
        for ocena in oceny:
            suma = suma + int(ocena.stopien)
        return suma/len(oceny)
    return None

def oblicz_srednia_wszystkie(id_student_class, class_name):
    id_class = Klasa.objects.get(nazwa=class_name)
    subjects = Klasa_Przedmiot.objects.filter(klasa=id_class)
    suma = 0
    licz_przedmiot = 0
    for sub in subjects:
        wynik = oblicz_srednia_jeden(id_student_class, class_name, sub.przedmiot.nazwa)
        if wynik != None:
            suma = suma + wynik
            licz_przedmiot = licz_przedmiot + 1
    if licz_przedmiot > 0:
        return suma/licz_przedmiot
    else:
        return None

def oblicz_srednia_klasy(class_name):
    students = pobierz_uczniow(class_name)
    suma = 0
    for student in students:
        suma = suma + oblicz_srednia_wszystkie(student.nr_dziennik, class_name)
    return suma/len(students)





