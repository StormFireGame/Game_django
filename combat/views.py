from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from hero.models import Hero
from combat.models import Combat, CombatHero, CombatLog, TYPES

from combat.forms import DuelForm, GroupForm, ChaoticForm, CombatForm

from combat import combatmanipulation
from hero import heromanipulation

def combat_duel(request, template_name='combat/duel.html'):
    
    hero = heromanipulation.hero_init(request)
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = is_fight = is_refuse = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero) != False
        is_fight = combatmanipulation.is_fight(hero)
        is_refuse = combatmanipulation.is_refuse(hero)
    
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
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_duel'))
    else:
        form = DuelForm()
    
    combats = Combat.objects.filter(type=0, is_active=0, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'form': form,
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel,
                                         'is_fight': is_fight,
                                         'is_refuse': is_refuse})
    
    return render_to_response(template_name, variables)

def combat_group(request, template_name='combat/group.html'):

    hero = heromanipulation.hero_init(request)
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero) != False
        combatmanipulation.is_combat(hero)
          
    if request.method == 'POST' and not in_combat:
        form = GroupForm(request.POST)
        if form.is_valid():
            combat = Combat(type=1,
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
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_group'))
    else:
        form = GroupForm()
        
    combats = Combat.objects.filter(type=1, is_active=0, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'form': form,
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

def combat_chaotic(request, template_name='combat/chaotic.html'):
    
    hero = heromanipulation.hero_init(request)
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero) != False
        combatmanipulation.is_combat(hero)
    
     
    if request.method == 'POST' and not in_combat:
        form = ChaoticForm(request.POST)
        if form.is_valid():
            combat = Combat(type=2,
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
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_chaotic'))
    else:
        form = ChaoticForm()
    
    combats = Combat.objects.filter(type=2, is_active=0, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'form': form,
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

def combat_territorial(request, template_name='combat/territorial.html'):
    
    hero = heromanipulation.hero_init(request)
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero) != False
        combatmanipulation.is_combat(hero)
    
    combats = Combat.objects.filter(type=3, is_active=1, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

def combat_current(request, template_name='combat/current.html'):
    
    hero = heromanipulation.hero_init(request)
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero) != False
        combatmanipulation.is_combat(hero)
    
    combats = Combat.objects.filter(is_active=1,
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'combats': combats,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

def cancel(request):
    
    hero = heromanipulation.hero_init(request)
    
    combat = combatmanipulation.is_cancel(hero)
    
    if combat != False:
        type = TYPES[combat.type][1].lower()
        combat.delete()
#
        messages.add_message(request, messages.SUCCESS, 'Your demand cancel.')
            
        return HttpResponseRedirect(reverse('combat_' + type))
    else:
        return HttpResponseRedirect(reverse('combat_duel'))     

def accept(request, id, team):
   
    hero = heromanipulation.hero_init(request)
    in_combat = combatmanipulation.in_combat(hero)
    
    if not in_combat:
        try:
            combat = Combat.objects.get(id=id)
        except Combat.DoesNotExist:
            return HttpResponseRedirect(reverse('combat_duel')) 
            
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
            messages.add_message(request, messages.SUCCESS, 'Demand accept.')
        else:
#
            messages.add_message(request, messages.ERROR, 
                                 'Demand accept until you.')
        return HttpResponseRedirect(reverse('combat_' + TYPES[combat.type][1] \
                                                                    .lower()))
    
    return HttpResponseRedirect(reverse('combat_duel'))

def refuse(request):
    
    hero = heromanipulation.hero_init(request)
    combat = combatmanipulation.is_refuse(hero)
    
    if combat != False:
        combat.combathero_set.get(team=1).delete()
#
        messages.add_message(request, messages.SUCCESS, 'Demand refuse.')
    return HttpResponseRedirect(reverse('combat_duel'))

def fight(request):
    
    hero = heromanipulation.hero_init(request)
    
    combat = combatmanipulation.is_refuse(hero)
    
    if combat != False:
        combat.is_active = 1
        combat.save()
        return HttpResponseRedirect(reverse('combat'))
    
    return HttpResponseRedirect(reverse('combat_duel'))
    
def combat(request, template_name='combat/combat.html'):
    
    hero = heromanipulation.hero_init(request)
    combat = combatmanipulation.in_combat(hero, 1)
    
    if combat == False:
        return HttpResponseRedirect(reverse('combat_duel'))
    
    team = combat.combathero_set.get(hero=hero).team
    
    if team == 0:    
        enemies = [ i.hero for i in combat.combathero_set.filter().exclude(team=team) if not combat.combatlog_set.filter(hero_one=hero, hero_two=i.hero, is_past=False, hero_two_wstrike=None) ]  
    else:
        enemies = [ i.hero for i in combat.combathero_set.filter().exclude(team=team) if not combat.combatlog_set.filter(hero_two=hero, hero_one=i.hero, is_past=False, hero_one_wstrike=None) ]
    enemy = enemies[0] if enemies else None
        
    form = CombatForm(hero.feature.strike_count, hero.feature.block_count, enemy.id if enemy else None)
    
    if request.method == 'POST':
        form = CombatForm(hero.feature.strike_count, hero.feature.block_count, enemy.id, request.POST)
        if form.is_valid():
            
            strikes = [ str(form.cleaned_data['strike'+str(strike)]) for strike in range(int(hero.feature.strike_count)) ]
            
            blocks = []
            if form.cleaned_data['block_head']: blocks.append('0')
            if form.cleaned_data['block_breast']: blocks.append('1')
            if form.cleaned_data['block_zone']: blocks.append('2')
            if form.cleaned_data['block_legs']: blocks.append('3')
            
            hero_two = Hero.objects.get(id=form.cleaned_data['hero_two_id'])
               
            try:
                if team == 0:
                    combatlog = combat.combatlog_set.filter(hero_one=hero, hero_two=hero_two, is_past=False).get()
                else:
                    combatlog = combat.combatlog_set.filter(hero_two=hero, hero_one=hero_two, is_past=False).get()
                combatmanipulation.write_log(combat, combatlog, team, hero, hero_two, strikes, blocks)
            except CombatLog.DoesNotExist:
                combatmanipulation.write_log(combat, None, team, hero, hero_two, strikes, blocks)

            return HttpResponseRedirect(reverse('combat'))
    
    variables = RequestContext(request, {'hero': hero,
                                         'hero_two': enemy,
                                         'form': form,
                                         'combat': combat})
    
    return render_to_response(template_name, variables)   