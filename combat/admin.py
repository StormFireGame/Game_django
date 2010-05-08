from django.contrib import admin
from combat.models import Combat, CombatHero, CombatLog

class CombatHeroInline(admin.TabularInline):
    model = CombatHero
    extra = 1

class CombatLogInline(admin.TabularInline):
    model = CombatLog
    extra = 1
        
class CombatAdmin(admin.ModelAdmin):
    inlines = [CombatHeroInline, CombatLogInline]
    list_display = ('type', 'is_active', 'with_things', 'start_date_time',)
    ordering = ('type', 'is_active',)
    list_filter = ('type', 'is_active', 'with_things',)
    search_fields = ('start_date_time',)
    
    #    
    fieldsets = [
        ('General',               {'fields': ['type', 'is_active', 'time_out', 
                                              'injury', 'with_things', 
                                              'location']}),
        ('Other',               {'fields': ['time_wait', 'one_team_count', 
                    'two_team_count', 'one_team_lvl_min', 'one_team_lvl_max', 
                    'two_team_lvl_min', 'two_team_lvl_max'], 
                                                    'classes': ['collapse']}),
    ]

admin.site.register(Combat, CombatAdmin)