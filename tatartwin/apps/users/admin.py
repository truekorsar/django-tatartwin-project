from django.contrib import admin
from .models import *


class TatarUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(TatarUser, TatarUserAdmin)
