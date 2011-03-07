from django.shortcuts import render_to_response
from django.template import RequestContext

from building.models import Building

from hero.heromanipulation import hero_init
from building import buildingmanipulation

@hero_init
def index(request, slug, template_name='building/index.html'):
    
    hero = request.hero
    building = Building.objects.get(slug=slug)
    children = building.building_set.all()
    
    default_child_building = None
    for child in children:
        if child.default_child:
            default_child_building = child
            break
    children_of_default_child = None
    if default_child_building:
        children_of_default_child = default_child_building.building_set.all()
    
    if building.parent_id:
        parent = Building.objects.get(pk=building.parent_id)
    else:
        parent = None
    
    buildingmanipulation.remove_building_from_location(hero, slug)
    buildingmanipulation.add_building_to_location(hero, building, slug)
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'children': children,
                            'default_child_building': default_child_building,
                        'children_of_default_child': children_of_default_child,
                                         'parent': parent
                                         })
    
    return render_to_response(template_name, variables)