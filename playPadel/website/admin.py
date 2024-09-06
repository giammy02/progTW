from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Users, UserAdmin)
admin.site.register(Impianto)
admin.site.register(Campo)
admin.site.register(Prenotazione)
admin.site.register(Partita)
admin.site.register(News)
