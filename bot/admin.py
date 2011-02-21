from django.contrib import admin
from bot.models import Bot, BotImage

class BotImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail',)
 
admin.site.register(BotImage, BotImageAdmin)

class BotAdmin(admin.ModelAdmin):
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
                                   'coordinate_x2', 'coordinate_y2'], 
                        'classes': ['collapse']}),
        ('Things', {'fields': ['things'], 'classes': ['collapse']}),
    ]

admin.site.register(Bot, BotAdmin)