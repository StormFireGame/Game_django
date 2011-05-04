from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Sum
from django.conf import settings

from hero.models import Hero
from combat.models import Combat
from bot.models import Bot

from combat.forms import DuelForm, GroupForm, ChaoticForm, PastForm, \
                         CombatForm

from hero.manipulation import hero_init, HeroM
from combat.manipulation import CombatM

import datetime

# Before combat
# Combat forms
@hero_init
def duel(request, template_name='combat/duel.html'):

    hero = request.hero
    herom = HeroM(hero)
    combat = herom.get_combat(Combat.IS_ACTIVE_WAIT)

    is_cancel = is_fight = is_refuse = False
    if combat:
        combatm = CombatM(combat, hero)
        is_cancel = combatm.is_cancel()
        is_refuse = combatm.is_refuse()
        is_fight = combatm.is_fight()

    if request.method == 'POST' and not combat:
        form = DuelForm(request.POST)
        if form.is_valid():
            combat = Combat(type=Combat.TYPE_DUEL,
                            time_out=form.cleaned_data['time_out'],
                            injury=form.cleaned_data['injury'],
                            with_things=form.cleaned_data['with_things'],
                            location=herom.get_location(),
                            one_team_count=1, two_team_count=1)
            combat.save()
            combat.combatwarrior_set.create(hero=hero)
