from django.contrib import admin
from tableexperience.models import TableExperience

class TableExperienceAdmin(admin.ModelAdmin):
    list_display = ('level', 'experience', 'number_of_abilities', 
                    'number_of_skills', 'number_of_parameters', 'money')
    ordering = ('level',)

admin.site.register(TableExperience, TableExperienceAdmin)