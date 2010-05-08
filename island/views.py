from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from hero.views import _is_login

from hero.models import Hero
from island.models import Island, IslandPart

from island import islandmanipulation
from combat import combatmanipulation

def island(request, id, template_name='island/island.html'):
    _is_login(request)
    
    island = get_object_or_404(Island, id=id)
    hero = Hero.objects.get(id=request.session['hero_id'])
    
    hero_position = islandmanipulation.get_hero_location(hero.location)
    hero_time_left = islandmanipulation.get_time_left(hero.location)
    
    variables = RequestContext(request, {'hero': hero, 
                                         'island': island,
                                         'hero_position_x': 
                                            (int(hero_position[0])),
                                         'hero_position_y': 
                                            (int(hero_position[1])),
                                         'hero_time_left': hero_time_left})
    
    return render_to_response(template_name, variables)

def move(request, id, coordinate_x, coordinate_y):
    _is_login(request)
    
    island = get_object_or_404(Island, id=id)
    hero = Hero.objects.get(id=request.session['hero_id'])
    
    
    if not islandmanipulation.get_time_left(hero.location) and \
                                        not combatmanipulation.in_combat(hero):
        try:
            island.islandpart_set.get(coordinate_x=coordinate_x, 
                                      coordinate_y=coordinate_y, 
                                      is_move=False)
        except IslandPart.DoesNotExist:
            hero.location = islandmanipulation.join_hero_location(hero.location, 
                                                                  coordinate_x, 
                                                                  coordinate_y)
            hero.save()
    
    if combatmanipulation.in_combat(hero):
#
        request.user.message_set.create(message='Take away your demand')
    
    return HttpResponseRedirect(reverse('island', args=[id]))