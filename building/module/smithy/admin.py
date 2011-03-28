from django.contrib import admin
from building.module.smithy.models import BuildingSmithy, BuildingSmithyFeature

class BuildingSmithyFeatureInline(admin.TabularInline):
    model = BuildingSmithyFeature
    extra = 1

class BuildingSmithyAdmin(admin.ModelAdmin):
    list_display = ('building', 'percent_repair_money', 'percent_broken',)
    ordering = ('building',)
    search_fields = ('building',)
    inlines = [BuildingSmithyFeatureInline]

admin.site.register(BuildingSmithy, BuildingSmithyAdmin)