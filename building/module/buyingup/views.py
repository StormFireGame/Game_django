from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from building.models import Building
from building.module.buyingup.models import BuildingBuyingup
from thing.models import Thing

from hero.heromanipulation import hero_init, update_capacity
from building import buildingmanipulation

PLUGIN = 'buyingup'

@hero_init
def index(request, slug, template_name='building/module/buyingup/index.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    variables = RequestContext(request, {'hero': hero,
                                         'building': building})
    
    buildingmanipulation.add_building_to_location(hero, building, slug)
    
    return render_to_response(template_name, variables)

@hero_init
def view(request, slug, type, template_name='building/module/buyingup/view.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    type_num = [i[0] for i in Thing.TYPES if i[1].lower() == type][0]
    herothings = hero.herothing_set.filter(dressed=False, away=False, 
                                           thing__type=type_num)
    
    percent = BuildingBuyingup.objects.get(building=building).percent
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings,
                                         'percent': percent})
    return render_to_response(template_name, variables)

@hero_init
def sell(request, slug, id):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    herothing = hero.herothing_set.get(id=id)
    
    percent = BuildingBuyingup.objects.get(building=building).percent
    
    hero.money += herothing.thing.price * (percent / 100)
    hero.save()
    
    herothing.delete()
    
    update_capacity(hero)
#
    messages.add_message(request, messages.SUCCESS, 'You sell thing.')
    
    return HttpResponseRedirect(reverse('buyingup', args=[slug]))

    