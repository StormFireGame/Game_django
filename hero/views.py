from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

from hero.forms import SettingsForm
from hero.models import HeroSkill, HeroHeroSkill, HeroImage, Thing, HeroThing

from hero.manipulation import hero_init, HeroM
from thing.manipulation import ThingM

# Hero
@hero_init
def hero(request, template_name='hero/hero.html'):
    heroskills = HeroSkill.objects.all()
    
    variables = RequestContext(request, {'heroskills': heroskills})

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
        try:
            heroskill = HeroSkill.objects.get(id=int(what))
        except HeroSkill.DoesNotExist:
            return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

        hero.number_of_skills -= 1
        try:
            heroskill = hero.heroheroskill_set.get(skill=heroskill)
            heroskill.level += 1
            heroskill.save()
        except HeroHeroSkill.DoesNotExist:
            HeroHeroSkill.objects.create(hero=hero, skill=heroskill, level=1)
            
    hero.save()
    HeroM(hero).update_feature()
    
    return HttpResponseRedirect(reverse('hero'))
# End hero

# Hero preferences
@hero_init
def preferences(request, template_name='hero/preferences.html'):
    
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
            return HttpResponseRedirect(reverse('hero_preferences'))
    else:
        form = SettingsForm(request.session['hero_id'], instance=hero)
    
    variables = RequestContext(request, {'heroimages': heroimages,
                                         'form': form})
    
    return render_to_response(template_name, variables) 
# End hero preferences

# Hero Inventory
@hero_init
def inventory(request, template_name='hero/inventory.html'):
    
    hero = request.hero
    herothings = hero.herothing_set.filter(dressed=False, away=False)
    
    variables = RequestContext(request, {'herothings': herothings})
    
    return render_to_response(template_name, variables)

@hero_init
def throw(request, herothing_id):
    
    hero = request.hero
    try:
        hero.herothing_set.get(id=herothing_id).delete()
    except HeroThing.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    HeroM(hero).update_capacity()
#
    messages.add_message(request, messages.SUCCESS, 'Your thing thrown.')
    return HttpResponseRedirect(reverse('hero_inventory'))

@hero_init
def dress(request, herothing_id):
    
    hero = request.hero

    try:
        herothing = hero.herothing_set.get(id=herothing_id)
    except HeroThing.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if not ThingM(herothing.thing, hero).is_available_to_dress():
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

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
                                                exclude(id=herothing_id).get()
            herothing.dressed = False
            herothing.save()
        except HeroThing.DoesNotExist:
            pass
    elif type == Thing.TYPE_RING:
        herothings = hero.herothing_set.filter(dressed=True,
                                               thing__type=type). \
                                                    exclude(id=herothing_id)
        if len(herothings) == settings.THINGS_COUNT_OF_RINGS:
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
                                                dressed=True).\
                                                    exclude(id=herothing_id)
        if len(herothings):
            if len(herothings) == settings.THINGS_COUNT_OF_ARMS or \
               herothings[0].thing.take_two_hands or take_two_hands:
                if take_two_hands:
                    for herothing in herothings:
                        herothing.dressed = False
                        herothing.save()
                else:
                    herothings[0].dressed = False
                    herothings[0].save()
        
    HeroM(hero).update_feature()
#
    messages.add_message(request, messages.SUCCESS, 'Thing dressed.')
    return HttpResponseRedirect(reverse('hero_inventory'))

@hero_init
def undress(request, herothing_id):

    hero = request.hero

    try:
        herothing = hero.herothing_set.get(id=herothing_id)
    except HeroThing.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    herothing.dressed = False
    herothing.save()

    HeroM(hero).update_feature()
#
    messages.add_message(request, messages.SUCCESS, 'Thing undressed.')
    return HttpResponseRedirect(reverse('hero_inventory'))

@hero_init
def undressall(request):

    hero = request.hero
    
    hero.herothing_set.update(dressed=False)
    
#
    messages.add_message(request, messages.SUCCESS, 'All things undressed.')
    return HttpResponseRedirect(reverse('hero_inventory'))
# End hero inventory