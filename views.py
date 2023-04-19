from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

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
                    return HttpResponse('Zalogowano')
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

