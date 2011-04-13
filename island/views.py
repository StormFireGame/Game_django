from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from island.models import Island, IslandPart
from bot.models import Bot
from combat.models import Combat

from island import islandmanipulation
from combat import combatmanipulation
from combat.combatmanipulation import in_combat
from hero.heromanipulation import hero_init
from building.buildingmanipulation import remove_building_from_location

@hero_init
def island(request, template_name='island/island.html'):
    
    hero = request.hero
    remove_building_from_location(hero)
    island = Island.objects.get(pk=islandmanipulation.get_island(hero))
    
    hero_position = islandmanipulation.get_hero_position(hero)
    hero_time_left = islandmanipulation.get_time_left_to_move(hero)
    
    buildings = islandmanipulation.get_buildings(hero_position)
    
    bots = islandmanipulation.get_bots(hero_position)
    
    variables = RequestContext(request, {'hero': hero, 
                                         'island': island,
                                         'buildings': buildings,
                                         'bots': bots,
                                         'hero_position_x': hero_position[0],
                                         'hero_position_y': hero_position[1],
                                         'hero_time_left': hero_time_left})
    
    return render_to_response(template_name, variables)

@hero_init
def move(request, coordinate_x, coordinate_y):
    
    hero = request.hero
    island = Island.objects.get(pk=islandmanipulation.get_island(hero))
    
    if not in_combat(hero):
        if not islandmanipulation.get_time_left_to_move(hero):
            try:
                island.islandpart_set.get(coordinate_x=coordinate_x, 
                                          coordinate_y=coordinate_y, 
                                          is_move=False)
            except IslandPart.DoesNotExist:
                islandmanipulation.join_hero_location(hero, coordinate_x, 
                                                      coordinate_y)
                islandmanipulation.update_bots_position(coordinate_x, 
                                                        coordinate_y)
                combatmanipulation.update_bots_timeout(coordinate_x, 
                                                       coordinate_y)
    else:
#
        messages.add_message(request, messages.ERROR, 'Take away your demand.')
    
    return HttpResponseRedirect(reverse('island'))

@hero_init
def bot_attack(request, bot_id):
    hero = request.hero
    hero_position = islandmanipulation.get_hero_position(hero)
    
    bot = Bot.objects.get(id=bot_id)
    
    if bot.current_coordinate_x != hero_position[0] or \
        bot.current_coordinate_y != hero_position[1]:
#
        messages.add_message(request, messages.ERROR, 'Bot go away.')
        return HttpResponseRedirect(reverse('island'))
        
    if not bot.in_combat:
        combat = Combat(type=Combat.TYPE_TERRITORIAL,
                        is_active=Combat.IS_ACTIVE_FIGHT,
                        location=combatmanipulation.get_location(hero.location))
        combat.save()
        combat.combatwarrior_set.create(hero=hero, team=Combat.TEAM_FIRST)
        combat.combatwarrior_set.create(bot=bot, team=Combat.TEAM_SECOND)
        
        bot.in_combat = True
        bot.save()
        
        combatmanipulation.write_log_message(combat, True)
        return HttpResponseRedirect(reverse('combat'))
    else:
#
        messages.add_message(request, messages.ERROR, 'Bot in combat.')
        return HttpResponseRedirect(reverse('island'))