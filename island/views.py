from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from island.models import IslandPart
from bot.models import Bot
from combat.models import Combat
from building.models import Building

from island.manipulation import IslandM
from hero.manipulation import hero_init, in_given_location, HeroM
from building.manipulation import BuildingM
from combat.manipulation import CombatM

@hero_init
def island(request, template_name='island/island.html'):
    
    hero = request.hero
    herom = HeroM(hero)
    island = herom.get_island()
    islandm = IslandM(island)

    if not islandm.is_near_island(hero.location):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    BuildingM(None, hero).remove_from_location()

    hero_position = herom.get_position_on_island()
    hero_time_left = islandm.get_time_left_to_move(hero_position)

    x, y = hero_position[0], hero_position[1]
    buildings = Building.objects.filter(island=island,
                                        coordinate_x1__lte=x,
                                        coordinate_y1__lte=y,
                                        coordinate_x2__gte=x,
                                        coordinate_y2__gte=y)
    bots = Bot.objects.filter(island=island,
                              current_coordinate_x=x,
                              current_coordinate_y=y,
                              in_combat=False)
    
    variables = RequestContext(request, {'island': island,
                                         'buildings': buildings,
                                         'bots': bots,
                                         'hero_position_x': hero_position[0],
                                         'hero_position_y': hero_position[1],
                                         'hero_time_left': hero_time_left})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def move(request, coordinate_x, coordinate_y):
    
    hero = request.hero
    herom = HeroM(hero)
    island = herom.get_island()
    hero_position = herom.get_position_on_island()

    islandm = IslandM(island)
    if not islandm.is_can_make_step(coordinate_x, coordinate_y, hero_position):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if not herom.get_combat():
        if not islandm.get_time_left_to_move(hero_position):
            try:
                island.islandpart_set.get(coordinate_x=coordinate_x, 
                                          coordinate_y=coordinate_y, 
                                          is_move=False)
            except IslandPart.DoesNotExist:
                herom.update_position_on_island(coordinate_x, coordinate_y)
                islandm.update_bots_position(coordinate_x, coordinate_y)
                CombatM(None, hero).update_bots_in_combats(coordinate_x,
                                                           coordinate_y)
    else:
#
        messages.add_message(request, messages.ERROR, 'Take away your demand.')
    
    return HttpResponseRedirect(reverse('island'))

@hero_init
@in_given_location
def bot_attack(request, bot_id):
    hero = request.hero
    herom = HeroM(hero)
    hero_position = herom.get_position_on_island()

    try:
        bot = Bot.objects.get(id=bot_id)
    except Bot.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if bot.current_coordinate_x != hero_position[0] or \
        bot.current_coordinate_y != hero_position[1]:
#
        messages.add_message(request, messages.ERROR, 'Bot go away.')
        return HttpResponseRedirect(reverse('island'))

    if herom.get_combat():
#
        messages.add_message(request, messages.ERROR, 'Take away your demand.')
        return HttpResponseRedirect(reverse('island'))

    if not bot.in_combat:
        combat = Combat(type=Combat.TYPE_TERRITORIAL,
                        is_active=Combat.IS_ACTIVE_FIGHT,
                        location=herom.get_location())
        combat.save()
        combat.combatwarrior_set.create(hero=hero, team=Combat.TEAM_FIRST)
        combat.combatwarrior_set.create(bot=bot, team=Combat.TEAM_SECOND)
        
        bot.in_combat = True
        bot.save()
        
        CombatM(combat, hero).write_log_message(combat, True)
        return HttpResponseRedirect(reverse('combat'))
    else:
#
        messages.add_message(request, messages.ERROR, 'Bot in combat.')
        return HttpResponseRedirect(reverse('island'))