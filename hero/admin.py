from django.contrib import admin
from hero.models import HeroImage, Hero, HeroSkill, SkillFeature, \
                        HeroHeroSkill, HeroThing, HeroThingFeature
from django import forms

import re

class HeroHeroSkillInline(admin.TabularInline):
    model = HeroHeroSkill
    extra = 1

class HeroThingInline(admin.TabularInline):
    model = HeroThing
    extra = 1

class HeroAdminForm(forms.ModelForm):
    login = forms.CharField(min_length=3)
    password = forms.CharField(min_length=5, widget=forms.TextInput(
                                                            attrs={'size':50}))

    class Meta:
        model = Hero
   
    def clean_login(self):
        login = self.cleaned_data['login']
#
        if not re.search(r'^\w+$', login):
#
            raise forms.ValidationError('Login can only contain '
                                'alphanumeric characters and the underscore.')
        return login
            
class HeroAdmin(admin.ModelAdmin):
    inlines = [HeroHeroSkillInline, HeroThingInline]
    form = HeroAdminForm
    list_display = ('login', 'email', 'level', 'date_of_birthday', 'sex', 
                    'money')
    ordering = ('login',)
    list_filter = ('level', 'sex')
    search_fields = ('login', 'email')
   
#    
    fieldsets = [
        ('General',               {'fields': ['login', 'password', 'email',
                                              'date_of_birthday', 'sex']}),
        ('Parameters',               {'fields': ['experience', 'money', 
                    'money_art', 'location', 'level', 'image',
                    'number_of_wins', 'number_of_losses', 'number_of_draws',
                    'hp', 'strength', 'dexterity', 'intuition', 'health',
                    'swords', 'axes', 'knives', 'clubs', 'shields', 
                    'number_of_abilities', 'number_of_skills',
                    'number_of_parameters'], 
                                                    'classes': ['collapse']}),
        ('About hero', {'fields': ['country', 'city', 'name', 'about'], 
                                                    'classes': ['collapse']}),
    ]

admin.site.register(Hero, HeroAdmin)

class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'is_art')
    list_filter = ('is_art',)

admin.site.register(HeroImage, HeroImageAdmin)

class SkillFeatureInline(admin.TabularInline):
    model = SkillFeature
    extra = 1

class HeroSkillAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [SkillFeatureInline]

admin.site.register(HeroSkill, HeroSkillAdmin)

class HeroThingFeatureAdmin(admin.ModelAdmin):
    list_display = ('hero', 'thing', 'feature', 'plus')
    search_fields = ('hero',)
    
admin.site.register(HeroThingFeature, HeroThingFeatureAdmin)
