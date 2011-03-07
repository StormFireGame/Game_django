from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from island.models import Island, IslandPart

from island import islandmanipulation
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
    
    building = islandmanipulation.get_building(hero_position)
    
    variables = RequestContext(request, {'hero': hero, 
                                         'island': island,
                                         'building': building,
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
    else:
#
        messages.add_message(request, messages.ERROR, 'Take away your demand.')
    
    return HttpResponseRedirect(reverse('island'))