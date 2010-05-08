from django.contrib import admin
from island.models import Island, IslandPart

class IslandPartInline(admin.TabularInline):
    model = IslandPart
    extra = 1

class IslandAdmin(admin.ModelAdmin):
    inlines = [IslandPartInline]
    
admin.site.register(Island, IslandAdmin)