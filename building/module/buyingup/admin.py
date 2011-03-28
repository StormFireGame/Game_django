from django.contrib import admin
from building.module.buyingup.models import BuildingBuyingup
           
class BuyingupAdmin(admin.ModelAdmin):
    list_display = ('building', 'percent',)
    ordering = ('building',)
    list_filter = ('building',)

admin.site.register(BuildingBuyingup, BuyingupAdmin)