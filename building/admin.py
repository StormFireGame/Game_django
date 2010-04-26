from django.contrib import admin
from building.models import Building
       
class BuildingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Building, BuildingAdmin)