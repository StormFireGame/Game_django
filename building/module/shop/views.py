from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from building.models import Building
from building.module.shop.models import BuildingShopThing
from hero.models import HeroThing
from thing.models import Thing

from hero.heromanipulation import hero_init, update_capacity
from building import buildingmanipulation

PLUGIN = 'shop'

@hero_init
def index(request, slug, template_name='building/module/shop/index.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    variables = RequestContext(request, {'hero': hero,
                                         'building': building})
    
    buildingmanipulation.add_building_to_location(hero, building, slug)
    
    return render_to_response(template_name, variables)

@hero_init
def view(request, slug, type, template_name='building/module/shop/view.html'):
    building = Building.objects.get(slug=slug)
    
    type_num = [i[0] for i in Thing.TYPES if i[1].lower() == type][0]
    shopthings = BuildingShopThing.objects.filter(thing__type=type_num)
   
    variables = RequestContext(request, {'hero': request.hero,
                                         'building': building,
                                         'shopthings': shopthings})
    
    return render_to_response(template_name, variables)

@hero_init
def buy(request, slug, id):
    
    hero = request.hero
    shopthing = BuildingShopThing.objects.get(id=id)
    
    if shopthing.price > hero.money:
#
        messages.add_message(request, messages.ERROR, 
                             'You have not enough money.')
    elif not shopthing.count:
#
        messages.add_message(request, messages.ERROR, 
                             'Thing are not available.')
    else:
        HeroThing.objects.create(hero=hero, thing=shopthing.thing, 
                                 stability_all=shopthing.thing.stability,
                                 stability_left=shopthing.thing.stability)
        shopthing.count -= 1
        shopthing.save()
        hero.money -= shopthing.price
        hero.save()
        
        update_capacity(hero)
#
        messages.add_message(request, messages.SUCCESS, 'You buy thing.')

    return HttpResponseRedirect(reverse('shop', args=[slug]))