from django.contrib import admin

# Register your models here.

from county.models import City, County, State

admin.site.register(City)
admin.site.register(County)
admin.site.register(State)
