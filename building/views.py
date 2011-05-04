from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from building.models import Building

from hero.manipulation import hero_init
from building.manipulation import BuildingM

@hero_init
def index(request, slug, template_name='building/index.html'):
    
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    buildingm = BuildingM(building, hero)
    if not buildingm.is_near_building(slug):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

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

    buildingm.remove_from_location(slug)
    buildingm.add_to_location(slug)
    
    variables = RequestContext(request, {'building': building,
                                         'children': children,
                            'default_child_building': default_child_building,
                        'children_of_default_child': children_of_default_child,
                                         'parent': parent
                                         })
    
    return render_to_response(template_name, variables)