from django.contrib import admin
from building.module.commission.models import BuildingCommission, \
                                              BuildingCommissionHeroThing
           
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('building', 'percent',)
    ordering = ('building',)
    list_filter = ('building',)

admin.site.register(BuildingCommission, CommissionAdmin)

class CommissionHeroThingAdmin(admin.ModelAdmin):
    list_display = ('building', 'herothing', 'price',)
    ordering = ('building',)
    list_filter = ('building',)
    search_fields = ('thing', 'hero',)

admin.site.register(BuildingCommissionHeroThing, CommissionHeroThingAdmin)