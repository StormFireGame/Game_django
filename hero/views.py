from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q

from hero.forms import LoginForm, RegistrationForm, SettingsForm
from hero.models import Hero, HeroSkill, HeroHeroSkill, HeroImage, Thing, \
                        HeroThing

from hero.heromanipulation import hero_init, hero_feature, update_capacity

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
                messages.add_message(request, messages.ERROR, 
                                     'Hero doesn\'t exist.')
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

@hero_init
def hero(request, template_name='hero/hero.html'):
    
    heroskills = HeroSkill.objects.all()
    
    variables = RequestContext(request, {'hero': request.hero, 
                                         'heroskills': heroskills})

    return render_to_response(template_name, variables)

@hero_init
def increase(request, type, what):
    
    hero = request.hero
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
            
    hero.save()
    hero_feature(hero)
    
    return HttpResponseRedirect(reverse('hero'))

@hero_init
def settings(request, template_name='hero/settings.html'):
    
    hero = request.hero
    heroimages = HeroImage.objects.filter(is_art=False, sex=hero.sex)
    
    if request.method == 'POST':
        form = SettingsForm(request.session['hero_id'], request.POST, 
                            instance=hero)
        if form.is_valid():
            if form.cleaned_data['password0'] and \
                                                form.cleaned_data['password2']:
                hero.password = form.cleaned_data['password2']
            form.save()       
            return HttpResponseRedirect(reverse('hero_settings'))
    else:
        form = SettingsForm(request.session['hero_id'], instance=hero)
    
    variables = RequestContext(request, {'hero': hero, 
                                         'heroimages': heroimages,
                                         'form': form})
    
    return render_to_response(template_name, variables) 

#Inventory
@hero_init
def inventory(request, template_name='hero/inventory.html'):
    
    hero = request.hero
    herothings = hero.herothing_set.filter(dressed=False)
    
    variables = RequestContext(request, {'hero': hero,
                                         'herothings': herothings})
    
    return render_to_response(template_name, variables)

@hero_init
def throw(request, id):
    
    hero = request.hero
    hero.herothing_set.get(id=id).delete()

    update_capacity(hero)
#
    messages.add_message(request, messages.SUCCESS, 'Your thing thrown.')
    return HttpResponseRedirect(reverse('hero_inventory'))

##
@hero_init
def dress(request, id):
    
    hero = request.hero
    
    herothing = hero.herothing_set.get(id=id)    
    herothing.dressed = True
    herothing.save()
    
    type = herothing.thing.type
    take_two_hands = herothing.thing.take_two_hands
    
    if type == Thing.TYPE_HELMET or type == Thing.TYPE_KOLCHUGA or \
       type == Thing.TYPE_ARMOR or type == Thing.TYPE_BELT or \
       type == Thing.TYPE_PANTS or type == Thing.TYPE_TREETOP or \
       type == Thing.TYPE_GLOVE or type == Thing.TYPE_BOOT or \
       type == Thing.TYPE_AMULET:
        try:
            herothing = hero.herothing_set.filter(dressed=True, 
                                                  thing__type=type). \
                                                        exclude(id=id).get()
            herothing.dressed = False
            herothing.save()
        except HeroThing.DoesNotExist:
            pass
    elif type == Thing.TYPE_RING:
        herothings = hero.herothing_set.filter(dressed=True, 
                                               thing__type=type).exclude(id=id)
        if len(herothings) == 4:  
            herothings[0].dressed = False
            herothings[0].save()
    elif type == Thing.TYPE_SWORD or type == Thing.TYPE_AXE or \
         type == Thing.TYPE_KNIVE or type == Thing.TYPE_CLUBS or \
         type == Thing.TYPE_SHIELD:
        
        herothings = hero.herothing_set.filter(
                                            Q(thing__type=Thing.TYPE_SWORD) | 
                                               Q(thing__type=Thing.TYPE_AXE) |
                                            Q(thing__type=Thing.TYPE_KNIVE) |
                                            Q(thing__type=Thing.TYPE_CLUBS) |
                                            Q(thing__type=Thing.TYPE_SHIELD),
                                                dressed=True).exclude(id=id)
        if len(herothings):
            if len(herothings) == 2 or herothings[0].thing.take_two_hands or \
               take_two_hands:
                if take_two_hands:
                    for herothing in herothings:
                        herothing.dressed = False
                        herothing.save()
                else:
                    herothings[0].dressed = False
                    herothings[0].save()
        
    hero_feature(hero)  
#
    messages.add_message(request, messages.SUCCESS, 'Thing dressed.')
    return HttpResponseRedirect(reverse('hero_inventory'))

@hero_init
def undress(request, id):

    hero = request.hero
    
    herothing = hero.herothing_set.get(id=id)
    herothing.dressed = False
    herothing.save()

    #hero_feature(hero)
#
    messages.add_message(request, messages.SUCCESS, 'Thing undressed.')
    return HttpResponseRedirect(reverse('hero_inventory'))
#End