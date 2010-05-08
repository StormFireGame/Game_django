from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from hero.views import _is_login

from hero.models import Hero
from combat.models import Combat, CombatHero

from combat.forms import DuelForm, GroupForm, ChaoticForm

from combat import combatmanipulation

def combat(request, type, template_name='combat/combat.html'):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    in_combat = combatmanipulation.in_combat(hero)
    
    is_active = 0
    form = False
    is_cancel = is_fight = is_refuse = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero) != False
        if type == '0':
            is_fight = combatmanipulation.is_fight(hero)
            is_refuse = combatmanipulation.is_refuse(hero)      
        else:
            combatmanipulation.is_combat(hero)
    
    if type == '0':        
        if request.method == 'POST' and not in_combat:
            form = DuelForm(request.POST)
            if form.is_valid():
                combat = Combat(time_out=form.cleaned_data['time_out'],
                                injury=form.cleaned_data['injury'],
                                with_things=form.cleaned_data['with_things'],
                                location=combatmanipulation.get_location(
                                                                hero.location),
                                one_team_count = 1, two_team_count = 1)
                combat.save()
                combat.combathero_set.create(hero=hero)
    #
                request.user.message_set.create(
                                    message='Your demand accept')
                return HttpResponseRedirect(reverse('combat', args=[type]))
        else:
            form = DuelForm()
    elif type == '1':       
        if request.method == 'POST' and not in_combat:
            form = GroupForm(request.POST)
            if form.is_valid():
                combat = Combat(type=type,
                                time_out=form.cleaned_data['time_out'],
                                injury=form.cleaned_data['injury'],
                                with_things=form.cleaned_data['with_things'],
                                time_wait=form.cleaned_data['time_wait'],
                                location=combatmanipulation.get_location(
                                                                hero.location),
                        one_team_count = form.cleaned_data['one_team_count'],
                        two_team_count = form.cleaned_data['two_team_count'],
                    one_team_lvl_min = form.cleaned_data['one_team_lvl_min'],
                    one_team_lvl_max = form.cleaned_data['one_team_lvl_max'],
                    two_team_lvl_min = form.cleaned_data['two_team_lvl_min'],
                    two_team_lvl_max = form.cleaned_data['two_team_lvl_max'])
                
                combat.save()
                combat.combathero_set.create(hero=hero)
    #
                request.user.message_set.create(message='Your demand accept')
                return HttpResponseRedirect(reverse('combat', args=[type]))
        else:
            form = GroupForm()
    elif type == '2':       
        if request.method == 'POST' and not in_combat:
            form = ChaoticForm(request.POST)
            if form.is_valid():
                combat = Combat(type=type,
                                time_out=form.cleaned_data['time_out'],
                                injury=form.cleaned_data['injury'],
                                with_things=form.cleaned_data['with_things'],
                                time_wait=form.cleaned_data['time_wait'],
                                location=combatmanipulation.get_location(
                                                                hero.location),
                                one_team_count = form.cleaned_data['count'],
                                one_team_lvl_min = form.cleaned_data['lvl_min'],
                                one_team_lvl_max = form.cleaned_data['lvl_max'])
                
                combat.save()
                combat.combathero_set.create(hero=hero)
    #
                request.user.message_set.create(message='Your demand accept')
                return HttpResponseRedirect(reverse('combat', args=[type]))
        else:
            form = ChaoticForm()    
    elif type == '4':
        is_active = 1
    elif type == '5':
        pass
    
    combats = Combat.objects.filter(type=type, is_active=is_active, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'type': int(type),
                                         'hero': hero, 
                                         'form': form,
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel,
                                         'is_fight': is_fight,
                                         'is_refuse': is_refuse,})
    
    return render_to_response(template_name, variables)

def cancel(request):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    
    combat = combatmanipulation.is_cancel(hero)
    
    if combat != False:
        type = combat.type
        combat.delete()
#
        request.user.message_set.create(message='Your demand cancel')
        return HttpResponseRedirect(reverse('combat', args=[type]))
    else:
        return HttpResponseRedirect(reverse('combat', args=[0]))     

def accept(request, id, team):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    in_combat = combatmanipulation.in_combat(hero)
    
    if not in_combat:
        combat = get_object_or_404(Combat, id=id)
        
        if team == '0':
            team_count = combat.one_team_count
            team_lvl_min = combat.one_team_lvl_min
            team_lvl_max = combat.one_team_lvl_max
        else:
            team_count = combat.two_team_count
            team_lvl_min = combat.two_team_lvl_min
            team_lvl_max = combat.two_team_lvl_max
        
        team_count_now = combat.combathero_set.filter(team=team).count()
        
        if hero.level >= team_lvl_min and hero.level <= team_lvl_max \
           and team_count_now < team_count:
            combat.combathero_set.create(hero=hero, team=team)
#
            request.user.message_set.create(message='Demand accept')
        else:
#
            request.user.message_set.create(message='Demand accept until you')
        return HttpResponseRedirect(reverse('combat', args=[combat.type]))
    
    return HttpResponseRedirect(reverse('combat', args=[0]))

def refuse(request):
    _is_login(request)
    
    hero = Hero.objects.get(id=request.session['hero_id'])
    
    combat = combatmanipulation.is_refuse(hero)
    
    if combat != False:
        combat.combathero_set.get(team=1).delete()
#
        request.user.message_set.create(message='Demand refuse') 
    return HttpResponseRedirect(reverse('combat', args=[0]))