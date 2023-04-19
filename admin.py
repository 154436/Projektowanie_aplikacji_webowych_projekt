from django.contrib import admin
from .models import Rodzic, Uczen, Rodzic_Uczen, Nauczyciel, Klasa, Klasa_Przedmiot, Ocena, Przedmiot


# Register your models here.
admin.site.register(Rodzic)
admin.site.register(Uczen)
admin.site.register(Rodzic_Uczen)
admin.site.register(Nauczyciel)
admin.site.register(Klasa)
admin.site.register(Klasa_Przedmiot)
admin.site.register(Ocena)
admin.site.register(Przedmiot)
