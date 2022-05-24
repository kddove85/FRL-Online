from django.contrib import admin
from .models import Station
from .models import ScheduledItem
from .models import Weekday

admin.site.register(Station)
admin.site.register(ScheduledItem)
admin.site.register(Weekday)
