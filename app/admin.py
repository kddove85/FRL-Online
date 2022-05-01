from django.contrib import admin
from .models import Station
from .models import ScheduledItem

admin.site.register(Station)
admin.site.register(ScheduledItem)
