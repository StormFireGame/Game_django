from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from building.models import Building
from building.module.buyingup.models import BuildingBuyingup
from thing.models import Thing
from hero.models import HeroThing

from hero.manipulation import hero_init, in_given_location, HeroM
from building.manipulation import BuildingM

MODULE = 'buyingup'

@hero_init
def index(request, slug, template_name='building/module/buyingup/index.html'):
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
def view(request, slug, type,
         template_name='building/module/buyingup/view.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    herothings = hero.herothing_set.filter(dressed=False, away=False,
                                thing__type=eval('Thing.TYPE_' + type.upper()))
    
    percent = BuildingBuyingup.objects.get(building=building).percent
    
    variables = RequestContext(request, {'building': building,
                                         'herothings': herothings,
                                         'percent': percent})
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def sell(request, slug, herothing_id):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        herothing = hero.herothing_set.get(id=herothing_id, dressed=False,
                                           away=False)
    except (Building.DoesNotExist, HeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    percent = building.buildingbuyingup_set.get(building=building).percent
    
    hero.money += herothing.thing.price * (percent / 100)
    hero.save()
    
    herothing.delete()
    
    HeroM(hero).update_capacity()
#
    messages.add_message(request, messages.SUCCESS, 'You sell thing.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    