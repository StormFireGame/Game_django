from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from hero.forms import LoginForm, RegistrationForm, SettingsForm
from hero.models import Hero, HeroSkill, HeroHeroSkill, HeroImage

from hero import heromanipulation

import hashlib

def main(request, template_name='main/main.html'):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try: 
                hero = Hero.objects.get(login=form.cleaned_data['login'],
                                        password=hashlib.sha1(
                                    form.cleaned_data['password']).hexdigest())
                request.session['hero_id'] = hero.id
                return HttpResponseRedirect(reverse('hero'))
            except Hero.DoesNotExist:
#
                request.user.message_set.create(
                                message='Hero doesn\'t exist')
    else:
        form = LoginForm()
        
    variables = RequestContext(request, {'form': form})
    
    return render_to_response(template_name, variables)

def registration(request, template_name='main/registration.html'):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            hero = Hero(login=form.cleaned_data['login'],
                        password=form.cleaned_data['password1'],
                        email=form.cleaned_data['email'],
                    date_of_birthday = form.cleaned_data['date_of_birthday'],
                        sex = form.cleaned_data['sex'])
            hero.save()
            request.session['hero_id'] = hero.id
            return HttpResponseRedirect(reverse('hero'))
    else:
        form = RegistrationForm()
        
    variables = RequestContext(request, {'form': form})
    
    return render_to_response(template_name, variables)

def _is_login(request):
    if 'hero_id' not in request.session:
        request.user.message_set.create(message='You have to log in')
        return HttpResponseRedirect('/')

def hero(request, template_name='hero/hero.html'):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    heroskills = HeroSkill.objects.all()
    
    variables = RequestContext(request, {'hero': hero, 
                                         'heroskills': heroskills})
    
    return render_to_response(template_name, variables)

def increase(request, type, what):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    if type == 'abilities' and hero.number_of_abilities > 0:
        hero.number_of_abilities -= 1
        if what == 'swords': hero.swords += 1
        elif what == 'axes': hero.axes += 1
        elif what == 'knives': hero.knives += 1
        elif what == 'clubs': hero.clubs += 1
        elif what == 'shields': hero.shields += 1
        
    if type == 'parameters' and hero.number_of_parameters > 0:
        hero.number_of_parameters -= 1
        if what == 'strength': hero.strength += 1
        elif what == 'dexterity': hero.dexterity += 1
        elif what == 'intuition': hero.intuition += 1
        elif what == 'health': hero.health += 1
    
    if type == 'skills' and hero.number_of_skills > 0:
        heroskill = get_object_or_404(HeroSkill, id=int(what))
        hero.number_of_skills -= 1
        try:
            heroskill = hero.heroheroskill_set.get(skill=heroskill)
            heroskill.level += 1
            heroskill.save()
        except HeroHeroSkill.DoesNotExist:
            HeroHeroSkill.objects.create(hero=hero, skill=heroskill, level=1)
            
    heromanipulation.hero_feature(hero)
    hero.save()
    
    return HttpResponseRedirect(reverse('hero'))

def settings(request, template_name='hero/settings.html'):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    heroimages = HeroImage.objects.filter(is_art=False, sex=hero.sex)
    
    if request.method == 'POST':
        form = SettingsForm(request.session['hero_id'], request.POST, 
                            instance=hero)
        if form.is_valid():
            if form.cleaned_data['password0'] \
                                            and form.cleaned_data['password2']:
                hero.password = form.cleaned_data['password2']
            form.save()       
            return HttpResponseRedirect(reverse('settings'))
    else:
        form = SettingsForm(request.session['hero_id'], instance=hero)
    
    variables = RequestContext(request, {'hero': hero, 
                                         'heroimages': heroimages,
                                         'form': form})
    
    return render_to_response(template_name, variables)    