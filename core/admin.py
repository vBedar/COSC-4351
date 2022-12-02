from django.contrib import admin

# Register your models here.
from core.models import Table, Reservation

admin.site.register(Table)
admin.site.register(Reservation)