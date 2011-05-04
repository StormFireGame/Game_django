from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from building.models import Building
from building.module.shop.models import BuildingShopThing
from hero.models import HeroThing
from thing.models import Thing

from hero.manipulation import hero_init, in_given_location, HeroM
from building.manipulation import BuildingM

MODULE = 'shop'

@hero_init
def index(request, slug, template_name='building/module/shop/index.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
            
    buildingm = BuildingM(building, hero)
        
    if not buildingm.is_near_building(slug):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    buildingm.add_to_location(slug)
    
    variables = RequestContext(request, {'building': building})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def view(request, slug, type, template_name='building/module/shop/view.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    shopthings = building.buildingshopthing_set. \
                        filter(thing__type=eval('Thing.TYPE_' + type.upper()))
   
    variables = RequestContext(request, {'building': building,
                                         'shopthings': shopthings})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def buy(request, slug, shopthing_id):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        shopthing = building.buildingshopthing_set.get(id=shopthing_id)
    except (Building.DoesNotExist, BuildingShopThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

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
        
        HeroM(hero).update_capacity()
#
        messages.add_message(request, messages.SUCCESS, 'You buy thing.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))