from django.contrib import admin

# Register your models here.

from county.models import City, County, State


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


admin.site.register(City, CityAdmin)
admin.site.register(County)
admin.site.register(State)


