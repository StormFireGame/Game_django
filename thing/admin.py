from django.contrib import admin
from thing.models import Thing

class ThingAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'is_art', 'is_bot', 'thumbnail', 
                    'level_need')
    ordering = ('name', 'level_need')
    list_filter = ('type', 'is_art', 'is_bot', 'level_need')
    search_fields = ('name',)
#    
    fieldsets = [
        ('General', {'fields': ['name', 'type', 'price', 'is_art', 'is_bot', 
                                'stability', 'weight', 'image', 
                                'level_need']}),                                           
        ('Parameters need', {'fields': ['strength_need', 'dexterity_need', 
                                        'intuition_need', 'health_need', 
                                        'swords_need', 'axes_need', 
                                        'knives_need', 'clubs_need',
                                        'shields_need'], 
                             'classes': ['collapse']}),                
        ('Parameters give', {'fields': ['strength_give', 'dexterity_give', 
                                        'intuition_give', 'health_give', 
                                        'swords_give', 'axes_give', 
                                        'knives_give', 'clubs_give', 
                                        'shields_give'], 
                             'classes': ['collapse']}),
        ('Other give', {'fields': ['damage_min', 'damage_max', 
                                   'protection_head', 'protection_breast', 
                                   'protection_zone', 'protection_legs', 
                                   'accuracy', 'dodge', 'devastate',
                                   'durability', 'block_break', 'armor_break', 
                                   'hp', 'time_duration', 'strike_count',
                                   'block_count', 'capacity', 
                                   'take_two_hands'], 
                        'classes': ['collapse']}),
    ]
    
admin.site.register(Thing, ThingAdmin)