from django.contrib import admin

# Register your models here.

from county.models import City, County, State, Email, Feedback


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


class CountyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'fips_code']


admin.site.register(Feedback)
admin.site.register(City, CityAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(State)
admin.site.register(Email)


