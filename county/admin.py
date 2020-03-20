from django.contrib import admin

# Register your models here.

from county.models import City, County, State, Email


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


admin.site.register(City, CityAdmin)
admin.site.register(County)
admin.site.register(State)
admin.site.register(Email)


