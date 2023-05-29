from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    #path('',views.dashboard,name='dashboard'),
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    #path('login/main/', views.wyswietl_przedmioty_uczen, name='wyswietl_przedmioty_uczen'),
    path('login/main/', views.wyznacz_uzytkownika, name='wyznacz_uzytkownika'),
    path('login/main/add_marks/', views.dodaj_ocene, name='dodaj_ocene')
]