from django.contrib import admin
from building.models import Building
           
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'plugin',)
    ordering = ('name',)
    list_filter = ('plugin',)
    search_fields = ('name',)
# 
    fieldsets = [
        ('General', {'fields': ['name', 'parent', 'plugin',]}),
        ('Coordinates', {'fields': ['coordinate_x1', 'coordinate_y1', 
                                    'coordinate_x2', 'coordinate_y2'], 
                         'classes': ['collapse']}),
    ]
    
admin.site.register(Building, BuildingAdmin)