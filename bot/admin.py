from django.contrib import admin
from bot.models import Bot, BotImage, BotThing

class BotImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail',)
 
admin.site.register(BotImage, BotImageAdmin)

class BotThingInline(admin.TabularInline):
    model = BotThing
    extra = 1

class BotAdmin(admin.ModelAdmin):
    inlines = [BotThingInline]
    list_display = ('name', 'level',)
    ordering = ('name',)
    list_filter = ('level',)
    search_fields = ('name',)
    
#    
    fieldsets = [
        ('General', {'fields': ['name', 'level', 'image',]}),
        ('Parameters', {'fields': ['hp', 'strength', 'dexterity', 
                                   'intuition', 'health', 'swords', 'axes', 
                                   'knives', 'clubs', 'shields', 
                                   'coordinate_x1', 'coordinate_y1', 
                                   'coordinate_x2', 'coordinate_y2', 
                                   'current_coordinate_x', 
                                   'current_coordinate_y',
                                   'in_combat'], 
                        'classes': ['collapse']}),
        #('Things', {'fields': ['things'], 'classes': ['collapse']}),
    ]

admin.site.register(Bot, BotAdmin)