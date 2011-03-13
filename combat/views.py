from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Sum

from hero.models import Hero
from combat.models import Combat

from combat.forms import DuelForm, GroupForm, ChaoticForm, PastForm, \
                         CombatForm

from hero.heromanipulation import hero_init, hero_level_up, set_hp
from combat import combatmanipulation

import datetime

#Before combat
#Combat forms
@hero_init
def combat_duel(request, template_name='combat/duel.html'):
    
    hero = request.hero

    in_combat = combatmanipulation.in_combat(hero)

    is_cancel = is_fight = is_refuse = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero)
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
                            one_team_count=1, two_team_count=1)
            combat.save()
            combat.combathero_set.create(hero=hero)
#
            messages.add_message(request, messages.SUCCESS,
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_duel'))
    else:
        form = DuelForm()
    
    combats = Combat.objects.filter(type=Combat.TYPE_DUEL, 
                                    is_active=Combat.IS_ACTIVE_WAIT, 
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

@hero_init
def combat_group(request, template_name='combat/group.html'):

    hero = request.hero
    
    combatmanipulation.update_combats(Combat.TYPE_GROUP)
    if combatmanipulation.is_combat(hero):
        return HttpResponseRedirect(reverse('combat'))
    
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero)
          
    if request.method == 'POST' and not in_combat:
        form = GroupForm(request.POST)
        if form.is_valid():
            combat = Combat(type=Combat.TYPE_GROUP,
                            time_out=form.cleaned_data['time_out'],
                            injury=form.cleaned_data['injury'],
                            with_things=form.cleaned_data['with_things'],
                            time_wait=form.cleaned_data['time_wait'],
                            location=combatmanipulation.get_location(
                                                                hero.location),
                            one_team_count=form.cleaned_data['one_team_count'],
                            two_team_count=form.cleaned_data['two_team_count'],
                        one_team_lvl_min=form.cleaned_data['one_team_lvl_min'],
                        one_team_lvl_max=form.cleaned_data['one_team_lvl_max'],
                        two_team_lvl_min=form.cleaned_data['two_team_lvl_min'],
                        two_team_lvl_max=form.cleaned_data['two_team_lvl_max'])
            
            combat.save()
            combat.combathero_set.create(hero=hero)
#
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_group'))
    else:
        form = GroupForm()
        
    combats = Combat.objects.filter(type=Combat.TYPE_GROUP, 
                                    is_active=Combat.IS_ACTIVE_WAIT, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'form': form,
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def combat_chaotic(request, template_name='combat/chaotic.html'):
    
    hero = request.hero
    
    combatmanipulation.update_combats(Combat.TYPE_CHAOTIC)
    if combatmanipulation.is_combat(hero):
        return HttpResponseRedirect(reverse('combat'))
    
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero)    
     
    if request.method == 'POST' and not in_combat:
        form = ChaoticForm(request.POST)
        if form.is_valid():
            combat = Combat(type=Combat.TYPE_CHAOTIC,
                            time_out=form.cleaned_data['time_out'],
                            injury=form.cleaned_data['injury'],
                            with_things=form.cleaned_data['with_things'],
                            time_wait=form.cleaned_data['time_wait'],
                            location=combatmanipulation.get_location(
                                                            hero.location),
                            one_team_count=form.cleaned_data['count'],
                            one_team_lvl_min=form.cleaned_data['lvl_min'],
                            one_team_lvl_max=form.cleaned_data['lvl_max'])
            
            combat.save()
            combat.combathero_set.create(hero=hero)
#
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_chaotic'))
    else:
        form = ChaoticForm()
    
    combats = Combat.objects.filter(type=Combat.TYPE_CHAOTIC, 
                                    is_active=Combat.IS_ACTIVE_WAIT, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'form': form,
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def combat_territorial(request, template_name='combat/territorial.html'):
    
    hero = request.hero
    in_combat = combatmanipulation.in_combat(hero)
    
    is_cancel = False
    if in_combat:
        is_cancel = combatmanipulation.is_cancel(hero)
    
    combats = Combat.objects.filter(type=Combat.TYPE_TERRITORIAL, 
                                    is_active=Combat.IS_ACTIVE_WAIT, 
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'combats': combats,
                                         'in_combat': in_combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def combat_current(request, template_name='combat/current.html'):
    
    hero = request.hero
    
    is_cancel = combatmanipulation.is_cancel(hero)
        
    combats = Combat.objects.filter(is_active=Combat.IS_ACTIVE_FIGHT,
                                    location=combatmanipulation.get_location(
                                                                hero.location))
    
    variables = RequestContext(request, {'hero': hero, 
                                         'combats': combats,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def combat_past(request, template_name='combat/past.html'):
    
    hero = request.hero
    
    is_cancel = combatmanipulation.is_cancel(hero)
    
    combats = None
    if request.method == 'POST':
        form = PastForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            date_begin = form.cleaned_data['date_begin']
            date_end = form.cleaned_data['date_end']
            
            search_hero = Hero.objects.get(login=login)
            
            combats = Combat.objects.filter(is_active=Combat.IS_ACTIVE_PAST, 
                                            combathero__hero=search_hero, 
                                            start_date_time__gte=date_begin,
                                            start_date_time__lte=date_end)
    else:
        form = PastForm()
    
    variables = RequestContext(request, {'hero': hero,
                                         'form': form, 
                                         'combats': combats,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)
#End

#Combat actions
@hero_init
def cancel(request):
    
    hero = request.hero
    
    in_combat = combatmanipulation.in_combat(hero)
    is_cancel = combatmanipulation.is_cancel(hero)
    
    type = Combat.TYPES[in_combat.type][1].lower()
    if is_cancel != False:
        in_combat.delete()
#
        messages.add_message(request, messages.SUCCESS, 'Your demand cancel.')
    
    return HttpResponseRedirect(reverse('combat_' + type))

@hero_init
def accept(request, id, team):
   
    hero = request.hero
    in_combat = combatmanipulation.in_combat(hero)
    
    if not in_combat:
        try:
            combat = Combat.objects.filter(id=id, 
                                           is_active=Combat.IS_ACTIVE_WAIT). \
                                                                        get()
        except Combat.DoesNotExist:
            #
            messages.add_message(request, messages.ERROR, 'Fight is begin.')
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
        
        if hero.level >= team_lvl_min and hero.level <= team_lvl_max and \
           team_count_now < team_count:
            combat.combathero_set.create(hero=hero, team=team)
#
            messages.add_message(request, messages.SUCCESS, 'Demand accept.')
        else:
#
            messages.add_message(request, messages.ERROR, 
                                 'Demand accept until you.')
        return HttpResponseRedirect(reverse('combat_' + \
                                            Combat.TYPES[combat.type][1]. \
                                                                    lower()))
    
    return HttpResponseRedirect(reverse('combat_duel'))

#For duel only
@hero_init
def refuse(request):
    
    hero = request.hero
    combat = combatmanipulation.is_refuse(hero)
    
    if combat != False:
        combat.combathero_set.get(team=Combat.TEAM_FIRST).delete()
#
        messages.add_message(request, messages.SUCCESS, 'Demand refuse.')
    return HttpResponseRedirect(reverse('combat_duel'))

@hero_init
def fight(request):
    
    hero = request.hero
    
    combat = combatmanipulation.is_refuse(hero)
    
    if combat != False:
        combat.is_active = Combat.IS_ACTIVE_FIGHT
        combat.save()
        combatmanipulation.write_log_messages(combat, True)
        return HttpResponseRedirect(reverse('combat'))
    
    return HttpResponseRedirect(reverse('combat_duel'))
#End 
#End
#End

#Combat inside
@hero_init
def combat(request, template_name='combat/combat.html'):
    
    hero = request.hero
    combat = combatmanipulation.in_combat(hero, Combat.IS_ACTIVE_FIGHT)
    
    if not combat:
        return HttpResponseRedirect(reverse('combat_duel'))
        
    team = combat.combathero_set.get(hero=hero).team
    
    is_dead = combatmanipulation.is_dead(combat, hero)
    
    is_draw = combatmanipulation.is_draw(combat)
    is_win = combatmanipulation.is_win(combat, team, is_draw)
    is_lose = combatmanipulation.is_lose(combat, team, is_draw)
    
    enemy = form = all_experience = None
    is_timeout = is_next = False
    if is_dead == False and is_win == False and is_lose == False and \
       is_draw == False:
        cur_enemy_id_fn = None
        if request.method == 'POST':
            form = CombatForm(hero.feature.strike_count,
                              hero.feature.block_count, None, request.POST)

            if form.is_valid():
                
                if form.cleaned_data['next']:
                    cur_enemy_id_fn=form.cleaned_data['hero_two_id']
                else:
                    hero_two = Hero.objects. \
                                    get(id=form.cleaned_data['hero_two_id'])
                    if not combatmanipulation.is_dead(combat, hero_two):
                        strikes = \
                            [ str(form.cleaned_data['strike'+str(strike)]) \
                        for strike in range(int(hero.feature.strike_count)) ]
                        
                        blocks = []
                        if form.cleaned_data['block_head']: blocks.append('0')
                        if form.cleaned_data['block_breast']: 
                            blocks.append('1')
                        if form.cleaned_data['block_zone']: blocks.append('2')
                        if form.cleaned_data['block_legs']: blocks.append('3')
                        
                        combatlog = combatmanipulation.get_combat_log(combat,
                                                                      hero,
                                                                      hero_two,
                                                                      team)
                        combatmanipulation.write_log_strikes(combat,
                                                             combatlog,
                                                             team, hero,
                                                             hero_two,
                                                             strikes, blocks)
                        
                        return HttpResponseRedirect(reverse('combat'))
        
        enemies = combatmanipulation.get_enemies(combat, hero, team)
        enemy = combatmanipulation.get_enemy(enemies, cur_enemy_id_fn)
        if len(enemies) > 1:
            is_next = True
        
        form = CombatForm(hero.feature.strike_count, hero.feature.block_count,
                          enemy.id if enemy else None)
        if enemy == None:
            is_timeout = combatmanipulation.is_timeout(combat, team)
    else:
        if is_draw or is_win or is_lose:
            win_team = None
            if is_win:
                win_team = team
            elif is_lose:
                win_team = int(not team)
            combatmanipulation.write_log_messages(combat, is_finish=True,
                                                  win_team=win_team)
            
            if is_win:
                if team == Combat.TEAM_FIRST:
                    all_experience = combat.combatlog_set. \
                                                        filter(hero_one=hero) \
            .aggregate(Sum('hero_one_experience'))['hero_one_experience__sum']
                else:
                    all_experience = combat.combatlog_set. \
                                                        filter(hero_two=hero) \
            .aggregate(Sum('hero_two_experience'))['hero_two_experience__sum']
                
                if all_experience == None:
                    all_experience = 0

    if team == Combat.TEAM_FIRST:
        all_damage = combat.combatlog_set.filter(hero_one=hero). \
                    aggregate(Sum('hero_one_damage'))['hero_one_damage__sum']
    else:
        all_damage = combat.combatlog_set.filter(hero_two=hero). \
                    aggregate(Sum('hero_two_damage'))['hero_two_damage__sum']
    
    if all_damage == None:
        all_damage = 0
    
    variables = RequestContext(request, {'hero': hero,
                                         'hero_two': enemy,
                                         'form': form,
                                         'combat': combat,
                                         'combatlogs': combat.combatlog_set. \
                                                                        all(),
                                         'is_draw': is_draw,
                                         'is_win': is_win,
                                         'is_lose': is_lose,
                                         'is_dead': is_dead,
                                         'is_timeout': is_timeout,
                                         'is_next': is_next,
                                         'all_damage': all_damage,
                                         'all_experiance': all_experience})
    
    return render_to_response(template_name, variables)

@hero_init
def quit(request):
    
    hero = request.hero
    combat = combatmanipulation.in_combat(hero, Combat.IS_ACTIVE_FIGHT)
    
    combathero = combat.combathero_set.get(hero=hero)
    combathero.is_quit = True
    set_hp(hero)
    combathero.save()
    
    team = combat.combathero_set.get(hero=hero).team
    
    is_draw = combatmanipulation.is_draw(combat)
    is_win = combatmanipulation.is_win(combat, team, is_draw)
    
    if is_draw:
        hero.number_of_draws += 1
    elif is_win:
        if team == Combat.TEAM_FIRST:
            all_experience = combat.combatlog_set.filter(hero_one=hero). \
            aggregate(Sum('hero_one_experience'))['hero_one_experience__sum']
        else:
            all_experience = combat.combatlog_set.filter(hero_two=hero). \
            aggregate(Sum('hero_two_experience'))['hero_two_experience__sum']
        
        if all_experience == None:
            all_experience = 0
                
        hero.experience += all_experience
        hero.number_of_wins += 1
        
        hero_level_up(hero)
    else:
        hero.number_of_losses += 1
    hero.save()
    
    is_anybody_not_quit = combat.combathero_set.filter(is_quit=False).exists()
    if not is_anybody_not_quit:
        if is_win:
            combat.win_team = team
        elif not is_draw:
            combat.win_team = Combat.TEAM_FIRST if team else team
        combat.end_date_time = datetime.datetime.now()
        combat.is_active = Combat.IS_ACTIVE_PAST
        combat.save()
        
    return HttpResponseRedirect(reverse('hero'))

@hero_init
def victory(request):
    
    hero = request.hero
    combat = combatmanipulation.in_combat(hero, Combat.IS_ACTIVE_FIGHT)
    
    team = combat.combathero_set.get(hero=hero).team
    
    is_timeout = combatmanipulation.is_timeout(combat, team)
    
    if is_timeout == False:
        return HttpResponseRedirect(reverse('combat'))
    
    dead_heroes = []
    for combathero in combat.combathero_set.filter(is_dead=False). \
                                                            exclude(team=team):
        set_hp(combathero.hero, 0)
        combathero.is_dead = True
        combathero.save()
        dead_heroes.append({'hero': combathero.hero, 'team': combathero.team})
    
    combatmanipulation.after_death(combat, dead_heroes)
    
    return HttpResponseRedirect(reverse('combat'))
#End