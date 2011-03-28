from django.contrib import admin
from building.module.shop.models import BuildingShopThing
           
class ShopThingAdmin(admin.ModelAdmin):
    list_display = ('building', 'thing', 'count', 'price',)
    ordering = ('building',)
    list_filter = ('building','thing',)
    search_fields = ('thing',)

admin.site.register(BuildingShopThing, ShopThingAdmin)