#
            messages.add_message(request, messages.SUCCESS,
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_duel'))
    else:
        form = DuelForm()

    combats = Combat.objects.filter(type=Combat.TYPE_DUEL,
                                    is_active=Combat.IS_ACTIVE_WAIT,
                                    location=herom.get_location())

    variables = RequestContext(request, {'form': form,
                                         'combats': combats,
                                         'in_combat': combat,
                                         'is_cancel': is_cancel,
                                         'is_fight': is_fight,
                                         'is_refuse': is_refuse})

    return render_to_response(template_name, variables)

@hero_init
def group(request, template_name='combat/group.html'):

    hero = request.hero
    herom = HeroM(hero)
    combat = herom.get_combat(Combat.IS_ACTIVE_WAIT)

    combatm = CombatM(combat, hero)

    combatm.update_combats(Combat.TYPE_GROUP)
    if combat and combatm.is_active():
        return HttpResponseRedirect(reverse('combat'))

    is_cancel = False
    if combat:
        is_cancel = combatm.is_cancel()
          
    if request.method == 'POST' and not combat:
        form = GroupForm(request.POST)
        if form.is_valid():
            combat = Combat(type=Combat.TYPE_GROUP,
                            time_out=form.cleaned_data['time_out'],
                            injury=form.cleaned_data['injury'],
                            with_things=form.cleaned_data['with_things'],
                            time_wait=form.cleaned_data['time_wait'],
                            location=herom.get_location(),
                            one_team_count=form.cleaned_data['one_team_count'],
                            two_team_count=form.cleaned_data['two_team_count'],
                        one_team_lvl_min=form.cleaned_data['one_team_lvl_min'],
                        one_team_lvl_max=form.cleaned_data['one_team_lvl_max'],
                        two_team_lvl_min=form.cleaned_data['two_team_lvl_min'],
                        two_team_lvl_max=form.cleaned_data['two_team_lvl_max'])
            
            combat.save()
            combat.combatwarrior_set.create(hero=hero)
#
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand create.')
            return HttpResponseRedirect(reverse('combat_group'))
    else:
        form = GroupForm()
        
    combats = Combat.objects.filter(type=Combat.TYPE_GROUP, 
                                    is_active=Combat.IS_ACTIVE_WAIT, 
                                    location=herom.get_location())
    
    variables = RequestContext(request, {'form': form,
                                         'combats': combats,
                                         'in_combat': combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def chaotic(request, template_name='combat/chaotic.html'):
    
    hero = request.hero
    herom = HeroM(hero)
    combat = herom.get_combat(Combat.IS_ACTIVE_WAIT)

    combatm = CombatM(combat, hero)
    
    combatm.update_combats(Combat.TYPE_CHAOTIC)
    if combat and combatm.is_active():
        return HttpResponseRedirect(reverse('combat'))
    
    is_cancel = False
    if combat:
        is_cancel = combatm.is_cancel()
     
    if request.method == 'POST' and not combat:
        form = ChaoticForm(request.POST)
        if form.is_valid():
            combat = Combat(type=Combat.TYPE_CHAOTIC,
                            time_out=form.cleaned_data['time_out'],
                            injury=form.cleaned_data['injury'],
                            with_things=form.cleaned_data['with_things'],
                            time_wait=form.cleaned_data['time_wait'],
                            location=herom.get_location(),
                            one_team_count=form.cleaned_data['count'],
                            one_team_lvl_min=form.cleaned_data['lvl_min'],
                            one_team_lvl_max=form.cleaned_data['lvl_max'])
            
            combat.save()
            combat.combatwarrior_set.create(hero=hero)
#
            messages.add_message(request, messages.SUCCESS, 
                                 'Your demand accept.')
            return HttpResponseRedirect(reverse('combat_chaotic'))
    else:
        form = ChaoticForm()
    
    combats = Combat.objects.filter(type=Combat.TYPE_CHAOTIC, 
                                    is_active=Combat.IS_ACTIVE_WAIT, 
                                    location=herom.get_location())
    
    variables = RequestContext(request, {'form': form,
                                         'combats': combats,
                                         'in_combat': combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def territorial(request, template_name='combat/territorial.html'):
    
    hero = request.hero
    herom = HeroM(hero)

    combat = herom.get_combat(Combat.IS_ACTIVE_WAIT)

    is_cancel = False
    if combat:
        is_cancel = CombatM(combat, hero).is_cancel()
    
    combats = Combat.objects.filter(type=Combat.TYPE_TERRITORIAL, 
                                    is_active=Combat.IS_ACTIVE_FIGHT, 
                                    location=herom.get_location())
    
    variables = RequestContext(request, {'combats': combats,
                                         'in_combat': combat,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def current(request, template_name='combat/current.html'):
    
    hero = request.hero
    herom = HeroM(hero)

    combat = herom.get_combat(Combat.IS_ACTIVE_WAIT)
    is_cancel = False
    if combat:
        is_cancel = CombatM(combat, hero).is_cancel()
        
    combats = Combat.objects.filter(is_active=Combat.IS_ACTIVE_FIGHT,
                                    location=herom.get_location())

    variables = RequestContext(request, {'combats': combats,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)

@hero_init
def past(request, template_name='combat/past.html'):
    
    hero = request.hero
    herom = HeroM(hero)

    combat = herom.get_combat(Combat.IS_ACTIVE_WAIT)

    is_cancel = False
    if combat:
        is_cancel = CombatM(combat, hero).is_cancel()
    
    combats = None
    if request.method == 'POST':
        form = PastForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            date_begin = form.cleaned_data['date_begin']
            date_end = form.cleaned_data['date_end']
            
            search_hero = Hero.objects.get(login=login)
            
            combats = Combat.objects.filter(is_active=Combat.IS_ACTIVE_PAST, 
                                            combatwarrior__hero=search_hero,
                                            start_date_time__gte=date_begin,
                                            start_date_time__lte=date_end)
    else:
        form = PastForm()
    
    variables = RequestContext(request, {'form': form,
                                         'combats': combats,
                                         'is_cancel': is_cancel})
    
    return render_to_response(template_name, variables)
# End combat form

# Combat actions
@hero_init
def cancel(request):
    
    hero = request.hero
    combat = HeroM(hero).get_combat(Combat.IS_ACTIVE_WAIT)
    if not combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    is_cancel = CombatM(combat, hero).is_cancel()
    
    if is_cancel:
        combat.delete()
#
        messages.add_message(request, messages.SUCCESS, 'Your demand cancel.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@hero_init
def accept(request, combat_id, team):
   
    hero = request.hero
    combat = HeroM(hero).get_combat(Combat.IS_ACTIVE_WAIT)

    if combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    try:
        combat = Combat.objects.filter(id=combat_id).get()
    except Combat.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if combat.is_active != Combat.IS_ACTIVE_WAIT:
#
        messages.add_message(request, messages.ERROR, 'Fight is begin.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if int(team) == Combat.TEAM_FIRST:
        team_count = combat.one_team_count
        team_lvl_min = combat.one_team_lvl_min
        team_lvl_max = combat.one_team_lvl_max
    else:
        team_count = combat.two_team_count
        team_lvl_min = combat.two_team_lvl_min
        team_lvl_max = combat.two_team_lvl_max

    team_count_now = combat.combatwarrior_set.filter(team=team).count()

    if (hero.level >= team_lvl_min and hero.level <= team_lvl_max) or \
       combat.type == Combat.TYPE_DUEL:
        if team_count_now < team_count:
            combat.combatwarrior_set.create(hero=hero, team=team)
#
            messages.add_message(request, messages.SUCCESS, 'Demand accept.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
#
            messages.add_message(request, messages.SUCCESS,
                                 'Demand accept until you.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

# For duel
@hero_init
def refuse(request):
    
    hero = request.hero
    combat = HeroM(hero).get_combat(Combat.IS_ACTIVE_WAIT)
    if not combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    is_refuse = CombatM(combat, hero).is_refuse()
    
    if is_refuse:
        combat.combatwarrior_set.get(team=Combat.TEAM_SECOND).delete()
#
        messages.add_message(request, messages.SUCCESS, 'Demand refuse.')
    return HttpResponseRedirect(reverse('combat_duel'))

@hero_init
def fight(request):
    
    hero = request.hero
    combat = HeroM(hero).get_combat(Combat.IS_ACTIVE_WAIT)
    if not combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    is_fight = CombatM(combat, hero).is_fight()

    if is_fight:
        combat.is_active = Combat.IS_ACTIVE_FIGHT
        combat.save()
        CombatM(combat, hero).write_log_message(True)
        return HttpResponseRedirect(reverse('combat'))
    
    return HttpResponseRedirect(reverse('combat_duel'))
# End for duel

@hero_init
def enter(request, combat_id, team):
    hero = request.hero

    combat = HeroM(hero).get_combat(Combat.IS_ACTIVE_WAIT)

    if combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    try:
        combat = Combat.objects.filter(id=combat_id).get()
    except Combat.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if combat.is_active != Combat.IS_ACTIVE_FIGHT:
#
        messages.add_message(request, messages.ERROR, 'Fight is end.')
        return HttpResponseRedirect(reverse('combat_territorial'))

    combat.combatwarrior_set.create(hero=hero, team=team, is_join=True)
    CombatM(combat, hero).write_log_message(is_join=True, hero=hero)

    return HttpResponseRedirect(reverse('combat'))
# End combat action
# End before combat

# Combat inside
@hero_init
def combat(request, template_name='combat/combat.html'):
    
    hero = request.hero
    combat = HeroM(hero).get_combat()

    combatm = CombatM(combat, hero)

    if not combat or not combatm.is_active():
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
        
    team = combat.combatwarrior_set.get(hero=hero).team
    
    is_dead = combatm.is_dead(hero)
    
    is_draw = combatm.is_draw()
    is_win = combatm.is_win(team, is_draw)
    is_lose = combatm.is_lose(team, is_draw)
    
    enemy = form = all_experience = None
    is_timeout = is_next = is_enemy_hero = False    
    if is_dead == False and is_win == False and is_lose == False and \
       is_draw == False:
        cur_enemy_id_fn = None
        if request.method == 'POST':
            form = CombatForm(hero.feature.strike_count,
                              hero.feature.block_count, None, None,
                              request.POST)
            
            if form.is_valid():
                if form.cleaned_data['next']:
                    cur_enemy_id_fn = form.cleaned_data['hero_two_id']
                else:
                    hero_two = bot = None
                    if form.cleaned_data['hero_two_id']:
                        try:
                            hero_two = Hero.objects. \
                                    get(id=form.cleaned_data['hero_two_id'])
                        except Hero.DoesNotExist:
                            return HttpResponseRedirect(reverse(
                                                    settings.URL_REVERSE_404))
                    else:
                        try:
                            bot = Bot.objects. \
                                            get(id=form.cleaned_data['bot_id'])
                        except Bot.DoesNotExist:
                            return HttpResponseRedirect(reverse(
                                                    settings.URL_REVERSE_404))
                        
                        if not combatm.is_warrior_in_combat(hero_two, bot):
                            return HttpResponseRedirect(reverse('combat'))

                    if not combatm.is_dead(hero_two, bot):
                        strikes = \
                            [ str(form.cleaned_data['strike'+str(strike)]) \
                        for strike in range(int(hero.feature.strike_count)) ]
                        
                        blocks = []
                        if form.cleaned_data['block_head']: blocks.append('0')
                        if form.cleaned_data['block_breast']: 
                            blocks.append('1')
                        if form.cleaned_data['block_zone']: blocks.append('2')
                        if form.cleaned_data['block_legs']: blocks.append('3')
                        
                        combatm.write_log_strikes(team, hero_two, bot, strikes,
                                                  blocks)
                        
                        return HttpResponseRedirect(reverse('combat'))

        is_bot_make_timeout = combatm.update_bots_timeout()
        if is_bot_make_timeout:
            combat.is_active = Combat.IS_ACTIVE_AFTER_FIGHT
            combat.save()
            return HttpResponseRedirect(reverse('combat'))

        enemies = combatm.get_enemies(team)
        enemy = combatm.get_enemy(enemies, cur_enemy_id_fn)
        is_enemy_hero = type(enemy) == Hero

        if len(enemies) > 1:
            is_next = True

        try:
            past_enemy_id = int(form.data['hero_two_id']) \
                                if is_enemy_hero else int(form.data['bot_id'])
        except:
            past_enemy_id = None

        if not past_enemy_id or past_enemy_id != enemy.id:
            form = CombatForm(hero.feature.strike_count,
                              hero.feature.block_count,
                              enemy.id if enemy and is_enemy_hero else None,
                            enemy.id if enemy and not is_enemy_hero else None)
        if enemy is None:
            is_timeout = combatm.is_timeout(team)
    else:
        if is_draw or is_win or is_lose:
            win_team = None
            if is_win:
                win_team = team
            elif is_lose:
                win_team = int(not team)
            combatm.write_log_message(is_finish=True, win_team=win_team)
            
            if is_win:
                if team == Combat.TEAM_FIRST:
                    all_experience = combat.combatlog_set. \
                                                        filter(hero_one=hero) \
    .aggregate(Sum('warrior_one_experience'))['warrior_one_experience__sum']
                else:
                    all_experience = combat.combatlog_set. \
                                                        filter(hero_two=hero) \
    .aggregate(Sum('warrior_two_experience'))['warrior_two_experience__sum']
                
                if all_experience == None:
                    all_experience = 0
            
            combatm.free_bots()
            
            if combat.is_active == Combat.IS_ACTIVE_FIGHT:
                combat.is_active = Combat.IS_ACTIVE_AFTER_FIGHT
                combat.save()
            
    if team == Combat.TEAM_FIRST:
        all_damage = combat.combatlog_set.filter(hero_one=hero). \
                aggregate(Sum('warrior_one_damage'))['warrior_one_damage__sum']
    else:
        all_damage = combat.combatlog_set.filter(hero_two=hero). \
                aggregate(Sum('warrior_two_damage'))['warrior_two_damage__sum']
    
    if all_damage == None:
        all_damage = 0

    variables = RequestContext(request, {'hero_two': enemy if is_enemy_hero \
                                                                    else None,
                                         'bot': enemy if not is_enemy_hero \
                                                                    else None,
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
    herom = HeroM(hero)

    combat = herom.get_combat(Combat.IS_ACTIVE_AFTER_FIGHT)

    if not combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    combatm = CombatM(combat, hero)
    
    combatwarrior = combat.combatwarrior_set.get(hero=hero)
    combatwarrior.is_quit = True
    herom.set_hp()
    combatwarrior.save()
    
    team = combat.combatwarrior_set.get(hero=hero).team
    
    is_draw = combatm.is_draw()
    is_win = combatm.is_win(team, is_draw)
    
    if is_draw:
        hero.number_of_draws += 1
    elif is_win:
        if team == Combat.TEAM_FIRST:
            all_experience = combat.combatlog_set.filter(hero_one=hero). \
        aggregate(Sum('warrior_one_experience'))['warrior_one_experience__sum']
        else:
            all_experience = combat.combatlog_set.filter(hero_two=hero). \
        aggregate(Sum('warrior_two_experience'))['warrior_two_experience__sum']
        
        if all_experience == None:
            all_experience = 0
                
        hero.experience += all_experience
        hero.number_of_wins += 1
        
        herom.level_up()
    else:
        hero.number_of_losses += 1
    hero.save()
    
    if not combatm.is_anybody_not_quit():
        if is_win:
            combat.win_team = team
        elif is_draw:
            combat.win_team = None
        else:
            combat.win_team = Combat.TEAM_FIRST if team else Combat.TEAM_SECOND
        combat.end_date_time = datetime.datetime.now()
        combat.is_active = Combat.IS_ACTIVE_PAST
        combat.save()
        
    return HttpResponseRedirect(reverse('hero'))

@hero_init
def victory(request):
    
    hero = request.hero
    combat = HeroM(hero).get_combat(Combat.IS_ACTIVE_FIGHT)

    if not combat:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    team = combat.combatwarrior_set.get(hero=hero).team

    combatm = CombatM(combat, hero)
    is_timeout = combatm.is_timeout(team)
    
    if not is_timeout:
        return HttpResponseRedirect(reverse('combat'))
    
    dead_warriors = []
    for combatwarrior in combat.combatwarrior_set.filter(is_dead=False). \
                                                            exclude(team=team):
        HeroM(combatwarrior.hero).set_hp(0)
        combatwarrior.is_dead = True
        combatwarrior.save()
        dead_warriors.append({'warrior': combatwarrior.hero, 
                              'team': combatwarrior.team})
    
    combatm.after_death(dead_warriors)
    
    combat.is_active = Combat.IS_ACTIVE_AFTER_FIGHT
    combat.save()
    return HttpResponseRedirect(reverse('combat'))
# End combat inside