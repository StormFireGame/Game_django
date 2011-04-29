from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from building.models import Building
from building.module.commission.models import BuildingCommissionHeroThing
from thing.models import Thing
from hero.models import HeroThing

from building.module.commission.forms import PutForm

from hero.manipulation import hero_init, in_given_location, HeroM
from building.manipulation import BuildingM

MODULE = 'commission'

@hero_init
def index(request, slug, 
          template_name='building/module/commission/index.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    buildingm = BuildingM(building, hero)

    if not buildingm.is_near_building(slug):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    buildingm.add_to_location(slug)

    variables = RequestContext(request, {'hero': hero,
                                         'building': building})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def view(request, slug, type,
         template_name='building/module/commission/view.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    commissionherothings = building.buildingcommissionherothing_set. \
        filter(herothing__thing__type=eval('Thing.TYPE_' + type.upper())). \
                                                exclude(herothing__hero=hero)

    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                'commissionherothings': commissionherothings})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def buy(request, slug, commissionherothing_id):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        commissionherothing = building.buildingcommissionherothing_set. \
                                                get(id=commissionherothing_id)
    except (Building.DoesNotExist, BuildingCommissionHeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    price = commissionherothing.price

    if hero.money < price:
#
        messages.add_message(request, messages.ERROR,
                             'You have not enough money.')
    else:

        percent = building.buildingcommission_set.get().percent

        hero.money -= price
        hero.save()

        commissionherothing.herothing.hero.money += price - \
                                            round((price * (percent / 100)))
        commissionherothing.herothing.hero.save()

        commissionherothing.herothing.away = False
        commissionherothing.herothing.hero = hero
        commissionherothing.herothing.save()

        commissionherothing.delete()

        HeroM(hero).update_capacity()
#
        messages.add_message(request, messages.SUCCESS, 'You buy thing.')
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Put
@hero_init
@in_given_location
def put(request, slug, template_name='building/module/commission/put.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
        
    herothings = hero.herothing_set.filter(dressed=False, away=False)
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def put_select(request, slug, herothing_id,
               template_name='building/module/commission/put_select.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        herothing = hero.herothing_set.get(id=herothing_id, dressed=False,
                                           away=False)
    except (Building.DoesNotExist, HeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if request.method == 'POST':
        form = PutForm(request.POST)
        if form.is_valid():
            herothing.away = True
            herothing.save()
            
            commissionherothing = building.buildingcommissionherothing_set. \
                                                    create(herothing=herothing,
                                            price=form.cleaned_data['price'])
            commissionherothing.save()
            
            HeroM(hero).update_capacity()
#
            messages.add_message(request, messages.SUCCESS, 'You put thing.')
            return HttpResponseRedirect(reverse('commission_put', args=[slug]))
    else:
        form = PutForm()
        
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothing': herothing,
                                         'form': form})
    
    return render_to_response(template_name, variables)
# End put

# Take
@hero_init
@in_given_location
def take(request, slug, template_name='building/module/commission/take.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    commissionherothings = building.buildingcommissionherothing_set. \
                                                filter(herothing__hero=hero)
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                'commissionherothings': commissionherothings})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def take_select(request, slug, commissionherothing_id):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        commissionherothing = building.buildingcommissionherothing_set. \
                                                get(id=commissionherothing_id)
    except (Building.DoesNotExist, BuildingCommissionHeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    commissionherothing.herothing.away = False
    commissionherothing.herothing.save()
    commissionherothing.delete()
    
    HeroM(hero).update_capacity()
#
    messages.add_message(request, messages.SUCCESS, 'You take thing.')
    return HttpResponseRedirect(reverse('commission_take', args=[slug]))
# End take