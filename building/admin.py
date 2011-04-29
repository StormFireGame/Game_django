from django.contrib import admin
from building.models import Building
           
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'module', 'thumbnail',)
    ordering = ('name',)
    list_filter = ('module',)
    search_fields = ('name',)
# 
    fieldsets = [
        ('General', {'fields': ['name', 'slug', 'island', 'parent',
                                'default_child', 'module', 'image']}),
        ('Coordinates', {'fields': ['coordinate_x1', 'coordinate_y1', 
                                    'coordinate_x2', 'coordinate_y2'], 
                         'classes': ['collapse']}),
    ]
    prepopulated_fields = {'slug':('name',),}

admin.site.register(Building, BuildingAdmin)